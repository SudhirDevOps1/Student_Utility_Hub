import streamlit as st
from PIL import Image
import easyocr
import pytesseract
import cv2
import numpy as np
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(['en'], gpu=False)

def preprocess_image(image, preprocessing_type):
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    if preprocessing_type == "Threshold":
        processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    elif preprocessing_type == "Adaptive Threshold":
        processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    elif preprocessing_type == "Noise Removal":
        processed = cv2.medianBlur(gray, 3)
    else:
        processed = gray
    
    return Image.fromarray(processed)

def show():
    st.markdown("## 🔍 OCR & Text Tools")
    
    tabs = st.tabs(["Image OCR", "Batch OCR", "Handwriting OCR", "PDF OCR"])
    
    with tabs[0]:
        st.markdown("### 📸 Image to Text (OCR)")
        uploaded = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="ocr_single")
        
        if uploaded:
            image = Image.open(uploaded)
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, use_container_width=True)
            with col2:
                preprocess = st.selectbox("Preprocessing", ["None", "Threshold", "Adaptive Threshold", "Noise Removal"])
                if preprocess != "None":
                    processed = preprocess_image(image, preprocess)
                    st.image(processed, use_container_width=True)
                else:
                    processed = image
            
            if st.button("Extract Text"):
                with st.spinner("Processing..."):
                    try:
                        reader = get_ocr_reader()
                        results = reader.readtext(np.array(processed))
                        text = "\n".join([result[1] for result in results])
                        edited_text = st.text_area("Extracted Text:", text, height=300)
                        st.download_button("Download Text", edited_text, "ocr_output.txt", "text/plain")
                    except:
                        text = pytesseract.image_to_string(processed)
                        st.text_area("Extracted Text:", text, height=300)
    
    with tabs[1]:
        st.markdown("### 📚 Batch Image OCR")
        uploaded_files = st.file_uploader("Upload Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, key="batch_ocr")
        
        if uploaded_files and st.button("Process All"):
            reader = get_ocr_reader()
            all_text = []
            progress = st.progress(0)
            
            for idx, file in enumerate(uploaded_files):
                image = Image.open(file)
                results = reader.readtext(np.array(image))
                text = "\n".join([result[1] for result in results])
                all_text.append(f"=== {file.name} ===\n{text}\n\n")
                progress.progress((idx + 1) / len(uploaded_files))
            
            combined = "".join(all_text)
            st.download_button("Download All", combined, "batch_ocr.txt", "text/plain")
    
    with tabs[2]:
        st.markdown("### ✍️ Handwriting Recognition")
        uploaded = st.file_uploader("Upload Handwritten Image", type=['png', 'jpg', 'jpeg'], key="handwriting")
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True)
            
            if st.button("Recognize"):
                processed = preprocess_image(image, "Threshold")
                reader = get_ocr_reader()
                results = reader.readtext(np.array(processed), paragraph=True)
                text = "\n".join([result[1] for result in results])
                st.text_area("Recognized Text:", text, height=300)
                st.download_button("Download", text, "handwriting.txt", "text/plain")
    
    with tabs[3]:
        st.markdown("### 📄 OCR PDF to Searchable PDF")
        uploaded = st.file_uploader("Upload PDF", type=['pdf'], key="pdf_ocr")
        
        if uploaded:
            st.info("Feature: Convert scanned PDF to searchable text PDF")
            st.warning("Note: Requires PyMuPDF library")
