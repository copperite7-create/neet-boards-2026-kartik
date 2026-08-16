# NEET Roadmap 2026-27

A personalized 120-day study roadmap web app for Class 12 Biology students preparing for CBSE Boards and NEET.

## Features
- Daily checklist-based study schedule
- 7-phase structured roadmap (Foundation → Syllabus → Revision → Boards → NEET → Final Prep)
- Subject-wise progress tracking (Biology, Chemistry, Physics, English)
- Interactive calendar view
- Progress dashboard with charts
- Notes for each task
- Mobile-responsive design
- Dark theme with phase color coding

## Quick Start (Local)

1. Clone or download this folder.
2. Open a terminal/PowerShell in this directory.
3. Create the virtual environment:
   ```bash
   py -m venv venv
   ```
4. Activate it:
   ```bash
   venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the app:
   ```bash
   python app.py
   ```
7. Open http://127.0.0.1:5000 in your browser.

## Deploy to Render / Railway (Free)

1. Push this folder to a GitHub repo.
2. Create a new Web Service on [Render.com](https://render.com) or [Railway.app](https://railway.app).
3. Connect your repo.
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `python app.py`
6. Deploy! You get a public URL he can access on his phone.

## Structure
```
neet_roadmap/
├── app.py              # Flask backend with all 576 daily tasks
├── requirements.txt    # Python dependencies
├── runtime.txt         # Python version
├── Procfile            # For Heroku/Render
├── templates/
│   ├── index.html      # Dashboard
│   ├── day.html        # Daily view
│   ├── calendar.html   # 120-day calendar
│   └── progress.html   # Progress tracker
└── static/
    └── css/
        └── style.css   # All styling (dark gradient theme)
```

## Daily Workflow
1. Open the app each morning.
2. Click checkboxes as you complete each task.
3. Add notes if you struggle with a concept.
4. Check the progress page weekly to stay motivated.
