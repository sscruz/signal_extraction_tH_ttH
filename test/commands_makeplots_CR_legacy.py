#!/usr/bin/env python
import os, shlex
from subprocess import Popen, PIPE

from optparse import OptionParser
parser = OptionParser()
parser.add_option(
    "--odir",
    type="string",
    dest="odir",
    help="Full path of where to put the plots"
    )
parser.add_option(
    "--cards_dir",
    type="string",
    dest="cards_dir",
    help="Full path of where to put the plots"
    )
parser.add_option(
    "--fitDiagnosis",
    type="string",
    dest="fitDiagnosis",
    help="Full path of fitDiagnosis.root"
    )
parser.add_option(
    "--unblided",
    action="store_true",
    dest="unblided",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--doPostFit",
    action="store_true",
    dest="doPostFit",
    help="Self explanatory",
    default=False
    )
(options, args) = parser.parse_args()

print ()

def run_cmd(command):
  print ("executing command = '%s'" % command)
  p = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
  stdout, stderr = p.communicate()
  return stdout

odir         = options.odir
fitDiagnosis = options.fitDiagnosis
cards_dir    = options.cards_dir
doPostFit    = options.doPostFit
unblided     = options.unblided

eras = [ 2016, 2017, 2018, 0 ]

cards_to_do = {
    "ttH_1l_2tau_ERA"         : {
        "original"          : "ttH_1l_2tau_SS_mTTVis_ERA", # name of the datacard(.txt/.root) to take binX templates
        "binToReadOriginal" : "ttH_1l_2tau",               # if the datacard(.txt/.root) has a subfolder this is the name of the subfolder
        "IHEP"              : False ,                      # True if the datacard(.txt/.root) has no subfolder
        "channel"           : "1l_2tau_SS",                # to take the plot options of the options_plot_ranges function on configs/plot_options.py
        "binToRead"         : "ttH_1l_2tau_ERA",           # bin inside the fitDiagnosis, assumes that you use test/combine_cards_legacy_CR.py to merge cards before doing it
        "nameLabel"         : "none"                       # if you want to overwrite the option on plot options of the options_plot_ranges function on configs/plot_options.py
    },
    "tH_cr_4l_ERA"           : {
        "original"  : "none" ,
        "channel"   : "4lctrl",
        "IHEP"      : False ,
        "binToRead" : "ttH_cr_4l_ERA",
        "nameLabel" : "none"
    },
    "ttH_3l_cr_ERA"          : {
        "original"  : "none" ,
        "channel"   : "3lctrl",
        "IHEP"      : False ,
        "binToRead" : "ttH_3l_cr_ERA",
        "nameLabel" : "none"
    },
    "ttH_2lss_3j_ERA_ee"     : {
        "original"          : "ttH_2lss_3j_ERA_ee" ,
        "channel"           : "ttH_2lss_3j_ee",
        "IHEP"              : True ,
        "binToRead"         : "ttH_2lss_3j_ERA_ee",
        "nameLabel"         : "none" #" ee"
    },
    "ttH_2lss_3j_ERA_em_neg" : {
        "original"          : "ttH_2lss_3j_ERA_em_neg",
        "channel"           : "ttH_2lss_3j_em_neg",
        "IHEP"              : True ,
        "binToRead"         : "ttH_2lss_3j_ERA_em_neg",
        "nameLabel"         : "none" #" e\#mu --"
    },
    "ttH_2lss_3j_ERA_em_pos" : {
        "original"          : "ttH_2lss_3j_ERA_em_pos",
        "channel"           : "ttH_2lss_3j_em_pos",
        "IHEP"              : True ,
        "binToRead"         : "ttH_2lss_3j_ERA_em_pos",
        "nameLabel"         : "none" #" e\#mu ++"
    },
    "ttH_2lss_3j_ERA_mm_neg" : {
        "original"          : "ttH_2lss_3j_ERA_mm_neg" ,
        "channel"           : "ttH_2lss_3j_mm_neg" ,
        "IHEP"              : True ,
        "binToRead"         : "ttH_2lss_3j_ERA_mm_neg" ,
        "nameLabel"         : "none" #" \#mu\#mu --"
    },
    "ttH_2lss_3j_ERA_mm_pos" : {
        "original"          : "ttH_2lss_3j_ERA_mm_pos",
        "channel"           : "ttH_2lss_3j_mm_neg",
        "IHEP"              : True ,
        "binToRead"         : "ttH_2lss_3j_ERA_mm_pos" ,
        "nameLabel"         : "none" #" \#mu\#mu ++"
    }
}

for era in eras :
    for key in cards_to_do :
        print (key, era)
        eraDraw = str(era)
        if era == 0 :
            eraDraw = "2018"
        cmd = "python test/makePlots.py "
        cmd += "--input %s " % fitDiagnosis
        cmd += "--odir %s " % odir
        if not cards_to_do[key]["original"] == "none" :
            cmd += "--original  %s/%s.root " % (cards_dir, cards_to_do[key]["original"].replace("ERA", eraDraw) )
            if cards_to_do[key]["IHEP"] :
                cmd += "--IHEP "
            else :
                cmd += "--binToReadOriginal %s " % cards_to_do[key]["binToReadOriginal"].replace("ERA", eraDraw)
        cmd += "--era %s " % str(era)
        cmd += "--nameOut %s " % key.replace("ERA", str(era))
        cmd += "--do_bottom "
        cmd += "--channel %s " % cards_to_do[key]["channel"].replace("ERA", eraDraw)
        if doPostFit :
            cmd += "--doPostFit "
        cmd += "--binToRead %s " % cards_to_do[key]["binToRead"].replace("ERA", eraDraw)
        if unblided :
            cmd += "--unblind "
        if not cards_to_do[key]["nameLabel"] == "none" :
            cmd += "--nameLabel \"%s\" " % cards_to_do[key]["nameLabel"]
        #print (cmd)
        output = run_cmd(cmd)
        ff = open("%s/%s.log" % (odir, key.replace("ERA", str(era))) ,"w+")
        ff.write(output)
        ff.close()
