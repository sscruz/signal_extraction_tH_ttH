# For kt-kv parameter scan (and eventually CP-angle scan)

Most of the scripts are based on the original [here](https://github.com/stiegerb/cmgtools-lite/tree/80X_M17_tHqJan30_bbcombination/TTHAnalysis/python/plotter/tHq-multilepton/signal_extraction).

The main difference is that only the necessary scripts to make the interpretation in the context of the ttH/tH multilepton analyses. Morover, we will be adding fit options specifically for ttH/tH multilepton.


The scripts assumes the datacards for both ttH, tHq and tHW are done assuming the respective to be signal has SM cross section (independently of the kinematics that the card correspond to).

In the datacards both ttH, tHq must be marked as signal on the datacard.txt (as a negative entry).

To make workspaces from all datacards you do:

```
python test/kt_kv_scan/makeWorkspaces.py  /where/cards/are/tHq_*card.txt -m K7 -j 8 --outputFolder /where/to/save
```

Where `tHq_*card.txt` are the cards for the parameter scans (the naming conventions can be tunned [here](https://github.com/acarvalh/signal_extraction_tH_ttH/blob/master/test/kt_kv_scan/runAllLimits.py#L27-L39)) and the input and output paths need to be the absolute ones.

*WARNING*: The workspace is now done without considering float BKGs -- to correct that.

The next step is to run the multidimensional fit.

```
python test/kt_kv_scan/runNLLScan.py -t comb6 -c --cards /where/ws/are/saved/ -j 8  --outputFolder /where/to/save
```

Where `/where/ws/are/saved/` is the directory with the workspaces (named as e.g. `ws*_kt_m1p25_kv_1p5*.root`) that were created by the previous step. The `outputFolder` is where to save the .csv file with the numeric result of the scan, recomended to be the same of the last step.

NOTE:
 - by default kV is taken to be one, if you want to use reescalings to other values enter it on the commend line, eg  `--kV 1.2`
 - by default is takes the cards
 - The 'blind' option is not working --- To figure out why one cannot make NLL scan with asimov data

```
python test/kt_kv_scan/plotNLLScans.py cards/nllscan_test.json
```

Where `cards/nllscan_test.json` is a file that contains the location of the .csv file with the results of the nll scan done on the previous step (see exemple [here](https://github.com/acarvalh/signal_extraction_tH_ttH/blob/17388c588950c732fd356d98c7e716583c8808fa/cards/nllscan_couplingsVar.json)).
If you plot a cos(alpha) scan (that is defined on the json file just mentioned) you need to add to the above plotting command the option `--nosplines`
