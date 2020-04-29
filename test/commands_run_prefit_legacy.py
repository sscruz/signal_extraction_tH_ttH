#!/usr/bin/env python
import os, shlex
from subprocess import Popen, PIPE
import fileinput
from optparse import OptionParser

parser = OptionParser()
parser.add_option(
    "--cards_dir",
    type="string",
    dest="cards_dir",
    help="Full path of where the original datacards.txt/root are (to take templates)"
    )
parser.add_option(
    "--odir",
    type="string",
    dest="odir",
    help="Full path of where to put the plots -- it will create if not existent. If it is not given it will save the plots on 'cards_dir'/results",
    default="none"
    )
parser.add_option(
    "--unblinded",
    type="string",
    dest="unblinded",
    help="Overwrite the option on the cards/options.dat\n Chose between True / False / No\n --> 'No' does not overwrite what is already set in cards/options.dat",
    default="No"
    )
parser.add_option(
    "--do_only_cat",
    type="string",
    dest="do_only_cat",
    help="Self explanatory / No\n --> 'No' means that do all categories. See keys of plots_to_do_MVA for categories inside.",
    default="No"
    )
(options, args) = parser.parse_args()

print ("In the cards/options.dat you need to attemt too the following options: \n")

print ("blinded             = False ## use -t -1 --> It will be overwriten if you use the command line")
print ("doWS                = True ## To do any of the rest you must have ran with this being True once")
print ("preparePlotCombine  = True")
print ("preparePlotHavester = False")
print ("doPostFit           = False # if False do Prefit only, it True it does both")
print ("plainBins           = True # If False do not take the template to reescale X-axis ---> It will be overwriten accordingly with the choices for legacy harcoded in this script")
print ("drawPlot            = True # if \"doPostFit = True\" that is superseeded with False")
print ("doTableYields       = False \n")

print ("And the rest should be False. \n")
cards_file = os.environ["CMSSW_BASE"] + "/src/signal_extraction_tH_ttH/cards/options.dat"

def run_cmd(command):
  print ("executing command = '%s'" % command)
  p = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
  stdout, stderr = p.communicate()
  return stdout

odir         = options.odir
cards_dir    = options.cards_dir
unblinded    = options.unblinded
do_only_cat  = options.do_only_cat

if odir == "none" :
    odir = cards_dir + "/plots"
run_cmd("mkdir %s"  % (odir))

unblinded       = options.unblinded

eras = [ 2016, 2017, 2018,  0 ]
## era 0 means all eras, and it assumes that all the other eras was already run in the same naming convention




plots_to_do_MVA = {
    "ttH_0l_2tau_ERA"        : {
        "cards_to_merge"      : [],
        "plainBins"            : True,
        "channel"             : "0l_2tau"
    },
    "ttH_1l_1tau_ERA"        : {
        "cards_to_merge"      : [],
        "plainBins"            : True,
        "channel"             : "1l_1tau"
    },
    "ttH_1l_2tau_ERA"        : {
        "cards_to_merge"      : [],
        "plainBins"            : True,
        "channel"             : "1l_2tau"
    },
    "ttH_2los_1tau_ERA"      : {
        "cards_to_merge"      : [],
        "plainBins"            : True,
        "channel"             : "2los_1tau"
    },
    "ttH_2l_2tau_ERA"        : {
        "cards_to_merge"      : [],
        "plainBins"            : False,
        "channel"             : "2l_2tau"
    },
    "ttH_3l_1tau_ERA"        : {
        "cards_to_merge"      : [],
        "plainBins"            : False,
        "channel"             : "3l_1tau"
    },
    "ttH_4l_ERA"             : {
        "cards_to_merge"      : [],
        "plainBins"            : False,
        "channel"             : "4l_0tau"
    },
    "ttH_cr_4l_ERA"          : {
        "cards_to_merge"      : [],
        "plainBins"            : False,
        "channel"             : "4lctrl"
    },
    ###
    "ttH_cr_3l_ERA_cr"   : {
        "cards_to_merge"      : ["ttH_cr_3l_ERA_eee_cr", "ttH_cr_3l_ERA_eem_cr", "ttH_cr_3l_ERA_mmm_cr"],
        "plainBins"            : False,
        "channel"             : "3lctrl"
    },
    "ttH_2lss_1tau_ERA"      : {
        "cards_to_merge"      : ["ttH_2lss_1tau_rest_ERA", "ttH_2lss_1tau_tH_ERA", "ttH_2lss_1tau_ttH_ERA"],
        "plainBins"            : False,
        "channel"             : "2lss_1tau"
    },
    "ttH_2lss_0tau_rest_ERA" : {
        "cards_to_merge"      : ["ttH_2lss_0tau_ee_Restnode_ERA", "ttH_2lss_0tau_em_Restnode_ERA", "ttH_2lss_0tau_mm_Restnode_ERA" ],
        "plainBins"            : False,
        "channel"             : "2lss_0tau_rest"
    },
    "ttH_2lss_0tau_tH_ERA"   : {
        "cards_to_merge"      : ["ttH_2lss_0tau_ee_tHQnode_ERA", "ttH_2lss_0tau_em_tHQnode_ERA", "ttH_2lss_0tau_mm_tHQnode_ERA"],
        "plainBins"            : False,
        "channel"             : "2lss_0tau_tH"
    },
    "ttH_2lss_0tau_ttH_ERA"  : {
        "cards_to_merge"      : ["ttH_2lss_0tau_ee_ttHnode_ERA", "ttH_2lss_0tau_em_ttHnode_ERA", "ttH_2lss_0tau_mm_ttHnode_ERA"],
        "plainBins"            : False,
        "channel"             : "2lss_0tau_ttH"
    },
    "ttH_2lss_0tau_ttW_ERA"  : {
        "cards_to_merge"      : ["ttH_2lss_0tau_ee_ttWnode_ERA", "ttH_2lss_0tau_em_ttWnode_ERA", "ttH_2lss_0tau_mm_ttWnode_ERA" ],
        "plainBins"            : False,
        "channel"             : "2lss_0tau_ttW"
    },
    "ttH_3l_0tau_rest_ERA"   : {
        "cards_to_merge"      : ["ttH_3l_0tau_rest_eee_ERA", "ttH_3l_0tau_rest_eem_bl_ERA", "ttH_3l_0tau_rest_eem_bt_ERA", "ttH_3l_0tau_rest_emm_bl_ERA", "ttH_3l_0tau_rest_emm_bt_ERA", "ttH_3l_0tau_rest_mmm_bl_ERA", "ttH_3l_0tau_rest_mmm_bt_ERA"],
        "plainBins"            : False,
        "channel"             : "3l_0tau_rest"
    },
    "ttH_3l_0tau_tH_ERA"     : {
        "cards_to_merge"      : ["ttH_3l_0tau_tH_bl_ERA", "ttH_3l_0tau_tH_bt_ERA"],
        "plainBins"            : False,
        "channel"             : "ttH_3l_0tau_tH"
    },
    "ttH_3l_0tau_ttH_ERA"    : {
        "cards_to_merge"      : ["ttH_3l_0tau_ttH_bl_ERA", "ttH_3l_0tau_ttH_bt_ERA"],
        "plainBins"            : False,
        "channel"             : "ttH_3l_0tau_ttH"
    },
    "ttH_2lss_1tau_ERA"      : {
        "cards_to_merge"      : ["ttH_2lss_1tau_rest_ERA", "ttH_2lss_1tau_tH_ERA", "ttH_2lss_1tau_ttH_ERA"],
        "plainBins"            : False,
        "channel"             : "2lss_1tau"
    },


}

for era in eras :
    for key in plots_to_do_MVA :
        if not do_only_cat == "No" :
            if not do_only_cat == key :
                print ("skipping %s by command of the user" % key)
                continue
        print ("====================================================================")
        print (key, era)
        eraDraw = str(era)
        if era == 0 :
            print ("=====> Mind that 'era 0 ' will only work if the other eras are already done")
            eraDraw = "2018"
        ####################################################
        if len(plots_to_do_MVA[key]["cards_to_merge"]) :
            print ("Combine cards to do prefit plots")
            card_to_read = "combo_%s_%s" % (plots_to_do_MVA[key]["channel"], eraDraw)
            if not era == 0 :
                cmd = "cd %s; combineCards.py  " % cards_dir
                for cards_merge in plots_to_do_MVA[key]["cards_to_merge"] :
                    cmd += "%s=%s.txt " % (cards_merge.replace("ERA", str(era)), cards_merge.replace("ERA", str(era)))
                cmd += " > %s.txt" % (card_to_read)
                run_cmd(cmd)
        else :
            card_to_read = key.replace("ERA", str(eraDraw))
        ###################################################
        print (" ")
        cmd2 = "python test/run_limits_floating_components.py "
        cmd2 += "--cardFolder %s  " % cards_dir
        cmd2 += "--savePlotsOn %s " % odir
        if not unblinded == "No" : # True / False / No
            cmd2 += "--unblinded %s " % unblinded
        if plots_to_do_MVA[key]["plainBins"] :
            cmd2 += "--plainBins %s " % str(plots_to_do_MVA[key]["plainBins"])
        cmd2 += "--savePlotsOn %s " % odir
        cmd2 += "--era %s " % (str(era))
        cmd2 += "--cardToRead %s " % (card_to_read)
        cmd2 += "--channel %s " % (plots_to_do_MVA[key]["channel"])
        #print (cmd2)
        run_cmd(cmd2)




#####
