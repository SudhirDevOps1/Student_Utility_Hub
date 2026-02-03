import streamlit as st
import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import random
import json_utils

def show():
    st.markdown("## 🎯 Productivity Boosters")
    
    tabs = st.tabs(["Habit Tracker", "Goal Setter", "Focus Mode", "Daily Journal", "Expense Tracker"])
    
    # Habit Tracker
    with tabs[0]:
        st.markdown("### ✅ Habit Tracker")
        
        if 'habits' not in st.session_state:
            st.session_state.habits = []
        if 'habit_logs' not in st.session_state:
            st.session_state.habit_logs = {}
        
        col1, col2 = st.columns([3, 1])
        with col1:
            new_habit = st.text_input("New Habit", placeholder="e.g., Read for 30 minutes")
        with col2:
            if st.button("➕ Add Habit", use_container_width=True):
                if new_habit and new_habit not in st.session_state.habits:
                    st.session_state.habits.append(new_habit)
                    st.session_state.habit_logs[new_habit] = []
                    st.success("Habit added!")
                    st.rerun()
        
        if st.session_state.habits:
            st.markdown("### 📅 Today's Habits")
            today = datetime.date.today().isoformat()
            
            for habit in st.session_state.habits:
                col_a, col_b, col_c = st.columns([3, 1, 1])
                
                with col_a:
                    st.write(f"**{habit}**")
                
                with col_b:
                    if today in st.session_state.habit_logs.get(habit, []):
                        st.success("✅ Done")
                    else:
                        if st.button("✓ Mark Done", key=f"hab_{habit}"):
                            if habit not in st.session_state.habit_logs:
                                st.session_state.habit_logs[habit] = []
                            st.session_state.habit_logs[habit].append(today)
                            st.rerun()
                
                with col_c:
                    streak = 0
                    if habit in st.session_state.habit_logs:
                        logs = sorted(st.session_state.habit_logs[habit], reverse=True)
                        for i, log_date in enumerate(logs):
                            expected_date = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
                            if log_date == expected_date:
                                streak += 1
                            else:
                                break
                    st.metric("🔥 Streak", f"{streak} days")
            
            st.markdown("---")
            st.markdown("### 📊 Habit Statistics")
            for habit in st.session_state.habits:
                total_days = len(st.session_state.habit_logs.get(habit, []))
                st.write(f"**{habit}**: {total_days} days completed")
    
    # Goal Setter
    with tabs[1]:
        st.markdown("### 🎯 Goal Setter")
        
        if 'goals' not in st.session_state:
            st.session_state.goals = []
        
        goal_type = st.radio("Goal Type", ["Short-term (1-3 months)", "Long-term (6+ months)"], horizontal=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            goal_title = st.text_input("Goal Title")
            goal_desc = st.text_area("Description", height=100)
        with col2:
            target_date = st.date_input("Target Date")
            category = st.selectbox("Category", ["Academic", "Personal", "Career", "Health", "Other"])
        
        if st.button("➕ Add Goal"):
            if goal_title:
                st.session_state.goals.append({
                    "title": goal_title,
                    "description": goal_desc,
                    "type": goal_type,
                    "category": category,
                    "target_date": str(target_date),
                    "progress": 0,
                    "created": datetime.date.today().isoformat()
                })
                st.success("Goal added!")
                st.rerun()
        
        if st.session_state.goals:
            st.markdown("---")
            st.markdown("### 🎯 Your Goals")
            
            for idx, goal in enumerate(st.session_state.goals):
                days_left = (datetime.datetime.strptime(goal['target_date'], "%Y-%m-%d").date() - datetime.date.today()).days
                
                with st.expander(f"{goal['category']} - {goal['title']} ({days_left} days left)"):
                    st.write(f"**Description:** {goal['description']}")
                    st.write(f"**Type:** {goal['type']}")
                    st.write(f"**Target:** {goal['target_date']}")
                    
                    progress = st.slider("Progress", 0, 100, goal['progress'], key=f"goal_{idx}")
                    if progress != goal['progress']:
                        st.session_state.goals[idx]['progress'] = progress
                    
                    st.progress(progress / 100)
                    
                    if st.button("🗑️ Delete Goal", key=f"del_goal_{idx}"):
                        st.session_state.goals.pop(idx)
                        st.rerun()
    
    # Focus Mode
    with tabs[2]:
        st.markdown("### 🎯 Focus Mode")
        
        st.info("Block distractions and stay focused with motivational quotes!")
        
        # Load quotes from JSON
        quotes_data = json_utils.load_json_data('quotes.json')
        quotes = quotes_data.get('quotes', [
            "The secret of getting ahead is getting started. - Mark Twain",
            "Success is not final, failure is not fatal. - Winston Churchill"
        ])
        
        st.markdown(f"### 💡 *\"{random.choice(quotes)}\"*")
        
        col1, col2 = st.columns(2)
        with col1:
            focus_duration = st.number_input("Focus Duration (minutes)", 15, 180, 25)
        with col2:
            task_name = st.text_input("What are you working on?", "Study Session")
        
        if 'focus_active' not in st.session_state:
            st.session_state.focus_active = False
        if 'focus_remaining' not in st.session_state:
            st.session_state.focus_remaining = 0
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎯 Start Focus", use_container_width=True, key="focus_start"):
                st.session_state.focus_active = True
                st.session_state.focus_remaining = focus_duration * 60
                st.success(f"Focus mode started for {focus_duration} minutes!")
        
        with col_b:
            if st.button("🛑 Stop Focus", use_container_width=True, key="focus_stop"):
                st.session_state.focus_active = False
                st.warning("Focus mode stopped")
        
        if st.session_state.focus_remaining > 0:
            mins = st.session_state.focus_remaining // 60
            secs = st.session_state.focus_remaining % 60
            
            st.markdown(f"### ⏱️ {mins:02d}:{secs:02d}")
            st.progress(1 - (st.session_state.focus_remaining / (focus_duration * 60)))
            
            if st.session_state.focus_remaining == 0:
                st.success("🎉 Focus session complete! Great work!")
                st.balloons()
    
    # Daily Journal
    with tabs[3]:
        st.markdown("### 📔 Daily Journal")
        
        if 'journal_entries' not in st.session_state:
            st.session_state.journal_entries = {}
        
        today = datetime.date.today().isoformat()
        
        st.markdown(f"### 📅 {datetime.date.today().strftime('%A, %B %d, %Y')}")
        
        mood = st.select_slider("How are you feeling?", 
                               options=["😞 Terrible", "😕 Bad", "😐 Okay", "🙂 Good", "😄 Great"],
                               value="😐 Okay")
        
        entry = st.text_area("Write your thoughts...", height=300, 
                           value=st.session_state.journal_entries.get(today, {}).get('entry', ''),
                           placeholder="What happened today? How do you feel? What are you grateful for?")
        
        tags = st.multiselect("Tags", ["Personal", "Academic", "Goals", "Challenges", "Achievements", "Reflection"])
        
        if st.button("💾 Save Entry"):
            st.session_state.journal_entries[today] = {
                "entry": entry,
                "mood": mood,
                "tags": tags,
                "date": today
            }
            st.success("Journal entry saved!")
        
        if st.session_state.journal_entries:
            st.markdown("---")
            st.markdown("### 📚 Past Entries")
            
            for date, data in sorted(st.session_state.journal_entries.items(), reverse=True)[:5]:
                with st.expander(f"{data['mood']} {date}"):
                    st.write(data['entry'])
                    if data.get('tags'):
                        st.write(f"Tags: {', '.join(data['tags'])}")
    
    # Expense Tracker
    with tabs[4]:
        st.markdown("### 💰 Student Expense Tracker")
        
        if 'expenses' not in st.session_state:
            st.session_state.expenses = []
        if 'budget' not in st.session_state:
            st.session_state.budget = 10000
        
        col1, col2 = st.columns(2)
        with col1:
            monthly_budget = st.number_input("Monthly Budget (₹)", 0, 100000, st.session_state.budget)
            if monthly_budget != st.session_state.budget:
                st.session_state.budget = monthly_budget
        
        st.markdown("---")
        st.markdown("### ➕ Add Expense")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            expense_name = st.text_input("Expense", key="exp_name")
        with col_b:
            amount = st.number_input("Amount (₹)", 0, 50000, 0, key="exp_amount")
        with col_c:
            category = st.selectbox("Category", 
                                   ["Food", "Transport", "Books", "Entertainment", "Bills", "Other"],
                                   key="exp_category")
        
        expense_date = st.date_input("Date", datetime.date.today(), key="exp_date")
        
        if st.button("➕ Add Expense"):
            if expense_name and amount > 0:
                st.session_state.expenses.append({
                    "name": expense_name,
                    "amount": amount,
                    "category": category,
                    "date": str(expense_date)
                })
                st.success("Expense added!")
                st.rerun()
        
        if st.session_state.expenses:
            st.markdown("---")
            st.markdown("### 📊 Expense Summary")
            
            total_spent = sum(exp['amount'] for exp in st.session_state.expenses)
            remaining = st.session_state.budget - total_spent
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Budget", f"₹{st.session_state.budget:,.0f}")
            with col2:
                st.metric("Spent", f"₹{total_spent:,.0f}")
            with col3:
                st.metric("Remaining", f"₹{remaining:,.0f}")
            
            st.progress(min(total_spent / st.session_state.budget, 1.0))
            
            # Category breakdown
            st.markdown("### 📈 By Category")
            category_totals = {}
            for exp in st.session_state.expenses:
                category_totals[exp['category']] = category_totals.get(exp['category'], 0) + exp['amount']
            
            for cat, total in category_totals.items():
                st.write(f"**{cat}:** ₹{total:,.0f}")
            
            # Recent expenses
            st.markdown("### 📝 Recent Expenses")
            for idx, exp in enumerate(sorted(st.session_state.expenses, key=lambda x: x['date'], reverse=True)[:10]):
                with st.expander(f"₹{exp['amount']} - {exp['name']} ({exp['date']})"):
                    st.write(f"**Category:** {exp['category']}")
                    if st.button("🗑️ Delete", key=f"del_exp_{idx}"):
                        st.session_state.expenses.remove(exp)
                        st.rerun()
