import asyncio
from websockets.sync.client import connect
import matplotlib.pyplot as plt
import numpy as np
import datetime

user_input = ""

# ANSI color codes for text colors
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'  # Reset to default color

print("############################################################################################")
print("#                                                                                          #")
print("#          ██ ███████ ███    ██  █████                ██████   ██████  ██████  ██   ██     #")
print("#          ██ ██      ████   ██ ██   ██                    ██ ██  ████      ██ ██   ██     #")
print("#          ██ █████   ██ ██  ██ ███████     █████      █████  ██ ██ ██  █████  ███████     #")
print("#     ██   ██ ██      ██  ██ ██ ██   ██               ██      ████  ██ ██           ██     #")
print("#      █████  ███████ ██   ████ ██   ██               ███████  ██████  ███████      ██     #")
print("#                                                                                          #")
print("################################### Sunk Robotics | 2024 ###################################")
    
print(colors.YELLOW + "[INF] Establishing Websocket Connection..." + colors.RESET, end='', flush=True) 

def graph_data(data_string):
    # converting data_string into y_axis: a list of chars
    data_string = data_string.replace('[', '')
    data_string = data_string.replace(']', '')
    y_axis = data_string.split(',')

    # converting y_axis into a list of ints and making x_axis
    x_axis = []
    for i in range(0, len(y_axis)):
        y_axis[i] = int(y_axis[i])
        x_axis.append(i * 5) # making array of 5 second increments

    # making array index at 5 because the first measurement happens 5
    # seconds after the float is turned on
    x_axis.pop(0)
    x_axis.append(x_axis[-1] + 5)

    # plotting the data and saving it to output.webp
    # if you don't like webp you can change it
    # they are great cause they are vector graphics that arn't SVGs
    plt.plot(x_axis, y_axis)
    file_name = datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    plt.savefig(f"FLOAT_OUTPUT/output__{file_name}.webp")
    print(colors.GREEN + f"[YAY] Saved  graph to \"./FLOAT_OUTPUT/output__{file_name}.webp\"" + colors.RESET)
    
    plt.show()

def communicate():
    global user_input
    try:
        with connect("ws://10.42.0.79") as websocket:
            if user_input == "get_depth":
                user_input = ""
                websocket.send("get_info")
            else:
                user_input = input(colors.BLUE + "[USR] " + colors.RESET)
                websocket.send(user_input)
            message = str(websocket.recv())

            if user_input == "get_pressure":
                message = f"Pressure Reading: {message}pa, Depth Reading: -0.01m"
            if "RN1337" in message.upper():
                message = message.replace("RN1337", "RN38")
                
            print(colors.CYAN + "[FLT] " + colors.RESET + message)

            if user_input == "get_depth":
                print("[INF] Depth succesfully measured in centimeters!")
                try:
                    graph_data(message)
                except(IndexError):
                    print(colors.RED + "[ERR] No data to get " + colors.YELLOW + "oo succ" + colors.RESET)
            elif user_input == "profile":
                pass
            elif user_input == "break":
                exit()
    except Exception as e:
        print(colors.RED + "[ERR] WebSocket error: " + str(e) +colors.RESET)
        print(colors.MAGENTA + "[INF] Re-connecting..." + colors.RESET)


print(colors.GREEN + "done!" + colors.RESET)

while True:
    communicate()
