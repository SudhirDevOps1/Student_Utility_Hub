import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ExifTags
import io
import cv2
import numpy as np


def show():
    st.markdown("## 🖼 Image Tools")
    
    tabs = st.tabs([
        "Background Remover",
        "Resize & Compress",
        "Filters & Effects", 
        "Batch Compression",
        "Metadata Viewer",
        "Screenshot Crop",
        "AI Upscaler"
    ])
    
    # Background Remover
    with tabs[0]:
        st.markdown("### 🎭 Background Remover")
        uploaded = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="bg_remove")
        
        if uploaded:
            image = Image.open(uploaded)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original**")
                st.image(image, use_container_width=True)
            
            with col2:
                if st.button("Remove Background"):
                    with st.spinner("Processing..."):
                        output = remove(image)
                        st.markdown("**Result**")
                        st.image(output, use_container_width=True)
                        
                        buf = io.BytesIO()
                        output.save(buf, format='PNG')
                        st.download_button("Download PNG", buf.getvalue(), "no_bg.png", "image/png")
    
    # Resize & Compress
    with tabs[1]:
        st.markdown("### 📏 Resize & Compress")
        uploaded = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="resize")
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Original", use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                width = st.number_input("Width (px)", 1, 5000, image.width)
            with col2:
                height = st.number_input("Height (px)", 1, 5000, image.height)
            with col3:
                quality = st.slider("Quality", 1, 100, 85)
            
            maintain_ratio = st.checkbox("Maintain Aspect Ratio", True)
            
            if st.button("Process Image"):
                if maintain_ratio:
                    ratio = image.width / image.height
                    if width != image.width:
                        height = int(width / ratio)
                    else:
                        width = int(height * ratio)
                
                resized = image.resize((width, height), Image.Resampling.LANCZOS)
                
                buf = io.BytesIO()
                resized.save(buf, format='JPEG', quality=quality, optimize=True)
                buf.seek(0)
                
                st.image(resized, caption=f"Resized: {width}x{height}", use_container_width=True)
                st.info(f"Original: {len(uploaded.getvalue())/1024:.2f} KB → New: {len(buf.getvalue())/1024:.2f} KB")
                st.download_button("Download", buf.getvalue(), "resized.jpg", "image/jpeg")
    
    # Filters & Effects
    with tabs[2]:
        st.markdown("### 🎨 Filters & Effects")
        uploaded = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="filters")
        
        if uploaded:
            image = Image.open(uploaded)
            
            filter_type = st.selectbox("Select Filter", [
                "None", "Blur", "Sharpen", "Black & White", 
                "Sepia", "Edge Detect", "Emboss", "Vintage"
            ])
            
            result = image.copy()
            
            if filter_type == "Blur":
                amount = st.slider("Blur Amount", 0, 10, 3)
                result = result.filter(ImageFilter.GaussianBlur(amount))
            elif filter_type == "Sharpen":
                result = result.filter(ImageFilter.SHARPEN)
            elif filter_type == "Black & White":
                result = result.convert('L')
            elif filter_type == "Sepia":
                result = result.convert('RGB')
                pixels = np.array(result)
                tr = pixels[:,:,0] * 0.393 + pixels[:,:,1] * 0.769 + pixels[:,:,2] * 0.189
                tg = pixels[:,:,0] * 0.349 + pixels[:,:,1] * 0.686 + pixels[:,:,2] * 0.168
                tb = pixels[:,:,0] * 0.272 + pixels[:,:,1] * 0.534 + pixels[:,:,2] * 0.131
                pixels[:,:,0] = np.clip(tr, 0, 255)
                pixels[:,:,1] = np.clip(tg, 0, 255)
                pixels[:,:,2] = np.clip(tb, 0, 255)
                result = Image.fromarray(pixels.astype('uint8'))
            elif filter_type == "Edge Detect":
                result = result.filter(ImageFilter.FIND_EDGES)
            elif filter_type == "Emboss":
                result = result.filter(ImageFilter.EMBOSS)
            elif filter_type == "Vintage":
                enhancer = ImageEnhance.Color(result)
                result = enhancer.enhance(0.5)
                enhancer2 = ImageEnhance.Brightness(result)
                result = enhancer2.enhance(0.8)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original**")
                st.image(image, use_container_width=True)
            with col2:
                st.markdown("**Filtered**")
                st.image(result, use_container_width=True)
            
            buf = io.BytesIO()
            result.save(buf, format='PNG')
            st.download_button("Download Result", buf.getvalue(), "filtered.png", "image/png")
    
    # Batch Compression
    with tabs[3]:
        st.markdown("### 📦 Batch Image Compression")
        uploaded_files = st.file_uploader("Upload Images", type=['png', 'jpg', 'jpeg'], 
                                         accept_multiple_files=True, key="batch")
        
        if uploaded_files:
            st.info(f"📁 {len(uploaded_files)} images uploaded")
            
            col1, col2 = st.columns(2)
            with col1:
                quality = st.slider("Quality", 1, 100, 75)
            with col2:
                target_size = st.selectbox("Target Size", 
                    ["Original", "2KB", "10KB", "20KB", "50KB", "100KB", "200KB", "500KB"])
            
            if st.button("Compress All"):
                compressed_files = []
                progress = st.progress(0)
                
                for idx, file in enumerate(uploaded_files):
                    img = Image.open(file)
                    
                    buf = io.BytesIO()
                    temp_quality = quality
                    
                    if target_size != "Original":
                        target_bytes = int(target_size.replace("KB", "")) * 1024
                        
                        # Iterative compression
                        for q in range(quality, 5, -5):
                            buf = io.BytesIO()
                            img.save(buf, format='JPEG', quality=q, optimize=True)
                            if len(buf.getvalue()) <= target_bytes:
                                break
                    else:
                        img.save(buf, format='JPEG', quality=quality, optimize=True)
                    
                    buf.seek(0)
                    compressed_files.append((file.name, buf.getvalue()))
                    progress.progress((idx + 1) / len(uploaded_files))
                
                st.success(f"✅ Compressed {len(compressed_files)} images!")
                
                for name, data in compressed_files:
                    st.download_button(f"📥 {name}", data, f"compressed_{name}", "image/jpeg")
    
    # Metadata Viewer
    with tabs[4]:
        st.markdown("### 📋 Image Metadata Viewer")
        uploaded = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="metadata")
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Image", use_container_width=True)
            
            st.markdown("#### 📊 Basic Info")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Width", f"{image.width}px")
            with col2:
                st.metric("Height", f"{image.height}px")
            with col3:
                st.metric("Format", image.format)
            
            st.markdown("#### 🏷️ EXIF Data")
            try:
                exif = image._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag = ExifTags.TAGS.get(tag_id, tag_id)
                        st.text(f"{tag}: {value}")
                else:
                    st.warning("No EXIF data found")
            except:
                st.warning("Unable to read EXIF data")
            
            if st.button("Remove Metadata"):
                clean_img = Image.new(image.mode, image.size)
                clean_img.putdata(list(image.getdata()))
                
                buf = io.BytesIO()
                clean_img.save(buf, format='PNG')
                st.download_button("Download Clean Image", buf.getvalue(), "clean.png", "image/png")
    
    # Screenshot Crop
    with tabs[5]:
        st.markdown("### ✂️ Screenshot Crop Tool")
        uploaded = st.file_uploader("Upload Screenshot", type=['png', 'jpg', 'jpeg'], key="crop")
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Original", use_container_width=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                left = st.number_input("Left", 0, image.width, 0)
            with col2:
                top = st.number_input("Top", 0, image.height, 0)
            with col3:
                right = st.number_input("Right", 0, image.width, image.width)
            with col4:
                bottom = st.number_input("Bottom", 0, image.height, image.height)
            
            if st.button("Crop Image"):
                cropped = image.crop((left, top, right, bottom))
                st.image(cropped, caption="Cropped", use_container_width=True)
                
                buf = io.BytesIO()
                cropped.save(buf, format='PNG')
                st.download_button("Download Cropped", buf.getvalue(), "cropped.png", "image/png")
    
    # AI Upscaler
    with tabs[6]:
        st.markdown("### 🚀 AI Upscaler")
        uploaded = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="upscale")
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption=f"Original: {image.width}x{image.height}", use_container_width=True)
            
            scale_factor = st.slider("Upscale Factor", 2, 4, 2)
            
            if st.button("Upscale Image"):
                with st.spinner("Upscaling..."):
                    # Convert to numpy array
                    img_array = np.array(image)
                    
                    # Use OpenCV super resolution (simple bicubic for speed)
                    new_width = image.width * scale_factor
                    new_height = image.height * scale_factor
                    
                    upscaled = cv2.resize(img_array, (new_width, new_height), 
                                        interpolation=cv2.INTER_CUBIC)
                    
                    # Sharpen
                    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                    upscaled = cv2.filter2D(upscaled, -1, kernel)
                    
                    result = Image.fromarray(upscaled)
                    
                    st.image(result, caption=f"Upscaled: {new_width}x{new_height}", 
                           use_container_width=True)
                    
                    buf = io.BytesIO()
                    result.save(buf, format='PNG')
                    st.download_button("Download Upscaled", buf.getvalue(), "upscaled.png", "image/png")

