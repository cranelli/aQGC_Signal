# Functions for Normalization 
# Python script created by Christopher Anelli, 5/6/2015
# Example Execution
# python Normalize.py

from ROOT import TH1F
from ROOT import TFile

import os



CHANNELS = ["MuonChannel", "ElectronChannel"]
#PHOTON_LOCATIONS=["All", "EBEB", "EBEE", "EEEB", "EBEEandEEEB"]

BASE= "/Users/Chris/WGamGam/aQGC_Signal/Analysis/test/Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_6_9_ScaleFactors/"
SAMPLES = ["LM0123_Reweight", "LT012_Reweight"]

WEIGHTED_ISR_FSR_FILE_NAME="/Users/Chris/CMS/WGamGam/Acceptances/Fiducial/test/Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_4_19_ScaleFactors_PDFReweights/WeightedTotal_RecoCategoryHistograms.root"


# Normalizing the expected Reconstructed aQGC (coupling = 0) samples 
# to the weighted ISR + FSR samples.
def Normalize():
    
    # Weighted Combination of ISR and FSR samples
    weighted_ISR_FSR_file = TFile(WEIGHTED_ISR_FSR_FILE_NAME, "READ")

    # aQGC samples
    for sample_name in SAMPLES:
    
        aQGC_file_name = BASE + sample_name + "/Reweighted_RecoCategoryHistograms.root"
        aQGC_file = TFile(aQGC_file_name, "READ")

        out_file_name =  os.path.splitext(aQGC_file_name)[0]+"_Normalized.root"
        print out_file_name
        out_file = TFile(out_file_name, "RECREATE")
        NormalizeAllHistograms(aQGC_file, weighted_ISR_FSR_file, out_file)

        out_file.Close()
        aQGC_file.Close()
    
    weighted_ISR_FSR_file.Close()

    
    

# Loop Over the channels and normalize the histograms
def NormalizeAllHistograms(aQGC_file, weighted_ISR_FSR_file, out_file):

    for channel in CHANNELS:        
        weighted_ISR_FSR_hist_name =channel+"_unweighted_Count"
        weighted_ISR_FSR_hist = weighted_ISR_FSR_file.Get(weighted_ISR_FSR_hist_name)

        # Coupling set to 0 (SM)
        aQGC_SM_hist_name = channel+"_All_aQGC_Weight_0_Count"
        aQGC_SM_hist = aQGC_file.Get(aQGC_SM_hist_name)

        scale = CalcScale(aQGC_SM_hist, weighted_ISR_FSR_hist)

        NormalizeHistogramsByChannel(channel, scale, aQGC_file, out_file)

        #normalized_aQGC_SM_hist = NormalizeFirstHistogramToSecond(aQGC_SM_hist, weighted_ISR_FSR_hist)
        #normalized_aQGC_SM_hist.Draw()
        

# Scale Histograms in a given channel, each channel has it's own scaling value.
def NormalizeHistogramsByChannel(channel, scale, in_file, out_file):
    
    list = in_file.GetListOfKeys()
    # Must be in the channel
    for key in list:
        histName = key.GetName()
        if channel in histName:
            hist = in_file.Get(histName)
            hist.Scale(scale)
            hist.Write()
            print "Scale ", hist.GetName(), "by ", scale
            
    #out_file.Close()

# Takes two histograms, and calculates the scale necessary to normalize the first
# to the second.
def CalcScale(h_first, h_second):
    print "Calculating Scale to change from", h_first.GetName(), "to ", h_second.GetName()
    nbins_first = h_first.GetNbinsX()
    # Include Overflow                                                                                                              
    total_events_first = h_first.Integral(0, nbins_first +1)

    nbins_second = h_second.GetNbinsX()
    total_events_second = h_second.Integral(0, nbins_second+1)

    scale = total_events_second / total_events_first
    print "Scale equals ", scale

    return scale


# Takes two histograms.  Scales the first so that it has the
# same number of total events as the second Histogram.  Then returns
# the scaled histogram.    
def NormalizeFirstHistogramToSecond(h_first, h_second):
    print "Normalizing ", h_first.GetName(), "to ", h_second.GetName()
    nbins_first = h_first.GetNbinsX()
    # Include Overflow
    total_events_first = h_first.Integral(0, nbins_first +1)    

    nbins_second = h_second.GetNbinsX()
    total_events_second = h_second.Integral(0, nbins_second+1)

    scale = total_events_second / total_events_first

    h_first.Scale(scale)
    print "Has been scaled by ", scale

    return h_first

if __name__=="__main__":
    Normalize()

    

