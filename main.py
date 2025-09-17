import tkinter as tk
from tkinter import ttk
from ExpenseTracker import ExpenseTracker

class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Expense Tracker")
        self.root.geometry("400x250")
        self.root.minsize(300, 200)
        self.root.configure(bg="#f0f0f0")

        # Allow window resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Set font and style
        self.font = ("Segoe UI", 12)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=self.font, padding=8)

        self.create_widgets()

    def create_widgets(self):
        # Main frame to hold all widgets, fills the window and is responsive
        main_frame = ttk.Frame(self.root)
        main_frame.grid(sticky="NSEW", padx=20, pady=20)

        # Configure grid weights for responsiveness
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # Description label row
        main_frame.rowconfigure(2, weight=1)  # Buttons frame row

        # Welcome label
        welcome_label = ttk.Label(main_frame, text="Welcome to Expense Tracker",
                                  font=("Segoe UI", 16, "bold"), background="#f0f0f0")
        welcome_label.grid(row=0, column=0, sticky="N", pady=(0, 10))

        # Description label
        desc_label = ttk.Label(main_frame, text="Track your expenses easily and efficiently.",
                               font=self.font, background="#f0f0f0", wraplength=360, justify="center")
        desc_label.grid(row=1, column=0, sticky="NSEW", pady=(0, 20))

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky="EW")

        # Configure button frame columns for equal button widths
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Open Expense Tracker button
        open_button = ttk.Button(button_frame, text="Open Expense Tracker",
                                 command=self.open_expense_tracker)
        open_button.grid(row=0, column=0, padx=5, sticky="EW")

        # Exit button
        exit_button = ttk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_button.grid(row=0, column=1, padx=5, sticky="EW")

    def open_expense_tracker(self):
        # Hide the main page window
        self.root.withdraw()

        # Create a new Toplevel window for ExpenseTracker
        expense_window = tk.Toplevel(self.root)
        app = ExpenseTracker(expense_window)

        # When ExpenseTracker window is closed, show main page again
        def on_close():
            expense_window.destroy()
            self.root.deiconify()

        expense_window.protocol("WM_DELETE_WINDOW", on_close)


def main():
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
