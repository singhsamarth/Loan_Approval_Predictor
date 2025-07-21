import streamlit as st
from PIL import Image
import pickle
import base64
from io import BytesIO

# Load ML model
model = pickle.load(open('./Model/ML_Model.pkl', 'rb'))

# Convert image to base64 to embed it
def Image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

# Inject custom CSS
st.markdown("""
    <style>
        .center-logo {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }

        .stApp {
            background: linear-gradient(135deg, #f0f4f8, #e6f0ff);
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3, h4 {
            text-align: center;
            color: #1f2937;
        }

        .section {
            background-color: #ffffff;
            padding: 2em;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }

        .stSelectbox > div, .stNumberInput > div, .stTextInput > div {
            padding: 0.4em !important;
            border-radius: 10px !important;
        }

        input, select, textarea {
            border-radius: 8px !important;
        }

        input:focus, select:focus {
            border-color: #005eff !important;
            box-shadow: 0 0 4px rgba(0, 94, 255, 0.4) !important;
        }

        .stButton > button {
            background-color: #0066cc;
            color: white;
            border-radius: 10px;
            padding: 0.6em 1.5em;
            border: none;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #004c99;
        }

        .stAlert {
            border-radius: 10px !important;
            padding: 1.2em !important;
        }
    </style>
""", unsafe_allow_html=True)


# Main Function
def run():
    # Bank logo centered
    img1 = Image.open('bank.png')
    st.markdown(
        '<div class="center-logo"><img src="data:image/png;base64,{}" width="140"></div>'.format(
            Image_to_base64(img1)
        ), unsafe_allow_html=True
    )

    st.title("🏦 Bank Loan Prediction using Machine Learning")
    st.markdown("#### _Fill the form below to check if you're eligible for a bank loan._")

    # --- Section 1: Personal Info ---
    with st.container():
        st.markdown("#### 🔍 Personal Information")
        st.markdown('<div class="section">', unsafe_allow_html=True)

        account_no = st.text_input('📄 Account Number')
        fn = st.text_input('🧑 Full Name')
        gen = st.selectbox("Gender", ['Female', 'Male'])
        mar = st.selectbox("Marital Status", ['No', 'Yes'])
        dep = st.selectbox("Number of Dependents", ['No', 'One', 'Two', 'More than Two'])
        edu = st.selectbox("Education", ['Not Graduate', 'Graduate'])
        emp = st.selectbox("Employment Status", ['Job', 'Business'])
        prop = st.selectbox("Property Area", ['Rural', 'Semi-Urban', 'Urban'])
        cred = st.selectbox("Credit Score", ['Between 300 to 500', 'Above 500'])

        st.markdown('</div>', unsafe_allow_html=True)

    # --- Section 2: Financial Info ---
    with st.container():
        st.markdown("#### 💰 Financial Information")
        st.markdown('<div class="section">', unsafe_allow_html=True)

        mon_income = st.number_input("Applicant's Monthly Income ($)", min_value=0, step=100)
        co_mon_income = st.number_input("Co-Applicant's Monthly Income ($)", min_value=0, step=100)
        loan_amt = st.number_input("Loan Amount (in thousands $)", min_value=0, step=10)
        dur_display = ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month']
        dur = st.selectbox("Loan Duration", dur_display)

        st.markdown('</div>', unsafe_allow_html=True)

    # Map duration to numerical
    dur_map = {
        '2 Month': 60,
        '6 Month': 180,
        '8 Month': 240,
        '1 Year': 360,
        '16 Month': 480
    }
    duration = dur_map[dur]

    # --- Predict ---
    if st.button("📊 Submit for Prediction"):
        if not account_no.strip() or not fn.strip():
            st.warning("Please enter your full name and account number.")
            return
        if mon_income <= 0 or loan_amt <= 0:
            st.warning("Monthly income and loan amount must be greater than 0.")
            return

        # Encode categorical variables
        gen_val = 1 if gen == 'Male' else 0
        mar_val = 1 if mar == 'Yes' else 0
        dep_val = ['No', 'One', 'Two', 'More than Two'].index(dep)
        edu_val = 1 if edu == 'Graduate' else 0
        emp_val = 1 if emp == 'Business' else 0
        cred_val = 1 if cred == 'Above 500' else 0
        prop_val = ['Rural', 'Semi-Urban', 'Urban'].index(prop)

        # Feature vector
        features = [[
            gen_val, mar_val, dep_val, edu_val, emp_val,
            mon_income, co_mon_income, loan_amt, duration,
            cred_val, prop_val
        ]]

        prediction = model.predict(features)[0]

        st.markdown("---")
        if prediction == 0:
            st.error(
                f"🚫 Hello **{fn}** (Account: `{account_no}`),\n\n"
                "Unfortunately, you are **not eligible** for the loan based on your details."
            )
        else:
            st.success(
                f"✅ Hello **{fn}** (Account: `{account_no}`),\n\n"
                "🎉 Congratulations! You are **eligible** for the loan."
            )


run()
