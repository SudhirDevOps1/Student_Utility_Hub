import streamlit as st
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import os

def show():
    st.markdown("## 📄 PDF Tools")
    
    tabs = st.tabs([
        "Merge PDFs",
        "Split PDF",
        "Compress PDF",
        "PDF to Images",
        "Images to PDF",
        "Extract Text",
        "Rotate Pages",
        "Watermark",
        "Password Protect",
        "Metadata Viewer"
    ])
    
    # Merge PDFs
    with tabs[0]:
        st.markdown("### 🔗 Merge PDFs")
        uploaded_files = st.file_uploader("Upload PDFs", type=['pdf'], 
                                         accept_multiple_files=True, key="merge")
        
        if uploaded_files and len(uploaded_files) > 1:
            st.success(f"📁 {len(uploaded_files)} PDFs uploaded")
            
            for i, file in enumerate(uploaded_files):
                st.text(f"{i+1}. {file.name}")
            
            if st.button("Merge PDFs"):
                merger = PdfMerger()
                
                for pdf in uploaded_files:
                    merger.append(pdf)
                
                output = io.BytesIO()
                merger.write(output)
                merger.close()
                output.seek(0)
                
                st.success("✅ PDFs merged successfully!")
                st.download_button("Download Merged PDF", output, "merged.pdf", "application/pdf")
    
    # Split PDF
    with tabs[1]:
        st.markdown("### ✂️ Split PDF")
        uploaded = st.file_uploader("Upload PDF", type=['pdf'], key="split")
        
        if uploaded:
            reader = PdfReader(uploaded)
            total_pages = len(reader.pages)
            
            st.info(f"📄 Total Pages: {total_pages}")
            
            split_mode = st.radio("Split Mode", ["Range", "Individual Pages", "Every N Pages"])
            
            if split_mode == "Range":
                col1, col2 = st.columns(2)
                with col1:
                    start = st.number_input("Start Page", 1, total_pages, 1)
                with col2:
                    end = st.number_input("End Page", 1, total_pages, total_pages)
                
                if st.button("Extract Range"):
                    writer = PdfWriter()
                    for i in range(start-1, end):
                        writer.add_page(reader.pages[i])
                    
                    output = io.BytesIO()
                    writer.write(output)
                    output.seek(0)
                    
                    st.download_button("Download", output, f"pages_{start}-{end}.pdf", "application/pdf")
            
            elif split_mode == "Individual Pages":
                page_num = st.number_input("Page Number", 1, total_pages, 1)
                
                if st.button("Extract Page"):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[page_num-1])
                    
                    output = io.BytesIO()
                    writer.write(output)
                    output.seek(0)
                    
                    st.download_button("Download", output, f"page_{page_num}.pdf", "application/pdf")
            
            else:  # Every N Pages
                n = st.number_input("Split Every N Pages", 1, total_pages, 5)
                
                if st.button("Split PDF"):
                    for i in range(0, total_pages, n):
                        writer = PdfWriter()
                        for j in range(i, min(i+n, total_pages)):
                            writer.add_page(reader.pages[j])
                        
                        output = io.BytesIO()
                        writer.write(output)
                        output.seek(0)
                        
                        st.download_button(f"Download Part {i//n + 1}", output, 
                                         f"split_part_{i//n + 1}.pdf", "application/pdf")
    
    # Compress PDF
    with tabs[2]:
        st.markdown("### 📦 Compress PDF")
        uploaded = st.file_uploader("Upload PDF", type=['pdf'], key="compress")
        
        if uploaded:
            original_size = len(uploaded.getvalue())
            st.metric("Original Size", f"{original_size/1024:.2f} KB")
            
            if st.button("Compress PDF"):
                reader = PdfReader(uploaded)
                writer = PdfWriter()
                
                for page in reader.pages:
                    page.compress_content_streams()
                    writer.add_page(page)
                
                output = io.BytesIO()
                writer.write(output)
                output.seek(0)
                
                compressed_size = len(output.getvalue())
                reduction = ((original_size - compressed_size) / original_size) * 100
                
                st.success(f"✅ Compressed by {reduction:.1f}%")
                st.metric("Compressed Size", f"{compressed_size/1024:.2f} KB")
                
                st.download_button("Download Compressed", output, "compressed.pdf", "application/pdf")
    
    # PDF to Images
    with tabs[3]:
        st.markdown("### 🖼️ PDF to Images")
        uploaded = st.file_uploader("Upload PDF", type=['pdf'], key="pdf2img")
        
        if uploaded:
            st.info("Note: This feature requires pdf2image library with poppler")
            st.warning("Converting pages to images using PyMuPDF alternative...")
            
            if st.button("Convert to Images"):
                try:
                    import fitz  # PyMuPDF
                    doc = fitz.open(stream=uploaded.read(), filetype="pdf")
                    
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        pix = page.get_pixmap(dpi=200)
                        img_data = pix.tobytes("png")
                        
                        st.image(img_data, caption=f"Page {page_num + 1}")
                        st.download_button(f"Download Page {page_num + 1}", 
                                         img_data, f"page_{page_num + 1}.png", "image/png")
                except:
                    st.error("PyMuPDF not available. Please install: pip install PyMuPDF")
    
    # Images to PDF
    with tabs[4]:
        st.markdown("### 📄 Images to PDF")
        uploaded_files = st.file_uploader("Upload Images", type=['png', 'jpg', 'jpeg'], 
                                         accept_multiple_files=True, key="img2pdf")
        
        if uploaded_files:
            st.success(f"📁 {len(uploaded_files)} images uploaded")
            
            for img in uploaded_files:
                st.image(img, width=150)
            
            if st.button("Create PDF"):
                images = []
                for file in uploaded_files:
                    img = Image.open(file)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    images.append(img)
                
                output = io.BytesIO()
                images[0].save(output, format='PDF', save_all=True, append_images=images[1:])
                output.seek(0)
                
                st.success("✅ PDF created successfully!")
                st.download_button("Download PDF", output, "images.pdf", "application/pdf")
    
    # Extract Text
    with tabs[5]:
        st.markdown("### 📝 Extract Text from PDF")
        uploaded = st.file_uploader("Upload PDF", type=['pdf'], key="extract")
        
        if uploaded:
            reader = PdfReader(uploaded)
            
            st.info(f"📄 Total Pages: {len(reader.pages)}")
            
            extract_all = st.checkbox("Extract from all pages", True)
            
            if extract_all:
                if st.button("Extract Text"):
                    full_text = ""
                    for page in reader.pages:
                        full_text += page.extract_text() + "\n\n"
                    
                    st.text_area("Extracted Text", full_text, height=300)
                    st.download_button("Download Text", full_text, "extracted.txt", "text/plain")
            else:
                page_num = st.number_input("Page Number", 1, len(reader.pages), 1)
                if st.button("Extract Text"):
                    text = reader.pages[page_num-1].extract_text()
                    st.text_area("Extracted Text", text, height=300)
    
    # Rotate Pages
    with tabs[6]:
        st.markdown("### 🔄 Rotate PDF Pages")
        uploaded = st.file_uploader("Upload PDF", type=['pdf'], key="rotate")
        
        if uploaded:
            reader = PdfReader(uploaded)
            st.info(f"📄 Total Pages: {len(reader.pages)}")
            
            rotation = st.selectbox("Rotation", [90, 180, 270])
            rotate_all = st.checkbox("Rotate all pages", True)
            
            if not rotate_all:
                page_num = st.number_input("Page Number", 1, len(reader.pages), 1)
            
            if st.button("Rotate PDF"):
                writer = PdfWriter()
                
                for i, page in enumerate(reader.pages):
                    if rotate_all or (i == page_num - 1):
                        page.rotate(rotation)
                    writer.add_page(page)
                
                output = io.BytesIO()
                writer.write(output)
                output.seek(0)
                
                st.success("✅ PDF rotated successfully!")
                st.download_button("Download Rotated PDF", output, "rotated.pdf", "application/pdf")
    
    # Watermark
    with tabs[7]:
        st.markdown("### 💧 Add Watermark to PDF")
        
        col1, col2 = st.columns(2)
        with col1:
            pdf_file = st.file_uploader("Upload PDF", type=['pdf'], key="watermark_pdf")
        with col2:
            watermark_text = st.text_input("Watermark Text", "CONFIDENTIAL")
        
        if pdf_file:
            if st.button("Add Watermark"):
                # Create watermark
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=letter)
                can.setFont("Helvetica", 40)
                can.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.3)
                can.saveState()
                can.translate(300, 400)
                can.rotate(45)
                can.drawCentredString(0, 0, watermark_text)
                can.restoreState()
                can.save()
                packet.seek(0)
                
                watermark_pdf = PdfReader(packet)
                reader = PdfReader(pdf_file)
                writer = PdfWriter()
                
                for page in reader.pages:
                    page.merge_page(watermark_pdf.pages[0])
                    writer.add_page(page)
                
                output = io.BytesIO()
                writer.write(output)
                output.seek(0)
                
                st.success("✅ Watermark added!")
                st.download_button("Download", output, "watermarked.pdf", "application/pdf")
    
    # Password Protect
    with tabs[8]:
        st.markdown("### 🔐 Password Protect PDF")
        uploaded = st.file_uploader("Upload PDF", type=['pdf'], key="password")
        
        if uploaded:
            password = st.text_input("Set Password", type="password")
            
            if password and st.button("Protect PDF"):
                reader = PdfReader(uploaded)
                writer = PdfWriter()
                
                for page in reader.pages:
                    writer.add_page(page)
                
                writer.encrypt(password)
                
                output = io.BytesIO()
                writer.write(output)
                output.seek(0)
                
                st.success("✅ PDF protected!")
                st.download_button("Download Protected PDF", output, "protected.pdf", "application/pdf")
    
    # Metadata Viewer
    with tabs[9]:
        st.markdown("### 📋 PDF Metadata Viewer")
        uploaded = st.file_uploader("Upload PDF", type=['pdf'], key="metadata")
        
        if uploaded:
            reader = PdfReader(uploaded)
            
            st.markdown("#### 📊 Document Info")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Pages", len(reader.pages))
            with col2:
                st.metric("Size", f"{len(uploaded.getvalue())/1024:.2f} KB")
            
            st.markdown("#### 🏷️ Metadata")
            metadata = reader.metadata
            if metadata:
                for key, value in metadata.items():
                    st.text(f"{key}: {value}")
            else:
                st.warning("No metadata found")
