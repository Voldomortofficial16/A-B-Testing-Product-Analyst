import streamlit as st
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

st.set_page_config(
    page_title="A/B Testing Simulator",
    layout="wide"
)

st.title("📊 A/B Testing Simulator")

uploaded_file = st.file_uploader(
    "Upload Experiment CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    summary = (
        df.groupby('variant')
        .agg(
            impressions=('click','count'),
            clicks=('click','sum')
        )
    )

    summary['CTR (%)'] = (
        summary['clicks']
        /
        summary['impressions']
        *100
    )

    st.subheader("CTR Summary")
    st.dataframe(summary)

    clicks = summary['clicks'].values
    impressions = summary['impressions'].values

    z_stat, p_value = proportions_ztest(
        count=clicks,
        nobs=impressions
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Z Statistic",
            round(z_stat,4)
        )

    with col2:
        st.metric(
            "P Value",
            round(p_value,6)
        )

    if p_value < 0.05:
        st.success("✅ Statistically Significant")
    else:
        st.error("❌ Not Significant")

    st.bar_chart(summary['CTR (%)'])
