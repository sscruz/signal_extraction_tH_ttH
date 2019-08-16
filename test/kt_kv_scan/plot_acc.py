#!/usr/bin/env python
import sys
import os
import re
import multiprocessing
import numpy as np
import glob
import pandas as pd 
import ROOT
execfile(os.environ["CMSSW_BASE"] + "/src/signal_extraction_tH_ttH/python/data_manager_makePostFitPlots.py")
ROOT.gStyle.SetOptStat(0)
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib import ticker

from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#
#rc('font',**{'family':'sans-serif','sans-serif':['Nimbus Sans']})
rc('font',**{'family':'sans-serif'})


def print_header(axes, x_low, x_high, y_low, y_high, inside = False, logscale = False):
  y_val = y_high + 0.015 * (y_high - y_low)
  if inside:
    axes.text(x_low + abs(x_low) * 0.045, y_high - 0.46 * (y_high - y_low), 'CMS', style='normal', fontsize=15, fontweight='bold')
  else:
    axes.text(x_low, y_val, 'CMS', style='normal', fontsize=12, fontweight='bold') # 15 for a 6 X 6 figure
  #axes.text(x_low + (x_high - x_low) * 0.14, y_val, 'Preliminary', fontsize=15, style='italic') # for a 6 X 6 figure
  axes.text(x_low + (x_high - x_low) * 0.12, y_val, 'Preliminary', fontsize=12, style='italic') # for a 5 X 5 figure
  if logscale:
    axes.text(x_low + (x_high - x_low) * 0.67, y_high + 0.05 * (y_high - y_low), '35.9 fb$^{-1}$ (13 TeV)', fontsize=10)
  else:
    axes.text(x_low + (x_high - x_low) * 0.67, y_high + 0.01 * (y_high - y_low), '35.9 fb$^{-1}$ (13 TeV)', fontsize=10)
 
#/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/testPlots_master10X/datacard_1l_2tau_mvaOutput_plainKin_SUM_VT_noRebin_noNeg_kt_m3_kv_1.root

mom = "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/"
#"datacard_1l_2tau_mvaOutput_plainKin_SUM_VT_noRebin_noNeg_"
nllscan_file = mom + "nll_scan_comb6.csv"
#"nll_scan_blinded.csv"
channel = "1l_2tau"

info_file = os.environ["CMSSW_BASE"] + "/src/signal_extraction_tH_ttH/configs/plot_options.py"
execfile(info_file)
print ("list of signals/bkgs by channel taken from: " +  info_file)
list_channel_opt   = options_plot_labels("ttH") 

CX_tHq_SM = 0.74 ## placeholder, justb to have a reasonable number
CX_tHW_SM = 0.15

# To read all the avaiable cards
file = open(nllscan_file, mode='r')
all_of_it = file.read()
file.close()

all_of_it_by_line = all_of_it.split("\n")
kt = []
kv = []
ratio = []
for ll, line in enumerate(all_of_it.split("\n")) :
    if ll == 0 : continue
    listNum = line.split(",")
    if len(listNum) < 6 : continue
    kt += [float(listNum[2])]
    kv += [float(listNum[1])]
    ratio += [float(listNum[3])]

data = pd.DataFrame() 
data["kt"]    = kt #[ float(ktt) for ktt in kt]
data["kv"]    = kv #[ float(kvv) for kvv in kv]
data["ratio"] = ratio #[ float(ratio) for kvv in kv]
data["ktstring"] = [ (("m" if ktt < 0 else "") + str(abs(ktt))).replace(".", "p").replace("p0", "") for ktt in kt]
data["kvstring"] = [ (("m" if kvv < 0 else "") + str(abs(kvv))).replace(".", "p").replace("p0", "") for kvv in kv]

for key in list_channel_opt.keys() :
    if "ctrl" in key : continue
    if key in ["4l_0tau", "2l_2tau", "3l_1tau"] : continue
    yield_tHq   = []
    yield_tHW   = []
    yield_ttHLO = []
    for index, row in data.iterrows():
        # access data using column names
        #filetoread = mom + datacard_prefix + "kt_" + row["ktstring"] + "_kv_" + row["kvstring"] + ".root"
        filetoread = list_channel_opt[key]["mom"] + list_channel_opt[key]["prefix"] + row["kvstring"] + "_" + row["ktstring"] + ".input.root"
        filetoread = filetoread.replace("_0.input.root", "_m0.input.root")
        tfile = ROOT.TFile(filetoread )
        #tHq_hww = tfile.Get("ttH_" + channel + "/tHq_hww").Integral()
        #tHq_hzz = tfile.Get("ttH_" + channel + "/tHq_hzz").Integral()
        #tHq_htt = tfile.Get("ttH_" + channel + "/tHq_htt").Integral()
        tHq_hww = tfile.Get("x_tHq_hww").Integral()
        tHq_hzz = tfile.Get("x_tHq_hzz").Integral()
        tHq_htt = tfile.Get("x_tHq_htt").Integral()
        yield_tHq += [(tHq_hww + tHq_hzz + tHq_hzz)/CX_tHq_SM]
        #tHW_hww = tfile.Get("ttH_" + channel + "/tHW_hww").Integral()
        #tHW_hzz = tfile.Get("ttH_" + channel + "/tHW_hzz").Integral()
        #tHW_htt = tfile.Get("ttH_" + channel + "/tHW_htt").Integral()
        tHW_hww = tfile.Get("x_tHW_hww").Integral()
        tHW_hzz = tfile.Get("x_tHW_hzz").Integral()
        tHW_htt = tfile.Get("x_tHW_htt").Integral()
        yield_tHW += [(tHW_hww + tHW_hzz + tHW_hzz)/CX_tHW_SM]
        yield_ttHLO += [0.2]
        #print(index, row["yield_tHq"], row["ktstring"], row["kvstring"])

    data[key + "_tHq"] = yield_tHq
    data[key + "_tHW"] = yield_tHW
    data[key + "_ttHLO"] = yield_ttHLO

data = data.sort_values(by="ratio")
print data 
# datacard_PREFIX_kt_(m)1p25_kv_0p5.root

x_low, x_high = -6.5, 6.5
y_low, y_high = 0., 9.9

for process in ["tHq", "tHW"] :
    fig, ax = plt.subplots(figsize=(5, 5))
    colors = ["b", "g", "r", "springgreen", "fuchsia", "y", "k", "darkviolet", "teal", "orange" ] #"#ff7f0e#", "#8c564b", "#9467bd"]
    ii = 0
    list_labels = []
    for key in list_channel_opt.keys() :
        print key
        if "ctrl" in key : continue
        if key in ["4l_0tau", "2l_2tau", "3l_1tau"] : continue
        plt.plot(data["ratio"], data[key + "_" + process], 'o-', markersize=3, color=colors[ii], linestyle='-', markeredgewidth=0, linewidth=1, label=list_channel_opt[key]["latex"] )
        #list_labels += [list_channel_opt[key]["latex"]]
        ii += 1
    ax.set_xlabel(r'$\kappa_{t} / \kappa_{V}$', fontsize=14)
    ax.set_ylabel("acceptance X efficiency")
    plt.axis([x_low, x_high, y_low, y_high])
    leg = ax.legend(loc='upper left', fancybox=False, shadow=False, frameon=1, ncol=3, fontsize=10, title=process+ " process") 
    leg._legend_box.align = "left"
    leg.get_title().set_fontsize('9') 
    frame = leg.get_frame()
    frame.set_color('white')
    frame.set_linewidth(0)
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
    plt.axvline(x=1.0, color="k", linestyle=':', linewidth=1)
    print_header(ax, x_low, x_high, y_low, y_high)
    namefig    = mom + "AccTimeEff_" + process +".pdf"
    fig.savefig(namefig)
    print ("saved",namefig)