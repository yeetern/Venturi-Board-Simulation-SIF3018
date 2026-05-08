import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Venturi Board Apparent Temperature Simulation",
    layout="wide"
)

st.title("Venturi Board Apparent Temperature Simulation")
st.caption(
    "A first-order model estimating how airflow enhancement changes apparent temperature "
    "at a semi-open food stall."
)

# =========================================================
# SIDEBAR INPUTS
# =========================================================

st.sidebar.header("Environmental Parameters")

T_air = st.sidebar.slider(
    "Ambient Temperature, T_air (°C)",
    25.0, 45.0, 34.0, 0.5
)

RH = st.sidebar.slider(
    "Relative Humidity, RH (%)",
    30.0, 100.0, 70.0, 1.0
)

wind_speed = st.sidebar.slider(
    "Outdoor Wind Speed, v_wind (m/s)",
    0.0, 8.0, 2.0, 0.1
)

wind_angle = st.sidebar.slider(
    "Wind Incident Angle, θ (degree)",
    0, 90, 20, 1
)

st.sidebar.header("Bottle / Board Parameters")

R_big_cm = st.sidebar.slider(
    "Large Opening Radius, R_big (cm)",
    3.5, 6.0, 4.5, 0.1
)

R_small_cm = st.sidebar.slider(
    "Small Neck Radius, R_small (cm)",
    1.2, 2.0, 1.5, 0.1
)

N_bottles = st.sidebar.slider(
    "Number of Bottles",
    1, 80, 36, 1
)

board_width_cm = st.sidebar.slider(
    "Board Width (cm)",
    30, 200, 30, 5
)

board_height_cm = st.sidebar.slider(
    "Board Height (cm)",
    30, 150, 120, 5
)

st.sidebar.header("Empirical Airflow Factors")

r_max = st.sidebar.slider(
    "Maximum Velocity Amplification, r",
    1.0, 5.0, 3.0, 0.1,
    help=(
        "Capped maximum amplification factor. "
        "The ideal area ratio may be larger, but the real passive system is limited."
    )
)

Cd = st.sidebar.slider(
    "Discharge Coefficient, Cd",
    0.30, 1.00, 0.70, 0.05,
    help="Represents friction, turbulence, leakage, and imperfect bottle geometry."
)

f_eff = st.sidebar.slider(
    "Effective Felt-Airflow Factor, f_eff",
    0.10, 1.00, 0.50, 0.05,
    help="Fraction of outlet airflow that effectively reaches the user."
)

# =========================================================
# CALCULATION FUNCTIONS
# =========================================================

def vapour_pressure_hpa(T_c: float, RH_percent: float) -> float:
    """
    Water vapour pressure in hPa.

    The 6.105 coefficient gives saturation vapour pressure in hPa.
    Therefore the Steadman coefficient used later is 0.33.
    """
    return (RH_percent / 100) * 6.105 * np.exp((17.27 * T_c) / (237.7 + T_c))


def apparent_temperature(T_c: float, RH_percent: float, v_ms: float) -> float:
    """
    Steadman apparent temperature approximation.

    AT = T_air + 0.33e - 0.70v - 4.00

    where:
    - T_air is in °C
    - e is water vapour pressure in hPa
    - v is local wind speed in m/s
    """
    e_hpa = vapour_pressure_hpa(T_c, RH_percent)
    return T_c + 0.33 * e_hpa - 0.70 * v_ms - 4.00

# =========================================================
# GEOMETRY AND AIRFLOW MODEL
# =========================================================

theta = np.deg2rad(wind_angle)

R_big = R_big_cm / 100
R_small = R_small_cm / 100
board_width = board_width_cm / 100
board_height = board_height_cm / 100

A_big = np.pi * R_big**2
A_small = np.pi * R_small**2
A_board = board_width * board_height

geometric_area_ratio = A_big / A_small if A_small > 0 else np.nan
used_amplification = min(geometric_area_ratio, r_max)

# Wind component normal to the board
v_eff = wind_speed * max(np.cos(theta), 0)

# Outlet and felt wind
v_out_ideal = used_amplification * v_eff
v_out = Cd * v_out_ideal
v_feel = f_eff * v_out

# Apparent temperature before and after
AT_before = apparent_temperature(T_air, RH, v_eff)
AT_after = apparent_temperature(T_air, RH, v_feel)
AT_change = AT_before - AT_after

# Geometry metrics
total_big_area = N_bottles * A_big
total_small_area = N_bottles * A_small
inlet_coverage = total_big_area / A_board if A_board > 0 else np.nan
throat_open_fraction = total_small_area / A_board if A_board > 0 else np.nan

# =========================================================
# MODEL SUMMARY
# =========================================================

st.subheader("1. Model Summary")

col1, col2 = st.columns([1.1, 1])

with col1:
    st.markdown(
        """
This model estimates how the Venturi board changes the **local wind speed felt by the user**, then uses the Steadman apparent temperature equation to estimate perceived comfort.

The simulation focuses on **apparent temperature reduction**, not actual air-temperature reduction.
"""
    )

    st.latex(r"v_{\mathrm{eff}} = v_{\mathrm{wind}}\cos\theta")
    st.latex(r"v_{\mathrm{feel}} = f_{\mathrm{eff}}\,C_d\,r\,v_{\mathrm{eff}}")
    st.latex(r"AT = T_{\mathrm{air}} + 0.33e - 0.70v - 4.00")

    st.caption(
        "Here, e is water vapour pressure in hPa, and v is the local wind speed used in the apparent temperature equation."
    )

with col2:
    summary_df = pd.DataFrame(
        {
            "Quantity": [
                "Ambient temperature",
                "Relative humidity",
                "Water vapour pressure",
                "Outdoor wind speed",
                "Effective incoming wind",
                "Felt wind after board",
                "Apparent temperature before",
                "Apparent temperature after",
                "Apparent cooling effect",
            ],
            "Value": [
                f"{T_air:.1f} °C",
                f"{RH:.0f} %",
                f"{vapour_pressure_hpa(T_air, RH):.2f} hPa",
                f"{wind_speed:.2f} m/s",
                f"{v_eff:.2f} m/s",
                f"{v_feel:.2f} m/s",
                f"{AT_before:.2f} °C",
                f"{AT_after:.2f} °C",
                f"{max(AT_change, 0):.2f} °C",
            ],
        }
    )
    st.dataframe(summary_df, hide_index=True, use_container_width=True)

# =========================================================
# KEY METRICS
# =========================================================

st.subheader("2. Key Output")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Effective Incoming Wind", f"{v_eff:.2f} m/s")
m2.metric("Felt Wind After Board", f"{v_feel:.2f} m/s")
m3.metric("AT Before", f"{AT_before:.2f} °C")
m4.metric("AT After", f"{AT_after:.2f} °C", delta=f"{-AT_change:.2f} °C")

st.metric(
    "Estimated Apparent Cooling Effect",
    f"{max(AT_change, 0):.2f} °C",
    help="Positive value means the model predicts lower apparent temperature after installation."
)

if AT_change <= 0:
    st.warning(
        "Under the current settings, the model does not predict an apparent cooling improvement. "
        "This usually means the felt wind after the board is not higher than the baseline effective wind."
    )
elif AT_change < 0.7:
    st.info("The predicted apparent cooling effect is small under the current settings.")
elif AT_change <= 2.0:
    st.success("The predicted apparent cooling effect is within the expected 0.7–2.0 °C range.")
else:
    st.warning(
        "The predicted apparent cooling effect is above 2.0 °C. "
        "Check whether r, Cd, or f_eff is too optimistic."
    )

# =========================================================
# USEFUL PLOTS
# =========================================================

st.subheader("3. Useful Plots")

# Plot 1: AT vs local wind speed
local_wind_range = np.linspace(0, 8, 200)
AT_local_wind = np.array([apparent_temperature(T_air, RH, v) for v in local_wind_range])

fig1, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.plot(local_wind_range, AT_local_wind, linewidth=2)
ax1.scatter([v_eff], [AT_before], s=80, label="Before installation")
ax1.scatter([v_feel], [AT_after], s=80, label="After installation")
ax1.set_xlabel("Local wind speed used in AT equation, v (m/s)")
ax1.set_ylabel("Apparent temperature, AT (°C)")
ax1.set_title(f"Apparent Temperature vs Wind Speed\nT = {T_air:.1f} °C, RH = {RH:.0f}% held constant")
ax1.grid(True, alpha=0.3)
ax1.legend()
st.pyplot(fig1, use_container_width=True)

st.caption(
    "This is the cleanest graph for presentation: temperature and humidity are fixed, "
    "so the curve shows only how apparent temperature changes with wind speed."
)

# Plot 2: Before vs after AT
before_after_df = pd.DataFrame(
    {
        "Case": ["Before", "After"],
        "Apparent Temperature (°C)": [AT_before, AT_after],
    }
)

fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.bar(before_after_df["Case"], before_after_df["Apparent Temperature (°C)"])
ax2.set_ylabel("Apparent temperature, AT (°C)")
ax2.set_title("Before vs After Apparent Temperature")
ax2.grid(axis="y", alpha=0.3)

for i, value in enumerate(before_after_df["Apparent Temperature (°C)"]):
    ax2.text(i, value, f"{value:.2f} °C", ha="center", va="bottom")

st.pyplot(fig2, use_container_width=True)

# Plot 3: Outdoor wind sweep
wind_range = np.linspace(0, 8, 200)
v_eff_sweep = wind_range * max(np.cos(theta), 0)
v_feel_sweep = f_eff * Cd * used_amplification * v_eff_sweep
AT_before_sweep = np.array([apparent_temperature(T_air, RH, v) for v in v_eff_sweep])
AT_after_sweep = np.array([apparent_temperature(T_air, RH, v) for v in v_feel_sweep])
AT_improvement_sweep = AT_before_sweep - AT_after_sweep

fig3, ax3 = plt.subplots(figsize=(8, 4.5))
ax3.plot(wind_range, AT_improvement_sweep, linewidth=2)
ax3.axhspan(0.7, 2.0, alpha=0.15, label="Expected useful range: 0.7–2.0 °C")
ax3.axhline(0, linestyle="--", linewidth=1)
ax3.set_xlabel("Outdoor wind speed, v_wind (m/s)")
ax3.set_ylabel("Apparent cooling effect, ΔAT (°C)")
ax3.set_title("Predicted Apparent Cooling Effect vs Outdoor Wind Speed")
ax3.grid(True, alpha=0.3)
ax3.legend()
st.pyplot(fig3, use_container_width=True)

# =========================================================
# DESIGN CHECKS
# =========================================================

st.subheader("4. Design Checks")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Geometric Area Ratio", f"{geometric_area_ratio:.2f}")
c2.metric("Used Amplification r", f"{used_amplification:.2f}")
c3.metric("Inlet Coverage", f"{inlet_coverage * 100:.1f}%")
c4.metric("Throat Open Fraction", f"{throat_open_fraction * 100:.1f}%")

if inlet_coverage > 1:
    st.error("Bottle inlet area exceeds board area. The bottle layout is physically impossible without overlap.")
elif inlet_coverage > 0.85:
    st.warning("Bottle inlet coverage is very high. Check whether bottles can physically fit on the board.")
else:
    st.success("Bottle inlet coverage is within a physically reasonable range.")

if geometric_area_ratio > r_max:
    st.info(
        "The ideal geometric area ratio is larger than the chosen maximum amplification. "
        "The model uses the capped empirical value r instead of the full ideal area ratio."
    )

# =========================================================
# EXPORTABLE TABLE
# =========================================================

st.subheader("5. Presentation Table")

presentation_df = pd.DataFrame(
    {
        "Parameter / Result": [
            "Ambient temperature",
            "Relative humidity",
            "Outdoor wind speed",
            "Wind incident angle",
            "Discharge coefficient",
            "Amplification factor used",
            "Effective airflow factor",
            "Effective wind before",
            "Felt wind after",
            "Apparent temperature before",
            "Apparent temperature after",
            "Apparent cooling effect",
        ],
        "Value": [
            f"{T_air:.1f} °C",
            f"{RH:.0f} %",
            f"{wind_speed:.2f} m/s",
            f"{wind_angle:.0f}°",
            f"{Cd:.2f}",
            f"{used_amplification:.2f}",
            f"{f_eff:.2f}",
            f"{v_eff:.2f} m/s",
            f"{v_feel:.2f} m/s",
            f"{AT_before:.2f} °C",
            f"{AT_after:.2f} °C",
            f"{max(AT_change, 0):.2f} °C",
        ],
    }
)

st.dataframe(presentation_df, hide_index=True, use_container_width=True)

csv = presentation_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download presentation table as CSV",
    data=csv,
    file_name="venturi_apparent_temperature_results.csv",
    mime="text/csv",
)

# =========================================================
# ASSUMPTIONS
# =========================================================

with st.expander("Assumptions and Limitations"):
    st.markdown(
        """
- Incoming wind is assumed steady during each simulation case.
- Wind direction matters; only the component normal to the board is used.
- Air density is treated as approximately constant.
- Bottles are assumed identical.
- The velocity amplification factor is capped instead of using the full ideal area ratio.
- Losses are represented by the discharge coefficient, Cd.
- Airflow spreading and distance from the board are represented by f_eff.
- Apparent temperature is used as the comfort indicator.
- The model is not CFD and does not prove actual air-temperature reduction.
"""
    )
