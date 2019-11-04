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
from ROOT import TMultiGraph
from ROOT import TGraph
from ROOT import gPad

gROOT.SetBatch(1)

def drawlik(input, gr = TGraph(), color = 8, second = False) :
    print ("reading " + folder+"/"+input)
    tf2 = TFile.Open(folder+"/"+input, "READ")
    tree2 = tf2.Get("limit")
    bu = "P"
    if second : bu = "P same"
    tree2.Draw("2*deltaNLL:kappa_t>>hist(50,-3,3)","2*deltaNLL<20", bu)
    canv.Update();
    canv.Modified();
    gr = gROOT.FindObject("Graph").Clone()
    tf2.Close()
    gROOT.Reset()
    #hist = gDirectory.Get("hist")
    gr.GetXaxis().SetTitleFont(43)
    gr.GetYaxis().SetTitleFont(43)
    gr.GetXaxis().SetTitleSize(28)
    gr.GetYaxis().SetTitleSize(28)
    gr.GetXaxis().SetTitleOffset(0.8)
    gr.GetYaxis().SetTitleOffset(0.7)
    gr.GetXaxis().SetTitle("#kappa_t")
    gr.GetYaxis().SetTitle("-2#Delta lnL")
    #gr2.SetMarkerStyle(34)
    return gr

def colorset(gr = TGraph(), color = 8) :
    gr.SetMarkerSize(0.5)
    gr.SetMarkerColor(color)
    gr.SetLineColor(color)
    gr.SetLineWidth(4)


from optparse import OptionParser
parser = OptionParser()
parser.add_option("--input", type="string", dest="input", help="from grid in multidim fit", default="none")
parser.add_option("--label", type="string", dest="label", help="  Set ", default="test")

parser.add_option("--input2", type="string", dest="input2", help="from grid in multidim fit", default="none")
parser.add_option("--label2", type="string", dest="label2", help="  Set ", default="test")

parser.add_option("--input3", type="string", dest="input3", help="from grid in multidim fit", default="none")
parser.add_option("--label3", type="string", dest="label3", help="  Set ", default="test")

parser.add_option("--input4", type="string", dest="input4", help="from grid in multidim fit", default="none")
parser.add_option("--label4", type="string", dest="label4", help="  Set ", default="test")

parser.add_option("--input5", type="string", dest="input5", help="from grid in multidim fit", default="none")
parser.add_option("--label5", type="string", dest="label5", help="  Set ", default="test")

parser.add_option("--input6", type="string", dest="input6", help="from grid in multidim fit", default="none")
parser.add_option("--label6", type="string", dest="label6", help="  Set ", default="test")

parser.add_option("--outputFolder", type="string", dest="outputFolder", help="  Set ", default="multilep_3l_withTH_withMET_only_CRs_2017")
(options, args) = parser.parse_args()

folder = options.outputFolder

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

canv = TCanvas("canv", "canv", 600, 600)
canv.SetBottomMargin(0.1)
canv.SetLeftMargin(0.1)
canv.SetRightMargin(0.1)

leg = TLegend(0.14, 0.55, .5, .8)
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.SetLineColor(0)
leg.SetTextFont(43)
leg.SetTextSize(18)
leg.SetHeader("no BKG floating")
#leg.SetHeader("ttW BKG floating")
#leg.SetHeader("2lss (ttW floating)")

mg = TMultiGraph()

entries = 0
if options.input != "none" :
    gr1 = TGraph()
    dumb = drawlik(options.input, gr = gr1, color = 53, second = False)
    gr1 = dumb.Clone()
    gr1.GetYaxis().SetRangeUser(0.,3.)
    gr1.Draw("Ap")
    mg.Add(gr1)
    colorset(gr = gr1, color = 53)
    leg.AddEntry(gr1, options.label, 'Lp')
    entries += 1

if options.input2 != "none" :
    gr2 = TGraph()
    dumb = TGraph()
    dumb = drawlik(options.input2, gr = gr2, color = 8)
    gr2 = dumb.Clone()
    gr2.GetYaxis().SetRangeUser(0.,3.)
    gr2.Draw("p, same")
    mg.Add(gr2)
    colorset(gr = gr2, color = 6)
    leg.AddEntry(gr2, options.label2, 'Lp')
    entries += 1

if options.input3 != "none" :
    gr3 = TGraph()
    dumb = drawlik(options.input3, gr = gr3, color = 93, second = True)
    gr3 = dumb.Clone()
    gr3.GetYaxis().SetRangeUser(0.,3.)
    gr3.Draw("p, same")
    #gr3.Draw("p, same")
    mg.Add(gr3)
    colorset(gr = gr3, color = 93)
    leg.AddEntry(gr3, options.label3, 'Lp')
    entries += 1

if options.input4 != "none" :
    gr4 = TGraph()
    dumb = drawlik(options.input4, gr = gr4, color = 2, second = True)
    gr4 = dumb.Clone()
    gr4.GetYaxis().SetRangeUser(0.,3.)
    gr4.Draw("p, same")
    mg.Add(gr4)
    colorset(gr = gr4, color = 2)
    leg.AddEntry(gr4, options.label4, 'Lp')
    entries += 1

if options.input5 != "none" :
    gr5 = TGraph()
    dumb = drawlik(options.input5, gr = gr5, color = 6, second = True)
    gr5 = dumb.Clone()
    gr5.GetYaxis().SetRangeUser(0.,3.)
    gr5.Draw("p, same")
    mg.Add(gr5)
    colorset(gr = gr5, color = 8)
    leg.AddEntry(gr5, options.label5, 'Lp')
    entries += 1

if options.input6 != "none" :
    gr6 = TGraph()
    dumb = drawlik(options.input6, gr = gr6, color = 1, second = True)
    gr6 = dumb.Clone()
    gr6.GetYaxis().SetRangeUser(0.,3.)
    gr5.Draw("p, same")
    mg.Add(gr6)
    colorset(gr = gr6, color = 1)
    leg.AddEntry(gr6, options.label6, 'Lp')
    entries += 1

#canv.Update()
#mg.GetXaxis().SetTitle("#kappa_t (no kinematics)")
#mg.GetYaxis().SetTitle("-2#Delta lnL")
#gPad.Modified()
#mg.GetYaxis().SetRangeUser(0.,3.)


mg.SetTitle("Multi-graph Title; X-axis Title; Y-axis Title");
mg.Draw('apl, same')
canv.Update()
mg.GetXaxis().SetTitle("#kappa_t (no kinematics)")
mg.GetYaxis().SetTitle("-2#Delta lnL")
gPad.Modified()
mg.GetYaxis().SetRangeUser(0.,22.)

#mg.Draw('ap')

lat = TLatex()
lat.SetNDC()
lat.SetTextFont(43)
lat.SetTextSize(32)
lat.DrawLatex(0.12, 0.92, "#bf{CMS} #it{Internal}")
lat.SetTextSize(26)
lat.DrawLatex(0.14, 0.845, "pp #rightarrow tH+t#bar{t}H, H #rightarrow WW*/ZZ*/#tau#tau")
##lat.DrawLatex(0.14, 0.8, "2lss only - ttH-sel + ttW-sel")
#lat.DrawLatex(0.14, 0.755, addLabel)

leg.Draw('same')

if entries == 1 :
    canv.SaveAs(folder+"/kappa_nllscan_" + options.label + ".pdf")
    canv.SaveAs(folder+"/kappa_nllscan_" + options.label + ".C")
else :
    canv.SaveAs(folder+"/kappa_nllscan_2lss_1tau.pdf")
    canv.SaveAs(folder+"/kappa_nllscan_2lss_1tau.C")
#canv.SaveAs("/nllscan_tH-vs_ttH.png")
#canv.SaveAs("/nllscan_tH-vs_ttH.C")
