#!/usr/bin/env python
import os
import glob
import CombineHarvester.CombineTools.ch as ch

## type-3

# This script is only an example based on the cards used on HIG-18-019
# -- this adaptation was not tested -- you need to workout it itself 

#####################################################################
## From where to take the cards:
# The bellow is going to construct the combo card from scratch given the path of the cards by channel (see mom_2017/mom_2016)
copy_cards =  False
combine_cards = False
#####################################################################

# Download the bellow folders to mom and untar them on the same location than this script
# https://svnweb.cern.ch/cern/wsvn/cmshcg/trunk/cadi/HIG-18-019/
# https://svnweb.cern.ch/cern/wsvn/cmshcg/trunk/cadi/HIG-17-018/
mom_2017 = "HIG-18-019.r7705/2018jun28/" ## these are updated from svn version !!!!!!!!!!!

print "Working directory is: "+os.getcwd()+"/"
procP1=glob.glob(os.getcwd()+"/"+mom_2017+"/multilep/*.txt")
all_cards = procP1

# to remove some cards of the 
for xx in [
    'HIG-18-019.r7705/2018jun28//multilep/comb_all16_mlep17_tau17_withCR.txt',
    'HIG-18-019.r7705/2018jun28//multilep/comb_all16_mlep17_withCR.txt',
    'HIG-18-019.r7705/2018jun28//multilep/comb_mlep17_tau17_withCR.txt',
    'HIG-18-019.r7705/2018jun28//multilep/comb_withCR.txt',
    'HIG-18-019.r7705/2018jun28//multilep/results_blind.txt',
    'HIG-18-019.r7705/2018jun28//multilep/ttH_4l.card.txt',
    'HIG-18-019.r7705/2018jun28//multilep/ttH_4l_crzz.card.txt',
    'HIG-18-019.r7705/2018jun28//multilep/ttH_3l_crwz.card.txt'
] : all_cards.remove(xx)

## The results are going to be saved on the local folder mom_result
mom_result = "multilep_only_CRs_2017/"

if blinded : blindStatement = ' -t -1 '
else : blindStatement = ' '

def decorrelate_btag(p) :
    cb.cp().process([p.process()]).RenameSystematic(cb, "CMS_ttHl16_btag_"+s , "CMS_ttHl17_btag_"+s);

def correlate_tauES(p) :
    cb.cp().process([p.process()]).RenameSystematic(cb, "CMS_ttHl_tauES", "CMS_scale_t");

def correlate_tauID(p) :
    cb.cp().process([p.process()]).RenameSystematic(cb, "CMS_ttHl17_tauID", "CMS_eff_t");

def decorrelate_JES(p) :
    cb.cp().process([p.process()]).RenameSystematic(cb, "CMS_scale_j" , "CMS_ttHl17_scale_j");

if copy_cards :
    run_cmd('mkdir '+os.getcwd()+"/"+mom_result)
    # rename only on the 2017
    for nn, process in enumerate(all_cards) :
        cb = ch.CombineHarvester()
        tokens = process.split("/")
        if not "ttH" in process :
            print tokens[8]+" "+tokens[9]+" ignoring card "+process
            continue
        proc_name = "Name"+str(nn+1)
        for part in tokens :
            if "ttH" in part :
                for name in part.split(".") :
                    if "ttH" in name :
                        print " adding process "+name
                        proc_name = name
        if "HIG-18-019" in process :
            complement = "_2017"
        if "HIG-17-018" in process :
            complement = "_2016"
        cb.ParseDatacard(process, analysis = proc_name+complement, mass = "")
        if not btag_correlated and "HIG-18-019" in process:
            print "start decorrelating btag"
            for s in  ["HF", "LF", "cErr1", "cErr2"] :
            print "renaming for "+s
            cb.ForEachProc(decorrelate_btag)
        if not JES_correlated and "HIG-18-019" in process:
            cb.ForEachProc(decorrelate_JES)
        writer = ch.CardWriter(os.getcwd()+"/"+mom_result+proc_name+complement+'.txt',
                    os.getcwd()+"/"+mom_result+proc_name+complement+'.root')
        writer.WriteCards('LIMITS/cmb', cb)

all_cards = glob.glob(os.getcwd()+"/"+mom_result+"*.txt")

if btag_correlated :
    cardToWrite = "card_combo_2016_2017_btag_correlated"
    cardToWrite_2017 = "card_combo_2017_btag_correlated"
else :
    cardToWrite = "card_combo_2016_2017_JES_Notcorrelated"
    cardToWrite_2017 = "card_combo_2017_JES_Notcorrelated"

if combine_cards :
    string_combine = "combineCards.py "
    string_combine_2017 = "combineCards.py "
    for nn, process in enumerate(all_cards) :
        tokens = process.split("/")
        # collect the cards
        if not "ttH" in process :
            print "ignoring card "+process
            continue
        proc_name = "Name"+str(nn+1)
        file_name = "Name"
        for part in tokens :
            if "ttH" in part :
                file_name = part
                for name in part.split(".") :
                    if "ttH" in name :
                        print " adding process "+name
                        proc_name = name
        if "Name" in proc_name and "ttH" in process :
            print "There is a problem ..... ..... .... not ignoring card "+process
            break
        # collect the cards to run full combo
        string_combine = string_combine + proc_name+"="+file_name+" "
        if "2016" not in proc_name :
            string_combine_2017 = string_combine_2017 + proc_name+"="+file_name+" "
    string_combine = string_combine+" > "+cardToWrite+".txt"
    run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; "+string_combine+" ; cd %s"  % (os.getcwd()+"/"))
    string_combine_2017 = string_combine_2017+" > "+cardToWrite_2017+".txt"
    run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; "+string_combine_2017+" ; cd %s"  % (os.getcwd()+"/"))
