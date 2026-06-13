import streamlit as st
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="A/B Testing Simulator",
    layout="wide"
)

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Overview",
        "A/B Results",
        "Device Analysis",
        "Country Analysis",
        "Recommendation"
    ]
)

# ---------------------------
# Main Title
# ---------------------------
st.title("📊 A/B Testing Simulator")

uploaded_file = st.file_uploader(
    "Upload Experiment CSV",
    type=["csv"]
)

# ---------------------------
# Load Data
# ---------------------------
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # ---------------------------
    # Basic Metrics
    # ---------------------------
    total_users = len(df)

    total_clicks = df["click"].sum()

    overall_ctr = (
        total_clicks /
        total_users
        * 100
    )

    # ---------------------------
    # A/B Summary
    # ---------------------------
    summary = (
        df.groupby("variant")
        .agg(
            impressions=("click", "count"),
            clicks=("click", "sum")
        )
    )

    summary["CTR (%)"] = (
        summary["clicks"]
        /
        summary["impressions"]
        * 100
    )

    clicks = summary["clicks"].values
    impressions = summary["impressions"].values

    z_stat, p_value = proportions_ztest(
        count=clicks,
        nobs=impressions
    )

    # ===========================
    # OVERVIEW PAGE
    # ===========================
    if page == "Overview":

        st.header("Experiment Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Users",
                total_users
            )

        with col2:
            st.metric(
                "Total Clicks",
                total_clicks
            )

        with col3:
            st.metric(
                "Overall CTR",
                f"{overall_ctr:.2f}%"
            )

        st.markdown("---")

        st.write("""
        ### Objective

        Compare Version A and Version B and determine
        whether the new version improves CTR.

        This dashboard performs:
        - CTR Analysis
        - A/B Testing
        - Statistical Significance Testing
        - Device Analysis
        - Country Analysis
        """)

    # ===========================
    # A/B RESULTS PAGE
    # ===========================
    elif page == "A/B Results":

        st.header("A/B Test Results")

        st.subheader("CTR Summary")

        st.dataframe(summary)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Z Statistic",
                round(z_stat, 4)
            )

        with col2:
            st.metric(
                "P Value",
                round(p_value, 6)
            )

        if p_value < 0.05:
            st.success(
                "✅ Statistically Significant"
            )
        else:
            st.error(
                "❌ Not Significant"
            )

        st.subheader("CTR Comparison")

        st.bar_chart(
            summary["CTR (%)"]
        )

    # ===========================
    # DEVICE ANALYSIS PAGE
    # ===========================
    elif page == "Device Analysis":

        st.header("Device Analysis")

        device_ctr = (
            df.groupby(
                ["device", "variant"]
            )["click"]
            .mean()
            .reset_index()
        )

        device_ctr["CTR (%)"] = (
            device_ctr["click"] * 100
        )

        st.dataframe(device_ctr)

        chart_data = (
            device_ctr.pivot(
                index="device",
                columns="variant",
                values="CTR (%)"
            )
        )

        st.bar_chart(chart_data)

    # ===========================
    # COUNTRY ANALYSIS PAGE
    # ===========================
    elif page == "Country Analysis":

        st.header("Country Analysis")

        country_ctr = (
            df.groupby(
                ["country", "variant"]
            )["click"]
            .mean()
            .reset_index()
        )

        country_ctr["CTR (%)"] = (
            country_ctr["click"] * 100
        )

        st.dataframe(country_ctr)

        chart_data = (
            country_ctr.pivot(
                index="country",
                columns="variant",
                values="CTR (%)"
            )
        )

        st.bar_chart(chart_data)

    # ===========================
    # RECOMMENDATION PAGE
    # ===========================
    elif page == "Recommendation":

        st.header("Final Recommendation")

        ctr_a = summary.loc["A", "CTR (%)"]
        ctr_b = summary.loc["B", "CTR (%)"]

        lift = (
            (ctr_b - ctr_a)
            / ctr_a
            * 100
        )

        st.metric(
            "CTR Lift (%)",
            f"{lift:.2f}%"
        )

        st.metric(
            "P Value",
            round(p_value, 6)
        )

        if p_value < 0.05:

            st.success(
                f"""
                Version B improved CTR by
                {lift:.2f}%.

                The result is statistically
                significant.

                Recommendation:
                Deploy Version B.
                """
            )

        else:

            st.warning(
                """
                No statistically significant
                difference detected.

                Recommendation:
                Continue testing.
                """
            )

else:

    st.info(
        "Please upload ab_testing_data.csv to continue."
    )
