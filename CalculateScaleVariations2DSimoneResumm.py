from ROOT import *; import glob, numpy as n; from array import array
from AdditionalFunctions import*

#inputFileName = "pwgevents-0001-mod"
gStyle.SetOptStat(0);
gStyle.SetTitleYOffset(1.2)
gStyle.SetTitleXOffset(1.2)
histcolors = [2,94, 209, 221, 4, 1, 923, 435,416,620,419]
CMS=False
if CMS:NVar = 9
else:NVar = 11
scaleVars=[]#array of histogram with scale variations
scaleVarsCMS=[]#array of histogram with scale variations
scaleVarsRebinnedCMS=[]#array of histogram with scale variations
scaleVarsRebinned=[]#array of histogram with scale variations
scaleVarsInclpT=[]#array of histogram with scale variations
scaleVarsInclpTXTitles=[]#array of histogram with scale variations
pTJetstitles = ["FWD","0-75 GeV0J", "0-75 GeV1J","0-75 GeVGE2J","75-150 GeV0J", "75-150 GeV1J","75-150 GeVGE2J","150-250 GeV0J", "150-250 GeV1J","150-250 GeVGE2J","250-400 GeV0J", "250-400 GeV1J","250-400 GeVGE2J",">400 GeV0J", ">400 GeV1J",">400 GeVGE2J"]
scaleTitles= ["#mu_{R}=1.0 & #mu_{F}=1.0","#mu_{R}=1.0 & #mu_{F}=2.0", "#mu_{R}=2.0 & #mu_{F}=1.0", "#mu_{R}=2.0 & #mu_{F}=2.0", "#mu_{R}=1.0 & #mu_{F}=0.5", "#mu_{R}=0.5 & #mu_{F}=1.0", "#mu_{R}=0.5 & #mu_{F}=0.5","#mu_{R}=2.0 & #mu_{F}=0.5","#mu_{R}=0.5 & #mu_{F}=2.","10th weight", "11th weight"]
if not CMS:
    #inputFileName = "pwgevents-0326-mod"
    inputFileName = "../VHSTXS_Files/full_isLepton"
    #inputFileName = "../VHSTXS_Files/all"
    #inputFileName = "../VHSTXS_Files/pwgevents-393"
    f = TFile(inputFileName+".root", "read")
else:
    filein = TFile("../STXSUnc/ZH_ZToLL_HToBB.root",'read')
    maintree=filein.Get("Events")

if not CMS:
    centralScale = f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30[000]") # mur = 1, muf=1
    #centralScale = f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30") # mur = 1, muf=1
    centralScaleRebinned = ReorganisedHist(centralScale, 'centralScaleRebinned')
else:
    centralScaleRebinned=scaleVarsRebinned[4].Clone()
    centralScaleRebinned.SetName("centralScaleRebinnedCMS")

scaleVarsRebinnedDiff=[]
for i in range(0,NVar):
    if not CMS:
        if i<10:
            #scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30["+str(i)+"]")) 
            scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30[00"+str(i)+"]")) 
#        elif i==0 :scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30")) #forward region
        elif i==10:scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30[010]")) #forward region
        scaleVars[i].SetName("scaleVars_"+str(i))
        scaleVarsRebinned.insert(i,ReorganisedHist(scaleVars[i], "scaleVarsRebinned_"+str(i)))
        scaleVarsRebinnedDiff.insert(i, scaleVarsRebinned[i].Clone()) 
        #scaleVarsRebinned[i].Scale(centralScaleRebinned.Integral()/scaleVarsRebinned[i].Integral())
    else:
        scaleVarsCMS.insert(i,  TH1F("scaleVarsCMS"+str(i),"scaleVarsCMS"+str(i),16,400,416))
        maintree.Draw("HTXS_stage_1p1_uncert_cat>>scaleVarsCMS"+str(i), "1*(LHEScaleWeight["+str(i)+"]*genWeight)","goff");
        scaleVarsCMS.insert(i, maintree.GetHistogram())
        scaleVarsRebinned.insert(i, ReorganisedHistCMS(scaleVarsCMS[i], "scaleVarsRebinned_"+str(i)))

MaxScaleDeviationRebinned1  = centralScaleRebinned.Clone()
MaxScaleDeviationRebinned2  = centralScaleRebinned.Clone()
MaxScaleDeviationRebinned1.SetName("MaxScaleDeviationRebinned1")#histogram with maximum deviations from central scale with all processes combined.
MaxScaleDeviationRebinned2.SetTitle("MaxScaleDeviationRebinned2")#histogram with maximum deviations from central scale with all processes combined.

for k in range(0, npTBins):
    for j in range(0, nJetBins):
        dN1=[]
        dN2=[]
        globalBin = nJetBins*k + j + 1
        binMax = nJetBins*k+(nJetBins)
        if centralScaleRebinned.GetBinContent(globalBin)==0:
            print globalBin
            continue;
        for i in range(0,NVar):
            #if (i<9) :continue;
            #if (i==5 or i==7) and CMS:continue;
            if (i==1 or i==2):dN1.insert(i,abs(scaleVarsRebinned[i].GetBinContent(globalBin) - centralScaleRebinned.GetBinContent(globalBin)))
            if (i>2 and i<9):dN2.insert(i,abs(scaleVarsRebinned[i].GetBinContent(globalBin) - centralScaleRebinned.GetBinContent(globalBin)))
            scaleVarsRebinnedDiff[i].SetBinContent(globalBin, scaleVarsRebinned[i].GetBinContent(globalBin) - centralScaleRebinned.GetBinContent(globalBin))
        dNMax_1 = max(dN1)
        dNMax_2 = max(dN2)
        print globalBin, dN1, dNMax_1 
        print globalBin, dN2, dNMax_2
        MaxScaleDeviationRebinned1.SetBinContent(globalBin, dNMax_1)
        MaxScaleDeviationRebinned2.SetBinContent(globalBin, dNMax_2)

centralScaleRebinnedCMS=scaleVarsRebinned[4].Clone()
centralScaleRebinnedCMS.SetName("centralScaleRebinnedCMS")
#if CMS:f0 = TFile("MaxScaleVarInclpT_CMS.root","read")
#else: f0 = TFile("MaxScaleVarInclpT_centralSimone.root","read")
#UncInPtBins5 = f0.Get("UncInPtBins5")

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
        #if j==0:
        delta1 = MaxScaleDeviationRebinned1.GetBinContent(globalBin)/centralScaleRebinned.GetBinContent(globalBin)
        delta2 = MaxScaleDeviationRebinned2.GetBinContent(globalBin)/centralScaleRebinned.GetBinContent(globalBin)
        #if j==1:
            #delta1 = MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j + 1)/(centralScaleRebinned.Integral(nJetBins*k + j + 1, nJetBins*k + j + 2))
#            delta2 = -MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j + 2)/(centralScaleRebinned.GetBinContent(nJetBins*k + j + 1))
#        #if j==2:
#            delta1 = MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j)/(centralScaleRebinned.Integral(nJetBins*k + j,nJetBins*k + j + 1))
#            delta2 = MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j+1)/centralScaleRebinned.GetBinContent(nJetBins*k + j+1)
        #deltapTTotal = UncInPtBins5.GetBinContent(k+1);
        #print deltapTTotal
        total = sqrt(delta1**2 +  delta2**2)
        #UncInPtandNJets[0].SetBinContent(globalBin+1, deltapTTotal)
        UncInPtandNJets[1].SetBinContent(globalBin+1, delta1)
        UncInPtandNJets[2].SetBinContent(globalBin+1, delta2)
        UncInPtandNJets[3].SetBinContent(globalBin+1, total)
        UncInPtandNJets[1].GetXaxis().SetBinLabel(globalBin,pTJetstitles[globalBin-1])
        UncInPtandNJets[2].GetXaxis().SetBinLabel(globalBin,pTJetstitles[globalBin-1])

#Save the results
if CMS:fOut = TFile("MaxScaleVarJetsandPt_CMS.root",'recreate')
else: fOut = TFile("MaxScaleVarJetsandPt_centralSimoneFO.root",'recreate')
MaxScaleDeviationRebinned1.Write()

MaxScaleDeviationRebinned2.Write()
centralScaleRebinned.Write()
UncInPtandNJets[1].Write()
UncInPtandNJets[2].Write()
UncInPtandNJets[3].Write()
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
UncInPtandNJets[1].SetAxisRange(-0.15, 0.25, "Y");
UncInPtandNJets[1].SetYTitle("Relative QCD uncertainty")
UncInPtandNJets[2].SetLineWidth(3)
#UncInPtandNJets[2].SetLineStyle(kDashed)
UncInPtandNJets[3].SetLineWidth(2)
UncInPtandNJets[1].SetLineWidth(3)
UncInPtandNJets[1].Draw()
#UncInPtandNJets[0].SetLineWidth(3)
UncInPtandNJets[2].Draw("same")
UncInPtandNJets[3].SetLineColor(kGreen+3)
UncInPtandNJets[3].Draw("same")
#UncInPtandNJets[0].SetLineColor(kBlack)
#UncInPtandNJets[0].Draw("same")
leg = TLegend(0.55, 0.71, 0.85, 0.91);
leg.SetTextFont(42)
leg.SetTextSize(0.03)
#leg.AddEntry(UncInPtandNJets[0], "p_{T}^{V} bins uncertainty", "l");
leg.AddEntry(UncInPtandNJets[1], "#Delta_{FO}", "l");
leg.AddEntry(UncInPtandNJets[2], "#Delta_{resum}", "l");
leg.AddEntry(UncInPtandNJets[3], "#sqrt{#Delta_{FO}^{2} + #Delta_{resumm}^{2}}", "l");
leg.SetBorderSize(0);
leg.Draw('same');
cB.SetTickx(0); cB.SetTicky(0);
if CMS:cB.SaveAs("pTBinsJetsUnc_CMS.pdf")
else: cB.SaveAs("pTBinsJetsUnc_centralSimonelastFOResum.pdf")


#scaleTitlesGeneva = ["nominal","\mu_{FO} up", "\mu_{FO} down", "\mu_{resumm}^{1}","\mu_{resumm}^{1}","\mu_{resumm}^{2}","\mu_{resumm}^{2}","\mu_{resumm}^{3}","\mu_{resumm}^{3}","\mu_{overall} up","\mu_{overall} down"]

#_MYW = 800; _MYH = 600
#_MYT = 0.08*_MYH; _MYB = 0.14*_MYH;
#_MYL = 0.14*_MYW; _MYR = 0.18*_MYW
#cB=0;
#cB=TCanvas("cB","cB",_MYW,_MYH);
#cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
#cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
#centralScaleRebinned.SetLineColor(kRed)
#centralScaleRebinned.SetYTitle("Cross-section")
#centralScaleRebinned.SetAxisRange(0, 1.1*max(MAXVAL), "Y");
#centralScaleRebinned.SetLineWidth(3)
#centralScaleRebinned.Draw("")
#for i in range(0, NVar):
#    scaleVarsRebinned[i].SetLineColor(i+1)
#    #scaleVarsRebinned[i].SetLineWidth(2)
#    scaleVarsRebinned[i].Draw("same")
##leg = TLegend(0.5, 0.5, 0.7, 0.90);
#leg = TLegend(0.55, 0.4, 0.75, 0.90);
#leg.SetTextFont(42)
#leg.SetBorderSize(0)
#leg.SetTextSize(0.03)
#for i in range(0, NVar):
#    leg.AddEntry(scaleVarsRebinned[i], scaleTitlesGeneva[i], "l");
#leg.Draw('same');
#centralScaleRebinned.Draw("same")
#cB.SetTickx(0); cB.SetTicky(0);
#cB.SaveAs("XsectionpTJetsBinsUnc_Geneva_Relative.pdf");
#
#MAXVAL=[]
#for i in range(0,NVar):
#    MAXVAL.insert(i,scaleVarsRebinned[i].GetMaximum())
#
#
#_MYW = 800; _MYH = 600
#_MYT = 0.08*_MYH; _MYB = 0.14*_MYH;
#_MYL = 0.14*_MYW; _MYR = 0.18*_MYW
#cB=0;
#cB=TCanvas("cB","cB",_MYW,_MYH);
#cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
#cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
#centralScaleRebinned.SetLineColor(kRed)
#centralScaleRebinned.SetYTitle("Cross-section")
#centralScaleRebinned.SetAxisRange(0, 1.1*max(MAXVAL), "Y");
##centralScaleRebinned.SetLineWidth(3)
#centralScaleRebinned.Draw("e1")
#for i in range(0, NVar):
#    scaleVarsRebinned[i].SetLineColor(histcolors[i])
#    #scaleVarsRebinned[i].SetLineWidth(2)
#    scaleVarsRebinned[i].Draw(" e1 same")
##leg = TLegend(0.5, 0.5, 0.7, 0.90);
#leg = TLegend(0.55, 0.4, 0.75, 0.90);
#leg.SetTextFont(42)
#leg.SetBorderSize(0)
#leg.SetTextSize(0.04)
#for i in range(0, NVar):
#    leg.AddEntry(scaleVarsRebinned[i], scaleTitles[i], "l");
#leg.Draw('same');
#centralScaleRebinned.Draw("same")
#cB.SetTickx(0); cB.SetTicky(0);
#cB.SaveAs("XsectionpTJetsBinsUnc_Geneva.pdf");
#

scaleTitlesGeneva = ["nominal","\mu_{FO} up", "\mu_{FO} down", "\mu_{resumm}^{1} up","\mu_{resumm}^{1} down","\mu_{resumm}^{2} up","\mu_{resumm}^{2} down","\mu_{resumm}^{3} up","\mu_{resumm}^{3} down","\mu_{overall} up","\mu_{overall} down"]

_MYW = 800; _MYH = 600
_MYT = 0.08*_MYH; _MYB = 0.14*_MYH;
_MYL = 0.14*_MYW; _MYR = 0.18*_MYW
MAXVAL=[]
MINVAL=[]
for i in range(0,NVar):
    scaleVarsRebinnedDiff[i].Divide(centralScaleRebinned)
    MAXVAL.insert(i,scaleVarsRebinnedDiff[i].GetMaximum())
    MINVAL.insert(i,scaleVarsRebinnedDiff[i].GetMinimum())

cB=0;
cB=TCanvas("cB","cB",_MYW,_MYH);
cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
scaleVarsRebinnedDiff[0].SetLineColor(kGray)
scaleVarsRebinnedDiff[0].SetLineStyle(kDashed)
scaleVarsRebinnedDiff[0].SetYTitle("Relative variation")
scaleVarsRebinnedDiff[0].SetTitle("")
scaleVarsRebinnedDiff[0].SetAxisRange(-1.1*max(MAXVAL), 1.6*max(MAXVAL), "Y");
scaleVarsRebinnedDiff[0].SetLineWidth(3)
scaleVarsRebinnedDiff[0].Draw("")
for i in range(1, NVar):
    if i==9 or i==4:
        if i==4:scaleVarsRebinnedDiff[i].SetLineColor(38)
        else: scaleVarsRebinnedDiff[i].SetLineColor(28)
    else:scaleVarsRebinnedDiff[i].SetLineColor(i+1)
    scaleVarsRebinned[i].SetLineWidth(3)
    scaleVarsRebinnedDiff[i].Draw("same")
#leg = TLegend(0.5, 0.5, 0.7, 0.90);
leg = TLegend(0.55, 0.62, 0.75, 0.90);
leg.SetNColumns(2);
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)
leg.AddEntry(scaleVarsRebinnedDiff[0], scaleTitlesGeneva[0], "l");
leg.AddEntry(0, "", "");
for i in range(1, NVar):
    leg.AddEntry(scaleVarsRebinnedDiff[i], scaleTitlesGeneva[i], "l");
leg.Draw('same');
cB.SetTickx(0); cB.SetTicky(0);
cB.SaveAs("XsectionpTJetsBinsUnc_Geneva_Relative.pdf");

