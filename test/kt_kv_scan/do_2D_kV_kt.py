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
from scipy.interpolate import interp2d
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
    print ("inputfile", inputfile)
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
shiftBy = 86.536 # hardcode the SM minimum to shift all kVs accordingly
for kVint in range(init, 155, 5) :
    kV = float(kVint)/100
    print ("doing kV = " + str(kV))
    if 0 > 1 :
        runCombineCommand(
            "python test/kt_kv_scan/runNLLScan.py  -c /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/legacy_10Feb_lepOv_tauTLL/MVA/results_102x/ -t kV_%s --kV %s -r 0 -j 8  --outputFolder /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/legacy_10Feb_lepOv_tauTLL/MVA/results_102x/" % (str(kV).replace(".","p"), str(kV)),
            "/afs/cern.ch/work/a/acarvalh/CMSSW_10_2_13/src/signal_extraction_tH_ttH"
        )
        runCombineCommand(
            "python test/kt_kv_scan/runNLLScan.py  -c /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/legacy_10Feb_lepOv_tauTLL/MVA/results_102x/ -t _kV_%s --kV %s -r 1 -j 8  --outputFolder /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/legacy_10Feb_lepOv_tauTLL/MVA/results_102x/" % (str(kV).replace(".","p"), str(kV)),
            "/afs/cern.ch/work/a/acarvalh/CMSSW_10_2_13/src/signal_extraction_tH_ttH"
        )
    elif 1 > 0 :
        filename = "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/legacy_10Feb_lepOv_tauTLL/MVA/results_102x/nll_scan_r1__kV_%s.csv" % str(kV).replace(".","p")
        filename2 = "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/legacy_10Feb_lepOv_tauTLL/MVA/results_102x/nll_scan_r0_kV_%s.csv" % str(kV).replace(".","p")
        if kVint == init :
            allPoints = process(filename, filename2, "rescalect", shiftBy)
        else :
            allPoints = allPoints.append(process(filename, filename2, "rescalect", shiftBy), ignore_index=True) #
allPoints.dropna(inplace=True)
#allPoints.drop(allPoints.loc[ (allPoints['cf']==-1) &  (allPoints['cv']==1) ].index, inplace=True)
print allPoints

if 1 > 0  :
    outfile = "plots/teste_2D_kappa_Nopoints"
    x1 = np.linspace(-2, 2, len(allPoints["rescalect"].unique()))
    y1 = np.linspace(-2, 2, len(allPoints["rescalecv"].unique()))
    x2, y2 = np.meshgrid(x1, y1, sparse=False)
    #interpolator = CloughTocher2DInterpolator((YREF.ravel(), XREF.ravel()),
    #                                          vals.ravel())
    z2 = griddata((allPoints["rescalect"], allPoints["rescalecv"]), allPoints['dnll'], (x2, y2), method='cubic')
    #z_sparse_smooth = fun_smooth(x2, y2)
    #N_dense = 20
    #x_dense,y_dense = gimme_mesh(N_dense)
    #z_dense_smooth_griddata = interp.griddata(np.array([x2.ravel(),y2.ravel()]).T,
    #                                      z_sparse_smooth.ravel(),
    #                                      (x_dense,y_dense), method='cubic')

    fig, ax = plt.subplots(figsize=(5, 5))
    levels = [2.3, 5.99 ] #[-1.0, 2.0 ] #np.arange(2.3, 5.99 )
    CS = ax.contour(x2, y2, z2, levels, colors='k', linestyles=['solid', 'dashed'] )
    #CS = ax.contour(x_dense, y_dense, z_dense_smooth_griddata, levels, colors='k',)
    #ax.clabel(CS, inline=False, fontsize=10, )
    #ax.plot(allPoints["rescalect"].values, allPoints["rescalecv"].values, 'ko', ms=3)

    x_low, x_high = -1.5, 1.5
    y_low, y_high = 0.5, 1.5
    ax.set_xlim(x_low, x_high)
    ax.set_ylim(y_low, y_high)

    ax.set_xlabel("$\\kappa_\\mathrm{t}$" , fontsize=16, labelpad=10)
    ax.set_ylabel("$\\kappa_{\\mathrm{V}}$", fontsize=16, labelpad=10)
    print_header(ax, x_low, x_high, y_low, y_high)

    line_up, = plt.plot(x1, ls='-', color='k',label="68% C.l.")
    line_down, = ax.plot(x1, ls='--', color='k',label="95% C.l.")
    legend = plt.legend(handles=[line_up, line_down], loc='lower left', title="Expected", frameon=True, framealpha=1.0, fontsize=12)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_linewidth(0)


    plt.savefig("%s.pdf"%outfile, bbox_inches='tight')
    #plt.savefig("%s.png"%outfilen bbox_inches='tight', dpi=300) #
    print ("saved ", "%s.pdf"%outfile)
