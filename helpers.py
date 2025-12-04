import numpy as np

# Helper functions for the impact calculation

def calc_LTO(ei_vector, fuel_flow_vec):
    """
    Returns full LTO cycle fuel burn (kg) and emissions for the given species (assume TO/CO/App/Taxi) per engine
    
    :param ei_vector: LTO emissions index vector (given for an engine)
    :param fuel_flow_vec: LTO fuel flow vector (given for an engine)
    """
    deltat_LTO = np.array([0.7 * 60, 2.2 * 60, 4 * 60, 26 * 60])
    emissions = np.sum(fuel_flow_vec * ei_vector * deltat_LTO)
    return emissions


def cruise_mission(origin, destination, mach):
    """
    Returns total distance and flight time to travel between two latitude/longitude tuples.
    
    :param origin: latitude, longitude tuple of origin
    :param destination: latitude, longitude tuple of destination
    :param mach: cruise mach number
    """
    
    phi_0 = origin[0] * np.pi / 180
    phi_1 = destination[0] * np.pi / 180
    lam_0 = origin[1] * np.pi / 180
    lam_1 = destination[1] * np.pi / 180
    T = 216.6  # in K at alt = 11000 m (near optimum altitude)
    gamma = 1.4
    R = 8.314
    r_earth = 6371 * 10**3
    M_air = 28.97 * 10**-3
    V = mach * np.sqrt((gamma * R * T) / M_air)
    D = r_earth * np.arccos(
        np.sin(phi_0) * np.sin(phi_1)
        + np.cos(phi_0) * np.cos(phi_1) * np.cos(lam_1 - lam_0)
    )
    return D, D / V


def cruise_fuel(L_over_D, distance, mass_initial):
    """
    Returns total fuel burn (kg) required to cruise between locations.
    
    :param L_over_D: Lift to drag ratio of the aircraft
    :param distance: cruise distance flown
    :param mass_initial: mass of payload + OEW
    """

    reserve = 0.1  # 10 percent of cruise fuel kept reserve
    eta_0 = 0.3
    LHV = 43.1 * 10**6
    C = 9.81 / (L_over_D * LHV * eta_0)
    fuelmass_cruise = (mass_initial * (np.exp(C * distance) - 1)) / (
        1 - reserve * (np.exp(C * distance) - 1)
    )
    return fuelmass_cruise


def NOx_EI(ei_vector, M, T, p, fuel_flow):
    """
    Returns NOx emissions index at cruise conditions using BFFM2.
    
    :param ei_vector: LTO emissions index vector (given for an engine)
    :param M: cruise mach number
    :param T: temperature at cruise
    :param p: pressure at cruise
    :param fuel_flow: cruise fuel flow rate
    """
    theta = T / 288.15  # in K at alt = 11000 m (near optimum altitude)
    delta = p / 101325  # in Pa at alt = 11000 m (near optimum altitude)
    fuel_flow_surf = fuel_flow * (theta**3.8 / delta) * np.exp(0.2 * M**2)
    deltat_LTO = np.array([0.7 * 60, 2.2 * 60, 4 * 60, 26 * 60])
    NOx_EI_SL = np.interp(fuel_flow_surf, deltat_LTO, ei_vector)
    H = -19 * -0.0063
    NOx_EI = NOx_EI_SL * np.sqrt(delta**1.02 / theta**3.3) * np.exp(H)
    return NOx_EI


def nvPM_EI(ei_nvpm_w, ei_nvpm_n, M, T, p, fuel_flow):
    """
    Returns nvPM emissions indices (mass, number) at cruise conditions using either BFFM2.
    
    :param ei_nvpm_w:  LTO emissions index vector for nvpm by weight (given for an engine)
    :param ei_nvpm_n: LTO emissions index vector for nvpm by mass (given for an engine)
    :param M: cruise mach number
    :param T: temperature at cruise
    :param p: pressure at cruise
    :param fuel_flow: cruise fuel flow rate
    """
    theta = T / 288.15  # in K at alt = 11000 m (near optimum altitude)
    delta = p / 101325  # in Pa at alt = 11000 m (near optimum altitude)
    fuel_flow_surf = fuel_flow * (theta**3.8 / delta) * np.exp(0.2 * M**2)
    deltat_LTO = np.array([0.7 * 60, 2.2 * 60, 4 * 60, 26 * 60])
    nvpm_w_EI_SL = np.interp(fuel_flow_surf, deltat_LTO, ei_nvpm_w)
    nvpm_n_EI_SL = np.interp(fuel_flow_surf, deltat_LTO, ei_nvpm_n)
    nvpm_w_EI = nvpm_w_EI_SL * (theta**3.3 / delta**1.02)
    nvpm_n_EI = nvpm_n_EI_SL * (theta**3.3 / delta**1.02)
    return nvpm_w_EI, nvpm_n_EI


def calc_waypoints(start, end, N):
    """
    Docstring for calc_waypoints
    
    :param start: Description
    :param end: Description
    :param N: Description
    """