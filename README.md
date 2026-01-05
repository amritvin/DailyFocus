# 🎯 Habit & Routine Tracker
A modern, feature-rich Flask web application for tracking daily habits, routines, and journaling with a beautiful glassmorphism UI. Built with mobile-first design principles for seamless use across all devices.
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
## ✨ Features
### 📊 Dashboard
- **Live Scoring System**: Real-time completion percentage with customizable targets
- **5-Day Week View**: Quick navigation with sliding window centered on current date
- **Smart Sorting**: Completed routines automatically move to the top
- **Digital Clock**: Always-visible time display
- **Reminders**: Daily reminders with quick-add functionality
### 📝 Journaling
- **Auto-Save**: Entries save automatically as you type (1-second debounce)
- **Pinned Thoughts**: Highlight important daily focuses
- **Multi-Photo Albums**: Drag-and-drop photo uploads with instant processing
- **Photo Management**: Delete unwanted photos with confirmation
### 📸 Gallery & Timeline
- **Visual Gallery**: Grid view of all your photo memories
- **Timeline View**: Chronological journey grouped by month and year
- **Album Display**: Multiple photos per day with thumbnail previews
### 📈 Analytics
- **Top Routines**: Bar chart of your most completed habits
- **Journaling Streak**: 7-day activity visualization
- **Category Distribution**: Pie chart showing habit focus areas
### ⚙️ Settings
- **Routine Management**: Add, edit, and delete routine items
- **Flexible Scheduling**: Separate weekday and weekend routines
- **Target Score**: Customize your daily completion goals
## 🚀 Quick Start
### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
### Installation
1. **Clone the repository**
```bash
git clone <your-repo-url>
cd habit_tracker
```
2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Initialize the database**
The database will be created automatically on first run. To seed with your custom routines:
```bash
python seed_data.py
```
4. **Run the application**
```bash
python app.py
```
5. **Access the app**
- Local: `http://localhost:5000`
- Network: `http://<your-ip>:5000` (for mobile access on same network)
### Database Setup
**Important**: The database file (`habit_tracker.db`) is **not** included in the repository. It will be created automatically when you first run the application.
The app uses SQLite with the following models:
- `RoutineItem`: Your daily habits and routines
- `TrackerLog`: Completion history for each routine
- `DiaryEntry`: Journal entries with text content
- `DiaryImage`: Photos linked to diary entries
- `Reminder`: Daily reminders and notes
- `UserSetting`: App preferences (e.g., target score)
To start fresh or reset your data, simply delete `habit_tracker.db` and restart the app.
## 📱 Mobile Access
To access from your phone/tablet on the same WiFi network:
1. Find your computer's local IP address:
   - **Windows**: `ipconfig` (look for IPv4 Address)
   - **Mac/Linux**: `ifconfig` or `ip addr`
2. On your mobile device, navigate to:
   ```
   http://<your-ip>:5000
   ```
3. Add to home screen for app-like experience!
## 🎨 Customization
### Modify Your Routines
Edit `seed_data.py` to customize your weekday and weekend routines, then run:
```bash
python seed_data.py
```
### Change Target Score
Navigate to Settings → Target Routine Completion Score
### Styling
All CSS is in `static/css/style.css` with CSS variables for easy theming:
```css
:root {
    --primary: #4F46E5;
    --secondary: #ec4899;
    --success: #10b981;
    /* ... */
}
```
## 📂 Project Structure
```
habit_tracker/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── seed_data.py           # Initial data seeding script
├── verify.py              # Verification script
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Styling with glassmorphism
│   └── uploads/          # User-uploaded photos
└── templates/
    ├── base.html         # Base template with navigation
    ├── index.html        # Dashboard
    ├── diary.html        # Journaling interface
    ├── gallery.html      # Photo gallery
    ├── timeline.html     # Timeline view
    ├── analytics.html    # Analytics dashboard
    ├── settings.html     # Settings page
    └── timetable.html    # Full routine schedule
```
## 🔮 Future Development Roadmap
### Phase 10: Advanced Features
- [ ] **Habit Streaks**: Track consecutive days of completion
- [ ] **Weekly/Monthly Reports**: Downloadable PDF summaries
- [ ] **Data Export**: JSON/CSV export for backup
- [ ] **Dark/Light Mode Toggle**: User-selectable themes
- [ ] **Notifications**: Browser notifications for reminders
### Phase 11: Multi-User & Social Platform
**Vision: "Jellyfin for Habits" - Self-hosted wellness server for families and organizations**
- [ ] **User Profiles & Authentication**: Individual accounts with login/logout
- [ ] **Family Mode**: Separate profiles with shared household routines
- [ ] **Privacy Controls**: Choose what to share with family members
- [ ] **Social Feed**: Activity timeline (opt-in sharing)
- [ ] **Community Challenges**: Group goals and competitions
- [ ] **Leaderboards**: Weekly/monthly rankings (privacy-respecting)
- [ ] **Templates**: Pre-built routine templates for common goals
- [ ] **Sharing**: Share achievements, journal entries, or progress
### Phase 12: Intelligence & Analytics
- [ ] **AI Insights**: Pattern recognition in your habits
- [ ] **Smart Suggestions**: Recommended routines based on goals
- [ ] **Predictive Analytics**: Forecast completion trends
- [ ] **Correlation Discovery**: Find connections between habits and outcomes
- [ ] **Natural Language Input**: "Remind me to exercise tomorrow"
- [ ] **Anomaly Detection**: Alert unusual patterns (health, mood, etc.)
### Phase 13: Integration & Sync
- [ ] **Google Fit Integration**: Sync sleep, heart rate, exercise data
- [ ] **Fitness Trackers**: Import from smartwatches and wearables
- [ ] **Calendar Sync**: Google Calendar, Outlook integration
- [ ] **API**: RESTful API for third-party integrations
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Voice Commands**: Alexa/Google Assistant integration
- [ ] **Webhooks**: Real-time notifications to other services
### Phase 14: Gamification
- [ ] **Achievements & Badges**: Unlock rewards for milestones
- [ ] **Points System**: Earn points for consistency
- [ ] **Custom Rewards**: Set personal rewards for goals
- [ ] **Team Battles**: Compete with friends or family
- [ ] **Streak Challenges**: Longest streak competitions
### Phase 15: Advanced Journaling
- [ ] **Rich Text Editor**: Markdown support, formatting
- [ ] **Voice Journaling**: Audio recording and transcription
- [ ] **Mood Tracking**: Daily mood logging with trends
- [ ] **Tags & Search**: Organize and find entries easily
- [ ] **Journal Templates**: Gratitude, reflection prompts
### Phase 16: Professional Health Platform
**Vision: Connect clients with coaches, dietitians, and healthcare providers**
#### Professional Roles:
- [ ] **Gym Coach/Personal Trainer Accounts**: Client management dashboard
- [ ] **Dietitian/Nutritionist Accounts**: Meal tracking and nutrition oversight
- [ ] **Doctor/Healthcare Provider Accounts**: Patient health monitoring
- [ ] **Wellness Coach Accounts**: Holistic lifestyle management
#### Professional Features:
- [ ] **Client Assignment System**: Professionals can manage multiple clients
- [ ] **Role-Based Dashboards**: Custom views for each professional type
- [ ] **Progress Monitoring**: Track client metrics over time
- [ ] **In-App Messaging**: Secure communication between clients and professionals
- [ ] **Appointment Scheduling**: Book sessions and consultations
- [ ] **Custom Program Builder**: Create personalized plans for clients
- [ ] **Professional Reports**: Generate client progress reports
### Phase 17: Food & Nutrition Tracking
- [ ] **Meal Photo Logging**: Snap photos of every meal
- [ ] **Food Diary**: Track breakfast, lunch, dinner, snacks
- [ ] **Dietitian Review Interface**: Professionals can review and annotate meal photos
- [ ] **Nutrition Estimation**: Calorie and macro tracking
- [ ] **Meal Plan Builder**: Create and share custom meal plans
- [ ] **Recipe Library**: Healthy recipe database
- [ ] **Hydration Tracking**: Water intake monitoring
### Phase 18: Advanced Fitness Tracking
- [ ] **Workout Logging**: Sets, reps, weight tracking
- [ ] **Exercise Video Recording**: Record form for coach review
- [ ] **Progress Photos**: Weekly body composition tracking
- [ ] **Body Measurements**: Track physical changes
- [ ] **Workout Builder**: Coaches create custom programs
- [ ] **Form Analysis**: Video playback with professional annotations
- [ ] **Progressive Overload**: Auto-adjust weights based on performance
### Phase 19: Health Monitoring
- [ ] **Vital Signs Tracking**: Heart rate, blood pressure, temperature
- [ ] **Symptoms Log**: Daily health check-ins
- [ ] **Medication Tracker**: Reminders and adherence monitoring
- [ ] **Sleep Quality**: Duration and quality ratings
- [ ] **Lab Results Integration**: Import and track medical tests
- [ ] **Doctor Dashboard**: Patient health timeline and alerts
- [ ] **HIPAA Compliance**: Healthcare data security standards
### Phase 20: Enterprise & Organizations
**Vision: Scalable platform for colleges, gyms, and corporate wellness**
- [ ] **Organization Accounts**: Manage departments, teams, or groups
- [ ] **SSO Integration**: Single Sign-On for enterprises
- [ ] **Admin Controls**: Organization-level permissions and moderation
- [ ] **White-Label Option**: Custom branding for organizations
- [ ] **Bulk User Management**: Import/export users
- [ ] **Usage Analytics**: Organization-wide engagement metrics
- [ ] **Custom Integrations**: LMS (Canvas, Blackboard), HR systems
### Phase 21: AI & LLM Integration
**Vision: Intelligent personal health assistant**
#### Conversational AI:
- [ ] **Chat Interface**: Natural language conversations about your health
- [ ] **Voice Commands**: "Hey Habit, log my breakfast"
- [ ] **Smart Reminders**: Context-aware notifications
- [ ] **Motivational Coaching**: Personalized encouragement
#### Computer Vision:
- [ ] **Food Recognition**: Identify foods from photos automatically
- [ ] **Nutrition Estimation**: AI-powered calorie and macro calculation
- [ ] **Exercise Form Analysis**: Review workout videos, suggest corrections
- [ ] **Progress Photo Comparison**: Track body composition changes
#### Intelligent Insights:
- [ ] **Pattern Recognition**: "Your sleep quality drops when you eat late"
- [ ] **Habit Stacking**: Suggest optimal habit combinations
- [ ] **Trend Prediction**: "At this rate, you'll hit your goal in 6 weeks"
- [ ] **Anomaly Detection**: Alert unusual health patterns
- [ ] **Correlation Discovery**: Find connections between behaviors
#### Professional AI Assistants:
- [ ] **Coach AI**: Auto-generate workout programs
- [ ] **Dietitian AI**: Create meal plans, suggest substitutions
- [ ] **Doctor AI**: Symptom analysis and risk stratification
- [ ] **Auto-Reports**: Generate client summaries and progress reports
#### Privacy Options:
- [ ] **Local LLM**: Self-hosted AI for complete privacy
- [ ] **Cloud LLM**: Powerful cloud-based AI (opt-in)
- [ ] **Hybrid Mode**: Balance privacy and performance
### Phase 22: Social Media Platform
**Vision: Instagram/Strava for holistic wellness**
- [ ] **Public Profiles**: Opt-in profile sharing
- [ ] **Follow System**: Connect with friends and teammates
- [ ] **Activity Feed**: See friends' achievements and progress
- [ ] **Likes & Comments**: Engage with community
- [ ] **Challenge Creation**: Create and share custom challenges
- [ ] **Viral Features**: "30-day transformation" stories
- [ ] **Campus-Wide Challenges**: University or organization competitions
- [ ] **Team Battles**: Dorm vs. Dorm, Department vs. Department
## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
## 🙏 Acknowledgments
- Built with [Flask](https://flask.palletsprojects.com/)
- Charts powered by [Chart.js](https://www.chartjs.org/)
- Design inspired by modern glassmorphism trends
## 📞 Support
For issues, questions, or suggestions, please open an issue on GitHub.
---
**Made with ❤️ for building better habits, one day at a time.**
