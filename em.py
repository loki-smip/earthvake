import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Serial port configuration
SERIAL_PORT = "COM5"  # Replace with your COM port
BAUD_RATE = 115200

# Graph settings
GRAPH_WIDTH = 120
Y_MIN, Y_MAX = -80, 80

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error connecting to {SERIAL_PORT}: {e}")
    exit()

# Data buffers for x, y, z
x_data = deque([0] * GRAPH_WIDTH, maxlen=GRAPH_WIDTH)
y_data = deque([0] * GRAPH_WIDTH, maxlen=GRAPH_WIDTH)
z_data = deque([0] * GRAPH_WIDTH, maxlen=GRAPH_WIDTH)


def parse_serial_data():
    """
    Reads and parses the serial data.
    Expected format: x=10y=20z=30$
    """
    try:
        line = ser.readline().decode('utf-8').strip()
        if '$' in line:
            x_start = line.index("x=") + 2
            y_start = line.index("y=") + 2
            z_start = line.index("z=") + 2

            x_val = int(line[x_start:x_start + 3])
            y_val = int(line[y_start:y_start + 3])
            z_val = int(line[z_start:z_start + 3])

            return x_val, y_val, z_val
    except Exception as e:
        print(f"Error parsing data: {e}")
    return None, None, None


def update_graph(frame):
    """
    Update the graph with new data.
    """
    global x_data, y_data, z_data

    x, y, z = parse_serial_data()
    if x is not None and y is not None and z is not None:
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)

    # Clear the plot
    ax.clear()

    # Plot X, Y, Z
    ax.plot(range(len(x_data)), x_data, label="X-axis", color="blue")
    ax.plot(range(len(y_data)), y_data, label="Y-axis", color="green")
    ax.plot(range(len(z_data)), z_data, label="Z-axis", color="red")

    # Graph styling
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_title("Earthquake Graph")
    ax.set_xlabel("Time")
    ax.set_ylabel("Acceleration")
    ax.legend(loc="upper right")
    ax.grid(True)


# Setup matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ani = animation.FuncAnimation(fig, update_graph, interval=50)

# Show the plot
plt.show()

# Close serial connection on exit
ser.close()
