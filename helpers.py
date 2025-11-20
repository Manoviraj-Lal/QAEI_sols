import numpy as np

# Helper functions for the impact calculation

def calc_LTO(ei_vector, fuel_flow_vec):
    deltat_LTO = np.array([0.7*60, 2.2*60, 4*60, 26*60])
    emissions = np.sum(fuel_flow_vec * ei_vector * deltat_LTO * 2)
    return emissions


def cruise_mission(origin, destination, mach):
    phi_0 = origin[0] * np.pi/180
    phi_1 = destination[0] * np.pi/180
    lam_0 = origin[1] * np.pi/180
    lam_1 = destination[1] * np.pi/180
    T = 216.6 # in K at alt = 11000 m (near optimum altitude)
    gamma = 1.4
    R = 8.314
    r_earth = 6371 * 10**3
    M_air = 28.97*10**-3
    V = mach * np.sqrt((gamma*R*T)/M_air)
    D = r_earth * np.arccos(np.sin(phi_0)*np.sin(phi_1) + np.cos(phi_0)*np.cos(phi_1)*np.cos(lam_1-lam_0))

    return D, D/V
