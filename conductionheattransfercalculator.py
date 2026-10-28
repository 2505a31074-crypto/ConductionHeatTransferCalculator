
import streamlit as st
import math

# Page configuration
st.set_page_config(
    page_title="Conduction Heat Transfer Calculator",
    page_icon="🌡️",
    layout="centered"
)

st.title("🌡️ Conduction Heat Transfer Calculator")
st.write(
    "Calculate the steady-state heat transfer rate through "
    "plane, cylindrical, and spherical walls."
)

st.divider()

# Select wall geometry
geometry = st.sidebar.selectbox(
    "Select Wall Geometry",
    ["Plane Wall", "Cylindrical Wall", "Spherical Wall"]
)

st.sidebar.info(
    "Choose a geometry and enter the required thermal properties."
)

# Common inputs
st.subheader(f"{geometry} Conduction")

with st.form("heat_transfer_form"):

    k = st.number_input(
        "Thermal conductivity, k (W/m·K)",
        min_value=0.000001,
        value=1.0,
        step=0.1,
        format="%.6f"
    )

    T1 = st.number_input(
        "Inner surface temperature, T1 (°C or K)",
        value=100.0,
        step=1.0
    )

    T2 = st.number_input(
        "Outer surface temperature, T2 (°C or K)",
        value=25.0,
        step=1.0
    )

    if geometry == "Plane Wall":
        A = st.number_input(
            "Surface area, A (m²)",
            min_value=0.000001,
            value=1.0,
            step=0.1
        )

        L = st.number_input(
            "Wall thickness, L (m)",
            min_value=0.000001,
            value=0.1,
            step=0.01
        )

    elif geometry == "Cylindrical Wall":
        L = st.number_input(
            "Cylinder length, L (m)",
            min_value=0.000001,
            value=1.0,
            step=0.1
        )

        r1 = st.number_input(
            "Inner radius, r1 (m)",
            min_value=0.000001,
            value=0.05,
            step=0.01
        )

        r2 = st.number_input(
            "Outer radius, r2 (m)",
            min_value=0.000002,
            value=0.10,
            step=0.01
        )

    else:  # Spherical Wall
        r1 = st.number_input(
            "Inner radius, r1 (m)",
            min_value=0.000001,
            value=0.05,
            step=0.01
        )

        r2 = st.number_input(
            "Outer radius, r2 (m)",
            min_value=0.000002,
            value=0.10,
            step=0.01
        )

    submitted = st.form_submit_button(
        "Calculate Heat Transfer Rate",
        use_container_width=True
    )

# Perform calculation
if submitted:

    if T1 == T2:
        st.info("The temperature difference is zero, so Q = 0 W.")
        st.metric("Heat Transfer Rate (Q)", "0.00 W")

    elif geometry == "Plane Wall":

        Q = k * A * (T1 - T2) / L

        st.success("Calculation completed successfully!")
        st.metric("Heat Transfer Rate (Q)", f"{Q:.2f} W")
        st.caption(
            "Formula: Q = k × A × (T1 − T2) / L"
        )

    elif geometry == "Cylindrical Wall":

        if r2 <= r1:
            st.error(
                "Outer radius (r2) must be greater than inner radius (r1)."
            )
        else:
            Q = (
                2 * math.pi * k * L * (T1 - T2)
                / math.log(r2 / r1)
            )

            st.success("Calculation completed successfully!")
            st.metric("Heat Transfer Rate (Q)", f"{Q:.2f} W")
            st.caption(
                "Formula: Q = 2πkL(T1 − T2) / ln(r2/r1)"
            )

    else:  # Spherical Wall

        if r2 <= r1:
            st.error(
                "Outer radius (r2) must be greater than inner radius (r1)."
            )
        else:
            Q = (
                4 * math.pi * k * r1 * r2 * (T1 - T2)
                / (r2 - r1)
            )

            st.success("Calculation completed successfully!")
            st.metric("Heat Transfer Rate (Q)", f"{Q:.2f} W")
            st.caption(
                "Formula: Q = 4πkr1r2(T1 − T2) / (r2 − r1)"
            )

st.divider()

st.markdown(
    """
    **Assumptions**
    - Steady-state, one-dimensional heat conduction.
    - Constant thermal conductivity.
    - No internal heat generation.
    - Temperatures use the same scale (°C or K).
    - A positive Q indicates heat transfer from the inner
      surface toward the outer surface when T1 > T2.
    """
)
