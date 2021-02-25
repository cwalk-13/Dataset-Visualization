# TODO: your reusable general-purpose functions here
import math 
import numpy as np
import importlib
import mypytable
importlib.reload(mypytable)
from mypytable import MyPyTable

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

def group_by(table, header, group_by_col_name):
    col = get_column(table, header, group_by_col_name)
    col_index = header.index(group_by_col_name)
    
    # we need the unique values for our group by column
    group_names = sorted(list(set(col))) # e.g. 74, 75, 76, 77
    group_subtables = [[] for _ in group_names] # [[], [], [], []]
    
    # algorithm: walk through each row and assign it to the appropriate
    # subtable based on its group_by_col_name value
    for row in table:
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
    pass

def dummy_function2():
    pass
