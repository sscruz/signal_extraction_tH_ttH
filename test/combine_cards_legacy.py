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
    cmd += " ttH_0l_2tau_%s=ttH_0l_2tau_%s.txt" % (era, era)
    cmd += " ttH_2l_2tau_%s=ttH_2l_2tau_%s.txt" % (era, era)
    cmd += " ttH_3l_1tau_%s=ttH_3l_1tau_%s.txt" % (era, era)
    cmd += " ttH_1l_1tau_%s=ttH_1l_1tau_%s.txt" % (era, era)
    cmd += " ttH_2los_1tau_%s=ttH_2los_1tau_%s.txt" % (era, era)
    cmd += " ttH_1l_2tau_%s=ttH_1l_2tau_%s.txt" % (era, era)
    cmd += " ttH_2lss_1tau_tH_%s=ttH_2lss_1tau_tH_%s.txt" % (era, era)
    cmd += " ttH_2lss_1tau_ttH_%s=ttH_2lss_1tau_ttH_%s.txt" % (era, era)
    cmd += " ttH_2lss_1tau_rest_%s=ttH_2lss_1tau_rest_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_rest_eee_%s=ttH_3l_0tau_rest_eee_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_rest_emm_bl_%s=ttH_3l_0tau_rest_emm_bl_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_rest_eem_bl_%s=ttH_3l_0tau_rest_eem_bl_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_rest_mmm_bl_%s=ttH_3l_0tau_rest_mmm_bl_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_rest_emm_bt_%s=ttH_3l_0tau_rest_emm_bt_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_rest_eem_bt_%s=ttH_3l_0tau_rest_eem_bt_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_rest_mmm_bt_%s=ttH_3l_0tau_rest_mmm_bt_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_tH_bl_%s=ttH_3l_0tau_tH_bl_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_tH_bt_%s=ttH_3l_0tau_tH_bt_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_ttH_bl_%s=ttH_3l_0tau_ttH_bl_%s.txt" % (era, era)
    cmd += " ttH_3l_0tau_ttH_bt_%s=ttH_3l_0tau_ttH_bt_%s.txt" % (era, era)
    cmd += " ttH_4l_%s=ttH_4l_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_ee_Restnode_%s=ttH_2lss_0tau_ee_Restnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_em_Restnode_%s=ttH_2lss_0tau_em_Restnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_mm_Restnode_%s=ttH_2lss_0tau_mm_Restnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_ee_tHQnode_%s=ttH_2lss_0tau_ee_tHQnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_em_tHQnode_%s=ttH_2lss_0tau_em_tHQnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_mm_tHQnode_%s=ttH_2lss_0tau_mm_tHQnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_ee_ttHnode_%s=ttH_2lss_0tau_ee_ttHnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_em_ttHnode_%s=ttH_2lss_0tau_em_ttHnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_mm_ttHnode_%s=ttH_2lss_0tau_mm_ttHnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_ee_ttWnode_%s=ttH_2lss_0tau_ee_ttWnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_em_ttWnode_%s=ttH_2lss_0tau_em_ttWnode_%s.txt" % (era, era)
    cmd += " ttH_2lss_0tau_mm_ttWnode_%s=ttH_2lss_0tau_mm_ttWnode_%s.txt" % (era, era)
    cmd += " ttH_cr_4l_%s=ttH_cr_4l_%s.txt" % (era, era)
    cmd += " ttH_cr_3l_%s_eee_cr=ttH_cr_3l_%s_eee_cr.txt" % (era, era)
    cmd += " ttH_cr_3l_%s_eem_cr=ttH_cr_3l_%s_eem_cr.txt" % (era, era)
    cmd += " ttH_cr_3l_%s_emm_cr=ttH_cr_3l_%s_emm_cr.txt" % (era, era)
    cmd += " ttH_cr_3l_%s_mmm_cr=ttH_cr_3l_%s_mmm_cr.txt" % (era, era)
    if options.per_year :
        cmd += " > combo_ttHmultilep_%s.txt" % era
        run_cmd(cmd)
        print (cmd)
if not options.per_year :
    cmd += " > combo_ttHmultilep.txt" #% era
    print (cmd)
    run_cmd(cmd)
