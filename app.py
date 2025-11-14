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

/* 🌈 Multi-Color Premium Background Gradient */
.stApp {
    background: linear-gradient(135deg,
        #0f2027 0%,
        #203a43 25%,
        #2c5364 50%,
        #005f73 75%,
        #94d2bd 100%
    );
    padding: 20px;
}

/******** 🌟 Glowing Title ********/
h1 {
    color: #eaffd0 !important;
    text-shadow:
        0 0 5px #38b000,
        0 0 10px #70e000,
        0 0 20px #9ef01a;
    font-weight: 800 !important;
    text-align: center;
    letter-spacing: 2px;
}

/******** 🧊 Glass Card Container ********/
.block-container {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(18px);
    padding: 45px;
    border-radius: 30px;
    max-width: 1200px;
    margin: auto;
    box-shadow: 
        0 8px 25px rgba(0,0,0,0.35),
        inset 0 0 20px rgba(255,255,255,0.15);
    animation: fadeIn 1.4s ease-in-out;
}

/******** ✨ Fade-in Animation ********/
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

/******** 📝 Stylish Labels ********/
label {
    color: #eaffd0 !important;
    font-weight: 600 !important;
    font-size: 16px;
}

/******** 🔳 Beautiful Input Boxes ********/
input[type="number"] {
    background: rgba(255,255,255,0.85) !important;
    border-radius: 12px !important;
    height: 50px;
    font-size: 17px;
    border: 2px solid #b5e48c !important;
    transition: 0.3s;
}

input[type="number"]:hover {
    border-color: #52b788 !important;
    box-shadow: 0 0 8px #b5e48c;
}

/******** 🟢 Premium Button ********/
button[kind="primary"] {
    background: linear-gradient(135deg, #80ed99, #38b000) !important;
    color: black !important;
    border-radius: 12px !important;
    padding: 15px 30px !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    border: none !important;
    transition: 0.3s ease;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}

button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.04);
    background: linear-gradient(135deg, #b5e48c, #52b788) !important;
    box-shadow: 0 6px 14px rgba(0,0,0,0.45);
}

/******** 🟦 Result Card ********/
.result-card {
    background: rgba(0, 0, 0, 0.55);
    padding: 30px;
    border-radius: 20px;
    margin-top: 25px;
    color: #d8f3dc;
    font-size: 18px;
    border-left: 4px solid #70e000;
    box-shadow: 0 4px 18px rgba(0,0,0,0.3);
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


