# Slide 1 — Title and Current Status

### Slide title

**Progress Presentation: Airflow Optimization for Thermal Comfort in Semi-Open Food Stalls**

### Content

* Project: Venturi-board airflow system
* Current stage: **pre-fabrication / simulation completion stage**
* Main update:

  * albedo paint removed due to budget
  * materials purchased
  * bengkel fabrication arranged
  * simulation almost completed
  * measurement and vendor feedback pending

### Suggested status bar

| Stage                 | Status           |
| --------------------- | ---------------- |
| Proposal              | Completed        |
| Scope revision        | Completed        |
| Material purchase     | Completed        |
| Simulation            | Almost completed |
| Prototype fabrication | Pending          |
| Installation          | Pending          |
| Measurement           | Pending          |
| Vendor feedback       | Pending          |

### What to say

“This progress presentation focuses on what has changed since the proposal and what has been completed so far. Our project has moved from concept stage to material preparation and simulation validation stage.”

---

# Slide 2 — Original Plan vs Revised Plan

### Purpose

Explain why the albedo paint was removed.

| Item             | Proposal Stage           | Current Progress Stage                         |
| ---------------- | ------------------------ | ---------------------------------------------- |
| Albedo paint     | Included                 | Removed                                        |
| Venturi board    | Included                 | Main focus                                     |
| Main mechanism   | Radiation + airflow      | Airflow + convective/evaporative cooling       |
| Main measurement | Temperature + wind speed | Wind speed before/after + thermal comfort      |
| Budget           | RM250                    | Focused on prototype materials and measurement |

### Key sentence

“Due to budget limitation, we removed the albedo paint and focused on a low-cost Venturi board that can be fabricated, installed, and tested within our available resources.”

---

# Slide 3 — Completed Progress So Far

### Purpose

Show real progress.

### Content

| Progress Item        | Evidence                               | Status                   |
| -------------------- | -------------------------------------- | ------------------------ |
| Materials purchased  | Photo / receipt / list                 | Completed                |
| Anemometer purchased | Photo                                  | Completed                |
| Bengkel booking      | Booking confirmation / verbal approval | Completed or in progress |
| Simulation model     | Screenshot / graph                     | Almost completed         |
| Prototype design     | Sketch / CAD / schematic               | Completed                |
| Installation site    | Vendor / stall location                | Confirmed or pending     |

### What to show visually

Use actual photos:

* bottles / board / frame material,
* anemometer,
* department bengkel,
* simulation screenshot,
* prototype sketch.

### What to say

“At this stage, our major progress is that the project is no longer only conceptual. We have purchased the required materials, arranged fabrication support from the department workshop, and developed the simulation model.”

---

# Slide 4 — Current Prototype Design

### Purpose

Show what you are going to build.

### Include

* diagram / schematic,
* airflow direction,
* bottle funnel arrangement,
* frame structure,
* where it will be installed.

### Physics labels

* inlet area (A_1)
* outlet area (A_2)
* incoming velocity (v_1)
* outlet velocity (v_2)
* user/stall region

### Suggested wording

“The prototype uses recycled plastic bottles as converging ducts. Air enters through the wider opening and exits through the smaller neck, increasing local airflow velocity.”

---

# Slide 5 — Physics Laws Used

### Purpose

Directly satisfy the rubric.

Use these four physics ideas.

### 1. Continuity equation

[
A_1v_1 = A_2v_2
]

Meaning: smaller outlet area gives higher outlet velocity under ideal flow.

---

### 2. Bernoulli principle

[
P + \frac{1}{2}\rho v^2 = \text{constant}
]

Meaning: increase in velocity is associated with pressure change.

---

### 3. Convective cooling

[
q_{\text{conv}} = hA(T_{\text{skin}} - T_{\text{air}})
]

Meaning: higher airflow increases (h), so heat leaves the body faster.

---

### 4. Humidity limitation

[
RH \uparrow \Rightarrow \text{evaporation} \downarrow \Rightarrow \text{cooling effectiveness} \downarrow
]

Meaning: in humid Malaysia, airflow may help comfort even if temperature does not drop much.

### Strong sentence

“Our revised project does not mainly cool the air itself. It aims to increase local airflow, which improves convective and evaporative heat loss from the human body.”

---

# Slide 6 — Simulation Progress

### Purpose

Show that your simulation is nearly done and useful.

### Content

* simulation objective,
* input variables,
* output variables,
* preliminary result / screenshot.

### Suggested table

| Simulation Component | Description                                          |
| -------------------- | ---------------------------------------------------- |
| Input                | inlet/outlet area, wind speed, temperature, humidity |
| Physics              | continuity equation, comfort model                   |
| Output               | predicted velocity increase, perceived cooling trend |
| Purpose              | guide prototype design and measurement expectation   |

### If you have a graph

Use one graph only, such as:

* humidity vs apparent comfort,
* inlet/outlet ratio vs velocity increase,
* before/after airflow prediction.

### What to say

“The simulation is used to estimate how geometry and humidity affect performance before we build the prototype. It helps us predict what measurement range we should expect during field testing.”

---

# Slide 7 — Measurement Plan

### Purpose

Show exactly how you will prove the prototype works.

### Before-after method

| Measurement  | Before Installation                 | After Installation               |
| ------------ | ----------------------------------- | -------------------------------- |
| Air velocity | Measure at same point without board | Measure at same point with board |
| Temperature  | Record ambient temperature          | Record ambient temperature       |
| Humidity     | Record RH if available              | Record RH if available           |
| User comfort | Ask vendor/customer                 | Ask vendor/customer              |

### Measurement setup

* Use anemometer bought by group
* Measure at:

  * front of board,
  * outlet of board,
  * working/customer zone
* Repeat readings:

  * 3–5 times per point
* Use average value
* Keep same time period if possible

### Suggested formula

[
% \text{ improvement} =
\frac{v_{\text{after}} - v_{\text{before}}}{v_{\text{before}}}
\times 100%
]

### What to say

“Our main quantitative evidence will be the percentage increase in local air velocity before and after installing the Venturi board.”

---

# Slide 8 — Community Feedback Plan / Preliminary Feedback

### Purpose

Handle the feedback rubric honestly.

Since final vendor feedback is not collected yet, split it into:

1. preliminary feedback, if any,
2. planned post-installation feedback.

### Preliminary feedback example

If vendor already commented:

| Feedback                                 | Meaning              | Planned Response                         |
| ---------------------------------------- | -------------------- | ---------------------------------------- |
| Prototype appearance may look messy      | Adoption issue       | Cover frame with cloth or cleaner casing |
| Installation should not disturb business | Practical constraint | Use removable mounting                   |
| Airflow should face customer/worker area | Direction issue      | Adjust orientation                       |

### Planned direct quotes

You cannot fake final quotes. But you can prepare the structure:

* Vendor quote after seeing prototype
* Worker quote after airflow test
* Customer or nearby user quote after installation

### Feedback form questions

| Question                                | Scale  |
| --------------------------------------- | ------ |
| Airflow is noticeable                   | 1–5    |
| The stall feels more comfortable        | 1–5    |
| Prototype appearance is acceptable      | 1–5    |
| Installation does not disturb operation | 1–5    |
| Would you keep this prototype?          | Yes/No |

### Negative comment

Your expected or preliminary negative comment:

> “The plastic bottle prototype may look messy and affect the image of the stall.”

### Revision

* cover with cloth,
* use cleaner frame,
* keep bottle openings unobstructed.

---

# Slide 9 — Current Challenges and Physics-Based Revisions

### Purpose

Show maturity and satisfy “what changed after feedback.”

| Challenge / Feedback         | Physics or Practical Meaning   | Revision                           |
| ---------------------------- | ------------------------------ | ---------------------------------- |
| Albedo paint too expensive   | Cannot reduce solar heat input | Focus on airflow comfort           |
| Natural wind may be weak     | Venturi needs inlet airflow    | Place near fan or wind-facing side |
| Humidity may reduce cooling  | Evaporation less effective     | Include humidity in simulation     |
| Prototype looks unattractive | Vendor may reject installation | Add cloth/casing                   |
| Measurements may fluctuate   | Outdoor airflow is unstable    | Repeat readings and average        |

### Strong sentence

“The feedback and constraints did not change the physical laws, but they changed our boundary conditions, design priorities, and success metrics.”

---

# Slide 10 — Remaining Work

### Purpose

Show what still needs to be completed.

### Clear remaining checklist

| Remaining Task               | Purpose                      | Status  |
| ---------------------------- | ---------------------------- | ------- |
| Build prototype at bengkel   | Convert design into hardware | Pending |
| Install at stall             | Field implementation         | Pending |
| Measure before/after airflow | Quantitative validation      | Pending |
| Measure temperature/humidity | Environmental context        | Pending |
| Collect vendor feedback      | Community validation         | Pending |
| Interpret data physically    | Final analysis               | Pending |

### What to say

“The remaining work is mainly experimental validation. Once the prototype is built and installed, we will compare airflow before and after, then connect the measurement results to the physics model.”

---

# Slide 11 — Updated Timeline and Contingency Plan

### Updated timeline

| Week              | Task                                            |
| ----------------- | ----------------------------------------------- |
| Current week      | Finalize simulation and bengkel booking         |
| Next week         | Build prototype                                 |
| Following week    | Install prototype and collect before/after data |
| After measurement | Analyze data and collect feedback               |
| Final stage       | Improve design and prepare final report         |

### Contingency plan

| Risk                         | Backup Plan                                                    |
| ---------------------------- | -------------------------------------------------------------- |
| Bengkel unavailable          | Use simpler hand tools / reschedule early                      |
| Natural wind too weak        | Test near fan or during windier period                         |
| Vendor rejects appearance    | Add cloth/casing                                               |
| Sensor readings unstable     | Repeat measurement and average                                 |
| Installation not allowed     | Use temporary non-invasive mounting                            |
| Simulation differs from data | Explain real-world losses: turbulence, leakage, wind direction |

---

# Slide 12 — Conclusion

### Purpose

End with a confident but honest status update.

### Suggested conclusion

“Our project has progressed from proposal to implementation preparation. The albedo paint component was removed due to budget constraints, so the project now focuses on a Venturi-board airflow system. We have purchased the materials, arranged access to the department workshop, and nearly completed the simulation model. The next stage is to fabricate and install the prototype, measure before-and-after airflow using the anemometer, and collect vendor feedback. The final interpretation will compare experimental results with the physics model and explain the effect of airflow and humidity on perceived thermal comfort.”