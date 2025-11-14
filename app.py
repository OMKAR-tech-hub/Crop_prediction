import streamlit as st
import numpy as np
import pickle

# -------------------------------
# Load model and scaler safely
# -------------------------------
try:
    model = pickle.load(open('model.pkl', 'rb'))
    st.write("✅ Model loaded.")
except Exception as e:
    st.write("❌ Model not found or invalid:", e)

try:
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    st.write("✅ Scaler loaded.")
except Exception as e:
    scaler = None
    st.write("⚠️ Scaler not found:", e)

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🌾 Crop Prediction System")
st.write("Enter the soil & weather values below:")

N = st.number_input("Nitrogen", value=0.0)
P = st.number_input("Phosphorus", value=0.0)
K = st.number_input("Potassium", value=0.0)
temperature = st.number_input("Temperature", value=0.0)
humidity = st.number_input("Humidity", value=0.0)
ph = st.number_input("pH Value", value=0.0)
rainfall = st.number_input("Rainfall", value=0.0)

# -------------------------------
# Predict button
# -------------------------------
if st.button("Predict Crop"):
    try:
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        # Scale if scaler exists
        if scaler is not None:
            input_data = scaler.transform(input_data)

        # Predict
        prediction = model.predict(input_data)

        # Crop dictionary mapping
        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Chickpea", 4: "Kidneybeans", 5: "Pigeonpeas",
            6: "Mothbeans", 7: "Mungbean", 8: "Blackgram", 9: "Lentil",
            10: "Pomegranate", 11: "Banana", 12: "Mango", 13: "Grapes", 14: "Watermelon",
            15: "Muskmelon", 16: "Apple", 17: "Orange", 18: "Papaya", 19: "Coconut",
            20: "Cotton", 21: "Jute", 22: "Coffee"
        }

        crop = crop_dict.get(int(prediction[0]), "Unknown Crop")

        # ------------------------------
        # Suggestion Text (Your original message)
        # ------------------------------
        result = f"""
🌱 **Recommended Crop:** {crop}

📝 **Suggestions:**
• Ensure proper irrigation and soil fertility.
• Maintain correct pH value and nutrient balance.
• Monitor rainfall & humidity for better growth.
"""

        st.success(result)

        # ------------------------------
        # Download TXT button
        # ------------------------------
        file_content = f"Recommended Crop: {crop}\n\nSuggestions:\n- Ensure proper irrigation and soil fertility.\n- Maintain correct pH and nutrients.\n- Monitor rainfall & humidity."

        st.download_button(
            label="📥 Download Result as TXT",
            data=file_content,
            file_name="crop_prediction.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")
