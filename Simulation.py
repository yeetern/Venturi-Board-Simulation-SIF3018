import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Venturi Board Ventilation Simulation",
    layout="wide"
)

st.title("Venturi Board Ventilation Simulation")
st.caption(
    "A simplified physics-based hypothesis model for food stall ventilation using a plastic-bottle Venturi board."
)

# =========================================================
# SIDEBAR INPUTS
# =========================================================

st.sidebar.header("Environmental Parameters")

T_in = st.sidebar.slider("Ambient Temperature, T_in (°C)", 25.0, 45.0, 34.0, 0.5)
RH = st.sidebar.slider("Relative Humidity, RH (%)", 30.0, 100.0, 70.0, 1.0)
wind_speed = st.sidebar.slider("Outdoor Wind Speed (m/s)", 0.0, 8.0, 2.0, 0.1)
wind_angle = st.sidebar.slider("Wind Angle Relative to Board Normal (degree)", 0, 90, 20, 1)

st.sidebar.header("Venturi Bottle Parameters")

R_big_cm = st.sidebar.slider("Large Radius of Bottle, R_big (cm)", 3.5, 6.0, 4.5, 0.1)
R_small_cm = st.sidebar.slider("Small Radius of Bottle Neck, R_small (cm)", 1.2, 2.0, 1.5, 0.1)
N_bottles = st.sidebar.slider("Number of Bottles", 1, 80, 45, 1)
Cd = st.sidebar.slider("Discharge Coefficient, Cd", 0.30, 1.00, 0.70, 0.05)

st.sidebar.header("Board Geometry")

board_width_cm = st.sidebar.slider("Board Width (cm)", 100, 200, 150, 5)
board_height_cm = st.sidebar.slider("Board Height (cm)", 20, 60, 30, 5)

max_speed_ratio = st.sidebar.slider("Maximum Allowed Speed Amplification", 1.0, 5.0, 3.0, 0.1)

# =========================================================
# UNIT CONVERSION
# =========================================================

R_big = R_big_cm / 100
R_small = R_small_cm / 100
board_width = board_width_cm / 100
board_height = board_height_cm / 100

# =========================================================
# GEOMETRY CALCULATION
# =========================================================

theta = np.deg2rad(wind_angle)

A_board = board_width * board_height
A_big = np.pi * R_big**2
A_small = np.pi * R_small**2

total_big_area = N_bottles * A_big
total_small_area = N_bottles * A_small

radius_ratio = R_big / R_small
area_ratio = A_big / A_small

open_area_ratio = total_big_area / A_board if A_board > 0 else 0
blockage_ratio = 1 - open_area_ratio
blockage_ratio = max(min(blockage_ratio, 1), 0)

# =========================================================
# AIRFLOW MODEL
# =========================================================

v_effective = wind_speed * max(np.cos(theta), 0)

v_out_ideal = v_effective * area_ratio
v_out = Cd * v_out_ideal
v_out = min(v_out, max_speed_ratio * wind_speed)

Q_open = A_board * v_effective
Q_venturi = total_small_area * v_out

airflow_ratio = Q_venturi / Q_open if Q_open > 0 else 0

# =========================================================
# THERMAL COMFORT MODEL
# =========================================================

if v_out > 0 and T_in > 26:
    cooling_effect = (
        0.7
        * (v_out ** 0.7)
        * (1 - RH / 100)
        * (T_in - 26)
    )
else:
    cooling_effect = 0

cooling_effect = max(cooling_effect, 0)
cooling_effect = min(cooling_effect, 6.0)

T_perceived = T_in - cooling_effect

# =========================================================
# MAIN RESULTS
# =========================================================

st.subheader("Simulation Results")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Effective Incoming Wind", f"{v_effective:.2f} m/s")
col2.metric("Outlet Wind Speed", f"{v_out:.2f} m/s")
col3.metric("Open-Area Airflow", f"{Q_open:.3f} m³/s")
col4.metric("Venturi Airflow", f"{Q_venturi:.3f} m³/s")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Airflow Ratio", f"{airflow_ratio:.2f}")
col6.metric("Blockage Ratio", f"{blockage_ratio * 100:.1f}%")
col7.metric("Estimated Cooling Effect", f"{cooling_effect:.2f} °C")
col8.metric("Perceived Temperature", f"{T_perceived:.2f} °C")

# =========================================================
# GEOMETRY RESULTS
# =========================================================

st.subheader("Geometry and Design Parameters")

col9, col10, col11, col12 = st.columns(4)
col9.metric("Board Size", f"{board_width_cm} cm × {board_height_cm} cm")
col10.metric("Number of Bottles", f"{N_bottles}")
col11.metric("Radius Ratio", f"{radius_ratio:.2f}")
col12.metric("Area Ratio", f"{area_ratio:.2f}")

col13, col14, col15, col16 = st.columns(4)
col13.metric("Large Radius", f"{R_big_cm:.1f} cm")
col14.metric("Small Radius", f"{R_small_cm:.1f} cm")
col15.metric("Bottle Coverage", f"{open_area_ratio * 100:.1f}%")
col16.metric("Board Area", f"{A_board:.3f} m²")

# =========================================================
# PHYSICAL INTERPRETATION
# =========================================================

st.subheader("Physical Interpretation")

if wind_speed == 0:
    st.info("No external wind is present. A passive Venturi board cannot generate airflow without incoming wind.")
elif airflow_ratio < 0.5:
    st.error(
        "The Venturi board strongly reduces total airflow. "
        "Although local outlet wind speed increases, whole-stall ventilation may become worse."
    )
elif airflow_ratio < 1.0:
    st.warning(
        "The Venturi board increases local outlet wind speed, but total airflow is lower than the open-area case."
    )
else:
    st.success(
        "The Venturi board gives comparable or higher airflow than the open-area case in this simplified model."
    )

if blockage_ratio > 0.70:
    st.warning(
        "High blockage ratio: most of the board blocks incoming wind. "
        "Try increasing bottle coverage or reducing the board area."
    )

if open_area_ratio > 0.85:
    st.warning(
        "Bottle coverage is very high. Check whether the bottles can physically fit without overlap."
    )

if radius_ratio > 4:
    st.warning("The radius ratio is large. Check whether the bottle geometry is physically realistic.")

if wind_angle > 60:
    st.warning(
        "Large wind angle: the wind is not hitting the board directly, so effective airflow is strongly reduced."
    )

st.markdown(
    """
### Model meaning

This model separates two effects:

1. **Local velocity increase**  
   The smaller bottle neck can increase local outlet wind speed.

2. **Global blockage effect**  
   The board blocks part of the incoming wind, so the total airflow may decrease.

For your prototype, the design goal is not only to increase wind speed, but also to maximize the usable bottle coverage on the board.
"""
)

# =========================================================
# DETAILED TABLE
# =========================================================

st.subheader("Detailed Parameters and Results")

data = {
    "Quantity": [
        "Ambient temperature",
        "Relative humidity",
        "Outdoor wind speed",
        "Wind angle",
        "Effective incoming wind",
        "Board width",
        "Board height",
        "Board area",
        "Large bottle radius",
        "Small bottle radius",
        "Number of bottles",
        "Single large opening area",
        "Single small opening area",
        "Total large opening area",
        "Total small opening area",
        "Bottle coverage",
        "Blockage ratio",
        "Radius ratio",
        "Area ratio",
        "Discharge coefficient",
        "Ideal outlet wind speed",
        "Capped outlet wind speed",
        "Open-area airflow",
        "Venturi airflow",
        "Airflow ratio",
        "Estimated cooling effect",
        "Actual temperature",
        "Perceived temperature"
    ],
    "Value": [
        f"{T_in:.2f} °C",
        f"{RH:.1f} %",
        f"{wind_speed:.2f} m/s",
        f"{wind_angle:.1f}°",
        f"{v_effective:.3f} m/s",
        f"{board_width:.2f} m",
        f"{board_height:.2f} m",
        f"{A_board:.3f} m²",
        f"{R_big_cm:.2f} cm",
        f"{R_small_cm:.2f} cm",
        f"{N_bottles}",
        f"{A_big:.5f} m²",
        f"{A_small:.5f} m²",
        f"{total_big_area:.5f} m²",
        f"{total_small_area:.5f} m²",
        f"{open_area_ratio * 100:.2f} %",
        f"{blockage_ratio * 100:.2f} %",
        f"{radius_ratio:.3f}",
        f"{area_ratio:.3f}",
        f"{Cd:.2f}",
        f"{v_out_ideal:.3f} m/s",
        f"{v_out:.3f} m/s",
        f"{Q_open:.5f} m³/s",
        f"{Q_venturi:.5f} m³/s",
        f"{airflow_ratio:.3f}",
        f"{cooling_effect:.3f} °C",
        f"{T_in:.2f} °C",
        f"{T_perceived:.2f} °C"
    ]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# =========================================================
# CHARTS
# =========================================================

st.subheader("Airflow Comparison")

airflow_df = pd.DataFrame({
    "Case": ["Open Area", "Venturi Board"],
    "Airflow Rate (m³/s)": [Q_open, Q_venturi]
})

st.bar_chart(airflow_df.set_index("Case"))

st.subheader("Temperature Comparison")

temp_df = pd.DataFrame({
    "Case": ["Actual Air Temperature", "Perceived Temperature"],
    "Temperature (°C)": [T_in, T_perceived]
})

st.bar_chart(temp_df.set_index("Case"))

# =========================================================
# SENSITIVITY ANALYSIS
# =========================================================

st.subheader("Wind Speed Sensitivity")

wind_range = np.linspace(0, 8, 50)
cooling_list = []
vout_list = []
qventuri_list = []

for v in wind_range:
    v_eff = v * max(np.cos(theta), 0)
    v_ideal = v_eff * area_ratio
    v_real = Cd * v_ideal
    v_real = min(v_real, max_speed_ratio * v)

    q_v = total_small_area * v_real

    if v_real > 0 and T_in > 26:
        cool = 0.7 * (v_real ** 0.7) * (1 - RH / 100) * (T_in - 26)
    else:
        cool = 0

    cool = max(cool, 0)
    cool = min(cool, 6.0)

    vout_list.append(v_real)
    cooling_list.append(cool)
    qventuri_list.append(q_v)

sensitivity_df = pd.DataFrame({
    "Outdoor Wind Speed (m/s)": wind_range,
    "Outlet Wind Speed (m/s)": vout_list,
    "Venturi Airflow (m³/s)": qventuri_list,
    "Estimated Cooling Effect (°C)": cooling_list
})

st.line_chart(sensitivity_df.set_index("Outdoor Wind Speed (m/s)"))

# =========================================================
# ASSUMPTIONS
# =========================================================

st.subheader("Assumptions and Limitations")

st.markdown(
    """
- The model assumes steady incoming wind.
- Only the wind component perpendicular to the board is used.
- The Venturi effect is approximated using the continuity equation.
- Energy losses are represented by the discharge coefficient, Cd.
- Unrealistic velocity amplification is capped.
- Bottle coverage is estimated from total large-opening area divided by board area.
- The board may increase local wind speed but reduce total airflow.
- The cooling effect is a perceived thermal comfort estimate, not true air temperature reduction.
- The model does not solve turbulence, recirculation, cooking heat, side leakage, or full CFD.
- Real experimental data is required for calibration.
"""
)

# =========================================================
# PROJECT STATEMENT
# =========================================================

st.subheader("Suggested Project Statement")

st.info(
    "This simulation acts as a physics-based hypothesis model. "
    "It predicts how a plastic-bottle Venturi board may change local outlet wind speed, "
    "total airflow rate, blockage ratio, bottle coverage, and perceived thermal comfort. "
    "The predicted results can later be compared with real measurements before and after installation."
)