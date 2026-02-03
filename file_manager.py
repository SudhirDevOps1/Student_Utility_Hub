import streamlit as st
import os
import psutil
from pathlib import Path
import datetime

def get_available_drives():
    drives = []
    for partition in psutil.disk_partitions():
        drives.append(partition.device)
    return drives

def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0

def search_files(drive, filename="", extension="", file_type="All"):
    results = []
    search_path = Path(drive)
    
    try:
        if extension:
            pattern = f"**/*.{extension}"
        elif filename:
            pattern = f"**/*{filename}*"
        else:
            pattern = "**/*"
        
        count = 0
        for file_path in search_path.glob(pattern):
            if count >= 100:
                break
            
            try:
                if file_path.is_file():
                    if file_type != "All":
                        ext = file_path.suffix.lower()
                        if file_type == "Images" and ext not in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                            continue
                        elif file_type == "Videos" and ext not in ['.mp4', '.avi', '.mkv', '.mov']:
                            continue
                        elif file_type == "PDFs" and ext != '.pdf':
                            continue
                        elif file_type == "Docs" and ext not in ['.doc', '.docx', '.txt']:
                            continue
                    
                    stat = file_path.stat()
                    results.append({
                        "Name": file_path.name,
                        "Path": str(file_path),
                        "Size": format_size(stat.st_size),
                        "Modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                        "Type": file_path.suffix
                    })
                    count += 1
            except (PermissionError, OSError):
                continue
                
    except Exception as e:
        st.error(f"Search error: {str(e)}")
    
    return results

def show():
    st.markdown("## 📂 File Manager & Search")
    
    st.info("🔍 Search files across your system drives (Read-only mode)")
    
    drives = get_available_drives()
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_drive = st.selectbox("Select Drive", drives)
    
    with col2:
        search_term = st.text_input("🔎 Search filename", placeholder="Enter filename or keyword")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        extension = st.text_input("Extension (without dot)", placeholder="e.g., pdf, docx")
    
    with col_b:
        file_type = st.selectbox("File Type", ["All", "Images", "Videos", "PDFs", "Docs"])
    
    with col_c:
        st.write("")
        st.write("")
        search_button = st.button("🔍 Search Files", type="primary")
    
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    if search_button:
        if search_term or extension:
            with st.spinner("Searching files..."):
                results = search_files(selected_drive, search_term, extension, file_type)
                
                if results:
                    st.success(f"✅ Found {len(results)} files (showing max 100)")
                    
                    st.session_state.search_history.insert(0, {
                        "term": search_term or extension,
                        "count": len(results)
                    })
                    st.session_state.search_history = st.session_state.search_history[:5]
                    
                    for idx, file_info in enumerate(results):
                        with st.expander(f"📄 {file_info['Name']}"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.text(f"📁 Path: {file_info['Path']}")
                                st.text(f"📊 Size: {file_info['Size']}")
                                st.text(f"📅 Modified: {file_info['Modified']}")
                                st.text(f"🏷️ Type: {file_info['Type']}")
                            
                            with col2:
                                if st.button("📋 Copy Path", key=f"copy_{idx}"):
                                    st.code(file_info['Path'])
                                
                                if st.button("📂 Open Folder", key=f"open_{idx}"):
                                    folder_path = os.path.dirname(file_info['Path'])
                                    st.code(f"explorer {folder_path}")
                                    st.info("Run this command in terminal")
                                
                                if file_info['Type'].lower() in ['.png', '.jpg', '.jpeg', '.gif']:
                                    if st.button("👁️ Preview", key=f"preview_{idx}"):
                                        try:
                                            st.image(file_info['Path'], width=300)
                                        except:
                                            st.error("Cannot preview")
                else:
                    st.warning("No files found matching your criteria")
        else:
            st.warning("Please enter a search term or extension")
    
    if st.session_state.search_history:
        st.markdown("### 🕒 Recent Searches")
        for item in st.session_state.search_history:
            st.text(f"• {item['term']} - {item['count']} results")
    
    st.markdown("---")
    st.markdown("### 💾 Drive Information")
    
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Drive", partition.device)
            with col2:
                st.metric("Total", format_size(usage.total))
            with col3:
                st.metric("Used", format_size(usage.used))
            with col4:
                st.metric("Free", format_size(usage.free))
            
            st.progress(usage.percent / 100)
            st.markdown("---")
        except:
            continue
