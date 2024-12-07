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
        
        for i in range(len(self.x)):
            value = m * self.x[i] + b
            self.norm1.append(value)
            residual = abs(value - self.y[i])
            residuals.append(residual)
        
        residual_sum = sum(residuals)
        return residual_sum
    
    def second_norm(self):
        m = 2
        b = 2
        
        self.norm2 = []
        residuals = []
        
        for i in range(len(self.x)):
            value = m * self.x[i] + b
            self.norm2.append(value)
            residual = (value - self.y[i])**2
            residuals.append(residual)
        
        residual_sum = round((sum(residuals))**(1/2), 4)
        return residual_sum
    
    def infinity_norm(self):
        m = 3
        b = 3
        
        self.norm3 = []
        residuals = []
        
        for i in range(len(self.x)):
            value = m * self.x[i] + b
            self.norm3.append(value)
            residual = abs(value - self.y[i])
            residuals.append(residual)
        
        residual_sum = max(residuals)
        return residual_sum

if __name__ == "__main__":
    x = [0, 5, 8, 12, 16, 20, 23, 31]
    y = [3, 3, 5, 6, 15, 17, 11, 18]
    
    var = CurveFitting(x, y)
    res1 = var.first_norm()
    res2 = var.second_norm()
    res3 = var.infinity_norm()

    print(var.norm1)
    print(res1)
    print(var.norm2)
    print(res2)
    print(var.norm3)
    print(res3)
    