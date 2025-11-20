# Chosen LEGACY AIRLINE

def main():
    # Airbus 321 neo data
    max_TO_weight = 97.0 # in tonnes
    fuel_capacity: 26.3 # in tonnes
    ma_c = 0.78 # cruise Mach
    range = 7,400 # in km
    cruise_ceiling = 40,000 # in ft
    seating = 206 # people
    cruise_LtoD = 20
    Wingspan = 35.80 # in m

    # Pratt and Whitney
    fuel_flow = {"takeoff" : 1.023, "climbout" : 0.839, "approach" : 0.279, "idle" : 0.099} # in kg/s
    NOx = {"takeoff" : 28.88, "climbout" : 22.01, "approach" : 10.79, "idle" : 5.74} # in g/kg
    nvpm_w = {"takeoff" : 37.7, "climbout" : 31.4, "approach" : 0.4, "idle" : 2.7} # in mg/kg
    nvpm_n = {"takeoff" : 3.12*10**14, "climbout" : 4.01*10**14, "approach" : 4.07*10**13, "idle" : 3.25*10**14} # in number/kg


if __name__ == "__main__":
    main()






