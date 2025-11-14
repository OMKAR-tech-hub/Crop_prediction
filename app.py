import streamlit as st
import numpy as np
import pickle

# -------------------------------
# SILENT MODEL LOADING
# -------------------------------
def load_model():
    try:
        return pickle.load(open("model.pkl", "rb"))
    except:
        return None

def load_scaler():
    try:
        return pickle.load(open("scaler.pkl", "rb"))
    except:
        return None

model = load_model()
scaler = load_scaler()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Crop Prediction", layout="wide")

# -------------------------------
# CUSTOM CSS FOR BEAUTIFUL UI
# -------------------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

/* PAGE BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #1b4332, #2d6a4f, #40916c);
    padding: 20px;
}

/******** TITLE ********/
h1 {
    color: #b7fbd3 !important;
    text-shadow: 0px 0px 12px #00ffb3;
    font-weight: 800 !important;
    text-align: center;
}

/******** CARD ********/
.block-container {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    animation: fadeIn 1.2s ease-in-out;
}

/******** INPUT BOXES ********/
input[type="number"] {
    background: #ffffffdd !important;
    border-radius: 10px !important;
    height: 45px;
    font-size: 16px;
}

/******** BUTTON ********/
button[kind="primary"] {
    background-color: #52b788 !important;
    border-radius: 10px !important;
    padding: 10px 25px !important;
    font-size: 18px !important;
    border: none;
}

button[kind="primary"]:hover {
    background-color: #74c69d !important;
    transform: scale(1.05);
}

/******** RESULT CARD ********/
.result-card {
    background: rgba(0,0,0,0.55);
    padding: 25px;
    border-radius: 15px;
    margin-top: 20px;
    color: #b7fbd3;
    font-size: 17px;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)


# -------------------------------
# UI START
# -------------------------------
st.markdown("<h1 class='title'>🌾 Crop Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enter the soil & weather values below</p>", unsafe_allow_html=True)

st.markdown("<div class='glass-box'>", unsafe_allow_html=True)

# -------------------------------
# INPUT COLUMNS
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    N = st.number_input("Nitrogen", value=0.0)

with col2:
    P = st.number_input("Phosphorus", value=0.0)

with col3:
    K = st.number_input("Potassium", value=0.0)

col4, col5, col6 = st.columns(3)

with col4:
    temperature = st.number_input("Temperature (°C)", value=0.0)

with col5:
    humidity = st.number_input("Humidity (%)", value=0.0)

with col6:
    ph = st.number_input("pH Value", value=0.0)

rainfall = st.number_input("Rainfall (mm)", value=0.0)

# -------------------------------
# PREDICTION LOGIC (UNCHANGED)
# -------------------------------
if st.button("Predict Crop"):

    if model is None:
        st.error("Model file missing! Upload model.pkl.")
    else:
        try:
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

            if scaler:
                data = scaler.transform(data)

            pred = model.predict(data)[0]

            crop_dict = {
                1: "Rice", 2: "Maize", 3: "Chickpea", 4: "Kidneybeans",
                5: "Pigeonpeas", 6: "Mothbeans", 7: "Mungbean",
                8: "Blackgram", 9: "Lentil", 10: "Pomegranate",
                11: "Banana", 12: "Mango", 13: "Grapes",
                14: "Watermelon", 15: "Muskmelon", 16: "Apple",
                17: "Orange", 18: "Papaya", 19: "Coconut",
                20: "Cotton", 21: "Jute", 22: "Coffee"
            }

            crop = crop_dict.get(int(pred), "Unknown Crop")

            result = f"""
**🌱 Recommended Crop:** {crop}

**📝 Suggestions:**
- Ensure proper irrigation and soil fertility  
- Maintain correct pH value and nutrient balance  
- Monitor rainfall & humidity for better growth  
"""

            st.markdown(f"<div class='result-card'>{result}</div>", unsafe_allow_html=True)

            file_text = (
                f"Recommended Crop: {crop}\n\n"
                "Suggestions:\n"
                "- Ensure proper irrigation and soil fertility.\n"
                "- Maintain correct pH and nutrients.\n"
                "- Monitor rainfall & humidity."
            )

            st.download_button(
                "📥 Download Result (TXT)",
                data=file_text,
                file_name="crop_prediction.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error("Error during prediction. Check input values or model file.")

st.markdown("</div>", unsafe_allow_html=True)


