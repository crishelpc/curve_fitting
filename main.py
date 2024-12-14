import tkinter as tk
from tkinter import filedialog, messagebox, Text
import csv
from interpolation import interpolate_missing_values
from curve_fitting import CurveFitting
from curve_fitting_k import CurveFitting_k

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline 

def handle_interpolation():
    file_path = filedialog.askopenfilename(title="Select Dataset", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Extract x and y values correctly
        x = [float(row[0]) for row in data[1:]]
        y = [float(row[1]) if row[1].lower() != 'none' else None for row in data[1:]]

        # Remove .0 for whole numbers from x and y values
        x_val = [int(val) if val.is_integer() else val for val in x]
        y_val = [int(val) if val and val.is_integer() else val for val in y]

        # Insert the dataset into the dataset box
        dataset_box.config(state=tk.NORMAL)
        dataset_box.delete(1.0, tk.END)
        dataset_box.insert(tk.END, "Dataset:\n")
        dataset_box.insert(tk.END, f"x = {x_val}\n")
        dataset_box.insert(tk.END, f"y = {y_val}\n")
        dataset_box.config(state=tk.DISABLED)

        # Interpolate missing values
        y_interpolated = interpolate_missing_values(x_val, y_val)

        # Insert the result into the result box
        result_box.config(state=tk.NORMAL)
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "Result (Interpolated):\n")
        result_box.insert(tk.END, f"x = {x_val}\n")
        result_box.insert(tk.END, f"y = {y_interpolated}")
        result_box.config(state=tk.DISABLED)
                
        graph_interpolation(x, y, y_interpolated)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def handle_linear_regression():
    file_path = filedialog.askopenfilename(title="Select Dataset", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Extract x and y values
        x = [float(row[0]) for row in data[1:]]
        y = [float(row[1]) for row in data[1:]]

        # Remove .0 for whole numbers from x and y values
        x = [int(val) if val.is_integer() else val for val in x]
        y = [int(val) if val.is_integer() else val for val in y]

        # Prompt for tree guessing values
        guess_values = get_three_guess_values()
        if guess_values is None:
            return  # User cancelled input

        # Perform curve fitting
        curve_fit = CurveFitting(x, y)
        curve_fit.optimize_norm1(guess_values[0])
        curve_fit.optimize_norm2(guess_values[1])
        curve_fit.optimize_norm3(guess_values[2])
        
        res1 = curve_fit.norm1_val
        res2 = curve_fit.norm2_val
        res3 = curve_fit.norm3_val

        # Insert the dataset into the dataset box
        dataset_box.config(state=tk.NORMAL)
        dataset_box.delete(1.0, tk.END)
        dataset_box.insert(tk.END, "Dataset:\n")
        dataset_box.insert(tk.END, f"x = {x}\n")
        dataset_box.insert(tk.END, f"y = {y}\n")
        
        dataset_box.insert(tk.END, "Guess Values:\n")
        for i in range(3):
            dataset_box.insert(tk.END, f"{i+1}. m: {guess_values[i][0]}\tb: {guess_values[i][1]}\n")
        
        dataset_box.config(state=tk.DISABLED)

        # Insert the result into the result box
        result_box.config(state=tk.NORMAL)
        result_box.delete(1.0, tk.END)
        
        # Insert header
        result_box.insert(tk.END, "Result (Optimized):\n")

        # Norm 1 Values
        result_box.insert(tk.END, "Norm 1 Values:\n")
        for val in res1:
            result_box.insert(tk.END, f"{round(float(val), 4)}\t")
        result_box.insert(tk.END, "\n\n")  # Add a newline for separation

        # Norm 2 Values
        result_box.insert(tk.END, "Norm 2 Values:\n")
        for val in res2:
            result_box.insert(tk.END, f"{round(float(val), 4)}\t")
        result_box.insert(tk.END, "\n\n")  # Add a newline for separation

        # Infinity Norm Values
        result_box.insert(tk.END, "Infinity Norm Values:\n")
        for val in res3:
            result_box.insert(tk.END, f"{round(float(val), 4)}\t")
        result_box.insert(tk.END, "\n\n")  # Add a newline for separation

        # Three Guessing Values
        result_box.insert(tk.END, "Three Guessing Values:\n")
        for i in range(1, 4):
            m_value = round(float(getattr(curve_fit, f'norm{i}_m')), 4)
            b_value = round(float(getattr(curve_fit, f'norm{i}_b')), 4)
            result_box.insert(tk.END, f"{i}. m: {m_value}\tb: {b_value}\n")

        # Disable the result box to prevent editing
        result_box.config(state=tk.DISABLED)
        
        graph_cf(x, y, res1, res2, res3)
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        
def handle_curve_fitting_k():
    file_path = filedialog.askopenfilename(title="Select Dataset", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Extract x and y values
        x = [float(row[0]) for row in data[1:]]
        y = [float(row[1]) for row in data[1:]]

        # Remove .0 for whole numbers from x and y values
        x = [int(val) if val.is_integer() else val for val in x]
        y = [int(val) if val.is_integer() else val for val in y]

        # Prompt for k value and forecasted points
        guess_k, forecasted_points = get_k_and_forecast_values()
        if guess_k is None or forecasted_points is None:
            return  # User cancelled input

        # Perform curve fitting with k
        curve_fit_k = CurveFitting_k(x, y)
        curve_fit_k.optimize_norm2(forecasted_points)
        norm2_val = curve_fit_k.norm2_val
        x_forecasted, y_forecasted = curve_fit_k.forecast(guess_k)

        # Insert the dataset into the dataset box
        dataset_box.config(state=tk.NORMAL)
        dataset_box.delete(1.0, tk.END)
        dataset_box.insert(tk.END, "Dataset:\n")
        dataset_box.insert(tk.END, f"x = {x}\n")
        dataset_box.insert(tk.END, f"y = {y}\n")
        dataset_box.insert(tk.END, f"k value: {guess_k}\n")
        dataset_box.insert(tk.END, f"Forecasted Points: {forecasted_points}\n")
        dataset_box.config(state=tk.DISABLED)

        # Insert the result into the result box
        result_box.config(state=tk.NORMAL)
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "Result (Curve Fitting with k):\n")
        result_box.insert(tk.END, f"Forecasted y values: {y_forecasted}\n")
        result_box.config(state=tk.DISABLED)

        graph_curve_fitting_k(x, y, x_forecasted, y_forecasted, norm2_val)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def get_three_guess_values():
    guess_window = tk.Toplevel(root)
    guess_window.title("Enter Three Guessing Value Pairs")
    guess_window.geometry("400x300")
    guess_window.configure(bg="#d4edda")

    tk.Label(
        guess_window,
        text="Enter three pairs of guess values (format: 'value1,value2'):",
        font=("Courier", 12, "bold"),
        bg="#d4edda",
        fg="#000000",
    ).pack(pady=10)

    entries = []
    for i in range(3):
        entry = tk.Entry(guess_window, font=("Courier", 12), width=30)
        entry.pack(pady=5)
        entries.append(entry)

    def submit():
        try:
            values = []
            for entry in entries:
                pair = entry.get().split(",")  # Split by comma
                if len(pair) != 2:
                    raise ValueError("Each input must contain exactly two values separated by a comma.")
                values.append([float(pair[0]), float(pair[1])])  # Convert to a list of floats
            guess_window.destroy()
            guess_window.quit()
            nonlocal result_values
            result_values = values
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    result_values = None
    submit_button = tk.Button(
        guess_window,
        text="Submit",
        command=submit,
        bg="#c3e6cb",
        fg="#000000",
        font=("Courier", 12, "bold"),
    )
    submit_button.pack(pady=10)

    guess_window.mainloop()
    return result_values

def get_k_and_forecast_values():
    input_window = tk.Toplevel(root)
    input_window.title("Enter k Value and Forecast Points")
    input_window.geometry("400x200")
    input_window.configure(bg="#d4edda")

    tk.Label(input_window, text="Enter k value:", font=("Courier", 12, "bold"), bg="#d4edda").pack(pady=5)
    k_entry = tk.Entry(input_window, font=("Courier", 12), width=30)
    k_entry.pack(pady=5)

    tk.Label(input_window, text="Enter forecasted points (comma-separated):", font=("Courier", 12, "bold"), bg="#d4edda").pack(pady=5)
    forecast_entry = tk.Entry(input_window, font=("Courier", 12), width=30)
    forecast_entry.pack(pady=5)

    def submit():
        try:
            k_value = float(k_entry.get())
            forecast_points = list(map(float, forecast_entry.get().split(',')))
            input_window.destroy()
            input_window.quit()
            nonlocal k_result, forecast_result
            k_result = k_value
            forecast_result = forecast_points
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    k_result = None
    forecast_result = None
    submit_button = tk.Button(input_window, text="Submit", command=submit, bg="#c3e6cb", font=("Courier", 12, "bold"))
    submit_button.pack(pady=10)

    input_window.mainloop()
    return k_result, forecast_result

def graph_curve_fitting_k(x, y, x_forecasted, y_forecasted, norm2):
    plt.plot(x, y, 'bo-', label='Original Data')
    plt.plot(x, norm2, 'bo-', label='Norm 2 Data')
    plt.plot(x_forecasted, y_forecasted, 'ro-', label='Forecasted Points')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Curve Fitting with k')
    plt.legend()
    plt.grid()
    plt.show()
        

def graph_cf(x, y, norm1, norm2, norm3):
    x = np.array(x)
    y = np.array(y)
    xnew = np.linspace(x.min(), x.max(), 100) 
    gfg1 = make_interp_spline(x, y, k=2) 
    ynew = gfg1(xnew) 

    gfg2 = make_interp_spline(x, norm1, k=2) 
    n1new = gfg2(xnew) 

    gfg3 = make_interp_spline(x, norm2, k=2) 
    n2new = gfg3(xnew) 

    gfg4 = make_interp_spline(x, norm3, k=2) 
    n3new = gfg4(xnew) 

    plt.plot(xnew, ynew, label='Base Data')
    plt.plot(xnew, n1new, label='Norm 1')
    plt.plot(xnew, n2new, label='Norm 2')
    plt.plot(xnew, n3new, label='Norm 3')
    plt.legend()
    plt.show()
    
    
def graph_interpolation(x, y, b):
    x = np.array(x)
    b = np.array(b)
    
    # Filter out None values
    a = np.array([x[i] for i in range(len(x)) if y[i] is not None])
    y = np.array([val for val in y if val is not None])
    
    # Interpolation
    anew = np.linspace(a.min(), a.max(), 100)
    xnew = np.linspace(x.min(), x.max(), 100)
    
    gfg1 = make_interp_spline(a, y, k=2)
    ynew = gfg1(anew)
    
    gfg2 = make_interp_spline(x, b, k=2)
    bnew = gfg2(xnew)
    
    # Plot
    plt.plot(anew, ynew, label='Filtered Data')
    plt.plot(xnew, bnew, label='Resampled Data')
    plt.legend()
    plt.show()

def exit_program():
    root.destroy()

# Create main window
root = tk.Tk()
root.title("Interpolation and Linear Regression Tool")
root.geometry("700x600")
root.configure(bg="#d4edda")

# Create and place buttons
label = tk.Label(root, text="Choose an Option", font=("Courier", 16, "bold"), bg="#d4edda")
label.pack(pady=10)

btn_interpolation = tk.Button(root, text="Newton Divided-and-Difference Interpolation", command=handle_interpolation, width=45, bg="#c3e6cb", font=("Courier", 12, "bold"))
btn_interpolation.pack(pady=5)

btn_linear_regression = tk.Button(root, text="Linear Regression", command=handle_linear_regression, width=45, bg="#c3e6cb", font=("Courier", 12, "bold"))
btn_linear_regression.pack(pady=5)

btn_curve_fitting_k = tk.Button(root, text="Curve Fitting (k)", command=handle_curve_fitting_k, width=45, bg="#c3e6cb", font=("Courier", 12, "bold"))
btn_curve_fitting_k.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=exit_program, width=45, bg="#c3e6cb", font=("Courier", 12, "bold"))
btn_exit.pack(pady=5)

# Create and place the dataset text box
dataset_box = Text(root, wrap=tk.WORD, font=("Courier", 12, "bold"), height=8, width=70, bg="#f8f9fa")
dataset_box.pack(expand=True, fill=tk.BOTH, pady=5)
dataset_box.config(state=tk.DISABLED)

# Create and place the result text box
result_box = Text(root, wrap=tk.WORD, font=("Courier", 12, "bold"), height=8, width=70, bg="#f8f9fa")
result_box.pack(expand=True, fill=tk.BOTH, pady=5)
result_box.config(state=tk.DISABLED)


root.mainloop()
