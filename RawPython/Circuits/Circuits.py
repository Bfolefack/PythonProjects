import numpy as np
import re
def branch_str(text: list):
    branches = np.array([])

    while(True):
        # print("Time for branch " + str(branches.shape[0] + 1) + "!")
        resistance = 0
        resistor = text[0]
        while(True):
            resistor = text[0]
            if(resistor == "("):
                text.pop(0)
                resistance += branch_str(text)
            elif(resistor == ")"):
                text.pop(0)
                break
            elif(resistor == ","):
                text.pop(0)
                break
            else:
                text.pop(0)
                resistance += float(resistor)
        branches = np.append(branches, resistance)
        print(branches)
        if(resistor == ")"):
            break
    return 1/np.sum(1/branches)

def prompt_str(text : list):
    resistance = 0
    while(len(text) > 0):
        resistor = text[0]
        if(resistor == "("):
            text.pop(0)
            resistance += branch_str(text)
        else:
            resistance += float(resistor)
            text.pop(0)
    return resistance

# def prompt_str(text : list, current : float = 0):
#     resistance = 0
#     currents = ""
#     while(len(text) > 0):
#         resistor = text[0]
#         if(resistor == "("):
#             text.pop(0)
#             currents += "("
#             resistance += branch_str(text, current)
#         else:
#             resistance += float(resistor)
#             currents += str(current) + " "
#             text.pop(0)
#     return resistance

def solve_circuit(text : str, current : float = 0):
    lis = re.findall("(\(|\)|\,|\d+)", text)
    resistance = prompt_str(lis)
    print("The total resistance is: " + str(resistance))
    return resistance


def solve_circuit_current(text : str, current : float = 0):
    lis = re.findall("(\(|\)|\,|\d+)", text)
    resistance, currents = prompt_str(lis, current)
    print("The total resistance is: " + str(resistance))
    return resistance
#"3-(-3-(-24-,-8-)-,-(-10-,-15-)-6-)-5"
#"2-8-6"
#"(-2-,-4-,-6-)"
#"2-(-3-(-1-5-,-6-)-,-(-4-,-12-)-9-)"
voltage = 24
resistance = solve_circuit("35(20, 60)")
print("The voltage is: " + str(voltage))
print("The current is: " + str(voltage/resistance))
print("The resistance is: " + str(resistance))