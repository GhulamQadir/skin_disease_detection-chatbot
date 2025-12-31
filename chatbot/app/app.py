import streamlit as st
from disease_info import DiseaseInfo
from image_processor import ImageProcessor
from PIL import Image
import time


class App:
    DISCLAIMER_TEXT = "This app is for educational purposes only. It does not provide professional medical advice. Always consult a licensed healthcare provider."

    def __init__(self):
        self.image_Processor = ImageProcessor()
        self.disease_info = DiseaseInfo()

    def run(self):
        st.header("🩺 Skin Disease Detection ChatBot")

        if "show_disclaimer" not in st.session_state:
            st.session_state.show_disclaimer = False

        if st.button("Show Disclaimer"):
            st.session_state.show_disclaimer = True

        if st.session_state.show_disclaimer:

            @st.dialog(
                title=App.DISCLAIMER_TEXT,
                width="small",
                dismissible=True,
                on_dismiss="ignore",
            )
            def disclaimer_dialog():
                pass

            disclaimer_dialog()

        # File uploader
        uploaded_image = st.file_uploader(
            "Upload an image of affected area", type=["jpg", "jpeg", "png"]
        )

        # Process button
        process_btn = st.button("Process")
        st.session_state.show_disclaimer = False

        if uploaded_image:
            # Open the image using Pillow
            image = Image.open(uploaded_image)
            resized_image = image.resize((680, 230))
            st.image(resized_image)
        if process_btn and uploaded_image is not None:
            with st.spinner("Processing Image"):
                # Process the uploaded image
                disease_name = self.image_Processor.process_image(uploaded_image)
                if disease_name != "Not Detected":
                    # Get disease info from dictionary
                    info = self.disease_info.get_info(disease_name)

                    st.success(f"Disease Detected: **{disease_name}**")
                    st.subheader("Description")
                    st.write(info.get("description"))
                    st.subheader("Treatment")
                    st.write(info.get("treatment"))
                else:
                    st.warning("No skin disease detected. Please try another image.")
        elif process_btn and uploaded_image is None:
            st.error("Please Upload an image of affected area")
