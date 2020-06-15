#!/usr/bin/env python
import os
import re
import sys
import json
import numpy as np
import pandas as pd

from functools import partial
from collections import namedtuple
from scipy.interpolate import splev, splrep
from scipy.interpolate import griddata
from scipy.interpolate import interp2d, SmoothBivariateSpline, interp1d
import scipy.interpolate as interp
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import axes3d

import sys, os, re, shlex
import multiprocessing
from subprocess import Popen, PIPE

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

# auxiliary function for mesh generation
def gimme_mesh(n):
    minval = -1
    maxval =  1
    # produce an asymmetric shape in order to catch issues with transpositions
    return np.meshgrid(np.linspace(minval,maxval,n), np.linspace(minval,maxval,n+1))

# set up underlying test functions, vectorized
def fun_smooth(x, y):
    #return np.cos(np.pi*x)*np.sin(np.pi*y)
    return 2.63*x*x - 5.21*x*y + 3.58*y*x

## FIXME: This should dump the limits for each card as it is running,
##        not all together at the end.

def runCombineCommand(combinecmd, card, verbose=False, outfolder=".", queue=None, submitName=None):
    print ("----------------------------------------------")
    print (combinecmd)
    if verbose:
        print 40*'-'
        print "%s %s" % (combinecmd, card)
        print 40*'-'
    try:
        p = Popen(shlex.split(combinecmd) + [card] , stdout=PIPE, stderr=PIPE, cwd=outfolder)
        comboutput = p.communicate()[0]
    except OSError:
        print ("combine command not known\n", combinecmd)
        comboutput = None
    return comboutput

def process(inputfile, inputfile2, xaxis, shiftBy):
    #print ("inputfile", inputfile)
    #print ("inputfile2", inputfile)
    df = pd.read_csv(inputfile, sep=",", index_col=None)
    df_r0 = pd.read_csv(inputfile2, sep=",", index_col=None)

    # Drop failed fit results
    df.dropna(subset=['dnll'], inplace=True)
    df_r0.dropna(subset=['dnll'], inplace=True)

    # Calculate relative NLL
    #df['dnll'] = -2*df.dnll
    df['dnll'] = 2*(df.dnll - df_r0.dnll)

    # Drop duplicates for equal ratios
    df.drop_duplicates(subset='ratio', inplace=True)
    df.sort_values([xaxis], inplace=True) # Xanda FIXME
    df.index = range(1,len(df)+1)

    # Shift dnll up by lowest value
    dnllmin = shiftBy #np.min(df.dnll)
    idxmin = df.dnll.idxmin()
    #assert(df.loc[idxmin].dnll == dnllmin), "inconsistent minimum?"
    print '... shifting dnll values by %5.3f (at %4.2f) for %s' % (np.abs(dnllmin), df.loc[idxmin][xaxis], inputfile)
    df['dnll'] = df.dnll + np.abs(dnllmin)

    return df

allPoints = pd.DataFrame()
init = 50
points = [
52,
54,
55,
56,
58,
60,
62,
64,
65,
66,
68,
70,
72,
74,
75,
76,
78,
80,
82,
84,
85,
86,
92,
94,
95,
96,
98,
100,
104,
105,
106,
108,
110,
112,
114,
115,
116,
118,
120,
122,
124,
126,
128,
130,
132,
134,
135,
138,
140,
142,
144,
145,
146,
147,
148,
150,
152,
154,
156,
158,
166,
168,
170,
172,
174,
176,
178,
180,
182,
184,
186,
188,
190,
190,
192,
194,
196,
198,
200,
201,
202,
203,
204,
206,
210,
212,
214,
216,
218,
220,
240,
260,
280,
]


"""

"""

"""
30,
--
35,
40,
45,
46,
48,
50, --> running
--
52,--done
54,
55,
56,
58,
60,
--
62,
64,
65,
66,
68,
70, --> running from 54
--
72,
74,
75,
76,
78,
80,
--
82,
84,
85,
86,
88,
90, --> running from 72
--
92, -- done
94,
95,
96,
98,
100,
--
102,
104,
105,
106,
108,
110, --> running from 94
--
112,
114,
115,
116,
118,
120,
--
122,
124,
125,
126,
128,
130, --> running from 112
--
132,
134,
135,
136,
138,
140,
--
142,
144,
145,
146,
147,
148,
150,-- runnning from 132
--
155
--
152,
154
156,
158,
160,
162,
164
--------------------------
"""

"""
52,
54,
55,
56,
58,
60,
62,
64,
65,
66,
68,
70,
72,
74,
75,
76,
78,
80,
82,
84,
85,
92,
94,
95,
96,
98,
104,
105,
106,
108,
100,
112,
114,
115,
116,
118,
110,
122,
124,
125,
126,
128,
120,
132,
134,
135,
136,
138,
142,
144,
140,

"""

shiftBy = 32.95 +1.1243172592437487 # 86.536 # hardcode the SM minimum to shift all kVs accordingly
for kVint in points : #range(init, 155, 5) :
    kV = float(kVint)/100
    #print ("doing kV = " + str(kV))
    if 0 > 0 :
        runCombineCommand(
            "python test/kt_kv_scan/runNLLScan.py  -c /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_15May20_kt_scan/results/ -t kV_%s --kV %s -r 0 -j 8  --outputFolder /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_15May20_kt_scan/results/" % (str(kV).replace(".","p"), str(kV)),
            "/home/acaan/CMSSW_10_2_13/src/signal_extraction_tH_ttH"
        )
        runCombineCommand(
            "python test/kt_kv_scan/runNLLScan.py  -c /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_15May20_kt_scan/results/ -t kV_%s --kV %s -r 1 -j 8  --outputFolder /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_15May20_kt_scan/results/" % (str(kV).replace(".","p"), str(kV)),
            "/home/acaan/CMSSW_10_2_13/src/signal_extraction_tH_ttH"
        )
        #runCombineCommand(
        #    "python test/kt_kv_scan/runNLLScan.py  -c /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_15May20_kt_scan/results/ -t _kV_%s --kV %s -r 2 -j 8  --outputFolder /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_16March20_Ov_lep_TLL_tau_kt_scan/results_oneGo/" % (str(kV).replace(".","p"), str(kV)),
        #    "/home/acaan/CMSSW_10_2_13/src/signal_extraction_tH_ttH"
        #)
    elif 1 > 0 :
        filename = "/home/acaan/CMSSW_10_2_13/src/cards_set/legacy_15May20_kt_scan/results/nll_scan_r1_kV_%s.csv" % str(kV).replace(".","p")
        filename2 = "/home/acaan/CMSSW_10_2_13/src/cards_set/legacy_15May20_kt_scan/results/nll_scan_r0_kV_%s.csv" % str(kV).replace(".","p")
        if kVint == init :
            allPoints = process(filename, filename2, "rescalect", shiftBy)
        else :
            allPoints = allPoints.append(process(filename, filename2, "rescalect", shiftBy), ignore_index=True) #
allPoints.dropna(inplace=True)
# drop one suspicious point
#if "kV_1p" in filename and not "kV_1p0" in filename :
#allPoints.drop(pd.Index(allPoints[(allPoints.cv == 1.0) & (abs(allPoints.cf) == 0.75) & (abs(allPoints.rescalecv) > 0.0) & ~(abs(allPoints.rescalecv) > 1.0)].index) , inplace=True ) #
#if "kV_0p" in filename and not ("kV_0p7" in filename or "kV_0p7" in filename) :
#allPoints.drop(pd.Index(allPoints[(allPoints.cv == 1.5) & (abs(allPoints.cf) == 2.0) & (abs(allPoints.rescalecv) < 0.0) & ~((abs(allPoints.rescalecv) == 0.7) | (abs(allPoints.rescalecv) == 0.75))].index) , inplace=True) #
#if  "kV_0p7" in filename or "kV_0p8" in filename:
#allPoints.drop(pd.Index(allPoints[(allPoints.cv == 1.5) & (abs(allPoints.cf) == 1.25) & ((abs(allPoints.rescalecv) == 0.7) | (abs(allPoints.rescalecv) == 0.8))].index) , inplace=True) #
#allPoints = allPoints[~((allPoints.cv == 1.5) & (abs(allPoints.cf) == 1.25))]
#allPoints.drop(pd.Index(allPoints[(allPoints.cv == 0.5) & (abs(allPoints.cf) == 1.25) & ((abs(allPoints.rescalecv) == 0.3))].index) , inplace=True) #

allPoints.drop(allPoints.loc[ (allPoints["rescalect"] > 2.3) | (allPoints["rescalect"] < -2.3)  ].index, inplace=True)
allPoints.drop(allPoints.loc[ (allPoints["rescalecv"] < 0.5) | (allPoints["rescalecv"] > 2.8)  ].index, inplace=True)
print allPoints

if 1 > 0  :
    ####
    # find BF
    kt_BF = 100.
    kv_BF = 100.
    nll_BF = 100.
    for pointY in points :
        #if 1 > 0 : continue
        kv_local = float(pointY)/100
        if not (pointY >=50 and pointY <= 200): continue
        print(kv_local)
        if (len(allPoints.loc[(allPoints["rescalecv"] == kv_local), "rescalect"]) >= 3) :
            #print (kv_local, allPoints.loc[(allPoints["rescalecv"] == kv_local), "rescalect"])
            try :
                fff = interp1d(
                allPoints.loc[(allPoints["rescalecv"] == kv_local), "rescalect"],
                allPoints.loc[(allPoints["rescalecv"] == kv_local), 'dnll'],
                kind='cubic'
                )
            except :
                continue
            ###
            xxx2 = range(int(np.min(allPoints.loc[(allPoints["rescalecv"] == kv_local).values, "rescalect"])*100), int(np.max(allPoints.loc[(allPoints["rescalecv"] == kv_local), "rescalect"].values)*100))
            #print (xxx2) #
            yyy2 = fff([float(x) / 100. for x in xxx2])
            min_index = np.argmin(yyy2)
            if yyy2[min_index] <= kt_BF :
                kt_BF = float(xxx2[min_index])/100.
                kv_BF = kv_local
                nll_BF = yyy2[min_index]
                #print(yyy2)
                print(yyy2[min_index],  fff(float(xxx2[min_index])/100.), float(xxx2[min_index])/100., kv_local)

    print ("found BF")
    print("kt_BF =", kt_BF)
    print("kv_BF =", kv_BF)
    print("nll_BF =", nll_BF)
    ###############
    xx = np.linspace(-1.5,1.5,50)
    xxx = np.linspace(1.5,2.4,10)
    ## those are the attemps to a 2D fit 
    #ff = SmoothBivariateSpline(allPoints["rescalect"], allPoints["rescalecv"], allPoints['dnll'])
    ff = interp2d(allPoints["rescalect"], allPoints["rescalecv"], allPoints['dnll'], kind='linear')
    #yy1 = ff(xx, xxx)
    print("interpolated", ff(1., 1.))
    if 0 > 0 :
        for pointY in points :
            #if 1 > 0 : continue
            kv_local = float(pointY)/100
            if not (pointY >= 50 and pointY <= 200): continue
            print(kv_local)
            if (len(allPoints.loc[(allPoints["rescalecv"] == kv_local), "rescalect"]) > 4) :
                #print (kv_local, allPoints.loc[(allPoints["rescalecv"] == kv_local), "rescalect"])
                try :
                    fff = interp1d(
                    allPoints.loc[(allPoints["rescalecv"] == kv_local), "rescalect"],
                    allPoints.loc[(allPoints["rescalecv"] == kv_local), 'dnll'],
                    kind='cubic'
                    )
                except :
                    continue
                for pointX in range(int(np.min(allPoints.loc[(allPoints["rescalecv"] == kv_local).values, "rescalect"])*100), int(np.max(allPoints.loc[(allPoints["rescalecv"] == kv_local), "rescalect"].values)*100), 10) :
                    kt_local = float(pointX)/100.
                    #print(kt_local)
                    result = -1
                    try :
                        fff(kt_local)
                        result = fff(kt_local)
                    except :
                        try :
                            fff(kt_local) > -100.
                            result = fff(kt_local)[0]
                        except :
                            print("fff(kt_local), not a number",  fff(kt_local))
                            continue
                    #print(fff(kt_local))
                    allPoints = allPoints.append(
                    {
                    #'Animal':'mouse',
                    #'Color':'black'
                    "fname": "interpolatedPoint",
                    "cv" : -1,
                    "cf" : -1,
                    "cosa" : -1,
                    "rescalecv" : kv_local,
                    "rescalect" : kt_local,
                    "ratio" : -1,
                    "bestfitr" : -1,
                    "dnll" : fff(kt_local)
                    },
                    ignore_index=True)
        #allPoints.drop_duplicates(subset=["rescalect", "rescalecv"], inplace=True)
        #"""
    ###############
    outfile = "plots/teste_2D_kappa_points_may2020_unblided"
    #outfile = "plots/teste_2D_kappa_points_may2020_unblided"
    x1 = np.linspace(-2, 2, len(allPoints["rescalect"].unique()))
    y1 = np.linspace(-2, 2, len(allPoints["rescalecv"].unique()))
    x2, y2 = np.meshgrid(x1, y1, sparse=False)
    z2 = griddata((allPoints["rescalect"], allPoints["rescalecv"]), allPoints['dnll'], (x2, y2), method='cubic')

    fig, ax = plt.subplots(figsize=(5, 5))
    levels = [ 2.3, 5.99 ]
    CS = ax.contour(x2, y2, z2, levels, colors='k', linestyles=['solid', 'dashed'] )
    ##
    print("number of points: " , len(allPoints['dnll']), len(x2))
    #ax.plot(allPoints["rescalect"].values, allPoints["rescalecv"].values, 'ko', ms=3)

    x_low, x_high = -1.5, 1.5
    y_low, y_high = 0.22, 2.5
    ax.set_xlim(x_low, x_high)
    ax.set_ylim(y_low, y_high)

    ax.set_xlabel("$\\kappa_\\mathrm{t}$" , fontsize=16, labelpad=10)
    ax.set_ylabel("$\\kappa_{\\mathrm{V}}$", fontsize=16, labelpad=10)
    print_header(ax, x_low, x_high, y_low, y_high)

    line_up, = plt.plot(x1, ls='-', color='k',label="68% C.l.")
    line_down, = ax.plot(x1, ls='--', color='k',label="95% C.l.")
    legend = plt.legend(handles=[line_up, line_down], loc='lower left', title="Observed", frameon=True, framealpha=1.0, fontsize=12)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_linewidth(0)
    line_SM = ax.scatter([1], [1], marker="*", label="SM expected", s=50, c='k')
    line_BF = ax.scatter([kt_BF], [kv_BF], marker="*", label="Best fit", s=50, c='r')

    legend2 = plt.legend(handles=[ line_SM, line_BF ], loc='lower right', title="", frameon=True, framealpha=1.0, fontsize=12, scatterpoints=1)
    legend2.get_frame().set_facecolor('white')
    legend2.get_frame().set_linewidth(0)
    ax.add_artist(legend)
    ax.add_artist(legend2)


    plt.savefig("%s.pdf"%outfile, bbox_inches='tight')
    #plt.savefig("%s.png"%outfilen bbox_inches='tight', dpi=300) #
    print ("saved ", "%s.pdf"%outfile)
    ###############
    outfile = "plots/teste_2D_kappa_points_may2020_unblided_pointss"
    fig, ax = plt.subplots(figsize=(5, 5))
    levels = [ 2.3, 5.99 ]
    ax.set_xlim(x_low, x_high)
    ax.set_ylim(y_low, y_high)
    CS = ax.contour(x2, y2, z2, levels, colors='k', linestyles=['solid', 'dashed'] )
    ax.plot(allPoints["rescalect"].values, allPoints["rescalecv"].values, 'ko', ms=3)
    plt.savefig("%s.pdf"%outfile, bbox_inches='tight')
    print ("saved ", "%s.pdf"%outfile)

    fig, ax = plt.subplots(figsize=(5, 5))
    xxx = np.linspace(-2.5,2.5,100)
    #yy1 = ff(xx, 2.0)
    #yy2 = ff(xxx, 2.6)
    #yy3 = ff(xxx, 0.52)
    #yy4 = ff(xxx, 1.04)
    #plt.plot(xx,yy1, 'g')
    #plt.plot(xxx,yy2, 'r')
    #plt.plot(xxx,yy3, 'g')
    #plt.plot(xxx,yy4, 'k')
    ax.set_ylim(0, 80)
    ax.set_xlim(-1.5, 1.5)
    print(allPoints.loc[(allPoints["rescalecv"] == 1.0), "rescalect"].values, allPoints.loc[(allPoints["rescalecv"] == 2.0), "dnll"].values)
    #print(allPoints.loc[(allPoints["rescalecv"] == 2.02), "rescalect"].values)
    print(allPoints.loc[(allPoints["rescalecv"] == 1.82), "rescalect"].values)
    fff2 = interp1d(
        allPoints.loc[(allPoints["rescalecv"] == 1.0), "rescalect"].values,
        allPoints.loc[(allPoints["rescalecv"] == 1.0), 'dnll'].values,
        kind='cubic'
        )
    fff4 = interp1d(
        allPoints.loc[(allPoints["rescalecv"] == 1.82), "rescalect"],
        allPoints.loc[(allPoints["rescalecv"] == 1.82), 'dnll'],
        kind='cubic'
        )
    fff5 = interp1d(
        allPoints.loc[(allPoints["rescalecv"] == 1.5), "rescalect"],
        allPoints.loc[(allPoints["rescalecv"] == 1.5), 'dnll'],
        kind='cubic'
        )
    fff6 = interp1d(
        allPoints.loc[(allPoints["rescalecv"] == 1.52), "rescalect"],
        allPoints.loc[(allPoints["rescalecv"] == 1.52), 'dnll'],
        kind='cubic'
        )
    fff7 = interp1d(
        allPoints.loc[(allPoints["rescalecv"] == 1.54), "rescalect"],
        allPoints.loc[(allPoints["rescalecv"] == 1.54), 'dnll'],
        kind='cubic'
        )
    print ("hfhagsfa", int(np.min(allPoints.loc[(allPoints["rescalecv"] == 1.52).values, "rescalect"])*100), int(np.max(allPoints.loc[(allPoints["rescalecv"] == 1.52), "rescalect"].values)*100))
    xxx2 = range(int(np.min(allPoints.loc[(allPoints["rescalecv"] == 1.0).values, "rescalect"])*100), int(np.max(allPoints.loc[(allPoints["rescalecv"] == 1.0), "rescalect"].values)*100))
    xxx4 = range(int(np.min(allPoints.loc[(allPoints["rescalecv"] == 1.82).values, "rescalect"])*100), int(np.max(allPoints.loc[(allPoints["rescalecv"] == 1.82), "rescalect"].values)*100))
    xxx5 = range(int(np.min(allPoints.loc[(allPoints["rescalecv"] == 1.5).values, "rescalect"])*100), int(np.max(allPoints.loc[(allPoints["rescalecv"] == 1.5), "rescalect"].values)*100))
    xxx6 = range(int(np.min(allPoints.loc[(allPoints["rescalecv"] == 1.52).values, "rescalect"])*100), int(np.max(allPoints.loc[(allPoints["rescalecv"] == 1.52), "rescalect"].values)*100))
    xxx7 = range(int(np.min(allPoints.loc[(allPoints["rescalecv"] == 1.54).values, "rescalect"])*100), int(np.max(allPoints.loc[(allPoints["rescalecv"] == 1.54), "rescalect"].values)*100))
    #print (xxx2) #
    yyy2 = fff2([float(x) / 100. for x in xxx2])
    yyy4 = fff4([float(x) / 100. for x in xxx4])
    yyy5 = fff5([float(x) / 100. for x in xxx5])
    yyy6 = fff6([float(x) / 100. for x in xxx6])
    yyy7 = fff7([float(x) / 100. for x in xxx7])
    plt.plot([float(x) / 100. for x in xxx2], yyy2, 'r-', label="kv = 1.0 interpolated")
    plt.plot([float(x) / 100. for x in xxx4], yyy4, 'k-', label="kv = 1.82 interpolated")
    plt.plot([float(x) / 100. for x in xxx5], yyy5, 'g-', label="kv = 1.5 interpolated")
    plt.plot([float(x) / 100. for x in xxx6], yyy6, 'y-', label="kv = 1.52 interpolated")
    plt.plot([float(x) / 100. for x in xxx7], yyy7, 'b-', label="kv = 1.54 interpolated")
    #plt.plot(allPoints.loc[(allPoints["rescalecv"] == 1.04), "rescalect"].values, allPoints.loc[(allPoints["rescalecv"] == 1.04), "dnll"].values, 'ko', ms=3)
    #plt.plot(allPoints.loc[(allPoints["rescalecv"] == 0.52), "rescalect"].values, allPoints.loc[(allPoints["rescalecv"] == 0.52), "dnll"].values, 'go', ms=3)
    #plt.plot(allPoints.loc[(allPoints["rescalecv"] == 2.6), "rescalect"].values, allPoints.loc[(allPoints["rescalecv"] == 2.6), "dnll"].values, 'ro', ms=3)
    plt.plot(
        allPoints.loc[(allPoints["rescalecv"] == 1.82), "rescalect"].values,
        allPoints.loc[(allPoints["rescalecv"] == 1.82), "dnll"].values, 'ko', ms=3,
        label="kv = 1.82"
        )
    #plt.plot(allPoints.loc[(allPoints["rescalecv"] == 0.52), "rescalect"].values, allPoints.loc[(allPoints["rescalecv"] == 0.52), "dnll"].values, 'go', ms=3)
    plt.plot(
        allPoints.loc[(allPoints["rescalecv"] == 1.0), "rescalect"].values,
        allPoints.loc[(allPoints["rescalecv"] == 1.0), "dnll"].values, 'ro', ms=3,
        label="kv = 1.0"
    )
    plt.plot(
        allPoints.loc[(allPoints["rescalecv"] == 1.5), "rescalect"].values,
        allPoints.loc[(allPoints["rescalecv"] == 1.5), "dnll"].values, 'go', ms=3,
        label="kv = 1.5"
    )
    plt.plot(
        allPoints.loc[(allPoints["rescalecv"] == 1.52), "rescalect"].values,
        allPoints.loc[(allPoints["rescalecv"] == 1.52), "dnll"].values, 'yo', ms=3,
        label="kv = 1.52"
    )
    plt.plot(
        allPoints.loc[(allPoints["rescalecv"] == 1.54), "rescalect"].values,
        allPoints.loc[(allPoints["rescalecv"] == 1.54), "dnll"].values, 'bo', ms=3,
        label="kv = 1.54"
    )
    plt.legend(loc='best', fancybox=False, shadow=False, ncol=1, fontsize=8)
    plt.savefig("%s_func.pdf"%outfile, bbox_inches='tight')
    print ("saved", "%s_func.pdf"%outfile)

    ## those are the attemps to a 2D fit
    """fig, ax = plt.subplots(figsize=(5, 5))
    xx = np.linspace(0.5,2.5,300)
    yy1 = ff(0.0, xx)
    yy2 = ff(1.0, xx)
    yy3 = ff(2.0, xx)
    #print(yy1[0])
    #print(len(yy1[0]), len(xxx), ff(0.6, 0.6))
    #plt.plot(xx, yy1[0], 'k')
    #plt.plot(xx, yy2[0], 'g')
    #plt.plot(xx, yy3[0], 'g')
    plt.plot(xx, yy1, 'k')
    plt.plot(xx, yy2, 'g')
    ax.set_ylim(0, 500)
    ax.set_xlim(0.5, 2.5)
    plt.plot(allPoints.loc[(allPoints["rescalect"] == 0.0), "rescalecv"].values, allPoints.loc[(allPoints["rescalect"] == 0.0), "dnll"].values, 'ko', ms=3)
    plt.plot(allPoints.loc[(allPoints["rescalect"] == 1.0), "rescalecv"].values, allPoints.loc[(allPoints["rescalect"] == 1.0), "dnll"].values, 'go', ms=3)
    plt.savefig("%s_funcY.pdf"%outfile, bbox_inches='tight')"""

    """fig, ax = plt.subplots(figsize=(5, 5))
    yy1 = ff(xx, xxx)
    #yy2 = ff(xx, xxx)
    #yy3 = ff(xx, xxx)
    #print(yy1)
    #print(len(yy1[0]), len(xxx), ff(0.6, 0.6))
    #plt.plot(xx,yy1[0], 'g')
    #plt.plot(xx,yy2[0], 'g')
    #plt.plot(xx,yy3[0], 'g')
    cp = plt.contour( xxx,  xx, yy1, levels, colors='k', linestyles=['solid', 'dashed'] )
    plt.savefig("%s_funcInterpolated.pdf"%outfile, bbox_inches='tight')"""
