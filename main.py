import streamlit as st
import matplotlib.pyplot as plt

# CTR values by keyword position
CTR_VALUES = {
    1: 0.35, 2: 0.18, 3: 0.11, 4: 0.07, 5: 0.04,
    6: 0.03, 7: 0.02, 8: 0.02, 9: 0.01, 10: 0.01,
    11: 0.01, 12: 0.01, 13: 0.01, 14: 0.01, 15: 0.01,
    16: 0.01, 17: 0.01, 18: 0.01, 19: 0.01, 20: 0.01
}

st.set_page_config(page_title="Keyword Performance Projection", layout="wide")

st.title("🔍 Keyword Performance Projection")

with st.form("projection_form"):
    keyword = st.text_input("Keyword")
    current_position = st.number_input("Current Keyword Position", min_value=1, max_value=20, step=1)
    target_position = st.number_input("Target Keyword Position", min_value=1, max_value=20, step=1)
    keyword_volume = st.number_input("Current Keyword Volume", min_value=0)
    conversion_rate = st.number_input("Estimated Conversion Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
    close_rate = st.number_input("Estimated Close Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
    average_order_value = st.number_input("Average Order Value", min_value=0.0)

    submitted = st.form_submit_button("Calculate")

if submitted:
    conversion_rate /= 100
    close_rate /= 100

    # Current Metrics
    ctr_current = CTR_VALUES.get(current_position, 0)
    current_clicks = ctr_current * keyword_volume
    current_conversions = current_clicks * conversion_rate
    current_closes = current_conversions * close_rate
    current_revenue = current_closes * average_order_value

    # Projected Metrics
    ctr_target = CTR_VALUES.get(target_position, 0)
    projected_clicks = ctr_target * keyword_volume
    projected_conversions = projected_clicks * conversion_rate
    projected_closes = projected_conversions * close_rate
    projected_revenue = projected_closes * average_order_value

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Current Metrics")
        st.write(f"CTR: {ctr_current * 100:.2f}%")
        st.write(f"Monthly Clicks: {current_clicks:.0f}")
        st.write(f"Monthly Conversions: {current_conversions:.0f}")
        st.write(f"Monthly Closes: {current_closes:.0f}")
        st.write(f"Monthly Revenue: ${current_revenue:.2f}")

    with col2:
        st.subheader("🚀 Projected Metrics")
        st.write(f"CTR: {ctr_target * 100:.2f}%")
        st.write(f"Monthly Clicks: {projected_clicks:.0f}")
        st.write(f"Monthly Conversions: {projected_conversions:.0f}")
        st.write(f"Monthly Closes: {projected_closes:.0f}")
        st.write(f"Monthly Revenue: ${projected_revenue:.2f}")

    # Revenue Comparison Chart
    st.subheader("💰 Revenue Comparison")
    fig, ax = plt.subplots()
    ax.bar(["Current Revenue", "Projected Revenue"], [current_revenue, projected_revenue], color=["skyblue", "lightcoral"])
    ax.set_ylabel("Revenue ($)")
    ax.set_title("Current vs Projected Revenue")
    st.pyplot(fig)
