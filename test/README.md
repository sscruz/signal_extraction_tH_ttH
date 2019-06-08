# For standalone run of one combined datacard

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


