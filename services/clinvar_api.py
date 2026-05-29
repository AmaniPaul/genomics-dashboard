import requests
import pandas as pd
import streamlit as st

@st.cache_data
def search_clinvar_by_gene (gene_symbol, max_results=5):
    NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    search_url = f"{NCBI_BASE}/esearch.fcgi"

    search_params = {
        "db": "clinvar",
        "term": f"{gene_symbol}[gene]",
        "retmode": "json",
        "retmax": max_results
    }

    try:
        search_response = requests.get(search_url, params=search_params, timeout=10)
        search_response.raise_for_status()
    except requests.exceptions.RequestException:
        st.error("Could not connect to ClinVar API.")
        return None

    ids = search_response.json()["esearchresult"]["idlist"]

    if not ids:
        return pd.DataFrame()

    summary_url = f"{NCBI_BASE}/esummary.fcgi"

    summary_params = {
        "db": "clinvar",
        "id": ",".join(ids),
        "retmode": "json"
    }
    
    summary_response = requests.get(summary_url, params=summary_params, timeout=10)
    summary_response.raise_for_status()

    data = summary_response.json()["result"]

    rows = []

    for clinvar_id in ids:
        item = data.get(clinvar_id, {})

        germline_data = item.get("germline_classification", {})

        clinical_significance = "N/A"
        review_status = "N/A"


        if isinstance(germline_data, dict):
            clinical_significance = germline_data.get("description", "N/A")
            review_status = germline_data.get("review_status", "N/A")

        clinical_data = item.get("clinical_significance")

        if clinical_significance == "N/A":
            if isinstance(clinical_data, dict):
                clinical_significance = clinical_data.get("description", "N/A")
                review_status = clinical_data.get("review_status", review_status)
            elif isinstance(clinical_data, str):
                clinical_significance = clinical_data

        review_status = item.get("review_status", review_status)

        rows.append({
            "ClinVar ID": clinvar_id,

            "Title": item.get(
                "title",
                "N/A"
            ),

            "Clinical Significance": clinical_significance,

            "Review Status": review_status,

            "Variation Type": item.get(
                "obj_type",
                item.get("variation_type", "N/A")
            ),

            "Last Updated": item.get(
                "last_updated",
                "N/A"
            ),
        })

    return pd.DataFrame(rows)