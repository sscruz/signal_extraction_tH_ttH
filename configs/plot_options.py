
def options_plot (analysis, channel, all_procs) : 
    dprocs = OrderedDict()
    Hdecays_long = ["hww", "hzz", "htt", ] # "hzg", "hmm"
    Hdecays      = ["hww", "htt" ] # , "hzz", "htt" 
    ## the order of the entries will be the order of the drawing, that is why this is almost manual
    # TODO: write it on a smarther way
    if analysis == "ttH" :
        #conversions = "conversions"
        #fakes       = "fakes_data"
        #flips       = "flips_data"
        # if label == "none" it means that this process is to be merged with the anterior key
        if fakes in all_procs       : dprocs[fakes]       = {"color" :  12, "fillStype" : 3345, "label" : "Non-prompt"  , "make border" : True}
        if flips in all_procs       : dprocs[flips]       = {"color" :   1, "fillStype" : 3006, "label" : "Charge mis-m", "make border" : True}
        if conversions in all_procs : dprocs[conversions] = {"color" :   5, "fillStype" : 1001, "label" : "Conv."       , "make border" :  True}
        if "Rares" in all_procs     : dprocs["Rares"]     = {"color" : 851, "fillStype" : 1001, "label" : "Rares"       , "make border" : True}
        if "EWK" in all_procs       : dprocs["EWK"]       = {"color" : 610, "fillStype" : 1001, "label" : "EWK"         , "make border" : True}
        if "ZZ" in all_procs        : dprocs["ZZ"]        = {"color" : 52,  "fillStype" : 1001, "label" : "ZZ"          , "make border" : True}
        if "WZ" in all_procs        : dprocs["WZ"]        = {"color" : 159, "fillStype" : 1001, "label" : "WZ"          , "make border" : True}
        #if "DY" in all_procs        : dprocs["DY"]        = {"color" : 221, "fillStype" : 1001, "label" : "WZ"          , "make border" : True}
        if "TTWW" in all_procs :
            dprocs["TTW"]                                 = {"color" : 823, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            dprocs["TTWW"]                                = {"color" : 823, "fillStype" : 1001, "label" : "ttW + ttWW"  , "make border" : True}
        elif "TTW" in all_procs :
            dprocs["TTW"]                                 = {"color" : 823, "fillStype" : 1001, "label" : "ttWW"        , "make border" : True}
        if "TTZ" in all_procs       : dprocs["TTZ"]       = {"color" : 822, "fillStype" : 1001, "label" : "ttZ"         , "make border" : True}
        ### signals
        if "VH" in all_procs :
            for decay in list(set(list(Hdecays)) - set(["htt"])) : 
                dprocs["VH"]               = {"color" :   4, "fillStype" : 1001, "label" : "VH"         , "make border" : True} # ["VH_%s" % decay]
            #dprocs["VH_htt"]                              = {"color" : 67, "fillStype" : 1001, "label" : "VH"           , "make border" : True}
        if "ttH" in all_procs :
            for decay in list(set(list(Hdecays_long)) - set(["htt"])) : 
                dprocs["ttH_%s" % decay]                 = {"color" :   2, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            dprocs["ttH_htt"]                                 = {"color" :   2, "fillStype" : 1001, "label" : "ttH"         , "make border" : True}
        if "tHq" in all_procs :
            for decay in list(set(list(Hdecays)) - set(["htt"])) : 
                dprocs["tHq_%s" % decay]              = {"color" : 205, "fillStype" : 1001, "label" : "none"        , "make border" : False} # "tHq_%s" % decay
            dprocs["tHq_htt"]                             = {"color" : 205, "fillStype" : 1001, "label" : "tHq * 3"           , "make border" : True}
        if "tHW" in all_procs :
            for decay in list(set(list(Hdecays)) - set(["htt"]))  : 
                dprocs["tHW_%s" % decay]              = {"color" : 207, "fillStype" : 1001, "label" : "none"         , "make border" : False} # "tHW_%s" % decay
            dprocs["tHW_htt"]                         = {"color" : 207, "fillStype" : 1001, "label" : "tHW * 3"      , "make border" : True}

        # change the order of the stack if channel is dominated by fakes
        if channel in ["2los_1tau", "1l_2tau", "0l_2tau", "1l_1tau"] :
            ## remove "fakes_data" from first entry and add as last
            del dprocs[fakes]
            dprocs[fakes]                                 = {"color" :   1, "fillStype" : 3005, "label" : "Mis."        , "make border" : True}
        if channel in ["0l_2tau", "1l_1tau"] :
            #del dprocs["DY"]
            dprocs["DY"]                                  = {"color" : 221, "fillStype" : 1001, "label" : "DY"         , "make border" : True}
            del dprocs[fakes]
            dprocs[fakes]                                 = {"color" :   1, "fillStype" : 3005, "label" : "Mis."        , "make border" : True}
            dprocs["TT"]                                  = {"color" : 114, "fillStype" : 1001, "label" : r'$t\bar{t}$ + jets'   , "make border" : True}
    else : sys.exit("analysis " + analysis + " not implemented")
    return dprocs

def Higgs_proc_decay (proc) :
    Hdecays_long = ["hww", "hzz", "htt", "hzg", "hmm" ]
    Hdecays      = ["hww", "hzz", "htt" ]
    #sum(higgs_procs,[])
    return sum([ [y + "_" + x  for x in decays if not (x in ["hzz", "htt", "hzg", "hmm"] and y != "ttH")] for y in sigs], [])

def options_plot_ranges (analysis) : 
    if analysis == "ttH" :
        ### it will have the subcategories for the DNNs
        info_channel = {
            "2lss_0tau_BKG" : { "minY" : 0.,   "maxY" :  35.,  "minYerr": 0.501, "maxYerr" : 1.59, "useLogPlot" : False, "label" : '2l ss + 0#tau_{h}, BKG - region', "labelX" : "DNN bin#", "cats" : ["ee", "em", "mm"]}, 
            "2lss_0tau_ttH" : { "minY" : 0.,   "maxY" :  15.,  "minYerr": 0.501, "maxYerr" : 1.59, "useLogPlot" : False, "label" : '2l ss + 0#tau_{h}, ttH - region', "labelX" : "DNN bin#", "cats" : ["ee", "em", "mm"]}, 
            "ttWctrl"   : { "minY" : -5.,   "maxY" :  115.,  "minYerr": -0.6,  "maxYerr" : 2.85, "useLogPlot" : False},
            "2lss_1tau" : { "minY" : 0,  "maxY" :  20.,   "minYerr":  0.0,  "maxYerr" : 2.75, "useLogPlot" : False, "label" : '2l ss + 1#tau_{h}', "labelX" : "DNN bin#", "cats" : ["BKG - region", "tH - refion", "ttH - region"]},
            "3l_0tau"   : { "minY" : -6,    "maxY" :  229.,  "minYerr": 0.501, "maxYerr" : 1.59, "useLogPlot" : False},
            "3l_0tau_NN" : { "minY" : 0,    "maxY" :  10.,   "minYerr": 0.501, "maxYerr" : 1.59, "useLogPlot" : False, "label" : '3l + 0#tau_{h}, tH - region | ttH region', "labelX" : "DNN bin#", "cats" : ["1b", "2b", "1b", "2b"]},
            "3l_0tau_rest" : { "minY" : 0,    "maxY" :  40.,   "minYerr": 0.501, "maxYerr" : 1.59, "useLogPlot" : False, "label" : '3l + 0#tau_{h}, BKG - region', "labelX" : "DNN bin#", "cats" : ["1b", "2b"]},
            "ttZctrl"   : { "minY" : -6,    "maxY" :  229.,  "minYerr": -0.6,  "maxYerr" : 2.85, "useLogPlot" : False},
            "2l_2tau"   : { "minY" : -0.35, "maxY" :  14.,   "minYerr":  0.0,  "maxYerr" : 2.75, "useLogPlot" : False},
            "3l_1tau"   : { "minY" : -0.2,  "maxY" :  6.9,   "minYerr":  0.0,  "maxYerr" : 5.35, "useLogPlot" : False}, 
            "1l_2tau"   : { "minY" : 0.07,  "maxY" :  5000., "minYerr": 0.59,  "maxYerr" : 1.87, "useLogPlot" : True},
            "2los_1tau" : { "minY" : 0.07,  "maxY" :  5000., "minYerr": -0.6,  "maxYerr" : 2.85, "useLogPlot" : False},
            "0l_2tau"   : { "minY" : 0.07,  "maxY" :  5000., "minYerr": -0.6,  "maxYerr" : 2.85, "useLogPlot" : False},
            "1l_1tau"   : { "minY" : 0.07,  "maxY" :  5000., "minYerr": -0.6,  "maxYerr" : 2.85, "useLogPlot" : False},
            "WZctrl"    : { "minY" : 0.07,  "maxY" :  5000., "minYerr": -0.6,  "maxYerr" : 2.85, "useLogPlot" : False},
            "4l_0tau"   : { "minY" : -0.35, "maxY" :  13.9,  "minYerr": 0.601, "maxYerr" : 2.19, "useLogPlot" : False},
            "ZZctrl"    : { "minY" : -0.35, "maxY" :  13.9,  "minYerr": -0.6,  "maxYerr" : 2.85, "useLogPlot" : False},
        }
    else : sys.exit("analysis " + analysis + " not implemented")
    return info_channel

def options_plot_labels (analysis) : 
    ## for cases where we merge subcategories
    if analysis == "ttH" :
        ### it will have the subcategories for the DNNs
        info_channel = {
            "ttWctrl"   : { "latex" : r'$2\ell ss +0\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
            "ttZctrl"   : { "latex" : r'$2\ell ss +0\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
            "WZctrl"    : { "latex" : r'$2\ell ss +0\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
            "ZZctrl"    : { "latex" : r'$2\ell ss +0\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
            "2lss_0tau" : { "latex" : r'$2\ell ss +0\tau_{h}$', "prefix" : "tHq_2lss_em_" , "mom" : "/afs/cern.ch/work/p/pdas/public/forXanda/cards_Aug9/2lss_em/" }, 
            "2los_1tau" : { "latex" : r'$2\ell os +0\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
            "3l_0tau"   : { "latex" : r'$3\ell +0\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
            "2lss_1tau" : { "latex" : r'$2\ell ss +1\tau_{h}$', "prefix" : "tHq_2lss_mm_" , "mom" : "/afs/cern.ch/work/p/pdas/public/forXanda/cards_Aug9/2lss_mm/"},
            "2l_2tau"   : { "latex" : r'$2\ell +2\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
            "3l_1tau"   : { "latex" : r'$3\ell +1\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" }, 
            "1l_2tau"   : { "latex" : r'$1\ell +2\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
            "0l_2tau"   : { "latex" : r'$0\ell +2\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
            "1l_1tau"   : { "latex" : r'$1\ell +1\tau_{h}$' , "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/"},
            "4l_0tau"   : { "latex" : r'$4\ell +0\tau_{h}$', "prefix" : "tHq_3l_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/tHq_pdas_3l_cards/" },
        }
    else : sys.exit("analysis " + analysis + " not implemented")
    return info_channel

def list_channels_draw(analysis) :
    if analysis == "ttH" :
        #sigs = ["ttH", "tHq", "tHW", "VH"] 
        #conversions = "conversions"
        #fakes       = "fakes_data"
        #flips       = "flips_data"

        info_channel = {
        "ttWctrl"   : { "bkg_proc_from_data" : [fakes, flips], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : []},
        "ttZctrl"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : []},
        "WZctrl"    : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares"],              "signal" : []},
        "ZZctrl"    : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTZ",  "ZZ", "Rares"],                                  "signal" : []},
        "2lss_0tau" : { "bkg_proc_from_data" : [fakes, flips], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", conversions], "signal" : ["ttH", "tHq", "tHW"]}, 
        "2lss_1tau" : { "bkg_proc_from_data" : [fakes, flips], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : ["ttH", "tHq", "tHW"]},
        "3l_0tau"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", conversions, "tHq", "tHW", "VH"], "signal" : ["ttH"]},
        "1l_2tau"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : ["ttH", "tHq", "tHW", "VH"]},
        "2l_2tau"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : ["ttH"]},
        "3l_1tau"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : ["ttH"]}, 
        "1l_2tau"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : ["ttH", "tHq", "tHW", "VH"]},
        "2los_1tau" : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : ["ttH", "tHq", "tHW", "VH"]},
        "0l_2tau"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares"],              "signal" : ["ttH", "tHq", "tHW", "VH"]},
        "1l_1tau"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares"],              "signal" : ["ttH", "tHq", "tHW", "VH"]},
        "4l_0tau"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTZ", "ZZ",  "Rares", conversions],              "signal" : ["ttH"]},
        }
    else : sys.exit("analysis " + analysis + " not implemented")
    return info_channel 