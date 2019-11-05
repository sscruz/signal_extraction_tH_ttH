#!/usr/bin/env python
import sys
import os
import re
import multiprocessing
import numpy as np
import glob

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


def runNLLScan(card, outfolder, kV, setratio=None, verbose=False, toysFile=None, blind=True):
    cv, ct, cosa, tag = parseName(card, printout=False)
    printout = "%-40s CV=%5.2f, Ct=%5.2f" % (os.path.basename(card), cv, ct)

    ratio = setratio or round(ct/cv, 3)
    filetag = "%s_kt_%s_kv_%s" % (tag, str(ratio*kV).replace("-","m").replace(".","p"), str(kV).replace("-","m").replace(".","p"))
    printout += ", Ratio=%7.4f: " % setratio

    if blind and 0 > 1:
        combinecmd_toys = "combine -M GenerateOnly  -t -1"
        combinecmd_toys += " -m 125 --verbose 0 -n _nll_scan_r1_%stoys" % (filetag)
        combinecmd_toys += " --setParameters kappa_t=%.2f,kappa_V=%.2f,kappa_tau=1.0,r=1,r_others=1" % (ratio*kV, kV)
        #combinecmd_toys += " --setParameters kappa_t=%.2f,kappa_V=%.2f,r=1" % (ratio*kV, kV)
        combinecmd_toys += " --freezeParameters r,r_others,kappa_t,kappa_V,"
        combinecmd_toys += "kappa_mu,kappa_b,kappa_c,"
        combinecmd_toys += "kappa_tau,kappa_mu,kappa_b,kappa_c,kappa_g,kappa_gam"
        #combinecmd_toys += "pdfindex_TTHHadronicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV"
        combinecmd_toys += " --saveToys "
        comboutput = runCombineCommand(combinecmd_toys, card, verbose=verbose, outfolder=outfolder)
        elapsed = parseOutput(comboutput)

    combinecmd = "combine -M MultiDimFit"
    #if blind :
    #    combinecmd += " -t -1"
    combinecmd += " --algo fixed --fixedPointPOIs r=0,r_others=1"
    combinecmd += " --rMin=0 --rMax=20 --X-rtd ADDNLL_RECURSIVE=0"
    combinecmd += " --cminDefaultMinimizerStrategy 0" # default is 1
    combinecmd += " --cminDefaultMinimizerTolerance 0.01" # default is 0.1
    combinecmd += " --cminPreScan" # default is off
    #combinecmd += " --X-rtd MINIMIZER_analytic" # trying out for aa toys
    #print(combinecmd)


    combinecmd += " -m 125 --verbose 0 -n _nll_scan_r1_%s" % (filetag)
    combinecmd += " --setParameters kappa_t=%.2f,kappa_V=%.2f,kappa_tau=1.0,r=1,r_others=1" % (ratio*kV, kV)
    #combinecmd += " --setParameters kappa_t=%.2f,kappa_V=%.2f,r=1" % (ratio*kV, kV)
    combinecmd += " --freezeParameters r,r_others,kappa_t,kappa_V,"
    combinecmd += "kappa_mu,kappa_b,kappa_c,"
    combinecmd += "kappa_tau,kappa_mu,kappa_b,kappa_c,kappa_g,kappa_gam"
    #combinecmd += "pdfindex_TTHHadronicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV"
    combinecmd += " --redefineSignalPOIs r"

    #if blind:
    #    #assert(os.path.isfile(toysFile)), "file not found %s" % toysFile
    #    combinecmd += " -t -1 " # + " --toysFile higgsCombine_nll_scan_r1_%stoys.GenerateOnly.mH125.*.root" % (filetag)


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
    #cards, runtag = processInputs(args, options)
    cards = glob.glob(options.cards + "/ws*.root")
    runtag = options.tag

    if options.toysFile:
        runtag += "_toys"
    if options.blind :
        runtag += "_blinded"
    csvfname = options.outputFolder + '/nll_scan%s.csv' % runtag
    pool = multiprocessing.Pool(processes=options.jobs)

    futures = []
    for card in cards:
        cv, ct, cosa, tag = parseName(card, printout=True)
        if not cosa == 1.0 and not options.cosa:
            print ("skipping CP scan by now")
            continue
        if not ct == 1 and options.cosa :
            print ("doing CP scan, skipping this one")
            continue
        ratio = round(ct/cv, 3)
        future = pool.apply_async(runNLLScan, (card,
                                               options.outputFolder,
                                               options.kV,
                                               ratio,
                                               options.printCommand,
                                               options.toysFile,
                                               options.blind))
        futures.append((card, ratio, future))

        if options.addValues:
            for added_val in ADD_RATIO_VALS.get(ratio):
                future = pool.apply_async(runNLLScan, (card,
                                                       options.outputFolder,
                                                       options.kV,
                                                       added_val,
                                                       options.printCommand,
                                                       options.toysFile,
                                                       options.blind))
                futures.append((card, added_val, future))

    with open(csvfname, 'w') as csvfile:
        rescalecv = options.kV
        csvfile.write('fname,cv,cf,cosa,rescalecv,rescalect,ratio,bestfitr,dnll\n')
        count=0
        for card, ratio, future in futures:
            count+=1
            cv, ct, cosa, tag = parseName(card, printout=False) # cosa,
            if not cosa == 1.0 and not options.cosa:
                print ("skipping CP scan by now")
                continue
            if not ct == 1 and options.cosa :
                print ("doing CP scan, skipping this one")
                continue
            bfr, dnll = future.get() # catch timeout?
            toparse = card.split("/")[len(card.split("/"))-1]
            rescalect = ratio*options.kV
            csvfile.write(','.join(map(str, [toparse, cv, ct, cosa, rescalecv, rescalect, ratio, bfr, dnll])) + '\n')
            count+=1

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
    parser.add_option("-c","--cards", dest="cards", type="string",
                      help="Folder with the workspaces, names as ws.*_kt_mXpX_kv_XpX*.root")
    parser.add_option("--addValues", dest="addValues", action='store_true',
                      help="Add three steps between each point for interpolation")
    parser.add_option("-o","--outputFolder", dest="outputFolder", type="string", default="",
                      help="where to save the outputs of combine run")
    parser.add_option("--kV", dest="kV", type="float", default=1.0,
                      help="KappaV to consider")
    parser.add_option("--cosa", dest="cosa", action='store_true', default=False,
                      help="if true only consider cards with cos(alpha)")
    (options, args) = parser.parse_args()

    sys.exit(main(args, options))
