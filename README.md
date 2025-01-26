# earthvake
To create a detailed guide for manual compilation and setup of the project on GitHub, here’s how you can structure the README and the steps involved. This includes setting up the environment, cloning the repository, manually installing dependencies, and running the code.

---

### **GitHub Repository Setup Guide**

---

#### **Project Overview**

This project reads data from an ESP32-based device (or any other microcontroller that sends serial data) and visualizes it in real-time using Python. The data is collected via the serial interface and plotted using `matplotlib`.

---

### **Steps for Manual Setup and Compilation**

---

#### **1. Prerequisites**

Make sure you have the following installed before starting the setup:

- **Python 3.12 or later**: Download from [Python's official website](https://www.python.org/downloads/).
- **Git**: If Git is not installed, download and install from [Git's official website](https://git-scm.com/downloads).

You can verify Python and Git installation by running the following commands in your terminal:
```bash
python --version
git --version
```

---

#### **2. Clone the GitHub Repository**

Start by cloning the repository to your local machine using Git.

```bash
git clone https://github.com/loki-smip/earthvake.git
cd earthvake
```

---

#### **3. Set Up a Virtual Environment**

A virtual environment is recommended to isolate your project dependencies. 

1. **Create a virtual environment** using the following command:
   
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

You will see the virtual environment's name (`venv`) in your terminal prompt, indicating that the environment is activated.

---

#### **4. Install Project Dependencies**

Install all necessary Python libraries using pip.

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file in your repository, you can manually install dependencies as follows:

```bash
pip install pyserial matplotlib
```

---

#### **5. Connect Your ESP32 or Microcontroller**

Ensure that your ESP32 or the microcontroller that is transmitting serial data is connected to the computer via USB. Make note of the **COM port** (for Windows) or the **device file** (for Linux/macOS) associated with the serial connection.

For Windows, the device might be something like `COM3`, and for Linux/macOS, it could be something like `/dev/ttyUSB0`.

---

#### **6. Modify the Python Script (if necessary)**

Open the `main.py` file in your code editor and ensure the following:
- The correct **serial port** is specified in the code:
  ```python
  ser = serial.Serial('COM3', 9600, timeout=1)  # Replace COM3 with your actual port
  ```

If you are on Linux or macOS, the port might look like `/dev/ttyUSB0`.

---

#### **7. Run the Python Script**

After everything is set up, you can run the Python script to start reading and plotting the data:

```bash
python main.py
```

This will open a live graph window that updates based on the serial data received from your ESP32 (or other microcontroller).

---

#### **8. Save Graph as Image**

If you want to save the graph as an image, you can use the save functionality within the Python script or modify the script to save the figure manually.

Here’s a quick example of how you can save the plot:

```python
# Save the current figure as a PNG image
plt.savefig('graph_output.png')
```

---

#### **9. Automating the Process (Optional)**

If you want to automate the setup process, you can use the `installer.bat` file to:
- Install Python and pip if not present.
- Set up a virtual environment.
- Install required dependencies.
- Run the Python script.

**Steps:**
1. Save the `installer.bat` file in the root directory of your repository.
2. Run the `installer.bat` file to automatically set up your environment.

---

### **Directory Structure**

Here’s a basic structure for your project repository:

```
your-repository/
│
├── main.py                 # Main Python script
├── requirements.txt        # List of dependencies
├── installer.bat           # Installer script (Windows)
├── run.bat                 # Run script to start the project
└── README.md               # Project documentation
```

---

### **FAQ**

- **Q: How do I find the correct serial port?**
  - On Windows, you can find the COM port from Device Manager under "Ports (COM & LPT)".
  - On Linux/macOS, run the following command to list serial devices:
    ```bash
    ls /dev/tty*
    ```
    Look for entries like `/dev/ttyUSB0` or `/dev/ttyACM0`.

- **Q: How can I modify the graph or add features?**
  - You can modify the `update_graph` function in the `main.py` file to customize the graph or add additional features.

- **Q: How do I use the batch files?**
  - After running `installer.bat`, simply double-click `run.bat` to start the Python script.

---

### **Contributing**

If you'd like to contribute to this project:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request for review.

---

### **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### **End of Guide**

This README guide will provide all the steps for users to manually set up the environment, clone the repository, and run the Python script.
