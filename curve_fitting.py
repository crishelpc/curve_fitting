import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize


class CurveFitting:
    def __init__(self, x_values, y_values):
        self.x = x_values
        self.y = y_values
        self.result = []
        
    def first_norm(self):
        m = 1
        b = 1
        
        self.norm1 = []
        residuals = []
        
        for i in range(self.x):
            value = m * self.x[i] + b
            self.norm1.append(value)
            residual = abs(value - self.x[i])
            residuals.append(residual)
        
        residual_sum = sum(residual)
        return residual_sum
    
    def second_norm(self):
        m = 2
        b = 2
        
        self.norm2 = []
        residuals = []
        
        for i in range(self.x):
            value = m * self.x[i] + b
            self.norm2.append(value)
            residual = abs(value - self.x[i])
            residuals.append(residual)
        
        residual_sum = sum(residual)
        return residual_sum
    
    def infinity_norm(self):
        m = 3
        b = 3
        
        self.norm3 = []
        residuals = []
        
        for i in range(self.x):
            value = m * self.x[i] + b
            self.norm3.append(value)
            residual = abs(value - self.x[i])
            residuals.append(residual)
        
        residual_sum = max(residual)
        return residual_sum
    