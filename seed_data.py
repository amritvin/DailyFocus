from app import app, db
from models import RoutineItem

def seed_data():
    with app.app_context():
        db.create_all()
        
        if RoutineItem.query.first():
            print("To prevent duplicates, clearing existing data...")
            RoutineItem.query.delete()
            db.session.commit()

        weekday_routine = [
            ("06:30 AM", "Wake Up + 500ml Water + B12", "Clear the Fog: Immediate hydration."),
            ("06:35 AM", "Fresh Up (Face, Teeth, Toilet)", "System 'Boot-up.'"),
            ("06:40 AM", "Archana (20 mins)", "Spiritual Grounding: Calm the overthinking."),
            ("07:00 AM", "Cook Breakfast (15 mins)", "Thyroid Fuel: Eggs + Spinach + Vit D3."),
            ("07:30 AM", "WORK START", "Early focus block."),
            ("08:30 AM", "Cook Lunch (45 mins)", "Liver Health: Lentils/Paneer + Veg."),
            ("09:30 AM", "Deep Work Block", "Drink 1st Liter of water."),
            ("12:30 PM", "Lunch + Omega-3", "Metabolic fuel."),
            ("01:00 PM", "Caffeine Cutoff", "Protect your 11 PM sleep window."),
            ("04:45 PM", "Work Ends (Shift 1)", "Hard boundary for the gym."),
            ("05:00 PM", "GYM (30-40m Weights)", "Athletic Body: Burn sedentary stress."),
            ("05:40 PM", "Meditation (15 mins)", "The Reset: Transition from 'Active' to 'Calm.'"),
            ("06:00 PM", "30 Min Walk", "Fresh air & metabolic flow."),
            ("06:30 PM", "Shower & Dinner", "Healthy fats & protein."),
            ("07:00 PM", "INDIA CALLS START", "Active Shift: Stand or walk during calls."),
            ("10:15 PM", "Magnesium Glycinate", "The Shutdown: Lowers cortisol while working."),
            ("10:30 PM", "WORK ENDS", "Close laptop. Stop all blue light."),
            ("10:35 PM", "Night Routine (Bath/Brush/Face)", "The Reset: Warm bath to drop core temp."),
            ("11:00 PM", "Lights Out", "Target: 7.5 hours of recovery.")
        ]

        weekend_routine = [
            ("08:00 AM", "Wake Up + Water + B12", "Recovery Sleep: +1.5 hours extra."),
            ("08:05 AM", "Fresh Up", "Prepare for spirit."),
            ("08:15 AM", "Archana (20 mins)", "Weekend Spiritual Anchor."),
            ("08:45 AM", "Tablets (D3 + Omega-3)", "Cognitive support."),
            ("09:00 AM", "STUDY BLOCK 1 (75 mins)", "Deep Focus: Hardest topics first."),
            ("10:15 AM", "Deep Workout (90 mins)", "Athletic Peak: Heavy lifting day."),
            ("11:45 AM", "Full Bath / Refresh", "Cleanse gym sweat."),
            ("12:15 PM", "Lunch", "Saturday: Batch Cook, Sunday: Relaxed meal."),
            ("01:00 PM", "STUDY BLOCK 2 (90 mins)", "Application: Practice/Review."),
            ("02:30 PM", "Activity Block", "Sat: Grocery Shopping, Sun: Travel to MA Centre."),
            ("03:00 PM", "MA Centre (Sunday Only)", "Archana & Community until 6:00 PM."),
            ("06:30 PM", "Evening Walk / Personal Time", "Reflect and relax."),
            ("09:30 PM", "Magnesium + Wind Down", "Early prep for Monday start."),
            ("11:00 PM", "Lights Out", "Consistent sleep rhythm.")
        ]

        for time, name, desc in weekday_routine:
            db.session.add(RoutineItem(
                name=name,
                time_start=time,
                routine_type='Weekday',
                description=desc
            ))

        for time, name, desc in weekend_routine:
            db.session.add(RoutineItem(
                name=name,
                time_start=time,
                routine_type='Weekend',
                description=desc
            ))

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
