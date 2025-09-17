import os
import json
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExpenseTracker:
    DATA_DIR = r"C:\Users\25G500010\Projects\Expense Tracker"
    JSON_FILENAME = "expenses.json"

    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x550")
        self.root.minsize(500, 500)

        # Set modern font and colors
        self.font = ("Segoe UI", 11)
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)

        # Ensure data directory exists
        os.makedirs(self.DATA_DIR, exist_ok=True)

        # Load data from JSON file or create empty DataFrame
        json_path = os.path.join(self.DATA_DIR, self.JSON_FILENAME)
        self.df = self.load_data(json_path)

        # Predefined categories
        self.category_options = ["Food", "Transportation", "Entertainment", "Utilities", "Rent", "Others"]

        # Initialize budgets dictionary
        self.budgets = {}

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 'clam' is clean and modern
        self.style.configure('TLabel', font=self.font, background=self.bg_color)
        self.style.configure('TButton', font=self.font, padding=6)
        self.style.configure('TEntry', font=self.font)
        self.style.configure('TCombobox', font=self.font)

        self.create_widgets()

    def load_data(self, path):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return pd.DataFrame(data)
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load data from JSON.\nError: {str(e)}")
                return pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
        else:
            return pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

    def create_widgets(self):
        padding_opts = {'padx': 10, 'pady': 8}

        # Main frame with padding and background color
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Configure grid weights for responsiveness
        main_frame.columnconfigure(1, weight=1)

        # Date
        ttk.Label(main_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W, **padding_opts)
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(main_frame, textvariable=self.date_var)
        self.date_entry.grid(row=0, column=1, sticky=tk.EW, **padding_opts)

        # Amount
        ttk.Label(main_frame, text="Amount ($):").grid(row=1, column=0, sticky=tk.W, **padding_opts)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(main_frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=1, column=1, sticky=tk.EW, **padding_opts)

        # Category
        ttk.Label(main_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, **padding_opts)
        self.selected_category = tk.StringVar()
        self.category_combobox = ttk.Combobox(main_frame, textvariable=self.selected_category, state="readonly")
        self.category_combobox['values'] = self.category_options
        self.category_combobox.current(0)
        self.category_combobox.grid(row=2, column=1, sticky=tk.EW, **padding_opts)

        # Description
        ttk.Label(main_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, **padding_opts)
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(main_frame, textvariable=self.description_var)
        self.description_entry.grid(row=3, column=1, sticky=tk.EW, **padding_opts)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky=tk.EW)
        button_frame.columnconfigure((0,1,2,3), weight=1)

        self.submit_button = ttk.Button(button_frame, text="Add Expense", command=self.add_expense)
        self.submit_button.grid(row=0, column=0, padx=5, sticky=tk.EW)

        self.show_button = ttk.Button(button_frame, text="Show Summary", command=self.show_summary)
        self.show_button.grid(row=0, column=1, padx=5, sticky=tk.EW)

        self.visualize_button = ttk.Button(button_frame, text="Visualize Spending", command=self.visualize_expenses)
        self.visualize_button.grid(row=0, column=2, padx=5, sticky=tk.EW)

        self.budget_button = ttk.Button(button_frame, text="Set Budget", command=self.set_budget)
        self.budget_button.grid(row=0, column=3, padx=5, sticky=tk.EW)

        # Status bar at bottom
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to Expense Tracker!")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, font=("Segoe UI", 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def add_expense(self):
        date = self.date_var.get().strip()
        amount = self.amount_var.get().strip()
        category = self.selected_category.get()
        description = self.description_var.get().strip()

        # Basic validation
        if not date or not amount or not category:
            messagebox.showerror("Input Error", "Please fill in all required fields (Date, Amount, Category).")
            return

        # Validate date format (simple check)
        if not self.validate_date_format(date):
            messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a positive number.")
            return

        new_expense = pd.DataFrame({
            "Date": [date],
            "Amount": [amount],
            "Category": [category],
            "Description": [description]
        })

        new_expense = new_expense.reindex(columns=self.df.columns)

        self.df = pd.concat([self.df, new_expense], ignore_index=True)

        self.save_data()

        self.status_var.set(f"Added expense: {category} - ${amount:.2f} on {date}")

        messagebox.showinfo("Success", "Expense added successfully!")

        self.clear_inputs()

    def validate_date_format(self, date_str):
        # Simple YYYY-MM-DD format check
        import re
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        return re.match(pattern, date_str) is not None

    def show_summary(self):
        if self.df.empty:
            messagebox.showinfo("Summary", "No expenses to summarize.")
            return

        summary = self.df.groupby("Category")["Amount"].sum().reset_index()
        summary = summary.sort_values(by="Amount", ascending=False)

        summary_window = tk.Toplevel(self.root)
        summary_window.title("Expense Summary")
        summary_window.geometry("350x350")
        summary_window.minsize(300, 300)

        # Use a Treeview for better tabular display
        tree = ttk.Treeview(summary_window, columns=("Category", "Total Amount"), show='headings', height=15)
        tree.heading("Category", text="Category")
        tree.heading("Total Amount", text="Total Amount ($)")
        tree.column("Category", anchor=tk.W, width=150)
        tree.column("Total Amount", anchor=tk.E, width=150)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for _, row in summary.iterrows():
            tree.insert("", tk.END, values=(row['Category'], f"${row['Amount']:.2f}"))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(summary_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def visualize_expenses(self):
        if self.df.empty:
            messagebox.showwarning("No Data", "No expenses to visualize.")
            return

        category_summary = self.df.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots(figsize=(6,6))
        ax.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
        ax.axis('equal')
        ax.set_title("Spending by Category", fontsize=16)

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Spending Visualization")
        chart_window.geometry("700x700")
        chart_window.minsize(600, 600)

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def save_data(self):
        json_path = os.path.join(self.DATA_DIR, self.JSON_FILENAME)
        try:
            data_records = self.df.to_dict(orient='records')
            with open(json_path, 'w', encoding='utf-8') as json_file:
                json.dump(data_records, json_file, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data.\nError: {str(e)}")

    def set_budget(self):
        def save_budget():
            category = category_var.get().strip()
            budget = budget_var.get().strip()
            if not category or not budget:
                messagebox.showerror("Input Error", "Please fill in both fields.")
                return
            if category not in self.category_options:
                messagebox.showerror("Input Error", f"Category must be one of: {', '.join(self.category_options)}")
                return
            try:
                budget_val = float(budget)
                if budget_val <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Budget must be a positive number.")
                return
            self.budgets[category] = budget_val
            messagebox.showinfo("Budget Set", f"Budget for {category} set to ${budget_val:.2f}.")
            budget_window.destroy()

        budget_window = tk.Toplevel(self.root)
        budget_window.title("Set Budget")
        budget_window.geometry("320x180")
        budget_window.minsize(300, 180)
        budget_window.grab_set()

        padding_opts = {'padx': 15, 'pady': 10}

        ttk.Label(budget_window, text="Category:", font=self.font).pack(anchor=tk.W, **padding_opts)
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(budget_window, textvariable=category_var, state="readonly", values=self.category_options)
        category_combobox.current(0)
        category_combobox.pack(fill=tk.X, **padding_opts)

        ttk.Label(budget_window, text="Budget Amount ($):", font=self.font).pack(anchor=tk.W, **padding_opts)
        budget_var = tk.StringVar()
        budget_entry = ttk.Entry(budget_window, textvariable=budget_var, font=self.font)
        budget_entry.pack(fill=tk.X, **padding_opts)

        save_button = ttk.Button(budget_window, text="Save Budget", command=save_budget)
        save_button.pack(pady=10)

    def clear_inputs(self):
        self.date_var.set("")
        self.amount_var.set("")
        self.description_var.set("")
        self.category_combobox.current(0)
        self.date_entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
