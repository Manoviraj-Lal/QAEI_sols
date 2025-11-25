import numpy as np
import helpers
import sys

np.set_printoptions(legacy='1.25')

# Chosen LEGACY AIRLINE test

def main():
    # Airbus A321 neo data
    max_TO_weight = 97.0 # in tonnes
    fuel_capacity = 26.3 # in tonnes
    mach = 0.78 # cruise Mach
    range = 7400 # in km
    seating = 206 # people
    cruise_LtoD = 20

    # Pratt and Whitney engine data
    fuel_flow = np.array([1.023, 0.839, 0.279, 0.099]) # in kg/s
    EI_NOx = np.array([28.88, 22.01, 10.79, 5.74]) # in g/kg
    EI_nvpm_w = np.array([37.7, 31.4, 0.4, 2.7]) # in mg/kg
    EI_nvpm_n = np.array([3.12*10**14, 4.01*10**14, 4.07*10**13, 3.25*10**14]) # in number/kg

    # Airport data in degrees
    lhr = (51.477500, -0.461389)
    bos = (42.363056, -71.006389)

    # LTO Fuel emissions
    mass_fuel_LTO = helpers.calc_LTO(np.array([1,1,1,1]),fuel_flow)/1000 # in tonnes
    NOx_LTO = helpers.calc_LTO(EI_NOx,fuel_flow) / 1000 # in kg
    nvpm_w_LTO = helpers.calc_LTO(EI_nvpm_w,fuel_flow) / 1000 # in g
    nvpm_n_LTO = helpers.calc_LTO(EI_nvpm_n,fuel_flow) # in number

    # Cruise mission
    distance, time = helpers.cruise_mission(lhr, bos, mach) # in m, secs
    if distance > range*10**3:
        sys.exit("Range exceeded")

    # Cruise fuel
    mass_init = 0.85 * seating * 0.1 + 50.1 # in tonnes w/o fuel ie payload + OEW
    mass_fuel_cruise = helpers.cruise_fuel(cruise_LtoD, distance, mass_init) # in tonnes
    mass_TO = mass_init + mass_fuel_LTO + mass_fuel_cruise # in tonnes

    if mass_fuel_cruise > fuel_capacity:
        sys.exit("Fuel capacity exceeded")
    elif mass_TO > max_TO_weight:
        sys.exit("Maximum take off weight exceeded")

    # Cruise emissions
    CO2_cruise = 3.16 * mass_fuel_cruise # in tonnes
    H2O_cruise = 1.24 * mass_fuel_cruise # in tonnes
    SO2_cruise = mass_fuel_cruise * 0.0006 * 0.98 * 2 * 1000 # in kg assuming 600 ppm FSC
    H2SO4_cruise = mass_fuel_cruise * 0.0006 * 0.02 * 3.0625 * 1000 # in kg assuming 600 ppm FSC

    fuel_flow_cruise = mass_fuel_cruise*1000/time # in kg/s
    NOx_cruise =  mass_fuel_cruise * helpers.NOx_EI(EI_NOx, mach, 216.6, 22631.7, fuel_flow_cruise) # in kg (tonnes * g/kg)

    EI_nvpm_w_cruise, EI_nvpm_n_cruise = helpers.nvPM_EI(EI_nvpm_w, EI_nvpm_n, mach, 216.6, 22631.7, fuel_flow_cruise) # in mg/kg, number/kg
    nvpm_w_cruise = mass_fuel_cruise * EI_nvpm_w_cruise # in g (tonnes * mg/kg)
    nvpm_n_cruise =  mass_fuel_cruise * EI_nvpm_n_cruise * 1000 # in number 

    summary_LTO = {
        "Fuel_LTO" : [mass_fuel_LTO, "tonnes"],
        "NOx_LTO": [NOx_LTO, "kg"],
        "nvpm_w_LTO": [nvpm_w_LTO, "g"],
        "nvpm_n_LTO": [nvpm_n_LTO, "by #"]
    }

    summary_cruise = {
        "Fuel_cruise" : [mass_fuel_cruise, "tonnes"],
        "NOx_cruise": [NOx_cruise, "kg"],
        "nvpm_w_cruise": [nvpm_w_cruise, "g"],
        "nvpm_n_cruise": [nvpm_n_cruise, "by #"],
        "CO2_cruise": [CO2_cruise, "tonnes"],
        "H2O_cruise": [H2O_cruise, "tonnes"],
        "SO2_cruise": [SO2_cruise, "kg"],
        "H2SO4_cruise": [H2SO4_cruise, "kg"],
    }

    print("\n")
    
    for key, value in summary_LTO.items():
        print(f"{key:<{14}} : {value[0]:<{10}.4g} {value[1]}")
    
    print("\n")

    for key, value in summary_cruise.items():
        print(f"{key:<{14}} : {value[0]:<{10}.4g} {value[1]}")

    print("\n")


if __name__ == "__main__":
    main()
