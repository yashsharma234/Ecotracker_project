import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random, csv
# Optional: import cv2 for real QR detection
# import cv2

class EcoTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 EcoTracker - Carbon Footprint Tracker")
        self.root.geometry("980x680")
        self.root.config(bg="#f1faee")

        self.username = "Yash Sharma"
        self.data = {"Transport": 0, "Food": 0, "Energy": 0, "Clothing": 0, "Other": 0}
        self.create_widgets()

    def create_widgets(self):
        # App Title
        tk.Label(self.root, text="🌍 EcoTracker", font=("Helvetica", 26, "bold"), bg="#f1faee", fg="#2d6a4f").pack(pady=10)

        # Profile Panel
        profile_frame = tk.Frame(self.root, bg="#caf0f8", bd=2, relief="ridge")
        profile_frame.pack(fill=tk.X, padx=20)
        tk.Label(profile_frame, text=f"👤 User: {self.username}", font=("Arial", 14), bg="#caf0f8").pack(side=tk.LEFT, padx=20)
        self.medal_label = tk.Label(profile_frame, text="🏅 Medal: Bronze", font=("Arial", 14, "bold"), bg="#caf0f8", fg="brown")
        self.medal_label.pack(side=tk.RIGHT, padx=20)

        # Input Panel
        input_frame = tk.Frame(self.root, bg="#f1faee")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Category:", font=("Arial", 13), bg="#f1faee").grid(row=0, column=0, padx=5)
        self.category_var = ttk.Combobox(input_frame, values=list(self.data.keys()), font=("Arial", 12), state="readonly")
        self.category_var.set("Transport")
        self.category_var.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Emissions (kg CO2):", font=("Arial", 13), bg="#f1faee").grid(row=0, column=2, padx=5)
        self.emission_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.emission_entry.grid(row=0, column=3, padx=5)

        tk.Button(input_frame, text="➕ Add", font=("Arial", 12, "bold"), bg="#52b788", fg="white", command=self.add_emission).grid(row=0, column=4, padx=10)

        # Table
        self.tree = ttk.Treeview(self.root, columns=("Category", "Emissions"), show='headings')
        self.tree.heading("Category", text="Category")
        self.tree.heading("Emissions", text="Emissions (kg CO2)")
        self.tree.pack(pady=10)

        # Button Panel
        btn_frame = tk.Frame(self.root, bg="#f1faee")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="📊 Charts", font=("Arial", 12, "bold"), bg="#1b4332", fg="white", command=self.show_charts).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="📁 Export", font=("Arial", 12, "bold"), bg="#0077b6", fg="white", command=self.export_csv).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="♻ Reset", font=("Arial", 12, "bold"), bg="#d00000", fg="white", command=self.reset_data).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="📷 Scan QR", font=("Arial", 12, "bold"), bg="#ffb703", fg="black", command=self.scan_qr).grid(row=0, column=3, padx=10)

        self.total_label = tk.Label(self.root, text="Total Carbon Footprint: 0 kg CO2", font=("Arial", 14, "bold"), bg="#f1faee", fg="#2d6a4f")
        self.total_label.pack(pady=10)

    def add_emission(self, category=None, value=None):
        category = category or self.category_var.get()
        try:
            value = float(value) if value is not None else float(self.emission_entry.get())
            self.data[category] += value
            self.refresh_tree()
            if value is None:
                self.emission_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        total = 0
        for category, value in self.data.items():
            self.tree.insert("", tk.END, values=(category, round(value, 2)))
            total += value
        self.total_label.config(text=f"Total Carbon Footprint: {round(total, 2)} kg CO2")
        self.update_medal(total)

    def update_medal(self, total):
        if total <= 50:
            stage, color = "🥇 Gold", "green"
        elif total <= 100:
            stage, color = "🥈 Silver", "blue"
        else:
            stage, color = "🥉 Bronze", "brown"
        self.medal_label.config(text=f"🏅 Medal: {stage}", fg=color)

    def show_charts(self):
        categories = list(self.data.keys())
        values = list(self.data.values())
        fig, axs = plt.subplots(2, 3, figsize=(18, 8))
        fig.suptitle("Emission Visualization", fontsize=16)

        # Bar Chart
        axs[0, 0].bar(categories, values, color="#80ed99")
        axs[0, 0].set_title("Bar Chart")

        # Pie Chart
        axs[0, 1].pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
        axs[0, 1].set_title("Pie Chart")

        # Line Chart
        axs[0, 2].plot(categories, values, marker='o', linestyle='-', color="#2d6a4f")
        axs[0, 2].set_title("Line Chart")

        # Donut Chart
        axs[1, 0].pie(values, labels=categories, wedgeprops=dict(width=0.4), startangle=90, autopct='%1.1f%%')
        axs[1, 0].set_title("Donut Chart")

        # Stacked bar (simulated)
        axs[1, 1].bar(categories, [v*0.6 for v in values], color="#a8dadc", label="Base")
        axs[1, 1].bar(categories, [v*0.4 for v in values], bottom=[v*0.6 for v in values], color="#1d3557", label="Extra")
        axs[1, 1].set_title("Stacked Bar")
        axs[1, 1].legend()

        # Radar-style (Spider) Chart
        angles = [i / float(len(categories)) * 2 * 3.1415 for i in range(len(categories))]
        values += values[:1]
        angles += angles[:1]
        axs[1, 2] = plt.subplot(2, 3, 6, polar=True)
        axs[1, 2].plot(angles, values, color="purple", linewidth=2)
        axs[1, 2].fill(angles, values, color="violet", alpha=0.4)
        axs[1, 2].set_title("Spider Chart")
        axs[1, 2].set_xticks(angles[:-1])
        axs[1, 2].set_xticklabels(categories)

        chart_win = tk.Toplevel(self.root)
        chart_win.title("Charts View")
        chart_win.geometry("1200x700")

        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Category", "Emissions (kg CO2)"])
                for category, value in self.data.items():
                    writer.writerow([category, round(value, 2)])
            messagebox.showinfo("Success", "Data exported successfully!")

    def reset_data(self):
        if messagebox.askyesno("Confirm", "This will clear all emission data. Proceed?"):
            self.data = {key: 0 for key in self.data}
            self.refresh_tree()

    def scan_qr(self):
        # Simulate scanned data (mock real QR scan)
        fake_products = [
            ("Food", 1.7, "Organic Bread"),
            ("Transport", 2.5, "E-Scooter Ride"),
            ("Energy", 3.8, "Lightbulb Usage"),
            ("Clothing", 0.9, "Cotton Shirt"),
            ("Other", 1.2, "Household Items"),
        ]
        cat, value, product = random.choice(fake_products)
        msg = f"📦 Product: {product}\n📁 Category: {cat}\n🌫 Emission: {value} kg CO2"
        if messagebox.askyesno("QR Code Detected", f"{msg}\n\n➕ Add this to your record?"):
            self.add_emission(cat, value)

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = EcoTracker(root)
    root.mainloop()
