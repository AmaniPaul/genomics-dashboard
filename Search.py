import requests
import streamlit as st

st.set_page_config(page_title="Genomics Dashboard", layout="wide")

st.title("AI-Powered Genomics Dashboard")
st.write("Search for a human gene to view basic genomic information.")

gene_symbol = st.text_input("Enter a gene symbol", placeholder="Example: BRCA1")

def search_gene(symbol):
    url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{symbol}"
    headers = {"Content-Type": "application/json"}

    response = requests.get(url,headers=headers)

    if response.status_code == 404:
        return None
    
    response.raise_for_status()
    return response.json()

if st.button("Search"):
    if not gene_symbol:
        st.warning("Please enter a gene symbol.")
    else:
        with st.spinner("Searching Ensembl..."):
            gene = search_gene(gene_symbol.upper())

        if gene is None:
            st.error("Gene not found. Try another symbol.")
        else:
            st.subheader(gene.get("display_name", gene_symbol.upper()))

            col1, col2, col3 = st.columns(3)

            col1.metric("Chromosome", gene.get("seq_region_name", "N/A"))
            col2.metric("Start", gene.get("start", "N/A"))
            col3.metric("End", gene.get("end", "N/A"))

            st.write("**Ensembl ID:**", gene.get("id", "N/A"))
            st.write("**Biotype:**", gene.get("biotype", "N/A"))
            st.write("**Strand:**", gene.get("strand", "N/A"))

            with st.expander("Raw API response"):
                st.json(gene)

if st.button("View Variants"):
    gene = search_gene(gene_symbol.upper())

    st.subheader("Variant Information")

    st.write("**Variant:**", )
    st.write("**Gene:**", gene.get(gene_symbol.upper()))
    st.write("**Chromosome:**", gene.get("seq_region_name", "N/A"))
    st.write("**Position:**", )