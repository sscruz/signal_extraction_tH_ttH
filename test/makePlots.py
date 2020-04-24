#!/usr/bin/env python
import os, subprocess, sys
import os, sys, time,math
import ROOT
from optparse import OptionParser
from collections import OrderedDict
sys.stdout.flush()
sys.stdout.flush()

from optparse import OptionParser
parser = OptionParser()
parser.add_option(
    "--nameOut", type="string",
    dest="nameOut",
    help="To appear on the name of the file with the final plot",
    default="test"
    )
parser.add_option(
    "--input", type="string", dest="input",
    help="A valid file with the shapes as output of combine FitDiagnostics"#,
    #default="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017/posfit_3poi_ttVFromZero/ttH_fitDiagnostics.Test_shapes.root"
    )
parser.add_option(
    "--odir", type="string", dest="odir",
    help="Directory for the output plots",
    default="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017/posfit_3poi_ttVFromZero/"
    )
parser.add_option(
    "--original", type="string", dest="original",
    help="The original datacard: used only to rebin (the datacard.root)",
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
    default="none"
    )
parser.add_option(
    "--labelX", type="string", dest="labelX",
    help="To appear on final plot",
    default="none"
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
    "--divideByBinWidth", action="store_true", dest="divideByBinWidth",
    help="If final plot shall be done dividing bin content by bin width ",
    default=False
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
parser.add_option(
    "--do_bottom", action="store_true", dest="do_bottom",
    help="If do bottom pad",
    default=False
    )
parser.add_option(
    "--IHEP", action="store_true", dest="IHEP",
    help="IHEP cards do not have directories",
    default=False
    )
parser.add_option(
    "--era", type="int",
    dest="era",
    help="To appear on the name of the file with the final plot. If era == 0 it assumes you gave the path for the 2018 era and it will use the same naming convention to look for the 2017/2016.",
    default=2017
    )
parser.add_option(
    "--binToRead", type="string", dest="binToRead",
    help="Folder to read on the input root file -- if none it will try yo read all and put side by side.",
    default="none"
    )
parser.add_option(
    "--binToReadOriginal", type="string", dest="binToReadOriginal",
    help="Folder to read on the input root file -- if none it will try yo read all and put side by side.",
    default="none"
    )
(options, args) = parser.parse_args()

divideByBinWidth = options.divideByBinWidth
category         = options.channel
if options.typeCat == "none" :
    typeCat          = category
else :
    typeCat          = options.typeCat
print ("category", category, typeCat)
do_bottom = options.do_bottom
shapes_input = options.input

binToRead = options.binToRead
if binToRead == "none" :
    binToRead = "ttH_" +  category
print ("binToRead", binToRead)

binToReadOriginal = options.binToReadOriginal
if binToReadOriginal == "none" :
    binToReadOriginal = "ttH_" + category
print ("binToReadOriginal", binToReadOriginal)

print ("nameOut", options.nameOut)

labelY = "Events"
if divideByBinWidth : labelY = "Events / bin width"

if options.doPostFit :
    if not options.fromHavester :
        folder = "shapes_fit_s"
        folder_data = "shapes_fit_s" # it is a TGraphAsymmErrors, not histogram
        typeFit = "postfit"
    else :
        folder = binToRead + "_postfit"
        folder_data = binToRead + "_postfit" # it is a histogram
        typeFit = "postfit"
else :
    if not options.fromHavester :
        folder = "shapes_prefit"
        folder_data = "shapes_prefit" # it is a TGraphAsymmErrors, not histogram
        typeFit = "prefit"
    else :
        folder = binToRead + "_prefit"
        folder_data = binToRead + "_prefit" # it is a histogram
        typeFit = "prefit"
print ("folder", folder)

if not options.fromHavester : name_total = "total" # "total_background" # "total_covar" #
#elif not options.doPostFit : name_total = "TotalBkg"
else : name_total = "TotalProcs"

execfile("python/data_manager_makePostFitPlots.py")
ROOT.gStyle.SetOptStat(0)

flips       = "data_flips" # "flips_mc" #
conversions = "Convs"
fakes       = "data_fakes" # "fakes_mc" #

info_file = "/home/acaan/CMSSW_10_2_13/" + "/src/signal_extraction_tH_ttH/configs/plot_options.py" # os.environ["CMSSW_BASE"] +
execfile(info_file)
print ("list of signals/bkgs by channel taken from: " +  info_file)
procs  = list_channels_draw("ttH")[category] #: OrderedDict()
print procs
dprocs = options_plot ("ttH", category, procs["bkg_proc_from_data"] + procs['bkg_procs_from_MC'] + procs["signal"])

label_head = options_plot_ranges("ttH")[typeCat]["label"]
print (options_plot_ranges("ttH")[typeCat])
list_cats = options_plot_ranges("ttH")[typeCat]["list_cats"]

if not options.nameLabel == "none" :
    label_head += options.nameLabel
#else :
#    if typeCat in options_plot_ranges("ttH").keys() :
#        label_head += options_plot_ranges("ttH")[typeCat]["label"]

if typeFit == "prefit" :
    label_head = label_head+", \n"+typeFit
else :
    label_head = label_head+", #mu(t#bar{t}H)=#hat{#mu}"

if not options.labelX == "none" :
    labelX = options.labelX
elif typeCat in options_plot_ranges("ttH").keys() :
    labelX = options_plot_ranges("ttH")[typeCat]["labelX"]
else : labelX = "BDT"

print ("will draw processes", list(dprocs.keys()))

if not options.original == "none" :
    fileOrig = options.original
else :
    fileOrig = shapes_input
print ("template on ", fileOrig)

era = options.era

minY = 1
if options.maxY == 1 :
    if typeCat in options_plot_ranges("ttH").keys() : minY = options_plot_ranges("ttH")[typeCat]["minY"]
else : minY = options.minY

maxY = 1
if options.maxY == 1 :
    if typeCat in options_plot_ranges("ttH").keys() :
        maxY = options_plot_ranges("ttH")[typeCat]["maxY"]
else : maxY = options.maxY
if options.era == 0 :
    maxY = 2 * maxY

print("reading shapes from: ", shapes_input)
fin = [ROOT.TFile(shapes_input, "READ")]
if options.era == 0 :
    fin = fin + [ROOT.TFile(shapes_input.replace("2018", "2017"), "READ")]
    fin = fin + [ROOT.TFile(shapes_input.replace("2018", "2016"), "READ")]
    print ("will sum up " + str(len(fin)) + " eras")
    print (shapes_input.replace("2018", "2017"))
    print (shapes_input.replace("2018", "2016"))

if not options.original == "none" :
    #catcats = [category]
    #catcats = getCats(folder, fin[0], options.fromHavester)
    if not binToRead == "none" :
        catcats =  [binToRead]
    else :
        catcats = getCats(folder, fin[0], options.fromHavester)
    if options.IHEP :
        readFrom = ""
    elif not binToReadOriginal == "none" :
        readFrom =  binToReadOriginal + "/"
    else :
        readFrom =  "ttH_" + category + "/"
    print ("original readFrom ", readFrom)
    fileorriginal = ROOT.TFile(fileOrig, "READ")
    if options.IHEP :
        histRead = "x_TTZ"
    else :
        histRead = "ttH_htt" #"ttH_htt"
    template = fileorriginal.Get(readFrom + histRead ) #name_total) "x_TTZ"  "ttH_htt"    "ttH_htt"
    template.GetYaxis().SetTitle(labelY)
    template.SetTitle(" ")
    nbinscatlist = [template.GetNbinsX()]
    datahist = fileorriginal.Get(readFrom + "data_obs")
else :
    #if not binToRead == "none" :
    #    catcats =  [binToRead]
    #else :
    if not binToRead == "none" :
        if len(list_cats) == 0 :
            catcats = [binToRead] #[folder]
        else :
            if not options.era == 0 :
                catcats = [ cat.replace("2018", str(era)) for cat in list_cats]
            else :
                catcats = [ cat for cat in list_cats]
    else :
        if len(list_cats) == 0 :
            catcats = getCats(folder, fin[0], options.fromHavester)
        else :
            if options.era == 0 :
                catcats = list_cats
            else :
                catcats = [ cat.replace("2018", str(era)) for cat in list_cats]
    catcats = [binToRead]
    print("Drawing: ", catcats)
    nbinstotal = 0
    nbinscatlist = []
    for catcat in catcats :
        if not options.fromHavester :
            readFrom = folder + "/" + catcat
        else :

            readFrom = catcat # folder #
            readFrom += "_prefit"
            #if options.doPostFit :
            #    readFrom += "_prefit"
            #else :
            #    readFrom += "_postfit"
        hist = fin[0].Get(readFrom + "/" + name_total )
        print ("reading shapes", readFrom + "/" + name_total)
        nbinscat =  GetNonZeroBins(hist) # hist.GetNbinsX()  # Combine add zero bins
        nbinscatlist += [nbinscat]
        print (readFrom, nbinscat)
        nbinstotal += nbinscat
        datahist = fin[0].Get(readFrom + "/data")
    template = ROOT.TH1F("my_hist", "", nbinstotal, 0 - 0.5 , nbinstotal - 0.5)
    template.GetYaxis().SetTitle(labelY)
    print (nbinscatlist)

legend_y0 = 0.645
legend1 = ROOT.TLegend(0.2400, legend_y0, 0.9450, 0.910)
legend1.SetNColumns(3)
legend1.SetFillStyle(0)
legend1.SetBorderSize(0)
legend1.SetFillColor(10)
legend1.SetTextSize(0.040)
print label_head
legend1.SetHeader(label_head)
header = legend1.GetListOfPrimitives().First()
header.SetTextSize(.05)
header.SetTextColor(1)
header.SetTextFont(62)

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
            #readFrom = folder #catcat
            readFrom = catcat # folder #
            readFrom += "_prefit"
        print( " histtotal ", readFrom + "/" + name_total )
        histtotal = fin[0].Get(readFrom + "/" + name_total )
        lastbin += rebin_data(
            template,
            dataTGraph1,
            readFrom,
            fin,
            options.fromHavester,
            lastbin,
            histtotal,
            nbinscatlist[cc]
            )
    dataTGraph1.Draw()
    legend1.AddEntry(dataTGraph1, "Data", "p")
hist_total = template.Clone()

lastbin = 0
for cc, catcat in enumerate(catcats) :
    if not options.fromHavester :
        readFrom = folder + "/" + catcat
    else :
        #readFrom = folder #catcat
        readFrom = catcat # folder #
        readFrom += "_prefit"
    print ("read the hist with total uncertainties", readFrom, catcat)
    lastbin += rebin_total(
        hist_total,
        readFrom,
        fin,
        divideByBinWidth,
        name_total,
        lastbin,
        do_bottom,
        labelX,
        nbinscatlist[cc]
        )

if do_bottom :
    canvas = ROOT.TCanvas("canvas", "canvas", 600, 1500)
else :
    canvas = ROOT.TCanvas("canvas", "canvas", 900, 900)
canvas.SetFillColor(10)
canvas.SetBorderSize(2)
dumb = canvas.Draw()
del dumb

if do_bottom :
    topPad = ROOT.TPad("topPad", "topPad", 0.00, 0.34, 1.00, 0.995)
    topPad.SetFillColor(10)
    topPad.SetTopMargin(0.075)
    topPad.SetLeftMargin(0.20)
    topPad.SetBottomMargin(0.053)
    topPad.SetRightMargin(0.04)
    if options.useLogPlot or options_plot_ranges("ttH")[typeCat]["useLogPlot"]:
        topPad.SetLogy()

    bottomPad = ROOT.TPad("bottomPad", "bottomPad", 0.00, 0.05, 1.00, 0.34)
    bottomPad.SetFillColor(10)
    bottomPad.SetTopMargin(0.036)
    bottomPad.SetLeftMargin(0.20)
    bottomPad.SetBottomMargin(0.35)
    bottomPad.SetRightMargin(0.04)
else :
    topPad = ROOT.TPad("topPad", "topPad", 0.00, 0.05, 1.00, 0.995)
    topPad.SetFillColor(10)
    topPad.SetTopMargin(0.075)
    topPad.SetLeftMargin(0.20)
    topPad.SetBottomMargin(0.1)
    topPad.SetRightMargin(0.04)
    if options.useLogPlot or options_plot_ranges("ttH")[typeCat]["useLogPlot"]:
        topPad.SetLogy()
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
poslinebinW_X = []
pos_linebinW_Y = []
y0 = options_plot_ranges("ttH")[typeCat]["position_cats"] # (legend_y0 - 0.01)*maxY
if options.era == 0 :
    y0 = 2 * y0
for kk, key in  enumerate(dprocs.keys()) :
    hist_rebin = template.Clone()
    lastbin = 0
    addlegend = True
    print("Stacking ", key)
    for cc, catcat in enumerate(catcats) :
        if not cc == 0 : addlegend = False
        if not options.fromHavester :
            readFrom = folder + "/" + catcat
        else :
            #readFrom = catcat
            readFrom = catcat # folder #
            readFrom += "_prefit"
        info_hist = rebin_hist(
            hist_rebin,
            fin,
            readFrom,
            key,
            dprocs[key],
            divideByBinWidth,
            addlegend,
            lastbin,
            nbinscatlist[cc]
            )
        # hist_rebin, fin, folder, name, itemDict, divideByBinWidth, addlegend, lastbin
        lastbin += info_hist["lastbin"]
        if kk == 0 :
            #print ("pllt category label at position: ", info_hist["labelPos"])
            print (info_hist)
            print ("info_hist[binEdge]", info_hist["binEdge"])
            if info_hist["binEdge"] > 0 :
                linebin += [ROOT.TLine(info_hist["binEdge"], 0., info_hist["binEdge"], y0*1.2)] # (legend_y0 + 0.05)*maxY
            x0 = float(lastbin - info_hist["labelPos"] -1)
            #linebinW += [
            #    ROOT.TLatex()
            #    ]
            sum_inX = 0.1950
            if cc > 2 :
                if cc == 3 :
                    sum_inX = 0.65
                else :
                    sum_inX = 0.35
            poslinebinW_X += [x0 - sum_inX]
            pos_linebinW_Y += [y0]

    if hist_rebin == 0 or not hist_rebin.Integral() > 0 or (info_hist["labelPos"] == 0 and not options.original == "none" )  : # : (info_hist["labelPos"] == 0 and not options.original == "none" )
        continue
    print (key,  0 if hist_rebin == 0 else hist_rebin.Integral() )
    #if "tHq" in key :
    #    hist_rebin.Scale(3.)
    dumb = histogramStack_mc.Add(hist_rebin)
    del dumb

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

labels = addLabel_CMS_preliminary(options.era)
for ll, label in enumerate(labels) :
    print ("printing label", ll)
    if ll == 0 :
        dumb = label.Draw("same")
        del dumb
    else :
        dumb = label.Draw()
        del dumb

for cc, cat in enumerate(options_plot_ranges("ttH")[typeCat]["cats"]) :
    print ("Draw label cat", cat, cc)
    sumBottom = 0
    for ccf, cf in enumerate(cat) :
        linebinW = ROOT.TLatex()
        linebinW.DrawLatex(poslinebinW_X[cc], pos_linebinW_Y[cc] + sumBottom, cf)
        linebinW.SetTextFont(50)
        linebinW.SetTextAlign(12)
        linebinW.SetTextSize(0.05)
        linebinW.SetTextColor(1)
        #if ccf == 0 and len(cat) > 2:
        #    sumBottom += -0.75
        #else :
        sumBottom += -2.6
        #linebinW[cc].SetFillStyle(0)
        #linebinW[cc].SetBorderSize(0)
        #if cc > 2 :
        #    linebinW[cc].SetTextAngle(-90.);
        #linebinW[cc].Draw("same")

legend1.AddEntry(hist_total, "Uncertainty", "f")

#################################
if do_bottom :
    #if len(fin) > 1 :
    #    sys.exit("The unblind version with the 3 eras summed up still need to be fixed.")
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
        histtotal = hist_total #fin[0].Get((readFrom + "/" + name_total).replace("2018", str(era)) )
        lastbin += do_hist_total_err(
            hist_total_err,
            labelX, histtotal  ,
            options_plot_ranges("ttH")[typeCat]["minYerr"],
            options_plot_ranges("ttH")[typeCat]["maxYerr"],
            era
            ) # , readFrom, lastbin
        # hist_total_err, labelX, total_hist
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
            histtotal = fin[0].Get((readFrom + "/" + name_total).replace("2018", str(era)) )
            lastbin += err_data(
                dataTGraph2,
                hist_total,
                dataTGraph1,
                options.fromHavester,
                hist_total,
                readFrom,
                fin[0])
                #lastbin, histtotal) # readFrom,
            # dataTGraph1, template, dataTGraph, fromHavester, histtotal, folder, fin
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
if options.useLogPlot :
    oplin = "log"
    print ("made log")
optbin = "plain"
if divideByBinWidth :
    optbin = "divideByBinWidth"
#canvas.Print(options.odir+category+"_"+typeFit+"_"+optbin+"_unblind"+str(options.unblind)+"_"+oplin+".pdf")
#canvas.Close()

savepdf = options.odir+category+"_"+typeFit+"_"+optbin+"_"+options.nameOut+"_unblind"+str(options.unblind)+"_"+oplin + "_" + options.typeCat
print ("saving...")
dumb = canvas.SaveAs(savepdf + ".pdf")
print ("saved", savepdf + ".pdf")
del dumb
dumb = canvas.SaveAs(savepdf + ".root")
print ("saved", savepdf + ".root")
del dumb
dumb = canvas.SaveAs(savepdf + ".png")
print ("saved", savepdf + ".png")
del dumb
print ("saved", savepdf)
