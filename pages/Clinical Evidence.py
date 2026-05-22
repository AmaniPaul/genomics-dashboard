import streamlit as st
import requests
from services.pubmed_api import search_pubmed



def generate_variant_explanation(variant, style):
    if style == "Patient-friendly":
        return f"""
        This variant is listed in ClinVar as **{variant['Clinical Significance']}**.

        This means researchers or clinical labs have submitted evidence about whether
        this DNA change may be related to disease.

        The review status is **{variant['Review Status']}**, which gives a rough idea
        of how strongly the classification is supported.

        This summary is educational only and is not medical advice.
        """

    if style == "Scientist":
        return f"""
        ClinVar reports this variant as **{variant['Clinical Significance']}**.

        The submitted review status is **{variant['Review Status']}**.
        The variant type is **{variant['Variation Type']}**.

        Further interpretation would require literature review, population frequency,
        functional evidence, and expert clinical assessment.
        """

    return f"""
    This dashboard demonstrates how software can combine public biomedical databases,
    clinical variant interpretation, and AI-style explanations into a usable genomics tool.
    """

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

st.subheader("Related PubMed Literature")

query = f"{variant['Title']} {variant['Clinical Significance']}"

papers = search_pubmed(query)

if not papers:
    st.info("No related PubMed articles found.")
else:
    for paper in papers:
        st.markdown(f"### {paper['Title']}")
        st.write("**Journal:**", paper["Journal"])
        st.write("**Publication Date:**", paper["Publication Date"])
        st.markdown(f"[View on PubMed]({paper['URL']})")
        st.divider()

st.warning(
    "This dashboard is for educational purposes only and not medical advice."
)

st.divider()

st.subheader("AI Explanation")

explanation_level = st.selectbox(
    "Choose explanation style",
    ["Patient-friendly", "Scientist", "Recruiter demo"]
)

if st.button("Generate Explanation"):
    explanation = generate_variant_explanation(variant, explanation_level)

    st.info(explanation)