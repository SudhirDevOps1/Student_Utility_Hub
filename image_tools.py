import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ExifTags
import io
import cv2
import numpy as np

# ---------------- OPTIONAL BACKGROUND REMOVAL ----------------
try:
    from rembg import remove
    REMBG_AVAILABLE = True
except Exception:
    remove = None
    REMBG_AVAILABLE = False


# ---------------- JPEG SAFE SAVE ----------------
def save_as_jpeg(image, buffer, quality):
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(buffer, format="JPEG", quality=quality, optimize=True)


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

    # ================= BACKGROUND REMOVER =================
    with tabs[0]:
        st.markdown("### 🎭 Background Remover")
        uploaded = st.file_uploader("Upload Image", ["png", "jpg", "jpeg"])

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Original", use_container_width=True)

            if not REMBG_AVAILABLE:
                st.warning("Background remover not available on cloud.")
            else:
                if st.button("Remove Background"):
                    with st.spinner("Processing..."):
                        output = remove(image)
                        st.image(output, caption="Result", use_container_width=True)

                        buf = io.BytesIO()
                        output.save(buf, format="PNG")
                        st.download_button(
                            "Download PNG",
                            buf.getvalue(),
                            "no_bg.png",
                            "image/png"
                        )

    # ================= RESIZE & COMPRESS =================
    with tabs[1]:
        st.markdown("### 📏 Resize & Compress")
        uploaded = st.file_uploader("Upload Image", ["png", "jpg", "jpeg"], key="resize")

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Original", use_container_width=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                width = st.number_input("Width", 1, 5000, image.width)
            with col2:
                height = st.number_input("Height", 1, 5000, image.height)
            with col3:
                quality = st.slider("Quality", 1, 100, 85)

            if st.button("Process Image"):
                resized = image.resize((width, height), Image.Resampling.LANCZOS)

                buf = io.BytesIO()
                save_as_jpeg(resized, buf, quality)
                buf.seek(0)

                st.image(resized, caption=f"{width}×{height}", use_container_width=True)
                st.download_button(
                    "Download",
                    buf.getvalue(),
                    "resized.jpg",
                    "image/jpeg"
                )

    # ================= FILTERS & EFFECTS =================
    with tabs[2]:
        st.markdown("### 🎨 Filters & Effects")
        uploaded = st.file_uploader("Upload Image", ["png", "jpg", "jpeg"], key="filters")

        if uploaded:
            image = Image.open(uploaded)
            filter_type = st.selectbox(
                "Select Filter",
                ["None", "Blur", "Sharpen", "Black & White", "Sepia",
                 "Edge Detect", "Emboss", "Vintage"]
            )

            result = image.copy()

            if filter_type == "Blur":
                result = result.filter(ImageFilter.GaussianBlur(3))
            elif filter_type == "Sharpen":
                result = result.filter(ImageFilter.SHARPEN)
            elif filter_type == "Black & White":
                result = result.convert("L")
            elif filter_type == "Sepia":
                arr = np.array(result.convert("RGB"))
                tr = arr[:,:,0]*0.393 + arr[:,:,1]*0.769 + arr[:,:,2]*0.189
                tg = arr[:,:,0]*0.349 + arr[:,:,1]*0.686 + arr[:,:,2]*0.168
                tb = arr[:,:,0]*0.272 + arr[:,:,1]*0.534 + arr[:,:,2]*0.131
                arr[:,:,0] = np.clip(tr,0,255)
                arr[:,:,1] = np.clip(tg,0,255)
                arr[:,:,2] = np.clip(tb,0,255)
                result = Image.fromarray(arr.astype("uint8"))
            elif filter_type == "Edge Detect":
                result = result.filter(ImageFilter.FIND_EDGES)
            elif filter_type == "Emboss":
                result = result.filter(ImageFilter.EMBOSS)
            elif filter_type == "Vintage":
                result = ImageEnhance.Color(result).enhance(0.5)
                result = ImageEnhance.Brightness(result).enhance(0.8)

            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Original", use_container_width=True)
            with col2:
                st.image(result, caption="Filtered", use_container_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button(
                "Download Result",
                buf.getvalue(),
                "filtered.png",
                "image/png"
            )

    # ================= BATCH COMPRESSION =================
    with tabs[3]:
        st.markdown("### 📦 Batch Image Compression")
        files = st.file_uploader(
            "Upload Images",
            ["png", "jpg", "jpeg"],
            accept_multiple_files=True
        )

        if files:
            quality = st.slider("Quality", 1, 100, 75)

            if st.button("Compress All"):
                progress = st.progress(0)

                for i, file in enumerate(files):
                    img = Image.open(file)
                    buf = io.BytesIO()
                    save_as_jpeg(img, buf, quality)
                    buf.seek(0)

                    st.download_button(
                        f"Download {file.name}",
                        buf.getvalue(),
                        f"compressed_{file.name}",
                        "image/jpeg"
                    )

                    progress.progress((i + 1) / len(files))

    # ================= METADATA VIEWER =================
    with tabs[4]:
        st.markdown("### 📋 Image Metadata Viewer")
        uploaded = st.file_uploader("Upload Image", ["png", "jpg", "jpeg"], key="meta")

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True)

            try:
                exif = image._getexif()
                if exif:
                    for k, v in exif.items():
                        tag = ExifTags.TAGS.get(k, k)
                        st.text(f"{tag}: {v}")
                else:
                    st.info("No EXIF data")
            except Exception:
                st.warning("Cannot read metadata")

    # ================= SCREENSHOT CROP =================
    with tabs[5]:
        st.markdown("### ✂️ Screenshot Crop")
        uploaded = st.file_uploader("Upload Screenshot", ["png", "jpg", "jpeg"], key="crop")

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True)

            left = st.number_input("Left", 0, image.width, 0)
            top = st.number_input("Top", 0, image.height, 0)
            right = st.number_input("Right", 0, image.width, image.width)
            bottom = st.number_input("Bottom", 0, image.height, image.height)

            if st.button("Crop"):
                cropped = image.crop((left, top, right, bottom))
                st.image(cropped, use_container_width=True)

                buf = io.BytesIO()
                cropped.save(buf, format="PNG")
                st.download_button(
                    "Download Cropped",
                    buf.getvalue(),
                    "cropped.png",
                    "image/png"
                )

    # ================= AI UPSCALER =================
    with tabs[6]:
        st.markdown("### 🚀 AI Upscaler")
        uploaded = st.file_uploader("Upload Image", ["png", "jpg", "jpeg"], key="up")

        if uploaded:
            image = Image.open(uploaded)
            scale = st.slider("Scale Factor", 2, 4, 2)

            if st.button("Upscale"):
                arr = np.array(image)
                up = cv2.resize(
                    arr,
                    (image.width * scale, image.height * scale),
                    interpolation=cv2.INTER_CUBIC
                )
                result = Image.fromarray(up)
                st.image(result, use_container_width=True)

                buf = io.BytesIO()
                result.save(buf, format="PNG")
                st.download_button(
                    "Download Upscaled",
                    buf.getvalue(),
                    "upscaled.png",
                    "image/png"
                )
