import os
import sys
from app import app, db
from models import RoutineItem

def verify():
    print("Verifying setup...")
    
    # 1. Check DB file
    if not os.path.exists('habit_tracker/habit_tracker.db') and not os.path.exists('habit_tracker.db'):
        # Flask-SQLAlchemy might create it in instance or root depending on config
        # Our config is specific, but let's check app context
        pass

    with app.app_context():
        # 2. Check Data
        count = RoutineItem.query.count()
        print(f"Routine Items found: {count}")
        if count == 0:
            print("ERROR: Database is empty!")
            return False
            
        # 3. Check Routes
        client = app.test_client()
        routes = ['/', '/settings', '/timetable', '/diary', '/gallery', '/timeline', '/analytics']
        for route in routes:
            response = client.get(route)
            print(f"Route {route} Status: {response.status_code}")
            if response.status_code != 200:
                print(f"ERROR: {route} failed!")
                return False
            
    print("Verification Successful!")
    return True

if __name__ == "__main__":
    if verify():
        sys.exit(0)
    else:
        sys.exit(1)
