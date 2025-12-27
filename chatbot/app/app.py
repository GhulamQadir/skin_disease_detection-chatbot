import streamlit as st
import time

# from engine.chatbot_engine import ChatbotEngine
from image_processor import ImageProcessor


class App:
    def __init__(self):
        pass

    def run(self):
        st.header("Skin Disease Detection ChatBot 🔍")
        uploaded_image = st.file_uploader(
            "Upload an image of affected area", type=["jpg", "jpeg", "png"]
        )
        process_btn = st.button("Process")
        image_Processor = ImageProcessor()

        if process_btn and uploaded_image is not None:
            with st.spinner("Processing Image", show_time=True):
                data = image_Processor.process_image(uploaded_image)
                st.write(type(data))
                st.write(data)
        elif process_btn and uploaded_image is None:
            st.error("Please Upload an image of affected area")

            # st.warning(f"Disease Detected")
            # st.header("Disease: **Acne**")
            # st.subheader("Description: ")
            # st.write("Dummy data")
            # st.subheader("Treatment: ")
            # st.write("dummy data")
