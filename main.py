import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

# CTR values by keyword position (default)
DEFAULT_CTR_VALUES = {
    i: val for i, val in zip(range(1, 21),
        [0.35, 0.18, 0.11, 0.07, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01,
         0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
}

st.set_page_config(page_title="Keyword Performance Projection", layout="wide")
st.title("🔍 Keyword Performance Projection")

with st.expander("📊 Customize Click-Through Rates (CTR)"):
    custom_ctr = st.checkbox("Customize CTR values")
    ctr_values = {}
    for i in range(1, 21):
        if custom_ctr:
            ctr_values[i] = st.number_input(f"Position {i} CTR (%)", min_value=0.0, max_value=100.0,
                                             value=DEFAULT_CTR_VALUES[i]*100, step=0.1) / 100
        else:
            ctr_values = DEFAULT_CTR_VALUES
            break

st.markdown("""
<style>
    .metrics-box {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

with st.form("projection_form"):
    st.subheader("📥 Input Your Keyword Data")
    keyword = st.text_input("Keyword")
    current_position = st.number_input("Current Keyword Position", min_value=1, max_value=20, step=1)
    target_position = st.number_input("Target Keyword Position", min_value=1, max_value=20, step=1)
    keyword_volume = st.number_input("Current Keyword Volume", min_value=0)
    conversion_rate = st.number_input("Estimated Conversion Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
    close_rate = st.number_input("Estimated Close Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
    average_order_value = st.number_input("Average Order Value ($)", min_value=0.0)
    submitted = st.form_submit_button("Calculate")

if submitted:
    if current_position == target_position:
        st.warning("Current and target positions are the same. Try changing one of them to see a projection.")
    else:
        # Convert rates to decimals
        conversion_rate /= 100
        close_rate /= 100

        # Calculate current metrics
        ctr_current = ctr_values.get(current_position, 0)
        current_clicks = ctr_current * keyword_volume
        current_conversions = current_clicks * conversion_rate
        current_closes = current_conversions * close_rate
        current_revenue = current_closes * average_order_value

        # Calculate projected metrics
        ctr_target = ctr_values.get(target_position, 0)
        projected_clicks = ctr_target * keyword_volume
        projected_conversions = projected_clicks * conversion_rate
        projected_closes = projected_conversions * close_rate
        projected_revenue = projected_closes * average_order_value

        # Metrics display
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='metrics-box'>", unsafe_allow_html=True)
            st.subheader("📉 Current Metrics")
            st.write(f"CTR: {ctr_current * 100:.2f}%")
            st.write(f"Monthly Clicks: {current_clicks:.0f}")
            st.write(f"Conversions: {current_conversions:.0f}")
            st.write(f"Closes: {current_closes:.0f}")
            st.write(f"Revenue: ${current_revenue:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='metrics-box'>", unsafe_allow_html=True)
            st.subheader("🚀 Projected Metrics")
            st.write(f"CTR: {ctr_target * 100:.2f}%")
            st.write(f"Monthly Clicks: {projected_clicks:.0f}")
            st.write(f"Conversions: {projected_conversions:.0f}")
            st.write(f"Closes: {projected_closes:.0f}")
            st.write(f"Revenue: ${projected_revenue:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        # Comparison chart
        st.subheader("📈 Revenue Comparison")
        fig, ax = plt.subplots()
        ax.bar(["Current", "Projected"], [current_revenue, projected_revenue], color=["#6fa8dc", "#f4a460"])
        ax.set_ylabel("Revenue ($)")
        st.pyplot(fig)

        # Export results to CSV
        df = pd.DataFrame({
            "Metric": ["CTR", "Clicks", "Conversions", "Closes", "Revenue"],
            "Current": [f"{ctr_current*100:.2f}%", int(current_clicks), int(current_conversions), int(current_closes), f"${current_revenue:,.2f}"],
            "Projected": [f"{ctr_target*100:.2f}%", int(projected_clicks), int(projected_conversions), int(projected_closes), f"${projected_revenue:,.2f}"]
        })

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV Report", data=csv, file_name="keyword_projection.csv", mime="text/csv")
