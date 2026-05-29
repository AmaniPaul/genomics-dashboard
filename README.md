# AI-Powered Genomics Dashboard

## Overview

The AI-Powered Genomics Dashboard is a Streamlit-based bioinformatics application that allows users to search for genes, explore ClinVar variants, review clinical evidence, visualize variant data, and discover related biomedical literature through PubMed.

This project combines:
- bioinformatics
- API integration
- data visualization
- biomedical data interpretation
- AI-style explanations
- full-stack application structure

The goal of the project is to demonstrate how software engineering and biotechnology can work together to make genomic information more accessible and understandable.

---

# Features

## Gene Search
Search for human genes using public genomic databases.

Examples:
- BRCA1
- TP53
- CFTR

---

## ClinVar Variant Retrieval
Retrieve clinical variant information from ClinVar including:
- clinical significance
- review status
- variation type
- last updated date

---

## Variant Filtering
Filter variants by:
- pathogenicity
- significance classification
- review status

---

## Variant Summary
View detailed summaries for selected variants including:
- ClinVar ID
- clinical interpretation
- variation type
- evidence summary

---

## Clinical Evidence Page
Explore:
- evidence interpretation
- review confidence
- related genomic information

---

## PubMed Literature Integration
Retrieve related biomedical research articles from PubMed.

Displays:
- article title
- journal
- publication date
- PubMed links

---

## AI-Style Explanations
Generate:
- patient-friendly explanations
- scientist explanations
- recruiter/demo explanations

---

## Downloadable Reports
Generate downloadable text reports summarizing:
- selected gene
- selected variant
- clinical significance
- explanation summary

---

## Data Visualizations
Visualize:
- clinical significance distribution
- variation type distribution
- review status distribution

---

# Technologies Used

## Frontend
- Streamlit

## Backend
- Python

## Data Processing
- pandas

## APIs
- Ensembl REST API
- NCBI ClinVar API
- NCBI PubMed API

## Visualization
- Streamlit Charts
- Plotly (optional)

---

# Project Structure

```text
genomics-dashboard/
├── Search.py
├── requirements.txt
├── README.md
│
├── services/
│   ├── clinvar_api.py
│   ├── ensembl_api.py
│   └── pubmed_api.py
│
├── pages/
│   ├── Clinical Evidence.py
│   └── Visualizations.py
```

---

# Installation

## Clone the repository

```bash
git clone <https://github.com/AmaniPaul/genomics-dashboard>
cd genomics-dashboard
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the application

```bash
streamlit run Search.py
```

---

# Example Workflow

```text
Search Gene
    ↓
Retrieve ClinVar Variants
    ↓
Filter Variants
    ↓
Select Variant
    ↓
View Clinical Evidence
    ↓
Search PubMed Literature
    ↓
Generate AI Explanation
    ↓
Download Report
```

---

# Future Improvements

Potential future upgrades:
- OpenAI API integration
- protein structure visualization
- AlphaFold integration
- user authentication
- database persistence
- advanced genomic visualizations
- machine learning classification
- variant pathogenicity prediction

---

# Educational Disclaimer

This application is for educational and demonstration purposes only.

It is NOT intended for:
- medical diagnosis
- treatment decisions
- clinical interpretation
- healthcare advice

All genomic interpretations should be reviewed by qualified professionals.

---

# Author

Built as a computational biology and software engineering portfolio project demonstrating the intersection of:
- computer science
- biotechnology
- bioinformatics
- AI-assisted scientific software

