import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import csv

class EcoTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("EcoTracker - Personal Carbon Footprint Tracker")
        self.root.geometry("900x600")
        self.root.config(bg="#e6f2ec")

        self.data = {
            "Transport": 0,
            "Food": 0,
            "Energy": 0,
            "Clothing": 0,
            "Other": 0
        }

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="🌍 EcoTracker", font=("Helvetica", 24, "bold"), bg="#e6f2ec", fg="#2d6a4f")
        title.pack(pady=20)

        frame = tk.Frame(self.root, bg="#e6f2ec")
        frame.pack(pady=10)

        tk.Label(frame, text="Category:", font=("Arial", 14), bg="#e6f2ec").grid(row=0, column=0, padx=5, pady=5)
        self.category_var = ttk.Combobox(frame, values=list(self.data.keys()), font=("Arial", 12), state="readonly")
        self.category_var.set("Transport")
        self.category_var.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Emissions (kg CO2):", font=("Arial", 14), bg="#e6f2ec").grid(row=0, column=2, padx=5, pady=5)
        self.emission_entry = tk.Entry(frame, font=("Arial", 12))
        self.emission_entry.grid(row=0, column=3, padx=5, pady=5)

        add_btn = tk.Button(frame, text="Add Entry", font=("Arial", 12, "bold"), bg="#40916c", fg="white", command=self.add_emission)
        add_btn.grid(row=0, column=4, padx=10, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Category", "Emissions"), show='headings')
        self.tree.heading("Category", text="Category")
        self.tree.heading("Emissions", text="Emissions (kg CO2)")
        self.tree.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#e6f2ec")
        btn_frame.pack(pady=10)

        chart_btn = tk.Button(btn_frame, text="📊 Show Charts", font=("Arial", 12, "bold"), bg="#1b4332", fg="white", command=self.show_charts)
        chart_btn.grid(row=0, column=0, padx=10)

        export_btn = tk.Button(btn_frame, text="📄 Export to CSV", font=("Arial", 12, "bold"), bg="#0077b6", fg="white", command=self.export_csv)
        export_btn.grid(row=0, column=1, padx=10)

        reset_btn = tk.Button(btn_frame, text="♻ Reset Data", font=("Arial", 12, "bold"), bg="#d00000", fg="white", command=self.reset_data)
        reset_btn.grid(row=0, column=2, padx=10)

        self.total_label = tk.Label(self.root, text="Total Carbon Footprint: 0 kg CO2", font=("Arial", 14, "bold"), bg="#e6f2ec", fg="#2d6a4f")
        self.total_label.pack(pady=10)

    def add_emission(self):
        category = self.category_var.get()
        try:
            value = float(self.emission_entry.get())
            self.data[category] += value
            self.refresh_tree()
            self.emission_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for emissions.")

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        total = 0
        for category, emission in self.data.items():
            self.tree.insert("", tk.END, values=(category, round(emission, 2)))
            total += emission
        self.total_label.config(text=f"Total Carbon Footprint: {round(total, 2)} kg CO2")

    def show_charts(self):
        fig, axs = plt.subplots(1, 3, figsize=(16, 4))
        categories = list(self.data.keys())
        emissions = list(self.data.values())

        # Bar Chart
        axs[0].bar(categories, emissions, color="#52b788")
        axs[0].set_title("Bar Chart")
        axs[0].set_ylabel("kg CO2")

        # Pie Chart
        axs[1].pie(emissions, labels=categories, autopct='%1.1f%%', startangle=140)
        axs[1].set_title("Pie Chart")

        # Line Chart
        axs[2].plot(categories, emissions, marker='o', linestyle='-', color="#2d6a4f")
        axs[2].set_title("Line Chart")
        axs[2].set_ylabel("kg CO2")

        chart_win = tk.Toplevel(self.root)
        chart_win.title("Emission Charts")
        chart_win.geometry("1000x400")

        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Category", "Emissions (kg CO2)"])
                    for category, emission in self.data.items():
                        writer.writerow([category, round(emission, 2)])
                messagebox.showinfo("Export Successful", "Data exported to CSV successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

    def reset_data(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to clear all data?"):
            for key in self.data:
                self.data[key] = 0
            self.refresh_tree()
            messagebox.showinfo("Data Reset", "All data has been reset.")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = EcoTracker(root)
    root.mainloop()
