import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Configure Serial Communication
port = "COM5"  # Replace with your port
baud_rate = 9600

try:
    ser = serial.Serial(port, baud_rate, timeout=1)
    print(f"Connected to {port}")
except serial.SerialException as e:
    print(f"Error connecting to {port}: {e}")
    ser = None

# Initialize Data
x_data, y_data, z_data, time_data = [], [], [], []

# Function to Read Data from Serial Port
def read_serial_data():
    if ser and ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("x=") and "y=" in line and "z=" in line:
            try:
                x_val = int(line.split("x=")[1].split("y=")[0].strip())
                y_val = int(line.split("y=")[1].split("z=")[0].strip())
                z_val = int(line.split("z=")[1].strip())
                return x_val, y_val, z_val
            except ValueError:
                return None
    return None

# Live Graph Update Function
def update_graph(frame):
    data = read_serial_data()
    if data:
        x, y, z = data
        time_data.append(len(time_data))  # Incremental time
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)

        # Update Graph
        ax.clear()
        ax.plot(time_data, x_data, label="X-axis", color="blue")
        ax.plot(time_data, y_data, label="Y-axis", color="green")
        ax.plot(time_data, z_data, label="Z-axis", color="red")
        ax.legend(loc="upper left")
        ax.set_title("Live Sensor Data")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.grid()

# Save Graph as Image
def save_graph():
    if len(time_data) > 0:
        filename = f"sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        fig.savefig(filename, dpi=300)
        messagebox.showinfo("Save Successful", f"Graph saved as {filename}")
    else:
        messagebox.showwarning("Save Error", "No data to save!")

# Start Live Graph
def start_live_graph():
    ani.event_source.start()

# Stop Live Graph
def stop_live_graph():
    ani.event_source.stop()

# Create Tkinter GUI
root = tk.Tk()
root.title("ESP Sensor Data Graph")

# Matplotlib Figure
fig, ax = plt.subplots(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

start_button = ttk.Button(button_frame, text="Live Graph", command=start_live_graph)
start_button.grid(row=0, column=0, padx=10)

stop_button = ttk.Button(button_frame, text="Stop", command=stop_live_graph)
stop_button.grid(row=0, column=1, padx=10)

save_button = ttk.Button(button_frame, text="Save as Image", command=save_graph)
save_button.grid(row=0, column=2, padx=10)

# Start Animation
ani = animation.FuncAnimation(fig, update_graph, interval=100)

# Run Tkinter Mainloop
root.mainloop()
