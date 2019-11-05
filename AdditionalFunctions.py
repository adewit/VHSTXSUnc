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

def getBin(Stage1_1_Fine):
    array = [0,1,22,47,63,79,95,97,99,101]
    P = Stage1_1_Fine / 100
    F = Stage1_1_Fine % 100
    return F + array[P];

def GetInclpT(finehisto, hname):
    nBins = finehisto.GetNbinsX()
    print nBins;
    nPtVbins = 5
    hist = TH1F(hname, hname, nPtVbins, 0, nPtVbins+1)
    N=0;
    for ib in range (0,71):
        if (finehisto.GetBinCenter(ib)<64):continue;
        cont=-99.; iB = ib
        cont = finehisto.GetBinContent(iB) + finehisto.GetBinContent(iB+5) + finehisto.GetBinContent(iB+10)
        print ib, finehisto.GetBinCenter(ib), cont, N
        hist.SetBinContent(N+1, cont)
        N=N+1
        if N>=nPtVbins:return hist
    return hist


