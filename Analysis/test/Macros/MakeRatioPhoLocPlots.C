/*
 * ROOT Macro
 * To plot aQGC to SM Ratio, for different photon locations
 * in the detector.
 * Example Execution
 * root -l MakeRatioPhoLocPlots.C
 */


#include "TFile.h"
#include "TH1F.h"
#include "TF1.h"
#include "TCanvas.h"
#include <vector>
#include <string>

//using namespace std;


const string HISTOGRAM_DIR="../Histograms/LepGammaGammaFinalElandMuUnblindAll_2015_6_9_ScaleFactors/";

const string PLOT_DIR="../Plots/LepGammaGammaFinalElandMuUnblindAll_2015_6_9_ScaleFactors/Ratio_PhoLoc/";

const int NUM_CHANNELS=2;
const string CHANNELS[]={"ElectronChannel", "MuonChannel"};

const int NUM_PHOTON_LOCATIONS=3;
const string PHOTON_LOCATIONS[]={"EBEB", "EBEE", "EEEB"};

const int NUM_AQGC_PARAMETERS=5;
const string AQGC_PARAMETERS[]={"LT0", "LT1", "LT2", "LM2", "LM3"};

const int NUM_SUBL_PHOTON_PT_CUTS = 1;
const string SUBL_PHOTON_PT_CUTS[]={"Sublph25"};

const int NUM_LEAD_PHOTON_PT_CUTS = 1;
const string LEAD_PHOTON_PT_CUTS[]={"Pt70"};

//const char* CHANNELS_ARR[]={"ElectronChannel", "MuonChannel"};

void MakeSingleRatioPhoLocPlot(TFile * histogram_file, string channel, string subl_cut,
			       string photon_location,  string aqgc_parameter, string lead_photon_cut) ;


/*
 * Plots the aQGC to SM fit for a given photon location channel (black), 
 * compared to the overall fit (red)
 */

void MakeRatioPhoLocPlots(){

  //std::vector<std::string> channels(std::begin(CHANNELS), std::end(CHANNELS));

  for(int aqgc_parameter_index=0; aqgc_parameter_index < NUM_AQGC_PARAMETERS; aqgc_parameter_index++){
    string aqgc_parameter=AQGC_PARAMETERS[aqgc_parameter_index];

    string fileLoc;
    if(aqgc_parameter=="LT0" || aqgc_parameter=="LT1" || aqgc_parameter=="LT2"){
      fileLoc = HISTOGRAM_DIR + "LT012_Reweight/Ratio_Couplings_SelectPT.root";
    }
    if(aqgc_parameter=="LM0" || aqgc_parameter=="LM1" || aqgc_parameter=="LM2" || aqgc_parameter=="LM3"){
      fileLoc = HISTOGRAM_DIR + "LM0123_Reweight/Ratio_Couplings_SelectPT.root";
    }
    TFile * histogram_file =TFile::Open(fileLoc.c_str(), "READ");
    
    for(int channel_index=0; channel_index < NUM_CHANNELS; channel_index++){
      string channel = CHANNELS[channel_index];
      for(int subl_cut_index=0; subl_cut_index < NUM_SUBL_PHOTON_PT_CUTS; subl_cut_index++){
	string subl_cut = SUBL_PHOTON_PT_CUTS[subl_cut_index];
	for(int photon_location_index=0; photon_location_index < NUM_PHOTON_LOCATIONS; photon_location_index++){
	  string photon_location = PHOTON_LOCATIONS[photon_location_index];
	  for(int lead_photon_cut_index = 0; lead_photon_cut_index < NUM_LEAD_PHOTON_PT_CUTS; lead_photon_cut_index++){
	    string lead_photon_cut = LEAD_PHOTON_PT_CUTS[lead_photon_cut_index];

	    MakeSingleRatioPhoLocPlot(histogram_file, channel, subl_cut, photon_location, aqgc_parameter, lead_photon_cut);

	  }
	}
      }
    }
  }
}

/*
 * With the channel, photon location, subl_cut, and aqgc_parameters 
 * passed as arguments. Makes the corresponding Histograms of the 
 * aQGC to SM ratios as a function of coupling strength
 */

void MakeSingleRatioPhoLocPlot(TFile * histogram_file, string channel, string subl_cut, 
			       string photon_location,  string aqgc_parameter, string lead_photon_cut){ 
  
  std::cout << aqgc_parameter << " " << channel << " " << photon_location << std::endl;
  //SetUp Canvas
  TCanvas * canvas = new TCanvas();
  
  //Draw Histogram In Black
  hist_photon_loc_name=aqgc_parameter+"_"+channel+"_"+ subl_cut+ "_" + photon_location+"_" + lead_photon_cut +"_RatiovsCoupling";
  TH1F *hist_photon_loc = histogram_file->Get(hist_photon_loc_name.c_str());

  
  //Range Depends on Coupling Type
  if(aqgc_parameter=="LT0" || aqgc_parameter=="LT1" || aqgc_parameter=="LT2"){
    hist_photon_loc->SetAxisRange(-60, 60, "X");
  }
  if(aqgc_parameter=="LM2" || aqgc_parameter=="LM3"){
    fileLoc = HISTOGRAM_DIR + "LM0123_Reweight/Ratio_Couplings_SelectPT.root";
    hist_photon_loc->SetAxisRange(-1000, 1000, "X");
  }
  
  hist_photon_loc->SetAxisRange(0.5, 4, "Y");
  hist_photon_loc->SetLineColor(kBlack);
  
  //Set Titles
  string title=photon_location+", "+channel +" "+aqgc_parameter;
  hist_photon_loc->SetTitle(title.c_str());
  hist_photon_loc->GetXaxis()->SetTitle("Coupling Strength (TeV^{-4})");


  hist_photon_loc->Draw();

  //Draw Fit (for Histogram) in Black Dashed Lines
  fit_photon_loc_name=aqgc_parameter+"_"+channel+"_"+ subl_cut+ "_" + photon_location+"_" + lead_photon_cut +"_RatiovsCouplingFit";
  TF1 * fit_photon_loc=histogram_file->Get(fit_photon_loc_name.c_str());
  fit_photon_loc->SetLineColor(kBlack);
  fit_photon_loc->SetLineWidth(2);
  fit_photon_loc->SetLineStyle(2); //Dashed line
  fit_photon_loc->Draw("same");

  //Draw Average Fit in Red Dashed Line
  /*
  string fit_average_name=aqgc_parameter+"_"+channel+"_All_Pt70_RatiovsCouplingFit";
  TF1 * fit_average=histogram_file->Get(fit_average_name.c_str());
  fit_average->SetLineColor(kRed);
  fit_average->SetLineWidth(2);
  fit_average->SetLineStyle(2); //Dashed line
  fit_average->Draw("same");
  */
  
  gStyle->SetOptStat(0); // No Stats Box
 
  string plotLoc=PLOT_DIR+aqgc_parameter+"_"+channel+"_"+ subl_cut+ "_" + photon_location+"_" + lead_photon_cut +".png";
  canvas->SaveAs(plotLoc.c_str());
}
