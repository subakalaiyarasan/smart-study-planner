import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from modules.chatbot import StudyPlannerChatbot
from modules.scheduler import ScheduleGenerator
from modules.database import Database
import json

# Load environment variables
load_dotenv()

# Initialize Streamlit Config
st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .timetable {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .goal-item {
            background-color: #e8f5e9;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            border-left: 4px solid #4CAF50;
        }
        .motivational-tip {
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = StudyPlannerChatbot()
    st.session_state.db = Database()
    st.session_state.conversation_history = []
    st.session_state.user_profile = None
    st.session_state.generated_schedule = None
    st.session_state.current_page = "Home"

def main():
    # Header
    st.title("📚 Smart Study Planner")
    st.markdown("*Your Personal AI Study Companion*")
    
    # Sidebar Navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/learning.png", width=80)
        st.markdown("---")
        
        page = st.radio(
            "🔍 Navigation",
            ["Home", "Chat with AI", "My Schedule", "Progress Tracker", "Settings"]
        )
        st.session_state.current_page = page
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        if st.session_state.user_profile:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Subjects", len(st.session_state.user_profile.get('subjects', [])))
            with col2:
                st.metric("Study Hours/Day", st.session_state.user_profile.get('daily_hours', 0))
    
    # Page Routing
    if st.session_state.current_page == "Home":
        show_home()
    elif st.session_state.current_page == "Chat with AI":
        show_chat()
    elif st.session_state.current_page == "My Schedule":
        show_schedule()
    elif st.session_state.current_page == "Progress Tracker":
        show_progress()
    elif st.session_state.current_page == "Settings":
        show_settings()

def show_home():
    """Home page with introduction and quick start"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Welcome to Smart Study Planner! 🎓")
        st.write("""
            Create a personalized study timetable that adapts to your unique needs.
            Our AI-powered system analyzes your subjects, exams, and preferences to
            generate an optimized study schedule.
        """)
        
        st.subheader("✨ Key Features")
        features = [
            "🎯 Personalized Study Schedules",
            "📅 Exam Date Tracking",
            "⏱️ Optimized Break Intervals",
            "📝 Revision & Practice Tests",
            "💪 Motivational Tips & Goals",
            "📊 Progress Monitoring"
        ]
        for feature in features:
            st.write(feature)
    
    with col2:
        st.info("👋 Ready to get started?\n\nClick 'Chat with AI' to begin!")
    
    st.markdown("---")
    st.subheader("📋 How It Works")
    
    steps = [
        ("1️⃣", "Tell AI About You", "Share your subjects, exams, and availability"),
        ("2️⃣", "AI Analysis", "Our system analyzes and prioritizes your studies"),
        ("3️⃣", "Get Schedule", "Receive a personalized, realistic timetable"),
        ("4️⃣", "Track Progress", "Monitor your performance and adjust as needed"),
    ]
    
    for step_num, title, desc in steps:
        col1, col2 = st.columns([0.5, 2])
        with col1:
            st.markdown(f"### {step_num}")
        with col2:
            st.markdown(f"**{title}**  \n{desc}")

def show_chat():
    """Chat interface with AI chatbot"""
    st.header("💬 Chat with Your Study Planner")
    
    # Display conversation history
    if st.session_state.conversation_history:
        st.subheader("Conversation History")
        for msg in st.session_state.conversation_history:
            if msg['role'] == 'user':
                st.write(f"**You:** {msg['content']}")
            else:
                st.info(f"**AI:** {msg['content']}")
    
    # Input section
    st.subheader("Ask Me Anything About Your Study Plan")
    
    # Quick prompts
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📚 Tell AI About Subjects"):
            prompt = "I want to tell you about my subjects and exams"
            handle_chat(prompt)
    with col2:
        if st.button("⏱️ Set Available Hours"):
            prompt = "How do I set my available study hours?"
            handle_chat(prompt)
    with col3:
        if st.button("🎯 Create Schedule"):
            prompt = "Can you create my study schedule now?"
            handle_chat(prompt)
    
    # Text input
    user_input = st.text_area("Your message:", height=100, placeholder="Type your question or provide information...")
    
    if st.button("Send", key="send_btn"):
        if user_input.strip():
            handle_chat(user_input)
        else:
            st.warning("Please enter a message!")

def handle_chat(user_message):
    """Handle chat interaction"""
    # Add user message to history
    st.session_state.conversation_history.append({
        'role': 'user',
        'content': user_message
    })
    
    # Get AI response
    ai_response = st.session_state.chatbot.get_response(user_message, st.session_state.user_profile)
    
    # Add AI response to history
    st.session_state.conversation_history.append({
        'role': 'assistant',
        'content': ai_response
    })
    
    st.rerun()

def show_schedule():
    """Display and manage study schedule"""
    st.header("📅 Your Study Schedule")
    
    if not st.session_state.user_profile:
        st.warning("⚠️ Please complete your profile first by chatting with the AI!")
        st.info("Go to 'Chat with AI' tab to get started.")
        return
    
    # Generate schedule if not already generated
    if not st.session_state.generated_schedule:
        st.info("🔄 Generating your personalized schedule...")
        scheduler = ScheduleGenerator(st.session_state.user_profile)
        st.session_state.generated_schedule = scheduler.generate_schedule()
    
    if st.session_state.generated_schedule:
        schedule = st.session_state.generated_schedule
        
        # Display schedule info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Study Period", f"{schedule['start_date']} to {schedule['end_date']}")
        with col2:
            st.metric("Daily Hours", schedule['daily_hours'])
        with col3:
            st.metric("Total Subjects", len(schedule['subjects']))
        
        st.markdown("---")
        
        # Timetable display
        st.subheader("Weekly Timetable")
        
        # Day selector
        selected_day = st.selectbox(
            "Select a day:",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        
        # Display day schedule
        st.markdown(f"### {selected_day}'s Schedule")
        day_schedule = schedule.get('weekly_schedule', {}).get(selected_day, [])
        
        if day_schedule:
            for slot in day_schedule:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.write(f"**{slot['time']}**")
                with col2:
                    st.write(f"{slot['subject']} - {slot['activity']}")
                with col3:
                    if slot['activity'] == 'BREAK':
                        st.markdown("☕")
                    else:
                        st.markdown("✏️")
        
        st.markdown("---")
        
        # Daily goals
        st.subheader("Today's Goals")
        goals = schedule.get('daily_goals', [])
        for goal in goals:
            st.markdown(f"<div class='goal-item'>✓ {goal}</div>", unsafe_allow_html=True)
        
        # Motivational tip
        st.markdown("---")
        st.subheader("💡 Motivational Tip")
        tip = schedule.get('motivational_tip', 'You are doing great! Keep it up! 🌟')
        st.markdown(f"<div class='motivational-tip'>{tip}</div>", unsafe_allow_html=True)
        
        # Options to update
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Regenerate Schedule"):
                st.session_state.generated_schedule = None
                st.rerun()
        with col2:
            if st.button("✏️ Update Profile"):
                st.session_state.current_page = "Settings"
                st.rerun()
        with col3:
            if st.button("📥 Download Schedule"):
                st.success("Schedule downloaded!")

def show_progress():
    """Progress tracking and analytics"""
    st.header("📊 Progress Tracker")
    
    if not st.session_state.user_profile:
        st.warning("⚠️ Please create a schedule first!")
        return
    
    # Progress metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study Completion", "72%", "+5%")
    with col2:
        st.metric("Sessions Completed", "18", "+2")
    with col3:
        st.metric("Total Study Hours", "42.5", "+5.5")
    with col4:
        st.metric("Average Rating", "4.2/5", "+0.3")
    
    st.markdown("---")
    
    # Subject-wise progress
    st.subheader("Subject-wise Progress")
    subjects = st.session_state.user_profile.get('subjects', [])
    
    for subject in subjects:
        progress = 65  # Simulated progress
        st.write(f"**{subject}**")
        st.progress(progress / 100)
    
    st.markdown("---")
    
    # Study time analysis
    st.subheader("Study Time Analysis")
    study_data = {
        'Mon': 5.5, 'Tue': 6, 'Wed': 5, 'Thu': 6.5, 'Fri': 5.5, 'Sat': 4, 'Sun': 3
    }
    st.bar_chart(study_data)
    
    st.markdown("---")
    
    # Exam prep status
    st.subheader("Exam Preparation Status")
    exams = st.session_state.user_profile.get('exams', [])
    
    for exam in exams:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**{exam['subject']}** - {exam['date']}")
        with col2:
            days_left = 15  # Simulated
            st.write(f"📅 {days_left} days left")

def show_settings():
    """Settings and profile management"""
    st.header("⚙️ Settings & Profile")
    
    st.subheader("👤 Your Profile")
    
    with st.form("profile_form"):
        name = st.text_input("Full Name", value=st.session_state.user_profile.get('name', '') if st.session_state.user_profile else "")
        
        st.subheader("Study Details")
        subjects_input = st.text_area(
            "Subjects (comma-separated)",
            value=",".join(st.session_state.user_profile.get('subjects', [])) if st.session_state.user_profile else "",
            height=100
        )
        
        daily_hours = st.slider("Available Study Hours per Day", 1, 12, 5)
        
        preferred_time = st.selectbox(
            "Preferred Study Time",
            ["Early Morning (5-7 AM)", "Morning (7-10 AM)", "Afternoon (12-3 PM)", "Evening (4-6 PM)", "Night (7-10 PM)"]
        )
        
        st.subheader("Exams")
        num_exams = st.number_input("Number of Exams", 1, 10, 1)
        
        exams = []
        for i in range(int(num_exams)):
            col1, col2 = st.columns(2)
            with col1:
                exam_subject = st.text_input(f"Exam {i+1} Subject", key=f"exam_subject_{i}")
            with col2:
                exam_date = st.date_input(f"Exam {i+1} Date", key=f"exam_date_{i}")
            exams.append({'subject': exam_subject, 'date': str(exam_date)})
        
        st.subheader("Difficult Subjects")
        difficult_subjects = st.multiselect(
            "Select your difficult subjects",
            subjects_input.split(',') if subjects_input else []
        )
        
        if st.form_submit_button("💾 Save Profile"):
            st.session_state.user_profile = {
                'name': name,
                'subjects': [s.strip() for s in subjects_input.split(',') if s.strip()],
                'daily_hours': daily_hours,
                'preferred_time': preferred_time,
                'exams': exams,
                'difficult_subjects': difficult_subjects
            }
            st.success("✅ Profile saved successfully!")
            st.rerun()

if __name__ == "__main__":
    main()
