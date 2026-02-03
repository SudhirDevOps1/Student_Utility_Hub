import streamlit as st
import datetime
from io import BytesIO

def show():
    st.markdown("## 🎨 Creative Tools")
    
    tabs = st.tabs(["Mind Map Creator", "Presentation Timer", "Essay Word Counter", "Code Snippet Manager"])
    
    # Mind Map Creator
    with tabs[0]:
        st.markdown("### 🧠 Mind Map Creator")
        
        st.info("Create simple text-based mind maps for brainstorming!")
        
        if 'mindmap' not in st.session_state:
            st.session_state.mindmap = {"Main Topic": []}
        
        main_topic = st.text_input("Main Topic", "My Project")
        
        st.markdown("#### Add Branches")
        new_branch = st.text_input("New Branch/Idea")
        
        if st.button("➕ Add Branch"):
            if new_branch:
                if main_topic not in st.session_state.mindmap:
                    st.session_state.mindmap[main_topic] = []
                st.session_state.mindmap[main_topic].append(new_branch)
                st.success("Branch added!")
                st.rerun()
        
        if main_topic in st.session_state.mindmap and st.session_state.mindmap[main_topic]:
            st.markdown("---")
            st.markdown(f"### 🌳 Mind Map: {main_topic}")
            
            st.markdown(f"**🎯 {main_topic}**")
            for idx, branch in enumerate(st.session_state.mindmap[main_topic]):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"  ├─ {branch}")
                with col2:
                    if st.button("🗑️", key=f"del_branch_{idx}"):
                        st.session_state.mindmap[main_topic].pop(idx)
                        st.rerun()
            
            # Export as text
            mindmap_text = f"{main_topic}\n"
            for branch in st.session_state.mindmap[main_topic]:
                mindmap_text += f"  ├─ {branch}\n"
            
            st.download_button("📥 Export Mind Map", mindmap_text, "mindmap.txt", "text/plain")
    
    # Presentation Timer
    with tabs[1]:
        st.markdown("### ⏱️ Presentation Timer")
        
        st.info("Practice your presentations with timed sections!")
        
        presentation_duration = st.number_input("Total Duration (minutes)", 1, 120, 10)
        
        if 'pres_sections' not in st.session_state:
            st.session_state.pres_sections = []
        
        col1, col2 = st.columns(2)
        with col1:
            section_name = st.text_input("Section Name", key="pres_section")
        with col2:
            section_duration = st.number_input("Duration (min)", 1, 30, 2, key="pres_duration")
        
        if st.button("➕ Add Section"):
            if section_name:
                st.session_state.pres_sections.append({
                    "name": section_name,
                    "duration": section_duration
                })
                st.success("Section added!")
                st.rerun()
        
        if st.session_state.pres_sections:
            st.markdown("### 📋 Presentation Outline")
            
            total_time = 0
            for idx, section in enumerate(st.session_state.pres_sections):
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.write(f"**{section['name']}**")
                with col_b:
                    st.write(f"{section['duration']} min")
                with col_c:
                    if st.button("🗑️", key=f"del_pres_{idx}"):
                        st.session_state.pres_sections.pop(idx)
                        st.rerun()
                
                total_time += section['duration']
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Time", f"{total_time} min")
            with col2:
                if total_time > presentation_duration:
                    st.error(f"⚠️ Over by {total_time - presentation_duration} min")
                elif total_time < presentation_duration:
                    st.info(f"📌 {presentation_duration - total_time} min remaining")
                else:
                    st.success("✅ Perfect timing!")
            
            if st.button("🎤 Start Presentation", type="primary"):
                st.balloons()
                st.success("Good luck with your presentation!")
    
    # Essay Word Counter
    with tabs[2]:
        st.markdown("### 📝 Essay Word Counter & Analyzer")
        
        essay_text = st.text_area("Paste your essay here...", height=300,
                                  placeholder="Type or paste your essay here for detailed analysis...")
        
        if essay_text:
            words = essay_text.split()
            word_count = len(words)
            char_count = len(essay_text)
            char_no_spaces = len(essay_text.replace(" ", ""))
            sentences = essay_text.split('.')
            sentence_count = len([s for s in sentences if s.strip()])
            paragraphs = essay_text.split('\n\n')
            paragraph_count = len([p for p in paragraphs if p.strip()])
            
            st.markdown("### 📊 Analysis Results")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Words", word_count)
            with col2:
                st.metric("Characters", char_count)
            with col3:
                st.metric("Sentences", sentence_count)
            with col4:
                st.metric("Paragraphs", paragraph_count)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Avg Words/Sentence", f"{word_count/sentence_count if sentence_count > 0 else 0:.1f}")
            with col_b:
                reading_time = word_count / 200  # Average reading speed
                st.metric("Reading Time", f"{reading_time:.1f} min")
            with col_c:
                speaking_time = word_count / 130  # Average speaking speed
                st.metric("Speaking Time", f"{speaking_time:.1f} min")
            
            # Target word count
            st.markdown("---")
            st.markdown("### 🎯 Target Word Count")
            target = st.number_input("Target Words", 100, 10000, 500)
            
            progress = min(word_count / target, 1.0)
            st.progress(progress)
            
            if word_count < target:
                st.info(f"📝 {target - word_count} more words needed")
            elif word_count > target:
                st.warning(f"✂️ {word_count - target} words over limit")
            else:
                st.success("✅ Perfect word count!")
            
            # Most common words
            st.markdown("### 🔤 Most Common Words")
            word_freq = {}
            for word in words:
                clean_word = word.lower().strip('.,!?;:')
                if len(clean_word) > 3:  # Ignore short words
                    word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
            
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            for word, count in top_words:
                st.write(f"**{word}:** {count} times")
    
    # Code Snippet Manager
    with tabs[3]:
        st.markdown("### 💻 Code Snippet Manager")
        
        if 'snippets' not in st.session_state:
            st.session_state.snippets = []
        
        st.markdown("#### Save New Snippet")
        
        col1, col2 = st.columns(2)
        with col1:
            snippet_name = st.text_input("Snippet Name", key="snippet_name")
        with col2:
            language = st.selectbox("Language", 
                                   ["Python", "JavaScript", "Java", "C++", "HTML", "CSS", "SQL", "Other"],
                                   key="snippet_lang")
        
        code = st.text_area("Code", height=200, key="snippet_code")
        description = st.text_input("Description (optional)", key="snippet_desc")
        tags = st.text_input("Tags (comma separated)", key="snippet_tags")
        
        if st.button("💾 Save Snippet"):
            if snippet_name and code:
                st.session_state.snippets.append({
                    "name": snippet_name,
                    "language": language,
                    "code": code,
                    "description": description,
                    "tags": tags,
                    "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("Snippet saved!")
                st.rerun()
        
        if st.session_state.snippets:
            st.markdown("---")
            st.markdown(f"### 💾 Saved Snippets ({len(st.session_state.snippets)})")
            
            # Filter
            search = st.text_input("🔍 Search snippets", key="snippet_search")
            
            for idx, snippet in enumerate(st.session_state.snippets):
                if search and search.lower() not in snippet['name'].lower():
                    continue
                
                with st.expander(f"💻 {snippet['language']} - {snippet['name']}"):
                    if snippet['description']:
                        st.write(f"**Description:** {snippet['description']}")
                    if snippet['tags']:
                        st.write(f"**Tags:** {snippet['tags']}")
                    st.write(f"**Created:** {snippet['created']}")
                    
                    st.code(snippet['code'], language=snippet['language'].lower())
                    
                    col_x, col_y = st.columns(2)
                    with col_x:
                        st.download_button("📥 Download", snippet['code'], 
                                         f"{snippet['name']}.txt", key=f"dl_snippet_{idx}")
                    with col_y:
                        if st.button("🗑️ Delete", key=f"del_snippet_{idx}"):
                            st.session_state.snippets.pop(idx)
                            st.rerun()
