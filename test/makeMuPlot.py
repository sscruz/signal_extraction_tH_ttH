#!/usr/bin/env python
import os, subprocess, sys
from array import array
import CombineHarvester.CombineTools.ch as ch
from ROOT import *
from math import sqrt, sin, cos, tan, exp
import numpy as np
import glob
workingDir = os.getcwd()
execfile("python/data_manager_makePostFitPlots.py")
from collections import OrderedDict

## type 1

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--input_folder", type="string", dest="input_folder", help="Where the ", default="categories_comb_2017/")
# combined
# combined stats only
# era
(options, args) = parser.parse_args()

input_folder = options.input_folder

dprocs = OrderedDict()
#dprocs["ttW"]           = [[], 12.25, "ttW"]
#dprocs["ttZ"]           = [[], 10.25, "ttZ"]
dprocs["ttH_1l_1tau"]    = [[], 14.25, "1l + 1#tau_{h}"]
dprocs["ttH_0l_2tau"]    = [[], 12.75, "0l + 2#tau_{h}"]
dprocs["ttH_2los_1tau"]  = [[], 11.25, "2los + 1#tau_{h}"]
dprocs["ttH_1l_2tau"]    = [[], 9.75, "1l + 2#tau_{h}"]
dprocs["ttH_2lss_0tau"]  = [[], 8.25, "2lss + 0#tau_{h}"]
dprocs["ttH_2lss_1tau"]  = [[], 6.75, "2lss + 1#tau_{h}"]
dprocs["ttH_2l_2tau"]    = [[], 5.25, "2l + 2#tau_{h}"]
dprocs["ttH_3l_0tau"]    = [[], 3.75, "3l + 0#tau_{h}"]
dprocs["ttH_3l_1tau"]    = [[], 2.25, "3l + 1#tau_{h}"]
dprocs["ttH_4l"]         = [[], 0.75, "4l + 0#tau_{h}"]

for key in dprocs.keys() :
    ## ttH_ttH_4l_0tau_ttHmultilep_2018_3.3601728.0.out
    ## take rate instead
    my_file_pattern =  os.path.join(input_folder, "*rate_%s*.log" % (key)) #"%s/ttH_%s_rate.txt" % (input_folder, key)
    #my_file = os.path.join(input_folder, "ttH_%s*.out" % (key))
    my_files = glob.glob(my_file_pattern)
    if not len(my_files) > 0 :
        dprocs[key][0] = [1, 1, 1]
        print ("did not found pattern:", my_file_pattern)
        continue
    my_file = my_files[len(my_files) - 1]
    print ("reading:", my_file)
    try: open(my_file, 'r')
    except :
        dprocs[key][0] = [1, 1, 1]
        print ("Could not open the file:", my_file)
        continue
    with open(my_file, 'r') as in_file :
      for line in in_file :
        if "r_ttH :" in line :
            for li in line.split() :
                try: float(li)
                except ValueError:
                    for li2 in li.split("/") :
                        try: float(li2)
                        except ValueError: continue
                        print float(li2)
                        dprocs[key][0].append(float(li2))
                    continue
                print li
                dprocs[key][0].append(float(li))
    if not len(dprocs[key][0]) > 0 :
        print ("file did not had rate written ", my_file)
        dprocs[key][0] = [1, 1, 1]
print " "
### read combined
my_file = "%s/../ttHmultilep_2017_rate_asimov_ttH.log" % (input_folder)
print ("reading:", my_file)
combined = []
print "Combined: "
with open(my_file, 'r') as in_file :
  for line in in_file :
    if "r_ttH :" in line :
        for li in line.split() :
            try: float(li)
            except ValueError:
                for li2 in li.split("/") :
                    try: float(li2)
                    except ValueError: continue
                    #print float(li2)
                    combined = combined + [float(li2)]
                continue
            print li
            combined = combined + [float(li)]
print combined
### read combined
my_file = "%s/../ttHmultilep_2018_rate_asimov_ttH.log" % (input_folder)
combined_stas_only = []
print "Combined stat only: "
with open(my_file, 'r') as in_file :
  for line in in_file :
    if "r_ttH :" in line :
        for li in line.split() :
            try: float(li)
            except ValueError:
                for li2 in li.split("/") :
                    try: float(li2)
                    except ValueError: continue
                    #print float(li2)
                    combined_stas_only = combined_stas_only + [float(li2)]
                continue
            print li
            combined_stas_only = combined_stas_only + [float(li)]
print combined_stas_only



########################
y_comb = 7.5
mu_comb_p1s_stat = combined_stas_only[2]
mu_comb_m1s_stat = abs(combined_stas_only[1])
mu_comb_p1s = combined[2]
mu_comb_m1s = abs(combined[1])
gr_mu_comb_stat = TGraphAsymmErrors()
gr_mu_comb_stat.SetPoint(0,combined_stas_only[0],y_comb)
gr_mu_comb_stat.SetPointError(0,abs(combined_stas_only[1]),combined_stas_only[2],y_comb,y_comb)
gr_mu_comb_stat.SetLineWidth(2)
gr_mu_comb_stat.SetMarkerSize(0)
gr_mu_comb_stat.SetFillColor(8) #ROOT.kGreen+2)

gr_mu_comb_syst = TGraphAsymmErrors()
gr_mu_comb_syst.SetPoint(0,combined[0],y_comb)
gr_mu_comb_syst.SetPointError(0,abs(combined[1]),combined[2],y_comb,y_comb)
gr_mu_comb_syst.SetLineWidth(2)
gr_mu_comb_syst.SetMarkerSize(0)
gr_mu_comb_syst.SetFillColor(5) #ROOT.kGreen)

gr_mu_comb = TGraphAsymmErrors()
gr_mu_comb.SetPoint(0,combined[0],y_comb)
gr_mu_comb.SetPointError(0,0,0,y_comb,y_comb)
gr_mu_comb.SetLineWidth(3)
gr_mu_comb.SetLineColor(1)
gr_mu_comb.SetMarkerSize(1)
gr_mu_comb.SetMarkerColor(1)

mg = TMultiGraph()
mg.Add(gr_mu_comb, "PL")
mg.Add(gr_mu_comb_syst, "E2")
mg.Add(gr_mu_comb_stat, "E2")
for kk, key in enumerate(dprocs.keys()) :
    gr_mu = TGraphAsymmErrors()
    gr_mu.SetPoint(0,dprocs[key][0][0], dprocs[key][1])
    gr_mu.SetPointError(0, abs(dprocs[key][0][2]), dprocs[key][0][1],0,0)
    gr_mu.SetLineWidth(3)
    gr_mu.SetLineColor(2) #ROOT.kRed)
    gr_mu.SetMarkerStyle(21)
    gr_mu.SetMarkerSize(1.5)
    mg.Add(gr_mu, "P")
#################################

c = TCanvas("c","c",750,700)
#c = TCanvas("c","c",800,750)
c.SetLeftMargin(0.25)
c.SetBottomMargin(0.15)

gStyle.SetEndErrorSize(0)
mg.Draw("A")
gPad.RedrawAxis()

xmin = -2.8 #-2.8
ymax = 17. # 12.
ylinemax = 14. # 10.0


mg.GetXaxis().SetLimits(xmin,5.0)
mg.GetYaxis().SetRangeUser(0, ymax)
mg.GetYaxis().SetLabelSize(0)
mg.GetYaxis().SetTickSize(0)
mg.GetXaxis().SetTitle("Best fit #mu(t#bar{t}H)")
mg.GetXaxis().SetTitleOffset(1.5)
mg.GetYaxis().SetTitle("")
mg.GetYaxis().SetTitleSize(0.)
mg.GetYaxis().SetLabelSize(0.)
mg.GetYaxis().SetTickLength(0.)
mg.GetYaxis().SetTickSize(0.)
mg.Draw("A")

link = TLine(combined[0], 0, combined[0], ylinemax)
link.SetLineWidth(2)
link.SetLineColor(1)
link.Draw()

luminosity=41400
tex = TLatex()
luminosity=41400
tex.SetTextSize(0.035)
tex.SetTextFont(61)
tex.DrawLatexNDC(0.26, 0.91, "CMS")
tex.SetTextFont(42)
tex.DrawLatexNDC(0.67, 0.91, "%.1f fb^{-1} (13 TeV)" % (41.5))
tex.SetTextSize(0.035)
tex.SetTextFont(52)
tex.DrawLatexNDC(0.36,0.91,"Preliminary")

tex2 = TLatex()
tex2.SetTextSize(0.035)
tex3 = TLatex()
tex3.SetTextSize(0.02)
xtext = 1.65 # 2.45
for kk, key in enumerate(dprocs.keys()) :
    tex2.DrawLatex(-xtext+xmin, dprocs[key][1]+0.3, dprocs[key][2])
    tex3.DrawLatex(-xtext+xmin-0.4, dprocs[key][1]-0.35, "#bf{#mu = %.2f ^{+%.2f}_{-%.2f}}" % (dprocs[key][0][0], dprocs[key][0][1], abs(dprocs[key][0][2])))

mu_comb_m1s_syst = sqrt(mu_comb_m1s*mu_comb_m1s-mu_comb_m1s_stat*mu_comb_m1s_stat)
mu_comb_p1s_syst = sqrt(mu_comb_p1s*mu_comb_p1s-mu_comb_p1s_stat*mu_comb_p1s_stat)

ycomb = 15.5 # 11.
tex2.DrawLatex(-2.0+xmin, ycomb, "Combined")
tex2.SetTextSize(0.04)
tex2.DrawLatex(0.5+xmin, ycomb, "#mu = %.2f ^{+%.2f}_{-%.2f}  #bf{#left[ {}^{+%.2f}_{-%.2f}(stat.) {}^{+%.2f}_{-%.2f}(syst.)#right]}" % (combined[0], mu_comb_p1s, mu_comb_m1s, mu_comb_p1s_stat, mu_comb_m1s_stat, mu_comb_p1s_syst, mu_comb_m1s_syst))

"""labels = addLabel_CMS_preliminary()
for ll in labels :
    ll.Draw()"""

savefile = os.path.join(input_folder, "test_mu_ttH_%s.pdf" % ("test"))
c.SaveAs(savefile)
c.SaveAs(savefile)
