import os
from datetime import datetime, timedelta
import json
from typing import Optional, Dict, List

class StudyPlannerChatbot:
    """AI Chatbot for creating personalized study plans"""
    
    def __init__(self):
        self.conversation_state = {}
        self.required_info = [
            'class_degree',
            'year',
            'subjects',
            'exams',
            'daily_hours',
            'preferred_time',
            'difficult_subjects',
            'easy_subjects',
            'commitments'
        ]
        self.collected_info = {}
        self.conversation_stage = 0
    
    def get_response(self, user_message: str, user_profile: Optional[Dict]) -> str:
        """Generate AI response based on user input"""
        
        user_message_lower = user_message.lower()
        
        # Greeting
        if any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'start', 'begin']):
            return self._greeting_response()
        
        # Class/Degree information
        elif any(word in user_message_lower for word in ['class', 'degree', 'semester', 'year', 'standard']):
            return self._handle_class_degree(user_message)
        
        # Subject information
        elif any(word in user_message_lower for word in ['subject', 'studying', 'study', 'courses', 'classes']):
            return self._handle_subjects(user_message)
        
        # Exam dates
        elif any(word in user_message_lower for word in ['exam', 'test', 'date', 'when', 'scheduled']):
            return self._handle_exams(user_message)
        
        # Days remaining
        elif any(word in user_message_lower for word in ['days', 'remaining', 'left', 'how many days']):
            return self._handle_days_remaining(user_message)
        
        # Available hours
        elif any(word in user_message_lower for word in ['hour', 'time', 'available', 'how much', 'how many']):
            return self._handle_hours(user_message)
        
        # Preferred study time
        elif any(word in user_message_lower for word in ['prefer', 'morning', 'afternoon', 'evening', 'night']):
            return self._handle_preferred_time(user_message)
        
        # Difficult subjects
        elif any(word in user_message_lower for word in ['difficult', 'hard', 'tough', 'struggle', 'challenge']):
            return self._handle_difficult(user_message)
        
        # Easy subjects
        elif any(word in user_message_lower for word in ['easy', 'simple', 'good at', 'strong', 'comfortable']):
            return self._handle_easy_subjects(user_message)
        
        # Commitments
        elif any(word in user_message_lower for word in ['commitment', 'work', 'job', 'class', 'activity', 'sport', 'break']):
            return self._handle_commitments(user_message)
        
        # Generate schedule
        elif any(word in user_message_lower for word in ['create', 'generate', 'make', 'schedule', 'plan', 'timetable', 'analysis']):
            return self._handle_schedule_generation(user_profile)
        
        # Update information
        elif any(word in user_message_lower for word in ['update', 'change', 'modify', 'adjust']):
            return self._handle_update(user_message)
        
        # Help and tips
        elif any(word in user_message_lower for word in ['help', 'how', 'tip', 'advice', 'suggest']):
            return self._provide_help()
        
        else:
            return self._default_response()
    
    def _greeting_response(self) -> str:
        """Handle greeting"""
        return """
🎓 **Welcome to Smart Study Planner!**

I'm your personal AI study companion. I'll help you create a realistic, personalized study timetable that maximizes your exam preparation! 📚

To get started, I need to understand your situation better. Let me collect some important information:

**Here's what we'll cover:**
1. 📚 Your class/degree and year
2. 📖 Subjects you're studying
3. 📅 Exam dates for each subject
4. ⏳ Days remaining until your exams
5. ⏱️ Available study hours per day
6. 🌅 Your preferred study time (morning/afternoon/night)
7. 💪 Difficult vs easy subjects
8. 🎯 Your break times and other commitments

Let's start! **What class/degree are you in, and which year?**
(Example: "I'm in 12th grade" or "I'm a 2nd year engineering student")
        """
    
    def _handle_class_degree(self, message: str) -> str:
        """Handle class/degree information"""
        return """
Great! 🎓 Understanding your academic level helps me tailor the schedule.

Now, **tell me about the subjects you need to study:**
- How many subjects do you have?
- What are their names?

(Example: "I have 5 subjects: Math, Physics, Chemistry, Biology, and English")
        """
    
    def _handle_subjects(self, message: str) -> str:
        """Handle subject information"""
        return """
Perfect! 📚 I've noted your subjects.

Now I need **exam dates for each subject:**
Please provide the dates when each exam is scheduled.

(Example: "Math on December 15, Physics on December 18, Chemistry on December 20")
        """
    
    def _handle_exams(self, message: str) -> str:
        """Handle exam date information"""
        return """
Excellent! 📅 I can see your exam timeline.

Now, tell me **how many days are remaining** until your exams?
This helps me understand the urgency and allocate study time accordingly.

(Example: "Math in 30 days, Physics in 33 days")
        """
    
    def _handle_days_remaining(self, message: str) -> str:
        """Handle days remaining information"""
        return """
Perfect! ⏳ I can now prioritize your subjects based on exam proximity.

Next, **how many hours per day can you dedicate to studying?**
Be realistic - it's better to have an achievable schedule!

(Example: "I can study 5-6 hours daily")
        """
    
    def _handle_hours(self, message: str) -> str:
        """Handle available hours information"""
        return """
Good! ⏱️ I'll create a schedule within those hours.

Now, **what is your preferred study time?**
- 🌅 Early morning (5-7 AM)?
- ☀️ Morning (7-10 AM)?
- 🌤️ Afternoon (12-3 PM)?
- 🌆 Evening (4-6 PM)?
- 🌙 Night (7-10 PM)?

Or a combination? (Example: "I prefer morning and evening sessions")
        """
    
    def _handle_preferred_time(self, message: str) -> str:
        """Handle preferred study time"""
        return """
Great! 🌅 I'll schedule your sessions at your preferred times.

Now, **which subjects are difficult for you?**
These need extra time and focus!

(Example: "Physics and Chemistry are tough for me. I struggle with quantum mechanics and organic reactions.")
        """
    
    def _handle_difficult(self, message: str) -> str:
        """Handle difficult subjects information"""
        return """
I hear you! 💪 I'll allocate more time to these challenging subjects.

Now, **which subjects do you find easy?**
These are your strength areas!

(Example: "English and Biology are easy for me. I enjoy reading and understanding concepts.")
        """
    
    def _handle_easy_subjects(self, message: str) -> str:
        """Handle easy subjects information"""
        return """
Perfect! 🌟 Knowing your strengths helps balance the schedule.

Finally, **tell me about your daily commitments and break times:**
- Do you have classes/work at specific times?
- Any sports, hobbies, or activities?
- How much break time do you need?

(Example: "I have classes from 9 AM to 1 PM, gym at 4 PM for 1 hour, and I need 30 mins for lunch and snacks")
        """
    
    def _handle_commitments(self, message: str) -> str:
        """Handle commitments and breaks"""
        return """
Excellent! 🎯 Now I have all the information I need!

**Your Profile Summary:**
✅ Class/Degree and Year
✅ Subjects and Exam Dates
✅ Days Remaining
✅ Available Study Hours
✅ Preferred Study Time
✅ Difficult and Easy Subjects
✅ Daily Commitments

Let me **analyze your information** and create your personalized study schedule...

🔄 **Analysis Process:**
1. 📊 Calculating priority scores for each subject
2. ⏰ Distributing time based on difficulty and exam dates
3. 🎯 Balancing workload across study hours
4. 📝 Creating realistic daily goals
5. 💪 Adding motivational tips
6. 🔧 Optimizing breaks and sessions

Your schedule is being prepared! 📅

Would you like me to:
1️⃣ **Generate your full schedule** - See the complete timetable
2️⃣ **Show analysis** - See how I prioritized your studies
3️⃣ **Get recommendations** - Receive study tips for difficult subjects
4️⃣ **View exam prep strategy** - See your exam-wise preparation plan
        """
    
    def _handle_schedule_generation(self, user_profile: Optional[Dict]) -> str:
        """Handle schedule generation request"""
        if not user_profile:
            return """
I'd love to create your schedule! 🗓️

To generate your personalized study plan, I need complete information:

**Missing Information:**
- ❓ Your class/degree and year
- ❓ List of subjects
- ❓ Exam dates for each subject
- ❓ Days remaining until exams
- ❓ Daily available study hours
- ❓ Preferred study time
- ❓ Difficult subjects
- ❓ Easy subjects
- ❓ Daily commitments

Please go back and share these details! Start with: 
"I'm in [class/year], studying [subjects]..."
            """
        
        return """
🎉 **PERSONALIZED STUDY PLAN GENERATED!**

Based on your complete profile, I've created an optimized schedule! ✨

**What's Included:**
✅ **Priority Analysis** - Subjects ranked by difficulty & exam dates
✅ **Time Distribution** - Hours allocated to each subject
✅ **Daily Timetable** - Hour-by-hour study schedule
✅ **Revision Plan** - Spacing out revisions effectively
✅ **Practice Tests** - Mock exams before the actual test
✅ **Daily Goals** - Achievable targets for each day
✅ **Break Schedule** - Optimal breaks for productivity
✅ **Motivational Tips** - Daily encouragement
✅ **Exam Prep Strategy** - Subject-specific preparation tips

**Next Steps:**
1. 👉 Go to **"My Schedule"** tab to view your full timetable
2. 📊 Check **"Progress Tracker"** to monitor your journey
3. ⚙️ Use **"Settings"** to update your profile anytime
4. 💬 Come back to chat for study tips and motivation

**Remember:** 
✨ Consistency is key! Follow your schedule and you'll ace those exams! 💪
        """
    
    def _handle_update(self, message: str) -> str:
        """Handle update requests"""
        return """
No problem! 🔄 Your schedule can adapt with you.

What would you like to update?
- 📚 **Subjects** - Add or remove subjects?
- 📅 **Exam Dates** - Exam postponed or rescheduled?
- ⏱️ **Hours** - More or less time available?
- 🌅 **Preferences** - Different study time?
- 💪 **Difficulty** - New challenging topics?
- 🎯 **Commitments** - Schedule changes?

Tell me what changed, and I'll regenerate your schedule! 📋
        """
    
    def _provide_help(self) -> str:
        """Provide helpful tips and advice"""
        return """
📚 **Study Tips & Effective Techniques**

**🎯 PROVEN STUDY METHODS:**

1️⃣ **Pomodoro Technique**
   - Study 25 minutes → 5 minute break
   - After 4 sessions → 15-30 minute break
   - Perfect for focus and preventing burnout!

2️⃣ **Spaced Repetition**
   - Day 1: Learn the concept
   - Day 3: Review and practice
   - Day 7: Full revision
   - Day 30: Final review before exam

3️⃣ **Active Learning**
   - Don't just read! Practice problems
   - Teach concepts to someone else
   - Make flashcards and mind maps
   - Solve previous year question papers

4️⃣ **Chunking**
   - Break large topics into smaller parts
   - Study one chunk at a time
   - Easier to understand and retain

**💪 FOR DIFFICULT SUBJECTS:**
✓ Start with fundamentals first
✓ Watch video explanations
✓ Practice problems regularly
✓ Discuss with teachers/friends
✓ Create visual aids (diagrams, flowcharts)
✓ Take more practice tests

**🌟 STAY MOTIVATED:**
✓ Track daily progress
✓ Celebrate small wins
✓ Study with friends (group study)
✓ Take care of health (sleep, exercise, nutrition)
✓ Maintain a clean study space
✓ Put your phone on silent!

**📝 BEFORE EXAMS:**
✓ Solve previous year papers
✓ Identify question patterns
✓ Practice time management
✓ Review common mistakes
✓ Get good sleep the night before

Which topic would you like more details on? 🤔
        """
    
    def _default_response(self) -> str:
        """Default response for unrecognized input"""
        return """
I'm here to help you ace your exams! 🎓

You can ask me about:
- 📚 Creating your personalized study schedule
- 📅 Managing subjects and exam dates
- 📖 Study tips and effective techniques
- 🔄 Updating your information
- 📊 Tracking your progress
- 💪 Motivation and encouragement

What would you like to do? 🤔

Or just tell me about your studies, and I'll guide you through the process!
        """
    
    def analyze_profile(self, profile: Dict) -> Dict:
        """Analyze user profile for schedule generation"""
        analysis = {
            'class_degree': profile.get('class_degree', ''),
            'year': profile.get('year', ''),
            'subjects_count': len(profile.get('subjects', [])),
            'total_hours': profile.get('daily_hours', 5),
            'exam_count': len(profile.get('exams', [])),
            'difficult_count': len(profile.get('difficult_subjects', [])),
            'easy_count': len(profile.get('easy_subjects', [])),
            'priority_scores': self._calculate_priorities(profile),
            'analysis_summary': self._generate_analysis_summary(profile)
        }
        return analysis
    
    def _calculate_priorities(self, profile: Dict) -> Dict:
        """Calculate study priority for each subject"""
        priorities = {}
        subjects = profile.get('subjects', [])
        difficult = profile.get('difficult_subjects', [])
        easy = profile.get('easy_subjects', [])
        exams = profile.get('exams', [])
        
        today = datetime.now()
        
        for subject in subjects:
            # Base priority
            priority = 50
            
            # Increase if difficult
            if subject in difficult:
                priority += 30
            
            # Decrease if easy
            if subject in easy:
                priority -= 10
            
            # Increase based on exam date proximity
            for exam in exams:
                if exam['subject'] == subject:
                    try:
                        exam_date = datetime.strptime(exam['date'], '%Y-%m-%d')
                        days_until = (exam_date - today).days
                        
                        if days_until <= 7:
                            priority += 40
                        elif days_until <= 14:
                            priority += 30
                        elif days_until <= 30:
                            priority += 20
                        elif days_until > 60:
                            priority -= 10
                    except:
                        pass
            
            priorities[subject] = min(max(priority, 10), 100)  # Keep between 10-100
        
        return priorities
    
    def _generate_analysis_summary(self, profile: Dict) -> str:
        """Generate analysis summary"""
        priorities = self._calculate_priorities(profile)
        sorted_subjects = sorted(priorities.items(), key=lambda x: x[1], reverse=True)
        
        summary = "**ANALYSIS SUMMARY:**\n\n"
        summary += f"Class/Degree: {profile.get('class_degree', 'N/A')} - {profile.get('year', 'N/A')}\n\n"
        
        summary += "**Subject Priority Ranking:**\n"
        for i, (subject, score) in enumerate(sorted_subjects, 1):
            emoji = "🔴" if score >= 80 else "🟡" if score >= 60 else "🟢"
            summary += f"{i}. {emoji} {subject} (Priority: {score}/100)\n"
        
        summary += f"\n**Study Allocation:**\n"
        summary += f"- Total Daily Hours: {profile.get('daily_hours')} hours\n"
        summary += f"- Preferred Time: {profile.get('preferred_time', 'N/A')}\n"
        summary += f"- Difficult Subjects: {', '.join(profile.get('difficult_subjects', []))}\n"
        summary += f"- Strong Subjects: {', '.join(profile.get('easy_subjects', []))}\n"
        
        return summary
