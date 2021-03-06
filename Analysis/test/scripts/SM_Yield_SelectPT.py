# Calculates the expected SM Yield, for a final Pt bin.
# Uses weighted merger of the NLO ISR and FSR samples.
from ROOT import TFile
from ROOT import TH1F
from ROOT import TF1
from ROOT import TGraph

from math import sqrt

from array import array

from ctypes import c_double

#QGC_HISTOGRAM_DIRS=[("LM","../Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_6_9_ScaleFactors/LM0123_Reweight/"),
#                ("LT", "../Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_6_9_ScaleFactors/LT012_Reweight/")]

HISTOGRAM_DIR="../Histograms/"

CHANNELS = ["ElectronChannel", "MuonChannel"]
PHOTON_LOCATIONS = ["EBEB", "EBEE", "EEEB"]
SUBL_PHOTON_CUTS = ["25"]
#SUBL_PHOTON_CUTS = ["15", "20", "25", "30", "35", "40"]

LAST_PTS = [70] # 70+, 100+ etc
#LAST_PTS = [70, 80, 90, 100, 125, 150, 200] # 70+, 100+ etc
#BACKGROUND_UNCERTAINTY = {'ElectronChannel':9.1, 'MuonChannel':10.5}

# Run over all the aQGC Classes, in this case the LT's and the LM's
def SMYield_AllCouplingClasses():
    #for coupling_class, histogram_dir in QGC_HISTOGRAM_DIRS:
    in_file_name =  HISTOGRAM_DIR+"NLO_SM_WeightedTotal_RecoCategoryHistograms_2015_09_16.root"
    out_file_name =HISTOGRAM_DIR+"NLO_SM_Yield_SelectPT.root"
    SMYield(in_file_name, out_file_name)
        
def SMYield(in_file_name, out_file_name):

    inFile = TFile(in_file_name, "READ")
    outFile = TFile(out_file_name, "RECREATE")

    # Separate Histogram for each Channel, Lead Photon Pt Bin, and Coupling Type"
    
    for channel in CHANNELS:
        for photon_location in PHOTON_LOCATIONS:
            for subl_cut in SUBL_PHOTON_CUTS:
                for last_pt in LAST_PTS:
                    MakeHists(channel, subl_cut, photon_location, last_pt, inFile, outFile)

def MakeHists(channel, subl_cut, photon_location, last_pt, inFile, outFile):
    print channel, subl_cut, photon_location, last_pt 
    #print "Coupling Type ", coupling_type

    # Histogram Range Depends on Coupling Type
    smLastPtHist=TH1F()
    
    smLastPtHist = TH1F("SM_Signal_LastPT", "SM Signal Last pT", 1, last_pt, 400);
    smLastPtHist.GetXaxis().SetTitle("Lead Photon pT (GeV)")
    smLastPtHist.GetYaxis().SetTitle("SM Yield")

    # Get SM and Error
    smHistName=photon_location+ "_Sublph" +subl_cut +"_"+channel+ "_ScaleFactors_Pt"
    h1SM = inFile.Get(smHistName)
    bin_start = h1SM.FindBin(last_pt)
    bin_finish = h1SM.GetNbinsX() + 1 # Include Overflow Bin
    sm_error_ctype= c_double()
    sm_count = h1SM.IntegralAndError(bin_start, bin_finish, sm_error_ctype)
    sm_error = sm_error_ctype.value

    smLastPtHist.SetBinContent(1, sm_count)
    smLastPtHist.SetBinError(1, sm_error)
    smLastPtHist.Write(channel+"_"+photon_location+"_Pt"+str(last_pt)+"_"+subl_cut+"_SMYield")
    

if __name__=="__main__":
    SMYield_AllCouplingClasses()
