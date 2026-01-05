from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RoutineItem(db.Model):
    __tablename__ = 'routine_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time_start = db.Column(db.String(20), nullable=False) # Store as string for flexibility e.g., "06:30 AM"
    time_end = db.Column(db.String(20), nullable=True)   # Optional end time
    routine_type = db.Column(db.String(20), nullable=False) # 'Weekday', 'Saturday', 'Sunday'
    category = db.Column(db.String(50), nullable=True) # Health, Work, Spirit, etc.
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'time_start': self.time_start,
            'time_end': self.time_end,
            'routine_type': self.routine_type,
            'category': self.category,
            'description': self.description
        }

class TrackerLog(db.Model):
    __tablename__ = 'tracker_logs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    routine_item_id = db.Column(db.Integer, db.ForeignKey('routine_items.id'), nullable=False)
    status = db.Column(db.Boolean, default=False) # True if completed

    routine_item = db.relationship('RoutineItem', backref=db.backref('logs', lazy=True))

class DiaryImage(db.Model):
    __tablename__ = 'diary_images'
    id = db.Column(db.Integer, primary_key=True)
    diary_entry_id = db.Column(db.Integer, db.ForeignKey('diary_entries.id'), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)

class DiaryEntry(db.Model):
    __tablename__ = 'diary_entries'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    content = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(200), nullable=True) # Kept for legacy/primary thumbnail if needed, or deprecate
    pinned_text = db.Column(db.String(200), nullable=True) # Highlight/Pinned thought for the day
    mood = db.Column(db.String(50), nullable=True)
    
    images = db.relationship('DiaryImage', backref='entry', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'content': self.content,
            'image_path': self.image_path,
            'pinned_text': self.pinned_text,
            'mood': self.mood,
            'images': [img.image_path for img in self.images]
        }

class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    message = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

class UserSetting(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(200), nullable=True)
