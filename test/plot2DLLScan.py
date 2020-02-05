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
(options, args) = parser.parse_args()

to_do  = options.second
folder = options.outputFolder
to_do_first  = options.first

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


tf = TFile.Open(options.input, "READ")
tree = tf.Get("limit")

#to_do = sys.argv[2]
if to_do == "ttW" or to_do == "ttZ" : limitssecond = "-2,3"
else : limitssecond = "-10,10"

addLabel = options.label

doContours = True

tf3 = TFile.Open(options.input95, "READ")
if doContours :
    try: tree95 = tf3.Get("limit")
    except AttributeError or ReferenceError:
        doContours = False
else : tree95 = None

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

if doContours :
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
    bestfit = BestFit(tree68)
    gr68 = contourPlot(tree68, 0.310, 1.0, bestfit)
    gr68.SetLineWidth(2)
    gr68.SetLineStyle(1)
    gr68.SetLineColor(1)
    gr68.SetFillStyle(1001)
    gr68.SetFillColor(82)

    gr95 = contourPlot(tree95, 0.049, 1.0, bestfit)
    gr95.SetLineWidth(2)
    gr95.SetLineStyle(7)
    gr95.SetLineColor(1)
    gr95.SetFillStyle(1001)
    gr95.SetFillColor(89)

canv = TCanvas("canv", "canv", 600, 600)
canv.SetBottomMargin(0.10)
canv.SetLeftMargin(0.08)
canv.SetRightMargin(0.12)

tree.Draw("2*deltaNLL:r_" + to_do_first + ":r_"+to_do+">>hist(50,"+limitssecond+",50,-2,3)","2*deltaNLL<10","prof")

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
hist.GetYaxis().SetTitle("#mu_{t#bar{t}Z}")
hist.GetZaxis().SetTitleFont(43)
hist.GetZaxis().SetTitleSize(28)
hist.GetZaxis().SetTitle("-2#Delta lnL")

print "GetCorrelationFactor: %.3f" % hist.GetCorrelationFactor()

tree.Draw("r_" + to_do_first + ":r_"+to_do,"quantileExpected == -1","P same")
best_fit = gROOT.FindObject("Graph").Clone()
best_fit.SetMarkerSize(2)
best_fit.SetMarkerColor(0)
best_fit.SetMarkerStyle(34)
best_fit.Draw("p same")

bf_for_leg = best_fit.Clone()
bf_for_leg.SetMarkerStyle(28)
bf_for_leg.SetMarkerColor(1)

# bf_for_leg.Draw("p same")

sm_point = TGraph(1)
sm_point.SetPoint(0, 1, 1)
sm_point.SetMarkerSize(2)
sm_point.SetLineWidth(2)
sm_point.SetMarkerStyle(29)
sm_point.Draw("p same")

if doContours :
    gr95.Draw("L SAME")
    gr68.Draw("L SAME")

# hist.Draw("AXIS SAME")

lat = TLatex()
lat.SetNDC()
lat.SetTextFont(43)
lat.SetTextSize(32)
lat.DrawLatex(0.12, 0.92, "#bf{CMS} #it{Internal}")
lat.SetTextSize(26)
lat.DrawLatex(0.14, 0.845, "pp #rightarrow tH+t#bar{t}H, H #rightarrow WW*/ZZ*/#tau#tau")
lat.DrawLatex(0.14, 0.755, addLabel)

leg = TLegend(0.12, 0.15, .3, .3)
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.SetLineColor(0)
leg.SetTextFont(43)
leg.SetTextSize(18)
leg.AddEntry(bf_for_leg, "Best fit", 'P')
leg.AddEntry(sm_point, "SM expected", 'P')
if doContours :
    leg.AddEntry(gr68, "68% C.I.", 'L')
    leg.AddEntry(gr95, "95% C.I.", 'L')
leg.Draw()

if folder == "" :
    saveout = "nllscan_%s-vs_%s_%s.pdf" % (folder, to_do, to_do_first, options.plotName)
else :
    saveout = "%s/nllscan_%s-vs_%s_%s.pdf" % (folder, to_do, to_do_first, options.plotName)
print "SaveAs %s" % (saveout)
canv.SaveAs(saveout)
