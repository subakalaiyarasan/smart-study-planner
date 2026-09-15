from datetime import datetime, timedelta
from typing import Dict, List
import math

class ScheduleGenerator:
    """Generate personalized study schedules"""
    
    BREAK_DURATION = 5  # minutes
    SESSION_DURATION = 50  # minutes
    EXTENDED_BREAK = 15  # minutes
    MEAL_BREAK = 60  # minutes
    
    def __init__(self, user_profile: Dict):
        self.profile = user_profile
        self.subjects = profile.get('subjects', [])
        self.daily_hours = profile.get('daily_hours', 5)
        self.exams = profile.get('exams', [])
        self.difficult_subjects = profile.get('difficult_subjects', [])
        self.easy_subjects = profile.get('easy_subjects', [])
        self.preferred_time = profile.get('preferred_time', 'Morning (7-10 AM)')
        self.commitments = profile.get('commitments', [])
    
    def generate_schedule(self) -> Dict:
        """Generate complete study schedule"""
        schedule = {
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
            'daily_hours': self.daily_hours,
            'subjects': self.subjects,
            'weekly_schedule': self._generate_weekly_schedule(),
            'daily_goals': self._generate_daily_goals(),
            'motivational_tip': self._get_motivational_tip(),
            'exam_schedule': self._prepare_exam_schedule(),
            'revision_plan': self._create_revision_plan(),
            'subject_analysis': self._analyze_subjects()
        }
        return schedule
    
    def _generate_weekly_schedule(self) -> Dict:
        """Generate weekly timetable"""
        weekly_schedule = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Calculate priority scores
        priorities = self._calculate_priorities()
        
        for day in days:
            # Adjust for weekends
            daily_hours = self.daily_hours if day not in ["Saturday", "Sunday"] else self.daily_hours * 0.7
            
            # Generate time slots
            slots = self._generate_daily_slots(day, daily_hours, priorities)
            weekly_schedule[day] = slots
        
        return weekly_schedule
    
    def _generate_daily_slots(self, day: str, hours: float, priorities: Dict) -> List[Dict]:
        """Generate study slots for a day"""
        slots = []
        
        # Start time based on preference
        if 'Early Morning' in self.preferred_time:
            start_hour = 5
        elif 'Morning' in self.preferred_time:
            start_hour = 7
        elif 'Afternoon' in self.preferred_time:
            start_hour = 12
        elif 'Evening' in self.preferred_time:
            start_hour = 16
        else:  # Night
            start_hour = 19
        
        current_time = start_hour
        minutes_allocated = int(hours * 60)
        subject_index = 0
        
        while minutes_allocated > 0 and current_time < 23:
            # Get current subject based on priority
            sorted_subjects = sorted(self.subjects, key=lambda s: priorities.get(s, 50), reverse=True)
            subject = sorted_subjects[subject_index % len(sorted_subjects)]
            
            # Determine activity type
            if subject in self.difficult_subjects:
                activity = "🔴 Difficult Topics - Focus & Practice"
            elif subject in self.easy_subjects:
                activity = "🟢 Revision & Quick Review"
            else:
                activity = "🟡 Regular Study"
            
            # Allocate study session
            session_mins = min(self.SESSION_DURATION, minutes_allocated)
            end_time = current_time + (session_mins / 60)
            
            # Format time
            start_str = self._format_time(current_time)
            end_str = self._format_time(end_time)
            
            slots.append({
                'time': f"{start_str} - {end_str}",
                'subject': subject,
                'activity': activity,
                'duration': session_mins,
                'priority': priorities.get(subject, 50),
                'type': 'STUDY'
            })
            
            current_time = end_time
            minutes_allocated -= session_mins
            
            # Add break
            if minutes_allocated > 0:
                break_end = current_time + (self.BREAK_DURATION / 60)
                slots.append({
                    'time': f"{self._format_time(current_time)} - {self._format_time(break_end)}",
                    'subject': '☕ BREAK',
                    'activity': 'Rest & Refresh',
                    'duration': self.BREAK_DURATION,
                    'type': 'BREAK'
                })
                current_time = break_end
            
            subject_index += 1
        
        return slots
    
    def _format_time(self, hour: float) -> str:
        """Convert decimal hour to time format"""
        hour_int = int(hour)
        minute_int = int((hour % 1) * 60)
        
        if hour_int < 12:
            period = "AM"
        else:
            period = "PM"
            if hour_int > 12:
                hour_int -= 12
        
        return f"{hour_int}:{minute_int:02d} {period}"
    
    def _calculate_priorities(self) -> Dict:
        """Calculate priority score for each subject"""
        priorities = {}
        today = datetime.now()
        
        for subject in self.subjects:
            score = 50  # Base score
            
            # Increase if difficult
            if subject in self.difficult_subjects:
                score += 30
            
            # Decrease if easy
            if subject in self.easy_subjects:
                score -= 10
            
            # Adjust based on exam date
            for exam in self.exams:
                if exam['subject'] == subject:
                    try:
                        exam_date = datetime.strptime(exam['date'], '%Y-%m-%d')
                        days_until = (exam_date - today).days
                        
                        if days_until <= 7:
                            score += 40
                        elif days_until <= 14:
                            score += 30
                        elif days_until <= 30:
                            score += 20
                        elif days_until > 60:
                            score -= 10
                    except:
                        pass
            
            priorities[subject] = min(max(score, 10), 100)
        
        return priorities
    
    def _generate_daily_goals(self) -> List[str]:
        """Generate daily study goals"""
        goals = [
            "✓ Complete 2 sessions of difficult topics",
            "✓ Solve 15-20 practice problems",
            "✓ Review previous day's notes",
            "✓ Attempt 1-2 practice test questions",
            "✓ Identify and focus on weak areas",
            "✓ Take short breaks every 45 minutes",
            "✓ Complete all scheduled subjects",
            "✓ Update study progress journal"
        ]
        return goals
    
    def _prepare_exam_schedule(self) -> List[Dict]:
        """Prepare exam-wise study schedule"""
        exam_schedule = []
        today = datetime.now()
        
        for exam in self.exams:
            try:
                exam_date = datetime.strptime(exam['date'], '%Y-%m-%d')
                days_until = (exam_date - today).days
                
                # Determine prep intensity
                if days_until <= 7:
                    intensity = "🔴 CRITICAL - Intensive Revision"
                elif days_until <= 14:
                    intensity = "🟠 HIGH - Focus on Problem Areas"
                elif days_until <= 30:
                    intensity = "🟡 MEDIUM - Regular Study & Practice"
                else:
                    intensity = "🟢 LOW - Build Strong Foundation"
                
                exam_schedule.append({
                    'subject': exam['subject'],
                    'date': exam['date'],
                    'days_until': days_until,
                    'prep_intensity': intensity,
                    'weeks_left': days_until // 7,
                    'status': 'UPCOMING' if days_until > 0 else 'COMPLETED'
                })
            except:
                pass
        
        # Sort by days until exam
        exam_schedule.sort(key=lambda x: x['days_until'])
        return exam_schedule
    
    def _create_revision_plan(self) -> Dict:
        """Create revision schedule"""
        return {
            'week_1': 'Foundation building - Learn concepts',
            'week_2_4': 'Practice problems - Apply concepts',
            'week_5_6': 'Revision and consolidation',
            'day_7_before': 'First full revision',
            'day_3_before': 'Subject-wise mock tests',
            'day_1_before': 'Final revision - Focus on important topics',
            'tips': [
                'Use spaced repetition for better retention',
                'Practice previous year papers 2 weeks before exam',
                'Attempt mock tests in exam conditions',
                'Identify weak topics and focus extra',
                'Get 7-8 hours sleep before exam day'
            ]
        }
    
    def _analyze_subjects(self) -> Dict:
        """Analyze each subject in detail"""
        analysis = {}
        priorities = self._calculate_priorities()
        
        for subject in self.subjects:
            difficulty = "🔴 DIFFICULT" if subject in self.difficult_subjects else "🟢 EASY" if subject in self.easy_subjects else "🟡 MODERATE"
            
            # Find exam date
            exam_date = "TBD"
            for exam in self.exams:
                if exam['subject'] == subject:
                    exam_date = exam['date']
            
            analysis[subject] = {
                'priority_score': priorities.get(subject, 50),
                'difficulty': difficulty,
                'exam_date': exam_date,
                'recommended_hours': self._calculate_subject_hours(subject, priorities),
                'study_strategy': self._get_study_strategy(subject),
                'resources': self._get_resources(subject)
            }
        
        return analysis
    
    def _calculate_subject_hours(self, subject: str, priorities: Dict) -> float:
        """Calculate recommended hours per week for subject"""
        total_priority = sum(priorities.values())
        subject_priority = priorities.get(subject, 50)
        
        hours_per_week = (subject_priority / total_priority) * (self.daily_hours * 6)  # 6 study days
        return round(hours_per_week, 1)
    
    def _get_study_strategy(self, subject: str) -> List[str]:
        """Get recommended study strategy for subject"""
        if subject in self.difficult_subjects:
            return [
                "1. Start with fundamentals - Don't skip basics",
                "2. Watch video explanations for complex topics",
                "3. Practice problems daily - 20-30 problems minimum",
                "4. Group study with friends - Discuss doubts",
                "5. Create concept maps and flowcharts",
                "6. Solve mock tests in exam format"
            ]
        elif subject in self.easy_subjects:
            return [
                "1. Quick concept review - Refresh your memory",
                "2. Solve problems for speed and accuracy",
                "3. Attempt previous year papers",
                "4. Focus on tricky variations",
                "5. Help peers - Teaching reinforces learning"
            ]
        else:
            return [
                "1. Read and understand concepts thoroughly",
                "2. Make notes and summaries",
                "3. Practice 15-20 problems daily",
                "4. Revise weekly",
                "5. Solve topic-wise tests"
            ]
    
    def _get_resources(self, subject: str) -> List[str]:
        """Get recommended study resources"""
        return [
            "📚 Textbooks - Official curriculum",
            "📹 YouTube - Topic explanations",
            "📝 Previous Year Papers - Exam patterns",
            "💻 Online Quiz Platforms - Self-assessment",
            "👥 Study Groups - Peer learning",
            "🎓 Tutoring - Expert guidance if needed"
        ]
    
    def _get_motivational_tip(self) -> str:
        """Get motivational tip"""
        tips = [
            "🌟 Every hour of focused study brings you 2 hours closer to your goals! Consistency is your superpower! 💪",
            "💪 These difficult subjects? They're sharpening your mind! You'll emerge as a master after this journey! 🚀",
            "📚 Success is not about studying harder—it's about studying SMARTER. You've got the right plan! ✨",
            "🎯 Small progress daily = BIG results monthly. Celebrate every completed session! 🎉",
            "✨ Your future self will be grateful for every hour you invest today. You're building your success! 🏆",
            "🚀 These exams are just checkpoints, not your destination. Focus on learning, not just passing! 🧠",
            "💯 You have what it takes! Believe in yourself, trust your plan, and ace these exams! 🎓",
            "🧠 Your brain is POWERFUL! Feed it with focused study, healthy food, and good sleep. You've got this! 😎"
        ]
        
        import random
        return random.choice(tips)
