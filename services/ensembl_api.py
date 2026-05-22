import requests

def search_gene(symbol):
    url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{symbol}"
    headers = {"Content-Type": "application/json"}

    response = requests.get(url,headers=headers)

    if response.status_code == 404:
        return None
    
    response.raise_for_status()
    return response.json()