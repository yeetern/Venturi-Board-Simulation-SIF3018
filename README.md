# Venturi Board Ventilation Simulation

A simplified physics-based simulation for evaluating airflow behavior and perceived thermal comfort in a tropical food stall environment using a **plastic-bottle Venturi board**.

This project investigates whether a low-cost passive ventilation prototype can improve **localized airflow** and **perceived cooling** for food stall workers under hot and humid outdoor conditions.

---

## 1. Project Overview

This simulation was developed as part of a *Physics for Work* project, where fundamental physics principles are applied to real-world workplace problems.

The prototype concept is based on a board fitted with recycled plastic bottles. Each bottle acts as a simplified nozzle: air enters through a larger opening and exits through a smaller neck. The model estimates whether this geometry can increase local outlet wind speed and improve perceived thermal comfort.

The simulation follows the simplified pipeline:

```text
Geometry → Airflow → Local Velocity → Perceived Cooling
````

The model is intended as a **hypothesis-generation tool** before prototype testing. It is not intended to replace experimental measurements or full Computational Fluid Dynamics (CFD).

---

## 2. Research Question

The main question addressed by this simulation is:

> Does a plastic-bottle Venturi board improve overall ventilation, or does it mainly produce localized high-speed airflow?

This distinction is important because a Venturi-like geometry may increase local outlet velocity while simultaneously reducing total airflow due to blockage.

---

## 3. Model Capabilities

The Streamlit dashboard estimates:

* Effective incoming wind speed
* Outlet wind speed
* Open-area airflow rate
* Venturi-board airflow rate
* Airflow ratio
* Bottle coverage ratio
* Blockage ratio
* Estimated perceived cooling effect
* Perceived temperature
* Sensitivity of performance to wind speed

These outputs allow the user to compare the ideal open-area case with the proposed Venturi-board configuration.

---

## 4. Environmental Context

The model is designed for tropical outdoor food stall conditions, such as those commonly found in Kampung Baru, Kuala Lumpur.

Typical operating conditions include:

| Parameter                           | Typical Range |
| ----------------------------------- | ------------: |
| Ambient temperature                 |       30–35°C |
| Relative humidity                   |        70–90% |
| Outdoor wind speed                  |   0.5–2.0 m/s |
| Wind angle relative to board normal |         0–60° |

### Key Implication

High humidity and low natural wind speed limit the performance of passive cooling systems. Therefore, the design should not be expected to reduce actual air temperature significantly. Instead, its main potential benefit is improving **localized perceived cooling** through directed airflow.

---

## 5. Physical Model

### 5.1 Wind Direction Correction

Only the wind component normal to the board is assumed to contribute to flow through the bottle openings:

```math
v_{\text{effective}} = v_{\text{wind}}\cos\theta
```

where:

* (v_{\text{wind}}) is the outdoor wind speed
* (\theta) is the wind angle relative to the board normal
* (v_{\text{effective}}) is the usable incoming wind speed

When the wind hits the board directly, (\theta = 0^\circ), and the effective wind speed is maximum. When the wind is nearly parallel to the board, the effective flow through the bottles becomes small.

---

### 5.2 Continuity-Based Velocity Estimate

The outlet velocity is estimated using the continuity equation:

```math
A_1 v_1 = A_2 v_2
```

For a bottle-nozzle approximation:

```math
v_{\text{out, ideal}} = v_{\text{effective}} \frac{A_{\text{big}}}{A_{\text{small}}}
```

where:

* (A_{\text{big}}) is the large bottle opening area
* (A_{\text{small}}) is the bottle neck area
* (v_{\text{out, ideal}}) is the ideal outlet velocity

Since real airflow involves losses, the model introduces a discharge coefficient:

```math
v_{\text{out}} = C_d v_{\text{out, ideal}}
```

or:

```math
v_{\text{out}} = C_d v_{\text{effective}} \frac{A_{\text{big}}}{A_{\text{small}}}
```

where:

* (C_d) is the discharge coefficient
* (0 < C_d \leq 1)
* lower (C_d) represents stronger losses due to friction, turbulence, separation, and imperfect bottle geometry

To avoid unrealistic velocity predictions, the outlet velocity is capped by a maximum speed amplification factor.

---

### 5.3 Airflow Rate Comparison

The model compares two airflow cases.

#### Case 1: Open Area

The open-area case represents the airflow that would pass through the same board area if there were no blockage:

```math
Q_{\text{open}} = A_{\text{board}} v_{\text{effective}}
```

#### Case 2: Venturi Board

The Venturi-board airflow is estimated using the total neck area of all bottles:

```math
Q_{\text{venturi}} = N A_{\text{small}} v_{\text{out}}
```

where:

* (N) is the number of bottles
* (A_{\text{small}}) is the area of one bottle neck
* (v_{\text{out}}) is the estimated outlet velocity

The airflow ratio is then:

```math
\text{Airflow Ratio} = \frac{Q_{\text{venturi}}}{Q_{\text{open}}}
```

This ratio helps determine whether the board improves total airflow or mainly produces localized velocity enhancement.

---

## 6. Geometry Model

The board area is calculated as:

```math
A_{\text{board}} = W \times H
```

The circular bottle opening areas are:

```math
A_{\text{big}} = \pi R_{\text{big}}^2
```

```math
A_{\text{small}} = \pi R_{\text{small}}^2
```

The bottle coverage ratio is:

```math
\text{Coverage Ratio} = \frac{N A_{\text{big}}}{A_{\text{board}}}
```

The blockage ratio is:

```math
\text{Blockage Ratio} = 1 - \text{Coverage Ratio}
```

A high blockage ratio means that most of the board blocks incoming wind. This may reduce total ventilation even if the bottle necks increase local outlet speed.

---

## 7. Perceived Thermal Comfort Model

The simulation uses a simplified empirical perceived-cooling approximation:

```math
\Delta T_{\text{cool}} =
0.7 v_{\text{out}}^{0.7}
\left(1 - \frac{RH}{100}\right)
(T_{\text{in}} - 26)
```

The perceived temperature is then estimated as:

```math
T_{\text{perceived}} = T_{\text{in}} - \Delta T_{\text{cool}}
```

where:

* (v_{\text{out}}) is the estimated outlet wind speed
* (RH) is the relative humidity in percent
* (T_{\text{in}}) is the ambient temperature
* (26^\circ\text{C}) is treated as an assumed comfort baseline
* (\Delta T_{\text{cool}}) is the estimated perceived cooling effect

### Important Clarification

This formula is **not a standard ASHRAE PMV/SET model** and is **not the NOAA heat index equation**. It is a project-specific empirical approximation based on physical assumptions:

1. Higher air speed improves convective and evaporative cooling.
2. Higher humidity reduces evaporative cooling effectiveness.
3. Cooling benefit becomes more relevant when ambient temperature exceeds a comfort baseline.
4. The cooling effect is perceived cooling, not actual thermodynamic air temperature reduction.

Therefore, the model should be interpreted as a **thermal comfort proxy**, not a validated human comfort index.

---

## 8. Prototype Configuration

Typical simulation parameters:

| Parameter                   |      Typical Value |
| --------------------------- | -----------------: |
| Board dimensions            | 120–150 cm × 30 cm |
| Large bottle radius         |         4.5–5.0 cm |
| Bottle neck radius          |         1.5–1.6 cm |
| Number of bottles           |              36–45 |
| Discharge coefficient       |            0.6–0.8 |
| Maximum speed amplification |               2–3× |

### Design Objective

The design aims to balance two competing effects:

1. **Velocity enhancement**
   A smaller outlet area can increase local outlet wind speed.

2. **Blockage reduction**
   Excessive board blockage can reduce total airflow.

The best design is therefore not necessarily the one with the highest speed amplification, but the one that provides useful directed airflow without excessively blocking the incoming wind.

---

## 9. Assumptions

### 9.1 Airflow Assumptions

* The incoming wind is steady.
* Only the wind component normal to the board is considered.
* The bottle geometry is approximated as a simplified nozzle.
* The continuity equation is used as a first-order approximation.
* Energy losses are represented by a single discharge coefficient, (C_d).
* Unrealistic outlet velocities are limited using a maximum amplification cap.

### 9.2 Geometry Assumptions

* Bottles are uniformly distributed across the board.
* Bottle openings are approximated as circular.
* Bottle overlap and structural interference are not fully modeled.
* The total open area is estimated from the sum of bottle opening areas.

### 9.3 Thermal Comfort Assumptions

* Increased outlet velocity improves perceived cooling.
* Higher relative humidity reduces evaporative cooling.
* The cooling effect is expressed as an equivalent perceived temperature reduction.
* Radiative heat from cooking equipment is not included.
* Human factors such as clothing, metabolic rate, and sweating rate are not included.

---

## 10. Limitations

This model has several important limitations:

* It is not a CFD simulation.
* It does not solve the Navier–Stokes equations.
* It does not model turbulence, recirculation, vortex shedding, or flow separation.
* It does not include cooking heat, solar radiation, or radiant heat from hot surfaces.
* It does not simulate full spatial airflow distribution inside the stall.
* The perceived cooling equation is not a validated thermal comfort standard.
* The discharge coefficient and cooling parameters require experimental calibration.

### Critical Limitation

The model should be treated as an **upper-bound and first-order estimate**, not an exact prediction of real-world performance.

---

## 11. Expected Findings

Based on the simplified model, the following behavior is expected:

1. The Venturi-board configuration can increase local outlet wind speed.
2. Total airflow may decrease if blockage is too high.
3. High humidity reduces the effectiveness of perceived cooling.
4. Wind direction strongly affects performance.
5. The system is more likely to improve localized comfort than reduce ambient air temperature.

### Main Interpretation

The plastic-bottle Venturi board should be evaluated primarily as a **localized airflow and perceived-cooling device**, not as a system that lowers the actual surrounding air temperature.

---

## 12. Experimental Validation Plan

To validate the model, real measurements should be collected before and after prototype installation.

Suggested measurements:

* Wind speed before installation
* Wind speed after installation
* Outlet wind speed at bottle necks
* Temperature near the vendor working area
* Relative humidity
* Vendor comfort feedback

A simple feedback scale can be used:

| Rating | Comfort Description |
| -----: | ------------------- |
|      1 | Very uncomfortable  |
|      2 | Uncomfortable       |
|      3 | Neutral             |
|      4 | Slightly improved   |
|      5 | Clearly improved    |

Experimental data can then be used to calibrate:

* Discharge coefficient, (C_d)
* Cooling coefficient
* Velocity exponent
* Humidity correction factor

---

## 13. Future Improvements

Possible improvements include:

* Calibrating the model using experimental data
* Replacing the custom cooling approximation with PMV or SET-based comfort calculations
* Adding radiant heat effects from cooking equipment
* Comparing different bottle layouts
* Comparing different hole sizes and spacing
* Testing different board angles relative to incoming wind
* Performing CFD simulation for detailed airflow visualization

---

## 14. Installation and Usage

### Requirements

* Python 3.x
* Streamlit
* NumPy
* Pandas

### Install Dependencies

```bash
pip install streamlit numpy pandas
```

### Run the Application

```bash
python -m streamlit run simulation.py
```

---

## 15. Intended Applications

This simulation can be used for:

* Physics-based hypothesis testing
* Preliminary design evaluation
* Educational demonstration of airflow and continuity equation concepts
* Supporting prototype planning before field testing
* Comparing simulated predictions with experimental measurements

---

## 16. Project Statement

This project presents a simplified physics-based model for evaluating a plastic-bottle Venturi board as a passive ventilation prototype for tropical food stall environments. The model estimates local airflow enhancement, total airflow change, blockage ratio, and perceived cooling effect. The results are intended to guide prototype design and experimental validation, rather than provide exact real-world predictions.

---

## 17. Author

Developed as part of an undergraduate physics project exploring the application of fundamental physical principles to low-cost workplace ventilation solutions.

```