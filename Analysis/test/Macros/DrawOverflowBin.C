#include "TH1F.h"
#include <iostream>
#include <sstream>


TH1F * DrawOverflowBin(TH1F * h)
{
  // This function paint the histogram h with an extra bin for overflows                                                                               
  
  UInt_t nx = h->GetNbinsX()+1;
  Double_t *xbins= new Double_t[nx+1];
  for (UInt_t i=0;i<nx;i++){
    xbins[i]=h->GetBinLowEdge(i+1);
  }
  xbins[nx]=xbins[nx-1]+h->GetBinWidth(nx);
  
  //char *tempName= new char[strlen(h->GetName())+10];
  //sprintf(tempName,"%swtOverFlow",h->GetName());
  
  stringstream tempName;
  tempName << h->GetName() << "wtOverFlow";
  // Book a temporary histogram having ab extra bin for overflows                                                                                      
  TH1F *htmp = new TH1F(tempName.str().c_str(), h->GetTitle(), nx, xbins);
  
  // Reset the axis labels                                                                                                                             
  htmp->SetXTitle(h->GetXaxis()->GetTitle());
  htmp->SetYTitle(h->GetYaxis()->GetTitle());
  
  // Fill the new hitogram including the extra bin for overflows                                                                                       
  for (UInt_t i=1; i<=nx; i++){
    htmp->Fill(htmp->GetBinCenter(i), h->GetBinContent(i));
    htmp->SetBinError(i, h->GetBinError(i));
  }
  //htmp->Draw();
  // Fill the underflows                                                                                                                               
  //htmp->Fill(h->GetBinLowEdge(1)-1, h->GetBinContent(0));                                                                                            
  // Restore the number of entries                                                                                                                       
 
  htmp->SetEntries(h->GetEntries());
   /*
  // FillStyle and color                                                                                                                               
  htmp->SetFillStyle(h->GetFillStyle());
  htmp->SetFillColor(h->GetFillColor());
  */
  return htmp;                          
  //return h;
}
