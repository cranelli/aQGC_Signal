//#include "TFile.h"
#include "TH1F.h"
#include <iostream>
#include "DrawOverflowBin.C"
//#include <string>
#include <vector>
//#include "plotHistsAndRatio.C"

/*
 * Macro to Overlay Multiple Histograms
 */
void Overlay(TH1F * h1, TH1F *h2);
void Overlay(std::vector<TH1F*> hists);


//Overlay Two Histograms
void Overlay(TH1F * h1, TH1F *h2){
    std::vector<TH1F*> hists;
    hists.push_back(h1);
    hists.push_back(h2);
   

    Overlay(hists);
};

//Overlay a vector of Histograms
void Overlay(std::vector<TH1F*> hists){
    // TFile * rootFile = TFile::Open(rootName, "READ");
  
    //TH1F * hists[num_hists];
    vector<TH1F*> hists_overflow;
    
    for(int i =0; i < hists.size(); i++){
      
        std::cout << hists[i]->GetName() << std::endl;
        hists_overflow.push_back( DrawOverflowBin(hists[i]));
        //TH1F * hist_overflow= DrawOverflowBin(hists[i]);
	// DrawOverflowBin(hists[i])->Draw();
        
       
        gStyle->SetOptStat(0);
        if(i==0){
	  std::cout << "working" << std::endl;
	  hists_overflow[i]->SetLineColor(kRed);
	  hists_overflow[i]->Draw();
        }
        else {
	  hists_overflow[i]->SetLineColor(kBlue);
	  hists_overflow[i]->Draw("same");
        }
        
    }
    
};

    //For First One, Set Axis Titles
    /*
    if(i ==0){
      hists_Overflow[i]->SetTitle(title.c_str());
      hists_Overflow[i]->GetXaxis()->SetTitle(xaxis_title.c_str());
      hists_Overflow[i]->GetYaxis()->SetTitle(yaxis_title.c_str());
      
      leg = new TLegend(0.1,0.7,0.48,0.9);
      hists_Overflow[i]->Draw();
      leg->AddEntry(hists_Overflow[i], leg_titles[i].c_str());
    } else {
      hists_Overflow[i]->Draw("same"); 
      leg->AddEntry(hists_Overflow[i], leg_titles[i].c_str());
    }
  }
  leg->Draw();
  
  //rootFile->Close();
  */
