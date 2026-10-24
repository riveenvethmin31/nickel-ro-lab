# ==============================================================================
# Project: NickelRO Lab
# Module: Permeate Flux Calculation Model
# Reference: Shigidi et al. (2022), "Studying Different Operating Conditions on 
#            Reverse Osmosis Performance in the Treatment of Wastewater..."
# ==============================================================================

def calculate_permeate_flux(temperature, pressure, concentration, flow_rate):
    """
    Calculates the reverse osmosis permeate flux (kg / m^2 * h) 
    using the empirical polynomial model from Shigidi et al. (2022).
    
    Parameters:
    - temperature (float): Feed temperature in °C (Range: 25 - 45)
    - pressure (float): Operating pressure in bar (Range: 10 - 40)
    - concentration (float): Initial nickel concentration in ppm (Range: 25 - 150)
    - flow_rate (float): Feed flow rate in L/min (Range: 2 - 4.4)
    
    Returns:
    - float: Calculated permeate flux in kg/(m^2*h)
    """
    
    # Constants optimized via MATLAB (Table 4 in the reference paper)[cite: 9]
    a0 = -36.1488
    a1 = 1.2078       # Temperature coefficient[cite: 9]
    a2 = 6.1149       # Pressure linear coefficient[cite: 9]
    a3 = -0.0681      # Pressure quadratic coefficient[cite: 9]
    a4 = -0.1867      # Concentration linear coefficient[cite: 9]
    a5 = 0.0007       # Concentration quadratic coefficient[cite: 9]
    a6 = 1.4248       # Flow rate coefficient[cite: 9]
    
    # Governing polynomial equation for Permeate Flux[cite: 9]
    flux = (a0 
            + (a1 * temperature) 
            + (a2 * pressure) 
            + (a3 * (pressure ** 2)) 
            + (a4 * concentration) 
            + (a5 * (concentration ** 2)) 
            + (a6 * flow_rate))
    
    return flux

# --- Testing the Model with a Baseline Case ---
if __name__ == "__main__":
    # Let's test standard operating conditions reported in the paper:
    # Temperature = 25 °C, Pressure = 20 bar, Concentration = 25 ppm, Flow Rate = 3.2 L/min
    
    test_temp = 25.0
    test_pressure = 20.0
    test_conc = 25.0
    test_flow = 3.2
    
    result = calculate_permeate_flux(test_temp, test_pressure, test_conc, test_flow)
    
    print("--------------------------------------------------")
    print(" NickelRO Lab: Python Model Initialized Successfully ")
    print("--------------------------------------------------")
    print(f"Operating Conditions Tested:")
    print(f" - Temperature: {test_temp} °C")
    print(f" - Pressure:    {test_pressure} bar")
    print(f" - Concentration: {test_conc} ppm")
    print(f" - Flow Rate:   {test_flow} L/min")
    print(f"--------------------------------------------------")
    print(f"Predicted Permeate Flux: {result:.2f} kg/(m^2·h)")
    print("--------------------------------------------------")
    # ==============================================================================
# Project: NickelRO Lab
# Module: Permeate Flux and Nickel Rejection Calculation Models
# Reference: Shigidi et al. (2022), "Studying Different Operating Conditions on 
#            Reverse Osmosis Performance in the Treatment of Wastewater..."
# ==============================================================================

def calculate_permeate_flux(temperature, pressure, concentration, flow_rate):
    """
    Calculates the reverse osmosis permeate flux (kg / m^2 * h) 
    using the empirical polynomial model from Shigidi et al. (2022).[cite: 9]
    """
    a0 = -36.1488
    a1 = 1.2078       # Temperature coefficient[cite: 9]
    a2 = 6.1149       # Pressure linear coefficient[cite: 9]
    a3 = -0.0681      # Pressure quadratic coefficient[cite: 9]
    a4 = -0.1867      # Concentration linear coefficient[cite: 9]
    a5 = 0.0007       # Concentration quadratic coefficient[cite: 9]
    a6 = 1.4248       # Flow rate coefficient[cite: 9]
    
    flux = (a0 
            + (a1 * temperature) 
            + (a2 * pressure) 
            + (a3 * (pressure ** 2)) 
            + (a4 * concentration) 
            + (a5 * (concentration ** 2)) 
            + (a6 * flow_rate))
    
    return flux


def calculate_nickel_rejection(temperature, pressure, concentration, flow_rate):
    """
    Calculates the nickel ion rejection percentage (R %) 
    using the empirical cubic model from Shigidi et al. (2022).[cite: 10]
    
    Parameters:
    - temperature (float): Feed temperature in °C
    - pressure (float): Operating pressure in bar
    - concentration (float): Initial feed nickel concentration in ppm (C_F)
    - flow_rate (float): Feed flow rate in L/min
    
    Returns:
    - float: Calculated nickel rejection percentage (%)
    """
    # Constants optimized via MATLAB (Table 6 in the reference paper)[cite: 10]
    b0 = 16.7254
    b1 = -0.1830
    b2 = 0.0022
    b3 = -1.6601
    b4 = 0.0732
    b5 = -0.0010
    b6 = 0.1424
    b7 = -0.0006
    b8 = 1.1594e-6
    b9 = -0.6872
    b10 = 0.0274
    
    # Calculate the estimated permeate concentration numerator (Eq. 6 in reference)[cite: 10]
    cp_numerator = (b0 
                    + (b1 * temperature) 
                    + (b2 * (temperature ** 2)) 
                    + (b3 * pressure) 
                    + (b4 * (pressure ** 2)) 
                    + (b5 * (pressure ** 3)) 
                    + (b6 * concentration) 
                    + (b7 * (concentration ** 2)) 
                    + (b8 * (concentration ** 3)) 
                    + (b9 * flow_rate) 
                    + (b10 * (flow_rate ** 2)))
    
    # Rejection percentage formula: R% = (1 - (Cp / Cf)) * 100[cite: 3, 10]
    rejection_percentage = (1.0 - (cp_numerator / concentration)) * 100.0
    
    return rejection_percentage


# --- Testing the Complete Model ---
if __name__ == "__main__":
    test_temp = 25.0
    test_pressure = 20.0
    test_conc = 25.0
    test_flow = 3.2
    
    flux_result = calculate_permeate_flux(test_temp, test_pressure, test_conc, test_flow)
    rejection_result = calculate_nickel_rejection(test_temp, test_pressure, test_conc, test_flow)
    
    print("--------------------------------------------------")
    print(" NickelRO Lab: Dual-Model Python Script Test        ")
    print("--------------------------------------------------")
    print(f"Operating Conditions Tested:")
    print(f" - Temperature:   {test_temp} °C")
    print(f" - Pressure:      {test_pressure} bar")
    print(f" - Concentration: {test_conc} ppm")
    print(f" - Flow Rate:     {test_flow} L/min")
    print(f"--------------------------------------------------")
    print(f"Predicted Permeate Flux:     {flux_result:.2f} kg/(m^2·h)")
    print(f"Predicted Nickel Rejection:  {rejection_result:.2f} %")
    print("--------------------------------------------------")