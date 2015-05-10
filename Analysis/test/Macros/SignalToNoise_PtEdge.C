#include "TFile.h"
#include "TH1F.h"

#include <iostream>
#include <string>
#include <cmath>

const char * gRootName = "../LM0123_Reweight_RecoCategoryHistograms.root";

//string gAQGCName = "MuonChannel_aQGC_Weight_57_Pt"; //LM2 =500
string gAQGCName = "MuonChannel_aQGC_Weight_61_Pt"; // LM2 = 900
// Treating SM as the Background
string gSMName="MuonChannel_aQGC_Weight_0_Pt";

double gDefaultPtEdge = 70;
double gDefaultBkgdUncert = 10.5;

void SignalToNoise_PtEdge(){
    
    std::cout << "AQGC Reweighting: " << gAQGCName << std::endl;
    TFile * rootFile = TFile::Open(gRootName, "READ");
    rootFile->Print();
    
    TH1F * h1AQGC = rootFile->Get(gAQGCName.c_str());
    TH1F * h1SM = rootFile->Get(gSMName.c_str());
    
    //Scale to Normalize to the expected number of events in the combined ISR FSR weighted sample
    double scale =31115; 

    h1AQGC->Scale(scale);
    h1SM->Scale(scale);

    Int_t num_bins = h1AQGC->GetNbinsX();
    std::cout << num_bins << std::endl;
    
    Int_t default_bin_index = h1SM->FindBin(gDefaultPtEdge);
    double sm_events_above_default = h1SM->Integral(default_bin_index, num_bins+1);
    std::cout<< sm_events_above_default << std::endl;
    
    const int num_edge_pts = 14;
    Double_t edge_pts[] = {71, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400};
    
    Double_t snrs[num_edge_pts];
    
    for(int i =0; i < num_edge_pts; i++){
        std::cout << edge_pts[i] << std::endl;
        
        Int_t bin_index = h1AQGC->FindBin(edge_pts[i]);
        //std::cout << bin_index << std::endl;
        
        //Include Overflow bin
        double aqgc_events_above_threshold = h1AQGC->Integral(bin_index, num_bins+1);
        std::cout << aqgc_events_above_threshold << std::endl;
        
        double sm_events_above_threshold = h1SM->Integral(bin_index, num_bins+1);
        std::cout << sm_events_above_threshold << std::endl;
        
        double signal = aqgc_events_above_threshold - sm_events_above_threshold;
	std::cout << "Signal: " << signal << std::endl;
	
	double fracDefaultBkgdUncert = sqrt((sm_events_above_threshold/sm_events_above_default)*pow(gDefaultBkgdUncert, 2));
	std::cout << "Fractional Background Uncertainty: " << fracDefaultBkgdUncert << std::endl;

	
        double noise = sqrt(pow(fracDefaultBkgdUncert, 2) + aqgc_events_above_threshold);
        
        std::cout << "Noise: " << noise << std::endl;
        
        double snr = signal/noise;
        snrs[i]=snr;
        std::cout << "Signal to Noise: " << snr << std::endl;
       
    }
    TGraph * snr_graph = new TGraph(num_edge_pts, edge_pts, snrs);
    snr_graph->GetXaxis()->SetTitle("Lead Photon Pt Edge");
    snr_graph->GetYaxis()->SetTitle("Signal to Noise Ratio");
    snr_graph->Draw("ap*");
}
    //TH1F * h1BkgdRebin = h1Bkgd->Rebin(4, "BkgdRebin", xbins)
    
    //h1SignalRebin->Draw();
    //h1BkgdRebin->Draw("same");
    

    //rootFile->Close();
