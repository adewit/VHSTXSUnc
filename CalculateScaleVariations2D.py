from ROOT import *; import glob, numpy as n; from array import array
from AdditionalFunctions import*

#inputFileName = "pwgevents-0001-mod"
gStyle.SetOptStat(0);
gStyle.SetTitleYOffset(1.2)
gStyle.SetTitleXOffset(1.2)
histcolors = [221,94, 209, 4, 2, 1]
CMS=False
if CMS:NVar = 9
else:NVar = 8
scaleVars=[]#array of histogram with scale variations
scaleVarsCMS=[]#array of histogram with scale variations
scaleVarsRebinnedCMS=[]#array of histogram with scale variations
scaleVarsRebinned=[]#array of histogram with scale variations
scaleVarsInclpT=[]#array of histogram with scale variations
scaleVarsInclpTXTitles=[]#array of histogram with scale variations
pTJetstitles = ["FWD","0-75 GeV0J", "0-75 GeV1J","0-75 GeVGE2J","75-150 GeV0J", "75-150 GeV1J","75-150 GeVGE2J","150-250 GeV0J", "150-250 GeV1J","150-250 GeVGE2J","250-400 GeV0J", "250-400 GeV1J","250-400 GeVGE2J",">400 GeV0J", ">400 GeV1J",">400 GeVGE2J"]

if not CMS:
    #inputFileName = "cmsgrid_final_weights"
    #inputFileName = "cmsgrid_final_weights"
    #inputFileName = "cmsgrid_final_weights"
    #inputFileName = "pwgevents-0222-mod_rec"
    inputFileName = "../pwgevents-hadd-mod"
    f = TFile(inputFileName+".root", "read")
else:
    filein = TFile("../STXSUnc/ZH_ZToLL_HToBB.root",'read')
    maintree=filein.Get("Events")

if not CMS:
    centralScale = f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30") # mur = 1, muf=1
    centralScaleRebinned = ReorganisedHist(centralScale, 'centralScaleRebinned')
#    centralScaleRebinned.Scale(100000)
else:
    centralScaleRebinned=scaleVarsRebinned[4].Clone()
    centralScaleRebinned.SetName("centralScaleRebinnedCMS")


for i in range(0,NVar):
    if not CMS:
        if i>0:
            scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30["+str(i)+"]")) 
        else:scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30")) #forward region
        scaleVars[i].SetName("scaleVars_"+str(i))
#        scaleVars[i].Scale(centralScale.Integral()/scaleVars[i].Integral())
#
        scaleVarsRebinned.insert(i,ReorganisedHist(scaleVars[i], "scaleVarsRebinned_"+str(i)))
        scaleVarsRebinned[i].Scale(centralScaleRebinned.Integral()/scaleVarsRebinned[i].Integral())
    else:
        scaleVarsCMS.insert(i,  TH1F("scaleVarsCMS"+str(i),"scaleVarsCMS"+str(i),16,400,416))
        maintree.Draw("HTXS_stage_1p1_uncert_cat>>scaleVarsCMS"+str(i), "1*(LHEScaleWeight["+str(i)+"]*genWeight)","goff");
        scaleVarsCMS.insert(i, maintree.GetHistogram())
        scaleVarsRebinned.insert(i, ReorganisedHistCMS(scaleVarsCMS[i], "scaleVarsRebinned_"+str(i)))

#if not CMS:
#    centralScale = f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30") # mur = 1, muf=1
#    centralScaleRebinned = ReorganisedHist(centralScale, 'centralScaleRebinned')
##    centralScaleRebinned.Scale(100000)
#else:
#    centralScaleRebinned=scaleVarsRebinned[4].Clone()
#    centralScaleRebinned.SetName("centralScaleRebinnedCMS")
#
MaxScaleDeviationRebinned  = centralScaleRebinned.Clone()
MaxScaleDeviationRebinned.SetName("MaxScaleDeviationRebinned")#histogram with maximum deviations from central scale with all processes combined.
MaxScaleDeviationRebinned.SetTitle("MaxScaleDeviationRebinned")#histogram with maximum deviations from central scale with all processes combined.


for k in range(0, npTBins):
    for j in range(0, nJetBins):
        dN=[]
        globalBin = nJetBins*k + j + 1
        binMax = nJetBins*k+(nJetBins)
        if centralScaleRebinned.GetBinContent(globalBin)==0:
            print globalBin
            continue;
        for i in range(0,NVar):
            if (i==5 or i==6 or i==7) and not CMS:continue;
            #if i==6 and CMS:continue;
            dN.insert(i,abs(scaleVarsRebinned[i].Integral(globalBin, binMax)-centralScaleRebinned.Integral(globalBin, binMax)))
        dNMax = max(dN)
        print globalBin, dN, dNMax, centralScaleRebinned.Integral(globalBin, binMax)
        MaxScaleDeviationRebinned.SetBinContent(globalBin, dNMax)

centralScaleRebinnedCMS=scaleVarsRebinned[4].Clone()
centralScaleRebinnedCMS.SetName("centralScaleRebinnedCMS")
if CMS:f0 = TFile("MaxScaleVarInclpT_CMS.root","read")
else: f0 = TFile("MaxScaleVarInclpT_central.root","read")
UncInPtBins5 = f0.Get("UncInPtBins5")

UncInPtandNJets=[]
for k in range(0, 4):
    UncInPtandNJets.insert(k, TH1F("UncInPtandNJets"+str(k), "",nJetBins*npTBins+1, 0,nJetBins*npTBins+1))#k:0=deltapTTotal, 1=delta1, 2=delta2, 3=total
UncInPtandNJets[0].SetBinContent(1, 0)
UncInPtandNJets[1].SetBinContent(1, 0)
UncInPtandNJets[2].SetBinContent(1, 0)
UncInPtandNJets[3].SetBinContent(1, 0)
##Define deltas:
for j in range(0, nJetBins):
    for k in range(0, npTBins):
        delta1=0;  delta2 = 0;
        globalBin = nJetBins*k + j + 1
        binMax = nJetBins*k+(nJetBins) 
        if j==0:
            delta1 = -MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j+ 2)/centralScaleRebinned.GetBinContent(nJetBins*k+j+1)
            delta2 = 0
        if j==1:
            delta1 = MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j + 1)/(centralScaleRebinned.Integral(nJetBins*k + j + 1, nJetBins*k + j + 2))
            delta2 = -MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j + 2)/(centralScaleRebinned.GetBinContent(nJetBins*k + j + 1))
        if j==2:
            delta1 = MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j)/(centralScaleRebinned.Integral(nJetBins*k + j,nJetBins*k + j + 1))
            delta2 = MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j+1)/centralScaleRebinned.GetBinContent(nJetBins*k + j+1)
        deltapTTotal = UncInPtBins5.GetBinContent(k+1);
        print deltapTTotal
        total = sqrt(deltapTTotal**2 + delta1**2 +  delta2**2)
        UncInPtandNJets[0].SetBinContent(globalBin+1, deltapTTotal)
        UncInPtandNJets[1].SetBinContent(globalBin+1, delta1)
        UncInPtandNJets[2].SetBinContent(globalBin+1, delta2)
        UncInPtandNJets[3].SetBinContent(globalBin+1, total)
        UncInPtandNJets[1].GetXaxis().SetBinLabel(globalBin,pTJetstitles[globalBin-1])
        UncInPtandNJets[2].GetXaxis().SetBinLabel(globalBin,pTJetstitles[globalBin-1])

#Save the results
if CMS:fOut = TFile("MaxScaleVarJetsandPt_CMS.root",'recreate')
else: fOut = TFile("MaxScaleVarJetsandPt_central.root",'recreate')
MaxScaleDeviationRebinned.Write()
centralScaleRebinned.Write()
UncInPtandNJets[1].Write()
UncInPtandNJets[2].Write()
UncInPtandNJets[3].Write()
UncInPtandNJets[0].Write()
for i in range(0,NVar):
    if CMS:scaleVarsCMS[i].Write()
    else: scaleVars[i].Write()
    scaleVarsRebinned[i].Write()
fOut.Close()

_MYW = 800; _MYH = 600
_MYT = 0.08*_MYH; _MYB = 0.18*_MYH;
_MYL = 0.12*_MYW; _MYR = 0.1*_MYW
cB=0;
cB=TCanvas("cB","cB",_MYW,_MYH);
cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
UncInPtandNJets[1].SetLineColor(kRed)
#UncInPtandNJets[1].SetAxisRange(-0.5, 0.5, "Y");
UncInPtandNJets[1].SetAxisRange(-0.45, 0.5, "Y");
#UncInPtandNJets[1].SetAxisRange(-0.1, 0.3, "Y");
UncInPtandNJets[1].SetYTitle("Relative QCD uncertainty")
UncInPtandNJets[1].Draw()
UncInPtandNJets[2].SetLineColor(kBlue)
UncInPtandNJets[2].SetLineWidth(3)
UncInPtandNJets[3].SetLineWidth(3)
UncInPtandNJets[1].SetLineWidth(3)
UncInPtandNJets[0].SetLineWidth(3)
UncInPtandNJets[2].Draw("same")
UncInPtandNJets[3].SetLineColor(kGreen+3)
UncInPtandNJets[3].Draw("same")
UncInPtandNJets[0].SetLineColor(kBlack)
UncInPtandNJets[0].Draw("same")
leg = TLegend(0.6, 0.7, 0.9, 0.90);
leg.SetTextFont(42)
leg.AddEntry(UncInPtandNJets[0], "p_{T}^{V} bins uncertainty", "l");
leg.AddEntry(UncInPtandNJets[1], "#Delta_{1}", "l");
leg.AddEntry(UncInPtandNJets[2], "#Delta_{2}", "l");
leg.AddEntry(UncInPtandNJets[3], "Total", "l");
leg.SetBorderSize(0);
#leg.Draw('same');
cB.SetTickx(0); cB.SetTicky(0);
if CMS:cB.SaveAs("pTBinsJetsUnc_CMS.pdf")
else: cB.SaveAs("pTBinsJetsUnc_central.pdf")
