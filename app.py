from flask import Flask, render_template, request, redirect, url_for, flash
from exercises.pullDay import PullDay
from exercises.pushDay import PushDay
from exercises.legDay import LegsWorkout
from exercises.biceps import Biceps
from exercises.shoulders import Shoulders
import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Define your workout schedule
workout_schedule = {
    "Monday": "Pull Day (Back)",
    "Tuesday": "Biceps",
    "Wednesday": "Legs",
    "Thursday": "Push Day (Chest & Triceps)",
    "Friday": "Shoulders",
    "Saturday": "Rest or Cardio",
    "Sunday": "Abs and Swimming"
}

# Define a mapping of workouts to their plan methods
workout_plans = {
    "Pull Day (Back)": lambda: get_pull_day_plan(),
    "Push Day (Chest & Triceps)": lambda: get_push_day_plan(),
    "Legs": lambda: get_legs_day_plan(),
    "Biceps": lambda: get_biceps_day_plan(),
    "Shoulders": lambda: get_shoulders_day_plan(),
}


def get_todays_WO_plan():
    today = datetime.datetime.now().strftime("%A")
    return workout_schedule.get(today, "Rest or Custom Workout")


@app.route('/')
def index():
    today = datetime.datetime.now().strftime("%A")
    workout = get_todays_WO_plan()

    if workout in workout_plans:
        workout_plan = workout_plans[workout]()
        workout_message = f"Good morning! Today is {today}, and your workout is: {workout} \n\n{workout_plan}"
    else:
        workout_message = f"Good morning! Today is {today}, and your workout is: {workout}"

    return render_template('index.html', workout_message=workout_message)


@app.route('/end_of_day', methods=['GET', 'POST'])
def end_of_day_checkin():
    if request.method == 'POST':
        if 'yes' in request.form:
            flash("Great job! Keep it up!")
        else:
            flash("Don't worry, you'll get it next time!")
        return redirect(url_for('index'))

    return render_template('end_of_day.html')


# Define workout plan functions
def get_pull_day_plan():
    workout = PullDay()
    plan = workout.pullDay()
    plan_message = "\n".join([f"{key}: {value}" for key, value in plan.items()])
    return plan_message


def get_biceps_day_plan():
    workout = Biceps()
    plan = workout.bicepDay()
    plan_message = "\n".join([f"{key}: {value}" for key, value in plan.items()])
    return plan_message


def get_legs_day_plan():
    workout = LegsWorkout()
    plan = workout.legDay()
    plan_message = "\n".join([f"{key}: {value}" for key, value in plan.items()])
    return plan_message


def get_push_day_plan():
    workout = PushDay()
    plan = workout.pushDay()
    plan_message = "\n".join([f"{key}: {value}" for key, value in plan.items()])
    return plan_message


def get_shoulders_day_plan():
    workout = Shoulders()
    plan = workout.shoulderDay()
    plan_message = "\n".join([f"{key}: {value}" for key, value in plan.items()])
    return plan_message


if __name__ == "__main__":
    app.run(debug=True)
