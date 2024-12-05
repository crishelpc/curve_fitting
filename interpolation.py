import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline, BSpline
import csv 

# Function to calculate product term
def proterm(i, value, x):
    pro = 1
    for j in range(i):
        pro *= (value - x[j])
    return pro

# Function to calculate divided difference table
def dividedDiffTable(x, y, n):
    diff_table = np.zeros((n, n))
    diff_table[:, 0] = y 

    for i in range(1, n):
        for j in range(n - i):
            diff_table[j, i] = (
                (diff_table[j + 1, i - 1] - diff_table[j, i - 1])
                / (x[j + i] - x[j])
            )
    return diff_table

# Function to apply Newton's Divided-Difference formula
def applyFormula(value, x, diff_table, n):
    result = diff_table[0, 0]
    for i in range(1, n):
        result += proterm(i, value, x) * diff_table[0, i]
    return result

# Function to interpolate missing values
def interpolate_missing_values(x, y):
    n = len(x)
    known_indices = [i for i in range(n) if not pd.isnull(y[i])]
    x_known = [x[i] for i in known_indices]
    y_known = [y[i] for i in known_indices]

    #Calculate divided difference table 
    diff_table = dividedDiffTable(x_known, y_known, len(x_known))
    
    # Interpolate missing values
    for i in range(n):
        if pd.isnull(y[i]):
            y[i] = int(round(applyFormula(x[i], x_known, diff_table, len(x_known))))
    return y