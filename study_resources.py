import streamlit as st
import json_utils

def show():
    st.markdown("## 📚 Study Resources & Tips")
    
    tabs = st.tabs(["Study Techniques", "Exam Strategies", "Keyboard Shortcuts", "Study Schedules", "Productivity Apps"])
    
    # Study Techniques
    with tabs[0]:
        st.markdown("### 🎓 Proven Study Techniques")
        
        study_data = json_utils.load_json_data('study_guide.json')
        techniques = study_data.get('study_techniques', [])
        
        for technique in techniques:
            with st.expander(f"📌 {technique['name']}"):
                st.markdown(f"**Description:** {technique['description']}")
                st.markdown(f"**Best for:** {technique['best_for']}")
                
                st.markdown("**Steps:**")
                for i, step in enumerate(technique['steps'], 1):
                    st.write(f"{i}. {step}")
        
        st.markdown("---")
        st.markdown("### 💡 General Study Tips")
        tips = study_data.get('study_tips', [])
        
        for i, tip in enumerate(tips, 1):
            st.write(f"✅ {tip}")
    
    # Exam Strategies
    with tabs[1]:
        st.markdown("### 📝 Exam Strategies")
        
        study_data = json_utils.load_json_data('study_guide.json')
        exam_strategies = study_data.get('exam_strategies', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 Before Exam")
            for strategy in exam_strategies.get('before_exam', []):
                st.write(f"• {strategy}")
        
        with col2:
            st.markdown("#### ✍️ During Exam")
            for strategy in exam_strategies.get('during_exam', []):
                st.write(f"• {strategy}")
        
        st.markdown("---")
        st.markdown("### 📚 Subject-Specific Strategies")
        
        subject_specific = exam_strategies.get('subject_specific', {})
        
        for subject, strategies in subject_specific.items():
            with st.expander(f"📖 {subject.title()}"):
                for strategy in strategies:
                    st.write(f"✓ {strategy}")
    
    # Keyboard Shortcuts
    with tabs[2]:
        st.markdown("### ⌨️ Keyboard Shortcuts")
        
        resources_data = json_utils.load_json_data('resources.json')
        shortcuts_data = resources_data.get('shortcuts', {})
        
        platform = st.selectbox("Select Platform", ["Windows", "Mac"])
        
        platform_key = platform.lower()
        platform_shortcuts = shortcuts_data.get(platform_key, {})
        
        for category, shortcuts in platform_shortcuts.items():
            st.markdown(f"#### {category.title()}")
            
            for shortcut in shortcuts:
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.code(shortcut['keys'])
                with col_b:
                    st.write(shortcut['action'])
            
            st.markdown("---")
    
    # Study Schedules
    with tabs[3]:
        st.markdown("### 📅 Study Schedule Templates")
        
        settings_data = json_utils.load_json_data('custom_settings.json')
        schedules = settings_data.get('study_schedules', {})
        
        schedule_type = st.selectbox("Select Schedule Type", 
                                    list(schedules.keys()))
        
        if schedule_type in schedules:
            schedule = schedules[schedule_type]
            
            st.markdown(f"### {schedule['name']}")
            st.info(f"A structured daily schedule to maximize {schedule_type.replace('_', ' ')} productivity")
            
            st.markdown("#### 📊 Daily Schedule")
            
            for slot in schedule['schedule']:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"**{slot['time']}**")
                with col2:
                    st.write(slot['activity'])
            
            if st.button("📥 Export Schedule"):
                schedule_text = f"{schedule['name']}\n\n"
                for slot in schedule['schedule']:
                    schedule_text += f"{slot['time']}: {slot['activity']}\n"
                
                st.download_button("Download Schedule", schedule_text, 
                                 f"{schedule_type}_schedule.txt", "text/plain")
    
    # Productivity Apps
    with tabs[4]:
        st.markdown("### 📱 Recommended Productivity Apps")
        
        resources_data = json_utils.load_json_data('resources.json')
        apps = resources_data.get('productivity_apps', [])
        
        st.info("Boost your productivity with these recommended apps!")
        
        for app in apps:
            with st.expander(f"💡 {app['name']} - {app['category']}"):
                st.markdown(f"**Description:** {app['description']}")
                st.markdown(f"**Available on:** {app['platform']}")
        
        st.markdown("---")
        st.markdown("### 🆕 Add Your Own App Recommendation")
        
        col_a, col_b = st.columns(2)
        with col_a:
            new_app_name = st.text_input("App Name", key="new_app")
            new_app_category = st.text_input("Category", key="new_cat")
        with col_b:
            new_app_desc = st.text_area("Description", key="new_desc")
            new_app_platform = st.text_input("Platforms", key="new_plat")
        
        if st.button("➕ Add to JSON"):
            if new_app_name and new_app_desc:
                apps.append({
                    "name": new_app_name,
                    "category": new_app_category,
                    "description": new_app_desc,
                    "platform": new_app_platform
                })
                
                resources_data['productivity_apps'] = apps
                if json_utils.save_json_data('resources.json', resources_data):
                    st.success("✅ App added to resources.json!")
                    st.rerun()
                else:
                    st.error("Failed to save")
