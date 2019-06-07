# For kt-kv parameter scan (and eventually CP-angle scan)

Most of the scripts are based on the original [here](https://github.com/stiegerb/cmgtools-lite/tree/80X_M17_tHqJan30_bbcombination/TTHAnalysis/python/plotter/tHq-multilepton/signal_extraction). 

The main difference is that only the necessary scripts to make the interpretation in the context of the ttH.tH multilepton analyses.


The scripts assumes the datacards for both ttH, tHq and tHW are done assuming the respective to be signal.

```
python ../test/kt_kv_scan/makeWorkspaces.py K7 tHq_*card.txt -j 8
```

Where `tHq_*card.txt` are the cards for the parameter scans (the naming conventions can be tunned [here](bla))

```
python ../test/kt_kv_scan/runNLLScan.py -t comb6 ws_tHq_3l_*_K7.card.root -j 8
```

Where `ws_tHq_3l_*_K7.card.root` was created by the previous step.

In this repository there are input for scalings commited to model K7, if you want to make other model please refer to the original set of scripts linked on the beggining of this README.
