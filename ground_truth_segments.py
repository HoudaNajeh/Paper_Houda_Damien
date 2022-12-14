# author: houda.najeh@imt-atlantique.fr
""
" ----Import Librairies ----"
""
import numpy as np
import pandas as pd
import re
from datetime import datetime
import matplotlib.pyplot as plt
import time
import pylab
import statistics
""
" read the real dataset"
""
df = pd.read_csv("Aruba_raw_data.csv",  delimiter=";", header=None, on_bad_lines='skip',engine='python')
df = df[0:1500]
datetimes, sensor, value, activity = df[0], df[1], df[2], df[3]
def indices_begin_end(df):
    " This function determines the indexes of begin and end for each activity"
    indices_begin, indices_fin = list(), list()
    for i in range(len(df)):
        if activity[i] == 'Sleeping'+'_begin' or activity[i] == 'Bed_to_Toilet'+'_begin' or activity[i] == 'Work' + '_begin' or activity[i] == 'Eating'+'_begin' or activity[i] == 'Housekeeping'+'_begin' or activity[i] == 'Enter_Home'+'_begin' or activity[i] == 'Leave_Home'+'_begin' or activity[i] == 'Meal_Preparation'+'_begin' or activity[i] == 'Wash_Dishes'+'_begin' or activity[i] == 'Relax'+'_begin':
            indices_begin.append(i)
        if activity[i] == 'Sleeping' + '_end' or activity[i] == 'Bed_to_Toilet'+'_end' or activity[i] == 'Work' + '_end' or activity[i] == 'Eating'+'_end' or activity[i] == 'Housekeeping'+'_end' or activity[i] == 'Enter_Home'+'_end' or activity[i] == 'Leave_Home'+'_end' or activity[i] == 'Meal_Preparation'+'_end' or activity[i] == 'Wash_Dishes'+'_end' or activity[i] == 'Relax'+'_end':
            indices_fin.append(i)
    return indices_begin, indices_fin
print(indices_begin_end(df))

def intervalles(begins, ends):
    " This function creates the interval from the index of begin and end"
    intervs = list()
    for i in range(len(begins)):
        #interv = [begins[i], ends[i]]
        #intervs.append(interv)
        interv = list(range(begins[i], ends[i]))
        intervs.append(interv)
    print('intervalles=', intervs)
    return intervs
begins = indices_begin_end(df)[0]
ends = indices_begin_end(df)[1]
intervals = intervalles(begins[0:len(ends)], ends)
print('intervalles=', intervals)

""

""
def slices(L):
    " This function determine the slices between intervals "
    m = list()
    my_slices = list()
    for i in range(len(L)-1):
        print('i=', i)
        start, end = L[i][0], L[i][-1]
        print('start=', start)
        print('end=', end)
        s = L[i]+L[i+1]
        m.append(s)
        res = sorted(set(range(s[0], s[-1] + 1)).difference(s))
        print(res)
        my_slices.append(res)
        print('my_slices=', my_slices)
    return my_slices

print(' ---- Test 2 ----')
I = intervals
print('slices_I=', slices(intervals))
print('interval+slices=', I+slices(intervals))
print('sorted_interval+slices=', np.sort(I+slices(I)))

def the_gound_truth_segments(df):
    datetimes = df[0]
    begins = indices_begin_end(df)[0]
    ends = indices_begin_end(df)[1]
    intervals = intervalles(begins[0:len(ends)], ends)
    k = np.sort(intervals+slices(intervals))
    ground_truth_segments = list()
    for i in range(len(k)):
        start_index = k[i][0]
        end_index = k[i][-1]
        print('a=', (start_index, end_index))
        print('a=', (datetimes[start_index], datetimes[end_index]))
        kk = (start_index, end_index)
        aa = start_index
        bb = end_index
        ground_truth_segment = (datetime.strptime(datetimes[aa], '%Y-%m-%d %H:%M:%S.%f'), datetime.strptime(datetimes[bb], '%Y-%m-%d %H:%M:%S.%f'))
        print('ground_truth_segment=', ground_truth_segment)
        ground_truth_segments.append(ground_truth_segment)
    return ground_truth_segments

real_segments = the_gound_truth_segments(df)
print('real_segments=', real_segments)
ground_truth_segments = {
        'ground_truth_segments': real_segments,
      }
df_ground_truth_segments = pd.DataFrame(data=ground_truth_segments)
df_ground_truth_segments.to_csv('ground_truth_segments.csv', index=False)


