import requests
import streamlit as st

def search_gene(symbol):
    url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{symbol}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        st.error("Could not connect to Ensembl API.")
        return None
    
    return response.json()