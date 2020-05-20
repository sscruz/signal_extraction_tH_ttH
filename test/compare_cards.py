#!/usr/bin/env python
import os, subprocess, sys
import os, sys, time,math
import ROOT
from optparse import OptionParser
from collections import OrderedDict
ROOT.gStyle.SetOptStat(0)

card1 = "/home/acaan/CMSSW_10_2_13/src/cards_set/legacy_TLL_11April20_unblinded/ttH_1l_1tau_2018.root"
card2 = "/home/acaan/CMSSW_10_2_13/src/cards_set/legacy_TLL_11April20_first_unblinded/forXanda/ttH_1l_1tau_2018.root"

tfile1 = ROOT.TFile(card1, "READ")
tfile2 = ROOT.TFile(card2, "READ")

for nkey, keyO in enumerate(tfile1.GetListOfKeys()) :
    # this bellow would be interesting if we would know all the histogram names
    #rootmv file:part1_*_part2 file:new_name
    # https://root.cern.ch/how/how-quickly-inspect-content-file
    obj0 =  keyO.ReadObj()
    obj0_name =  keyO.GetName()
    for nkey, key in enumerate(obj0.GetListOfKeys()) :
        obj =  key.ReadObj()
        obj_name = key.GetName()
        if "CMS" in obj_name or "ttHl" in obj_name or "data_obs" in obj_name :
            continue
        if type(obj) is not ROOT.TH1F :
            print ("is not a histogram ", obj_name)
            continue
        print ("found ", obj_name)
        in_second_file = "%s/%s" % (obj0_name, obj_name)
        print ( "%s/%s" % (obj0_name, obj_name))
        try :
            obj2 = tfile2.Get(in_second_file)
        except :
            print ("not found ", in_second_file, " in second file")
            continue
        try :
            integral_first_file = obj.Integral()
        except :
            print ("is not a histogram (no integral) ", obj_name)
            continue
        try :
            integral_second_file = obj2.Integral()
        except :
            print ("is not a histogram (no integral) in the second file ", obj_name)
            continue
        print (integral_first_file, integral_second_file)
        canvas = ROOT.TCanvas("canvas", "canvas", 900, 900)
        canvas.SetFillColor(10)
        canvas.SetBorderSize(2)
        dumb = canvas.Draw()
        del dumb
        ######
        legend_y0 = 0.745
        legend = ROOT.TLegend(0.3400, legend_y0, 0.9450, 0.850)
        legend.SetNColumns(1)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        legend.SetFillColor(10)
        legend.SetTextSize(0.040)
        ######
        hist_rebin = obj.Clone()
        #hist_rebin.SetMarkerSize(0)
        hist_rebin.SetLineColor(8)
        hist_rebin.SetLineWidth(3)
        #hist_rebin.SetFillStyle(itemDict["fillStype"])
        hist_rebin.Draw()
        legend.AddEntry(hist_rebin, "second version", "f")
        ######
        hist_rebin2 = obj2.Clone()
        #hist_rebin2.SetMarkerSize(0)
        hist_rebin2.SetLineColor(2)
        hist_rebin2.SetLineWidth(1)
        #hist_rebin.SetFillStyle(itemDict["fillStype"])
        hist_rebin2.Draw("same")
        legend.AddEntry(hist_rebin2, "first version", "f")
        ######
        dumb = legend.Draw("same")
        del dumb
        savepdf = card1 = "/home/acaan/CMSSW_10_2_13/src/cards_set/legacy_TLL_11April20_comparison/ttH_1l_1tau_2018/ttH_1l_1tau_2018_compare_" + obj_name
        dumb = canvas.SaveAs(savepdf + ".pdf")
        print ("saved", savepdf + ".pdf")
        #try : intproc = obj.Integral()
        #except : continue
