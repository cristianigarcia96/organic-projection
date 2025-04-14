import streamlit as st
import pandas as pd

st.set_page_config(page_title="Keyword Value Calculator", layout="centered")

st.markdown("""
    <style>
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {
            border-radius: 0.5rem;
        }
        .stButton>button {
            background-color: #24554F;
            color: white;
            border-radius: 0.5rem;
            padding: 0.5rem 1.5rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1E4742;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 800px;
            margin: 0 auto;
        }
        .result-card {
            background-color: #FBEDE6;
            border-left: 6px solid #24554F;
            padding: 1rem;
            border-radius: 0.75rem;
            margin-top: 1rem;
        }
        .result-card h4 {
            margin: 0;
            color: #1F1A17;
        }
        .result-card p {
            margin: 0.25rem 0 0;
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 📩 Input Your Keyword Data")

with st.container():
    with st.form("keyword_form"):
        st.markdown("### 🔍 Keyword Details")
        keyword = st.text_input("Keyword", key="kw")

        keyword_type = st.selectbox(
            "Select Keyword Type",
            ["Branded", "Navigational", "Informational", "Transactional", "Commercial", "Local"]
        )

        ctr_models = {
            "Branded": 0.35,
            "Navigational": 0.20,
            "Informational": 0.07,
            "Transactional": 0.25,
            "Commercial": 0.12,
            "Local": 0.30
        }

        col1, col2 = st.columns(2)
        with col1:
            current_position = st.number_input("Current Keyword Position", min_value=1, max_value=100, value=5, key="cp")
        with col2:
            target_position = st.number_input("Target Keyword Position", min_value=1, max_value=100, value=1, key="tp")

        keyword_volume = st.number_input("Current Keyword Volume", min_value=0, value=100, step=10, key="vol")

        st.markdown("### 💰 Conversion & Revenue Estimates")
        col3, col4 = st.columns(2)
        with col3:
            conversion_rate = st.number_input("Estimated Conversion Rate (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.1, key="cr")
        with col4:
            close_rate = st.number_input("Estimated Close Rate (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key="clr")

        aov = st.number_input("Average Order Value ($)", min_value=0.0, value=100.0, step=10.0, key="aov")

        submitted = st.form_submit_button("Calculate")

        if submitted:
            ctr_value = ctr_models.get(keyword_type, 0.20)

            def get_ctr(position, base_ctr):
                if position <= 1:
                    return base_ctr
                elif position <= 3:
                    return base_ctr * 0.75
                elif position <= 5:
                    return base_ctr * 0.5
                elif position <= 10:
                    return base_ctr * 0.25
                else:
                    return base_ctr * 0.1

            traffic_current = keyword_volume * get_ctr(current_position, ctr_value)
            traffic_target = keyword_volume * get_ctr(target_position, ctr_value)
            traffic_gain = traffic_target - traffic_current

            leads = traffic_gain * (conversion_rate / 100)
            closed_sales = leads * (close_rate / 100)
            revenue_gain = closed_sales * aov

            st.success("✅ Calculation completed!")

            st.markdown(f"""
                <div class=\"result-card\">
                    <h4>📈 Estimated Additional Monthly Revenue:</h4>
                    <p><strong>${revenue_gain:,.2f}</strong></p>
                </div>
                <div class=\"result-card\">
                    <h4>📊 Estimated Traffic Gain:</h4>
                    <p>{traffic_gain:.0f} visitors/month</p>
                </div>
                <div class=\"result-card\">
                    <h4>🧲 Leads:</h4>
                    <p>{leads:.1f}</p>
                </div>
                <div class=\"result-card\">
                    <h4>🤝 Closed Deals:</h4>
                    <p>{closed_sales:.1f}</p>
                </div>
            """, unsafe_allow_html=True)
