import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

def show():
    st.markdown("## 📊 Analytics & Reports")
    
    tabs = st.tabs(["Study Analytics", "Grade Predictor", "Attendance Tracker", "Performance Dashboard"])
    
    # Study Analytics
    with tabs[0]:
        st.markdown("### 📈 Study Analytics")
        
        if 'study_sessions' not in st.session_state:
            st.session_state.study_sessions = []
        
        st.markdown("#### Log Study Session")
        col1, col2, col3 = st.columns(3)
        with col1:
            subject = st.text_input("Subject", key="study_subject")
        with col2:
            duration = st.number_input("Duration (hours)", 0.5, 12.0, 1.0, 0.5, key="study_duration")
        with col3:
            session_date = st.date_input("Date", datetime.date.today(), key="study_date")
        
        if st.button("📊 Log Session"):
            if subject:
                st.session_state.study_sessions.append({
                    "subject": subject,
                    "duration": duration,
                    "date": str(session_date)
                })
                st.success("Session logged!")
                st.rerun()
        
        if st.session_state.study_sessions:
            df = pd.DataFrame(st.session_state.study_sessions)
            
            # Total study time
            total_hours = df['duration'].sum()
            st.metric("📚 Total Study Time", f"{total_hours:.1f} hours")
            
            # Subject-wise breakdown
            subject_totals = df.groupby('subject')['duration'].sum().reset_index()
           
            fig = px.pie(subject_totals, values='duration', names='subject', 
                        title='Study Time Distribution by Subject')
            st.plotly_chart(fig, use_container_width=True)
            
            # Timeline
            df['date'] = pd.to_datetime(df['date'])
            daily_study = df.groupby('date')['duration'].sum().reset_index()
            
            fig2 = px.line(daily_study, x='date', y='duration', 
                          title='Daily Study Hours',
                          labels={'duration': 'Hours', 'date': 'Date'})
            st.plotly_chart(fig2, use_container_width=True)
    
    # Grade Predictor
    with tabs[1]:
        st.markdown("### 🎯 Grade Predictor")
        
        st.info("Predict your final grade based on current scores!")
        
        col1, col2 = st.columns(2)
        with col1:
            current_grade = st.number_input("Current Grade (%)", 0, 100, 75)
        with col2:
            current_weight = st.number_input("Current Weight (%)", 0, 100, 60)
        
        remaining_weight = 100 - current_weight
        
        st.write(f"**Remaining Weight:** {remaining_weight}%")
        
        st.markdown("### 🎯 Grade Scenarios")
        
        target_grades = [90, 80, 70, 60, 50]
        
        for target in target_grades:
            required = (target - (current_grade * current_weight / 100)) / (remaining_weight / 100)
            
            if required > 100:
                status = "❌ Not achievable"
                color = "red"
            elif required < 0:
                status = "✅ Already achieved"
                color = "green"
            else:
                status = f"📊 Need {required:.1f}%"
                color = "blue"
            
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.markdown(f"**Target: {target}%**")
            with col_b:
                st.markdown(f":{color}[{status}]")
    
    # Attendance Tracker
    with tabs[2]:
        st.markdown("### 📅 Attendance Tracker")
        
        if 'attendance' not in st.session_state:
            st.session_state.attendance = {}
        
        st.markdown("#### Add Course")
        col1, col2 = st.columns(2)
        with col1:
            course_name = st.text_input("Course Name", key="att_course")
        with col2:
            required_percentage = st. number_input("Required %", 0, 100, 75, key="att_req")
        
        if st.button("➕ Add Course"):
            if course_name and course_name not in st.session_state.attendance:
                st.session_state.attendance[course_name] = {
                    "required": required_percentage,
                    "present": 0,
                    "total": 0
                }
                st.success("Course added!")
                st.rerun()
        
        if st.session_state.attendance:
            st.markdown("---")
            st.markdown("### 📊 Attendance Status")
            
            for course, data in st.session_state.attendance.items():
                with st.expander(f"📚 {course}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        present = st.number_input(f"Classes Attended", 0, 200, data['present'], key=f"p_{course}")
                    with col2:
                        total = st.number_input(f"Total Classes", 0, 200, data['total'], key=f"t_{course}")
                    
                    if present != data['present'] or total != data['total']:
                        st.session_state.attendance[course]['present'] = present
                        st.session_state.attendance[course]['total'] = total
                    
                    if total > 0:
                        percentage = (present / total) * 100
                        
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Attendance", f"{percentage:.1f}%")
                        with col_b:
                            st.metric("Required", f"{data['required']}%")
                        with col_c:
                            shortage = total * (data['required'] / 100) - present
                            if shortage > 0:
                                st.metric("Classes Needed", int(shortage))
                            else:
                                st.metric("Extra Classes", int(abs(shortage)))
                        
                        if percentage >= data['required']:
                            st.success(f"✅ Meeting requirement!")
                        else:
                            st.error(f"⚠️ Below requirement by {data['required'] - percentage:.1f}%")
                        
                        st.progress(min(percentage / 100, 1.0))
    
    # Performance Dashboard
    with tabs[3]:
        st.markdown("### 📊 Performance Dashboard")
        
        st.info("Comprehensive overview of your academic performance")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate from existing data
        total_study_hours = sum(s['duration'] for s in st.session_state.get('study_sessions', []))
        total_tasks = len(st.session_state.get('todo_list', []))
        completed_tasks = sum(1 for t in st.session_state.get('todo_list', []) if t.get('completed', False))
        total_assignments = len(st.session_state.get('assignments', []))
        
        with col1:
            st.metric("📚 Study Hours", f"{total_study_hours:.1f}")
        with col2:
            st.metric("✅ Tasks Done", f"{completed_tasks}/{total_tasks}")
        with col3:
            st.metric("📝 Assignments", total_assignments)
        with col4:
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            st.metric("🎯 Completion", f"{completion_rate:.0f}%")
        
        st.markdown("---")
        
        # Activity overview
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("### 📈 Study Progress")
            if st.session_state.get('study_sessions'):
                df = pd.DataFrame(st.session_state.study_sessions)
                subject_totals = df.groupby('subject')['duration'].sum().reset_index()
                
                fig = px.bar(subject_totals, x='subject', y='duration',
                           title='Hours by Subject',
                           labels={'duration': 'Hours', 'subject': 'Subject'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No study sessions logged yet")
        
        with col_b:
            st.markdown("### 🎯 Task Completion")
            if total_tasks > 0:
                task_data = pd.DataFrame({
                    'Status': ['Completed', 'Pending'],
                    'Count': [completed_tasks, total_tasks - completed_tasks]
                })
                
                fig2 = px.pie(task_data, values='Count', names='Status',
                            title='Task Status',
                            color_discrete_sequence=['#00ff00', '#ff6b6b'])
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No tasks created yet")
        
        # Weekly overview
        st.markdown("### 📅 Weekly Overview")
        
        week_start = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        week_data = []
        
        for i in range(7):
            day = week_start + datetime.timedelta(days=i)
            day_name = day.strftime('%A')
            
            # Count sessions for this day
            sessions = sum(1 for s in st.session_state.get('study_sessions', []) 
                          if s['date'] == str(day))
            
            week_data.append({'Day': day_name[:3], 'Sessions': sessions})
        
        df_week = pd.DataFrame(week_data)
        
        fig3 = px.bar(df_week, x='Day', y='Sessions',
                     title='Study Sessions This Week',
                     labels={'Sessions': 'Number of Sessions'})
        st.plotly_chart(fig3, use_container_width=True)
