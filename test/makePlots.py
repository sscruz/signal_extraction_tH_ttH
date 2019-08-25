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
    "--typeCat", type="string", dest="typeCat",
    help="Name of the category as it is appear on the input file",
    default="ttH_1l_2tau_OS"
    )
parser.add_option(
    "--labelX", type="string", dest="labelX",
    help="To appear on final plot",
    default="none"
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
category         = options.channel
typeCat          = options.typeCat
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
#elif not options.doPostFit : name_total = "TotalBkg"
else : name_total = "TotalProcs"

if 1 > 0 :
    conversions = "Conv" #"conversions"
    fakes       = "Fakes" #"fakes_data"
    flips       = "Flips" #"flips_data"
else :
    conversions = "conversions"
    fakes       = "fakes_data"
    flips       = "flips_data"


info_file = os.environ["CMSSW_BASE"] + "/src/signal_extraction_tH_ttH/configs/plot_options.py"
execfile(info_file)
print ("list of signals/bkgs by channel taken from: " +  info_file)
procs  = list_channels_draw("ttH")[category] #: OrderedDict()
print procs
dprocs = options_plot ("ttH", category, procs["bkg_proc_from_data"] + procs['bkg_procs_from_MC'] + procs["signal"])

label_head = ""

if not options.nameLabel == "none" :
    label_head += options.nameLabel
else :
    if typeCat in options_plot_ranges("ttH").keys() :
        label_head += options_plot_ranges("ttH")[typeCat]["label"]

if typeFit == "prefit" : 
    label_head = label_head+", "+typeFit
else : 
    label_head = label_head+", #mu(ttH)=#hat{#mu}"

if not options.labelX == "none" :
    labelX = options.labelX
elif typeCat in options_plot_ranges("ttH").keys() :
    labelX = options_plot_ranges("ttH")[typeCat]["labelX"]
else : labelX = "BDT"

print ("will draw processes", list(dprocs.keys()))

if not options.original == "none" :
    fileOrig = options.original
else :
    fileOrig = options.input
print ("template on ", fileOrig)

minY = 1
if options.maxY == 1 :
    if typeCat in options_plot_ranges("ttH").keys() : minY = options_plot_ranges("ttH")[typeCat]["minY"]
else : minY = options.minY

maxY = 1
if options.maxY == 1 :
    if typeCat in options_plot_ranges("ttH").keys() : maxY = options_plot_ranges("ttH")[typeCat]["maxY"]
else : minY = options.maxY



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
    template = ROOT.TH1F("my_hist", "", nbinstotal, 0 - 0.5 , nbinstotal - 0.5)

legend_y0 = 0.650
legend1 = ROOT.TLegend(0.2400, legend_y0, 0.9450, 0.9150)
legend1.SetNColumns(3)
legend1.SetFillStyle(0)
legend1.SetBorderSize(0)
legend1.SetFillColor(10)
legend1.SetTextSize(0.040)
print label_head
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
bottomPad = ROOT.TPad("bottomPad", "bottomPad", 0.00, 0.05, 1.00, 0.34)
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

linebin = []
linebinW = []
y0 = (legend_y0 - 0.001)*maxY
for kk, key in  enumerate(dprocs.keys()) :
    hist_rebin = template.Clone()
    lastbin = 0 
    addlegend = True
    for cc, catcat in enumerate(catcats) :
        if not cc == 0 : addlegend = False
        if not options.fromHavester :
            readFrom = folder + "/" + catcat  
        else : 
            readFrom = catcat
        info_hist = rebin_hist(hist_rebin, fin, readFrom, key, dprocs[key], divideByBinWidth, addlegend) 
        lastbin += info_hist["lastbin"]
        print (readFrom, lastbin)
        if kk == 0 :
            if info_hist["binEdge"] > 0 : 
                linebin += [ROOT.TLine(info_hist["binEdge"], 0., info_hist["binEdge"], (legend_y0 + 0.05)*maxY)]
            x0 = float(lastbin - info_hist["labelPos"] -1)
            linebinW += [ROOT.TPaveText(x0 - 0.0950, y0, x0 + 0.0950, y0 + 0.0600)]
    if hist_rebin == 0 : continue
    if "tHW" in key or "tHq" in key :
        hist_rebin.Scale(3.)
    dumb = histogramStack_mc.Add(hist_rebin)
    del dumb
    print (key, hist_rebin.Integral())

for line1 in linebin :
    line1.SetLineColor(1)
    line1.SetLineStyle(3)
    line1.Draw()

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

for cc, cat in enumerate(options_plot_ranges("ttH")[typeCat]["cats"]) :
    linebinW[cc].AddText(cat)
    linebinW[cc].SetTextFont(50)
    #label_cat.SetTextAlign(13)
    linebinW[cc].SetTextSize(0.05)
    linebinW[cc].SetTextColor(1)
    linebinW[cc].SetFillStyle(0)
    linebinW[cc].SetBorderSize(0)
    linebinW[cc].Draw("same")

"""x0 = float( (12. - 6./2.) /(nbinstotal))
y0 = legend_y0 - 0.05
label_cat2 = ROOT.TPaveText(x0, y0, x0 + 0.0950, y0 + 0.0600, "NDC")
label_cat2.AddText("2b")
label_cat2.SetTextFont(50)
label_cat2.SetTextAlign(13)
label_cat2.SetTextSize(0.055)
label_cat2.SetTextColor(1)
label_cat2.SetFillStyle(0)
label_cat2.SetBorderSize(0)
label_cat2.Draw("same")"""

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
    lastbin += do_hist_total_err(hist_total_err, labelX, name_total, readFrom, lastbin) 
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

savepdf = options.odir+category+"_"+typeFit+"_"+optbin+"_"+options.nameOut+"_unblind"+str(options.unblind)+"_"+oplin + "_" + options.typeCat + ".pdf"
dumb = canvas.SaveAs(savepdf)
del dumb
print ("saved", savepdf)