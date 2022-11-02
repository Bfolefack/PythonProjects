from math import copysign, cos
from math import sin
import csv
from math import radians
from turtle import position
import numpy as np


import matplotlib.pyplot as plt


def openCSV(filename: str):
    arr = np.loadtxt(open(filename,"rb"), delimiter="\t")
    return arr

def magnitude(x: float, y: float):
    return np.sqrt(x**2 + y**2)

# np.interp(np.linspace(0, 4, 1000), arr[:,0], arr[:,1])

oxide_mass = {
    "L200-1685" : (13.05, .3916, .2302),
    "L225-1685" : (12.4,  .3963, .2275),
    "L355-1685" : (8.6,   .3963, .2325),
    "L475-1685" : (5.75,  .3916, .2373),
    "L535-1685" : (5.6,   .3963, .2347),
    "L540-2800" : (8.6,   .5646, .3087),
    "L610-1685" : (5.07,   .3974, .2371)
}


def main(ang, engine_path):
    wind_speed = 11
    dry_mass = 6
    launch_angle = ang
    tube_radius = 0.04
    gravity = 9.81
    
    drogue_radius = 0.25
    main_radius = 1.5
    
    drogue_chute = False
    main_chute = False
    
    
    
    mach_drag = openCSV("Mach.csv")
    ADS = openCSV("Altitude-Density-SoS.csv")
    engine = openCSV(engine_path)
    time = np.linspace(0, 450, 10000)
    
    F_thrust = np.interp(time, engine[:,0], engine[:,1])
    
    mass = np.ndarray(shape=(len(time), 1), dtype=float)
    
    Cd = np.ndarray(shape=(len(time), 1), dtype=float)
    angle = np.ndarray(shape=(len(time), 1), dtype=float)
    air_angle = np.ndarray(shape=(len(time), 1), dtype=float)
    drag = np.ndarray(shape=(len(time), 2), dtype=float)
    thrust = np.ndarray(shape=(len(time), 2), dtype=float)
    acceleration = np.ndarray(shape=(len(time), 2), dtype=float)
    velocity = np.ndarray(shape=(len(time), 2), dtype=float)
    position = np.ndarray(shape=(len(time), 2), dtype=float)
    mach = np.ndarray(shape=(len(time), 1), dtype=float)
    
    engine_tuple = oxide_mass[engine_path[0:9]]
    m = (engine_tuple[1] - engine_tuple[2])/(0 - engine_tuple[0])
    b = engine_tuple[2]
    
    mass[0] = dry_mass + engine_tuple[1]
    Cd[0] = 0.75
    angle[0] = 90 - launch_angle
    drag[0] = [0, 0]
    thrust[0] = [F_thrust[0] * cos(radians(angle[0])), F_thrust[0] * sin(radians(angle[0]))]
    i = 0
    for i in range(1, len(time)):
        mass[i] = dry_mass + (m * time[i] + b > 0) * (m * time[i] + b)
        thrust[i] = [F_thrust[i] * cos(radians(angle[i-1])), F_thrust[i] * sin(radians(angle[i-1]))]
        acceleration[i] = [(thrust[i][0] + drag[i - 1][0]) / (mass[i]), (thrust[i][1] + drag[i - 1][1]) / (mass[i]) - gravity]
        velocity[i] = [velocity[i - 1][0] + acceleration[i][0] * (time[i] - time[i - 1]), velocity[i - 1][1] + acceleration[i][1] * (time[i] - time[i - 1])]
        position[i] = [position[i - 1][0] + velocity[i][0] * (time[i] - time[i - 1]), position[i - 1][1] + velocity[i][1] * (time[i] - time[i - 1])]
        mach[i][0] = magnitude(velocity[i][0], velocity[i][1]) / np.interp(position[i][1], ADS[:,0], ADS[:,2])
        Cd[i] = np.interp(mach[i - 1], mach_drag[:,0], mach_drag[:,1])
        
        if(velocity[i][1] < 0 and not drogue_chute):
            drogue_chute = True
        if(drogue_chute and position[i][1] < 200 and not main_chute):
            main_chute = True
        airspeed = magnitude(velocity[i][0] + wind_speed, velocity[i][1])
        if(not drogue_chute and not main_chute):
            step_drag = 0.5 * np.interp(position[i][1], ADS[:,0], ADS[:,1]) * Cd[i] * np.pi * tube_radius**2  * airspeed**2
            drag[i] = [abs(step_drag * cos(radians(air_angle[i - 1]))) * -copysign(1, velocity[i][0]+wind_speed), abs(step_drag * sin(radians(air_angle[i - 1]))) * -(copysign(1, velocity[i][1]))]
        elif drogue_chute and not main_chute:
            step_drag = 0.5 * np.interp(position[i][1], ADS[:,0], ADS[:,1]) * 1.5 * np.pi * drogue_radius**2 * airspeed**2
            drag[i] = [abs(step_drag * cos(radians(air_angle[i - 1]))) * -copysign(1, velocity[i][0]+wind_speed), abs(step_drag * sin(radians(air_angle[i - 1]))) * -(copysign(1, velocity[i][1]))]
        else:
            step_drag = 0.5 * np.interp(position[i][1], ADS[:,0], ADS[:,1]) * 1.5 * np.pi * main_radius**2   * airspeed**2
            drag[i] = [abs(step_drag * cos(radians(air_angle[i - 1]))) * -copysign(1, velocity[i][0]+wind_speed), abs(step_drag * sin(radians(air_angle[i - 1]))) * -(copysign(1, velocity[i][1]))]
        angle[i] = np.arctan2(velocity[i][1], velocity[i][0]) * 180 / np.pi
        air_angle[i] = np.arctan2(velocity[i][1], velocity[i][0] + wind_speed) * 180 / np.pi
        # print(position[i])
        # print(drag[i])
        if(position[i][1] < 0):
            break
    position = position[:i] * 3.28084
    velocity = velocity[:i]
    acceleration = acceleration[:i]
    thrust = thrust[:i]
    time = time[:i]
    mass = mass[:i]
    mach = mach[:i]
    
    
        # print(time[i])
        # time, angle, air_angle, thrust, drag, acceleration, velocity, position, mach
        # return np.hstack((time, angle, air_angle, thrust, drag, acceleration, velocity, position, mach))
    #plt.plot(time, position[:,1])
    #plt.plot(time, mach)
    #plt.plot(time, position[:,1])
    plt.plot(position[:,0], position[:,1])
    print(velocity[-1])
    # plt.plot(time, drag[:,1])
    
    print("Done!")
# main(0)
main(5, "L610-1685.csv")
plt.show()
