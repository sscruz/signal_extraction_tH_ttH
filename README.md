# signal_extraction_tH_ttH

Repository to keep all the scripts that make signal extraction and interpretation on ttH/tH multilepton analysis based on .txt combine-like datacards. 

The different scripts need different setups to be loaded.
In the beggining of each script there is a note for which setup (type-1, type-2 or type-3) should be loaded.

* type-1) CMSSW_10X, to contain all the python packages -- nothing else needs to be installed on top.

* type-2) CMSSW with [Combine](https://github.com/cms-analysis/higgsanalysis-combinedlimit/wiki/gettingstarted#for-end-users-that-dont-need-to-commit-or-do-any-development
) (at least v7.0.12)

```
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src 
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v7.0.12
scramv1 b clean; scramv1 b # always make a clean build
```

* type-3) CMSSW with Combine and CombineHavester

On top of the setup for type-2 scripts install CombineHavester: 

```
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scram b
```

In case of KBFI use [this one](https://github.com/HEP-KBFI/CombineHarvester) instead.

## For standalone run of datacards

* The systematics entries of the combine .txt datacard can be manipulated with CombineHavester, "test/"

* 

* The "test/makeMuPlot.py" and "test/make_limit_plot.py" are

* The prefit/postfit plots can be made with the example bellow



* To make the prefit plots through combine may take time depending

test/draw_prefit_plain_bin_list.py

## For kt-kv parameter scan (and eventually CP-angle scan)

Most of the scripts are based on the original [here](https://github.com/stiegerb/cmgtools-lite/tree/80X_M17_tHqJan30_bbcombination/TTHAnalysis/python/plotter/tHq-multilepton/signal_extraction). 

The main difference is that only the necessary scripts to make the interpretatio
It assumes the datacards for both ttH, tHq and tHW are done assuming the respective 

python ../test/kt_kv_scan/makeWorkspaces.py K7 tHq_*card.txt -j 8
python ../test/kt_kv_scan/runNLLScan.py -t comb6 ws_tHq_3l_*_K7.card.root -j 8