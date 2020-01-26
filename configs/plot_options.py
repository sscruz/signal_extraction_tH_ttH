def sigmatHq(KT, KV) :
    return (2.63*KT**2 + 3.588*KV**2 - 5.21*KT*KV)
def sigmatHW(KT, KV):
    return (2.91*KT**2 + 2.31*KV**2 - 4.22*KT*KV)


def options_plot (analysis, channel, all_procs) :
    dprocs = OrderedDict()
    Hdecays_long = ["hww", "hzz", "htt", "hzg", "hmm"] #
    Hdecays      = ["hww", "htt" , "hzz"] # , "htt"
    ## the order of the entries will be the order of the drawing, that is why this is almost manual
    # TODO: write it on a smarther way
    if analysis == "ttH" :
        #conversions = "conversions"
        #fakes       = "fakes_data"
        #flips       = "flips_data"
        # if label == "none" it means that this process is to be merged with the anterior key
        if "data_fakes" in all_procs       : dprocs["data_fakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Non-prompt"  , "make border" : True}
        if "fakes_mc" in all_procs       : dprocs["fakes_mc"]       = {"color" :  12, "fillStype" : 3345, "label" : "Non-prompt"  , "make border" : True}
        if "flips_mc" in all_procs       : dprocs["flips_mc"]       = {"color" :   1, "fillStype" : 3006, "label" : "Charge mis-m", "make border" : True}
        if "data_flips" in all_procs       : dprocs["data_flips"]       = {"color" :   1, "fillStype" : 3006, "label" : "Charge mis-m", "make border" : True}
        if conversions in all_procs : dprocs[conversions] = {"color" :   5, "fillStype" : 1001, "label" : "Conv."       , "make border" :  True}
        if "Fakes" in all_procs       : dprocs["Fakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Non-prompt"  , "make border" : True}
        if "Flips" in all_procs       : dprocs["Flips"]       = {"color" :   1, "fillStype" : 3006, "label" : "Charge mis-m", "make border" : True}
        if "Conv" in all_procs : dprocs["Conv"] = {"color" :   5, "fillStype" : 1001, "label" : "Conv."       , "make border" :  True}
        if "mcFakes" in all_procs       : dprocs["mcFakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Non-prompt"  , "make border" : True}
        if "mcFlips" in all_procs       : dprocs["mcFlips"]       = {"color" :   1, "fillStype" : 3006, "label" : "Charge mis-m", "make border" : True}
        if "Convs" in all_procs : dprocs["Convs"] = {"color" :   5, "fillStype" : 1001, "label" : "Conv."       , "make border" :  True}
        if "TT" in all_procs     : dprocs["TT"]           = {"color" : 114, "fillStype" : 1001, "label" : 'TT + jets'   , "make border" : True}
        if "Rares" in all_procs     : dprocs["Rares"]     = {"color" : 851, "fillStype" : 1001, "label" : "Rares"       , "make border" : True}
        if "EWK" in all_procs       : dprocs["EWK"]       = {"color" : 610, "fillStype" : 1001, "label" : "EWK"         , "make border" : True}
        if "ZZ" in all_procs        : dprocs["ZZ"]        = {"color" : 52,  "fillStype" : 1001, "label" : "ZZ"          , "make border" : True}
        if "WZ" in all_procs        : dprocs["WZ"]        = {"color" : 6, "fillStype" : 1001, "label" : "WZ"          , "make border" : True}
        if "TTWW" in all_procs :
            dprocs["TTW"]                                 = {"color" : 823, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            dprocs["TTWW"]                                = {"color" : 823, "fillStype" : 1001, "label" : "ttW + ttWW"  , "make border" : True}
        elif "TTW" in all_procs :
            dprocs["TTW"]                                 = {"color" : 823, "fillStype" : 1001, "label" : "ttW"        , "make border" : True}
        if "TTZ" in all_procs       : dprocs["TTZ"]       = {"color" : 822, "fillStype" : 1001, "label" : "ttZ"         , "make border" : True}
        ### signals
        if "HH" in all_procs         : dprocs["HH"]         = {"color" : 4, "fillStype" : 1001, "label" : "none"           , "make border" : False}
        for hig_proc in ["TTWH", "TTZH", "qqH", "tHW", "VH", "WH", "ZH", "ggH"] :
            if hig_proc in all_procs       :
                for decay in Hdecays : # list(set(list(Hdecays)) - set(["htt"])) :
                    if "%s_%s" % (hig_proc, decay) == "tHW_htt" :
                        dprocs["tHW_htt"]       = {"color" : 4, "fillStype" : 1001, "label" : "other H proc."         , "make border" : False}
                    else :
                        dprocs["%s_%s" % (hig_proc, decay)]       = {"color" : 4, "fillStype" : 1001, "label" : "none"         , "make border" : False}
                    #dprocs["%s_htt" % hig_proc]       = {"color" : 4, "fillStype" : 1001, "label" : "none"         , "make border" : False}
        """if "qqH" in all_procs :
            for decay in list(set(list(Hdecays)) - set(["htt"])) :
                dprocs["qqH_%s" % decay]               = {"color" :    4, "fillStype" : 1001, "label" : "none"         , "make border" : False} # ["VH_%s" % decay]
            dprocs["qqH_htt"]                           = {"color" :   4, "fillStype" : 1001, "label" : "none"         , "make border" : False}
            #dprocs["qqH"]                           = {"color" :   4, "fillStype" : 1001, "label" : "none"         , "make border" : False}
        if "tHW" in all_procs :
            for decay in list(set(list(Hdecays)) - set(["htt"]))  :
                dprocs["tHW_%s" % decay]              = {"color" : 4, "fillStype" : 1001, "label" : "none"         , "make border" : False} # "tHW_%s" % decay
            dprocs["tHW_htt"]                         = {"color" : 4, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            #dprocs["tHW"]                         = {"color" : 4, "fillStype" : 1001, "label" : "none"        , "make border" : False}
        if "VH" in all_procs :
            for decay in list(set(list(Hdecays)) - set(["htt"])) :
                dprocs["VH_%s" % decay]                   = {"color" : 4, "fillStype" : 1001, "label" : "none"         , "make border" : False} # ["VH_%s" % decay]
            dprocs["VH_htt"]                              = {"color" : 4, "fillStype" : 1001, "label" : "other Higgs proc"           , "make border" : True}
            dprocs["VH"]                              = {"color" : 4, "fillStype" : 1001, "label" : "other Higgs proc"           , "make border" : True}
        if "ggH" in all_procs :
            for decay in list(set(list(Hdecays)) - set(["htt"])) :
                dprocs["ggH_%s" % decay]               = {"color" :   2, "fillStype" : 3005, "label" : "none"         , "make border" : False} # ["VH_%s" % decay]
            dprocs["ggH_htt"]                           = {"color" :   2, "fillStype" : 3005, "label" : "ggH"         , "make border" : True}
            #dprocs["ggH"]                           = {"color" :   2, "fillStype" : 3005, "label" : "ggH"         , "make border" : True}"""
        if "ttH" in all_procs :
            for decay in list(set(list(Hdecays_long)) - set(["htt"])) :
                dprocs["ttH_%s" % decay]                 = {"color" :   2, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            dprocs["ttH_htt"]                                 = {"color" :   2, "fillStype" : 1001, "label" : "ttH"         , "make border" : True}
            #dprocs["ttH"]                                 = {"color" :   2, "fillStype" : 1001, "label" : "ttH"         , "make border" : True}
        if "tHq" in all_procs :
            for decay in list(set(list(Hdecays)) - set(["htt"])) :
                dprocs["tHq_%s" % decay]              = {"color" : 205, "fillStype" : 1001, "label" : "none"        , "make border" : False} # "tHq_%s" % decay
            dprocs["tHq_htt"]                             = {"color" : 205, "fillStype" : 1001, "label" : "tHq * 3"           , "make border" : True}
            #dprocs["tHq"]                             = {"color" : 205, "fillStype" : 1001, "label" : "tHq * 3"           , "make border" : True}
        # change the order of the stack if channel is dominated by fakes
        if channel in [ "1l_2tau", "2l_2tau"] :
            ## remove "fakes_data" from first entry and add as last
            del dprocs[fakes]
            dprocs[fakes]                                 = {"color" :   1, "fillStype" : 3005, "label" : "Mis."        , "make border" : True}
        if channel in ["0l_2tau", "1l_1tau", "2los_1tau"] :
            #del dprocs["DY"]
            dprocs["DY"]                                  = {"color" : 221, "fillStype" : 1001, "label" : "DY"         , "make border" : True}
            del dprocs[fakes]
            dprocs[fakes]                                 = {"color" :   1, "fillStype" : 3005, "label" : "Mis."        , "make border" : True}
            del dprocs["TT"]
            dprocs["TT"]                                  = {"color" : 17, "fillStype" : 1001, "label" : 'TT + jets'   , "make border" : True}
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
            "2lss_0tau_NN" : {
                "minY" : 1.,   "maxY" :  10000.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : True,
                "label" : '2l ss + 0#tau_{h}, ttW - region',
                "labelX" : "DNN bin#",
                "position_cats": 250. ,
                "cats" : ["ee", "em", "mm"]
                },
            "2lss_0tau_rest" : {
                "minY" : 1.,   "maxY" :  70.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '2l ss + 0#tau_{h}, ttH - region',
                "labelX" : "DNN bin#",
                "position_cats": 45. ,
                "cats" : ["ee", "em", "mm"]
                },
            "2lss_0tau_ttW" : {
                "minY" : 1.,   "maxY" :  20.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '2l ss + 0#tau_{h}, ttW - region',
                "labelX" : "DNN bin#",
                "position_cats": 12. ,
                "cats" : ["ee", "em", "mm"]
                },
            "2lss_0tau_ttH" : {
                "minY" : 1.,   "maxY" :  25.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '2l ss + 0#tau_{h}, ttH - region',
                "labelX" : "DNN bin#",
                "position_cats": 12. ,
                "cats" : ["ee", "em", "mm"]
                },
            "2lss_0tau_tH" : {
                "minY" : 1.,   "maxY" :  50.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '2l ss + 0#tau_{h}, tHq - region',
                "labelX" : "DNN bin#",
                "position_cats": 30. ,
                "cats" : ["ee", "em", "mm"]
                },
            "ttWctrl"   : { "minY" : -5.,   "maxY" :  115.,  "minYerr": -0.6,  "maxYerr" : 2.85, "useLogPlot" : False, "label" : '2l + 2#tau_{h}', "labelX" : "BDT", "cats" : [""]},
            #"2lss_1tau" : { "minY" : 0,  "maxY" :  20.,   "minYerr":  0.0,  "maxYerr" : 2.75, "useLogPlot" : False, "label" : '2l ss + 1#tau_{h}', "labelX" : "DNN bin#", "cats" : ["BKG - region", "tH - refion", "ttH - region"]},
            "2lss_1tau_plain" : {
                "minY" : 0,  "maxY" :  25.,
                "minYerr":  0.0,  "maxYerr" : 2.75,
                "useLogPlot" : False,
                "label" : '2l ss + 1#tau_{h}',
                "labelX" : "DNN bin#", "cats" : [""]
                },
            "2lss_1tau" : {
                "minY" : 0,  "maxY" :  18.0,
                "minYerr":  0.0,  "maxYerr" : 2.75,
                "useLogPlot" : False,
                "label" : '2l ss + 1#tau_{h}',
                "labelX" : "DNN bin#",
                "position_cats": 10.5 ,
                "cats" : ["BKG-reg", "tH-reg", "ttH-reg"]
                },
            "3l_0tau"   : {
                "minY" : -6,    "maxY" :  229.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}',
                "labelX" : "BDT", "cats" : [""]
                },
            "3l_0tau_NN"   : {
                "minY" : -6,    "maxY" :  229.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}',
                "labelX" : "BDT", "cats" : ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9", "ch10", "ch11", "ch12", "ch13", "ch11", "ch12", "ch13"]
                },
            "3l_0tau_ttH" : {
                "minY" : 0,    "maxY" :  40.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}, ttH-region',
                "labelX" : "DNN bin#",
                "position_cats": 20. ,
                "cats" : ["bl", "bt"]
                },
            "3l_0tau_tH" : {
                "minY" : 0,    "maxY" :  15.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}, tHq-region',
                "labelX" : "DNN bin#",
                "position_cats": 10. ,
                "cats" : ["bl", "bt"]
                },
            "3l_0tau_rest" : {
                "minY" : 0,    "maxY" :  28.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}, BKG region',
                "labelX" : "DNN bin#",
                "position_cats": 8. ,
                "cats" : ['', "", '', '', '', '', '']
                #"cats" : ['', 'emm bl', "eem bl",  'mmm bl', 'emm bt', "eem bt",  'mmm bt']
                },
            "3lctrl" : {
                "minY" : 0.1,    "maxY" :  100000.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : True,
                "label" : '3l + 0#tau_{h} CR',
                "labelX" : "bin#",
                "position_cats": 600. ,
                "cats" : ["eee" , "eem", "emm", "mmm"]
                },
            "4lctrl" : {
                "minY" : 0.1,    "maxY" :  50000.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : True,
                "label" : '4l + 0#tau_{h} CR',
                "labelX" : "DNN bin#",
                "position_cats": 300. ,
                "cats" : [""]
                },
            "2l_2tau"   : {
                "minY" : 0.0,
                "maxY" :  5.5,
                "minYerr":  0.0,
                "maxYerr" : 2.75,
                "useLogPlot" : False,
                "label" : '2l + 2#tau_{h}',
                "position_cats": 300. ,
                "labelX" : "BDT bin#",
                "cats" : [""]
                },
            "3l_1tau"   : {
                "minY" : 0.,  "maxY" :  3.5,
                "minYerr":  0.0,  "maxYerr" : 5.35,
                "useLogPlot" : False,
                "label" : '3l + 1#tau_{h}',
                "labelX" : "BDT bin#",
                "position_cats": 300. ,
                "cats" : [""]
                },
            "1l_2tau"   : {
                "minY" : 0.1,  "maxY" :  5000.,
                "minYerr": 0.59,  "maxYerr" : 1.87,
                "useLogPlot" : True,
                "label" : '1l + 2#tau_{h}',
                "position_cats": 300. ,
                "labelX" : "BDT", "cats" : [""]
                },
            "2los_1tau" : {
                "minY" : 0.07,  "maxY" :  5000.,
                "minYerr": -0.6,  "maxYerr" : 2.85,
                "useLogPlot" : True,
                "label" : '2l os + 1#tau_{h}',
                "position_cats": 300. ,
                "labelX" : "BDT", "cats" : [""]
                },
            "0l_2tau"   : {
                "minY" : 0.07,  "maxY" :  100000.,
                "minYerr": -0.6,  "maxYerr" : 2.85,
                "useLogPlot" : True,
                "label" : '0l + 2#tau_{h}',
                "labelX" : "BDT",
                "position_cats": 300. ,
                "cats" : [""]
                },
            "1l_1tau"   : {
                "minY" : 1.,  "maxY" :  1000000.,
                "minYerr": -0.6,  "maxYerr" : 2.85,
                "useLogPlot" : True,
                "label" : '1l + 1#tau_{h}',
                "position_cats": 300. ,
                "labelX" : "BDT", "cats" : [""]
                },
            "4l_0tau"   : {
                "minY" : 0.,
                "maxY" :  7.5,
                "minYerr": 0.601,
                "maxYerr" : 2.19,
                "useLogPlot" : False,
                "label" : '4l + 0#tau_{h}',
                "position_cats": 300. ,
                "labelX" : "BDT bin#", "cats" : [""]
                },
            "2lss_0tau" : {
                "minY" : -0.35, "maxY" :  13.9,
                "minYerr": 0.601, "maxYerr" : 2.19,
                "useLogPlot" : False,
                "label" : '2l ss + 0#tau_{h}',
                "labelX" : "BDT",
                "cats" : [""]
                },
            "ZZctrl"    : { "minY" : -0.35, "maxY" :  13.9,  "minYerr": -0.6,  "maxYerr" : 2.85, "useLogPlot" : False, "label" : '2l + 2#tau_{h}', "labelX" : "BDT", "cats" : [""]},
        }
    else : sys.exit("analysis " + analysis + " not implemented")
    return info_channel

def options_plot_labels (analysis) :
    ## for cases where we merge subcategories
    ## mainly for the acc X eff plot
    if analysis == "ttH" :
        ### it will have the subcategories for the DNNs
        info_channel = {
            "2lss_0tau" : {
                "latex" : r'$2\ell ss +0\tau_{h}$',
                "prefix" : "datacard_2lss_mvaDiscr_2lss_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_2lss_0tau/",
                "stat" : "high"
            },
            "2lss_1tau" : {
                "latex" : r'$2\ell ss +1\tau_{h}$',
                "prefix" : "datacard_2lss_1tau_sumOS_mvaOutput_final_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_2lss_1tau/",
                "stat" : "high"
            },
            "2los_1tau" : {
                "latex" : r'$2\ell os +1\tau_{h}$',
                "prefix" : "datacard_2los_1tau_mTauTauVis_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_2los_1tau/",
                "stat" : "high"
            },
            "3l_0tau"   : {
                "latex" : r'$3\ell +0\tau_{h}$',
                "prefix" : "datacard_3l_OS_numJets_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_3l_0tau/",
                "stat" : "high"
                },
            #"2lss_1tau" : { "latex" : r'$2\ell ss +1\tau_{h}$', "prefix" : "tHq_2lss_mm_" , "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_2lss_1tau/", "stat" : "low"},
            "2l_2tau"   : {
                "latex" : r'$2\ell +2\tau_{h}$',
                "prefix" : "datacard_2l_2tau_lepdisabled_taudisabled_sumOS_mvaOutput_final_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_2l_2tau/",
                "stat" : "low"
            },
            "3l_1tau"   : {
                "latex" : r'$3\ell +1\tau_{h}$',
                "prefix" : "datacard_3l_1tau_OS_EventCounter_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_3l_1tau/",
                "stat" : "low"
            },
            "1l_2tau"   : {
                "latex" : r'$1\ell +2\tau_{h}$',
                "prefix" : "datacard_1l_2tau_mvaOutput_final_2017_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/1l_2tau_master10X/",
                "stat" : "high"
            },
            "0l_2tau"   : {
                "latex" : r'$0\ell +2\tau_{h}$',
                "prefix" : "datacard_0l_2tau_0l_2tau_mTauTau_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_0l_2tau/",
                "stat" : "high"
            },
            "1l_1tau"   : {
                "latex" : r'$1\ell +1\tau_{h}$' ,
                "prefix" : "datacard_1l_1tau_1l_1tau_mTauTau_disabled_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_1l_1tau/",
                "stat" : "high"
            },
            "4l_0tau"   : {
                "latex" : r'$4\ell +0\tau_{h}$',
                "prefix" : "datacard_4l_OS_numJets_" ,
                "mom" : "/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/higgs_4l_0tau/",
                "stat" : "low"
            },
        }
    else : sys.exit("analysis " + analysis + " not implemented")
    return info_channel

def list_channels_draw(analysis) :
    if analysis == "ttH" :
        sigs = ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "TTWH", "TTZH"]

        info_channel = {
        "ttWctrl"   : { "bkg_proc_from_data" : [fakes, flips], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : []},
        "ttZctrl"   : { "bkg_proc_from_data" : [fakes       ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions], "signal" : []},
        #"3lctrl"    : { "bkg_proc_from_data" : [fakes, flips], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares"],              "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]},
        #"4lctrl"    : { "bkg_proc_from_data" : [fakes, flips], "bkg_procs_from_MC"  : ["TTZ",  "ZZ", "Rares"],                                  "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]},
        "2lss_0tau" : {
            "bkg_proc_from_data" : [ fakes, "mcFlips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"], ##  EWK should be substituted by WZ and ZZ and Conv uniformized with the rest --- update that!
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]
            },
        "2lss_0tau_NN" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"], ##  EWK should be substituted by WZ and ZZ and Conv uniformized with the rest --- update that!
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]
            },
        "2lss_0tau_tH" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"], ##  EWK should be substituted by WZ and ZZ and Conv uniformized with the rest --- update that!
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]
            },
        "2lss_0tau_ttH" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"], ##  EWK should be substituted by WZ and ZZ and Conv uniformized with the rest --- update that!
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]
            },
        "2lss_0tau_ttW" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"], ##  EWK should be substituted by WZ and ZZ and Conv uniformized with the rest --- update that!
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]
            },
        "2lss_0tau_rest" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"], ##  EWK should be substituted by WZ and ZZ and Conv uniformized with the rest --- update that!
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]
            },
        "2lss_1tau" : {
            "bkg_proc_from_data" : [fakes, flips], # , "data_flips"
            "bkg_procs_from_MC"  : ["TTW",  "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "HH", "TTWH", "TTZH"]
            },
        "2lss_1tau_NN" : {
            "bkg_proc_from_data" : [fakes, flips], # , "data_flips"
            "bkg_procs_from_MC"  : ["TTW",  "TTZ", "WZ", "ZZ", "Rares", conversions, "TT", "TTWH", "TTZH", "HH",],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "HH"] # , "TTWH", "TTZH"
            },
        "3l_0tau"   : {
            "bkg_proc_from_data" : [fakes, flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "tHq", "tHW", "VH"],
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "HH", "TTWH", "TTZH"]
            },
        "3lctrl"   : {
            "bkg_proc_from_data" : [fakes, flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions],
            "signal" : ["ttH", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"]
            },
        "4lctrl"   : {
            "bkg_proc_from_data" : [fakes, flips ],
            "bkg_procs_from_MC"  : ["TTZ", "WZ", "ZZ", "Rares", conversions],
            "signal" : ["ttH", ]
            },
        "3l_0tau_NN"   : {
            "bkg_proc_from_data" : [fakes,  flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"], # "EWK",
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"]
            },
        "3l_0tau_ttH"   : {
            "bkg_proc_from_data" : [fakes,  flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"], # "EWK",
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"]
            },
        "3l_0tau_tH"   : {
            "bkg_proc_from_data" : [fakes,  flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"], # "EWK",
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"]
            },
        "3l_0tau_rest"   : {
            "bkg_proc_from_data" : ["data_fakes" ], # ,  flips
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ",  "WZ", "ZZ", "Rares", conversions, "TT"], # "EWK",
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "HH", "TTWH", "TTZH"]
            },
        "1l_2tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "VH", "HH", "TTWH", "TTZH"]
            },
        "2l_2tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "VH", "qqH", "VH", "HH", "TTWH", "TTZH"]
            },
        "3l_1tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "TT", "Rares", conversions],
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]
            },
        "2los_1tau" : {
            "bkg_proc_from_data" : [fakes, flips],
            "bkg_procs_from_MC"  : ["TTW",  "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "VH", "HH", "TTWH", "TTZH"]
        },
        "0l_2tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "DY", "Rares", "TT", conversions, "EWK"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ggH", "qqH", "ZH", "HH", "TTWH", "TTZH"]
            },
        "1l_1tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "DY", "Rares", "TT", conversions, "EWK"],
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "WH", "ZH", "HH", "TTWH", "TTZH"]
            },
        "4l_0tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "DY", "Rares", "TT", conversions, "EWK"],
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"]},
            }
    else : sys.exit("analysis " + analysis + " not implemented")
    return info_channel
