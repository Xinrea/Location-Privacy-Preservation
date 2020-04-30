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
        self.radius = range_radius(lat, lon)
        # k for adjust feature proportion

        self.feature = np.array([self.distance,self.radius])

    def __sub__(self, other):
        return np.sum(np.abs(self.feature-other.feature))

    def get_distance(self):
        return self.distance
    
    def get_radius(self):
        return self.radius
        
def range_radius(lat, lon):
    radius = 0
    points = []
    for i in range(len(lat)):
        p = np.array(lat[i],lon[i])
        points.append(p)
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            dis = np.linalg.norm(points[i]-points[j])
            if (dis > radius):
                radius = dis
    return radius

