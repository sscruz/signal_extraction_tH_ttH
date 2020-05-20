#!/usr/bin/env python
import os, shlex
from subprocess import Popen, PIPE
#from subprocess import Popen, PIPE

# python test/do_kt_scans.py --inputShapes /afs/cern.ch/work/a/acarvalh/CMSSW_10_2_10/src/data_tth/prepareDatacards_1l_2tau_mvaOutput_plainKin_SUM_VT_noRebin_noNeg.root --channel 1l_2tau --cardFolder testPlots_master10X
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--inputShapes",    type="string",       dest="inputShapes", help="Full path of prepareDatacards.root")
(options, args) = parser.parse_args()

def get_tH_weight_str(kt, kv, cosa = -10):
    if cosa == -10 :
        return ("kt_%.3g_kv_%.3gA" % (kt, kv)).replace('.', 'p').replace('-', 'm').replace('kv_1A', 'kv_1p0A').replace('kv_1_', 'kv_1p0_').replace('_1_', '_1p0_').replace('_2_', '_2p0_').replace('_3_', '_3p0_').replace('_0_', '_0p0_').replace('_m1_', '_m1p0_').replace('_m2_', '_m2p0_').replace('_m3_', '_m3p0_')
    else :
        return ("kt_%.3g_kv_%s_cosa_%s" % (kt, str(kv), str(cosa))).replace('.', 'p').replace('-', 'm')

def runCombineCmd(combinecmd, outfolder=".", saveout=None):
    print ("Command: ", combinecmd)
    try:
        p = Popen(shlex.split(combinecmd) , stdout=PIPE, stderr=PIPE, cwd=outfolder)
        comboutput = p.communicate()[0]
    except OSError:
        print ("command not known\n", combinecmd)
        comboutput = None
    if not saveout == None :
        saveTo = outfolder + "/" + saveout
        with open(saveTo, "w") as text_file:
            text_file.write(comboutput)
        print ("Saved result to: " + saveTo)
    print ("\n")
    return comboutput

def run_cmd(command):
  print ("executing command = '%s'" % command)
  p = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
  stdout, stderr = p.communicate()
  print (stderr)
  return stdout

inputShapes = options.inputShapes

tHweights = [
  {"kt" : -1.0, "kv" : 1.0, "cosa" : -10}, # the default (i.e. no weight)
  {"kt" : -3.0, "kv" : 1.0, "cosa" : -10},
  {"kt" : -2.0, "kv" : 1.0, "cosa" : -10},
  {"kt" : -1.5, "kv" : 1.0, "cosa" : -10},
  {"kt" : -1.25, "kv" : 1.0, "cosa" : -10},
  {"kt" : -0.75, "kv" : 1.0, "cosa" : -10},
  {"kt" : -0.5, "kv" : 1.0, "cosa" : -10},
  {"kt" : -0.25, "kv" : 1.0, "cosa" : -10},
  {"kt" : 0.0, "kv" : 1.0, "cosa" : -10},
  {"kt" : 0.25, "kv" : 1.0, "cosa" : -10},
  {"kt" : 0.5, "kv" : 1.0, "cosa" : -10},
  {"kt" : 0.75, "kv" : 1.0, "cosa" : -10},
  {"kt" : 1.0, "kv" : 1.0, "cosa" : -10},
  {"kt" : 1.25, "kv" : 1.0, "cosa" : -10},
  {"kt" : 1.5, "kv" : 1.0, "cosa" : -10},
  {"kt" : 2.0, "kv" : 1.0, "cosa" : -10},
  {"kt" : 3.0, "kv" : 1.0, "cosa" : -10},
  {"kt" : -2.0, "kv" : 1.5, "cosa" : -10},
  {"kt" : -1.25, "kv" : 1.5, "cosa" : -10},
  {"kt" : -1.0, "kv" : 1.5, "cosa" : -10},
  {"kt" : -0.5, "kv" : 1.5, "cosa" : -10},
  {"kt" : -0.25, "kv" : 1.5, "cosa" : -10},
  {"kt" : 0.25, "kv" : 1.5, "cosa" : -10},
  {"kt" : 0.5, "kv" : 1.5, "cosa" : -10},
  {"kt" : 1.0, "kv" : 1.5, "cosa" : -10},
  {"kt" : 1.25, "kv" : 1.5, "cosa" : -10},
  {"kt" : 2.0, "kv" : 1.5, "cosa" : -10},
  {"kt" : -3.0, "kv" : 0.5, "cosa" : -10},
  {"kt" : -2.0, "kv" : 0.5, "cosa" : -10},
  {"kt" : -1.25, "kv" : 0.5, "cosa" : -10},
  {"kt" : 1.25, "kv" : 0.5, "cosa" : -10},
  {"kt" : 2.0, "kv" : 0.5, "cosa" : -10},
  {"kt" : 3.0, "kv" : 0.5, "cosa" : -10},
  #{"kt" : 1.0, "kv" : -1.1111, "cosa" : -0.9},
  #{"kt" : 1.0, "kv" : -1.25, "cosa" : -0.8},
  #{"kt" : 1.0, "kv" : -1.42857, "cosa" : -0.7},
  #{"kt" : 1.0, "kv" : -1.6667, "cosa" : -0.6},
  #{"kt" : 1.0, "kv" : -2, "cosa" : -0.5},
  #{"kt" : 1.0, "kv" : -2.5, "cosa" : -0.4},
  #{"kt" : 1.0, "kv" : -3.333, "cosa" : -0.3},
  #{"kt" : 1.0, "kv" : -5, "cosa" : -0.2},
  #{"kt" : 1.0, "kv" : -10, "cosa" : -0.1},
  #{"kt" : 1.0, "kv" : -10000, "cosa" : 0.0001},
  #{"kt" : 1.0, "kv" : 10, "cosa" : 0.1},
  #{"kt" : 1.0, "kv" : 5, "cosa" : 0.2},
  #{"kt" : 1.0, "kv" : 3.333, "cosa" : 0.3},
  #{"kt" : 1.0, "kv" : 2.5, "cosa" : 0.4},
  #{"kt" : 1.0, "kv" : 2, "cosa" : 0.5},
  #{"kt" : 1.0, "kv" : 1.6667, "cosa" : 0.6},
  #{"kt" : 1.0, "kv" : 1.42857, "cosa" : 0.7},
  #{"kt" : 1.0, "kv" : 1.25, "cosa" : 0.8},
  #{"kt" : 1.0, "kv" : 1.1111, "cosa" : 0.9}
]

list_couplings = [
  {
    "name" : get_tH_weight_str(entry["kt"], entry["kv"], entry["cosa"]), "ratio" : entry["kt"]/entry["kv"]
  } for entry in tHweights
]

for ee, entry in enumerate(list_couplings) :
    cmd = "cd %s; combineCards.py  " % inputShapes
    couplingsName = entry["name"].replace("A", "")
    for era in ["2018", "2017", "2016"] :
        cmd += " ttH_0l_2tau_%s=ttH_0l_2tau_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2l_2tau_%s=ttH_2l_2tau_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_1tau_%s=ttH_3l_1tau_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_1l_1tau_%s=ttH_1l_1tau_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2los_1tau_%s=ttH_2los_1tau_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_1l_2tau_%s=ttH_1l_2tau_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_1tau_tH_%s=ttH_2lss_1tau_tH_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_1tau_ttH_%s=ttH_2lss_1tau_ttH_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_1tau_rest_%s=ttH_2lss_1tau_rest_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_rest_eee_%s=ttH_3l_0tau_rest_eee_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_rest_emm_bl_%s=ttH_3l_0tau_rest_emm_bl_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_rest_eem_bl_%s=ttH_3l_0tau_rest_eem_bl_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_rest_mmm_bl_%s=ttH_3l_0tau_rest_mmm_bl_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_rest_emm_bt_%s=ttH_3l_0tau_rest_emm_bt_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_rest_eem_bt_%s=ttH_3l_0tau_rest_eem_bt_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_rest_mmm_bt_%s=ttH_3l_0tau_rest_mmm_bt_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_tH_bl_%s=ttH_3l_0tau_tH_bl_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_tH_bt_%s=ttH_3l_0tau_tH_bt_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_ttH_bl_%s=ttH_3l_0tau_ttH_bl_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_3l_0tau_ttH_bt_%s=ttH_3l_0tau_ttH_bt_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_4l_%s=ttH_4l_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_ee_Restnode_%s=ttH_2lss_0tau_ee_Restnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_em_Restnode_%s=ttH_2lss_0tau_em_Restnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_mm_Restnode_%s=ttH_2lss_0tau_mm_Restnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_ee_tHQnode_%s=ttH_2lss_0tau_ee_tHQnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_em_tHQnode_%s=ttH_2lss_0tau_em_tHQnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_mm_tHQnode_%s=ttH_2lss_0tau_mm_tHQnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_ee_ttHnode_%s=ttH_2lss_0tau_ee_ttHnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_em_ttHnode_%s=ttH_2lss_0tau_em_ttHnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_mm_ttHnode_%s=ttH_2lss_0tau_mm_ttHnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_ee_ttWnode_%s=ttH_2lss_0tau_ee_ttWnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_em_ttWnode_%s=ttH_2lss_0tau_em_ttWnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_2lss_0tau_mm_ttWnode_%s=ttH_2lss_0tau_mm_ttWnode_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_cr_4l_%s=ttH_cr_4l_%s_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_cr_3l_%s_eee_cr=ttH_cr_3l_%s_eee_cr_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_cr_3l_%s_eem_cr=ttH_cr_3l_%s_eem_cr_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_cr_3l_%s_emm_cr=ttH_cr_3l_%s_emm_cr_%s.txt" % (era, era, couplingsName)
        cmd += " ttH_cr_3l_%s_mmm_cr=ttH_cr_3l_%s_mmm_cr_%s.txt" % (era, era, couplingsName)
    cmd += " > combo_ttHmultilep_%s.txt" % couplingsName
    #cmd += " > combo_tau_%s.txt" % couplingsName
    #print (cmd)
    #runCombineCmd(cmd, inputShapes)
    run_cmd(cmd)
