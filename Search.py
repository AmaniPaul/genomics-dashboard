import requests
import streamlit as st
import pandas as pd

# Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "home"

if "variants_df" not in st.session_state:
    st.session_state.variants_df = None

if "gene_symbol" not in st.session_state:
    st.session_state.gene_symbol = ""

if "selected_variant" not in st.session_state:
    st.session_state.selected_variant = None


def search_clinvar_by_gene (gene_symbol, max_results=20):
    NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    search_url = f"{NCBI_BASE}/esearch.fcgi"

    search_params = {
        "db": "clinvar",
        "term": f"{gene_symbol}[gene]",
        "retmode": "json",
        "retmax": max_results
    }

    search_response = requests.get(search_url, params=search_params)

    search_response.raise_for_status()

    ids = search_response.json()["esearchresult"]["idlist"]

    if not ids:
        return pd.DataFrame()

    summary_url = f"{NCBI_BASE}/esummary.fcgi"

    summary_params = {
        "db": "clinvar",
        "id": ",".join(ids),
        "retmode": "json"
    }
    
    summary_response = requests.get(summary_url, params=summary_params)
    summary_response.raise_for_status()

    data = summary_response.json()["result"]

    rows = []

    for clinvar_id in ids:
        item = data.get(clinvar_id, {})

        rows.append({
            "ClinVar ID": clinvar_id,
            "Title": item.get("title", "N/A"),
            "Clinical Significance": item.get("clinical_significance", {}).get("description", "N/A"),
            "Review Status": item.get("clinical_significance", {}).get("review_status", "N/A"),
            "Variation Type": item.get("variation_type", "N/A"),
            "Last Updated": item.get("last_updated", "N/A"),
        })

    return pd.DataFrame(rows)


def search_gene(symbol):
    url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{symbol}"
    headers = {"Content-Type": "application/json"}

    response = requests.get(url,headers=headers)

    if response.status_code == 404:
        return None
    
    response.raise_for_status()
    return response.json()



# Home Page

if st.session_state.page == "home":

    st.title("AI-Powered Genomics Dashboard")

    gene_symbol = st.text_input(
        "Enter a gene symbol",
        placeholder="BRCA1"
    )

    if st.button("Search"):

        st.session_state.gene_symbol = gene_symbol.upper()

        st.session_state.variants_df = search_clinvar_by_gene(
            gene_symbol.upper()
        )

        st.session_state.page = "variants"

        st.rerun()

# Variant Page

elif st.session_state.page == "variants":

    st.title(
        f"Variants for {st.session_state.gene_symbol}"
    )

    variants_df = st.session_state.variants_df

    st.dataframe(variants_df)

    selected_title = st.selectbox(
        "Choose a variant",
        variants_df["Title"],
        key="variant_dropdown"
    )

    selected_variant = variants_df[
        variants_df["Title"] == selected_title
    ].iloc[0]

    st.subheader("Variant Summary")

    st.write("**Title:**", selected_variant["Title"])
    st.write(
        "**Clinical Significance:**",
        selected_variant["Clinical Significance"]
    )

    if st.button("Back to Search"):

        st.session_state.page = "home"

        st.rerun()

    st.subheader("Variant Summary")

    

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

    st.subheader("Clinical Significance Breakdown")

    chart_data = variants_df["Clinical Significance"].value_counts()

    st.bar_chart(chart_data)