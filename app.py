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
# STREAMLIT UI
# -------------------------------
st.title("🌾 Crop Prediction System")
st.write("Enter the soil & weather values below:")

# Inputs
N = st.number_input("Nitrogen", value=0.0)
P = st.number_input("Phosphorus", value=0.0)
K = st.number_input("Potassium", value=0.0)
temperature = st.number_input("Temperature (°C)", value=0.0)
humidity = st.number_input("Humidity (%)", value=0.0)
ph = st.number_input("pH Value", value=0.0)
rainfall = st.number_input("Rainfall (mm)", value=0.0)

# -------------------------------
# PREDICTION LOGIC
# -------------------------------
if st.button("Predict Crop"):

    if model is None:
        st.error("Model file missing! Upload model.pkl.")
    else:
        try:
            # Create input array
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

            # Scale
            if scaler:
                data = scaler.transform(data)

            pred = model.predict(data)[0]

            # Crop dictionary
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

            # Result Text
            result = f"""
🌱 **Recommended Crop:** {crop}

📝 **Suggestions:**
• Ensure proper irrigation and soil fertility.  
• Maintain correct pH value and nutrient balance.  
• Monitor rainfall & humidity for better growth.  
"""
            st.success(result)

            # Download Button
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

