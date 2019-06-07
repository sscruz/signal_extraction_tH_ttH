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

## Description of the scripts

### For standalone run of datacards


* 1) To run the combined limits

Where datacard.txt contains all the channels one wants to calculate limits to.

Different datacard_channelX.txt can be combined with the following command (type-2):

```
combineCards.py  datacard_channel1.txt datacard_channel2.txt > datacard.txt
```

* 2) The systematics entries of the combine .txt datacard can be manipulated (eg) with CombineHavester, examples of how to do it "test/"


* 3) Standalone prefit/postfit plots can be made with the example bellow:

For prefit:

```
python makePostFitPlots_FromCombine.py --channel  ttH_4l  --input WS_3poi_shapes_combo.root  --minY -0.35 --maxY 13.9  --notFlips --notConversions
```

Where WS_3poi_shapes_combo.root is the output of running (1) with option `preparePostFitCombine = True` OR `preparePostFitHavester = True` (if you use the second you need to add to comand line `--fromHavester` into the above)

By default all the processes are added on the plot (including flips/conversions), some command lines can be used/added as:   "--notFlips" or "--notConversions".

By default the resulting plots are made blinded, if you want to unbling add to the command line " --unblind".

For postfit:

```
python makePostFitPlots_FromCombine.py --channel  ttH_4l  --input WS_3poi_shapes_combo.root --minY -0.35 --maxY 13.9  --notFlips --notConversions --unblind  --original datacard_combo.root --doPostFit
```

* 6) The limits/mu plots done as frozen to PAS-HIG-18-019 are ran as:

```
python test/makeMuPlot.py --input_folder input_folder
python test/make_limit_plot.py --input_folder input_folder
```

Where `input_folder` is the folder that contains the output of (1)


### For kt-kv parameter scan (and eventually CP-angle scan)

See the README inside `kt_kv_scan`