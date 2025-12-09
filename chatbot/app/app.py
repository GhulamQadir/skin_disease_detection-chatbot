import streamlit as st
import time
from engine.chatbot_engine import ChatbotEngine


class App:
    def __init__(self):
        pass

    def run(self):
        st.header("Skin Disease Detection ChatBot 🔍")
        uploaded_image = st.file_uploader(
            "Upload an image of affected area", type=["jpg", "jpeg", "png"]
        )
        if uploaded_image is not None:
            st.image(uploaded_image, caption=None, width=400)

            chatbot_engine = ChatbotEngine()

            with st.spinner("Processing Image", show_time=True):
                chatbot_engine.process_image(uploaded_image)

            st.warning(f"Disease Detected")

            st.header("Disease: **Acne**")

            st.subheader("Description: ")
            st.write("Dummy data")

            st.subheader("Treatment: ")
            st.write("dummy data")
