
"""
Charles Walker 
CPSC 322
Section 02
PA2 
"""
import math 
import numpy as np
import importlib
import mypytable
import copy
importlib.reload(mypytable)
from mypytable import MyPyTable

def conv_num(mypy):
    mypy.convert_to_numeric
    pass

def get_column(table, header, col_name):
    col_index = header.index(col_name)
    col = []
    for row in table: 
        # ignore missing values ("NA")
        if row[col_index] != "NA":
            col.append(row[col_index])
    return col

def del_row(mypy, index):
    row = mypy.data[index]
    mypy.drop_rows([row])
    pass

def load_data(filename):
    mypytable = MyPyTable()
    mypytable.load_from_file(filename)
    return mypytable

# warmup task
def get_col(mypy, col_name):
    return mypy.get_column(col_name, False)

def get_min_max(values):
    return min(values), max(values)


def get_freq_str(mypy, col_name):
    
    col = get_col(mypy, col_name)
    header = [col_name]
    col_mypy = MyPyTable(header, col)

    dups = col_mypy.ordered_col(header)
    values = []
    counts = []

    for value in dups:
        if value not in values:
            # first time we have seen this value
            values.append(str(value))
            counts.append(1)
        else:
            # we have seen this value before 
            counts[-1] += 1 # ok because the list is sorted

    return values, counts

def group_by(mypy, col_name):
    col = get_col(mypy, col_name)
    col_index = mypy.column_names.index(col_name)
    
    # we need the unique values for our group by column
    group_names = sorted(list(set(col))) # e.g. 74, 75, 76, 77
    group_subtables = [[] for _ in group_names] # [[], [], [], []]
    
    # algorithm: walk through each row and assign it to the appropriate
    # subtable based on its group_by_col_name value
    for row in mypy.data:
        group_by_value = row[col_index]
        # which subtable to put this row in?
        group_index = group_names.index(group_by_value)
        group_subtables[group_index].append(row.copy()) # shallow copy
    
    return group_names, group_subtables

def compute_equal_width_cutoffs(values, num_bins):
    # first compute the range of the values
    values_range = max(values) - min(values)
    bin_width = values_range / num_bins 
    # bin_width is likely a float
    # if your application allows for ints, use them
    # we will use floats
    # np.arange() is like the built in range() but for floats
    cutoffs = list(np.arange(min(values), max(values), bin_width)) 
    cutoffs.append(max(values))
    # optionally: might want to round
    cutoffs = [round(cutoff, 2) for cutoff in cutoffs]
    return cutoffs 
    
def compute_bin_frequencies(values, cutoffs):
    freqs = [0 for _ in range(len(cutoffs) - 1)]

    for val in values:
        if val == max(values):
            freqs[-1] += 1
        else:
            for i in range(len(cutoffs) - 1):
                if cutoffs[i] <= val < cutoffs[i + 1]:
                    freqs[i] += 1

    return freqs
    

def compute_slope_intercept(x, y):
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    m = sum([(x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))])
    b = mean_y - m * mean_x
    return m, b 

def compute_corr_coef(x, y):
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    r = sum([(x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))]) / sum([((x[i] - mean_x)**2) * ((y[i] - mean_y)**2) for i in range(len(x))])
    return r

def compute_covar(x, y):
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    cov = sum([(x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))]) / len(x)
    return cov

def binary_freq(mypy, col_name):
    mypy.convert_to_numeric()
    col = get_col(mypy, col_name)
    freq = 0
    for i in range(len(col)):
        if col[i] == 1:
            freq += 1

    return col_name, freq

def percent_compare(mypy, col_names, total, get_sum=True):
    conv_num(mypy)
    percentages = []
    if get_sum == False:
        for i in range(len(col_names)):
            col = get_col(mypy, col_names[i])
            col2 = []
            for j in range(len(col)):
                if col[j] != 0:
                    col2.append(col[j])
            col_total = len(col2)
            prcnt = col_total / total
            percentages.append(prcnt)
    if get_sum == True:
        for i in range(len(col_names)):
            col = get_col(mypy, col_names[i])
            col_total = sum(col)
            prcnt = col_total / total
            percentages.append(prcnt)
    return col_names, percentages
