# For standalone run of one combined datacard

* 1) To run the combined limits

```
python test/run_limits_floating_components.py --cardToRead  datacard --cardFolder /relative/or/full/path --ttW --ttZ --tH
```

Where `datacard.txt` contains all the channels one wants to calculate limits to and `/relative/or/full/path` is the folder that contains `datacard.txt` and its relative root file.

The `--ttW` / `--ttW` command line adds it floating (that is false if not used).

The fits options are enetered in [cards/options.dat](https://github.com/acarvalh/signal_extraction_tH_ttH/blob/master/cards/options.dat) -- one needs to read carefully to know what its being booked as fit.

Different datacard_channelX.txt can be combined with the following command (type-2):

```
combineCards.py  datacard_channel1.txt datacard_channel2.txt > datacard.txt
```

* 2) The systematics entries of the combine .txt datacard can be manipulated (eg) with CombineHavester, examples of how to do it are found on `manipulate_datacards.py`. This one is not directly usable right now, as we do not know yet how we want to manipulate cards or not.

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

If you do not add the `--original` entry the on the command line the resultant plot the bins will be numbered by bin number and equidistant. 

* 6) The limits/mu plots done as frozen to PAS-HIG-18-019 are ran as:

```
python test/makeMuPlot.py --input_folder input_folder
python test/make_limit_plot.py --input_folder input_folder
```

Where `input_folder` is the folder that contains the output of (i)


