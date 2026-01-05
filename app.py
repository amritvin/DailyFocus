import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from models import db, RoutineItem, TrackerLog, DiaryEntry, Reminder, DiaryImage, UserSetting

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habit_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def dashboard():
    # handling date query param
    date_str = request.args.get('date')
    if date_str:
        try:
            current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            current_date = date.today()
    else:
        current_date = date.today()

    day_name = current_date.strftime("%A") # e.g., Monday
    
    # Determine routine type (Weekend or Weekday)
    # Simple logic: Sat/Sun = Weekend, else Weekday
    if day_name in ['Saturday', 'Sunday']:
        routine_filter = 'Weekend'
    else:
        routine_filter = 'Weekday'

    # Calculate 5-Day Sliding Window for Navigation (Current -2 to +2)
    # This ensures no scrolling is needed and focuses on immediate context
    start_date = current_date - timedelta(days=2)
    week_dates = []
    for i in range(5):
        d = start_date + timedelta(days=i)
        week_dates.append({
            'date': d,
            'day_name': d.strftime('%a'), # Mon
            'day_num': d.strftime('%d'), # 05
            'is_current': (d == current_date)
        })

    # Fetch routine items for the specific day type
    items = RoutineItem.query.filter_by(routine_type=routine_filter).all()

    # Fetch logs for the current_date to see what's completed
    logs = TrackerLog.query.filter_by(date=current_date).all()
    completed_ids = {log.routine_item_id for log in logs if log.status}

    def parse_time(t_str):
        try:
            return datetime.strptime(t_str, "%I:%M %p")
        except:
            return datetime.min # Fallback

    def get_sort_key(item):
        is_completed = item.id in completed_ids
        # Primary: Completed First (0), Incomplete Second (1)
        # Secondary: Time
        return (0 if is_completed else 1, parse_time(item.time_start))
            
    items.sort(key=get_sort_key)
    
    # Fetch diary entry if exists for current_date
    diary_entry = DiaryEntry.query.filter_by(date=current_date).first()
    pinned_text = diary_entry.pinned_text if diary_entry else None

    # Fetch reminders for current_date
    reminders = Reminder.query.filter_by(date=current_date).all()

    # Calculate Score
    total_habits = len(items)
    completed_habits = len(completed_ids)
    score = int((completed_habits / total_habits * 100)) if total_habits > 0 else 0
    
    # Get Target Score
    target_setting = UserSetting.query.filter_by(key='target_score').first()
    target_score = int(target_setting.value) if target_setting else 80

    return render_template('index.html', 
                           routine_items=items, 
                           completed_ids=completed_ids, 
                           current_date=current_date,
                           week_dates=week_dates,
                           day_name=day_name,
                           pinned=pinned_text,
                           reminders=reminders,
                           score=score,
                           target_score=target_score)



@app.route('/settings/add', methods=['POST'])
def add_routine():
    name = request.form.get('name')
    time_start = request.form.get('time_start')
    routine_type = request.form.get('routine_type')
    description = request.form.get('description')
    
    if name and time_start and routine_type:
        new_item = RoutineItem(
            name=name, 
            time_start=time_start, 
            routine_type=routine_type, 
            description=description
        )
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('settings'))

@app.route('/settings/delete/<int:item_id>', methods=['POST'])
def delete_routine(item_id):
    item = RoutineItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('settings'))

@app.route('/reminders/add', methods=['POST'])
def add_reminder():
    date_str = request.form.get('date')
    message = request.form.get('message')
    
    if date_str and message:
        reminder_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        new_reminder = Reminder(date=reminder_date, message=message)
        db.session.add(new_reminder)
        db.session.commit()
        
    return redirect(url_for('dashboard', date=date_str))

@app.route('/toggle_habit/<int:item_id>', methods=['POST'])
def toggle_habit(item_id):
    # We need to toggle for the SPECIFIC DATE shown on dashboard
    # Passing date via query param or JSON body is best.
    # For now, let's assume JSON body or fallback to today if not provided (legacy)
    # But better to use the query param concept
    
    data = request.get_json()
    date_str = data.get('date') if data else None
    
    if date_str:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        target_date = date.today()

    log = TrackerLog.query.filter_by(date=target_date, routine_item_id=item_id).first()
    
    if log:
        log.status = not log.status
        db.session.commit()
        clean_status = log.status
    else:
        new_log = TrackerLog(date=target_date, routine_item_id=item_id, status=True)
        db.session.add(new_log)
        db.session.commit()
        clean_status = True
        
    return jsonify({'success': True, 'status': clean_status})

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    today_str = request.args.get('date')
    if today_str:
        try:
            today = datetime.strptime(today_str, '%Y-%m-%d').date()
        except:
            today = date.today()
    else:
        today = date.today()

    entry = DiaryEntry.query.filter_by(date=today).first()
    
    if request.method == 'POST':
        content = request.form.get('content')
        pinned = request.form.get('pinned_text')
        
        # Handle multiple files
        files = request.files.getlist('photos')
        
        if not entry:
            entry = DiaryEntry(date=today, content=content, pinned_text=pinned)
            db.session.add(entry)
            db.session.commit() # Commit to get ID
        else:
            entry.content = content
            entry.pinned_text = pinned
            db.session.commit()

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{today}_{datetime.now().microsecond}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                # Add to DiaryImage table
                new_image = DiaryImage(diary_entry_id=entry.id, image_path=filename)
                db.session.add(new_image)
        
        db.session.commit()
        return redirect(url_for('diary', date=today.isoformat()))

    return render_template('diary.html', entry=entry, today=today)

@app.route('/diary/save', methods=['POST'])
def save_diary():
    """Auto-save diary entry without page reload"""
    date_str = request.form.get('date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            target_date = date.today()
    else:
        target_date = date.today()
    
    content = request.form.get('content', '')
    pinned_text = request.form.get('pinned_text', '')
    
    # Get or create entry
    entry = DiaryEntry.query.filter_by(date=target_date).first()
    if not entry:
        entry = DiaryEntry(date=target_date, content=content, pinned_text=pinned_text)
        db.session.add(entry)
    else:
        entry.content = content
        entry.pinned_text = pinned_text
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/timetable')
def timetable():
    weekday_items = RoutineItem.query.filter_by(routine_type='Weekday').all()
    weekend_items = RoutineItem.query.filter_by(routine_type='Weekend').all()
    return render_template('timetable.html', weekday=weekday_items, weekend=weekend_items)

@app.route('/gallery')
def gallery():
    # Fetch all images
    images = DiaryImage.query.join(DiaryEntry).order_by(DiaryEntry.date.desc()).all()
    return render_template('gallery.html', images=images)

@app.route('/timeline')
def timeline():
    # Fetch all entries for the timeline
    entries = DiaryEntry.query.order_by(DiaryEntry.date.desc()).all()
    
    # Process for grouping by Year -> Month
    # Structure: { 2024: { 'January': [entry1, entry2], 'February': [...] } }
    grouped_data = {}
    for entry in entries:
        year = entry.date.year
        month = entry.date.strftime('%B')
        
        if year not in grouped_data:
            grouped_data[year] = {}
        if month not in grouped_data[year]:
            grouped_data[year][month] = []
            
        grouped_data[year][month].append(entry)
        
    return render_template('timeline.html', grouped_data=grouped_data)

@app.route('/photo/delete/<int:image_id>', methods=['POST'])
def delete_photo(image_id):
    image = DiaryImage.query.get_or_404(image_id)
    entry_date = image.entry.date
    
    # Remove file from disk
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.image_path))
    except:
        pass # File might not exist
        
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for('diary', date=entry_date.isoformat()))

@app.route('/photo/upload', methods=['POST'])
def upload_photo():
    """Direct photo upload without requiring full entry save"""
    date_str = request.form.get('date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            target_date = date.today()
    else:
        target_date = date.today()
    
    # Get or create diary entry
    entry = DiaryEntry.query.filter_by(date=target_date).first()
    if not entry:
        entry = DiaryEntry(date=target_date, content='', pinned_text='')
        db.session.add(entry)
        db.session.commit()
    
    # Handle file upload
    files = request.files.getlist('photos')
    uploaded_count = 0
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{target_date}_{datetime.now().microsecond}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            new_image = DiaryImage(diary_entry_id=entry.id, image_path=filename)
            db.session.add(new_image)
            uploaded_count += 1
    
    db.session.commit()
    return jsonify({'success': True, 'count': uploaded_count})

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle Target Score Update
        target_score = request.form.get('target_score')
        if target_score:
            setting = UserSetting.query.filter_by(key='target_score').first()
            if not setting:
                setting = UserSetting(key='target_score', value=target_score)
                db.session.add(setting)
            else:
                setting.value = target_score
            db.session.commit()
        return redirect(url_for('settings'))

    items = RoutineItem.query.all()
    
    def parse_time(t_str):
        try:
            return datetime.strptime(t_str, "%I:%M %p")
        except:
            return datetime.min
            
    items.sort(key=lambda x: (x.routine_type, parse_time(x.time_start)))
    
    target_score_setting = UserSetting.query.filter_by(key='target_score').first()
    target_score = target_score_setting.value if target_score_setting else "80"

    return render_template('settings.html', items=items, target_score=target_score)

@app.route('/analytics')
def analytics():
    # Routine Frequency (Top 10 Most Completed)
    logs = TrackerLog.query.filter_by(status=True).all()
    routine_counts = {}
    for log in logs:
        item = RoutineItem.query.get(log.routine_item_id)
        if item:
            routine_counts[item.name] = routine_counts.get(item.name, 0) + 1
            
    sorted_routines = sorted(routine_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Diary Activity (Last 7 Days)
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    
    diary_counts = []
    dates = []
    current = start_date
    while current <= end_date:
        entry = DiaryEntry.query.filter_by(date=current).first()
        dates.append(current.strftime('%a')) # 'Mon', 'Tue'
        diary_counts.append(1 if (entry and entry.content) else 0)
        current += timedelta(days=1)
        
    # Category Distribution
    all_items = RoutineItem.query.all()
    categories = {}
    for item in all_items:
        cat = item.category or 'Uncategorized'
        categories[cat] = categories.get(cat, 0) + 1
        
    return render_template('analytics.html', 
                         routines_labels=[x[0] for x in sorted_routines],
                         routines_data=[x[1] for x in sorted_routines],
                         diary_labels=dates,
                         diary_data=diary_counts,
                         category_labels=list(categories.keys()),
                         category_data=list(categories.values()))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
