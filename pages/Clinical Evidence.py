import streamlit as st
import requests

def search_pubmed(query, max_results=5):
    NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    search_url = f"{NCBI_BASE}/esearch.fcgi"

    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
        "sort": "relevance"
    }

    search_response = requests.get(search_url, params=search_params)

    search_response.raise_for_status()

    ids = search_response.json()["esearchresult"]["idlist"]

    if not ids:
        return[]
    
    summary_url = f"{NCBI_BASE}/esummary.fcgi"

    summary_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "json"
    }

    summary_response = requests.get(summary_url, params=summary_params)

    summary_response.raise_for_status()

    data = summary_response.json()["result"]

    papers = []

    for pubmed_id in ids:
        item = data.get(pubmed_id, {})

        papers.append({
            "PubMed ID": pubmed_id,
            "Title": item.get("title", "N/A"),
            "Journal": item.get("fulljournalname", "N/A"),
            "Publication Date": item.get("pubdate", "N/A"),
            "URL": f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
        })

    return papers

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