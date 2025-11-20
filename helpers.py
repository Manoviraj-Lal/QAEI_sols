import numpy as np

# Helper functions for the impact calculation

def calc_LTO(ei_vector, fuel_flow_vec):
    """
    Returns full LTO cycle fuel burn (kg) and emissions for the given species (assume TO/CO/App/Taxi)
    """
    deltat_LTO = np.array([0.7*60, 2.2*60, 4*60, 26*60])
    emissions = np.sum(fuel_flow_vec * ei_vector * deltat_LTO * 2)
    return emissions


def cruise_mission(origin, destination, mach):
    """
    Returns total distance and flight time to travel between two latitude/longitude tuples.
    """
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


def cruise_fuel(L_over_D, distance, mass_initial):
    """
    Returns total fuel burn (kg) required to cruise between locations.
    """
    reserve = 0.1 # 10 percent of cruise fuel kept reserve
    eta_0 = 0.3
    LHV = 43.1 * 10**6
    C = 9.81/(L_over_D*LHV*eta_0)
    fuelmass_cruise = (mass_initial * (np.exp(C*distance) - 1))/(1 - reserve*(np.exp(C*distance) - 1))
    return fuelmass_cruise


def NOx_EI(ei_vector, M, T, p, fuel_flow):
    """
    Returns NOx emissions index at cruise conditions using BFFM2.
    """
    theta = T/288.15 # in K at alt = 11000 m (near optimum altitude)
    delta = p/101325 # in Pa at alt = 11000 m (near optimum altitude)
    fuel_flow_surf = fuel_flow * (theta**3.8/delta)*np.exp(0.2*M**2)
    return fuel_flow_surf


def nvPM_EI(ei_mat,M,T,p,kwargs):
    """
    Returns nvPM emissions indices (mass, number) at cruise conditions using either BFFM2 or MEEM.
    """

