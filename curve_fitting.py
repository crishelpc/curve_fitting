import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin_l_bfgs_b

class CurveFitting:
    def __init__(self, x_values, y_values):
        self.x_values = np.array(x_values)
        self.y_values = np.array(y_values)
        
    def error1(self, parameters):
        m, b = parameters
        
        norm1 = m * self.x_values + b
        error = np.sum(np.abs(norm1 - self.y_values))
        return error
    
    def error2(self, parameters):
        m, b = parameters
        
        norm1 = m * self.x_values + b
        error = np.sum(np.pow(norm1 - self.y_values, 2))
        return error
    
    def error3(self, parameters):
        m, b = parameters
        
        norm1 = m * self.x_values + b
        error = max(np.abs(norm1 - self.y_values))
        return error
    
    def optimize_norm1(self, initial_values):
        result = fmin_l_bfgs_b(
                self.error1, 
                x0=np.array(initial_values), 
                approx_grad=True  
            )
        
        self.norm1_m, self.norm1_b = result[0]
        self.norm1_val = self.norm1_m * self.x_values + self.norm1_b
        
    def optimize_norm2(self, initial_values):
        result = fmin_l_bfgs_b(
                self.error2, 
                x0=np.array(initial_values), 
                approx_grad=True  
            )
        
        self.norm2_m, self.norm2_b = result[0]
        self.norm2_val = self.norm2_m * self.x_values + self.norm2_b
        
    def optimize_norm3(self, initial_values):
        result = fmin_l_bfgs_b(
                self.error3, 
                x0=np.array(initial_values), 
                approx_grad=True  
            )
        
        self.norm3_m, self.norm3_b = result[0]
        self.norm3_val = self.norm3_m * self.x_values + self.norm3_b
        
        
if __name__ == "__main__":
    x = [0, 5, 8, 12, 16, 20, 23, 31]
    y = [3, 3, 5, 6, 15, 17, 11, 18]
    val1 = [1, 1]
    val2 = [2, 2]
    val3 = [3, 3]
    
    var = CurveFitting(x, y)
    var.optimize_norm1(val1)
    var.optimize_norm2(val2)
    var.optimize_norm3(val3)
    
    print(var.norm1_val)
    print(var.norm2_val)
    print(var.norm3_val)

    