# Location Privacy Preserving (待定)

# 面向特征的位置数据隐私保护

### 课题内容

1. 分析位置数据中多种特征之间的相关性，如：位置访问频率向量、共同访问位置、频繁访问位置等，根据一种或者多种特征的相似性，对位置数据进行社区划分，设计社区划分方法在划分社区之后，对满足一定特征相似度的社区进行合并，以满足社区内位置数据保持一定数量k的要求； 
2. 根据一种或者多种特征的的相似性，对社区内的位置数据进行扰动，使得社区内的位置数据具备相同的一种或者多种特征，不同社区的特征相似度差异较大，从而更好地保护位置数据中的特征； 
3. 设计一数据发布系统，该系统包含多种隐私保护算法，如至少还应包括K-匿名，差分隐私等。可以根据用户的需求，选择适当的扰动算法，当选择特征扰动时，可对需要保护的特征进行扰动。同时在若干数据可用性评价指标上满足保持数据的可用性，可进行多种扰动方法的对比。

### 课题任务要求

分析位置数据中多种特征之间的相关性，设计一种对位置数据进行扰动的方法，弱化特征或者特征之间的相关性，从而保护位置数据的隐私。同时设计一个简单的数据发布平台，可以根据用户的需求，选择不同的隐私保护方法，对位置数据进行扰动后发布。

### 主要参考文献
1. 熊平, 朱天清, 王晓峰. 差分隐私保护及其应用. 计算机学报, 2014, 37(1): 101~122   
2. Location Privacy Preservation for Mobile Users in Location-Based Services，GANG SUN , SHUAI CAI, HONGFANG YU, SABITA MAHARJAN, VICTOR CHANG, XIAOJIANG DU, AND MOHSEN GUIZANI，IEEE ACCESS，vol 7, 2019, pp. 87425-78438.   
3. Gedik, B. and L. Liu, A customizable k-anonymity model for protecting location privacy. Georgia Institute of Technology, 2004, 8(1):31~42

### 相关记录

2020/01/01 ~ 2020/01/06 基础参考文献阅读