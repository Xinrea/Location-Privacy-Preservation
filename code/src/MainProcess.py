from GowallaData import GowallaData
from Synthesize import SynTraj
import Convertor
import time
import pandas as pd
import numpy as np
import Util
from typing import List
from Evaluation import Evaluation
from Grid import Grid
from third.KAnonymity import dls
from third.PLM.GI.protections.noise import PlanarLaplace
from LengthDistribution import LengthDistribution
from StartEndDistribution import StartEndDistribution
from TimeDistribution import TimeDistribution

def ConstructBlockDistribution(db,uidlist:List,cluster:List):
    interp = True
    cellCount = 6
    clusterDB = {}
    clusterDistribution = {}
    for i in range(len(uidlist)):
        c = cluster[i]
        d = db[uidlist[i]]
        if (c in clusterDB):
            clusterDB[c].extend(d)
        else:
            clusterDB[c] = d
    for c,d in clusterDB.items():
        boundaries = Util.getDataBoundaries(d)
        minX = boundaries[0]
        maxX = boundaries[1]
        minY = boundaries[2]
        maxY = boundaries[3]
        grid = Grid(cellCount, minX,maxX,minY,maxY)
        dbGrid = Convertor.convertTrajToGridTraj(d, grid, interp, 0.05, 0.95)
        ld = LengthDistribution(dbGrid,grid)
        sed = StartEndDistribution(dbGrid)
        td = TimeDistribution(d)
        clusterDistribution[c] = [ld,sed,td]
    return clusterDistribution



def DoProcess(infile,outfile,op):
    print("Process Start")
    Gowalla = GowallaData()
    Gowalla.read_checkin_file(infile)
    Gowalla.gen_feature()
    Gowalla.divide_user()
    ulist = Gowalla.getUidlist().tolist()
    cluster = Gowalla.getCluster()
    originDB = Convertor.convertGowallaToTraj(Gowalla)
    synDB = {}
    evalist = []
    # method 1
    time1 = time.time()
    bd = ConstructBlockDistribution(originDB,ulist,cluster)
    for uid,db in originDB.items():
        synDB[uid] = SynTraj(originDB[uid],1,op,bd[cluster[ulist.index(uid)]])
    time2 = time.time()
    cOriginDB = {}
    cSynDB = {}
    for i in range(len(ulist)):
        c = cluster[i]
        d = originDB[ulist[i]]
        sd = synDB[ulist[i]]
        if (c in cOriginDB):
            cOriginDB[c].extend(d)
            cSynDB[c].extend(sd)
        else:
            cOriginDB[c] = d
            cSynDB[c] = sd
    eva = np.array([0.0,0.0,0.0,0.0])
    cnt = 0
    for c,d in cOriginDB.items():
        eva += np.array(Evaluation(time2-time1,d, cSynDB[c]).toList())
        cnt += 1
    evalist.append((eva/cnt).tolist())

    # method 2
    time3 = time.time()
    kresult = K(Gowalla.getGowallaData())
    newG = GowallaData()
    newG.load_from_dfc(kresult)
    ksynDB = Convertor.convertGowallaToTraj(newG)
    time4 = time.time()
    cKSynDB = {}
    for i in range(len(ulist)):
        c = cluster[i]
        sd = ksynDB[ulist[i]]
        if (c in cKSynDB):
            cKSynDB[c].extend(sd)
        else:
            cKSynDB[c] = sd
    eva = np.array([0.0,0.0,0.0,0.0])
    cnt = 0
    for c,d in cOriginDB.items():
        eva += np.array(Evaluation(time4-time3,d, cKSynDB[c]).toList())
        cnt += 1
    evalist.append((eva/cnt).tolist())
    
    # method 3
    time5 = time.time()
    presult = PLM(Gowalla.getGowallaData())
    newG = GowallaData()
    newG.load_from_dfc(presult)
    psynDB = Convertor.convertGowallaToTraj(newG)
    psynAllDB = Convertor.convertDbToList(psynDB)
    time6 = time.time()
    cPSynDB = {}
    for i in range(len(ulist)):
        c = cluster[i]
        sd = psynDB[ulist[i]]
        if (c in cPSynDB):
            cPSynDB[c].extend(sd)
        else:
            cPSynDB[c] = sd
    eva = np.array([0.0,0.0,0.0,0.0])
    cnt = 0
    for c,d in cOriginDB.items():
        eva += np.array(Evaluation(time6-time5,d, cPSynDB[c]).toList())
        cnt += 1
    evalist.append((eva/cnt).tolist())

    Convertor.convertTrajToFile(synDB,outfile)
    evadfc = pd.DataFrame(evalist)
    evadfc.to_csv(outfile+'.result',index=False)
    print("Process Complete")

def K(kdfc:pd.DataFrame, k=5):
    dfc = kdfc.copy()
    return dls.dls_pure(dfc,k)

def PLM(pdfc:pd.DataFrame):
    dfc = pdfc.copy()
    for index,row in dfc.iterrows():
        pos = (row['lon'],row['lat'])
        npos = PlanarLaplace.perturbate(pos,0.5)
        dfc.iloc[index,2] = npos[0]
        dfc.iloc[index,3] = npos[1]
    return dfc

if __name__ == "__main__":
    DoProcess("/home/Gowalla_sample.txt","output.csv")
    