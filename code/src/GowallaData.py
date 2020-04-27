#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import scipy
import scipy.cluster.hierarchy as sch
from matplotlib import pyplot as plt

from Feature import UsrFeature

class GowallaData(object):
    def __init__(self):
        print('GowallaData Init')
        self.dfc = pd.DataFrame(index=[],columns=[])
        self.feature_map = {}
    
    def read_checkin_file(self, filename, items):
        print('Checkin Filename:',filename)
        self.dfc = pd.read_table(filename,header=None)
        self.dfc.columns = items
        return True
    
    def gen_feature(self):
        self.uid_list = self.dfc['uid'].unique()
        self.feature_list = []
        for i in self.uid_list:
            self.feature_map[i] = UsrFeature(self.dfc.loc[self.dfc['uid']==i])
            self.feature_list.append(self.feature_map[i].feature)

    def divide_user(self):
        disMat = sch.distance.pdist(self.feature_list,'cityblock')
        Z = sch.linkage(disMat,method='average')
        p = sch.dendrogram(Z)
        plt.savefig('t.png')
        kmember = 2
        init_num = len(self.uid_list)//kmember
        self.cluster_result = []
        while True:
            slef.cluster_result = sch.fcluster(Z,init_num,criterion='maxclust')
            if (CheckCluster(cluster_result,init_num,kmember)):
                break
            init_num = init_num - 1
        print(self.cluster_result)
        
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
    items_checkin = ['uid','utc','lat','lon','lid']
    gowalla.read_checkin_file(default_checkin_file, items_checkin)
    gowalla.gen_feature()
    gowalla.divide_user()

