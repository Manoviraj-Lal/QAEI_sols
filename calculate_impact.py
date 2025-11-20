import numpy as np
import helpers
import sys

# Chosen LEGACY AIRLINE

def main():
    # Airbus 321 neo data
    max_TO_weight = 97.0 # in tonnes
    fuel_capacity = 26.3 # in tonnes
    ma_c = 0.78 # cruise Mach
    range = 7400 # in km
    seating = 206 # people
    cruise_LtoD = 20
    wingspan = 35.80 # in m

    # Pratt and Whitney
    fuel_flow = np.array([1.023, 0.839, 0.279, 0.099]) # in kg/s
    NOx = np.array([28.88, 22.01, 10.79, 5.74]) # in g/kg
    nvpm_w = np.array([37.7, 31.4, 0.4, 2.7]) # in mg/kg
    nvpm_n = np.array([3.12*10**14, 4.01*10**14, 4.07*10**13, 3.25*10**14]) # in number/kg
    bypass_ratio = 11.6
    opr = 38.1
    rated_thrust = 147.3 # in kN

    # Airport data in degrees
    lhr = (51.477500, -0.461389)
    bos = (42.363056, -71.006389)

    fuel_LTO = helpers.calc_LTO(np.array([1,1,1,1]),fuel_flow)
    NOx_LTO = helpers.calc_LTO(NOx,fuel_flow)
    nvpm_w_LTO = helpers.calc_LTO(nvpm_w,fuel_flow)
    nvpm_n_LTO = helpers.calc_LTO(nvpm_n,fuel_flow)

    distance, time = helpers.cruise_mission(lhr, bos, ma_c) # in m, secs
    if distance > range*10**3:
        sys.exit("Range exceeded")

    mass_init = 0.85 * seating * 0.1 + 44.3 # in tonnes w/o fuel ie OEW + payload
    mass_fuel_cruise = helpers.cruise_fuel(cruise_LtoD, distance, mass_init)
    mass_TO = mass_init + mass_fuel_cruise

    if mass_fuel_cruise > fuel_capacity:
        sys.exit("Fuel capacity exceeded")
    elif mass_TO > max_TO_weight:
        sys.exit("Maximum take off weight exceeded")
    
    
    


if __name__ == "__main__":
    main()





