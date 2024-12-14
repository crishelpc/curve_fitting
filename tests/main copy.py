import tkinter as tk
from tkinter import filedialog, messagebox, Text
import csv
from interpolation import interpolate_missing_values
from curve_fitting import CurveFitting
from curve_fitting_k import CurveFitting_k

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

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
        curve_fit_k = CurveFitting_k(x, y, guess_k)
        y_forecasted = curve_fit_k.forecast(forecasted_points)

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

        graph_curve_fitting_k(x, y, y_forecasted, forecasted_points)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

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

def graph_curve_fitting_k(x, y, y_forecasted, forecasted_points):
    plt.plot(x, y, 'bo-', label='Original Data')
    plt.plot(forecasted_points, y_forecasted, 'ro-', label='Forecasted Points')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Curve Fitting with k')
    plt.legend()
    plt.grid()
    plt.show()

def exit_program():
    root.destroy()

# Create main window
root = tk.Tk()
root.title("Interpolation and Curve Fitting Tool")
root.geometry("700x600")
root.configure(bg="#d4edda")

# Create and place buttons
label = tk.Label(root, text="Choose an Option", font=("Courier", 16, "bold"), bg="#d4edda")
label.pack(pady=10)

# btn_interpolation = tk.Button(root, text="Newton Divided-and-Difference Interpolation", command=handle_interpolation, width=45, bg="#c3e6cb", font=("Courier", 12, "bold"))
# btn_interpolation.pack(pady=5)

# btn_linear_regression = tk.Button(root, text="Linear Regression", command=handle_linear_regression, width=45, bg="#c3e6cb", font=("Courier", 12, "bold"))
# btn_linear_regression.pack(pady=5)

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
