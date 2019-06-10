#!/usr/bin/env python
import sys
import os
import re
import multiprocessing
import numpy as np

from ROOT import TFile

from runAllLimits import runCombineCommand
from runAllLimits import parseName
from runAllLimits import setParamatersFreezeAll
from runAllLimits import processInputs

## type 2

def parseOutput(comboutput):
    for line in comboutput.split('\n'):
        if "WARNING: MultiDimFit failed" in line:
            print "\033[91mFit Failed\033[0m"
        m = re.match(r'Done in [\d\.]+ min \(cpu\), ([\d\.]*) min \(real\)', line)
        if not m:
            continue

        return float(m.group(1))

    print "\033[91mFailed to parse output\033[0m"
    return None


def getNLLFromRootFile(rfilename):
    tf = TFile.Open(rfilename, 'read')
    tree = tf.Get("limit")
    if not tree:
        raise RuntimeError("Unable to read limit tree from file %s" % rfilename)

    data = [(float(e.r), float(e.deltaNLL)) for e in tree]
    tf.Close()

    assert(len(data) == 2 and len(data[0]) == 2 and len(data[1]) == 2), "something wrong? %s" % rfilename
    return data


def runNLLScan(card, outfolder, setratio=None, verbose=False, toysFile=None, blind=True):
    cv, ct, tag = parseName(card, printout=False)
    printout = "%-40s CV=%5.2f, Ct=%5.2f" % (os.path.basename(card), cv, ct)
    combinecmd = "combine -M MultiDimFit --algo fixed --fixedPointPOIs r=0,r_others=0"
    combinecmd += " --rMin=0 --rMax=20 --X-rtd ADDNLL_RECURSIVE=0"
    combinecmd += " --cminDefaultMinimizerStrategy 0" # default is 1
    combinecmd += " --cminDefaultMinimizerTolerance 0.01" # default is 0.1
    combinecmd += " --cminPreScan" # default is off
    # combinecmd += " --X-rtd MINIMIZER_analytic" # trying out for aa toys

    ratio = setratio or round(ct/cv, 3)
    filetag = "%s_%s" % (tag, str(ratio))
    printout += ", Ratio=%7.4f: " % setratio
    combinecmd += " -m 125 --verbose 0 -n _nll_scan_r1_%s" % (filetag)
    if blind :
        combinecmd += " -t -1 " 
    combinecmd += " --setParameters kappa_t=%.2f,kappa_V=1.0,r=1,r_others=1" % ratio
    combinecmd += " --freezeParameters r,r_others,kappa_t,kappa_V,"
    combinecmd += "kappa_tau,kappa_mu,kappa_b,kappa_c,kappa_g,kappa_gam,"
    combinecmd += "pdfindex_TTHHadronicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV"
    combinecmd += " --redefineSignalPOIs r"

    if toysFile:
        assert(os.path.isfile(toysFile)), "file not found %s" % toysFile
        combinecmd += " -t -1 --toysFile %s" % toysFile

    print (combinecmd)
    comboutput = runCombineCommand(combinecmd, card, verbose=verbose, outfolder=outfolder)
    elapsed = parseOutput(comboutput)
    try:
        data = getNLLFromRootFile(outfolder + "/higgsCombine_nll_scan_r1_%s.MultiDimFit.mH125.root" % filetag)
        printout += "r=%5.2f, dNLL=%+7.3f " % (data[0][0], data[1][1])
    except AssertionError, IndexError:
        return np.nan, np.nan

    printout += "  \033[92mDone\033[0m in %.2f min" % elapsed
    print printout

    return (data[0][0], data[1][1])


def main(args, options):
    cards, runtag = processInputs(args, options)

    if options.toysFile:
        runtag += "_toys"
    if options.blind : 
        runtag += "_blinded"
    csvfname = options.outputFolder + '/nll_scan%s.csv' % runtag
    pool = multiprocessing.Pool(processes=options.jobs)

    futures = []
    for card in cards:
        cv, ct, tag = parseName(card, printout=True)
        ratio = round(ct/cv, 3)
        future = pool.apply_async(runNLLScan, (card,
                                               options.outputFolder,
                                               ratio,
                                               options.printCommand,
                                               options.toysFile,
                                               options.blind))
        futures.append((card, ratio, future))

        if options.addValues:
            for added_val in ADD_RATIO_VALS.get(ratio):
                future = pool.apply_async(runNLLScan, (card,
                                                       options.outputFolder,
                                                       added_val,
                                                       options.printCommand,
                                                       options.toysFile,
                                                       options.blind))
                futures.append((card, added_val, future))

    with open(csvfname, 'w') as csvfile:
        csvfile.write('fname,cv,cf,ratio,bestfitr,dnll\n')
        for card, ratio, future in futures:
            cv, ct, tag = parseName(card, printout=False)
            bfr, dnll = future.get() # catch timeout?
            csvfile.write(','.join(map(str, [card, cv, ct, ratio, bfr, dnll])) + '\n')

        csvfile.write('\n')

    print "...wrote results to %s" % csvfname

    return 0

if __name__ == '__main__':
    from optparse import OptionParser
    usage = """
    %prog [options] dir/
    %prog [options] card.txt
    %prog [options] workspace1.root workspace2.root

    Call combine on all datacards ("*.card.txt") in an input directory.
    Run MultiDimFit with --algo fixed and --fixedPointPOIs r=1 and r=0


    Note that you need to have 'combine' in your path. Try:
    cd /afs/cern.ch/user/s/stiegerb/combine707/ ; cmsenv ; cd -
    """
    parser = OptionParser(usage=usage)
    parser.add_option("-t","--tag", dest="tag", type="string", default=None,
                      help="Tag to put in name of output csv files")
    parser.add_option("-j","--jobs", dest="jobs", type="int", default=1,
                      help="Number of jobs to run in parallel")
    parser.add_option("--toysFile", dest="toysFile", type="string", default=None,
                      help="File from which to read toys for expected nll")
    parser.add_option("-p","--printCommand", dest="printCommand", action='store_true',
                      help="Print the combine command that is run")
    parser.add_option("-b","--blind", dest="blind", action='store_true',
                      help="Print the combine command that is run")
    parser.add_option("--addValues", dest="addValues", action='store_true',
                      help="Add three steps between each point for interpolation")
    parser.add_option("-o","--outputFolder", dest="outputFolder", type="string", default="",
                      help="where to save the outputs of combine run")
    (options, args) = parser.parse_args()

    sys.exit(main(args, options))
