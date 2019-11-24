# For standalone run of one combined datacard

* 1) To run the combined limits

```
python test/run_limits_floating_components.py --cardToRead  datacard --cardFolder /relative/or/full/path --ttW --ttZ --tH
```

Where `datacard.txt` contains all the channels one wants to calculate limits to and `/relative/or/full/path` is the folder that contains `datacard.txt` and its relative root file.

The `--ttW` / `--ttW` command line adds it floating (that is false if not used).

The fits options are entered in [cards/options.dat](https://github.com/acarvalh/signal_extraction_tH_ttH/blob/master/cards/options.dat) -- one needs to read carefully to know what its being booked as fit.

Different datacard_channelX.txt can be combined with the following command (type-2):

```
combineCards.py  datacard_channel1.txt datacard_channel2.txt > datacard.txt
```

* 2) The systematics entries of the combine .txt datacard can be manipulated (eg) with CombineHavester, examples of how to do it are found on `manipulate_datacards.py`. This one is not directly usable right now, as we do not know yet how we want to manipulate cards or not.

* 3) Standalone prefit/postfit plots can be made with the example bellow:

For prefit:

```
python test/makePlots.py --channel "4l_CR" --nameOut a_name \
--input /path/WS_3poi_shapes_2017_combo.root \
--odir /path/  --era 2017
```

Where WS_3poi_shapes_2017_combo.root is the output of running (1) with option `preparePostFitCombine = True` OR `preparePostFitHavester = True` (if you use the second you need to add to command line `--fromHavester` into the above).
And `--channel` is the one that appears in the plot configs [here](https://github.com/acarvalh/signal_extraction_tH_ttH/blob/master/configs/plot_options.py#L351-L355) for the list of processes to draw and [here](https://github.com/acarvalh/signal_extraction_tH_ttH/blob/master/configs/plot_options.py#L170-L178) for the plot fine tunnings.

You can plot the three eras merged using the `makePlots.py` script with the `--input` being the 2018 one, and `--era 0`. It will fetch the other input shapes, provided that the only difference in their naming convention is to replace "2018" to "2017" or "2016" in the full `/path/WS_3poi_shapes_2017_combo.root`

By default the resulting plots are made blinded, if you want to unblind add to the command line " --unblind".

For postfit add the command line `--doPostFit`

For case where the shapes file was made by `preparePostFitCombine`: If you do not add the `--original` entry the on the command line the resultant plot the bins will be numbered by bin number and equidistant.

* 6) The limits/mu plots done as frozen to PAS-HIG-18-019 are ran as:

```
python test/makeMuPlot.py --input_folder input_folder
python test/make_limit_plot.py --input_folder input_folder
```

Where `input_folder` is the folder that contains the output of (i)
