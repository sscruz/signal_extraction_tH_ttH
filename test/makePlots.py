#!/usr/bin/env python
import os, subprocess, sys
import os, sys, time,math
import ROOT
from optparse import OptionParser
from collections import OrderedDict
execfile("python/data_manager_makePostFitPlots.py")
ROOT.gStyle.SetOptStat(0)

from optparse import OptionParser
parser = OptionParser()
parser.add_option(
    "--input", type="string", dest="input",
    help="A valid file with the shapes as output of combine FitDiagnostics",
    default="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017/posfit_3poi_ttVFromZero/ttH_fitDiagnostics.Test_shapes.root"
    )
parser.add_option(
    "--odir", type="string", dest="odir",
    help="Directory for the output plots",
    default="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017/posfit_3poi_ttVFromZero/"
    )
parser.add_option(
    "--original", type="string", dest="original",
    help="The original datacard: used only to rebin",
    default="none"
    )
parser.add_option(
    "--channel", type="string", dest="channel",
    help="Name of the category as it is appear on the input file",
    default="ttH_1l_2tau_OS"
    )
parser.add_option(
    "--labelX", type="string", dest="labelX",
    help="To appear on final plot",
    default="NN bin#"
    )
parser.add_option(
    "--nameOut", type="string", dest="nameOut",
    help="To appear on final plot",
    default="test"
    )
parser.add_option(
    "--nameLabel", type="string", dest="nameLabel",
    help="To appear on final plot",
    default="none"
    )
parser.add_option(
    "--useLogPlot", action="store_true", dest="useLogPlot",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--notFlips", action="store_true", dest="notFlips",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--notConversions", action="store_true", dest="notConversions",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--MC_IsSplit", action="store_true", dest="MC_IsSplit",
    help="If the MC components on card are separated as 'gentau' and 'faketau' ",
    default=False
    )
parser.add_option(
    "--divideByBinWidth", action="store_true", dest="divideByBinWidth",
    help="If final plot shall be done dividing bin content by bin width ",
    default=False
    )
parser.add_option(
    "--doMultilep", action="store_false", dest="doMultilep",
    help="Do subcategories from multilepton cards ",
    default=True
    )
parser.add_option(
    "--unblind", action="store_true", dest="unblind",
    help="Do subcategories from multilepton cards ",
    default=False
    )
parser.add_option(
    "--doPostFit", action="store_true", dest="doPostFit",
    help="Do the postfit instead of prefit ",
    default=False
    )
parser.add_option(
    "--minY", type="float", dest="minY",
    help="For the final plot",
    default=0.
    )
parser.add_option(
    "--maxY", type="float", dest="maxY",
    help="For the final plot",
    default=1.
    )
parser.add_option(
    "--fromHavester", action="store_true", dest="fromHavester",
    help="The input file is from CombineHavester. In this case you do not need to enter 'original' if you called the PostFitShapesFromWorkspace with the -d option",
    default=False
    )
(options, args) = parser.parse_args()

divideByBinWidth = options.divideByBinWidth
category = options.channel
print ("category", category)

labelY = "Events"
if divideByBinWidth : labelY = "Events / bin width"

if options.doPostFit :
    if not options.fromHavester :
        folder = "shapes_fit_s"
        folder_data = "shapes_fit_s" # it is a TGraphAsymmErrors, not histogram
        typeFit = "postfit"
    else :
        folder = category+"_postfit"
        folder_data = category+"_postfit" # it is a histogram
        typeFit = "postfit"
else :
    if not options.fromHavester :
        folder = "shapes_prefit"
        folder_data = "shapes_prefit" # it is a TGraphAsymmErrors, not histogram
        typeFit = "prefit"
    else :
        folder = category+"_prefit"
        folder_data = category+"_prefit" # it is a histogram
        typeFit = "prefit"
print ("folder", folder)

if not options.fromHavester : name_total = "total"
elif not options.doPostFit : name_total = "TotalBkg"
else : name_total = "TotalProcs"

conversions = "Conv" #"conversions"
fakes       = "Fakes" #"fakes_data"
flips       = "Flips" #"flips_data"

dprocs = OrderedDict()

# if label == "none" it means that this process is to be merged with the anterior key
#                      color, fillStype, label,       , make border
dprocs[fakes]        = [12,     3345,      "Non-prompt",        True]
dprocs[flips]        = [1,     3006,      "Charge mis-m",       True]
dprocs[conversions]  = [5,     1001,      "Conv.", True]
dprocs["Rares"]      = [851,   1001,      "Rares",       True]
#if "tau" in category :
if 1 > 0 :
    dprocs["EWK"]        = [610,   1001,      "EWK",         True]
#else :
#    dprocs["ZZ"]        = [610,   1001,      "none",         True]
#    dprocs["WZ"]        = [610,   1001,      "EWK",         True]
if not "2los_1tau" in category and not "2eos_1tau" in category and not "2muos_1tau" in category and not "1mu1eos_1tau" in category:
    dprocs["TTW"]        = [823,   1001,      "none",        False]
    dprocs["TTWW"]       = [823,   1001,      "ttW + ttWW",        True]
else : dprocs["TTW"]        = [823,   1001,      "ttWW",        True]
dprocs["TTZ"]        = [822,   1001,      "ttZ",         True]
#if not "2los_1tau" in category and not "2eos_1tau" in category and not "2muos_1tau" in category and not "1mu1eos_1tau" in category:
#    dprocs["ttH_hzg"]    = [2,     1001,      "none",        False]
#    dprocs["ttH_hmm"]    = [2,     1001,      "none",        False]
dprocs["ttH_hww"]    = [2,     1001,      "none",        False]
dprocs["ttH_hzz"]    = [2,     1001,      "none",        False]
dprocs["ttH_htt"]    = [2,     1001,      "ttH",     True]

label_head = "2017 fit,"

if typeFit == "prefit" : label_head = label_head+" "+typeFit
else : label_head = label_head+" #mu(ttH)=#hat{#mu}"

if not options.nameLabel == "none" :
    label_head += " " + options.nameLabel

print label_head

if options.notFlips : del dprocs[flips]
if options.notConversions : del dprocs[conversions]
print ("will draw processes", list(dprocs.keys()))

if not options.original == "none" :
    fileOrig = options.original
else :
    fileOrig = options.input
print ("template on ", fileOrig)

fin = ROOT.TFile(options.input, "READ")
if not options.original == "none" :
    catcats = [category]
    readFrom = category  
    print ("readFrom ", readFrom)
    fileorriginal = ROOT.TFile(fileOrig, "READ")
    template = fileorriginal.Get(readFrom + "/" + name_total)
    template.GetYaxis().SetTitle(labelY)
    template.SetTitle(" ")
    datahist = fileorriginal.Get(readFrom + "/data_obs")
else :
    catcats = getCats(folder, fin, options.fromHavester)
    print(catcats)
    nbinstotal = 0
    for catcat in catcats :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat  
        else : 
            readFrom = catcat 
        hist = fin.Get(readFrom + "/" + name_total )
        print (readFrom + "/" + name_total)
        nbinscat = GetNonZeroBins(hist)
        print (readFrom, nbinscat)
        nbinstotal += nbinscat
        datahist = fin.Get(readFrom + "/data")
    template = ROOT.TH1F("my_hist", "", nbinstotal, 0, nbinstotal+1)

legend_y0 = 0.650
legend1 = ROOT.TLegend(0.2400, legend_y0, 0.9450, 0.9150)
legend1.SetNColumns(3)
legend1.SetFillStyle(0)
legend1.SetBorderSize(0)
legend1.SetFillColor(10)
legend1.SetTextSize(0.040)
legend1.SetHeader(label_head)

if options.unblind :
    dataTGraph1 = "NoneType"
    if not options.fromHavester :
        dataTGraph1 = ROOT.TGraphAsymmErrors()
        dataTGraph1.Set(template.GetXaxis().GetNbins())
    else :
        dataTGraph1 = template.Clone()
    lastbin = 0 
    for cc, catcat in enumerate(catcats) :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat  
        else : 
            readFrom = catcat 
        histtotal = fin.Get(readFrom + "/" + name_total )
        lastbin += rebin_data(template, dataTGraph1, readFrom, fin, options.fromHavester, lastbin, histtotal) 
        print (readFrom, lastbin)
    dataTGraph1.Draw()
    legend1.AddEntry(dataTGraph1, "Observed", "p")
print folder
hist_total = template.Clone()
lastbin = 0 
for cc, catcat in enumerate(catcats) :
    if not options.fromHavester :
        readFrom = folder + "/" + catcat  
    else : 
        readFrom = catcat  
    lastbin += rebin_total(hist_total, readFrom, fin, divideByBinWidth, name_total, lastbin) 
legend1.AddEntry(hist_total, "Uncertainty", "f")

canvas = ROOT.TCanvas("canvas", "canvas", 600, 1500)
canvas.SetFillColor(10)
canvas.SetBorderSize(2)
dumb = canvas.Draw()
del dumb

topPad = ROOT.TPad("topPad", "topPad", 0.00, 0.34, 1.00, 0.995)
topPad.SetFillColor(10)
topPad.SetTopMargin(0.075)
topPad.SetLeftMargin(0.20)
topPad.SetBottomMargin(0.00)
topPad.SetRightMargin(0.04)
if options.useLogPlot : topPad.SetLogy()
bottomPad = ROOT.TPad("bottomPad", "bottomPad", 0.00, 0.01, 1.00, 0.34)
bottomPad.SetFillColor(10)
bottomPad.SetTopMargin(0.0)
bottomPad.SetLeftMargin(0.20)
bottomPad.SetBottomMargin(0.35)
bottomPad.SetRightMargin(0.04)
####################################
canvas.cd()
dumb = topPad.Draw()
del dumb
topPad.cd()
dumb = hist_total.Draw("axis")
del dumb
histogramStack_mc = ROOT.THStack()
print ("list of processes considered and their integrals")

for key in  dprocs.keys() :
    hist_rebin = template.Clone()
    lastbin = 0 
    addlegend = True
    for cc, catcat in enumerate(catcats) :
        if not cc == 0 : addlegend = False
        if not options.fromHavester :
            readFrom = folder + "/" + catcat  
        else : 
            readFrom = catcat 
        lastbin += rebin_hist(hist_rebin, fin, readFrom, key, dprocs[key], divideByBinWidth, addlegend) 
        print (readFrom, lastbin)
    if hist_rebin == 0 : continue
    dumb = histogramStack_mc.Add(hist_rebin)
    del dumb
    print (key, hist_rebin.Integral())

dumb = histogramStack_mc.Draw("hist,same")
del dumb
dumb = hist_total.Draw("e2,same")
del dumb
if options.unblind :
    dumb = dataTGraph1.Draw("e1P,same")
    del dumb
dumb = hist_total.Draw("axis,same")
del dumb
dumb = legend1.Draw("same")
del dumb
labels = addLabel_CMS_preliminary()
for label in labels :
    dumb = label.Draw("same")
    del dumb
#################################
canvas.cd()
dumb = bottomPad.Draw()
del dumb
bottomPad.cd()
bottomPad.SetLogy(0)
print ("doing bottom pad")
hist_total_err = template.Clone()
lastbin = 0
for cc, catcat in enumerate(catcats) :
    if not options.fromHavester :
        readFrom = folder + "/" + catcat  
    else : 
        readFrom = catcat 
    histtotal = fin.Get(readFrom + "/" + name_total )
    lastbin += do_hist_total_err(hist_total_err, options.labelX, name_total, readFrom, lastbin) 
    print (readFrom, lastbin)
dumb = hist_total_err.Draw("e2")
del dumb
if options.unblind :
    if not options.fromHavester :
        dataTGraph2 = ROOT.TGraphAsymmErrors()
    else :
        dataTGraph2 = template.Clone()
    lastbin = 0
    for cc, catcat in enumerate(catcats) :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat  
        else : 
            readFrom = catcat  
        histtotal = fin.Get(readFrom + "/" + name_total )
        lastbin += err_data(dataTGraph2, hist_total, readFrom, options.fromHavester, lastbin, histtotal) 
        print (readFrom, lastbin)
    dumb = dataTGraph2.Draw("e1P,same")
    del dumb
line = ROOT.TF1("line", "0", hist_total_err.GetXaxis().GetXmin(), hist_total_err.GetXaxis().GetXmax()) 
line.SetLineStyle(3)
line.SetLineColor(ROOT.kBlack)
dumb = line.Draw("same")
del dumb
print ("done bottom pad")
##################################
oplin = "linear"
if options.useLogPlot : oplin = "log"
optbin = "plain"
if divideByBinWidth : optbin = "divideByBinWidth"
print ("made log")
#canvas.Print(options.odir+category+"_"+typeFit+"_"+optbin+"_unblind"+str(options.unblind)+"_"+oplin+".pdf")
#canvas.Close()

savepdf = options.odir+category+"_"+typeFit+"_"+optbin+"_"+options.nameOut+"_unblind"+str(options.unblind)+"_"+oplin + "_" + options.nameLabel + ".pdf"
dumb = canvas.SaveAs(savepdf)
del dumb
print ("saved", savepdf)
