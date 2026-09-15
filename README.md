# Smart Study Planner 📚

An AI-powered chatbot that creates personalized study timetables for students. This intelligent system analyzes your subjects, exam dates, available study hours, and learning preferences to generate realistic, optimized study schedules.

## 🌟 Features

### Core Functionality
- **Personalized Study Schedules**: Creates custom timetables based on your specific needs
- **Subject Priority Analysis**: Automatically prioritizes difficult subjects
- **Exam Tracking**: Manages multiple exam dates and deadlines
- **Adaptive Scheduling**: Adjusts timetables based on your performance and feedback
- **Progress Monitoring**: Tracks study sessions, completion, and performance metrics

### Study Planning
- 📅 Dynamic time slot allocation
- 🎯 Subject-wise study sessions
- ⏱️ Optimized break intervals
- 📝 Revision and practice test scheduling
- 🔄 Daily goal setting and tracking
- 💪 Motivational tips and encouragement

### User Management
- ✏️ Update study details anytime
- 🔧 Adjust timetables on-the-fly
- 📊 View study analytics and progress
- 🎓 Customize difficulty levels and preferences

## 📋 Information Collected

The chatbot gathers the following details:

1. **Subjects**: List of subjects to study
2. **Exam Dates**: When each exam is scheduled
3. **Available Study Hours**: Daily hours available for studying
4. **Preferred Study Time**: Morning, afternoon, or evening preferences
5. **Difficult Subjects**: Topics that need extra attention
6. **Daily Commitments**: Classes, work, or other commitments
7. **Learning Style**: Visual, auditory, or kinesthetic preferences
8. **Target Grades**: Goals for each subject

## 🎯 How It Works

### 1. **Initial Setup**
- Chat with the AI to provide your study information
- Answer questions about your subjects, exams, and schedule

### 2. **Analysis & Planning**
- AI analyzes your input data
- Prioritizes difficult subjects and upcoming exams
- Calculates optimal study distribution

### 3. **Schedule Generation**
- Creates realistic study timetable
- Includes study sessions, breaks, and revision
- Adds practice tests before exams

### 4. **Active Learning**
- Follow your personalized schedule
- Track daily progress and goals
- Receive motivational tips

### 5. **Continuous Improvement**
- Update your details as needed
- Adjust timetable based on performance
- Get recommendations for better learning

## 💻 Technology Stack

- **Backend**: Python (Flask/FastAPI)
- **AI/ML**: OpenAI GPT, Natural Language Processing
- **Database**: PostgreSQL/MongoDB
- **Frontend**: React.js / Streamlit
- **Scheduling Algorithm**: Custom optimization engine

## 🚀 Quick Start

### Prerequisites
```bash
- Python 3.8+
- Node.js 14+ (for frontend)
- PostgreSQL or MongoDB
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/subakalaiyarasan/smart-study-planner.git
cd smart-study-planner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Add your API keys and database configuration
```

4. Run the application:
```bash
python app.py
# or
streamlit run app.py
```

5. Access the chatbot at `http://localhost:5000`

## 📱 Sample Interaction

**User**: "I need help creating a study schedule"

**Chatbot**: "Great! I'm here to help. Let me gather some information about your studies. How many subjects are you currently studying?"

**User**: "I'm studying 5 subjects: Math, Physics, Chemistry, Biology, and English"

**Chatbot**: "Perfect! Now, when are your exams? Please provide the subjects and their exam dates."

**User**: "Math on Dec 15, Physics on Dec 18, Chemistry on Dec 20, Biology on Dec 22, and English on Dec 25"

**Chatbot**: "How many hours per day can you dedicate to studying?"

**User**: "About 5-6 hours"

**Chatbot**: "Which subjects do you find most challenging?"

**User**: "Physics and Chemistry are quite tough for me"

**Chatbot**: "I understand. Let me create an optimized schedule for you that prioritizes Physics and Chemistry while preparing for all your exams..."

## 📊 Generated Timetable Example

```
PERSONALIZED STUDY TIMETABLE
Generated for: John Doe
Study Period: Nov 15 - Dec 25, 2024

MONDAY
6:00 AM - 6:30 AM  | Morning Review (Previous day revision)
6:30 AM - 7:30 AM  | Physics (Priority Subject) - Difficult topics
7:30 AM - 8:00 AM  | BREAK
8:00 AM - 9:00 AM  | Math (Problem Solving)
9:00 AM - 10:00 AM | Chemistry (Theory & Practicals)
10:00 AM - 11:00 AM| LUNCH BREAK
11:00 AM - 12:00 PM| Biology (Revision)
12:00 PM - 1:00 PM | English (Reading & Writing)
1:00 PM - 2:00 PM  | BREAK
2:00 PM - 3:00 PM  | Physics (Practice Problems)
3:00 PM - 4:00 PM  | Chemistry (Revision)
4:00 PM - 4:30 PM  | SNACK BREAK
4:30 PM - 5:30 PM  | Physics (Mock Test)

DAILY GOALS:
✓ Complete 2 units of Physics
✓ Solve 10 Math problems
✓ Review Chemistry formulas
✓ Read 1 chapter in Biology
✓ Write 2 essays in English

MOTIVATIONAL TIP:
"Every hour of focused study brings you closer to your goals! 
Physics might be challenging, but consistent practice will make 
you a master of it. You've got this! 💪"
```

## 🎯 Key Algorithms

### Priority Scoring Algorithm
```
Priority = (Difficulty Level × 0.4) + (Days Until Exam × 0.4) + (Current Progress × 0.2)
```

### Time Distribution Formula
```
Time for Subject = (Available Hours × Priority Score) / Total Priority Score
```

### Break Optimization
- Pomodoro technique (25 min study + 5 min break)
- Extended breaks every 2 hours
- Longer breaks for meal times

## 📈 Features Coming Soon

- [ ] AI-powered study recommendations
- [ ] Video integration for difficult topics
- [ ] Peer study group matching
- [ ] Performance analytics dashboard
- [ ] Mobile app (iOS & Android)
- [ ] Offline mode support
- [ ] Integration with popular study platforms
- [ ] Parent/Guardian notifications
- [ ] AI tutoring sessions

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@smartstudyplanner.com or open an issue in the GitHub repository.

## 👨‍💻 Author

Created by [subakalaiyarasan](https://github.com/subakalaiyarasan)

## 🙏 Acknowledgments

- OpenAI for GPT models
- Education research and study science community
- All contributors and users

---

**Happy Studying! 📖✨**
