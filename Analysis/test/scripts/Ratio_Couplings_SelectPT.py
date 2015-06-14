from ROOT import TFile
from ROOT import TH1F
from ROOT import TF1
from ROOT import TGraph

from math import sqrt

from array import array

from ctypes import c_double

QGC_HISTOGRAM_DIRS=[("LM","../Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_5_3/LM0123_Reweight/"),
                ("LT", "../Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_5_3/LT012_Reweight/")]


CHANNELS = ["ElectronChannel", "MuonChannel"]


LAST_PTS = [70, 100, 110, 120,  125, 150, 175, 200] # 70+, 100+ etc
#BACKGROUND_UNCERTAINTY = {'ElectronChannel':9.1, 'MuonChannel':10.5}



# Run over all the aQGC Classes, in this case the LT's and the LM's
def Ratio_Couplings_AllCouplingClasses():
    for coupling_class, histogram_dir in QGC_HISTOGRAM_DIRS:
        in_file_name =  histogram_dir+"Reweighted_RecoCategoryHistograms.root"
        out_file_name =histogram_dir+"Ratio_Couplings_SelectPT.root"
        Ratio_Couplings(in_file_name, out_file_name, coupling_class)
        
def Ratio_Couplings(in_file_name, out_file_name, coupling_class):

    inFile = TFile(in_file_name, "READ")
    outFile = TFile(out_file_name, "RECREATE")

    # Separate Histogram for each Channel, Lead Photon Pt Bin, and Coupling Type"
    
    for channel in CHANNELS:
        # Matching Coupling Strength To Histograms.  Based on the Madgraph Reweight Card
        coupling_strengths_match_to_histnames = MakeCouplingStrengthHistNameContainer(channel, coupling_class)
        for coupling_type, strength_and_histnames in coupling_strengths_match_to_histnames:
            for last_pt in LAST_PTS:
                MakeHistsByCouplingType(coupling_type, channel, last_pt, strength_and_histnames, inFile, outFile)


# For a specified coupling type, ie LM0, LM1, LM2, etc, makes a Ratio vs Coupling histogram
def MakeHistsByCouplingType(coupling_type, channel, last_pt, strength_and_histnames, inFile, outFile):
    print channel
    print "Coupling Type ", coupling_type

    # Histogram Range Depends on Coupling Type
    ratioHist=TH1F()
    if coupling_type == "LM2" or coupling_type == "LM3":
        ratioHist= TH1F("Ratio_Function_Coupling", "Ratio as a Function of Coupling Strength", 101, -1010, 1010)
    if coupling_type == "LT0" or coupling_type == "LT1" or coupling_type == "LT2":
        ratioHist= TH1F("Ratio_Function_Coupling", "Ratio as a Function of Coupling Strength", 101, -101, 101)
    ratioHist.GetXaxis().SetTitle("Coupling Strength (TeV^{-4})")
    ratioHist.GetYaxis().SetTitle("aQGC to SM Yield")

    # Get SM and Error
    h1SM = inFile.Get(channel+ "_aQGC_Weight_0_Pt")
    bin_start = h1SM.FindBin(last_pt)
    bin_finish = h1SM.GetNbinsX() + 1 # Include Overflow Bin
    sm_error_ctype= c_double()
    sm_count = h1SM.IntegralAndError(bin_start, bin_finish, sm_error_ctype)
    sm_error = sm_error_ctype.value

    #Loop Over All coupling_strengths
    for coupling_strength, hist_name, covariance_hist_name in strength_and_histnames:
        print "Coupling Strength", coupling_strength

        h1AQGC = inFile.Get(hist_name)
        #bin_start = h1AQGC.FindBin(last_pt)
        #bin_finish = h1AQGC.GetNbinsX() + 1 # Include Overflow Bin
        aqgc_error_ctype= c_double()
        aqgc_count = h1AQGC.IntegralAndError(bin_start, bin_finish, aqgc_error_ctype)
        aqgc_error = aqgc_error_ctype.value
        
        h1Cov = inFile.Get(covariance_hist_name)
        covariance = h1Cov.Integral(bin_start, bin_finish)

        #h1AQGC.GetBinContent(ptbin)
        #aqgc_error = h1AQGC.GetBinError(ptbin)
        print "Expected aQGC Events ", aqgc_count, " pm ", aqgc_error
        
        # Fill Histogram
        ratio = aqgc_count/sm_count
        ratio_error = CalcRatioError(aqgc_count, sm_count, aqgc_error, sm_error, covariance, coupling_strength)
        
        print "Ratio ", ratio , " pm ", ratio_error
        
        bin_index=ratioHist.FindBin(coupling_strength)
        ratioHist.SetBinContent(bin_index, ratio)
        ratioHist.SetBinError(bin_index, ratio_error)

    ratioHist.Write(coupling_type+"_"+channel+"Pt"+str(last_pt)+"_RatiovsCoupling")


    # Fit Histograms
    xmin = ratioHist.GetXaxis().GetXmin()
    xmax = ratioHist.GetXaxis().GetXmax()
    f1 = TF1("f1", "[0]+[1]*x+[2]*x*x", xmin, xmax)
    f1.SetParameters(1, 0, 0)
    ratioHist.Fit("f1", "RN")
    f1.Write(coupling_type+"_"+channel+"Pt"+str(last_pt)+"_RatiovsCouplingFit")
    


# Properly Calculates the Error on the Ratio, taking into account the correlation between 
# the two reweightings.
# Use the standard Error Propagation Formula
# Sigma(A/B)^2  = Sigma_A^2/B^2 + Sigma)B^2*A^2/B^4 - 2 Cov(A,B)*A/B^3
#
def CalcRatioError(A, B, sigma_A, sigma_B, covariance_AB, coupling_strenth):
    if coupling_strenth == 0: return 0 # Special Case when comparing SM to itself.  No uncertainty.
    
    ratio_error = sqrt((sigma_A**2/B**2) + ((sigma_B**2)*A**2/B**4) - (2 * covariance_AB*A/B**3))
    return ratio_error


# Mapping between weight number and coupling value is defined in the MadGraph Reweight Card
def MakeCouplingStrengthHistNameContainer(channel, coupling_class):
    coupling_strength_histnames_container=[]
    
    if coupling_class == "LM":
        # LM2
        coupling_type = "LM2"
        strength_and_histnames = [
                                  ( -1000, channel+ "_aQGC_Weight_74_Pt", channel+ "_aQGC_Covariance_74_Pt"),
                                  ( -900, channel+ "_aQGC_Weight_73_Pt", channel+ "_aQGC_Covariance_73_Pt"),
                                  ( -800, channel+ "_aQGC_Weight_72_Pt", channel+ "_aQGC_Covariance_72_Pt"),
                                  ( -700, channel+ "_aQGC_Weight_71_Pt", channel+ "_aQGC_Covariance_71_Pt"),
                                  ( -600, channel+ "_aQGC_Weight_70_Pt", channel+ "_aQGC_Covariance_70_Pt"),
                                  ( -500, channel+ "_aQGC_Weight_69_Pt", channel+ "_aQGC_Covariance_69_Pt"),
                                  ( -400, channel+ "_aQGC_Weight_68_Pt", channel+ "_aQGC_Covariance_68_Pt"),
                                  ( -300, channel+ "_aQGC_Weight_67_Pt", channel+ "_aQGC_Covariance_67_Pt"),
                                  ( -200, channel+ "_aQGC_Weight_66_Pt", channel+ "_aQGC_Covariance_66_Pt"),
                                  ( -100, channel+ "_aQGC_Weight_65_Pt",channel+ "_aQGC_Covariance_65_Pt" ),
                                  ( 0, channel+ "_aQGC_Weight_50_Pt", channel+ "_aQGC_Covariance_50_Pt"),
                                  ( 100, channel+ "_aQGC_Weight_53_Pt", channel+ "_aQGC_Covariance_53_Pt"),
                                  ( 200, channel+ "_aQGC_Weight_54_Pt", channel+ "_aQGC_Covariance_54_Pt"),
                                  ( 300, channel+ "_aQGC_Weight_55_Pt", channel+ "_aQGC_Covariance_55_Pt"),
                                  ( 400, channel+ "_aQGC_Weight_56_Pt", channel+ "_aQGC_Covariance_56_Pt"),
                                  ( 500, channel+ "_aQGC_Weight_57_Pt", channel+ "_aQGC_Covariance_57_Pt"),
                                  ( 600, channel+ "_aQGC_Weight_58_Pt", channel+ "_aQGC_Covariance_58_Pt"),
                                  ( 700, channel+ "_aQGC_Weight_59_Pt", channel+ "_aQGC_Covariance_59_Pt"),
                                  ( 800, channel+ "_aQGC_Weight_60_Pt", channel+ "_aQGC_Covariance_60_Pt"),
                                  ( 900, channel+ "_aQGC_Weight_61_Pt", channel+ "_aQGC_Covariance_61_Pt"),
                                  ( 1000, channel+ "_aQGC_Weight_62_Pt", channel+ "_aQGC_Covariance_62_Pt")
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
    """
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
    """
    if coupling_class == "LT":
        # LT0
        coupling_type = "LT0"
        strength_and_histnames = [
           # ( -100, channel+ "_aQGC_Weight_24_Pt", channel+"_aQGC_Correlation_40_Category_Pt"),
                                  #( -90, channel+ "_aQGC_Weight_23_Pt"),
                                  #( -80, channel+ "_aQGC_Weight_22_Pt"),
                                  #( -70, channel+ "_aQGC_Weight_21_Pt"),
                                  #( -60, channel+ "_aQGC_Weight_20_Pt"),
                                  ( -50, channel+ "_aQGC_Weight_19_Pt", channel+ "_aQGC_Covariance_19_Pt"),
                                  ( -40, channel+ "_aQGC_Weight_18_Pt", channel+ "_aQGC_Covariance_18_Pt"),
                                  ( -30, channel+ "_aQGC_Weight_17_Pt", channel+ "_aQGC_Covariance_17_Pt" ),
                                  ( -20, channel+ "_aQGC_Weight_16_Pt", channel+ "_aQGC_Covariance_16_Pt"),
                                  ( -10, channel+ "_aQGC_Weight_15_Pt", channel+ "_aQGC_Covariance_15_Pt"),
                                  ( 0, channel+ "_aQGC_Weight_0_Pt", channel+ "_aQGC_Covariance_0_Pt"),
                                  ( 10, channel+ "_aQGC_Weight_3_Pt", channel+ "_aQGC_Covariance_3_Pt"),
                                  ( 20, channel+ "_aQGC_Weight_4_Pt", channel+ "_aQGC_Covariance_4_Pt"),
                                  ( 30, channel+ "_aQGC_Weight_5_Pt", channel+ "_aQGC_Covariance_5_Pt"),
                                  ( 40, channel+ "_aQGC_Weight_6_Pt", channel+ "_aQGC_Covariance_6_Pt"),
                                  ( 50, channel+ "_aQGC_Weight_7_Pt", channel+ "_aQGC_Covariance_7_Pt"),
                                  #( 60, channel+ "_aQGC_Weight_8_Pt"),
                                  #( 70, channel+ "_aQGC_Weight_9_Pt"),
                                  #( 80, channel+ "_aQGC_Weight_10_Pt"),
                                  #( 90, channel+ "_aQGC_Weight_11_Pt"),
                                  #( 100, channel+ "_aQGC_Weight_12_Pt")
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
    """
        # LT1
        coupling_type = "LT1"
        strength_and_histnames = [
                                  #( -100, channel+ "_aQGC_Weight_49_Pt"),
                                  #( -90, channel+ "_aQGC_Weight_48_Pt"),
                                  #( -80, channel+ "_aQGC_Weight_47_Pt"),
                                  #( -70, channel+ "_aQGC_Weight_46_Pt"),
                                  #( -60, channel+ "_aQGC_Weight_45_Pt"),
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
                                  #( 60, channel+ "_aQGC_Weight_33_Pt"),
                                  #( 70, channel+ "_aQGC_Weight_34_Pt"),
                                  #( 80, channel+ "_aQGC_Weight_35_Pt"),
                                  #( 90, channel+ "_aQGC_Weight_36_Pt"),
                                  #( 100, channel+ "_aQGC_Weight_37_Pt")
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
        
        # LT2
        coupling_type = "LT2"
        strength_and_histnames = [
                                  #( -100, channel+ "_aQGC_Weight_74_Pt"),
                                  #( -90, channel+ "_aQGC_Weight_73_Pt"),
                                  #( -80, channel+ "_aQGC_Weight_72_Pt"),
                                  #( -70, channel+ "_aQGC_Weight_71_Pt"),
                                  #( -60, channel+ "_aQGC_Weight_70_Pt"),
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
                                  #( 60, channel+ "_aQGC_Weight_58_Pt"),
                                  #( 70, channel+ "_aQGC_Weight_59_Pt"),
                                  #( 80, channel+ "_aQGC_Weight_60_Pt"),
                                  #( 90, channel+ "_aQGC_Weight_61_Pt"),
                                  #( 100, channel+ "_aQGC_Weight_62_Pt"),
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
    """
    
    return coupling_strength_histnames_container


if __name__=="__main__":
    Ratio_Couplings_AllCouplingClasses()
