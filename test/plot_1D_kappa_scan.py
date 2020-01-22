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
from ROOT import TLine
from ROOT import TMultiGraph
from ROOT import TGraph
from ROOT import gPad
from root_numpy import tree2array
import pandas as pd

gROOT.SetBatch(1)

#####
## python test/plot_1D_kappa_scan.py --input higgsCombinekt_scan_ttH_2lss_BDT_2017.MultiDimFit.mH125.root --label ttH_2lss_BDT_2017 --outFolder datacards/ttH_2lss_0tau_test/BDT_RunII//results/ --input2 higgsCombinekt_scan_ttH_2lss_NN_2017.MultiDimFit.mH125.root --label2 ttH_2lss_NN_2017 --outFolder2 datacards/ttH_2lss_0tau_test/DNNSubCat2_BIN_RunII/results/  --channel 2lss0tau -n BDTvsNN
#####


def drawlik(input, gr = TGraph(), color = 8, second = False, Folder = "") :
    print ("reading " + Folder+"/"+input)
    tf2 = TFile.Open(Folder+"/"+input, "READ")
    tree2 = tf2.Get("limit")
    bu = "P"
    if second : bu = "P same"
    tree2.Draw("2*deltaNLL:kappa_t>>hist(50,-3,3)","2*deltaNLL<50", bu)
    canv.Update();
    canv.Modified();
    gr = gROOT.FindObject("Graph").Clone()
    gr.Sort()
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

def SaveCSV(inputfile, Folder):
    # Load dataset to .csv format file
    variables = ['kappa_t','deltaNLL']
    my_cols_list=['fname', 'cv', 'cf', 'cosa','ratio','rescalecv','rescalect','bestfitr','dnll']
    data = pd.DataFrame(columns=my_cols_list)
    try: tfile = TFile(Folder+"/"+inputfile)
    except:
        print(" file "+ Folder+"/"+inputfile+" doesn't exits ")
    try: tree = tfile.Get("limit")
    except:
        print (" limit tree doesn;t exists in " + Folder+"/"+inputfile)
    
    if tree is not None:
        try: chunk_arr = tree2array(tree=tree) # Can use  start=first entry, stop = final entry desired
        except :
            print(" fail to convert tree to array ") 
        else :
            chunk_df = pd.DataFrame(chunk_arr, columns=variables)
            data['ratio']=chunk_df["kappa_t"]
            data['rescalect']=chunk_df["kappa_t"]
            data['dnll']=chunk_df["deltaNLL"]
            data['fname']= inputfile
            data['cv']=1.0
            data['cf']=1.0
            data['cosa']=1.0
            data['rescalecv']=1.0
            data['bestfitr']=1.0
    data.to_csv("{}/{}.csv".format(Folder, inputfile.split(".")[0]), index=False)


from optparse import OptionParser
parser = OptionParser()
parser.add_option("--input", type="string", dest="input", help="from grid in multidim fit", default="none")
parser.add_option("--label", type="string", dest="label", help="  Set ", default="test")
parser.add_option("--outFolder", type="string", dest="outFolder", help="the input folder of input1 and the outputfolder", default="none")

parser.add_option("--input2", type="string", dest="input2", help="from grid in multidim fit", default="none")
parser.add_option("--label2", type="string", dest="label2", help="  Set ", default="test")
parser.add_option("--outFolder2", type="string", dest="outFolder2", help="the input folder of input2", default="none")

parser.add_option("--input3", type="string", dest="input3", help="from grid in multidim fit", default="none")
parser.add_option("--label3", type="string", dest="label3", help="  Set ", default="test")
parser.add_option("--outFolder3", type="string", dest="outFolder3", help="the input folder of input3", default="none")

parser.add_option("--input4", type="string", dest="input4", help="from grid in multidim fit", default="none")
parser.add_option("--label4", type="string", dest="label4", help="  Set ", default="test")
parser.add_option("--outFolder4", type="string", dest="outFolder4", help="the input folder of input4", default="none")

parser.add_option("--input5", type="string", dest="input5", help="from grid in multidim fit", default="none")
parser.add_option("--label5", type="string", dest="label5", help="  Set ", default="test")
parser.add_option("--outFolder5", type="string", dest="outFolder5", help="the input folder of input5", default="none")

parser.add_option("--input6", type="string", dest="input6", help="from grid in multidim fit", default="none")
parser.add_option("--label6", type="string", dest="label6", help="  Set ", default="test")
parser.add_option("--outFolder6", type="string", dest="outFolder6", help="the input folder of input6", default="none")

parser.add_option("--outputFolder", type="string", dest="outputFolder", help="  Set ", default="multilep_3l_withTH_withMET_only_CRs_2017")
parser.add_option("--channel", type="string", dest="channel", help="  channel ", default="2lss_0tau")
parser.add_option("-n", "--name", type="string", dest="name", help="  name ", default="NNvsBDT")


(options, args) = parser.parse_args()

folder = options.outputFolder


gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

canv = TCanvas("canv", "canv", 600, 600)
canv.SetBottomMargin(0.1)
canv.SetLeftMargin(0.1)
canv.SetRightMargin(0.1)


leg = TLegend(0.4, 0.7, .6, .8)
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.SetLineColor(0)
leg.SetTextFont(43)
leg.SetTextSize(18)
leg.SetHeader(options.channel)

#leg.SetHeader("ttW BKG floating")
#leg.SetHeader("2lss (ttW floating)")



mg = TMultiGraph()

entries = 0
if options.input != "none" :
    if options.outFolder =="none":
        gr1 = TGraph()
        dumb = drawlik(options.input, gr = gr1, color = 53, second = False, Folder = folder)
        gr1 = dumb.Clone()
        gr1.GetYaxis().SetRangeUser(0.,3.)
        gr1.Draw("Ap")
        mg.Add(gr1)
        colorset(gr = gr1, color = 53)
        leg.AddEntry(gr1, options.label, 'Lp')
        entries += 1
    else:
        gr1 = TGraph()
        dumb = drawlik(options.input, gr = gr1, color = 53, second = False, Folder = options.outFolder)
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
    dumb = drawlik(options.input2, gr = gr2, color = 8, second = False, Folder = options.outFolder2)
    gr2 = dumb.Clone()
    gr2.GetYaxis().SetRangeUser(0.,3.)
    gr2.Draw("p, same")
    mg.Add(gr2)
    colorset(gr = gr2, color = 6)
    leg.AddEntry(gr2, options.label2, 'Lp')
    entries += 1

if options.input3 != "none" :
    gr3 = TGraph()
    dumb = drawlik(options.input3, gr = gr3, color = 93, second = False, Folder = options.outFolder3)
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
    dumb = drawlik(options.input4, gr = gr4, color = 2, second = False, Folder = options.outFolder4)
    gr4 = dumb.Clone()
    gr4.GetYaxis().SetRangeUser(0.,3.)
    gr4.Draw("p, same")
    mg.Add(gr4)
    colorset(gr = gr4, color = 2)
    leg.AddEntry(gr4, options.label4, 'Lp')
    entries += 1

if options.input5 != "none" :
    gr5 = TGraph()
    dumb = drawlik(options.input5, gr = gr5, color = 6, second = False, Folder = options.outFolder5)
    gr5 = dumb.Clone()
    gr5.GetYaxis().SetRangeUser(0.,3.)
    gr5.Draw("p, same")
    mg.Add(gr5)
    colorset(gr = gr5, color = 8)
    leg.AddEntry(gr5, options.label5, 'Lp')
    entries += 1

if options.input6 != "none" :
    gr6 = TGraph()
    dumb = drawlik(options.input6, gr = gr6, color = 1, second = False, Fodler = options.outFolder6)
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

mg.GetYaxis().SetRangeUser(0.,55.)
xmin = mg.GetXaxis().GetXmin()
xmax = mg.GetXaxis().GetXmax()
mg.GetXaxis().SetRangeUser(xmin,xmax)


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

line1 = TLine(xmin,1, xmax, 1)
line1.SetLineStyle(2)
line2 = TLine(xmin,4, xmax, 4)
line2.SetLineStyle(2)
line3 = TLine(xmin,9, xmax, 9)
line3.SetLineStyle(2)
line4 = TLine(xmin,16, xmax, 16)
line4.SetLineStyle(2)
line5 = TLine(xmin,25, xmax, 25)
line5.SetLineStyle(2)
line1.Draw('same')
line2.Draw('same')
line3.Draw('same')
line4.Draw('same')
line5.Draw('same')

if entries == 1 :
    canv.SaveAs(folder+"/kappa_nllscan_" + options.label + ".pdf")
    canv.SaveAs(folder+"/kappa_nllscan_" + options.label + ".C")
    SaveCSV(options.input, Folder = folder)
else :
    canv.SaveAs(options.outFolder+"/kappa_nllscan_%s_%s.pdf"%(options.channel,options.name))
    canv.SaveAs(options.outFolder+"/kappa_nllscan_%s_%s.C"%(options.channel,options.name))
#canv.SaveAs("/nllscan_tH-vs_ttH.png")
#canv.SaveAs("/nllscan_tH-vs_ttH.C")
