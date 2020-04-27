import numpy as np
import pandas as pd
import overload_function
import time
from GridTrajectory import GridTrajectory
from Trajectory import Trajectory
from GowallaData import GowallaData
from TimeDistribution import TimeDistribution
from Grid import Grid
from Cell import Cell

def convertTrajToGridTraj(origDB, g:Grid, interp:bool, epsilon:float = None, unusedEpsilon:float = None):
    tbr = []
    if(epsilon == None):
        for t in origDB:
            tbr.append(GridTrajectory(t,ug,interp))
        return tbr
    for t in origDB:
        tbr.append(GridTrajectory(t,g,interp))
    cellDensities = {}
    for c in g.getCells():
        cellDensities[c] = 0
    for t in tbr:
        for c in t.getCells():
            cellDensities[c] = cellDensities[c]+1/len(t.getCells())
    ld = np.random.laplace(0,1/epsilon)
    for c in g.getCells():
        noisydensity = cellDensities[c]+ld
        if(noisydensity < 0.0010):
            noisydensity = 0
        cellDensities[c] = noisydensity
    for c in g.getCells():
        c.divideFurther(cellDensities[c],epsilon+unusedEpsilon,origDB)
    return tbr

def convertGridTrajToTraj(input,tb:TimeDistribution):
    tbr = []
    for t in input:
        out = Trajectory()
        cellsForConversion = t.getCells()
        for c in cellsForConversion:
            out.addPoint(c.sampleRandomPoint(tb.sample(cellsForConversion.index(c))))
        tbr.append(out)
    return tbr

def convertGowallaToTraj(gowalla:GowallaData):
    tbr = {}
    rawData = gowalla.getGowallaData()
    uidlist = gowalla.getUidlist()
    for u in uidlist:
        traj = []
        urawData = rawData.loc[rawData['uid'] == u]
        urawData = urawData.iloc[::-1]
        # 'uid','utc','lat','lon','lid'
        lastDay = None
        oneTraj = Trajectory()
        for i in range(len(urawData)):
            line = urawData.iloc[i]
            t = time.strptime(line['utc'],"%Y-%m-%dT%H:%M:%SZ")
            day = time.strftime("%Y-%m-%d",t)
            if(lastDay == None):
                lastDay = day
            # Points in the same day -> traj
            if(day == lastDay):
                oneTraj.addCoordinates(line['lat'],line['lon'],t)
            else:
                lastDay = day
                traj.append(oneTraj)
                oneTraj = Trajectory()
                oneTraj.addCoordinates(line['lat'],line['lon'],t)
        traj.append(oneTraj)
        tbr[u] = traj
    return tbr



if __name__ == "__main__":
    Gowalla = GowallaData()
    Gowalla.read_checkin_file('/home/Gowalla_sample.txt')
    originDB = convertGowallaToTraj(Gowalla)
    print(originDB[0][0].getSize())
    print(originDB[0][0].getDistanceTravelled())
    print(originDB[0][0].getDiameter())