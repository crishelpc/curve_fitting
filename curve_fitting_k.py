import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin_l_bfgs_b

class CurveFitting_k:
    def __init__(self, x_values, y_values):
        self.x_values = np.array(x_values)
        self.y_values = np.array(y_values)
        
    def error2(self, parameters):
        m, b = parameters
        norm1 = m * self.x_values + b
        error = np.sum(np.pow(norm1 - self.y_values, 2))
        return error
    
    def optimize_norm2(self, initial_values):
        result = fmin_l_bfgs_b(
                self.error2, 
                x0=np.array(initial_values), 
                approx_grad=True  
            )
        
        self.norm2_m, self.norm2_b = result[0]
        self.norm2_val = self.norm2_m * self.x_values + self.norm2_b
        
    def forecast(self, k):
        max_x = max(self.x_values)
        forecast_x = np.arange(max_x + 1, max_x + k + 1)
        forecast_y = self.norm2_m * forecast_x + self.norm2_b
        return forecast_x, forecast_y

if __name__ == "__main__":
    x = [0, 5, 8, 12, 16, 20, 23, 31]
    y = [3, 3, 5, 6, 15, 17, 11, 18]
    val2 = [2, 2]
    
    var = CurveFitting_k(x, y)
    var.optimize_norm2(val2)
    
    k = 7
    forecast_x, forecast_y = var.forecast(k)
    
    plt.scatter(x, y, label="Original Data")
    plt.plot(x, y)
    plt.scatter(forecast_x, forecast_y, label="Forcasted Data")
    plt.plot(forecast_x, forecast_y)
    plt.plot(var.x_values, var.norm2_val, color="green", label="Fitted Line")
    plt.legend()
    plt.title("Linear Regression with Forecast")
    plt.show()
