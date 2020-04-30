#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import scipy
import time
import scipy.cluster.hierarchy as sch
from matplotlib import pyplot as plt

from Feature import UsrFeature

class GowallaData(object):
    def __init__(self):
        self.dfc = pd.DataFrame(index=[],columns=[])
        self.feature_map = {}
    
    def read_checkin_file(self, filename, items = ['uid','utc','lat','lon','lid']):
        print('Checkin Filename:',filename)
        self.dfc = pd.read_table(filename,header=None)
        self.dfc.columns = items
        self.uid_list = self.dfc['uid'].unique()

    def load_from_dfc(self,dfc,items = ['uid','utc','lat','lon','lid']):
        self.dfc = dfc
        self.dfc.columns = items
        self.uid_list = self.dfc['uid'].unique()
    
    def getGowallaData(self):
        return self.dfc
    
    def getUidlist(self):
        return self.uid_list

    def getCluster(self):
        return self.cluster_result
    
    def gen_feature(self):
        self.feature_list = []
        for i in self.uid_list:
            self.feature_map[i] = UsrFeature(self.dfc.loc[self.dfc['uid']==i])
            self.feature_list.append(self.feature_map[i].feature)

    def divide_user(self):
        disMat = sch.distance.pdist(self.feature_list,'cityblock')
        Z = sch.linkage(disMat,method='average')
        kmember = 10
        init_num = len(self.uid_list)# kmember
        self.cluster_result = []
        while True:
            self.cluster_result = sch.fcluster(Z,init_num,criterion='maxclust')
            if (CheckCluster(self.cluster_result,init_num,kmember)):
                break
            init_num = init_num - 1
        
def CheckCluster(result, number, k):
    r = list(result)
    fail_count = 0
    for i in range(1,number+1):
        if (r.count(i) < k):
            fail_count = fail_count + 1
        if (fail_count/number > 0.2):
            return False
    return True

if __name__ == '__main__':
    # Process Checkin Data
    gowalla = GowallaData()
    default_checkin_file = '/home/xinrea/location-privacy/Location-Privacy-Preservation/datasets/Gowalla20w.txt'
    gowalla.read_checkin_file(default_checkin_file)
    gowalla.gen_feature()
    gowalla.divide_user()

