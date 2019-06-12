# For kt-kv parameter scan (and eventually CP-angle scan)

Most of the scripts are based on the original [here](https://github.com/stiegerb/cmgtools-lite/tree/80X_M17_tHqJan30_bbcombination/TTHAnalysis/python/plotter/tHq-multilepton/signal_extraction). 

The main difference is that only the necessary scripts to make the interpretation in the context of the ttH/tH multilepton analyses. Morover, we will be adding fit options specifically for ttH/tH multilepton.


The scripts assumes the datacards for both ttH, tHq and tHW are done assuming the respective to be signal has SM cross section (independently of the kinematics that the card correspond to). 

In the datacards both ttH, tHq must be marked as signal on the datacard.txt (as a negative entry).

To make workspaces from all datacards you do:

```
python test/kt_kv_scan/makeWorkspaces.py K7 /where/cards/are/tHq_*card.txt -j 8 --outputFolder /where/to/save
```

Where `tHq_*card.txt` are the cards for the parameter scans (the naming conventions can be tunned [here](https://github.com/acarvalh/signal_extraction_tH_ttH/blob/master/test/kt_kv_scan/runAllLimits.py#L27-L39))

*WARNING*: The workspace is now done without considering float BKGs -- to correct that.

The next step is to run the multidimensional fit.

```
python test/kt_kv_scan/runNLLScan.py -t comb6 /where/ws/are/saved/ws_tHq_3l_*_K7.card.root -j 8 --blind --outputFolder /where/to/save
```

Where `ws_tHq_3l_*_K7.card.root` was created by the previous step and `outputFolder` is recomended to be the same of the last step.

```
python test/kt_kv_scan/plotNLLScans.py cards/nllscan_test.json
```

Where `cards/nllscan_test.json` is a file that contains the location of the .csv file with the results of the nll scan done on the previous step (see exemple [here]()).
By now only the 



