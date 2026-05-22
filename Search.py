import requests
import streamlit as st
import pandas as pd
from services.clinvar_api import search_clinvar_by_gene
from services.ensembl_api import search_gene

# Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "home"

if "variants_df" not in st.session_state:
    st.session_state.variants_df = None

if "gene_symbol" not in st.session_state:
    st.session_state.gene_symbol = ""

if "selected_variant" not in st.session_state:
    st.session_state.selected_variant = None


# Home Page

if st.session_state.page == "home":

    st.title("AI-Powered Genomics Dashboard")

    gene_symbol = st.text_input(
        "Enter a gene symbol",
        value = st.session_state.gene_symbol,
        placeholder="BRCA1"
    )

    if st.button("Search"):

        if not gene_symbol.strip():
            st.warning("Please enter a gene symbol.")
        else:
            st.session_state.gene_symbol = gene_symbol.upper()
            st.session_state.variants_df = search_clinvar_by_gene(gene_symbol.upper())
            st.session_state.page = "variants"
            st.rerun()
    


# Variant Page

elif st.session_state.page == "variants":

    st.title(
        f"Variants for {st.session_state.gene_symbol}"
    )

    if st.button("Back to Search"):
        st.session_state.page = "home"
        st.session_state.gene_symbol = ""
        st.session_state.variants_df = None
        st.session_state.selected_variant = None

        if "variant_dropdown" in st.session_state:
            del st.session_state["variant_dropdown"]

        st.rerun()

    variants_df = st.session_state.variants_df

    st.subheader("Filter Variants")

    significance_options = variants_df["Clinical Significance"].dropna().unique()

    selected_significance = st.multiselect(
        "Clinical significance",
        significance_options,
        default=significance_options
    )

    filtered_df = variants_df[
        variants_df["Clinical Significance"].isin(selected_significance)
    ]

    st.dataframe(filtered_df, use_container_width=True)

    selected_title = st.selectbox(
        "Choose a variant",
        filtered_df["Title"],
        key="variant_dropdown"
    )

    selected_variant = variants_df[
        variants_df["Title"] == selected_title
    ].iloc[0]

    st.session_state.selected_variant = selected_variant

    st.subheader("Variant Summary")

    st.write("**Title:**", selected_variant["Title"])
    st.write(
        "**Clinical Significance:**",
        selected_variant["Clinical Significance"]
    )


    selected_variant = variants_df[
        variants_df["Title"] == selected_title
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.write("**ClinVar ID:**", selected_variant["ClinVar ID"])
        st.write("**Clinical Significance:**", selected_variant["Clinical Significance"])
        st.write("**Review Status:**", selected_variant["Review Status"])

    with col2:
        st.write("**Variation Type:**", selected_variant["Variation Type"])
        st.write("**Last Updated:**", selected_variant["Last Updated"])

    st.write("**Variant Title:**")
    st.write(selected_variant["Title"])

    st.subheader("Plain-English Explanation")

    explanation = f"""
    This variant is currently classified as **{selected_variant['Clinical Significance']}**
    in ClinVar.

    Its review status is **{selected_variant['Review Status']}**, which gives a rough sense
    of how much evidence supports this classification.

    This is not medical advice. It is a summary of public ClinVar data.
    """

    st.info(explanation)

    report_text = f"""
        AI-Powered Genomics Dashboard Report

        Gene: {st.session_state.gene_symbol}

        Variant Title:
        {selected_variant["Title"]}

        ClinVar ID:
        {selected_variant["ClinVar ID"]}

        Clinical Significance:
        {selected_variant["Clinical Significance"]}

        Review Status:
        {selected_variant["Review Status"]}

        Variation Type:
        {selected_variant["Variation Type"]}

        Last Updated:
        {selected_variant["Last Updated"]}

        Plain-English Explanation:
        This variant is currently classified as {selected_variant["Clinical Significance"]} in ClinVar.
        Its review status is {selected_variant["Review Status"]}.

        Disclaimer:
        This report is for educational purposes only and is not medical advice.
        """
    
    st.download_button(
        label="Download Variant Report",
        data = report_text,
        file_name = f"{st.session_state.gene_symbol}_variant_report.txt",
        mime = "text/plain"
    )

    st.subheader("Clinical Significance Breakdown")

    chart_data = filtered_df["Clinical Significance"].value_counts()

    st.bar_chart(chart_data)


    selected_variant = filtered_df[
        filtered_df["Title"] == selected_title
    ].iloc[0]


    if st.button("View Clinical Evidence"):
        st.switch_page("pages/Clinical Evidence.py")

    if st.button("View Visualizations"):
        st.switch_page("pages/Visualizations.py")