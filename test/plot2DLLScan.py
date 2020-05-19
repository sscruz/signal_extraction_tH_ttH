import sys
from ROOT import gROOT
from ROOT import gStyle
from ROOT import gDirectory
from ROOT import TFile
from ROOT import TCanvas
from ROOT import TGraph
from ROOT import TLegend
from ROOT import TH2F
from ROOT import TLatex
from ROOT import TGraph2D

from functools import partial
from collections import namedtuple
from scipy.interpolate import splev, splrep
from scipy.interpolate import griddata
from scipy.interpolate import interp2d
import scipy.ndimage
#import scipy.interpolate as interp
from scipy import interpolate
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib import path as mpath
import pandas as pd

gROOT.SetBatch(1)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--first", type="string", dest="first", help="from grid in multidim fit", default="ttH")
parser.add_option("--second", type="string", dest="second", help="from grid in multidim fit", default="none")
parser.add_option("--label", type="string", dest="label", help="from grid in multidim fit", default="none")
parser.add_option("--plotName", type="string", dest="plotName", help="from grid in multidim fit", default="none")
parser.add_option("--outputFolder", type="string", dest="outputFolder", help="  Set ", default="")
parser.add_option("--input", type="string", dest="input", help="from grid in multidim fit", default="none")
parser.add_option("--input68", type="string", dest="input68", help="from grid in multidim fit", default="none")
parser.add_option("--input95", type="string", dest="input95", help="from grid in multidim fit", default="none")
parser.add_option("--fromGrid", action="store_true", dest="fromGrid", help="Take the contours from ready TGraph (from Oviedo script -- not automatic from combine)\n It still takes the center from combine directly.", default=False)
parser.add_option("--input68_forBestFit", type="string", dest="input68_forBestFit", help="from grid in multidim fit", default="none")

(options, args) = parser.parse_args()

to_do  = options.second
folder = options.outputFolder
to_do_first  = options.first
fromGrid = options.fromGrid

def print_header(axes, x_low, x_high, y_low, y_high, inside = False, logscale = False):
  y_val = y_high + 0.015 * (y_high - y_low)
  if inside:
    axes.text(x_low + abs(x_low) * 0.045, y_high - 0.46 * (y_high - y_low), 'CMS', style='normal', fontsize=15, fontweight='bold')
  else:
    axes.text(x_low, y_val, 'CMS', style='normal', fontsize=14, fontweight='bold') # 15 for a 6 X 6 figure
  #axes.text(x_low + (x_high - x_low) * 0.14, y_val, 'Preliminary', fontsize=15, style='italic') # for a 6 X 6 figure
  axes.text(x_low + (x_high - x_low) * 0.15, y_val, 'Preliminary', fontsize=14, style='italic') # for a 5 X 5 figure
  if logscale:
    axes.text(x_low + (x_high - x_low) * 0.67, y_high + 0.05 * (y_high - y_low), '137.2 fb$^{-1}$ (13 TeV)', fontsize=12)
  else:
    axes.text(x_low + (x_high - x_low) * 0.57, y_high + 0.01 * (y_high - y_low), '137.2 fb$^{-1}$ (13 TeV)', fontsize=12)


if folder == "" :
    saveout = "nllscan_%s-vs_%s_%s.pdf" % (folder, to_do, to_do_first, options.plotName)
else :
    saveout = "%s/nllscan_%s-vs_%s_%s.pdf" % (folder, to_do, to_do_first, options.plotName)
print "Will saveAs %s" % (saveout)

def BestFit(tree):
    n = tree.Draw( "r_" + to_do_first + ":r_"+to_do, "quantileExpected == -1", "")
    gr = gROOT.FindObject("Graph").Clone()
    bestFit = (gr.GetX()[0], gr.GetY()[0])
    print "BestFit from tree68: (%s, r_%s)" % (to_do, to_do_first), bestFit
    return bestFit

def contourPlot(tree, pmin, pmax, bestFit=(10.1, 1.5)):
    n = tree.Draw("r_" + to_do_first + ":r_"+to_do, "%f <= quantileExpected && quantileExpected <= %f && quantileExpected != 1" % (pmin,pmax), "")
    print "Drawing for r_%s:%s, %f <= quantileExpected && quantileExpected <= %f && quantileExpected != 1 yielded %d points" % (to_do_first, to_do,pmin, pmax, n)
    gr = gROOT.FindObject("Graph").Clone()

    xi = gr.GetX()
    yi = gr.GetY()
    npoints = gr.GetN()
    for i in range(npoints):
       xi[i] -= bestFit[0]
       yi[i] -= bestFit[1]

    def compArg(i, j):
        return 1 if TGraph.CompareArg(gr, i, j) else -1

    sorted_points = sorted(range(npoints), cmp=compArg)
    sorted_graph = TGraph(npoints+1)
    for n,i in enumerate(sorted_points):
        sorted_graph.SetPoint(n, xi[i], yi[i])
    sorted_graph.SetPoint(npoints, xi[sorted_points[0]],
                                   yi[sorted_points[0]])

    xi_sorted = sorted_graph.GetX()
    yi_sorted = sorted_graph.GetY()

    for i in range(npoints+1):
       xi_sorted[i] += bestFit[0]
       yi_sorted[i] += bestFit[1]

    return sorted_graph

#to_do = sys.argv[2]
if to_do == "ttW" or to_do == "ttZ" :
    minY = -1
    maxY = 3
    textX = -0.8
    limitssecond = "-1,3"
else :
    minY = -8
    maxY = 18
    textX = -7
    limitssecond = "-8,18"

if fromGrid :
    poi2 = ('r_%s' % to_do_first , -1,3)
    poi1 = ("r_%s" % to_do, minY,maxY)
    tf = TFile.Open(options.input)
    th2 = TH2F('scan_%s_%s'%(poi1[0],poi2[0]), '', 1000, poi1[1],poi1[2], 1000, poi2[1],poi2[2])
    data = []
    for ev in tf.Get("limit"):
        p1 = getattr(ev, poi1[0])
        p2 = getattr(ev, poi2[0])
        deltaNLL = 2*ev.deltaNLL

        bin = th2.FindBin(p1,p2)
        #print ("bins", p1,p2,deltaNLL)

        if th2.GetBinContent(bin):
            #raise RuntimeError("Bin has already been filled, you need a finer binning")
            continue
        th2.SetBinContent(bin, deltaNLL)
        if deltaNLL == 0 : continue

        data.append((p1, p2, deltaNLL))

    datapd = pd.DataFrame(data, columns=('x1', 'y1', 'z1'))
    datapd = datapd.fillna(0.)
    datapd.sort_values(by=[ 'z1', 'x1',  'y1', ])
    x2, y2 = np.meshgrid(datapd["x1"].values, datapd["y1"].values, sparse=False)
    xnew, ynew = np.mgrid[-8:18:170j, -1:3:170j]
    znew =  griddata((datapd["x1"].values, datapd["y1"].values), datapd["z1"].values, (xnew, ynew ), method='cubic') #
    idxmin = datapd.z1.idxmin()
    print (np.min(datapd.z1), datapd.loc[idxmin].z1, datapd.loc[idxmin].x1, datapd.loc[idxmin].y1)

    fig, ax = plt.subplots(figsize=(5, 5))
    levels = [2.3, 5.99]
    CS = ax.contour(xnew, ynew, znew, levels, colors='k', linestyles=['solid', 'dashed'] )

    x_low, x_high = minY, maxY
    y_low, y_high = -1, 3
    ax.set_xlim(x_low, x_high)
    ax.set_ylim(y_low, y_high)

    ax.set_ylabel("$\\mu_\\mathrm{%s}$" % to_do_first , fontsize=16, labelpad=10)
    ax.set_xlabel("$\\mu_{\\mathrm{%s}}$" % to_do, fontsize=16, labelpad=10)
    print_header(ax, x_low, x_high, y_low, y_high)
    line_SM = ax.scatter([1], [1], marker="*", label="SM expected", s=50, c='k')
    line_BF = ax.scatter(datapd.loc[idxmin].x1, datapd.loc[idxmin].y1, s=50, marker='$\\diamond$', label="Best fit", c='k')

    ax.text(textX, 2.7, "$pp \\rightarrow tH+t\\bar{t}H, H \\rightarrow WW^{*}/ZZ^{*}/\\tau\\tau$", fontsize=15)
    line_up, = plt.plot([-10, -15], ls='-', color='k',label="68% C.l.")
    line_down, = ax.plot([-10, -15], ls='--', color='k',label="95% C.l.")
    #
    legend = plt.legend(handles=[line_up, line_down, line_BF], loc='lower left', title="Observed", frameon=True, framealpha=1.0, fontsize=12, scatterpoints=1)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_linewidth(0)
    #
    legend2 = plt.legend(handles=[ line_SM], loc='lower right', title="", frameon=True, framealpha=1.0, fontsize=12, scatterpoints=1)
    legend2.get_frame().set_facecolor('white')
    legend2.get_frame().set_linewidth(0)
    ax.add_artist(legend)
    ax.add_artist(legend2)
    plt.savefig(saveout, bbox_inches='tight')
    print ("saved ", saveout)
    sys.exit()
else :
    tf = TFile.Open(options.input, "READ")
    tree = tf.Get("limit")

addLabel = options.label
doContours = True

if not fromGrid :
    tf3 = TFile.Open(options.input95, "READ")
    if doContours:
        try: tree95 = tf3.Get("limit")
        except AttributeError or ReferenceError:
            doContours = False
    else : tree95 = None

if not fromGrid :
    tf2 = TFile.Open(options.input68, "READ")
    if doContours :
        try:  tree68 = tf2.Get("limit")
        except AttributeError or ReferenceError:
            doContours = False
    else : tree68 = None


    try:
        print "%s tree loaded from %s" % (tree.GetName(), options.input)
    except AttributeError:
        print "tree not found!"
        sys.exit(-1)

if doContours and not fromGrid :
    try:
        print "%s tree loaded from %s" % (tree68.GetName(), options.input68)
    except AttributeError:
        doContours = False

    try:
        print "%s tree loaded from %s" % (tree95.GetName(), options.input95)
    except AttributeError:
        doContours = False

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

if doContours :
    if not fromGrid :
        bestfit = BestFit(tree68)
        gr68 = contourPlot(tree68, 0.310, 1.0, bestfit)
        gr68.SetLineWidth(2)
        gr68.SetLineStyle(1)
        gr68.SetLineColor(1)
        gr68.SetFillStyle(1001)
        gr68.SetFillColor(82)
        #####
        gr95 = contourPlot(tree95, 0.049, 1.0, bestfit)
        gr95.SetLineWidth(2)
        gr95.SetLineStyle(7)
        gr95.SetLineColor(1)
        gr95.SetFillStyle(1001)
        gr95.SetFillColor(89)
    else :
        #gr68 = TGraph()
        #gr68 = tree68
        #bestfit = BestFit(tfBF)
        graph = TGraph2D(th2)
        xbinsize = 0.05; ybinsize = 0.05

        graph.SetNpx( int((graph.GetXmax() - graph.GetXmin())/xbinsize) )
        graph.SetNpy( int((graph.GetYmax() - graph.GetYmin())/ybinsize) )

        kk = graph.GetHistogram()

canv = TCanvas("canv", "canv", 600, 600)
canv.SetBottomMargin(0.10)
canv.SetLeftMargin(0.08)
canv.SetRightMargin(0.12)
if fromGrid :
    graph.Draw('colz')
    #c.SaveAs('plot.pdf')
    gr68 = graph.GetContourList(2.3/2)
    #for keyO in gr68list.GetListOfKeys() :
    #    obj =  keyO.ReadObj()
    #    print type(obj)
    #    print keyO.GetName()
    #gr68list.Draw()
    #gr68 = gROOT.FindObject("hPt").Clone() # gr68list.FindObject("hPt");
    #gr68.SetLineWidth(2)
    #gr68.SetLineStyle(1)
    #gr68.SetLineColor(1)
    #gr68.SetFillStyle(1001)
    #gr68.SetFillColor(82)

    gr95 = graph.GetContourList(5.99/2)
    #print (gr95)
    #gr95.SetLineWidth(2)
    #gr95.SetLineStyle(7)
    #gr95.SetLineColor(1)
    #gr95.SetFillStyle(1001)
    #gr95.SetFillColor(89)
else :
    tree.Draw("2*deltaNLL:r_" + to_do_first + ":r_"+to_do+">>hist(50,"+limitssecond+",50,-1,3)","2*deltaNLL<10","prof")
    hist = gDirectory.Get("hist")
    hist.SetMarkerColor(0)
    hist.GetXaxis().SetTitleFont(43)
    hist.GetYaxis().SetTitleFont(43)
    hist.GetXaxis().SetTitleSize(28)
    hist.GetYaxis().SetTitleSize(28)
    hist.GetXaxis().SetTitleOffset(0.8)
    hist.GetYaxis().SetTitleOffset(0.7)
    hist.GetZaxis().SetTitleOffset(0.5)
    hist.GetXaxis().SetTitle("#mu_{"+to_do.replace("r_","")+"}")
    #hist.GetYaxis().SetTitle("#mu_{t#bar{t}Z}")
    hist.GetYaxis().SetTitle("#mu_{t#bar{t}H}")
    #hist.GetYaxis().SetTitle("#mu_{t#bar{t}W}")
    hist.GetZaxis().SetTitleFont(43)
    hist.GetZaxis().SetTitleSize(28)
    hist.GetZaxis().SetTitle("-2#Delta lnL")
    print "GetCorrelationFactor: %.3f" % hist.GetCorrelationFactor()

if not fromGrid :
    tree.Draw("r_" + to_do_first + ":r_"+to_do,"quantileExpected == -1","P same")
    best_fit = gROOT.FindObject("Graph").Clone()
    best_fit.SetMarkerSize(2)
    best_fit.SetMarkerColor(0)
    best_fit.SetMarkerStyle(34)
    best_fit.Draw("p same")

    bf_for_leg = best_fit.Clone()
    bf_for_leg.SetMarkerStyle(28)
    bf_for_leg.SetMarkerColor(1)

    bf_for_leg.Draw("p same")

sm_point = TGraph(1)
sm_point.SetPoint(0, 1, 1)
sm_point.SetMarkerSize(2)
sm_point.SetLineWidth(2)
sm_point.SetMarkerStyle(29)
sm_point.Draw("p same")

if doContours :
    gr95.Draw("L SAME")
    gr68.Draw("L SAME")
    gr68.SetLineWidth(2)

# hist.Draw("AXIS SAME")

lat = TLatex()
lat.SetNDC()
lat.SetTextFont(43)
lat.SetTextSize(32)
lat.DrawLatex(0.12, 0.92, "#bf{CMS} #it{Internal}")
lat.SetTextSize(26)
lat.DrawLatex(0.14, 0.845, "pp #rightarrow tH+t#bar{t}H, H #rightarrow WW*/ZZ*/#tau#tau")
if not addLabel == "test" :
    lat.DrawLatex(0.14, 0.755, addLabel)

leg = TLegend(0.12, 0.15, .3, .3)
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.SetLineColor(0)
leg.SetTextFont(43)
leg.SetTextSize(18)
if not fromGrid :
    leg.AddEntry(bf_for_leg, "Best fit", 'P')
leg.AddEntry(sm_point, "SM expected", 'P')
if doContours :
    leg.AddEntry(gr68, "68% C.I.", 'L')
    leg.AddEntry(gr95, "95% C.I.", 'L')
leg.Draw()


canv.SaveAs(saveout)
