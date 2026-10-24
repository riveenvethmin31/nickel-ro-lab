import streamlit as st
import pandas as pd
import numpy as np
from nickel_ro_model import calculate_permeate_flux, calculate_nickel_rejection

# Page Configuration
st.set_page_config(
    page_title="NickelRO Lab Pro", 
    page_icon="🧪", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# App Title & Header
st.title("🧪 NickelRO Lab: Advanced RO Performance & Energy Simulator")
st.caption("Research-Grade Digital Twin for Heavy Metal Wastewater Treatment | Shigidi et al. (2022) Model")
st.markdown("---")

# Sidebar Controls
st.sidebar.header("⚙️ Operating Parameters")
temp = st.sidebar.slider("Feed Temperature (°C)", 25.0, 45.0, 25.0, 1.0)
pressure = st.sidebar.slider("Operating Pressure (bar)", 10.0, 40.0, 20.0, 1.0)
concentration = st.sidebar.slider("Initial Nickel Concentration (ppm)", 25.0, 150.0, 25.0, 5.0)
flow_rate = st.sidebar.slider("Feed Flow Rate (L/min)", 2.0, 4.4, 3.2, 0.2)

st.sidebar.markdown("---")
st.sidebar.header("💡 Economic Assumptions")
pump_efficiency = st.sidebar.slider("High-Pressure Pump Efficiency (%)", 50.0, 85.0, 75.0, 5.0) / 100.0
elec_cost = st.sidebar.slider("Electricity Tariff ($/kWh)", 0.05, 0.30, 0.12, 0.01)

# Current single point calculations
flux = calculate_permeate_flux(temp, pressure, concentration, flow_rate)
rejection = calculate_nickel_rejection(temp, pressure, concentration, flow_rate)

# Specific Energy Consumption (SEC in kWh/m3 permeate)
# SEC ≈ (Pressure in bar * 100 kPa/bar) / (3600 * pump_efficiency * recovery_ratio)
# Assuming baseline recovery ratio ~ 0.50
sec = (pressure * 100) / (3600 * pump_efficiency * 0.50)  
cost_per_m3 = sec * elec_cost

# Multi-Tab Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Live Simulator & Energy", 
    "🔬 Sensitivity Studies", 
    "📥 Data Export & Report", 
    "📖 Model Documentation"
])

# TAB 1: Live Simulator & Pressure Sweeps
with tab1:
    st.markdown("### 🎯 Live System Performance & Operational Cost")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Permeate Flux (J)", value=f"{flux:.2f} kg/(m²·h)")
    with col2:
        st.metric(label="Nickel Rejection (R)", value=f"{rejection:.2f} %")
    with col3:
        st.metric(label="Specific Energy (SEC)", value=f"{sec:.2f} kWh/m³")
    with col4:
        st.metric(label="Treatment Cost", value=f"${cost_per_m3:.3f} / m³")

    if rejection >= 90.0:
        st.success("✅ High Separation Efficiency (>90%)")
    elif rejection >= 80.0:
        st.warning("⚠️ Moderate Separation Efficiency (80–90%)")
    else:
        st.error("🚨 Low Separation Efficiency (<80%)")

    st.markdown("---")
    st.markdown("### 📈 Pressure Sweep Analysis (10–40 bar)")
    
    pressures = np.linspace(10.0, 40.0, 31)
    flux_list, rej_list, sec_list = [], [], []
    for p in pressures:
        f_val = calculate_permeate_flux(temp, p, concentration, flow_rate)
        r_val = calculate_nickel_rejection(temp, p, concentration, flow_rate)
        s_val = (p * 100) / (3600 * pump_efficiency * 0.50)
        
        flux_list.append(f_val)
        rej_list.append(r_val)
        sec_list.append(s_val)
        
    df_press = pd.DataFrame({
        "Pressure (bar)": pressures,
        "Permeate Flux (kg/m²·h)": flux_list,
        "Nickel Rejection (%)": rej_list,
        "Energy Consumption (kWh/m³)": sec_list
    }).set_index("Pressure (bar)")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("**Permeate Flux vs. Pressure**")
        st.line_chart(df_press[["Permeate Flux (kg/m²·h)"]])
    with col_c2:
        st.markdown("**Energy Consumption (SEC) vs. Pressure**")
        st.line_chart(df_press[["Energy Consumption (kWh/m³)"]])

# TAB 2: Sensitivity Studies
with tab2:
    st.markdown("### 🔬 Temperature Sensitivity Study (25–45 °C)")
    
    temps = np.linspace(25.0, 45.0, 21)
    t_flux, t_rej = [], []
    for t in temps:
        t_flux.append(calculate_permeate_flux(t, pressure, concentration, flow_rate))
        t_rej.append(calculate_nickel_rejection(t, pressure, concentration, flow_rate))
        
    df_temp = pd.DataFrame({
        "Temperature (°C)": temps,
        "Permeate Flux (kg/m²·h)": t_flux,
        "Nickel Rejection (%)": t_rej
    }).set_index("Temperature (°C)")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**Permeate Flux vs. Temperature**")
        st.line_chart(df_temp[["Permeate Flux (kg/m²·h)"]])
    with col_t2:
        st.markdown("**Nickel Rejection vs. Temperature**")
        st.line_chart(df_temp[["Nickel Rejection (%)"]])

# TAB 3: Data Export
with tab3:
    st.markdown("### 📥 Export Simulation Data")
    st.markdown("Download the full pressure sweep and energy consumption dataset.")
    
    df_export = pd.DataFrame({
        "Pressure_bar": pressures,
        "Temperature_C": temp,
        "Feed_Concentration_ppm": concentration,
        "Flow_Rate_Lmin": flow_rate,
        "Permeate_Flux_kg_m2h": flux_list,
        "Nickel_Rejection_pct": rej_list,
        "SEC_kWh_m3": sec_list,
        "Cost_per_m3_USD": [s * elec_cost for s in sec_list]
    })
    
    st.dataframe(df_export, use_container_width=True)
    
    csv_data = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Download Full Technical & Cost Analysis CSV",
        data=csv_data,
        file_name="nickel_ro_energy_simulation.csv",
        mime="text/csv"
    )

# TAB 4: Model Documentation
with tab4:
    st.markdown("### 📚 Research Model Documentation")
    st.markdown("""
    * **Source Publication:** Shigidi et al. (2022), *Membranes*, PMC9695154.
    * **Process:** Reverse Osmosis (RO) treatment of wastewater containing Nickel (II) ions.
    * **Empirical Model Structure:**
      * **Permeate Flux ($J$):** Multi-variable polynomial empirical response model.
      * **Nickel Rejection ($R\%$):** Cubic polynomial empirical model.
      * **Energy Model:** Specific Energy Consumption (SEC) derived from hydrodynamic pressure requirements and pumping efficiency parameters.
    """)

st.markdown("---")
st.caption("NickelRO Lab Pro v1.1 | Energy & Performance Digital Twin")