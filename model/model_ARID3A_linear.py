
# coding: utf-8

# In[1]:

import numpy as np
from itertools import islice
import os
from sklearn.svm import SVC
from sklearn.cross_validation import LeaveOneLabelOut, cross_val_score
import time


# In[2]:

def merge_feature(input_files_list):
    x = []
    for i, file in enumerate(input_files_list): 
        with open(file) as f:
            if i ==0:
                for j, line in enumerate(f):
                    x.append([])
                    temp = line.rstrip(os.linesep)
                    temp = temp.split('\t')
                    temp = temp[3:]
                    x[j] = temp
            else:
                for j, line in enumerate(f):
                    temp = line.rstrip(os.linesep)
                    temp = temp.split('\t')
                    temp = temp[3:]
                    x[j].extend(temp)
            f.close()
    return x


# In[3]:

def read_label(file_name):
    y = []
    with open(file_name) as f:
        for line in islice(f,1,None):
            temp = line.rstrip(os.linesep)
            temp = temp.split('\t')
            temp = temp[-1]
            y.append(temp)
        f.close()
    return y


# In[4]:

def read_anno(file_name):
    anno = []
    with open(file_name) as f:
        for line in f:
            temp = line.rstrip(os.linesep)
            temp = temp.split('\t')
            temp[0] = temp[0].lstrip('chr')
            anno.append(temp)
        f.close()
    return anno


# In[5]:

input_files_dir = '../../data/features/'
input_files_list = [
    'train_shape_feature_HelT.bed',
    'train_shape_feature_MGW.bed',
    'train_shape_feature_ProT.bed',
    'train_shape_feature_Roll.bed',
    'HepG2.dnase.train.feature'
]
input_files_list = [input_files_dir + i for i in input_files_list]
x = merge_feature(input_files_list)
y = read_label('../../data/ChIPseq/label/ARID3A.train.labels.tsv')
anno = read_anno('../../data/annotations/train_regions.blacklistfiltered.bed')


# In[ ]:

y1 = ['B' if i =='B' else 'U' for i in y]
y2 = ['U' if i == 'U' else 'B' for i in y]


# In[ ]:

for i in range(len(x)):
    for j in range(len(x[i])):
        if x[i][j] == 'na':
            x[i][j] = np.nan
        else:
            x[i][j] = float(x[i][j])


# In[ ]:

x = np.array(x)
y1 = np.array(y1)
y2 = np.array(y2)
anno = np.array(anno)
not_nan = ~np.isnan(x).any(axis=1)
x_select = x[not_nan]
y1_select = y1[not_nan]
y2_select = y2[not_nan]
anno_select = anno[not_nan]


# In[ ]:

svc = SVC(kernel='linear')
start_time = time.time()
svc.fit(x_select, y1_select)
print("%s seconds" % (time.time() - start_time))


# In[ ]:

scores = cross_val_score(svc, x_select, y1_select,cv=LeaveOneLabelOut(anno_select[:,0]),
        scoring='f1_weighted')
print(np.mean(scores))


# In[ ]:

scores = cross_val_score(svc, x_select, y2_select,cv=LeaveOneLabelOut(anno_select[:,0]),
        scoring='f1_weighted')
print(np.mean(scores))

