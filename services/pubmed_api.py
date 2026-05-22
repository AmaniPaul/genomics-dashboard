import requests
import streamlit as st

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

    try:
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
    except requests.exceptions.RequestException:
        st.error("Could not connect to PubMed API.")
        return None

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