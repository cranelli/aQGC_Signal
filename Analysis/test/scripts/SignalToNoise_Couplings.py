from ROOT import TFile
from ROOT import TH1F
from ROOT import TGraph

from math import sqrt

from array import array

QGC_HISTOGRAM_DIRS=[("LM","../Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_5_3/LM0123_Reweight/"),
                ("LT", "../Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_5_3/LT012_Reweight/")]


CHANNELS = ["ElectronChannel", "MuonChannel"]


LAST_BIN_INDEX = 4 # 70+ Bin
BACKGROUND_UNCERTAINTY = {'ElectronChannel':100, 'MuonChannel':10.5}



# Run over all the aQGC Classes, in this case the LT's and the LM's
def SignalToNoise_Couplings_AllCouplingClasses():
    for coupling_class, histogram_dir in QGC_HISTOGRAM_DIRS:
        in_file_name=  histogram_dir+"Reweighted_RecoCategoryHistograms_Normalized.root"
        out_file_name =histogram_dir+"SignalToNoise_Couplings.root"
        SignalToNoise_Couplings(in_file_name, out_file_name, coupling_class)

    
    
def SignalToNoise_Couplings(in_file_name, out_file_name, coupling_class):

    inFile = TFile(in_file_name, "READ")
    outFile = TFile(out_file_name, "RECREATE")

    for channel in CHANNELS:
        sm_hist_name = channel+ "_aQGC_Weight_0_Category_Pt"
        h1SM = inFile.Get(sm_hist_name)
        # h1SM.Scale(LM_SCALE)

        sm_events = h1SM.GetBinContent(LAST_BIN_INDEX)
        print "Expected SM Events ", sm_events

        # Defined in the code.  Based on the Madgraph Reweight Card
        coupling_strength_histnames_container = MakeLMCouplingStrengthHistNameContainer(channel, coupling_class)

        for coupling_type, strength_and_histnames in coupling_strength_histnames_container:
            MakeGraphByCouplingType(channel, coupling_type, strength_and_histnames, sm_events, inFile, outFile)


# For a specified coupling type, ie LM0, LM1, LM2, etc, makes a Signal to Noise Graph as a
# function of coupling strength.
def MakeGraphByCouplingType(channel, coupling_type, strength_and_histnames, sm_events, inFile, outFile):
    print channel
    print "Coupling Type ", coupling_type
    coupling_strengths=[]
    snrs=[]

    #Loop Over All coupling_strengths
    for coupling_strength, hist_name in strength_and_histnames:
        coupling_strengths.append(coupling_strength)
        print "Coupling Strength", coupling_strength

        h1AQGC = inFile.Get(hist_name)
        #h1AQGC.Scale(LM_SCALE)

        aqgc_events = h1AQGC.GetBinContent(LAST_BIN_INDEX)
        print "Expected aQGC Events ", aqgc_events
        
        signal = aqgc_events - sm_events
        print "Signal ", signal
        
        noise = sqrt((BACKGROUND_UNCERTAINTY[channel]**2) + aqgc_events)
        print "Noise ", noise 
        
        snr = signal/noise
        snrs.append(snr)
        print "Signal to Noise Ratio ", snr

    print coupling_strengths
    print snrs
   # print len(COUPLING_STRENGH_HISTNAMES)
    snr_graph = TGraph(len(strength_and_histnames), array('d',coupling_strengths), array('d', snrs))
    snr_graph.SetTitle(coupling_type+" "+channel+" Signal to Noise As a Function of Coupling Strength")
    snr_graph.GetXaxis().SetTitle("Coupling Strength (TeV^{-4})")
    snr_graph.GetYaxis().SetTitle("Signal to Noise")
                                    
    
    snr_graph.Write(coupling_type+"_"+channel+"_Graph")

# Mapping between weight number and coupling value is defined in the MadGraph Reweight Card
def MakeLMCouplingStrengthHistNameContainer(channel, coupling_class):
    coupling_strength_histnames_container=[]
    
    if coupling_class == "LM":
        # LM2
        coupling_type = "LM2"
        strength_and_histnames = [
                                  ( 100, channel+ "_aQGC_Weight_53_Category_Pt"),
                                  ( 200, channel+ "_aQGC_Weight_54_Category_Pt"),
                                  ( 300, channel+ "_aQGC_Weight_55_Category_Pt"),
                                  ( 400, channel+ "_aQGC_Weight_56_Category_Pt"),
                                  ( 500, channel+ "_aQGC_Weight_57_Category_Pt"),
                                  ( 600, channel+ "_aQGC_Weight_58_Category_Pt"),
                                  ( 700, channel+ "_aQGC_Weight_59_Category_Pt"),
                                  ( 800, channel+ "_aQGC_Weight_60_Category_Pt"),
                                  ( 900, channel+ "_aQGC_Weight_61_Category_Pt"),
                                  ( 1000, channel+ "_aQGC_Weight_62_Category_Pt")
                                ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
    
        # LM3
        coupling_type = "LM3"
        strength_and_histnames = [
                                  ( 100, channel+ "_aQGC_Weight_78_Category_Pt"),
                                  ( 200, channel+ "_aQGC_Weight_79_Category_Pt"),
                                  ( 300, channel+ "_aQGC_Weight_80_Category_Pt"),
                                  ( 400, channel+ "_aQGC_Weight_81_Category_Pt"),
                                  ( 500, channel+ "_aQGC_Weight_82_Category_Pt"),
                                  ( 600, channel+ "_aQGC_Weight_83_Category_Pt"),
                                  ( 700, channel+ "_aQGC_Weight_84_Category_Pt"),
                                  ( 800, channel+ "_aQGC_Weight_85_Category_Pt"),
                                  ( 900, channel+ "_aQGC_Weight_86_Category_Pt"),
                                  ( 1000, channel+ "_aQGC_Weight_87_Category_Pt")
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
    
    if coupling_class == "LT":
        # LT0
        coupling_type = "LT0"
        strength_and_histnames = [
                                  ( 10, channel+ "_aQGC_Weight_3_Category_Pt"),
                                  ( 20, channel+ "_aQGC_Weight_4_Category_Pt"),
                                  ( 30, channel+ "_aQGC_Weight_5_Category_Pt"),
                                  ( 40, channel+ "_aQGC_Weight_6_Category_Pt"),
                                  ( 50, channel+ "_aQGC_Weight_7_Category_Pt"),
                                  ( 60, channel+ "_aQGC_Weight_8_Category_Pt"),
                                  ( 70, channel+ "_aQGC_Weight_9_Category_Pt"),
                                  ( 80, channel+ "_aQGC_Weight_10_Category_Pt"),
                                  ( 90, channel+ "_aQGC_Weight_11_Category_Pt"),
                                  ( 100, channel+ "_aQGC_Weight_12_Category_Pt")
                                  ]
        coupling_strength_histnames_container.append((coupling_type, strength_and_histnames))
    
    
    return coupling_strength_histnames_container


if __name__=="__main__":
    SignalToNoise_Couplings_AllCouplingClasses()
