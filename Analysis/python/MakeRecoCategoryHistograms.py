# Python Code for Histograming events based on their
# RECO values.  Splits signal events between the different
# channels and our different categories.
# 
# Example execution from command line:

#  python MakeRecoCategoryHistograms.py /afs/cern.ch/work/c/cranelli/public/WGamGam/ReFilterFinalNtuple/LepGammaGammaFinalElandMuUnblindAll_2015_6_9_ScaleFactors/job_LNuAA_LM_Reweight/Job_0000/tree.root ../test/Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_6_9_ScaleFactors/LM0123_Reweight/Reweighted_RecoCategoryHistograms.root



import sys

from ROOT import TFile
from ROOT import TTree
from ROOT import vector

#import particleIdentification
#import objectCuts
#import eventCuts
#import parentCuts

import histogramBuilder

# Define Root Files and Tree Locations and Names 

SM_WEIGHT_INDEX=0

#inFileDir="../test/"
TREE_LOC="ggNtuplizer/EventTree"


def MakeRecoCategoryHistograms(inFileLoc="ggTree_mc_ISR.root", outFileLoc="test.root"):

    # In File, Out File, and Tree
    inFile = TFile(inFileLoc)
    tree = inFile.Get(TREE_LOC)
    outFile = TFile(outFileLoc, "RECREATE")
    
    nentries = tree.GetEntries()
    print "Number of Entries", nentries
    
    for i in range(0, nentries):
        if(i%1000==0): print i
        tree.GetEntry(i)

        #Assign aQGC Weights
        aqgc_weights = tree.LHEWeight_weights
        sm_weight = aqgc_weights[SM_WEIGHT_INDEX]

        for aqgc_weight_index in range(0,aqgc_weights.size()):
            aqgc_weight = aqgc_weights[aqgc_weight_index]
            #(Using Scale Factors)

            scalefactor =1;
            isElectronChannel=(tree.el_passtrig_n> 0 and tree.el_n==1 and tree.mu_n==0)
            isMuonChannel=(tree.mu_passtrig25_n>0 and tree.mu_n==1 and tree.el_n==0)
        
            if(isElectronChannel):
                channel="ElectronChannel"
                scalefactor = tree.el_trigSF*tree.ph_idSF*tree.ph_evetoSF*tree.PUWeight
                MakeHistograms(tree, channel, aqgc_weight_index, aqgc_weight, sm_weight)
            if(isMuonChannel):
                channel="MuonChannel"
                scalefactor = tree.mu_trigSF*tree.mu_isoSF*tree.mu_idSF*tree.ph_idSF*tree.PUWeight
                MakeHistograms(tree, channel, aqgc_weight_index, aqgc_weight, sm_weight)
                # if(not isElectronChannel and not isMuonChannel):
            
    outFile.Write()

# Make Histograms weighted to the different aQGC coupling parameters.
def MakeHistograms(tree, channel, aqgc_weight_index, aqgc_weight, sm_weight):
    histogramBuilder.fillCountHistograms(channel+"_All_aQGC_Weight_"+str(aqgc_weight_index), aqgc_weight)
    histogramBuilder.fillPtHistograms(channel+"_All_aQGC_Weight_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight)
    histogramBuilder.fillPtCategoryHistograms(channel+"All_aQGC_Weight_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight)
    
    # Make Separate Histograms for EBEB, EB EE, and EE EB Cateogries
    MakePhotonLocationHistograms(tree, channel, aqgc_weight_index, aqgc_weight)

    #Make Reweighting Histograms
    #MakeReweightingHistograms(tree, channel, aqgc_weight_index, aqgc_weight, sm_weight)

    MakeCovarianceHistograms(tree, channel, aqgc_weight_index, aqgc_weight, sm_weight)

# Histogrmas the reweighting values, with respect to the SM.
def MakeReweightingHistograms(tree, channel, aqgc_weight_index, aqgc_weight, sm_weight):
    reweight = aqgc_weight/sm_weight

    if tree.pt_leadph12 > 200:
        histogramBuilder.fillAQGCReweightHistograms(channel+"PtGT200_"+str(aqgc_weight_index), reweight)
    
    if tree.pt_leadph12 > 70:
        histogramBuilder.fillAQGCReweightHistograms(channel+"PtGT70_"+str(aqgc_weight_index), reweight)

# Holds the weights of the sm_weight * the aqc_weight
def MakeCovarianceHistograms(tree, channel, aqgc_weight_index, aqgc_weight, sm_weight):
    histogramBuilder.fillPtCategoryHistograms(channel+"_All_aQGC_Covariance_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight*sm_weight)
    histogramBuilder.fillPtHistograms(channel+"_All_aQGC_Covariance_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight*sm_weight)

    if(tree.isEB_leadph12 and tree.isEB_sublph12):
        histogramBuilder.fillPtHistograms(channel+"_EBEB_aQGC_Covariance_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight*sm_weight)
    
    if(tree.isEB_leadph12 and tree.isEE_sublph12):
        histogramBuilder.fillPtHistograms(channel+"_EBEE_aQGC_Covariance_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight*sm_weight)
        histogramBuilder.fillPtHistograms(channel+"_EBEEandEEEB_aQGC_Covariance_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight*sm_weight)

    if(tree.isEE_leadph12 and tree.isEB_sublph12):
        histogramBuilder.fillPtHistograms(channel+"_EEEB_aQGC_Covariance_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight*sm_weight)
        histogramBuilder.fillPtHistograms(channel+"_EBEEandEEEB_aQGC_Covariance_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight*sm_weight)


def MakePhotonLocationHistograms(tree, channel, aqgc_weight_index, aqgc_weight):
    if(tree.isEB_leadph12 and tree.isEB_sublph12):
        histogramBuilder.fillPtHistograms(channel+"_EBEB_aQGC_Weight_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight)
    if(tree.isEB_leadph12 and tree.isEE_sublph12):
         histogramBuilder.fillPtHistograms(channel+"_EBEE_aQGC_Weight_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight)
         histogramBuilder.fillPtHistograms(channel+"_EBEEandEEEB_aQGC_Weight_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight)
    if(tree.isEE_leadph12 and tree.isEB_sublph12):
        histogramBuilder.fillPtHistograms(channel+"_EEEB_aQGC_Weight_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight)
        histogramBuilder.fillPtHistograms(channel+"_EBEEandEEEB_aQGC_Weight_"+str(aqgc_weight_index), tree.pt_leadph12, aqgc_weight)
    

#Separate Lead and Sub Lead Photons between Barrel and EndCap.
# 0 is EBEB, 1 EBEE, 2 EEEB, 3 is all others
def findPhotonLocations(tree):
    #Both in Barrel
    if(tree.isEB_leadph12 and tree.isEB_sublph12):
        return 0
    #Lead in Barrel Sub in EndCap
    if(tree.isEB_leadph12 and tree.isEE_sublph12):
        return 1
    #Lead in EndCap Sub in Barrel
    if(tree.isEE_leadph12 and tree.isEB_sublph12):
        return 2
    #Both in EndCap
    if(tree.isEE_leadph12 and tree.isEE_sublph12):
        return 3
    

if __name__=="__main__":
        MakeRecoCategoryHistograms(sys.argv[1], sys.argv[2])
    
