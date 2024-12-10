import tkinter as tk
from tkinter import filedialog, messagebox, Text
import csv
from interpolation import interpolate_missing_values
from curve_fitting import CurveFitting

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
        x = [int(val) if val.is_integer() else val for val in x]
        y = [int(val) if val and val.is_integer() else val for val in y]

        # Interpolate missing values
        y_interpolated = interpolate_missing_values(x, y)

        # Insert the dataset into the dataset box
        dataset_box.config(state=tk.NORMAL)
        dataset_box.delete(1.0, tk.END)
        dataset_box.insert(tk.END, "Dataset:\n")
        dataset_box.insert(tk.END, f"x = {x}\n")
        dataset_box.insert(tk.END, f"y = {y}\n")
        dataset_box.config(state=tk.DISABLED)

        # Insert the result into the result box
        result_box.config(state=tk.NORMAL)
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "Result:\n")
        result_box.insert(tk.END, f"x = {x}\n")
        result_box.insert(tk.END, f"y (interpolated) = {y_interpolated}")
        result_box.config(state=tk.DISABLED)

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

        # Perform curve fitting
        curve_fit = CurveFitting(x, y)
        res1 = curve_fit.first_norm()
        res2 = curve_fit.second_norm()
        res3 = curve_fit.infinity_norm()

        # Insert the dataset into the dataset box
        dataset_box.config(state=tk.NORMAL)
        dataset_box.delete(1.0, tk.END)
        dataset_box.insert(tk.END, "Dataset:\n")
        dataset_box.insert(tk.END, f"x = {x}\n")
        dataset_box.insert(tk.END, f"y = {y}\n")
        dataset_box.config(state=tk.DISABLED)

        # Insert the result into the result box
        result_box.config(state=tk.NORMAL)
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "Result:\n")
        result_box.insert(tk.END, f"First Norm Residual Sum: {res1}\n")
        result_box.insert(tk.END, f"Second Norm Residual Sum: {res2}\n")
        result_box.insert(tk.END, f"Infinity Norm Residual Sum: {res3}")
        result_box.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def exit_program():
    root.destroy()

# Create main window
root = tk.Tk()
root.title("Interpolation and Linear Regression Tool")
root.geometry("700x500")
root.configure(bg="#d4edda")  

# Create and place buttons
label = tk.Label(root, text="Choose an Option", font=("Courier", 16, "bold"), bg="#d4edda", fg="#000000")  
label.pack(pady=10)

btn_interpolation = tk.Button(root, text="Newton Divided-and-Difference Interpolation", command=handle_interpolation, width=45, bg="#c3e6cb", fg="#000000", font=("Courier", 12, "bold"))
btn_interpolation.pack(pady=5)

btn_linear_regression = tk.Button(root, text="Linear Regression", command=handle_linear_regression, width=45, bg="#c3e6cb", fg="#000000", font=("Courier", 12, "bold"))
btn_linear_regression.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=exit_program, width=45, bg="#c3e6cb", fg="#000000", font=("Courier", 12, "bold"))
btn_exit.pack(pady=5)

# Create and place the dataset text box
dataset_box = Text(root, wrap=tk.WORD, font=("Courier", 12, "bold"), height=8, width=70, bg="#f8f9fa", fg="#000000")
dataset_box.pack(expand=True, fill=tk.BOTH, pady=5)
dataset_box.config(state=tk.DISABLED)

# Create and place the result text box
result_box = Text(root, wrap=tk.WORD, font=("Courier", 12, "bold"), height=8, width=70, bg="#f8f9fa", fg="#000000")
result_box.pack(expand=True, fill=tk.BOTH, pady=5)
result_box.config(state=tk.DISABLED)

root.mainloop()
