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