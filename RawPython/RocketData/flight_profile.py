from math import copysign, cos
from math import sin
import csv
from math import radians
from time import sleep
from turtle import color, pos, position
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Worker Functions
def openCSV(filename: str):
    arr = np.loadtxt(open(filename,"rb"), delimiter="\t")
    return arr

def magnitude(x: float, y: float):
    return np.sqrt(x**2 + y**2)

# Burn Time, Full Mass, Empty Mass of Engines
oxide_mass = {
    "L200-1685" : (13.05, .3916, .2302),
    "L225-1685" : (12.4,  .3963, .2275),
    "L355-1685" : (8.6,   .3963, .2325),
    "L475-1685" : (5.75,  .3916, .2373),
    "L535-1685" : (5.6,   .3963, .2347),
    "L540-2800" : (8.6,   .5646, .3087),
    "L610-1685" : (5.07,  .3974, .2371)
}


def main(ang, engine_path):
    #Defining Constants
    wind_speed = 5
    dry_mass = 6
    launch_angle = ang
    tube_radius = 0.04
    gravity = 9.81
    
    drogue_radius = 0.3
    main_radius = 1.2
    
    main_height = 250
    
    ground_level = 330
    
    mach_drag = openCSV("Mach.csv")
    ADS = openCSV("Altitude-Density-SoS.csv")
    engine = openCSV(engine_path)
    time = np.linspace(0, 500, 100000)
    
    F_thrust = np.interp(time, engine[:,0], engine[:,1])
    
    #Defining Initial Values
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
    position[0] = [0, ground_level]
    i = 0
    
    
    #Defining Benchmark Values
    drogue_chute = False
    main_chute = False
    supersonic = False
    burnout = False
    max_Gs_value = 0
    drogue_position = [0, 0]
    main_position = [0, 0]
    max_Gs = [0, 0]
    supersonic_position = [0, 0]
    burnout_position = [0, 0]
    
    
    for i in range(1, len(time)):
        #Calculate mass based on engine burn time
        mass[i] = dry_mass + (m * time[i] + b > 0) * (m * time[i] + b)
        
        #Getting Thrust from Engine Data
        thrust[i] = [F_thrust[i] * cos(radians(angle[i-1])), F_thrust[i] * sin(radians(angle[i-1]))]
        
        #Calculating Acceleration, Velocity, and Position based on Drag, Mass, Thrust, and Gravity
        acceleration[i] = [(thrust[i][0] + drag[i - 1][0]) / (mass[i]), (thrust[i][1] + drag[i - 1][1]) / (mass[i]) - gravity]
        velocity[i] = [velocity[i - 1][0] + acceleration[i][0] * (time[i] - time[i - 1]), velocity[i - 1][1] + acceleration[i][1] * (time[i] - time[i - 1])]
        position[i] = [position[i - 1][0] + velocity[i][0] * (time[i] - time[i - 1]), position[i - 1][1] + velocity[i][1] * (time[i] - time[i - 1])]
        
        #Calculating Mach Based on Velocity and Speed of Sound at Altitude
        mach[i][0] = magnitude(velocity[i][0] + 11, velocity[i][1]) / np.interp(position[i][1], ADS[:,0], ADS[:,2])
        Cd[i] = np.interp(mach[i - 1], mach_drag[:,0], mach_drag[:,1])
        
        # Determine if Chutes Should Deploy
        if(velocity[i][1] < 0 and not drogue_chute):
            drogue_chute = True
            drogue_position = position[i]
        if(drogue_chute and position[i][1] < main_height + ground_level and not main_chute):
            main_chute = True
            main_position = position[i]
        

        #Calculating Drag based on Drag Coefficient, Air Density, and Velocity
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

        #Checks for Benchmark Values
        if(mach[i] > 1 and not supersonic):
            supersonic = True
            supersonic_position = position[i]
        if(F_thrust[i] <= 0 and not burnout):
            burnout = True
            burnout_position = position[i]
        if(magnitude(acceleration[i][0], acceleration[i][1]) / gravity > max_Gs_value):
            max_Gs = position[i]
            max_Gs_value = magnitude(acceleration[i][0], acceleration[i][1]) / gravity
        
        #End Calculations if Rocket Hits Ground
        if(position[i][1] < ground_level):
            break
    
    
    #Format all arrays to be the same size
    angle = angle[:i].flatten()
    air_angle = air_angle[:i].flatten()
    position = position[:i]
    velocity = velocity[:i]
    acceleration = acceleration[:i]
    thrust = thrust[:i]
    drag = drag[:i]
    time = time[:i].flatten()
    mass = mass[:i].flatten()
    mach = mach[:i].flatten()
    Cd = Cd[:i].flatten()
    
    
    #Constructing Spreadsheet and Graph
    
    #time, mass, angle, angle of attack, speed, mach, Cd, Gs, distance, altitude, thrust magnitude, drag magnitude, acc_x, acc_y, thrust_x, thrust_y, drag_x, drag_y, vel_x, vel_y, air_density, speed of sound
    np.vstack((time, mass, angle))
    spreadsheet = np.vstack((time, mass, angle, air_angle, magnitude(velocity[:,0], velocity[:,1]), mach, Cd, magnitude(acceleration[:,0], acceleration[:,1])/9.81, position[:,0], position[:,1], magnitude(thrust[:,0], thrust[:,1]), magnitude(drag[:,0], drag[:,1]), acceleration[:,0], acceleration[:,1], thrust[:,0], thrust[:,1], drag[:,0], drag[:,1], velocity[:,0], velocity[:,1], np.interp(position[:,1], ADS[:i,0], ADS[:i,1]), np.interp(position[:,1], ADS[:i,0], ADS[:i,2]))).T
    spreadsheet = spreadsheet[:, :]
    print(spreadsheet.shape)
    # np.savetxt("extended_spreadsheet.csv", spreadsheet, delimiter=",", fmt='%f', header='time (s), mass (kg), angle, angle of attack, speed (m/s), mach, Cd, Gs, distance (m), altitude (m), thrust magnitude (N), drag magnitude (N), acc_x (m/s^2), acc_y (m/s^2), thrust_x (N), thrust_y (N), drag_x (N), drag_y (N), vel_x (m/s), vel_y (m/s), air_density (kg/m^3), speed of sound (m/s)')
    fig, ax = plt.subplots(nrows=1, ncols=1)
    
    time_interval = 10
    time_stride = int(time_interval / (time[1] - time[0]))
    time_positions = position[::time_stride]
    
    fig.set_facecolor(color="#0B5394")
    ax.set_facecolor(color="#0B5394")
    
    ax.spines[:].set_color("#CCCCCC")
    ax.xaxis.label.set_color('#CCCCCC')
    ax.yaxis.label.set_color('#CCCCCC')
    ax.tick_params(axis='x', colors='#CCCCCC')
    ax.tick_params(axis='y', colors='#CCCCCC')
    
    ax.scatter(time_positions[:,0], time_positions[:,1], color='orange', zorder=2)
    ax.plot(position[:,0], position[:,1], color='#c4dbff' ,zorder=1)
    # ax.plot(time, acceleration[:, 1], color='#c4dbff' ,zorder=1)
    
    ax.annotate('Drogue Deployment: {} m'.format(int(drogue_position[1])), color='#CCCCCC', fontsize=15,
                xy=(drogue_position[0], drogue_position[1]), xycoords='data',
                xytext=(-50, 5), textcoords='offset points',
                arrowprops=dict(facecolor='#CCCCCC', color='#CCCCCC', shrink=0.05),
                horizontalalignment='right', verticalalignment='bottom')
    ax.annotate('Main Deployment: {} m'.format(int(main_position[1])), color='#CCCCCC', fontsize=15,
                xy=(main_position[0], main_position[1]), xycoords='data',
                xytext=(-20, 20), textcoords='offset points',
                arrowprops=dict(facecolor='#CCCCCC', color='#CCCCCC', shrink=0.05),
                horizontalalignment='right', verticalalignment='bottom')
    ax.annotate('Max G-Load: {} Gs'.format((max(magnitude(acceleration[:,0], acceleration[:,1]))/9.81).round(2)), color='#CCCCCC', fontsize=15,
                xy=(max_Gs[0], max_Gs[1]), xycoords='data',
                xytext=(-15, 60), textcoords='offset points',
                arrowprops=dict(facecolor='#CCCCCC', color='#CCCCCC', shrink=0.05),
                horizontalalignment='right', verticalalignment='bottom')
    ax.annotate('Mach 1: {} m'.format(int(supersonic_position[1])), color='#CCCCCC', fontsize=15,
                xy=(supersonic_position[0], supersonic_position[1]), xycoords='data',
                xytext=(-30, -15), textcoords='offset points',
                arrowprops=dict(facecolor='#CCCCCC', color='#CCCCCC', shrink=0.05),
                horizontalalignment='right', verticalalignment='top')
    ax.annotate('Burnout: {} m'.format(int(burnout_position[1])), color='#CCCCCC', fontsize=15,
                xy=(burnout_position[0], burnout_position[1]), xycoords='data',
                xytext=(45, 15), textcoords='offset points',
                arrowprops=dict(facecolor='#CCCCCC', color='#CCCCCC', shrink=0.05),
                horizontalalignment='left', verticalalignment='bottom')
    
    
    legend_elements = [Line2D([0], [0], marker='o', color='#0B5394', label='{} second intervals'.format(time_interval),
                        markerfacecolor='orange', markersize=10), 
                        Line2D([0], [0], color='#0B5394', label='Flight Time: {} seconds'.format(time[-1].round(2)))]
    
    legend = ax.legend(loc='upper left', shadow=True, fontsize='large', handles=legend_elements, facecolor="#0B5394", edgecolor="#CCCCCC")

    for text in legend.get_texts():
        text.set_color("#CCCCCC")
        

    ax.add_artist(legend)
    ax.set_title("Rocket Trajectory", color="#CCCCCC", fontsize=30)
    ax.set_xlabel("Distance (m)", color="#CCCCCC", fontsize=20)
    ax.set_ylabel("Altitude (m)", color="#CCCCCC", fontsize=20)
    
    print(max(mach))
    print(max(magnitude(velocity[:,0], velocity[:,1])))
    print(max(position[:,1]))
    print(max(magnitude(acceleration[:,0], acceleration[:,1])/9.81))
    print(min(position[:,0]))
    
    print("Done!")
    plt.show()
    sleep(30)
main(5, "L610-1685.csv")
plt.show()
