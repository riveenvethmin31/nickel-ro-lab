# 🔬 NickelRO Lab: Advanced RO Performance & Energy Simulator

A research-grade digital twin web application for evaluating reverse osmosis (RO) performance and energy economics in heavy-metal wastewater treatment (specifically nickel-laden industrial effluent). 

🌐 **Live App:** https://nickel-ro-lab-gtnhrhpjkrtjnndw2dbfnf.streamlit.app/
---

## 🚀 Key Features
* **Empirical Modeling:** Implements rigorous performance models based on Shigidi et al. (2022) to calculate Permeate Flux ($J$) and Nickel Rejection ($R\%$).
* **Energy & Economic Analysis:** Computes Specific Energy Consumption (SEC in $\text{kWh/m}^3$) and volumetric treatment cost ($\$/\text{m}^3$) under varying operating pressures and feed concentrations.
* **Interactive Visualizations:** Dynamic pressure sweep curves, efficiency status alerts, and real-time operational metric tracking.
* **Data Export:** Automated CSV report generation for experimental and simulation data logging.

## 🛠️ Tech Stack
* **Language:** Python
* **Web Framework:** Streamlit
* **Data Science & Math:** Pandas, NumPy
* **Deployment:** GitHub, Streamlit Community Cloud

## 📂 Project Structure
```text
nickel-ro-lab/
│
├── app.py                  # Main Streamlit user interface & layout
├── nickel_ro_model.py      # Core thermodynamic, flux, rejection, and cost calculation engine
└── requirements.txt        # Python package dependencies
