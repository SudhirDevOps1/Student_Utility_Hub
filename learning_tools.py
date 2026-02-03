import streamlit as st
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import random
import json_utils

def show():
    st.markdown("## 📚 Learning & Academic Tools")
    
    tabs = st.tabs(["Flashcard Maker", "Assignment Tracker", "Lecture Notes", "Citation Generator", "Formula Sheet"])
    
    # Flashcard Maker
    with tabs[0]:
        st.markdown("### 🃏 Flashcard Maker")
        
        if 'flashcards' not in st.session_state:
            st.session_state.flashcards = []
        if 'study_mode' not in st.session_state:
            st.session_state.study_mode = False
        if 'current_card' not in st.session_state:
            st.session_state.current_card = 0
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False
        
        if not st.session_state.study_mode:
            st.markdown("#### Create Flashcards")
            
            col1, col2 = st.columns(2)
            with col1:
                question = st.text_area("Question/Front", height=100, key="fc_question")
            with col2:
                answer = st.text_area("Answer/Back", height=100, key="fc_answer")
            
            category = st.selectbox("Category", ["General", "Math", "Science", "History", "Language", "Other"])
            
            if st.button("➕ Add Flashcard"):
                if question and answer:
                    st.session_state.flashcards.append({
                        "question": question,
                        "answer": answer,
                        "category": category,
                        "created": datetime.datetime.now().strftime("%Y-%m-%d")
                    })
                    st.success("Flashcard added!")
                    st.rerun()
            
            if st.session_state.flashcards:
                st.markdown(f"### 📚 Your Flashcards ({len(st.session_state.flashcards)})")
                
                for idx, card in enumerate(st.session_state.flashcards):
                    with st.expander(f"🃏 {card['category']} - {card['question'][:50]}..."):
                        st.markdown(f"**Q:** {card['question']}")
                        st.markdown(f"**A:** {card['answer']}")
                        st.text(f"Created: {card['created']}")
                        
                        if st.button("🗑️ Delete", key=f"del_fc_{idx}"):
                            st.session_state.flashcards.pop(idx)
                            st.rerun()
                
                if st.button("🎓 Start Study Mode", type="primary"):
                    random.shuffle(st.session_state.flashcards)
                    st.session_state.study_mode = True
                    st.session_state.current_card = 0
                    st.session_state.show_answer = False
                    st.rerun()
        else:
            # Study Mode
            if st.session_state.flashcards:
                card = st.session_state.flashcards[st.session_state.current_card]
                
                st.markdown(f"### Card {st.session_state.current_card + 1} of {len(st.session_state.flashcards)}")
                st.progress((st.session_state.current_card + 1) / len(st.session_state.flashcards))
                
                st.markdown(f"**Category:** {card['category']}")
                
                if not st.session_state.show_answer:
                    st.markdown("### 🃏 Question:")
                    st.info(card['question'])
                    
                    if st.button("🔍 Show Answer", type="primary"):
                        st.session_state.show_answer = True
                        st.rerun()
                else:
                    st.markdown("### 🃏 Question:")
                    st.info(card['question'])
                    st.markdown("### ✅ Answer:")
                    st.success(card['answer'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("← Previous"):
                            if st.session_state.current_card > 0:
                                st.session_state.current_card -= 1
                                st.session_state.show_answer = False
                                st.rerun()
                    with col2:
                        if st.button("Next →"):
                            if st.session_state.current_card < len(st.session_state.flashcards) - 1:
                                st.session_state.current_card += 1
                                st.session_state.show_answer = False
                                st.rerun()
                    with col3:
                        if st.button("Exit Study Mode"):
                            st.session_state.study_mode = False
                            st.rerun()
    
    # Assignment Tracker
    with tabs[1]:
        st.markdown("### 📝 Assignment Tracker")
        
        if 'assignments' not in st.session_state:
            st.session_state.assignments = []
        
        # Load categories from JSON
        settings_data = json_utils.load_json_data('custom_settings.json')
        assignment_cats = settings_data.get('assignment_categories', ["Homework", "Project", "Essay"])
        priority_levels = settings_data.get('priority_levels', ["🔴 High", "🟡 Medium", "🟢 Low"])
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            assignment_name = st.text_input("Assignment Name", key="assign_name")
        with col2:
            subject = st.text_input("Subject", key="assign_subject")
        with col3:
            due_date = st.date_input("Due Date", key="assign_due")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            category = st.selectbox("Category", assignment_cats, key="assign_cat")
        with col_b:
            priority = st.selectbox("Priority", priority_levels, key="assign_priority")
        with col_c:
            status = st.selectbox("Status", ["Not Started", "In Progress", "Submitted", "Graded"], key="assign_status")
        
        grade = st.text_input("Grade (optional)", key="assign_grade")
        
        if st.button("➕ Add Assignment"):
            if assignment_name:
                st.session_state.assignments.append({
                    "name": assignment_name,
                    "subject": subject,
                    "due_date": str(due_date),
                    "priority": priority,
                    "status": status,
                    "grade": grade,
                    "created": datetime.datetime.now().strftime("%Y-%m-%d")
                })
                st.success("Assignment added!")
                st.rerun()
        
        if st.session_state.assignments:
            st.markdown("---")
            st.markdown("### 📋 Your Assignments")
            
            # Sort by due date
            sorted_assignments = sorted(st.session_state.assignments, key=lambda x: x['due_date'])
            
            for idx, assign in enumerate(sorted_assignments):
                days_left = (datetime.datetime.strptime(assign['due_date'], "%Y-%m-%d").date() - datetime.date.today()).days
                
                with st.expander(f"{assign['priority']} {assign['name']} - Due: {assign['due_date']} ({days_left} days)"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Subject:** {assign['subject']}")
                        st.write(f"**Status:** {assign['status']}")
                    with col2:
                        st.write(f"**Priority:** {assign['priority']}")
                        if assign['grade']:
                            st.write(f"**Grade:** {assign['grade']}")
                    
                    if st.button("🗑️ Delete", key=f"del_assign_{idx}"):
                        st.session_state.assignments.remove(assign)
                        st.rerun()
            
            # Statistics
            total = len(st.session_state.assignments)
            submitted = sum(1 for a in st.session_state.assignments if a['status'] == 'Submitted')
            graded = sum(1 for a in st.session_state.assignments if a['status'] == 'Graded')
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", total)
            with col2:
                st.metric("Submitted", submitted)
            with col3:
                st.metric("Graded", graded)
    
    # Lecture Notes to PDF
    with tabs[2]:
        st.markdown("### 📓 Lecture Notes Editor")
        
        st.info("Write your notes and export them as PDF!")
        
        note_title = st.text_input("Note Title", "My Lecture Notes")
        subject = st.text_input("Subject/Course", "General")
        date = st.date_input("Date", datetime.date.today())
        
        notes_content = st.text_area("Write your notes here...", height=400, 
                                     placeholder="Type your lecture notes, summaries, or study materials here...")
        
        if st.button("📥 Export to PDF"):
            if notes_content:
                buffer = io.BytesIO()
                c = canvas.Canvas(buffer, pagesize=letter)
                
                # Title
                c.setFont("Helvetica-Bold", 18)
                c.drawString(50, 750, note_title)
                
                # Metadata
                c.setFont("Helvetica", 12)
                c.drawString(50, 730, f"Subject: {subject}")
                c.drawString(50, 710, f"Date: {date}")
                
                # Content
                c.setFont("Helvetica", 11)
                y = 680
                for line in notes_content.split('\n'):
                    if y < 50:
                        c.showPage()
                        y = 750
                    c.drawString(50, y, line[:80])
                    y -= 20
                
                c.save()
                buffer.seek(0)
                
                st.download_button("📄 Download PDF", buffer, f"{note_title}.pdf", "application/pdf")
                st.success("PDF ready to download!")
    
    # Citation Generator
    with tabs[3]:
        st.markdown("### 📖 Citation Generator")
        
        citation_style = st.selectbox("Citation Style", ["APA 7th", "MLA 9th", "Chicago"])
        source_type = st.selectbox("Source Type", ["Book", "Journal Article", "Website", "Magazine"])
        
        if source_type == "Book":
            author = st.text_input("Author (Last, First)")
            year = st.text_input("Year")
            title = st.text_input("Book Title")
            publisher = st.text_input("Publisher")
            
            if st.button("Generate Citation"):
                if citation_style == "APA 7th":
                    citation = f"{author} ({year}). *{title}*. {publisher}."
                elif citation_style == "MLA 9th":
                    citation = f"{author}. *{title}*. {publisher}, {year}."
                else:  # Chicago
                    citation = f"{author}. *{title}*. {publisher}, {year}."
                
                st.success("Citation Generated:")
                st.code(citation)
                st.button("📋 Copy Citation")
        
        elif source_type == "Journal Article":
            author = st.text_input("Author (Last, First)")
            year = st.text_input("Year")
            article_title = st.text_input("Article Title")
            journal = st.text_input("Journal Name")
            volume = st.text_input("Volume")
            pages = st.text_input("Pages")
            
            if st.button("Generate Citation"):
                if citation_style == "APA 7th":
                    citation = f"{author} ({year}). {article_title}. *{journal}, {volume}*, {pages}."
                elif citation_style == "MLA 9th":
                    citation = f"{author}. \"{article_title}.\" *{journal}*, vol. {volume}, {year}, pp. {pages}."
                else:
                    citation = f"{author}. \"{article_title}.\" *{journal}* {volume} ({year}): {pages}."
                
                st.success("Citation Generated:")
                st.code(citation)
        
        elif source_type == "Website":
            author = st.text_input("Author/Organization")
            year = st.text_input("Year")
            title = st.text_input("Page Title")
            url = st.text_input("URL")
            access_date = st.date_input("Access Date")
            
            if st.button("Generate Citation"):
                if citation_style == "APA 7th":
                    citation = f"{author} ({year}). *{title}*. Retrieved {access_date}, from {url}"
                elif citation_style == "MLA 9th":
                    citation = f"{author}. \"{title}.\" {year}. {url}. Accessed {access_date}."
                else:
                    citation = f"{author}. \"{title}.\" Accessed {access_date}. {url}."
                
                st.success("Citation Generated:")
                st.code(citation)
    
    # Formula Sheet
    with tabs[4]:
        st.markdown("### 📐 Formula Sheet Library")
        
        # Load formulas from JSON
        formulas_data = json_utils.load_json_data('formulas.json')
        
        if not formulas_data:
            st.error("Unable to load formulas. Please check formulas.json file.")
            return
        
        category = st.selectbox("Select Category", ["Mathematics", "Physics", "Chemistry"])
        
        if category == "Mathematics":
            st.markdown("### 🧮 Mathematics Formulas")
            
            math_data = formulas_data.get('mathematics', {})
            
            for section_name, formulas in math_data.items():
                section_title = section_name.replace('_', ' & ').title()
                with st.expander(section_title):
                    for formula_item in formulas:
                        st.latex(rf"{formula_item['formula']}")
                        st.caption(formula_item['name'])
        
        elif category == "Physics":
            st.markdown("### ⚡ Physics Formulas")
            
            physics_data = formulas_data.get('physics', {})
            
            for section_name, formulas in physics_data.items():
                section_title = section_name.replace('_', ' & ').title()
                with st.expander(section_title):
                    for formula_item in formulas:
                        st.latex(rf"{formula_item['formula']}")
                        st.caption(formula_item['name'])
        
        else:  # Chemistry
            st.markdown("### ⚗️ Chemistry Formulas")
            
            chem_data = formulas_data.get('chemistry', {})
            
            for section_name, formulas in chem_data.items():
                section_title = section_name.replace('_', ' ').title()
                with st.expander(section_title):
                    if section_name == "basic":
                        for formula_item in formulas:
                            st.latex(rf"{formula_item['formula']}")
                            st.caption(formula_item['name'])
                    else:
                        for formula_item in formulas:
                            st.latex(rf"{formula_item['formula']}")
                            st.caption(formula_item['name'])
