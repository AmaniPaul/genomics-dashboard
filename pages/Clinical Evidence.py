import streamlit as st

st.title("Clinical Evidence")

if "selected_variant" not in st.session_state:
    st.error("No variant selected.")
    st.stop()

variant = st.session_state.selected_variant

st.subheader(variant["Title"])

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Clinical Significance",
        variant["Clinical Significance"]
    )

    st.metric(
        "Review Status",
        variant["Review Status"]
    )

with col2:
    st.metric(
        "Variation Type",
        variant["Variation Type"]
    )

    st.metric(
        "ClinVar ID",
        variant["ClinVar ID"]
    )

st.divider()

st.subheader("Evidence Interpretation")

interpretation = f"""
This variant is currently classified as
**{variant['Clinical Significance']}**.

The review status is:
**{variant['Review Status']}**.

This classification comes from ClinVar submissions
and represents publicly available clinical evidence.
"""

st.write(interpretation)

st.warning(
    "This dashboard is for educational purposes only and not medical advice."
)