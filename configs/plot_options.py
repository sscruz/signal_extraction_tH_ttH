def sigmatHq(KT, KV) :
    return (2.63*KT**2 + 3.588*KV**2 - 5.21*KT*KV)
def sigmatHW(KT, KV):
    return (2.91*KT**2 + 2.31*KV**2 - 4.22*KT*KV)


def options_plot (analysis, channel, all_procs, leading_minor_H_local) :
    dprocs = OrderedDict()
    Hdecays_long = [ "hww", "hzz", "htt",] #  "hzg", "hmm"
    Hdecays      = ["hww", "htt" , "hzz"]
    other_H_proc = 0
    ## the order of the entries will be the order of the drawing, that is why this is almost manual
    # TODO: write it on a smarther way
    if analysis == "ttH" :
        #conversions = "conversions"
        #fakes       = "fakes_data"
        #flips       = "flips_data"
        # if label == "none" it means that this process is to be merged with the anterior key
        if "data_fakes" in all_procs       : dprocs["data_fakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Fakes"  , "make border" : True}
        if "fakes_mc" in all_procs       : dprocs["fakes_mc"]       = {"color" :  12, "fillStype" : 3345, "label" : "Fakes"  , "make border" : True}
        if "flips_mc" in all_procs       : dprocs["flips_mc"]       = {"color" :   1, "fillStype" : 3006, "label" : "Flips", "make border" : True}
        if "data_flips" in all_procs       : dprocs["data_flips"]       = {"color" :   1, "fillStype" : 3006, "label" : "Flips", "make border" : True}
        if conversions in all_procs : dprocs[conversions] = {"color" :   5, "fillStype" : 1001, "label" : "Conversions"       , "make border" :  True}
        if "Fakes" in all_procs       : dprocs["Fakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Fakes"  , "make border" : True}
        if "Flips" in all_procs       : dprocs["Flips"]       = {"color" :   1, "fillStype" : 3006, "label" : "Flips", "make border" : True}
        if "Conv" in all_procs : dprocs["Conv"] = {"color" :   5, "fillStype" : 1001, "label" : "Conversions"       , "make border" :  True}
        if "mcFakes" in all_procs       : dprocs["mcFakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Fakes"  , "make border" : True}
        if "mcFlips" in all_procs       : dprocs["mcFlips"]       = {"color" :   1, "fillStype" : 3006, "label" : "Flips", "make border" : True}
        if "Convs" in all_procs : dprocs["Convs"] = {"color" :   5, "fillStype" : 1001, "label" : "Conversions"       , "make border" :  True}
        if "TT" in all_procs     : dprocs["TT"]           = {"color" : 114, "fillStype" : 1001, "label" : 'TT + jets'   , "make border" : True}
        if "Rares" in all_procs     : dprocs["Rares"]     = {"color" : 851, "fillStype" : 1001, "label" : "Rares"       , "make border" : True}
        if "EWK" in all_procs       : dprocs["EWK"]       = {"color" : 610, "fillStype" : 1001, "label" : "EWK"         , "make border" : True}
        if "ZZ" in all_procs        : dprocs["ZZ"]        = {"color" : 52,  "fillStype" : 1001, "label" : "ZZ"          , "make border" : True}
        if "WZ" in all_procs        : dprocs["WZ"]        = {"color" : 6, "fillStype" : 1001, "label" : "WZ"          , "make border" : True}
        if "TTWW" in all_procs :
            dprocs["TTW"]                                 = {"color" : 823, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            dprocs["TTWW"]                                = {"color" : 823, "fillStype" : 1001, "label" : "ttW(W)"  , "make border" : True}
        elif "TTW" in all_procs :
            dprocs["TTW"]                                 = {"color" : 823, "fillStype" : 1001, "label" : "ttW(W)"        , "make border" : True}
        if "TTZ" in all_procs       : dprocs["TTZ"]       = {"color" : 822, "fillStype" : 1001, "label" : "ttZ"         , "make border" : True}
        ### signals
        if "HH" in all_procs         : dprocs["HH"]         = {"color" : 4, "fillStype" : 1001, "label" : "none"           , "make border" : False}
        for hig_proc in ["TTWH", "TTZH", "qqH", "VH", "WH", "ZH", "ggH"] :
            if hig_proc in all_procs       :
                for decay in Hdecays : # list(set(list(Hdecays)) - set(["htt"])) :
                    #if not "%s_%s" % (hig_proc, decay) in all_procs :
                    #    continue
                    #if other_H_proc == 0 :
                    #    dprocs["%s_%s" % (hig_proc, decay)]       = {"color" : 4, "fillStype" : 1001, "label" : "Other H processes"       , "make border" : False}
                    #    other_H_proc = 1
                    if "%s_%s" % (hig_proc, decay) == leading_minor_H_local : #
                        dprocs[leading_minor_H_local]       = {"color" : 4, "fillStype" : 1001, "label" : "VH + ggH + qqH"      , "make border" : False} # "Other H processes" "tHW + VH + ggH + qqH + HH + ttVH"
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
        if "tHW" in all_procs :
            #for decay in list(set(list(Hdecays)) - set(["htt"])) :
            #    dprocs["tHW_%s" % decay]              = {"color" : 208, "fillStype" : 1001, "label" : "none"        , "make border" : False} # "tHq_%s" % decay
            #dprocs["tHW_htt"]                             = {"color" : 208, "fillStype" : 1001, "label" : "tH"           , "make border" : True}
            for decay in list(Hdecays) :
                dprocs["tHW_%s" % decay]              = {"color" : 208, "fillStype" : 1001, "label" : "none"        , "make border" : False} # "tHq_%s" % decay
        if "tHq" in all_procs :
            for decay in list(set(list(Hdecays)) - set(["hww"])) :
                dprocs["tHq_%s" % decay]              = {"color" : 208, "fillStype" : 1001, "label" : "none"        , "make border" : False} # "tHq_%s" % decay
            dprocs["tHq_hww"]                             = {"color" : 208, "fillStype" : 1001, "label" : "tH"           , "make border" : True}
            #dprocs["tHq"]                             = {"color" : 205, "fillStype" : 1001, "label" : "tHq * 3"           , "make border" : True}
        # change the order of the stack if channel is dominated by fakes
        if "ttH" in all_procs :
            for decay in list(set(list(Hdecays_long)) - set(["htt"])) :
                dprocs["ttH_%s" % decay]                 = {"color" :   2, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            dprocs["ttH_htt"]                                 = {"color" :   2, "fillStype" : 1001, "label" : "ttH"         , "make border" : True}
            #dprocs["ttH"]                                 = {"color" :   2, "fillStype" : 1001, "label" : "ttH"         , "make border" : True}
        if channel in [ "1l_2tau", "2l_2tau"] :
            ## remove "fakes_data" from first entry and add as last
            del dprocs["data_fakes"]
            dprocs["data_fakes"]                                 = {"color" :   1, "fillStype" : 3005, "label" : "Fakes"        , "make border" : True}
        if channel in ["0l_2tau", "1l_1tau", "2los_1tau"] :
            #del dprocs["DY"]
            dprocs["DY"]                                  = {"color" : 221, "fillStype" : 1001, "label" : "DY"         , "make border" : True}
            del dprocs[fakes]
            dprocs[fakes]                                 = {"color" :   1, "fillStype" : 3005, "label" : "Fakes"        , "make border" : True}
            del dprocs["TT"]
            dprocs["TT"]                                  = {"color" : 17, "fillStype" : 1001, "label" : 'TT + jets'   , "make border" : True}
    else : sys.exit("analysis " + analysis + " not implemented")
    return dprocs

def Higgs_proc_decay (proc) :
    Hdecays_long = [  "htt",  "hww", "hzz",  "hzg", "hmm"] #
    Hdecays      = ["hww", "hzz", "htt" ]
    #sum(higgs_procs,[])
    return sum([ [y + "_" + x  for x in decays if not (x in ["hzz", "htt", "hzg", "hmm"] and y != "ttH")] for y in sigs], [])

def options_plot_ranges (analysis) :
    if analysis == "ttH" :
        ### it will have the subcategories for the DNNs
        info_channel = {
            "2lss_0tau_rest" : {
                "minY" : 0,   "maxY" :  95.,
                "minYerr": -0.64, "maxYerr" : 1.1,
                "useLogPlot" : False,
                "label" : "2l ss + 0#tau_{h}, Other BKG node",
                "labelX" : "Bin number",
                "position_cats": 55. ,
                "list_cats" : ["ttH_2lss_0tau_ee_Restnode_2018", "ttH_2lss_0tau_em_Restnode_2018", "ttH_2lss_0tau_mm_Restnode_2018"],
                "list_cats_original" : ["ttH_2lss_0tau_ee_Restnode_2018", "ttH_2lss_0tau_em_Restnode_2018", "ttH_2lss_0tau_mm_Restnode_2018"],
                "cats" : [['ee'], ['e#mu'], ['#mu#mu']],
                "catsX" :  [ 2.5, 10.5, 20.0 ]
                },
            "2lss_0tau_ttW" : {
                "minY" : 0.,   "maxY" :  45.,
                "minYerr": -1.1, "maxYerr" : 2.74,
                "useLogPlot" : False,
                "label" : '2l ss + 0#tau_{h}, t#bar{t}W node',
                "labelX" : "Bin number",
                "position_cats": 26.0 ,
                "list_cats" : ["ttH_2lss_0tau_ee_ttWnode_2018", "ttH_2lss_0tau_em_ttWnode_2018", "ttH_2lss_0tau_mm_ttWnode_2018"],
                "list_cats_original" : ["ttH_2lss_0tau_ee_ttWnode_2018", "ttH_2lss_0tau_em_ttWnode_2018", "ttH_2lss_0tau_mm_ttWnode_2018"],
                "cats" : [['ee'], ['e#mu'], ['#mu#mu']],
                "catsX" :  [ 1.5, 14.0, 31.0 ]
                },
            "2lss_0tau_ttH" : {
                "minY" : 0,   "maxY" :  35.,
                "minYerr": -1.1, "maxYerr" : 2.35,
                "useLogPlot" : False,
                "label" : '2l ss + 0#tau_{h}, t#bar{t}H node',
                "labelX" : "Bin number",
                "position_cats": 19. ,
                "list_cats" : ["ttH_2lss_0tau_ee_ttHnode_2018", "ttH_2lss_0tau_em_ttHnode_2018", "ttH_2lss_0tau_mm_ttHnode_2018"],
                "list_cats_original" : ["ttH_2lss_0tau_ee_ttHnode_2018", "ttH_2lss_0tau_em_ttHnode_2018", "ttH_2lss_0tau_mm_ttHnode_2018"],
                "cats" : [['ee'], ['e#mu'], ['#mu#mu']],
                "catsX" :  [ 1.5, 10.0, 23.0 ]
                },
            "2lss_0tau_tH" : {
                "minY" : 0,   "maxY" :  75.,
                "minYerr": -1.1, "maxYerr" : 1.1,
                "useLogPlot" : False,
                "label" : '2l ss + 0#tau_{h}, tHQ node',
                "labelX" : "Bin number",
                "position_cats": 42. ,
                "list_cats" : ["ttH_2lss_0tau_ee_tHQnode_2018", "ttH_2lss_0tau_em_tHQnode_2018", "ttH_2lss_0tau_mm_tHQnode_2018"],
                "list_cats_original" : ["ttH_2lss_0tau_ee_tHQnode_2018", "ttH_2lss_0tau_em_tHQnode_2018", "ttH_2lss_0tau_mm_tHQnode_2018"],
                "cats" : [['ee'], ['e#mu'], ['#mu#mu']],
                "catsX" :  [ 1.0, 8.0, 17.5 ]
                },
            "2lss_1tau_plain" : {
                "minY" : 0,  "maxY" :  10.,
                "minYerr":  0.0,  "maxYerr" : 2.75,
                "useLogPlot" : False,
                "label" : '2l ss + 1#tau_{h}',
                "list_cats" : ["ttH_2lss_1tau"],
                "list_cats_original" : ["ttH_2lss_1tau"],
                "position_cats": 300. ,
                "labelX" : "Bin number",
                "cats" : ["ttH_2lss_1tau"],
                "catsX" : []
                },
            "2lss_1tau_no_miss" : {
                "minY" : 0,  "maxY" :  25.,
                "minYerr":  0.0,  "maxYerr" : 2.75,
                "useLogPlot" : False,
                "label" : '2l ss + 1#tau_{h}',
                "list_cats" : [],
                "list_cats_original" : [],
                "position_cats": 300. ,
                "labelX" : "Bin number",
                "cats" : ["ttH_2lss_1tau_nomiss"],
                "catsX" : []
                },
            "2lss_1tau" : {
                "minY" : 0,  "maxY" :  42.0,
                "minYerr":  -1.1,  "maxYerr" : 2.8,
                "useLogPlot" : False,
                "label" : '2l ss + 1#tau_{h}',
                "labelX" : "Bin number",
                "position_cats": 22.5 ,
                "list_cats" : ["ttH_2lss_1tau_rest_2018", "ttH_2lss_1tau_tH_2018", "ttH_2lss_1tau_ttH_2018"],
                "list_cats_original" : ["ttH_2lss_1tau_rest_2018", "ttH_2lss_1tau_tH_2018", "ttH_2lss_1tau_ttH_2018"],
                "cats" :  [
                ["'Other'", " node"],
                [' tHQ', 'node'],
                [' ttH', 'node'] ],
                "catsX" :  [
                0.8,
                5.6,
                10.6 ]
                },
            "3l_0tau"   : {
                "minY" : -6,    "maxY" :  10.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}',
                "position_cats": 20. ,
                "list_cats" : ["ttH_3l_0tau_2018"],
                "list_cats_original" : ["ttH_3l_0tau"],
                "labelX" : "BDT",
                "cats" : [""],
                "catsX" : []
                },
            "3l_0tau_NN"   : {
                "minY" : -6,    "maxY" :  229.,
                "minYerr": 0.501, "maxYerr" : 1.59,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}',
                "list_cats" : [],
                "list_cats_original" : [],
                "labelX" : "BDT",
                "cats" :   ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9", "ch10", "ch11", "ch12", "ch13", "ch11", "ch12", "ch13"],
                "catsX" :  [ 1.0,   10.0,  10.0,  10.0,  10.0,  10.0,  10.0,  10.0,  10.0,   10.0,   10.0,   10.0, 10.0,     10.0,   10.0,   10.0 ]
                },
            "3l_0tau_ttH" : {
                "minY" : 0,    "maxY" :  40.,
                "minYerr":  -1.1,  "maxYerr" : 1.64,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}, t#bar{t}H output node',
                "labelX" : "Bin number",
                "position_cats": 20. ,
                "list_cats" : ["ttH_3l_0tau_ttH_bl_2018", "ttH_3l_0tau_ttH_bt_2018"],
                "list_cats_original" : ["ttH_3l_0tau_ttH_bl_2018", "ttH_3l_0tau_ttH_bt_2018"],
                "cats" : [["bl"], ["bt"]],
                "catsX" :  [ 1.2, 5.8 ]
                },
            "3l_0tau_tH" : {
                "minY" : 0,    "maxY" :  25.,
                "minYerr":  -1.1,  "maxYerr" : 1.64,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}, tH output node',
                "labelX" : "Bin number",
                "position_cats": 13. ,
                "list_cats" : ["ttH_3l_0tau_tH_bl_2018", "ttH_3l_0tau_tH_bt_2018"],
                "list_cats_original" : ["ttH_3l_0tau_tH_bl_2018", "ttH_3l_0tau_tH_bt_2018"],
                "cats" : [["bl"], ["bt"]],
                "catsX" :  [ 2.5, 7.5 ]
                },
            "3l_0tau_rest" : {
                "minY" : 0,    "maxY" :  45.,
                "minYerr":  -1.1,  "maxYerr" : 1.84,
                "useLogPlot" : False,
                "label" : '3l + 0#tau_{h}, Other BKG node',
                "labelX" : "Bin number",
                "position_cats": 26. ,
                "list_cats" : [
                    "ttH_3l_0tau_rest_eee_2018",
                    "ttH_3l_0tau_rest_eem_bl_2018",
                    "ttH_3l_0tau_rest_emm_bl_2018",
                    "ttH_3l_0tau_rest_mmm_bl_2018",
                    "ttH_3l_0tau_rest_emm_bt_2018",
                    "ttH_3l_0tau_rest_mmm_bt_2018",
                    "ttH_3l_0tau_rest_eem_bt_2018",
                     ],
                "list_cats_original" : [
                    "ttH_3l_0tau_rest_eee_2018",
                    "ttH_3l_0tau_rest_eem_bl_2018",
                    "ttH_3l_0tau_rest_emm_bl_2018",
                    "ttH_3l_0tau_rest_mmm_bl_2018",
                    "ttH_3l_0tau_rest_emm_bt_2018",
                    "ttH_3l_0tau_rest_mmm_bt_2018",
                    "ttH_3l_0tau_rest_eem_bt_2018",
                     ],
                "cats" : [
                ["e", "e", "e"],
                ["ee#mu", " bl"],
                ["e#mu#mu", " bl"],
                ["#mu#mu#mu", " bl"],
                ["e", "e", "m", "bt"],
                ["e",'#mu', '#mu', "bt"],
                ["#mu","#mu","#mu", "bt"],
                ],
                "catsX" :  [ -0.1, 1.8, 5.8, 9.4, 11.6, 12.6, 13.6]
                },
            "3lctrl" : {
                "minY" : 0.1,    "maxY" :  100000.,
                "minYerr": -1.1, "maxYerr" : 2.5,
                "useLogPlot" : True,
                "label" : '3l-CR',
                "labelX" : "Bin number",
                "position_cats": 750. ,
                "list_cats" : ["ttH_cr_3l_2018_eee_cr", "ttH_cr_3l_2018_eem_cr", "ttH_cr_3l_2018_emm_cr", "ttH_cr_3l_2018_mmm_cr"],
                "list_cats_original" : ["ttH_cr_3l_2018_eee_cr", "ttH_cr_3l_2018_eem_cr", "ttH_cr_3l_2018_emm_cr", "ttH_cr_3l_2018_mmm_cr"],
                "cats" : [ ['eee'], ['ee#mu'], ['e#mu#mu'], ['#mu#mu#mu']],
                "catsX" :  [ 3.5, 14.5, 27.0, 39.0]
                },
            "4lctrl" : {
                "minY" : 0.1,    "maxY" :  100000.,
                "minYerr": -1.1, "maxYerr" : 1.8,
                "useLogPlot" : True,
                "label" : '4l-CR',
                "labelX" : "Bin number",
                "position_cats": 300. ,
                "list_cats" : ["ttH_cr_4l_2018"],
                "list_cats_original" : ["ttH_cr_4l_2018"],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "2lss_3j" : {
                "minY" : 0.,    "maxY" :  50.,
                "minYerr": -1.02, "maxYerr" : 1.32,
                "useLogPlot" : False,
                "label" : '2lss-3j ',
                "labelX" : "mass(ll) (GeV)",
                "position_cats": 300. ,
                "list_cats" : [],
                "list_cats_original" : [],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            #######
            "ttH_2lss_3j_ee" : {
                "minY" : 0.,    "maxY" :  50.,
                "minYerr": -1.02, "maxYerr" : 1.32,
                "useLogPlot" : False,
                "label" : " ee",
                "labelX" : "mass(ll) (GeV)",
                "position_cats": 300. ,
                "list_cats" : ["ttH_2lss_3j_2018_ee"],
                "list_cats_original" : ["ttH_2lss_3j_2018_ee"],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "ttH_2lss_3j_em_neg" : {
                "minY" : 0.,    "maxY" :  50.,
                "minYerr": -1.02, "maxYerr" : 1.32,
                "useLogPlot" : False,
                "label" : " e#mu --",
                "labelX" : "mass(ll) (GeV)",
                "position_cats": 300. ,
                "list_cats" : ["ttH_2lss_3j_2018_em_neg"],
                "list_cats_original" : ["ttH_2lss_3j_2018_em_neg"],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "ttH_2lss_3j_em_pos" : {
                "minY" : 0.,    "maxY" :  50.,
                "minYerr": -1.02, "maxYerr" : 1.32,
                "useLogPlot" : False,
                "label" : " e#mu ++",
                "labelX" : "mass(ll) (GeV)",
                "position_cats": 300. ,
                "list_cats" : ["ttH_2lss_3j_2018_em_pos"],
                "list_cats_original" : ["ttH_2lss_3j_2018_em_pos"],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "ttH_2lss_3j_mm_neg" : {
                "minY" : 0.,    "maxY" :  50.,
                "minYerr": -1.02, "maxYerr" : 1.32,
                "useLogPlot" : False,
                "label" : " #mu#mu --",
                "labelX" : "mass(ll) (GeV)",
                "position_cats": 300. ,
                "list_cats" : ["ttH_2lss_3j_2018_mm_neg"],
                "list_cats_original" : ["ttH_2lss_3j_2018_mm_neg"],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "ttH_2lss_3j_mm_pos" : {
                "minY" : 0.,    "maxY" :  50.,
                "minYerr": -1.02, "maxYerr" : 1.32,
                "useLogPlot" : False,
                "label" : " #mu#mu ++",
                "labelX" : "mass(ll) (GeV)",
                "position_cats": 300. ,
                "list_cats" : ["ttH_2lss_3j_2018_mm_pos"],
                "list_cats_original" : ["ttH_2lss_3j_2018_mm_pos"],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "2l_2tau"   : {
                "minY" : 0.0,
                "maxY" :  6.5,
                "minYerr":  -1.1,  "maxYerr" : 1.4,
                "useLogPlot" : False,
                "label" : '2l + 2#tau_{h}',
                "position_cats": 300. ,
                "list_cats" : ["ttH_2l_2tau_2018"],
                "list_cats_original" : ["ttH_2l_2tau"],
                "labelX" : "Bin number",
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "3l_1tau"   : {
                "minY" : 0.,  "maxY" :  8.0,
                "minYerr":  -1.1,  "maxYerr" : 1.84,
                "useLogPlot" : False,
                "label" : '3l + 1#tau_{h}',
                "labelX" : "Bin number",
                "position_cats": 300. ,
                "list_cats" : ["ttH_3l_1tau_2018"],
                "list_cats_original" : ["ttH_3l_1tau"],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "1l_2tau"   : {
                "minY" : 0,  "maxY" :  55.,
                "minYerr":  -1.24,  "maxYerr" : 1.64,
                "useLogPlot" : False,
                "label" : '1l + 2#tau_{h}',
                "position_cats": 300. ,
                "list_cats" : ["ttH_1l_2tau_2018"],
                "list_cats_original" : ["ttH_1l_2tau"],
                "labelX" : "BDT output",
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "1l_2tau_SS"   : {
                "minY" : 0,  "maxY" :  55.,
                "minYerr":  -1.24,  "maxYerr" : 3.64,
                "useLogPlot" : False,
                "label" : '1l + 2#tau_{h} SS',
                "position_cats": 300. ,
                "list_cats" : ["ttH_1l_2tau_2018"],
                "list_cats_original" : ["ttH_1l_2tau"],
                "labelX" : "M(#tau #tau) Vis (GeV)", #   "m_{#tau_{h}#tau_{h}} (GeV)"
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "2los_1tau" : {
                "minY" : 0,  "maxY" :  85.,
                "minYerr":  -1.10,  "maxYerr" : 1.3,
                "useLogPlot" : False,
                "label" : '2l os + 1#tau_{h}',
                "position_cats": 300. ,
                "list_cats" : ["ttH_2los_1tau_2018"],
                "list_cats_original" : ["ttH_2los_1tau"],
                "labelX" : "BDT output",
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "0l_2tau"   : {
                "minY" : 0.1,  "maxY" :  1500000.,
                "minYerr": -1.01,  "maxYerr" : 1.7,
                "useLogPlot" : True,
                "label" : '0l + 2#tau_{h}',
                "labelX" : "BDT output",
                "position_cats": 300. ,
                "list_cats" : ["ttH_0l_2tau_2018"],
                "list_cats_original" : ["ttH_0l_2tau"],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "1l_1tau"   : {
                "minY" : 10,  "maxY" :  400000.,
                "minYerr":  -0.74,  "maxYerr" : 0.74,
                "useLogPlot" : True,
                "label" : '1l + 1#tau_{h}',
                "position_cats": 300. ,
                "list_cats" : ["ttH_1l_1tau_2018"],
                "list_cats_original" : ["ttH_1l_1tau"],
                "labelX" : "BDT output",
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "4l_0tau"   : {
                "minY" : 0.,
                "maxY" :  9.5,
                "minYerr":  -1.14,  "maxYerr" : 2.99,
                "useLogPlot" : False,
                "label" : '4l + 0#tau_{h}',
                "position_cats": 300. ,
                "list_cats" : ["ttH_4l_2018"],
                "list_cats_original" : ["ttH_4l_2018"],
                "labelX" : "Bin number",
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "2lss_0tau" : {
                "minY" : 0., "maxY" :  13.9,
                "minYerr":  -1.1,  "maxYerr" : 1.54,
                "useLogPlot" : False,
                "label" : '2l ss - 3j ',
                "labelX" : "BDT",
                "list_cats" : [],
                "list_cats_original" : [],
                "position_cats": 300. ,
                "cats" : [""],
                "catsX" :  [0.0]
                },
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
        "2lss_0tau" : {
            "bkg_proc_from_data" : [ fakes, "mcFlips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : ["ttH", "tHq", "tHW", "ZH", "WH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_0tau_NN" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : ["ttH", "tHq", "tHW", "VH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_3j": {
            "bkg_proc_from_data" : [ fakes, "data_flips"], #
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : [ "ttH", "tHq", "tHW", "ggH", "qqH", "ZH", "WH" , "HH", "TTWH", "TTZH" ],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        ####
        "ttH_2lss_3j_ee": {
            "bkg_proc_from_data" : [ fakes, "data_flips"], #
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : [ "ttH", "tHq", "tHW", "ggH", "qqH", "ZH", "WH" , "HH", "TTWH", "TTZH" ],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "ttH_2lss_3j_em_neg": {
            "bkg_proc_from_data" : [ fakes, "data_flips"], #
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : [ "ttH", "tHq", "tHW", "ggH", "qqH", "ZH", "WH" , "HH", "TTWH", "TTZH" ],
            "leading_minor_H" : "ZH_hww" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "ttH_2lss_3j_em_pos": {
            "bkg_proc_from_data" : [ fakes, "data_flips"], #
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : [ "ttH", "tHq", "tHW", "ggH", "qqH", "ZH", "WH" , "HH", "TTWH", "TTZH" ],
            "leading_minor_H" : "ZH_hww" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "ttH_2lss_3j_mm_neg": {
            "bkg_proc_from_data" : [ fakes, "data_flips"], #
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : [ "ttH", "tHq", "tHW", "ggH", "qqH", "ZH", "WH" , "HH", "TTWH", "TTZH" ],
            "leading_minor_H" : "ZH_hww" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "ttH_2lss_3j_mm_pos": {
            "bkg_proc_from_data" : [ fakes, "data_flips"], #
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : [ "ttH", "tHq", "tHW", "ggH", "qqH", "ZH", "WH" , "HH", "TTWH", "TTZH" ],
            "leading_minor_H" : "WH_hww" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_0tau_tH" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : ["ttH", "tHq", "tHW", "ZH", "WH", "ggH", "qqH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "WH_hww" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_0tau_ttH" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : ["ttH", "tHq", "tHW", ], # too low to appear in plot: "ZH", "WH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_0tau_ttW" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : ["ttH", "tHq", "tHW"], # too low to appear in plot: "ZH", "WH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"
            "leading_minor_H" : "WH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_0tau_rest" : {
            "bkg_proc_from_data" : [ fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", "Convs"],
            "signal" : ["ttH", "tHq", "tHW", "ZH", "WH", "ggH", "qqH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "WH_hww" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_1tau_plain" : {
            "bkg_proc_from_data" : [fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW",  "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "qqH", "ggH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_1tau_nno_miss" : {
            "bkg_proc_from_data" : [fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW",  "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_1tau" : {
            "bkg_proc_from_data" : [fakes, "data_flips"],
            "bkg_procs_from_MC"  : ["TTW",  "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "HH", "ggH", "qqH", "TTWH", "TTZH"],
            "leading_minor_H" : "ZH_hww" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2lss_1tau_NN" : {
            "bkg_proc_from_data" : [fakes, flips],
            "bkg_procs_from_MC"  : ["TTW",  "TTZ", "WZ", "ZZ", "Rares", conversions, "TT", "TTWH", "TTZH", "HH",],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH"], # , "TTWH", "TTZH"
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "3l_0tau"   : {
            "bkg_proc_from_data" : [fakes, flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "tHq", "tHW", "VH"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "3lctrl"   : {
            "bkg_proc_from_data" : [fakes, flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions],
            "signal" : ["ttH", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "4lctrl"   : {
            "bkg_proc_from_data" : ["data_fakes", flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTZ", "WZ", "ZZ", "Rares", conversions],
            "signal" : ["ttH", ],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "3l_0tau_NN"   : {
            "bkg_proc_from_data" : [fakes,  flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "3l_0tau_ttH"   : {
            "bkg_proc_from_data" : [fakes,  flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "3l_0tau_tH"   : {
            "bkg_proc_from_data" : [fakes,  flips ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "3l_0tau_rest"   : {
            "bkg_proc_from_data" : ["data_fakes" ], # ,  flips
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ",  "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "1l_2tau"   : {
            "bkg_proc_from_data" : [ "data_fakes"      ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW"], # Too small to matter: "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "1l_2tau_SS"   : {
            "bkg_proc_from_data" : [ "data_fakes"      ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2l_2tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "qqH", "ggH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "3l_1tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "TT", "Rares", conversions],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "2los_1tau" : {
            "bkg_proc_from_data" : [fakes, flips],
            "bkg_procs_from_MC"  : ["TTW",  "TTZ", "WZ", "ZZ", "Rares", conversions, "TT"],
            "signal" : ["ttH", "tHq", "tHW"], # Too small to matter: "WH", "ZH", "ggH", "qqH", "HH", "TTWH", "TTZH"
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
        "0l_2tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : [ "TTZ", "WZ", "ZZ", "DY", "Rares", "TT", "TTWW" ,"TTW",],
            "signal" : ["ttH", "tHq", "tHW",  "ggH", "qqH", "HH", "TTWH", "TTZH"    "WH",  "ZH",],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "1l_1tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "DY", "Rares", "TT", conversions, "EWK"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "WH", "ZH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        "4l_0tau"   : {
            "bkg_proc_from_data" : [fakes       ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "WZ", "ZZ", "DY", "Rares", "TT", conversions, "EWK"],
            "signal" : ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH", "VH", "HH", "TTWH", "TTZH"],
            "leading_minor_H" : "ggH_htt" ## The legend for the mino H proc will only appear if this process is in the card
            },
        }
    else : sys.exit("analysis " + analysis + " not implemented")
    return info_channel
