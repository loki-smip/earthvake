@echo off
REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python...
    REM Download Python installer (replace URL with the latest Python version URL if necessary)
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
    echo Installing Python...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
)

REM Verify Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python installation failed. Please install Python manually.
    pause
    exit /b
)

echo Python is installed.

REM Create project directory
echo Creating project directory...
mkdir my_project
cd my_project

REM Set up a virtual environment
echo Setting up virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Virtual environment setup failed. Please check your Python installation.
    pause
    exit /b
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Create the requirements.txt file
echo requests==2.28.1 > requirements.txt
echo zeroconf==0.39.0 >> requirements.txt
echo matplotlib==3.7.1 >> requirements.txt

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Please check your internet connection or package names.
    pause
    exit /b
)

REM Create the Python script
echo Generating Python script...
(
echo import tkinter as tk
echo from tkinter import ttk
echo import requests
echo import json
echo import time
echo from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
echo from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
echo from matplotlib.figure import Figure
echo.
echo class MyListener(ServiceListener):
echo     def __init__(self):
echo         self.service_name = None
echo.
echo     def add_service(self, zeroconf, service_type, name):
echo         self.service_name = name
echo         print(f"Service discovered: %name%")
echo.
echo     def resolve_service(self, zeroconf, service_type, name):
echo         info = zeroconf.get_service_info(service_type, name)
echo         if info:
echo             self.service_ip = f"{info.server[:-1]}:{info.port}"
echo.
echo zeroconf = Zeroconf()
echo listener = MyListener()
echo browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
echo.
echo print("Searching for ESP32...")
echo while not hasattr(listener, "service_ip"):
echo     time.sleep(1)
echo ESP32_IP = f"http://{listener.service_ip}"
echo print(f"ESP32 found at %ESP32_IP%")
echo.
echo time_data = []
echo magnitude_data = []
echo rating_data = []
echo.
echo def fetch_data():
echo     try:
echo         response = requests.get(f"%ESP32_IP%/data", timeout=1)
echo         if response.status_code == 200:
echo             data = response.json()
echo             update_gui(data)
echo     except Exception as e:
echo         status_label.config(text="Error: Could not fetch data", foreground="red")
echo.
echo def update_gui(data):
echo     global time_data, magnitude_data, rating_data
echo.
echo     magnitude = data.get("magnitude", 0)
echo     rating = data.get("rating", 1)
echo     level = data.get("level", "Normal")
echo.
echo     magnitude_label.config(text=f"Current Magnitude: {magnitude:.2f}")
echo     level_label.config(text=f"Earthquake Level: {level}")
echo     rating_label.config(text=f"%rating%")
echo     status_label.config(text="Connected to ESP32", foreground="green")
echo.
echo     time_data.append(time.time())
echo     magnitude_data.append(magnitude)
echo     rating_data.append(rating)
echo.
echo     if len(time_data) > 100:
echo         time_data.pop(0)
echo         magnitude_data.pop(0)
echo         rating_data.pop(0)
echo.
echo     ax.clear()
echo     ax.plot(time_data, magnitude_data, label="Magnitude")
echo     ax.set_title("Real-Time Earthquake Magnitude")
echo     ax.set_xlabel("Time")
echo     ax.set_ylabel("Magnitude")
echo     ax.legend()
echo     canvas.draw()
echo.
echo def update_data():
echo     fetch_data()
echo     root.after(1000, update_data)
echo.
echo root = tk.Tk()
echo root.title("Earthquake Monitor (ADXL345)")
echo.
echo magnitude_label = ttk.Label(root, text="Current Magnitude: 0.00", font=("Arial", 16))
echo magnitude_label.pack(pady=10)
echo level_label = ttk.Label(root, text="Earthquake Level: Normal", font=("Arial", 16))
echo level_label.pack(pady=10)
echo rating_frame = tk.Frame(root, bg="white", relief=tk.RAISED, borderwidth=2)
echo rating_frame.place(x=700, y=10, width=80, height=50)
echo rating_label = tk.Label(rating_frame, text="1", font=("Arial", 24), bg="white")
echo rating_label.pack(expand=True)
echo status_label = ttk.Label(root, text="Connecting to ESP32...", font=("Arial", 12))
echo status_label.pack(pady=5)
echo.
echo fig = Figure(figsize=(8, 4), dpi=100)
echo ax = fig.add_subplot(111)
echo canvas = FigureCanvasTkAgg(fig, root)
echo canvas.get_tk_widget().pack()
echo.
echo update_data()
echo root.mainloop()
echo zeroconf.close()
) > earthquake_monitor.py

REM Inform user that the setup is complete
echo Setup Complete! The virtual environment is created, dependencies are installed, and the Python script is ready.
echo You can now activate the virtual environment using "call venv\Scripts\activate" and run "python earthquake_monitor.py".

REM Pause to keep the command window open
pause
