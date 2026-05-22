import streamlit as st

st.title("Variant Visualizations")

if "variants_df" not in st.session_state or st.session_state.variants_df is None:
    st.error("No variant data found. Search for a gene first.")
    st.stop()

variants_df = st.session_state.variants_df

st.subheader("Clinical Significance Breakdown")
st.bar_chart(variants_df["Clinical Significance"].value_counts())

st.subheader("Variation Type Breakdown")
st.bar_chart(variants_df["Variation Type"].value_counts())

st.subheader("Review Status Breakdown")
st.bar_chart(variants_df["Review Status"].value_counts())

if st.button("Back to Search"):
    st.switch_page("Search.py")