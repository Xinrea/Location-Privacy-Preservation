# Location Privacy Preservation

# 面向特征的位置数据隐私保护

### 课题内容

1. 分析位置数据中多种特征之间的相关性，如：位置访问频率向量、共同访问位置、频繁访问位置等，根据一种或者多种特征的相似性，对位置数据进行社区划分，设计社区划分方法在划分社区之后，对满足一定特征相似度的社区进行合并，以满足社区内位置数据保持一定数量k的要求； 
2. 根据一种或者多种特征的的相似性，对社区内的位置数据进行扰动，使得社区内的位置数据具备相同的一种或者多种特征，不同社区的特征相似度差异较大，从而更好地保护位置数据中的特征； 
3. 设计一数据发布系统，该系统包含多种隐私保护算法，如至少还应包括K-匿名，差分隐私等。可以根据用户的需求，选择适当的扰动算法，当选择特征扰动时，可对需要保护的特征进行扰动。同时在若干数据可用性评价指标上满足保持数据的可用性，可进行多种扰动方法的对比。

### 课题任务要求

分析位置数据中多种特征之间的相关性，设计一种对位置数据进行扰动的方法，弱化特征或者特征之间的相关性，从而保护位置数据的隐私。同时设计一个简单的数据发布平台，可以根据用户的需求，选择不同的隐私保护方法，对位置数据进行扰动后发布。

### 测试数据

Gowalla is a location-based social networking website where users share their locations by checking-in. The friendship network is undirected and was collected using their public API, and consists of 196,591 nodes and 950,327 edges. We have collected a total of 6,442,890 check-ins of these users over the period of Feb. 2009 - Oct. 2010.

```
Dataset Sample
[user]	[check-in time]		[latitude]	[longitude]	[location id]
196514  2010-07-24T13:45:06Z    53.3648119      -2.2723465833   145064
196514  2010-07-24T13:44:58Z    53.360511233    -2.276369017    1275991
196514  2010-07-24T13:44:46Z    53.3653895945   -2.2754087046   376497
196514  2010-07-24T13:44:38Z    53.3663709833   -2.2700764333   98503
196514  2010-07-24T13:44:26Z    53.3674087524   -2.2783813477   1043431
196514  2010-07-24T13:44:08Z    53.3675663377   -2.278631763    881734
196514  2010-07-24T13:43:18Z    53.3679640626   -2.2792943689   207763
196514  2010-07-24T13:41:10Z    53.364905       -2.270824       1042822	
```

```
Dataset statistics
Nodes	196591
Edges	950327
Nodes in largest WCC	196591 (1.000)
Edges in largest WCC	950327 (1.000)
Nodes in largest SCC	196591 (1.000)
Edges in largest SCC	950327 (1.000)
Average clustering coefficient	0.2367
Number of triangles	2273138
Fraction of closed triangles	0.007952
Diameter (longest shortest path)	14
90-percentile effective diameter	5.7
Check-ins	6,442,890
```

http://snap.stanford.edu/data/

http://networkrepository.com/loc-gowalla-edges.php

### 主要参考文献

1. 熊平, 朱天清, 王晓峰. 差分隐私保护及其应用. 计算机学报, 2014, 37(1): 101~122   
2. Location Privacy Preservation for Mobile Users in Location-Based Services，GANG SUN , SHUAI CAI, HONGFANG YU, SABITA MAHARJAN, VICTOR CHANG, XIAOJIANG DU, AND MOHSEN GUIZANI，IEEE ACCESS，vol 7, 2019, pp. 87425-78438.   
3. Gedik, B. and L. Liu, A customizable k-anonymity model for protecting location privacy. Georgia Institute of Technology, 2004, 8(1):31~42
4. 卢小丹, 张乐峰, 熊平. 位置隐私保护技术研究综述[J]. 计算机科学与应用, 2016, 6(6): 354-367.
Mehmet Emre Gursoy, Ling Liu, Stacey Truex, Lei Yu, and Wenqi Wei. 2018. Utility-Aware Synthesis of Differentially Private and Attack-Resilient Location Traces. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security (CCS ’18). Association for Computing Machinery, New York, NY, USA, 196–211. DOI:https://doi.org/10.1145/3243734.3243741
5. Salvatore Scellato, Anastasios Noulas, and Cecilia Mascolo. 2011. Exploiting place features in link prediction on location-based social networks. In Proceedings of the 17th ACM SIGKDD international conference on Knowledge discovery and data mining (KDD ’11). Association for Computing Machinery, New York, NY, USA, 1046–1054. DOI:https://doi.org/10.1145/2020408.2020575

### 进展记录

#### 第一周

参考找到的数据集处理样例，在进行数据预处理，提取特征；主要是对于python数据处理不是很熟悉，因此在边参考学习边写；接着要尽快熟悉python的数据处理，实现特征提取，然后据此尝试社区划分的效果