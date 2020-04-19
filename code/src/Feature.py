#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class UsrFeature(object):
    def __init__(self, usrData):
        # Need To Reset The Index, Or The Index Couldn't Begin From 0
        lat = usrData['lat'].reset_index(drop=True)
        lon = usrData['lon'].reset_index(drop=True)
        # Move Distance
        self.distance = 0
        for i in range(len(usrData)):
            if i != 0:
                p1 = np.array([lat[i-1],lon[i-1]])
                p2 = np.array([lat[i],lon[i]])
                self.distance += np.linalg.norm(p1-p2)
        
        # Move Range Radius
        self.radius = range_radius(usrData)

    def get_distance(self):
        return self.distance
    
    def get_radius(self):
        return self.radius
        


def range_radius(usrData):
    points = usrData[['lat','lon']]
    return 0

