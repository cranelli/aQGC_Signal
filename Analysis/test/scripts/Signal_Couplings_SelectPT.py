from ROOT import TFile
from ROOT import TH1F
from ROOT import TGraph

from math import sqrt

from array import array

from ctypes import c_double

QGC_HISTOGRAM_DIRS=[("LM","../Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_5_3/LM0123_Reweight/"),
                ("LT", "../Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_5_3/LT012_Reweight/")]


CHANNELS = ["ElectronChannel", "MuonChannel"]


LAST_PT = 100 # 70+ Bin
#BACKGROUND_UNCERTAINTY = {'ElectronChannel':9.1, 'MuonChannel':10.5}



# Run over all the aQGC Classes, in this case the LT's and the LM's
def Signal_Couplings_AllCouplingClasses():
    for coupling_class, histogram_dir in QGC_HISTOGRAM_DIRS:
        in_file_name =  histogram_dir+"Reweighted_RecoCategoryHistograms_Normalized.root"
        out_file_name =histogram_dir+"Signal_Couplings_SelectPT.root"
        Signal_Couplings(in_file_name, out_file_name, coupling_class)

    
    
def Signal_Couplings(in_file_name, out_file_name, coupling_class):

    inFile = TFile(in_file_name, "READ")
    outFile = TFile(out_file_name, "RECREATE")

    # Separate Histogram for each Channel, Lead Photon Pt Bin, and Coupling Type"
    
    for channel in CHANNELS:
        # Matching Coupling Strength To Histograms.  Based on the Madgraph Reweight Card
        coupling_strengths_match_to_histnames = MakeCouplingStrengthHistNameContainer(channel, coupling_class)
        for coupling_type, strength_and_histnames in coupling_strengths_match_to_histnames:
            MakeHistsByCouplingType(coupling_type, channel, strength_and_histnames, inFile, outFile)


# For a specified coupling type, ie LM0, LM1, LM2, etc, makes a Signal vs Coupling histogram
def MakeHistsByCouplingType(coupling_type, channel, strength_and_histnames, inFile, outFile):
    print channel
    print "Coupling Type ", coupling_type

    # Histogram Range Depends on Coupling Type
    signalHist=TH1F()
    if coupling_type == "LM2" or coupling_type == "LM3":
        signalHist= TH1F("Signal_Function_Coupling", "Signal as a Function of Coupling Strength", 101, -1010, 1010)
    if coupling_type == "LT0" or coupling_type == "LT1" or coupling_type == "LT2":
        signalHist= TH1F("Signal_Function_Coupling", "Signal as a Function of Coupling Strength", 101, -101, 101)

    #Loop Over All coupling_strengths
    for coupling_strength, hist_name in strength_and_histnames:
        print "Coupling Strength", coupling_strength

        h1AQGC = inFile.Get(hist_name)
        bin_start = h1AQGC.FindBin(LAST_PT)
        bin_finish = h1AQGC.GetNbinsX() + 1 # Include Overflow Bin
        aqgc_error_ctype= c_double()
        aqgc_count = h1AQGC.IntegralAndError(bin_start, bin_finish, aqgc_error_ctype)
        aqgc_error = aqgc_error_ctype.value

        #h1AQGC.GetBinContent(ptbin)
        #aqgc_error = h1AQGC.GetBinError(ptbin)
        print "Expected aQGC Events ", aqgc_count, " pm ", aqgc_error
        
        # Fill Histogram
        bin_index=signalHist.FindBin(coupling_strength)
        signalHist.SetBinContent(bin_index, aqgc_count)
        signalHist.SetBinError(bin_index, aqgc_error)

    signalHist.Write(coupling_type+"_"+channel+"Pt"+str(LAST_PT)+"_SignalvsCoupling")


# Mapping between weight number and coupling value is defined in the MadGraph Reweight Card
def MakeCouplingStrengthHistNameContainer(channel, coupling_class):
    coupling_strength_histnames_container=[]
    
    if coupling_class == "LM":
        # LM2
        coupling_type = "LM2"
        strength_and_histnames = [
                                  ( -1000, channel+ "_aQGC_Weight_74_Pt"),
                                  ( -900, channel+ "_aQGC_Weight_73_Pt"),
                                  ( -800, channel+ "_aQGC_Weight_72_Pt"),
                                  ( -700, channel+ "_aQGC_Weight_71_Pt"),
                                  ( -600, channel+ "_aQGC_Weight_70_Pt"),
                                  ( -500, channel+ "_aQGC_Weight_69_Pt"),
                                  ( -400, channel+ "_aQGC_Weight_68_Pt"),
                                  ( -300, channel+ "_aQGC_Weight_67_Pt"),
                                  ( -200, channel+ "_aQGC_Weight_66_Pt"),
                                  ( -100, channel+ "_aQGC_Weight_65_Pt"),
                                  ( 0, channel+ "_aQGC_Weight_50_Pt"),
                                  ( 100, channel+ "_aQGC_Weight_53_Pt"),
                                  ( 200, channel+ "_aQGC_Weight_54_Pt"),
                                  ( 300, channel+ "_aQGC_Weight_55_Pt"),
                                  ( 400, channel+ "_aQGC_Weight_56_Pt"),
                                  ( 500, channel+ "_aQGC_Weight_57_Pt"),
                                  ( 600, channel+ "_aQGC_Weight_58_Pt"),
                                  ( 700, channel+ "_aQGC_Weight_59_Pt"),
                                  ( 800, channel+ "_aQGC_Weight_60_Pt"),
                                  ( 900, channel+ "_aQGC_Weight_61_Pt"),
                                  ( 1000, channel+ "_aQGC_Weight_62_Pt")
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
    
        # LM3
        coupling_type = "LM3"
        strength_and_histnames = [
                                  ( -1000, channel+ "_aQGC_Weight_99_Pt"),
                                  ( -900, channel+ "_aQGC_Weight_98_Pt"),
                                  ( -800, channel+ "_aQGC_Weight_97_Pt"),
                                  ( -700, channel+ "_aQGC_Weight_96_Pt"),
                                  ( -600, channel+ "_aQGC_Weight_95_Pt"),
                                  ( -500, channel+ "_aQGC_Weight_94_Pt"),
                                  ( -400, channel+ "_aQGC_Weight_93_Pt"),
                                  ( -300, channel+ "_aQGC_Weight_92_Pt"),
                                  ( -200, channel+ "_aQGC_Weight_91_Pt"),
                                  ( -100, channel+ "_aQGC_Weight_90_Pt"),
                                  ( 0, channel+ "_aQGC_Weight_75_Pt"),
                                  ( 100, channel+ "_aQGC_Weight_78_Pt"),
                                  ( 200, channel+ "_aQGC_Weight_79_Pt"),
                                  ( 300, channel+ "_aQGC_Weight_80_Pt"),
                                  ( 400, channel+ "_aQGC_Weight_81_Pt"),
                                  ( 500, channel+ "_aQGC_Weight_82_Pt"),
                                  ( 600, channel+ "_aQGC_Weight_83_Pt"),
                                  ( 700, channel+ "_aQGC_Weight_84_Pt"),
                                  ( 800, channel+ "_aQGC_Weight_85_Pt"),
                                  ( 900, channel+ "_aQGC_Weight_86_Pt"),
                                  ( 1000, channel+ "_aQGC_Weight_87_Pt"),
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
    
    if coupling_class == "LT":
        # LT0
        coupling_type = "LT0"
        strength_and_histnames = [
                                  ( -100, channel+ "_aQGC_Weight_24_Pt"),
                                  ( -90, channel+ "_aQGC_Weight_23_Pt"),
                                  ( -80, channel+ "_aQGC_Weight_22_Pt"),
                                  ( -70, channel+ "_aQGC_Weight_21_Pt"),
                                  ( -60, channel+ "_aQGC_Weight_20_Pt"),
                                  ( -50, channel+ "_aQGC_Weight_19_Pt"),
                                  ( -40, channel+ "_aQGC_Weight_18_Pt"),
                                  ( -30, channel+ "_aQGC_Weight_17_Pt"),
                                  ( -20, channel+ "_aQGC_Weight_16_Pt"),
                                  ( -10, channel+ "_aQGC_Weight_15_Pt"),
                                  ( 0, channel+ "_aQGC_Weight_0_Pt"),
                                  ( 10, channel+ "_aQGC_Weight_3_Pt"),
                                  ( 20, channel+ "_aQGC_Weight_4_Pt"),
                                  ( 30, channel+ "_aQGC_Weight_5_Pt"),
                                  ( 40, channel+ "_aQGC_Weight_6_Pt"),
                                  ( 50, channel+ "_aQGC_Weight_7_Pt"),
                                  ( 60, channel+ "_aQGC_Weight_8_Pt"),
                                  ( 70, channel+ "_aQGC_Weight_9_Pt"),
                                  ( 80, channel+ "_aQGC_Weight_10_Pt"),
                                  ( 90, channel+ "_aQGC_Weight_11_Pt"),
                                  ( 100, channel+ "_aQGC_Weight_12_Pt")
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
      
        # LT1
        coupling_type = "LT1"
        strength_and_histnames = [
                                  ( -100, channel+ "_aQGC_Weight_49_Pt"),
                                  ( -90, channel+ "_aQGC_Weight_48_Pt"),
                                  ( -80, channel+ "_aQGC_Weight_47_Pt"),
                                  ( -70, channel+ "_aQGC_Weight_46_Pt"),
                                  ( -60, channel+ "_aQGC_Weight_45_Pt"),
                                  ( -50, channel+ "_aQGC_Weight_44_Pt"),
                                  ( -40, channel+ "_aQGC_Weight_43_Pt"),
                                  ( -30, channel+ "_aQGC_Weight_42_Pt"),
                                  ( -20, channel+ "_aQGC_Weight_41_Pt"),
                                  ( -10, channel+ "_aQGC_Weight_40_Pt"),
                                  ( 0, channel+ "_aQGC_Weight_25_Pt"),
                                  ( 10, channel+ "_aQGC_Weight_28_Pt"),
                                  ( 20, channel+ "_aQGC_Weight_29_Pt"),
                                  ( 30, channel+ "_aQGC_Weight_30_Pt"),
                                  ( 40, channel+ "_aQGC_Weight_31_Pt"),
                                  ( 50, channel+ "_aQGC_Weight_32_Pt"),
                                  ( 60, channel+ "_aQGC_Weight_33_Pt"),
                                  ( 70, channel+ "_aQGC_Weight_34_Pt"),
                                  ( 80, channel+ "_aQGC_Weight_35_Pt"),
                                  ( 90, channel+ "_aQGC_Weight_36_Pt"),
                                  ( 100, channel+ "_aQGC_Weight_37_Pt")
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
        
        # LT2
        coupling_type = "LT2"
        strength_and_histnames = [
                                  ( -100, channel+ "_aQGC_Weight_74_Pt"),
                                  ( -90, channel+ "_aQGC_Weight_73_Pt"),
                                  ( -80, channel+ "_aQGC_Weight_72_Pt"),
                                  ( -70, channel+ "_aQGC_Weight_71_Pt"),
                                  ( -60, channel+ "_aQGC_Weight_70_Pt"),
                                  ( -50, channel+ "_aQGC_Weight_69_Pt"),
                                  ( -40, channel+ "_aQGC_Weight_68_Pt"),
                                  ( -30, channel+ "_aQGC_Weight_67_Pt"),
                                  ( -20, channel+ "_aQGC_Weight_66_Pt"),
                                  ( -10, channel+ "_aQGC_Weight_65_Pt"),
                                  ( 0, channel+ "_aQGC_Weight_50_Pt"),
                                  ( 10, channel+ "_aQGC_Weight_53_Pt"),
                                  ( 20, channel+ "_aQGC_Weight_54_Pt"),
                                  ( 30, channel+ "_aQGC_Weight_55_Pt"),
                                  ( 40, channel+ "_aQGC_Weight_56_Pt"),
                                  ( 50, channel+ "_aQGC_Weight_57_Pt"),
                                  ( 60, channel+ "_aQGC_Weight_58_Pt"),
                                  ( 70, channel+ "_aQGC_Weight_59_Pt"),
                                  ( 80, channel+ "_aQGC_Weight_60_Pt"),
                                  ( 90, channel+ "_aQGC_Weight_61_Pt"),
                                  ( 100, channel+ "_aQGC_Weight_62_Pt"),
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
    
    
    return coupling_strength_histnames_container


if __name__=="__main__":
    Signal_Couplings_AllCouplingClasses()
