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

import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

import sys, os, re, shlex
import multiprocessing
from subprocess import Popen, PIPE
 
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

def process(inputfile, xaxis):
    df = pd.read_csv(inputfile, sep=",", index_col=None) 

    # Drop failed fit results
    df.dropna(subset=['dnll'], inplace=True)

    # Calculate relative NLL
    df['dnll'] = -2*df.dnll

    # Drop duplicates for equal ratios
    df.drop_duplicates(subset='ratio', inplace=True)
    df.sort_values([xaxis], inplace=True) # Xanda FIXME
    df.index = range(1,len(df)+1)

    # Shift dnll up by lowest value
    dnllmin = np.min(df.dnll)
    idxmin = df.dnll.idxmin()
    assert(df.loc[idxmin].dnll == dnllmin), "inconsistent minimum?"
    print '... shifting dnll values by %5.3f (at %4.2f) for %s' % (np.abs(dnllmin), df.loc[idxmin][xaxis], inputfile)
    df['dnll'] = df.dnll + np.abs(dnllmin)

    return df

allPoints = pd.DataFrame()
init = -29
for kVint in range(init, 29) :
    kV = float(kVint)/10
    if kV == 0.2 : continue
    #runCombineCommand(
    #    "python test/kt_kv_scan/runNLLScan.py  -c /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt//tHq_pdas_3l_ws/ -j 8 --outputFolder /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/signal_extraction_tH_ttH/tHq_pdas_3l_ws_2/ -t kV_%s --kV %s" % (str(kV).replace(".","p"), str(kV)),
    #    "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/signal_extraction_tH_ttH"
    #)
    filename = "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/signal_extraction_tH_ttH/tHq_pdas_3l_ws_2//nll_scankV_%s.csv" % str(kV).replace(".","p")
    if kVint == init : 
        allPoints = process(filename, "rescalect") 
    else :
        allPoints = allPoints.append(process(filename, "rescalect"), ignore_index=True) #
#print allPoints

outfile = "plots/teste_2D_kappa_nopoints"
x1 = np.linspace(-5, 5, len(allPoints["rescalect"].unique()))
y1 = np.linspace(-3, 3, len(allPoints["rescalecv"].unique()))
x2, y2 = np.meshgrid(x1, y1)
z2 = griddata((allPoints["rescalect"], allPoints["rescalecv"]), allPoints['dnll'], (x2, y2), method='cubic')

fig, ax = plt.subplots(figsize=(6, 6))
levels = [-1.0, 2.0 ] #np.arange(4.0, 9.0 ) 
CS = ax.contour(x2, y2, z2-2.0, levels, colors='k',)
ax.clabel(CS, inline=False, fontsize=10, )
#ax.plot(allPoints["rescalect"].values, allPoints["rescalecv"].values, 'ko', ms=3)

ax.set_xlim(-5, 5)
ax.set_ylim(-3, 3)

ax.set_xlabel("kt" , fontsize=24, labelpad=20)
ax.set_ylabel("kv", fontsize=24, labelpad=20)

plt.savefig("%s.pdf"%outfile, bbox_inches='tight')
plt.savefig("%s.png"%outfile, bbox_inches='tight', dpi=300)
