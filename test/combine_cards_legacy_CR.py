#!/usr/bin/env python
import os, shlex
from subprocess import Popen, PIPE

from optparse import OptionParser
parser = OptionParser()
parser.add_option(
    "--inputShapes",
    type="string",
    dest="inputShapes",
    help="Full path of prepareDatacards.root"
    )
parser.add_option(
    "--per_year",
    action="store_true",
    dest="per_year",
    help="self-explaining",
    default=False
    )
(options, args) = parser.parse_args()

def run_cmd(command):
  print ("executing command = '%s'" % command)
  p = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
  stdout, stderr = p.communicate()
  return stdout

inputShapes = options.inputShapes

if not options.per_year :
    cmd = "cd %s; combineCards.py  " % inputShapes

for era in ["2018", "2017", "2016"] :
    if options.per_year :
        cmd = "cd %s; combineCards.py  " % inputShapes
    cmd += " ttH_1l_2tau_%s=ttH_1l_2tau_SS_mTTVis_%s.txt" % (era, era)
    cmd += " ttH_cr_4l_%s=ttH_cr_4l_%s.txt" % (era, era)
    cmd += " ttH_2lss_3j_%s_ee=ttH_2lss_3j_%s_ee.txt" % (era, era)
    cmd += " ttH_2lss_3j_%s_em_pos=ttH_2lss_3j_%s_em_pos.txt" % (era, era)
    cmd += " ttH_2lss_3j_%s_mm_pos=ttH_2lss_3j_%s_mm_pos.txt" % (era, era)
    cmd += " ttH_2lss_3j_%s_em_neg=ttH_2lss_3j_%s_em_neg.txt" % (era, era)
    cmd += " ttH_2lss_3j_%s_mm_neg=ttH_2lss_3j_%s_mm_neg.txt" % (era, era)
    cmd += " ttH_cr_3l_%s_eem_cr=ttH_cr_3l_%s_eem_cr.txt" % (era, era)
    cmd += " ttH_cr_3l_%s_mmm_cr=ttH_cr_3l_%s_mmm_cr.txt" % (era, era)
    cmd += " ttH_cr_3l_%s_eee_cr=ttH_cr_3l_%s_eee_cr.txt" % (era, era)
    cmd += " ttH_cr_3l_%s_emm_cr=ttH_cr_3l_%s_emm_cr.txt" % (era, era)
    if options.per_year :
        cmd += " > combo_ttHmultilep_CRs_%s.txt" % era
        run_cmd(cmd)
        #print (cmd)
if not options.per_year :
    cmd += " > combo_ttHmultilep_CRs.txt" #% era
    #print (cmd)
    run_cmd(cmd)
