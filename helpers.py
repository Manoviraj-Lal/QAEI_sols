import numpy as np

# Helper functions for the impact calculation

def calc_LTO(ei_vector, fuel_flow_vec):
    deltat_LTO = np.array([0.7*60, 2.2*60, 4*60, 26*60])
    emissions = np.sum(fuel_flow_vec * ei_vector * deltat_LTO * 2)
    return emissions


def cruise_mission(origin, destination, mach):
    T = 216.6 # in K at alt = 11000 m (near optimum altitude)
    gamma = 1.4
    R = 8.314
    M_air = 28.97*10**-3
    V = mach * np.sqrt((gamma*R*T)/M_air)
