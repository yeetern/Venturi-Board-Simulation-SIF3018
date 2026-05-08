# Venturi Board Ventilation Simulation

A simplified physics-based Streamlit simulation for evaluating a **plastic-bottle Venturi board** as a passive local airflow amplifier for tropical food stall environments.

The model estimates whether a low-cost prototype can increase the **local wind speed felt by a person** and reduce **apparent temperature** under hot and humid conditions.

This project is designed for a *Physics for Work* context, where fundamental physics principles are applied to a real community/workplace problem.

---

## 1. Project Overview

Semi-open food stalls in tropical environments often experience thermal discomfort due to:

- high ambient temperature,
- high relative humidity,
- weak natural wind,
- cooking heat,
- limited access to active cooling systems.

The proposed prototype is a board fitted with recycled plastic bottles. Each bottle acts as a simplified converging nozzle: air enters through the larger bottle mouth and exits through the smaller bottle neck.

The simulation treats this setup as a **passive local airflow amplifier**.

The simplified model pipeline is:

```text
Environment + Geometry
→ Effective Incoming Wind
→ Capped Velocity Amplification
→ Loss-Corrected Outlet Wind
→ Felt Wind Speed
→ Apparent Temperature Before/After
```

This model is intended as a **hypothesis-generation and design-evaluation tool** before physical prototype testing. It is not a substitute for experimental measurements or full Computational Fluid Dynamics (CFD).

---

## 2. Main Research Question

The main question addressed by this simulation is:

> Can a plastic-bottle Venturi board increase the local wind speed felt by workers or customers enough to produce a measurable improvement in apparent thermal comfort?

The project does **not** claim that the prototype significantly lowers actual air temperature.

Instead, the goal is to evaluate whether the board can improve **localized perceived comfort** through directed airflow.

---

## 3. What the Dashboard Estimates

The Streamlit dashboard estimates:

* effective incoming wind speed,
* capped speed amplification ratio,
* ideal outlet wind speed,
* real outlet wind speed after losses,
* felt wind speed at the user position,
* water vapour pressure,
* apparent temperature before installation,
* apparent temperature after installation,
* apparent cooling improvement,
* geometry and packing parameters,
* sensitivity to wind speed,
* sensitivity to relative humidity.

The model intentionally focuses on **local wind-speed transformation**, not total airflow rate through the board.

---

## 4. Environmental Context

The model is designed for tropical semi-open food stall conditions, such as those commonly found in Kampung Baru, Kuala Lumpur.

Typical operating conditions may include:

| Parameter                           | Typical Range |
| ----------------------------------- | ------------: |
| Ambient temperature                 |      30–35 °C |
| Relative humidity                   |        70–90% |
| Outdoor wind speed                  |  ~0.3–1.7 m/s |
| Wind angle relative to board normal |         0–60° |

For reference:

$$
1~\text{km/h} = 0.278~\text{m/s}
$$

So a local wind speed of (1–6km/h) corresponds to approximately:

$$
0.28\text{–}1.67~\text{m/s}
$$

### Key Implication

Under weak natural wind, a passive Venturi board cannot create strong cooling by itself. Its realistic role is to slightly improve localized comfort by directing and accelerating available airflow.

---

## 5. Fluid Model

The model does not use total airflow (Q) as the main success metric.

Instead, it follows the wind-speed chain:

$$
v_{\text{wind}}
\rightarrow
v_{\text{eff}}
\rightarrow
v_{\text{out,ideal}}
\rightarrow
v_{\text{out}}
\rightarrow
v_{\text{feel}}
$$

---

### 5.1 Wind-Angle Correction

Only the wind component normal to the board is assumed to enter the bottle openings:

$$
v_{\text{eff}} = v_{\text{wind}}\cos\theta
$$

where:

| Symbol            | Meaning                             |
| ----------------- | ----------------------------------- |
| $v_{wind}$ | outdoor wind speed                  |
| $\theta$          | wind angle relative to board normal |
| $v_{eff}$  | effective incoming wind speed       |

If the wind hits the board directly:

$$
\theta = 0^\circ
$$

then:

$$
v_{\text{eff}} = v_{\text{wind}}
$$

If the wind is nearly parallel to the board:

$$
\theta \approx 90^\circ
$$

then:

$$
v_{\text{eff}} \approx 0
$$

This represents a key limitation of the design: the board only works well when incoming wind is reasonably aligned with the bottle openings.

---

### 5.2 Capped Velocity Amplification

For an ideal incompressible flow, the continuity equation suggests:

$
A_1v_1 = A_2v_2
$

For a bottle-nozzle approximation:

$
\frac{v_2}{v_1}=
\frac{A_{\text{big}}}{A_{\text{small}}}
$

where:

| Symbol             | Meaning                 |
| ------------------ | ----------------------- |
| $A_{\text{big}}$   | large bottle-mouth area |
| $A_{\text{small}}$ | bottle-neck area        |

However, a real passive plastic-bottle system cannot fully achieve an ideal geometric area-ratio amplification because of:

* turbulence,
* friction,
* flow separation,
* leakage,
* imperfect bottle cutting,
* nonuniform incoming wind,
* poor alignment.

Therefore, the simulation uses a capped speed-amplification ratio:

$$
r =
\min
\left(
\frac{A_{\text{big}}}{A_{\text{small}}},
r_{\max}
\right)
$$

where:

| Symbol     | Meaning                             |
| ---------- | ----------------------------------- |
| $r$        | used speed amplification ratio      |
| $r_{\max}$ | maximum allowed speed amplification |

This avoids overclaiming unrealistic outlet speeds.

---

### 5.3 Ideal Outlet Wind Speed

The ideal outlet wind speed is calculated as:

$$
v_{\text{out,ideal}} = r v_{\text{eff}}
$$

This represents the outlet speed before internal losses are applied.

---

### 5.4 Discharge Coefficient

Real airflow through a bottle nozzle is not lossless. The model introduces a discharge coefficient:

$$
v_{\text{out}} = C_d v_{\text{out,ideal}}
$$

or equivalently:

$$
v_{\text{out}} = C_d r v_{\text{eff}}
$$

where:

| Symbol           | Meaning                |
| ---------------- | ---------------------- |
| $C_d$            | discharge coefficient  |
| $v_{\text{out}}$ | real outlet wind speed |

A lower $C_d$ represents stronger loss due to:

* turbulence,
* rough bottle edges,
* friction,
* leakage,
* flow separation,
* imperfect construction.

Typical assumed values:

$$
0.5 \lesssim C_d \lesssim 0.8
$$

The actual value should be calibrated experimentally using an anemometer.

---

### 5.5 Effective Wind Factor

The outlet wind speed at the bottle neck is not necessarily the same wind speed felt by the worker or customer.

The jet may:

* spread out,
* weaken with distance,
* miss the person,
* mix with surrounding air,
* be blocked by objects.

Therefore, the model defines:

$$
v_{\text{feel}} = f_{\text{eff}}v_{\text{out}}
$$

where:

| Symbol            | Meaning                                   |
| ----------------- | ----------------------------------------- |
| $f_{\text{eff}}$  | effective wind factor                     |
| $v_{\text{feel}}$ | wind speed effectively felt by the person |

Typical assumed values:

$$
0 \leq f_{\text{eff}} \leq 1.0
$$

A value of $f_{\text{eff}} = 1.0$ means the full outlet wind reaches the person, which is usually optimistic.

A more realistic value may be:

$$
0.3 \text{–} 0.7
$$

depending on placement and distance.

---

## 6. Geometry Model

The board area is:

$$
A_{\text{board}} = W \times H
$$

The bottle-mouth area is:

$$
A_{\text{big}} = \pi R_{\text{big}}^2
$$

The bottle-neck area is:

$$
A_{\text{small}} = \pi R_{\text{small}}^2
$$

where:

| Symbol             | Meaning                      |
| ------------------ | ---------------------------- |
| $W$               | board width                  |
| $H$                | board height                 |
| $R_{\text{big}}$   | radius of large bottle mouth |
| $R_{\text{small}}$ | radius of bottle neck        |

The total projected bottle-mouth area is:

$$
A_{\text{big,total}} = N A_{\text{big}}
$$

The total throat area is:

$$
A_{\text{small,total}} = N A_{\text{small}}
$$

where $N$ is the number of bottles.

---

### 6.1 Inlet Coverage

The inlet coverage ratio is:

$$
\text{Inlet Coverage}=
\frac{N A_{\text{big}}}{A_{\text{board}}}
$$

This estimates how much of the board face is occupied by the large bottle-mouth footprint.

It is a **geometry/packing metric**, not the main airflow-success metric.

---

### 6.2 Inlet Blockage

The inlet blockage ratio is:

$$
\text{Inlet Blockage}=
1 -
\text{Inlet Coverage}
$$

This describes the fraction of the board face that is not occupied by bottle-mouth inlet area.

---

### 6.3 Throat Open-Area Fraction

The throat open-area fraction is:

$$
\text{Throat Open Fraction}=
\frac{N A_{\text{small}}}{A_{\text{board}}}
$$

This tells how much of the board area corresponds to the small bottle-neck openings.

---

### 6.4 Throat Restriction

The throat restriction ratio is:

$$
\text{Throat Restriction}=
1 -
\frac{A_{\text{small}}}{A_{\text{big}}}
$$

This measures the geometric contraction from the large bottle mouth to the small bottle neck.

A high throat restriction can produce faster local outlet wind, but it also means the system is highly dependent on losses and alignment.

---

## 7. Apparent Temperature Model

The simulation uses the Steadman apparent-temperature formulation to estimate perceived thermal comfort before and after installation.

The apparent temperature is calculated as:

$$
AT = T_a + 0.33e - 0.70v - 4.00
$$

where:

| Symbol | Meaning                            |
| ------ | ---------------------------------- |
| $AT$   | apparent temperature in °C         |
| $T_a$  | ambient dry-bulb temperature in °C |
| $e$    | water vapour pressure in hPa       |
| $v$    | effective local wind speed in m/s  |

The water vapour pressure is estimated from relative humidity:

$$
e =
\frac{RH}{100}
\times
6.105
\times
\exp
\left(
\frac{17.27T_a}{237.7 + T_a}
\right)
$$

where:

| Symbol | Meaning                       |
| ------ | ----------------------------- |
| $RH$   | relative humidity in percent  |
| $T_a$  | ambient air temperature in °C |

This model estimates perceived heat stress, not actual air-temperature reduction.

---

## 8. Before-and-After Comparison

The key comparison is:

$$
\Delta AT =
AT_{\text{before}}-
AT_{\text{after}}
$$

Before installation:

$$
AT_{\text{before}}=
T_a + 0.33e - 0.70v_{\text{before}} - 4.00
$$

with:

$$
v_{\text{before}} = v_{\text{eff}}
$$

After installation:

$$
AT_{\text{after}}=
T_a + 0.33e - 0.70v_{\text{after}} - 4.00
$$

with:

$$
v_{\text{after}} = v_{\text{feel}}
$$

If:

$$
\Delta AT > 0
$$

then the simulation predicts an improvement in apparent thermal comfort.

---

## 9. Important Interpretation

The Venturi board does **not** directly lower the actual air temperature.

The expected physical behaviour is:

$$
T_{\text{actual, after}}
\approx
T_{\text{actual, before}}
$$

but:

$$
v_{\text{feel, after}}>
v_{\text{before}}
$$

may reduce apparent temperature.

Therefore, the model output should be interpreted as:

> predicted improvement in perceived thermal comfort,

not:

> actual thermodynamic cooling of the surrounding air.

Under high humidity, apparent temperature may be higher than actual air temperature. This is expected because humid air reduces sweat evaporation and increases perceived heat stress.

---

## 10. Example Prototype Configuration

The current prototype concept uses:

| Quantity                    |               Value |
| --------------------------- | ------------------: |
| Board size                  |      120 cm × 30 cm |
| Layout                      | 3 columns × 12 rows |
| Number of bottles           |                  36 |
| Large bottle-mouth diameter |              ~95 mm |
| Bottle-neck hole diameter   |           ~30–32 mm |
| Nominal bottle-neck radius  |             ~1.5 cm |

### Design Advantage

The 3 × 12 layout increases the number of distributed local jets and improves the chance that airflow reaches the worker or customer.

### Design Risk

The bottle necks are much smaller than the bottle mouths. This increases local speed but makes the result sensitive to:

* discharge losses,
* poor alignment,
* weak natural wind,
* distance from the user,
* whether the jet reaches the person.

---

## 11. Assumptions

### 11.1 Fluid Assumptions

* The incoming wind is steady.
* Only the wind component perpendicular to the board is used.
* The bottle array is modeled as a capped local velocity amplifier.
* The full geometric area ratio is not assumed to be fully achievable.
* The used speed amplification ratio is limited by $r_{\max}$.
* Energy losses inside the bottle/nozzle are represented by $C_d$.
* Delivery losses from the outlet jet to the person are represented by $f_{\text{eff}}$.
* The model focuses on local wind-speed transformation rather than total airflow rate.

### 11.2 Geometry Assumptions

* Bottles are uniformly distributed across the board.
* Bottle openings are approximated as circular.
* Bottle-mouth footprint and bottle-neck throat area are treated separately.
* Bottle overlap and structural interference are not fully modeled.
* Inlet coverage is treated as a packing/geometry indicator, not a guarantee of captured airflow.

### 11.3 Thermal Comfort Assumptions

* Apparent temperature is estimated using the Steadman apparent-temperature model.
* The model estimates perceived thermal comfort, not true air-temperature reduction.
* Apparent temperature can be higher than actual air temperature under humid conditions.
* The key result is $AT_{\text{before}} - AT_{\text{after}}$.
* Radiative heat from cooking equipment is not included.
* Direct solar radiation is not included.
* Clothing, metabolic rate, sweating rate, and posture are not included.
* Distance-dependent jet decay is not explicitly modeled.

---

## 12. Limitations

This model has several important limitations:

* It is not a CFD simulation.
* It does not solve the Navier–Stokes equations.
* It does not model turbulence, recirculation, vortex shedding, or flow separation.
* It does not simulate full spatial airflow distribution inside the stall.
* It does not include cooking heat, solar radiation, or radiant heat from hot surfaces.
* It does not calculate total airflow rate as the main performance metric.
* The discharge coefficient $C_d$ requires experimental calibration.
* The maximum amplification ratio $r_{\max}$ is an assumption and should be calibrated.
* The effective wind factor $f_{\text{eff}}$ requires experimental or user-feedback calibration.
* Steadman apparent temperature is a simplified thermal-stress estimate and does not replace detailed indices such as PMV, SET, or UTCI.

### Critical Limitation

The model should be treated as a **first-order hypothesis model**, not an exact prediction of real-world performance.

---

## 13. Expected Findings

Based on the simplified model, the following behaviour is expected:

1. The Venturi-board configuration can increase local outlet wind speed.
2. The felt wind speed depends strongly on $f_{\text{eff}}$.
3. High humidity increases apparent temperature.
4. Wind direction strongly affects performance.
5. Weak natural wind limits passive performance.
6. Apparent-temperature improvement may be small under low-wind conditions.
7. The system is more likely to improve localized comfort than reduce actual ambient temperature.

### Main Interpretation

The plastic-bottle Venturi board should be evaluated primarily as a:

> passive local airflow amplifier,

not as:

> a system that lowers the actual surrounding air temperature.

---

## 14. Experimental Validation Plan

To validate the model, real measurements should be collected before and after prototype installation.

Suggested measurements:

* ambient wind speed before installation,
* outlet wind speed at the bottle necks,
* wind speed at the worker/customer position before installation,
* wind speed at the worker/customer position after installation,
* ambient temperature,
* relative humidity,
* vendor comfort feedback.

A simple feedback scale can be used:

| Rating | Comfort Description |
| -----: | ------------------- |
|      1 | Very uncomfortable  |
|      2 | Uncomfortable       |
|      3 | Neutral             |
|      4 | Slightly improved   |
|      5 | Clearly improved    |

Experimental data can be used to calibrate:

* $C_d$,
* $r_{\max}$,
* $f_{\text{eff}}$,
* practical comfort response.

---

## 15. Future Improvements

Possible improvements include:

* calibrating the model using experimental data,
* adding a two-board or multi-board coverage model,
* comparing different bottle layouts,
* comparing different bottle-neck diameters,
* testing different board angles relative to incoming wind,
* adding distance-dependent airflow decay,
* adding fan-assisted airflow conditions,
* adding radiant heat effects from cooking equipment,
* performing CFD simulation for detailed airflow visualization,
* comparing Steadman apparent temperature with PMV, SET, or UTCI.

---

## 16. Installation and Usage

### Requirements

* Python 3.x
* Streamlit
* NumPy
* Pandas

### Install Dependencies

```bash
pip install streamlit numpy pandas

### Run the Application

streamlit run simulation.py

or:

python -m streamlit run simulation.py

```

---

## 17. Suggested File Structure

```text
venturi-board-simulation/
│
├── simulation.py
├── README.md
```

Example `requirements.txt`:

```text
streamlit
numpy
pandas
```

---

## 18. Intended Applications

This simulation can be used for:

* physics-based hypothesis testing,
* preliminary prototype evaluation,
* educational demonstration of continuity and airflow concepts,
* supporting prototype planning before field testing,
* explaining the limits of passive ventilation,
* comparing simulated predictions with anemometer measurements.

---

## 19. Citation

The apparent-temperature calculation follows the Steadman apparent-temperature formulation.

```text
Steadman, R. G. (1994). Norms of apparent temperature in Australia.
Australian Meteorological Magazine, 43, 1–16.
https://doi.org/10.1071/ES94001
```

The simplified form used in this project is:

$$
AT = T_a + 0.33e - 0.70v - 4.00
$$

where (e) is water vapour pressure and (v) is effective local wind speed.

---

## 20. Project Statement

This project presents a simplified physics-based model for evaluating a plastic-bottle Venturi board as a passive local airflow amplifier for tropical food stall environments. The model estimates how incoming wind is transformed into ideal outlet wind, loss-corrected outlet wind, and finally felt wind speed at the user position. The felt wind speed is then used in the Steadman apparent-temperature model to compare apparent temperature before and after installation. The main result is predicted improvement in perceived thermal comfort, not actual air-temperature reduction. The model is intended to guide prototype design and experimental validation.

---

## 21. Author

Developed as part of an undergraduate physics project exploring low-cost workplace ventilation solutions using fundamental physical principles.