import streamlit as st
from PIL import Image
import cv2
import numpy as np
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ---- SAFE OCR IMPORTS ----
OCR_AVAILABLE = True

try:
    import easyocr
except Exception:
    easyocr = None
    OCR_AVAILABLE = False

try:
    import pytesseract
except Exception:
    pytesseract = None

# ---- OCR READER ----
@st.cache_resource
def get_ocr_reader():
    if not easyocr:
        return None
    return easyocr.Reader(['en'], gpu=False)

# ---- IMAGE PREPROCESSING ----
def preprocess_image(image, preprocessing_type):
    img_array = np.array(image)

    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array

    if preprocessing_type == "Threshold":
        processed = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]
    elif preprocessing_type == "Adaptive Threshold":
        processed = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
    elif preprocessing_type == "Noise Removal":
        processed = cv2.medianBlur(gray, 3)
    else:
        processed = gray

    return Image.fromarray(processed)

# ---- MAIN UI ----
def show():
    st.markdown("## 🔍 OCR & Text Tools")

    if not OCR_AVAILABLE:
        st.warning(
            "⚠️ OCR features are disabled on cloud deployment.\n\n"
            "Reason: Heavy ML libraries (EasyOCR / Tesseract) are not supported.\n\n"
            "Run this app locally to enable OCR."
        )
        return

    tabs = st.tabs([
        "Image OCR",
        "Batch OCR",
        "Handwriting OCR",
        "PDF OCR"
    ])

    # ---------- IMAGE OCR ----------
    with tabs[0]:
        uploaded = st.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg']
        )

        if uploaded:
            image = Image.open(uploaded)
            col1, col2 = st.columns(2)

            with col1:
                st.image(image, use_container_width=True)

            with col2:
                preprocess = st.selectbox(
                    "Preprocessing",
                    ["None", "Threshold", "Adaptive Threshold", "Noise Removal"]
                )

                processed = (
                    preprocess_image(image, preprocess)
                    if preprocess != "None"
                    else image
                )

                st.image(processed, use_container_width=True)

            if st.button("Extract Text"):
                reader = get_ocr_reader()
                with st.spinner("Processing..."):
                    if reader:
                        results = reader.readtext(np.array(processed))
                        text = "\n".join([r[1] for r in results])
                    else:
                        text = pytesseract.image_to_string(processed)

                st.text_area("Extracted Text", text, height=300)
                st.download_button(
                    "Download Text",
                    text,
                    "ocr_output.txt",
                    "text/plain"
                )

    # ---------- BATCH OCR ----------
    with tabs[1]:
        uploaded_files = st.file_uploader(
            "Upload Images",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True
        )

        if uploaded_files and st.button("Process All"):
            reader = get_ocr_reader()
            all_text = []

            for file in uploaded_files:
                image = Image.open(file)
                results = reader.readtext(np.array(image))
                text = "\n".join([r[1] for r in results])
                all_text.append(f"=== {file.name} ===\n{text}\n\n")

            combined = "".join(all_text)
            st.download_button(
                "Download All",
                combined,
                "batch_ocr.txt",
                "text/plain"
            )

    # ---------- HANDWRITING ----------
    with tabs[2]:
        uploaded = st.file_uploader(
            "Upload Handwritten Image",
            type=['png', 'jpg', 'jpeg']
        )

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True)

            if st.button("Recognize"):
                processed = preprocess_image(image, "Threshold")
                reader = get_ocr_reader()
                results = reader.readtext(
                    np.array(processed),
                    paragraph=True
                )
                text = "\n".join([r[1] for r in results])
                st.text_area("Recognized Text", text, height=300)

    # ---------- PDF OCR ----------
    with tabs[3]:
        st.info(
            "PDF OCR is disabled on cloud.\n\n"
            "Use local deployment or OCR API."
        )
