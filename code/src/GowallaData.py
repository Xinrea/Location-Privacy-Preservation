#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

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
        uid_list = self.dfc['uid'].unique()
        for i in uid_list:
            self.feature_map[i] = UsrFeature(self.dfc.loc[self.dfc['uid']==i])
        print(self.feature_map)
        

if __name__ == '__main__':
    # Process Checkin Data
    gowalla = GowallaData()
    default_checkin_file = '/home/xinrea/location-privacy/Location-Privacy-Preservation/datasets/Gowalla_sample.txt'
    items_checkin = ['uid','utc','lat','lon','lid']
    gowalla.read_checkin_file(default_checkin_file, items_checkin)
    gowalla.gen_feature()

