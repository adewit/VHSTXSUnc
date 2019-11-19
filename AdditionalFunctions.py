#from ROOT import *
import ROOT
from ROOT import *
from math import sqrt
from math import *
from array import *
# qq -> WH
QQ2HLNU_FWDH = 300,
QQ2HLNU_PTV_0_75_0J = 301,
QQ2HLNU_PTV_75_150_0J = 302,
QQ2HLNU_PTV_150_250_0J = 303,
QQ2HLNU_PTV_250_400_0J = 304,
QQ2HLNU_PTV_GT400_0J = 305,
QQ2HLNU_PTV_0_75_1J = 306,
QQ2HLNU_PTV_75_150_1J = 307,
QQ2HLNU_PTV_150_250_1J = 308,
QQ2HLNU_PTV_250_400_1J = 309,
QQ2HLNU_PTV_GT400_1J = 310,
QQ2HLNU_PTV_0_75_GE2J = 311,
QQ2HLNU_PTV_75_150_GE2J = 312,
QQ2HLNU_PTV_150_250_GE2J = 313,
QQ2HLNU_PTV_250_400_GE2J = 314,
QQ2HLNU_PTV_GT400_GE2J = 315,
# qq -> ZH
QQ2HLL_FWDH = 400,
QQ2HLL_PTV_0_75_0J = 401,
QQ2HLL_PTV_75_150_0J = 402,
QQ2HLL_PTV_150_250_0J = 403,
QQ2HLL_PTV_250_400_0J = 404,
QQ2HLL_PTV_GT400_0J = 405,
QQ2HLL_PTV_0_75_1J = 406,
QQ2HLL_PTV_75_150_1J = 407,
QQ2HLL_PTV_150_250_1J = 408,
QQ2HLL_PTV_250_400_1J = 409,
QQ2HLL_PTV_GT400_1J = 410,
QQ2HLL_PTV_0_75_GE2J = 411,
QQ2HLL_PTV_75_150_GE2J = 412,
QQ2HLL_PTV_150_250_GE2J = 413,
QQ2HLL_PTV_250_400_GE2J = 414,
QQ2HLL_PTV_GT400_GE2J = 415,
# gg -> ZH
GG2HLL_FWDH = 500,
GG2HLL_PTV_0_75_0J = 501,
GG2HLL_PTV_75_150_0J = 502,
GG2HLL_PTV_150_250_0J = 503,
GG2HLL_PTV_250_400_0J = 504,
GG2HLL_PTV_GT400_0J = 505,
GG2HLL_PTV_0_75_1J = 506,
GG2HLL_PTV_75_150_1J = 507,
GG2HLL_PTV_150_250_1J = 508,
GG2HLL_PTV_250_400_1J = 509,
GG2HLL_PTV_GT400_1J = 510,
GG2HLL_PTV_0_75_GE2J = 511,
GG2HLL_PTV_75_150_GE2J = 512,
GG2HLL_PTV_150_250_GE2J = 513,
GG2HLL_PTV_250_400_GE2J = 514,
GG2HLL_PTV_GT400_GE2J = 515,

nJetBins = 3;
npTBins = 5
Stage1_1_FineZH = 63
Stage1_1_FineZHCMS = 0

pTJetstitles = ["FWD","0-75 GeV0J", "0-75 GeV1J","0-75 GeV0GE2J","75-150 GeV0J", "75-150 GeV1J","75-150 GeVGE2J","150-250 GeV0J", "150-250 GeV1J","150-250 GeVGE2J","250-400 GeV0J", "250-400 GeV1J","250-400 GeVGE2J",">400 GeV0J", ">400 GeV1J",">400 GeVGE2J"]
scaleTitles= ["#mu_{R}=1.0 & #mu_{F}=1.0","#mu_{R}=1.0 & #mu_{F}=2.0", "#mu_{R}=2.0 & #mu_{F}=1.0", "#mu_{R}=2.0 & #mu_{F}=2.0", "#mu_{R}=1.0 & #mu_{F}=0.5", "#mu_{R}=0.5 & #mu_{F}=1.0", "#mu_{R}=0.5 & #mu_{F}=0.5"]


def getBin(Stage1_1_Fine):
    array = [0,1,22,47,63,79,95,97,99,101]
    P = Stage1_1_Fine / 100
    F = Stage1_1_Fine % 100
    return F + array[P];

def GetInclpT(finehisto, hname):
    nBins = finehisto.GetNbinsX()
    nPtVbins = npTBins
    hist = TH1F(hname, hname, nPtVbins, 0, nPtVbins+1)
    N=0;
    for ib in range (Stage1_1_FineZH + 2,103):
        if N>=nPtVbins:return hist
        cont=-99.; iB = ib
        cont = finehisto.GetBinContent(iB) + finehisto.GetBinContent(iB+npTBins) + finehisto.GetBinContent(iB+2*npTBins)
        hist.SetBinContent(N+1, cont)
        N=N+1
    return hist

def GetInclpTCMS(finehisto, hname):
    nBins = finehisto.GetNbinsX()
    nPtVbins = npTBins
    hist = TH1F(hname, hname, nPtVbins, 0, nPtVbins+1)
    N=0;
    for k in range (0,npTBins):
        pTBinCont = 0;
        for i in range (0, nJetBins):
            OldBinNum = Stage1_1_FineZHCMS + 1 + nJetBins*k + i +1
            pTBinCont = pTBinCont + finehisto.GetBinContent(OldBinNum)
        NewBinNum = k + 1;
        hist.SetBinContent(NewBinNum, pTBinCont)
    return hist


def ReorganisedHist(finehisto, hname):
    hist = TH1F(hname, hname, nJetBins*npTBins, 0, nJetBins*npTBins)
    for k in range (0,npTBins):
        for i in range (0, nJetBins):
            OldBinNum = Stage1_1_FineZH + 1 + k + i*npTBins + 1
            NewBinNum = nJetBins*k + i +1
            hist.SetBinContent(NewBinNum, finehisto.GetBinContent(OldBinNum))
            hist.GetXaxis().SetBinLabel(NewBinNum, pTJetstitles[NewBinNum])
    return hist

def ReorganisedHistCMS(finehisto, hname):
    hist = TH1F(hname, hname, nJetBins*npTBins, 0, nJetBins*npTBins)
    for k in range (0,npTBins):
        for i in range (0, nJetBins):
            OldBinNum = Stage1_1_FineZHCMS + 1 + nJetBins*k + i +1
            NewBinNum = nJetBins*k + i +1
            hist.SetBinContent(NewBinNum, finehisto.GetBinContent(OldBinNum))
            hist.GetXaxis().SetBinLabel(NewBinNum, pTJetstitles[NewBinNum])
    return hist

