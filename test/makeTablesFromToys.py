#!/usr/bin/env python 
import sys, os, re
import numpy as np
import ROOT  as r
import pickle
from tabulate import tabulate

from optparse import OptionParser
parser = OptionParser()

processes = {
    'Fakes' : ['data_fakes', 'fakes_mc'],
    'Flips' : ['data_flips'],
    'Conv'  : ['Conv'],
    'TT+jets' : ['TT'],
    'Rares' : ['Rares'],
    'ZZ'    : ['ZZ'],
    'WZ'    : ['WZ'],
    'TTW TTWW' : ['TTW','TTWW'],
    'Other Higgs'    : ['HH', 'VH', 'TTWH',"TTWH", "TTZH", "qqH", "VH", "WH", "ZH", "ggH"],
    'tHW' : ['tHW'],
    'tHq' : ['tHq'],
    'ttH' : ['ttH'],
    'ttZ' : ['TTZ'],
    
}
signals='ttH,tHW,tHq'.split(',')

regionMapping = { 
    '0l 2tau'   : ['ttH_0l_2tau_2016','ttH_0l_2tau_2017','ttH_0l_2tau_2018'],
    '1l 1tau'   : ['ttH_1l_1tau_2016','ttH_1l_1tau_2017','ttH_1l_1tau_2018'],
    '1l 2tau'   : ['ttH_1l_2tau_2016','ttH_1l_2tau_2017','ttH_1l_2tau_2018'],
    '2l 2tau'   : ['ttH_2l_2tau_2016','ttH_2l_2tau_2017','ttH_2l_2tau_2018'],
    '2los 1tau' : ['ttH_2los_1tau_2016','ttH_2los_1tau_2017','ttH_2los_1tau_2018'],
    '3l 1tau'   : ['ttH_3l_1tau_2016','ttH_3l_1tau_2017','ttH_3l_1tau_2018'],
    '4l'        : ['ttH_4l_2017','ttH_4l_2016','ttH_4l_2018'],
    'cr 4l'     : ['ttH_cr_4l_2016','ttH_cr_4l_2017','ttH_cr_4l_2018'],
    'cr 3l'     : ['ttH_cr_3l_2016_eee_cr','ttH_cr_3l_2016_eem_cr','ttH_cr_3l_2016_emm_cr','ttH_cr_3l_2016_mmm_cr','ttH_cr_3l_2017_eee_cr','ttH_cr_3l_2017_eem_cr','ttH_cr_3l_2017_emm_cr','ttH_cr_3l_2017_mmm_cr','ttH_cr_3l_2018_eee_cr','ttH_cr_3l_2018_eem_cr','ttH_cr_3l_2018_emm_cr','ttH_cr_3l_2018_mmm_cr'],
    
    # separated regions for AN
    '3l 0tau rest' : ['ttH_3l_0tau_rest_eem_bl_2016','ttH_3l_0tau_rest_eem_bl_2017','ttH_3l_0tau_rest_eem_bl_2018','ttH_3l_0tau_rest_emm_bl_2016','ttH_3l_0tau_rest_emm_bl_2017','ttH_3l_0tau_rest_emm_bl_2018','ttH_3l_0tau_rest_mmm_bl_2016','ttH_3l_0tau_rest_mmm_bl_2018','ttH_3l_0tau_rest_eee_2016','ttH_3l_0tau_rest_eee_2017','ttH_3l_0tau_rest_eee_2018','ttH_3l_0tau_rest_eem_bt_2016','ttH_3l_0tau_rest_eem_bt_2017','ttH_3l_0tau_rest_eem_bt_2018','ttH_3l_0tau_rest_emm_bt_2016','ttH_3l_0tau_rest_emm_bt_2017','ttH_3l_0tau_rest_emm_bt_2018','ttH_3l_0tau_rest_mmm_bl_2017','ttH_3l_0tau_rest_mmm_bt_2016','ttH_3l_0tau_rest_mmm_bt_2017','ttH_3l_0tau_rest_mmm_bt_2018'],
    'ttH 3l 0tau_tH' : ['ttH_3l_0tau_tH_bl_2016','ttH_3l_0tau_tH_bl_2017','ttH_3l_0tau_tH_bl_2018','ttH_3l_0tau_tH_bt_2016','ttH_3l_0tau_tH_bt_2017','ttH_3l_0tau_tH_bt_2018'],
    'ttH 3l 0tau_ttH': ['ttH_3l_0tau_ttH_bl_2018','ttH_3l_0tau_ttH_bt_2016','ttH_3l_0tau_ttH_bt_2017','ttH_3l_0tau_ttH_bt_2018','ttH_3l_0tau_ttH_bl_2016','ttH_3l_0tau_ttH_bl_2017'],

    '2lss 0tau Rest'   : ['ttH_2lss_0tau_mm_Restnode_2016','ttH_2lss_0tau_ee_Restnode_2016','ttH_2lss_0tau_ee_Restnode_2017','ttH_2lss_0tau_ee_Restnode_2018','ttH_2lss_0tau_em_Restnode_2016','ttH_2lss_0tau_em_Restnode_2017','ttH_2lss_0tau_em_Restnode_2018','ttH_2lss_0tau_mm_Restnode_2017','ttH_2lss_0tau_mm_Restnode_2018'],
    '2lss 0tau tHQnode': ['ttH_2lss_0tau_mm_tHQnode_2016','ttH_2lss_0tau_ee_tHQnode_2016','ttH_2lss_0tau_ee_tHQnode_2017','ttH_2lss_0tau_ee_tHQnode_2018','ttH_2lss_0tau_em_tHQnode_2016','ttH_2lss_0tau_em_tHQnode_2017','ttH_2lss_0tau_em_tHQnode_2018','ttH_2lss_0tau_mm_tHQnode_2017','ttH_2lss_0tau_mm_tHQnode_2018'],
    '2lss 0tau ttWnode': ['ttH_2lss_0tau_mm_ttWnode_2016','ttH_2lss_0tau_mm_ttWnode_2018','ttH_2lss_0tau_ee_ttWnode_2016','ttH_2lss_0tau_ee_ttWnode_2017','ttH_2lss_0tau_ee_ttWnode_2018','ttH_2lss_0tau_em_ttWnode_2016','ttH_2lss_0tau_em_ttWnode_2017','ttH_2lss_0tau_em_ttWnode_2018','ttH_2lss_0tau_mm_ttWnode_2017'],
    '2lss 0tau ttHnode': ['ttH_2lss_0tau_mm_ttHnode_2016','ttH_2lss_0tau_mm_ttHnode_2018','ttH_2lss_0tau_ee_ttHnode_2016','ttH_2lss_0tau_ee_ttHnode_2017','ttH_2lss_0tau_ee_ttHnode_2018','ttH_2lss_0tau_em_ttHnode_2016','ttH_2lss_0tau_em_ttHnode_2017','ttH_2lss_0tau_em_ttHnode_2018','ttH_2lss_0tau_mm_ttHnode_2017'],

    '2lss 1tau rest'  : ['ttH_2lss_1tau_rest_2016','ttH_2lss_1tau_rest_2017','ttH_2lss_1tau_rest_2018'],
    '2lss 1tau tH'    : ['ttH_2lss_1tau_tH_2016','ttH_2lss_1tau_tH_2017','ttH_2lss_1tau_tH_2018'],
    '2lss 1tau ttH'   : ['ttH_2lss_1tau_ttH_2016','ttH_2lss_1tau_ttH_2017','ttH_2lss_1tau_ttH_2018'],

    # merged regions for paper
    '2lss 0tau'   : ['ttH_2lss_0tau_mm_Restnode_2016','ttH_2lss_0tau_ee_Restnode_2016','ttH_2lss_0tau_ee_Restnode_2017','ttH_2lss_0tau_ee_Restnode_2018','ttH_2lss_0tau_em_Restnode_2016','ttH_2lss_0tau_em_Restnode_2017','ttH_2lss_0tau_em_Restnode_2018','ttH_2lss_0tau_mm_Restnode_2017','ttH_2lss_0tau_mm_Restnode_2018', 'ttH_2lss_0tau_mm_tHQnode_2016','ttH_2lss_0tau_ee_tHQnode_2016','ttH_2lss_0tau_ee_tHQnode_2017','ttH_2lss_0tau_ee_tHQnode_2018','ttH_2lss_0tau_em_tHQnode_2016','ttH_2lss_0tau_em_tHQnode_2017','ttH_2lss_0tau_em_tHQnode_2018','ttH_2lss_0tau_mm_tHQnode_2017','ttH_2lss_0tau_mm_tHQnode_2018','ttH_2lss_0tau_mm_ttWnode_2016','ttH_2lss_0tau_mm_ttWnode_2018','ttH_2lss_0tau_ee_ttWnode_2016','ttH_2lss_0tau_ee_ttWnode_2017','ttH_2lss_0tau_ee_ttWnode_2018','ttH_2lss_0tau_em_ttWnode_2016','ttH_2lss_0tau_em_ttWnode_2017','ttH_2lss_0tau_em_ttWnode_2018','ttH_2lss_0tau_mm_ttWnode_2017','ttH_2lss_0tau_mm_ttHnode_2016','ttH_2lss_0tau_mm_ttHnode_2018','ttH_2lss_0tau_ee_ttHnode_2016','ttH_2lss_0tau_ee_ttHnode_2017','ttH_2lss_0tau_ee_ttHnode_2018','ttH_2lss_0tau_em_ttHnode_2016','ttH_2lss_0tau_em_ttHnode_2017','ttH_2lss_0tau_em_ttHnode_2018','ttH_2lss_0tau_mm_ttHnode_2017'],
    '3l 0tau'     : ['ttH_3l_0tau_rest_eem_bl_2016','ttH_3l_0tau_rest_eem_bl_2017','ttH_3l_0tau_rest_eem_bl_2018','ttH_3l_0tau_rest_emm_bl_2016','ttH_3l_0tau_rest_emm_bl_2017','ttH_3l_0tau_rest_emm_bl_2018','ttH_3l_0tau_rest_mmm_bl_2016','ttH_3l_0tau_rest_mmm_bl_2018','ttH_3l_0tau_rest_eee_2016','ttH_3l_0tau_rest_eee_2017','ttH_3l_0tau_rest_eee_2018','ttH_3l_0tau_rest_eem_bt_2016','ttH_3l_0tau_rest_eem_bt_2017','ttH_3l_0tau_rest_eem_bt_2018','ttH_3l_0tau_rest_emm_bt_2016','ttH_3l_0tau_rest_emm_bt_2017','ttH_3l_0tau_rest_emm_bt_2018','ttH_3l_0tau_rest_mmm_bl_2017','ttH_3l_0tau_rest_mmm_bt_2016','ttH_3l_0tau_rest_mmm_bt_2017','ttH_3l_0tau_rest_mmm_bt_2018', 'ttH_3l_0tau_tH_bl_2016','ttH_3l_0tau_tH_bl_2017','ttH_3l_0tau_tH_bl_2018','ttH_3l_0tau_tH_bt_2016','ttH_3l_0tau_tH_bt_2017','ttH_3l_0tau_tH_bt_2018','ttH_3l_0tau_ttH_bl_2018','ttH_3l_0tau_ttH_bt_2016','ttH_3l_0tau_ttH_bt_2017','ttH_3l_0tau_ttH_bt_2018','ttH_3l_0tau_ttH_bl_2016','ttH_3l_0tau_ttH_bl_2017'],
    '2lss 1tau' : ['ttH_2lss_1tau_rest_2016','ttH_2lss_1tau_rest_2017','ttH_2lss_1tau_rest_2018','ttH_2lss_1tau_tH_2016','ttH_2lss_1tau_tH_2017','ttH_2lss_1tau_tH_2018','ttH_2lss_1tau_ttH_2016','ttH_2lss_1tau_ttH_2017','ttH_2lss_1tau_ttH_2018'],

}
procswithdecays=['ttH','VH', 'TTWH',"TTWH", "TTZH", "qqH", "VH", "WH", "ZH", "ggH",'tHq','tHW']



results = {} 
data = {}

def readNominalAndToys(nominalFile, toyexp, fit='fit_s'):
    tf = r.TFile.Open(nominalFile)
    cats=[key.GetName() for key in tf.Get('shapes_%s'%fit).GetListOfKeys()]
    for proc in processes: 
        results[proc]={}
        results[proc]['nom']={}
        for cat in cats:
            results[proc]['nom'][cat]=None
            for comp in processes[proc]:
                for compwithdecay in ([comp] if comp not in procswithdecays else ['%s_%s'%(comp,x) for x in ["hww", "hzz", "htt"]]):
                    hist = tf.Get('shapes_%s/%s/%s'%(fit,cat,compwithdecay))
                    if not hist: continue
                    thehist=hist.Clone('shapes_%s_%s_%s'%(fit,cat,compwithdecay)); thehist.SetDirectory(None)
                    if not results[proc]['nom'][cat]: 
                        results[proc]['nom'][cat]=thehist
                    else: 
                        results[proc]['nom'][cat].Add(thehist)
        
        for toy in range(200): 
            results[proc]['toy_%d'%toy]={}
            for cat in cats:
                results[proc]['toy_%d'%toy][cat]=None

    # also take the chance to read data
    for cat in cats:
        data_obs=tf.Get('shapes_%s/%s/data'%(fit,cat))
        # get the binning from another random process
        data_hist=None
        for proc in results:
            if results[proc]['nom'][cat]: 
                data_hist=results[proc]['nom'][cat].Clone('data_%s_%s'%(fit,cat))
                data_hist.Reset()
                break
        if not data_hist:
            raise RuntimeError("tried to get that with a category with no process...")
        bin=1
        for y in data_obs.GetY():
            data_hist.SetBinContent(bin, y)
            bin=bin+1
        data[cat]=data_hist
            
    pickle.dump( data, open('data.p','w'))

    tf.Close()

    for toy in range(200): 
        print 'reading toy %d'%toy
        tftoy=r.TFile.Open(toyexp.format(toy=toy,fit=fit))
        for proc in processes: 
            for cat in cats:
                for comp in processes[proc]:
                    for compwithdecay in ([comp] if comp not in procswithdecays else ['%s_%s'%(comp,x) for x in ["hww", "hzz", "htt"]]):
                        hist = tftoy.Get('n_exp_final_bin%s_proc_%s'%(cat,compwithdecay))
                        if not hist: 
                            hist = tftoy.Get('n_exp_bin%s_proc_%s'%(cat,compwithdecay))
                            if not hist:
                                continue
                        thehist=hist.Clone('shapes_%s_%s_%s_toy%s'%(fit,cat,compwithdecay,toy)); thehist.SetDirectory(None)
                        if not results[proc]['toy_%d'%toy][cat]: 
                            results[proc]['toy_%d'%toy][cat]=thehist
                        else: 
                            results[proc]['toy_%d'%toy][cat].Add(thehist)
        tftoy.Close()

    results['total_signal']={}
    results['total background']={}
    for what in ['nom']+['toy_%d'%toy for toy in range(200)]:
        results['total_signal'][what]={}
        results['total background'][what]={}
    
    # build total sums now
    for cat in cats:
        for what in ['nom']+['toy_%d'%toy for toy in range(200)]:
            results['total_signal'][what][cat]=None
            results['total background'][what][cat]=None
            for proc in processes:
                if proc in signals: 
                    group='total_signal'
                else: 
                    group='total background'
                if not results[group][what][cat]:
                    if results[proc][what][cat]:
                        results[group][what][cat] = results[proc][what][cat].Clone('shapes_%s_%s_%s'%(group, what,cat))
                else:
                    if results[proc][what][cat]:
                        results[group][what][cat].Add( results[proc][what][cat] )

    pickle.dump( results, open('save.p','w'))



def stackByMapping():
    for cat in regionMapping: 
        for proc in [x for x in processes] + ['total_signal','total background']:
            for what in ['nom']+['toy_%d'%toy for toy in range(200)]:
                results[proc][what][cat]=None
                for year in regionMapping[cat]:
                    if not results[proc][what][year]: 
                        continue
                    if not results[proc][what][cat]: 
                        results[proc][what][cat] = results[proc][what][year].Clone('%s_%s_%s'%(proc, what,cat))
                    else: 
                        results[proc][what][cat].Add(results[proc][what][year])
        data[cat]=None
        for year in regionMapping[cat]:
            if not data[cat]:
                data[cat]=data[year].Clone('data_%s'%cat)
            else: 
                data[cat].Add(data[year].Clone('data_%s'%cat))
    
    # cleanup the dict now
    for cat in regionMapping: 
        for proc in [x for x in processes] +['total_signal','total background']: 
            for year in regionMapping[cat]:
                for what in ['nom']+['toy_%d'%toy for toy in range(200)]:
                    if year in results[proc][what]: del results[proc][what][year]
                if year in data: 
                    del data[year]
    pickle.dump( results, open('save_2.p','w') )
    pickle.dump( data, open('data_2.p','w') )

def tableToNumbers():

    for cat in regionMapping: 
        for proc in [x for x in processes] +['total_signal','total background']: 
            for what in ['nom']+['toy_%d'%toy for toy in range(200)]:
                if results[proc][what][cat]: 
                    results[proc][what][cat] = results[proc][what][cat].Integral()
        data[cat]=data[cat].Integral()

def buildRms():
    for proc in [x for x in processes]+['total_signal','total background']: 
        results[proc]['up']={}; results[proc]['dn']={}
        for cat in regionMapping: 
            toyvalues = []
            for what in ['toy_%d'%toy for toy in range(200)]:
                if results[proc][what][cat]: 
                    toyvalues.append( results[proc][what][cat] ) 
            if len(toyvalues) not in [0,200]:
                raise RuntimeError("Theres something wrong")
            if not len(toyvalues) and results[proc]['nom'][cat]:
                # theres nominal but not variations...
                print proc, cat, results[proc]['nom'][cat]
                raise RuntimeError("Theres something wrong")
            if len(toyvalues)==200:
                dn = np.percentile(np.array(toyvalues), 16)
                up = np.percentile(np.array(toyvalues), 84)
                #print dn, results[proc]['nom'][cat], up
                if results[proc]['nom'][cat] < dn:
                    results[proc]['up'][cat]=(up-results[proc]['nom'][cat])/2
                    results[proc]['dn'][cat]=results[proc]['up'][cat]
                    print 'warning, this shouldnt happen many times', proc, cat, results[proc]['nom'][cat], dn, up
                elif results[proc]['nom'][cat] > up:
                    results[proc]['up'][cat]=(results[proc]['nom'][cat]-dn)/2
                    results[proc]['dn'][cat]=results[proc]['up'][cat]
                    print 'warning, this shouldnt happen many times', proc, cat, results[proc]['nom'][cat], dn, up
                else:
                    results[proc]['up'][cat]=up-results[proc]['nom'][cat]
                    results[proc]['dn'][cat]=results[proc]['nom'][cat]-dn
            for what in ['toy_%d'%toy for toy in range(200)]:
                del results[proc][what][cat]

def makeTable(regions, vetoProcesses=[]):
    header=['Process']
    for cat in regions:
        header.append(cat)
    table=[header]

    for proc in [x for x in processes] +['total background']:  # 'total_signal',
        line=[proc]
        for cat in regions: 
            nom=results[proc]['nom'][cat]
            if nom and nom >0.1:
                up=results[proc]['up'][cat]
                dn=results[proc]['dn'][cat]
                line.append('$%4.1f^{+%4.1f}_{-%4.1f}$'%(nom, up,dn))
            else:
                line.append('$<$0.1')
        table.append(line)
    line=['Data']
    for cat in regions: 
        line.append('%d'%data[cat])
    table.append(line)
    print tabulate(table, tablefmt='latex_raw')
        


#step1 
readNominalAndToys('/nfs/fanae/user/sscruz/Combine/CMSSW_10_2_13/src/postfit_tests/fitDiagnostics_shapes_combine_combo_ttHmultilep_cminDefaultMinimizerStrategy0robustHesse_MINIMIZER_analytic_fixXtrg.root', '/nfs/fanae/user/sscruz/Combine/CMSSW_10_2_13/src/postfit_tests/toys/toys_{fit}{toy}.root')

#step2
results = pickle.load(open('save.p'))
data = pickle.load(open('data.p'))
stackByMapping()

#step3 
results = pickle.load(open('save_2.p'))
data = pickle.load(open('data_2.p'))
tableToNumbers()
buildRms()

makeTable(['ttH_0l_2tau',    'ttH_1l_1tau',    'ttH_1l_2tau',    'ttH_2l_2tau'  ,    'ttH_2los_1tau',    'ttH_3l_1tau'  ,    'ttH_2lss_1tau'])
makeTable(['ttH_2lss_0tau',    'ttH_3l_0tau'  ,    'ttH_4l'],vetoProcesses=['TT+jets'])
makeTable(['ttH_cr_4l',    'ttH_cr_3l'],vetoProcesses=['TT+jets'])


