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

## For standalone run of one combined datacard

See the README inside `test/`

## For kt-kv parameter scan (and eventually CP-angle scan)

See the README inside `test/kt_kv_scan/`