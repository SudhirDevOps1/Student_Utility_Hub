import streamlit as st
import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def show():
    st.markdown("## 🎓 Student Utilities")
    
    tabs = st.tabs(["Study Planner", "Exam Countdown", "Notes Manager", "Productivity Tracker", "Calculator", "To-Do List", "Countdown Timer", "Stopwatch", "Pomodoro Timer"])
    
    with tabs[0]:
        st.markdown("### 📅 Daily Study Planner")
        
        if 'schedule' not in st.session_state:
            st.session_state.schedule = []
        
        col1, col2, col3 = st.columns(3)
        with col1:
            subject = st.text_input("Subject", key="subject_input")
        with col2:
            time_slot = st.text_input("Time (e.g., 9:00 AM - 10:00 AM)", key="time_input")
        with col3:
            if st.button("Add to Schedule"):
                if subject and time_slot:
                    st.session_state.schedule.append({"Subject": subject, "Time": time_slot})
                    st.success("Added!")
        
        if st.session_state.schedule:
            df = pd.DataFrame(st.session_state.schedule)
            st.dataframe(df, use_container_width=True)
            
            if st.button("Clear Schedule"):
                st.session_state.schedule = []
                st.rerun()
    
    with tabs[1]:
        st.markdown("### ⏰ Exam Countdown Timer")
        
        exam_name = st.text_input("Exam Name", "Final Exams")
        exam_date = st.date_input("Exam Date", datetime.date.today() + datetime.timedelta(days=30))
        
        today = datetime.date.today()
        days_left = (exam_date - today).days
        
        if days_left > 0:
            st.markdown(f"### 🎯 {days_left} Days Until {exam_name}")
            st.progress(max(0, min(1, (30 - days_left) / 30)))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Days", days_left)
            with col2:
                st.metric("Weeks", round(days_left / 7, 1))
            with col3:
                st.metric("Months", round(days_left / 30, 1))
        elif days_left == 0:
            st.success("🎉 Exam is TODAY! Good luck!")
        else:
            st.info("Exam has passed")
    
    with tabs[2]:
        st.markdown("### 📝 Notes Manager")
        
        if 'notes' not in st.session_state:
            st.session_state.notes = {}
        
        col1, col2 = st.columns([2, 1])
        with col1:
            note_subject = st.text_input("Subject/Topic", key="note_subject")
        with col2:
            folder = st.selectbox("Folder", ["General", "Important", "Revision", "Assignments"])
        
        note_content = st.text_area("Write your notes here...", height=200, key="note_content")
        
        if st.button("Save Note"):
            if note_subject and note_content:
                key = f"{folder}/{note_subject}"
                st.session_state.notes[key] = note_content
                st.success(f"✅ Saved to {folder}")
        
        st.markdown("### 📚 Saved Notes")
        for key, content in st.session_state.notes.items():
            with st.expander(f"📄 {key}"):
                st.write(content)
                if st.button(f"Delete", key=f"del_{key}"):
                    del st.session_state.notes[key]
                    st.rerun()
    
    with tabs[3]:
        st.markdown("### 📊 Daily Productivity Tracker")
        
        if 'productivity' not in st.session_state:
            st.session_state.productivity = []
        
        col1, col2, col3 = st.columns(3)
        with col1:
            task = st.text_input("Task", key="task_input")
        with col2:
            hours = st.number_input("Hours Spent", 0.0, 24.0, 1.0, 0.5)
        with col3:
            status = st.selectbox("Status", ["Completed", "In Progress", "Pending"])
        
        if st.button("Log Task"):
            if task:
                st.session_state.productivity.append({
                    "Date": datetime.date.today(),
                    "Task": task,
                    "Hours": hours,
                    "Status": status
                })
                st.success("Logged!")
        
        if st.session_state.productivity:
            df = pd.DataFrame(st.session_state.productivity)
            st.dataframe(df, use_container_width=True)
            
            total_hours = sum([item['Hours'] for item in st.session_state.productivity])
            st.metric("Total Hours Tracked", f"{total_hours} hrs")
            
            if st.button("Export as PDF"):
                buffer = io.BytesIO()
                c = canvas.Canvas(buffer, pagesize=letter)
                c.drawString(100, 750, "Productivity Report")
                y = 700
                for item in st.session_state.productivity:
                    c.drawString(50, y, f"{item['Date']} - {item['Task']} - {item['Hours']}h - {item['Status']}")
                    y -= 20
                c.save()
                buffer.seek(0)
                st.download_button("Download PDF", buffer, "productivity.pdf", "application/pdf")
    
    with tabs[4]:
        st.markdown("### 🧮 Student Calculator")
        
        calc_type = st.selectbox("Calculator Type", ["GPA Calculator", "Percentage Calculator", "CGPA Calculator"])
        
        if calc_type == "GPA Calculator":
            st.markdown("#### Calculate GPA")
            num_subjects = st.number_input("Number of Subjects", 1, 10, 5)
            
            grades = []
            credits = []
            
            for i in range(num_subjects):
                col1, col2 = st.columns(2)
                with col1:
                    grade = st.selectbox(f"Subject {i+1} Grade", ["A+", "A", "B+", "B", "C", "D", "F"], key=f"grade_{i}")
                with col2:
                    credit = st.number_input(f"Credits", 1, 6, 3, key=f"credit_{i}")
                
                grade_points = {"A+": 4.0, "A": 3.7, "B+": 3.3, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
                grades.append(grade_points[grade])
                credits.append(credit)
            
            if st.button("Calculate GPA"):
                gpa = sum([g * c for g, c in zip(grades, credits)]) / sum(credits)
                st.success(f"### Your GPA: {gpa:.2f}")
        
        elif calc_type == "Percentage Calculator":
            obtained = st.number_input("Marks Obtained", 0, 1000, 450)
            total = st.number_input("Total Marks", 0, 1000, 500)
            
            if st.button("Calculate"):
                percentage = (obtained / total) * 100
                st.success(f"### Percentage: {percentage:.2f}%")
        
        else:
            st.markdown("#### CGPA Calculator")
            num_semesters = st.number_input("Number of Semesters", 1, 8, 4)
            
            gpas = []
            for i in range(num_semesters):
                gpa = st.number_input(f"Semester {i+1} GPA", 0.0, 4.0, 3.5, key=f"sem_{i}")
                gpas.append(gpa)
            
            if st.button("Calculate CGPA"):
                cgpa = sum(gpas) / len(gpas)
                st.success(f"### Your CGPA: {cgpa:.2f}")
    
    # To-Do List
    with tabs[5]:
        st.markdown("### ✅ To-Do List Manager")
        
        if 'todo_list' not in st.session_state:
            st.session_state.todo_list = []
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            new_task = st.text_input("Add new task", key="new_task", placeholder="Enter your task here...")
        with col2:
            priority = st.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"], key="priority")
        with col3:
            st.write("")
            st.write("")
            if st.button("➕ Add Task", use_container_width=True):
                if new_task:
                    st.session_state.todo_list.append({
                        "task": new_task,
                        "priority": priority,
                        "completed": False,
                        "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("Task added!")
                    st.rerun()
        
        if st.session_state.todo_list:
            st.markdown("---")
            st.markdown("### 📋 Your Tasks")
            
            # Filter options
            filter_opt = st.radio("Filter", ["All", "Active", "Completed"], horizontal=True)
            
            for idx, item in enumerate(st.session_state.todo_list):
                if filter_opt == "Active" and item['completed']:
                    continue
                if filter_opt == "Completed" and not item['completed']:
                    continue
                
                col_a, col_b, col_c, col_d = st.columns([0.5, 3, 1.5, 1])
                
                with col_a:
                    if st.checkbox("", value=item['completed'], key=f"check_{idx}"):
                        st.session_state.todo_list[idx]['completed'] = True
                    else:
                        st.session_state.todo_list[idx]['completed'] = False
                
                with col_b:
                    if item['completed']:
                        st.markdown(f"~~{item['task']}~~")
                    else:
                        st.markdown(f"**{item['task']}**")
                
                with col_c:
                    st.text(f"{item['priority']} • {item['created']}")
                
                with col_d:
                    if st.button("🗑️", key=f"del_todo_{idx}"):
                        st.session_state.todo_list.pop(idx)
                        st.rerun()
            
            # Statistics
            total = len(st.session_state.todo_list)
            completed = sum(1 for item in st.session_state.todo_list if item['completed'])
            pending = total - completed
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tasks", total)
            with col2:
                st.metric("Completed", completed)
            with col3:
                st.metric("Pending", pending)
            
            if total > 0:
                st.progress(completed / total)
            
            if st.button("🗑️ Clear All Completed"):
                st.session_state.todo_list = [item for item in st.session_state.todo_list if not item['completed']]
                st.rerun()
        else:
            st.info("📝 No tasks yet. Add your first task above!")
    
    # Countdown Timer
    with tabs[6]:
        st.markdown("### ⏱️ Countdown Timer")
        
        st.info("Set a countdown timer for your study sessions, breaks, or any timed activity!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            hours = st.number_input("Hours", 0, 23, 0, key="countdown_hours")
        with col2:
            minutes = st.number_input("Minutes", 0, 59, 25, key="countdown_minutes")
        with col3:
            seconds = st.number_input("Seconds", 0, 59, 0, key="countdown_seconds")
        
        total_seconds = hours * 3600 + minutes * 60 + seconds
        
        if 'countdown_active' not in st.session_state:
            st.session_state.countdown_active = False
        if 'countdown_remaining' not in st.session_state:
            st.session_state.countdown_remaining = 0
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("▶️ Start", use_container_width=True, key="countdown_start"):
                st.session_state.countdown_active = True
                st.session_state.countdown_remaining = total_seconds
                st.success(f"Timer started for {hours}h {minutes}m {seconds}s")
        
        with col_b:
            if st.button("⏸️ Pause", use_container_width=True, key="countdown_pause"):
                st.session_state.countdown_active = False
                st.info("Timer paused")
        
        with col_c:
            if st.button("🔄 Reset", use_container_width=True, key="countdown_reset"):
                st.session_state.countdown_active = False
                st.session_state.countdown_remaining = 0
                st.warning("Timer reset")
        
        if st.session_state.countdown_remaining > 0:
            hrs = st.session_state.countdown_remaining // 3600
            mins = (st.session_state.countdown_remaining % 3600) // 60
            secs = st.session_state.countdown_remaining % 60
            
            st.markdown(f"### ⏰ {hrs:02d}:{mins:02d}:{secs:02d}")
            st.progress(1 - (st.session_state.countdown_remaining / total_seconds if total_seconds > 0 else 0))
            
            if st.session_state.countdown_remaining == 0:
                st.success("⏰ Time's up!")
                st.balloons()
    
    # Stopwatch
    with tabs[7]:
        st.markdown("### ⏲️ Stopwatch")
        
        st.info("Track time spent on tasks, study sessions, or any activity!")
        
        if 'stopwatch_start' not in st.session_state:
            st.session_state.stopwatch_start = None
        if 'stopwatch_elapsed' not in st.session_state:
            st.session_state.stopwatch_elapsed = 0
        if 'stopwatch_running' not in st.session_state:
            st.session_state.stopwatch_running = False
        if 'stopwatch_laps' not in st.session_state:
            st.session_state.stopwatch_laps = []
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("▶️ Start", use_container_width=True, key="sw_start"):
                if not st.session_state.stopwatch_running:
                    st.session_state.stopwatch_start = datetime.datetime.now()
                    st.session_state.stopwatch_running = True
                    st.success("Stopwatch started!")
        
        with col2:
            if st.button("⏸️ Stop", use_container_width=True, key="sw_stop"):
                if st.session_state.stopwatch_running:
                    elapsed = (datetime.datetime.now() - st.session_state.stopwatch_start).total_seconds()
                    st.session_state.stopwatch_elapsed += elapsed
                    st.session_state.stopwatch_running = False
                    st.info("Stopwatch stopped")
        
        with col3:
            if st.button("📍 Lap", use_container_width=True, key="sw_lap"):
                if st.session_state.stopwatch_running:
                    current_elapsed = st.session_state.stopwatch_elapsed
                    if st.session_state.stopwatch_running:
                        current_elapsed += (datetime.datetime.now() - st.session_state.stopwatch_start).total_seconds()
                    st.session_state.stopwatch_laps.append(current_elapsed)
                    st.success(f"Lap {len(st.session_state.stopwatch_laps)} recorded!")
        
        with col4:
            if st.button("🔄 Reset", use_container_width=True, key="sw_reset"):
                st.session_state.stopwatch_start = None
                st.session_state.stopwatch_elapsed = 0
                st.session_state.stopwatch_running = False
                st.session_state.stopwatch_laps = []
                st.warning("Stopwatch reset")
        
        # Display elapsed time
        current_elapsed = st.session_state.stopwatch_elapsed
        if st.session_state.stopwatch_running and st.session_state.stopwatch_start:
            current_elapsed += (datetime.datetime.now() - st.session_state.stopwatch_start).total_seconds()
        
        hrs = int(current_elapsed // 3600)
        mins = int((current_elapsed % 3600) // 60)
        secs = int(current_elapsed % 60)
        msecs = int((current_elapsed % 1) * 100)
        
        st.markdown(f"### ⏱️ {hrs:02d}:{mins:02d}:{secs:02d}.{msecs:02d}")
        
        # Display laps
        if st.session_state.stopwatch_laps:
            st.markdown("### 📍 Lap Times")
            for i, lap_time in enumerate(st.session_state.stopwatch_laps):
                lap_hrs = int(lap_time // 3600)
                lap_mins = int((lap_time % 3600) // 60)
                lap_secs = int(lap_time % 60)
                st.text(f"Lap {i+1}: {lap_hrs:02d}:{lap_mins:02d}:{lap_secs:02d}")
    
    # Pomodoro Timer
    with tabs[8]:
        st.markdown("### 🍅 Pomodoro Timer")
        
        st.info("Boost productivity with the Pomodoro Technique: 25 min work + 5 min break cycles!")
        
        col1, col2 = st.columns(2)
        with col1:
            work_duration = st.number_input("Work Duration (minutes)", 1, 60, 25, key="pomodoro_work")
        with col2:
            break_duration = st.number_input("Break Duration (minutes)", 1, 30, 5, key="pomodoro_break")
        
        if 'pomodoro_mode' not in st.session_state:
            st.session_state.pomodoro_mode = "work"  # "work" or "break"
        if 'pomodoro_remaining' not in st.session_state:
            st.session_state.pomodoro_remaining = work_duration * 60
        if 'pomodoro_active' not in st.session_state:
            st.session_state.pomodoro_active = False
        if 'pomodoro_completed' not in st.session_state:
            st.session_state.pomodoro_completed = 0
        
        # Display current mode
        if st.session_state.pomodoro_mode == "work":
            st.markdown("### 💼 Work Session")
            mode_color = "🔴"
        else:
            st.markdown("### ☕ Break Time")
            mode_color = "🟢"
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("▶️ Start Pomodoro", use_container_width=True, key="pomodoro_start"):
                st.session_state.pomodoro_active = True
                if st.session_state.pomodoro_mode == "work":
                    st.session_state.pomodoro_remaining = work_duration * 60
                else:
                    st.session_state.pomodoro_remaining = break_duration * 60
                st.success("Pomodoro started!")
        
        with col_b:
            if st.button("⏸️ Pause", use_container_width=True, key="pomodoro_pause"):
                st.session_state.pomodoro_active = False
                st.info("Pomodoro paused")
        
        with col_c:
            if st.button("🔄 Reset", use_container_width=True, key="pomodoro_reset"):
                st.session_state.pomodoro_active = False
                st.session_state.pomodoro_mode = "work"
                st.session_state.pomodoro_remaining = work_duration * 60
                st.warning("Pomodoro reset")
        
        # Display timer
        mins = st.session_state.pomodoro_remaining // 60
        secs = st.session_state.pomodoro_remaining % 60
        
        st.markdown(f"### {mode_color} {mins:02d}:{secs:02d}")
        
        total = work_duration * 60 if st.session_state.pomodoro_mode == "work" else break_duration * 60
        st.progress(1 - (st.session_state.pomodoro_remaining / total if total > 0 else 0))
        
        # Statistics
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🍅 Pomodoros Completed", st.session_state.pomodoro_completed)
        with col2:
            total_time = st.session_state.pomodoro_completed * work_duration
            st.metric("⏱️ Total Focus Time", f"{total_time} min")
        
        if st.session_state.pomodoro_remaining == 0 and st.session_state.pomodoro_active:
            if st.session_state.pomodoro_mode == "work":
                st.success("🎉 Work session completed! Time for a break!")
                st.balloons()
                st.session_state.pomodoro_mode = "break"
                st.session_state.pomodoro_remaining = break_duration * 60
                st.session_state.pomodoro_completed += 1
            else:
                st.success("✨ Break over! Ready for another work session?")
                st.session_state.pomodoro_mode = "work"
                st.session_state.pomodoro_remaining = work_duration * 60
                st.session_state.pomodoro_active = False
