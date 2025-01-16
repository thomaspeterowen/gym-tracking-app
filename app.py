
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

st.title("Gym Tracking App")

users = ["", "Tommy", "Simon"]

selected_user = st.selectbox("Select a user:", users)
st.session_state["selected_user"] = selected_user


exercises = [
    "Select an option", "Bench Press", "Push-Ups", "Incline Dumbbell Press", "Chest Fly",
    "Pull-Ups", "Deadlifts", "Bent Over Rows", "Lat Pulldown",
    "Squats", "Leg Press", "Lunges", "Bulgarian Split Squats",
    "Bicep Curls", "Tricep Dips", "Hammer Curls", "Overhead Tricep Extension",
    "Overhead Press", "Lateral Raises", "Front Raises",
    "Plank", "Russian Twists", "Sit-Ups", "Leg Raises"
    ]

def select_exercise():
    print("Select an exercise from the list:")
    for i, exercise in enumerate(exercises, 1):
        print(f"{i}. {exercise}")

# Connect to server
client = MongoClient("mongodb://localhost:27017/")
# Specify the database
db = client["gym_tracker"]
# create or get collection
workouts = db["workouts"]

# create workout
def create_workout(user, db):

    workout_doc = {
        "user": user,
        "date": str(datetime.now().date()),
        "exercises": []
    }

    # insert data
    result = db.workouts.insert_one(workout_doc)
    return str(result.inserted_id) # return the workout ID as a string


# update workout add exercise
def add_exercise(workout_id, exercise_name, db):
    # Check if the exercise already exists
    workout = db.workouts.find_one({"_id": ObjectId(workout_id)})
    if workout:
        existing_exercises = [ex["name"] for ex in workout["exercises"]]
        if exercise_name not in existing_exercises:
            # Add the exercise
            db.workouts.update_one(
                {"_id": ObjectId(workout_id)},
                {"$push": {"exercises": {"name": exercise_name, "sets": []}}}
            )

# update exercise add rep
def add_rep(workout_id, exercise_name, reps, weight, db):
    db.workouts.update_one(
        {"_id": ObjectId(workout_id), "exercises.name": exercise_name},
        {"$push": {"exercises.$.sets": {"reps": reps, "weight": weight}}}
    )

# output workout
def get_workout(workout_id, db):
    return db.workouts.find_one({"_id": ObjectId(workout_id)})

if selected_user:
    st.write(f"You selected {selected_user}")
    option = st.radio("What would you like to do?", ["View History", "Log a Workout"])

    if option == "Log a Workout":
        st.header("Log a Workout")

        if "workout_id" not in st.session_state:
            st.session_state["workout_id"] = create_workout(st.session_state["selected_user"], db)
            st.write("Workout created!")

        # Step 1: Initialise session state for the dropdown key
        if "dropdown_key" not in st.session_state:
            st.session_state["dropdown_key"] = 0

        # Step 2: Create the dropdown with a dynamic key
        exercise = st.selectbox(
            "Select an exercise:",
            exercises,
            index=None,
            key=f"dropdown_{st.session_state['dropdown_key']}"
        )

        # Step 3: Handle dropdown actions
        if exercise != "Select an option":
            if "current_exercise" not in st.session_state or st.session_state["current_exercise"] != exercise:
                st.session_state["current_exercise"] = exercise
                add_exercise(st.session_state["workout_id"], exercise, db)
                st.write(f"Exercise {exercise} added!")
            # Input fields for reps and weight
            reps = st.number_input("How many reps?", value=0, min_value=0, step=1)
            weight = st.number_input("How much weight?", value=0.0, step=0.5)

            # Log Set button
            if st.button("Log set"):
                add_rep(st.session_state["workout_id"], exercise, reps, weight, db)
                st.write(f"Set logged: {reps} reps at {weight} kg.")

            if st.button("Show Exercise"):
                workout = get_workout(st.session_state["workout_id"], db)
                #st.write("Current Workout:", workout)
                # Header for the workout
                st.header(f"Workout for {workout['user']} on {workout['date']}")
                # Loop through exercises and display them
                for exercise in workout["exercises"]:
                    st.subheader(f"Exercise: {exercise['name']}")
                    # Display the sets in a formatted way
                    for i, set_ in enumerate(exercise["sets"], start=1):
                        st.write(f"Set {i}: {set_['reps']} reps at {set_['weight']} kg")

            # Log Exercise button to reset dropdown
            if st.button("Finish Workout"):
                #Increment the key to reset the dropdown
                #st.session_state["dropdown_key"] += 1
                #st.rerun()  # Immediately rerun the script
                st.write("Workout finished! Click View History to see your progress.")


    elif option == "View History":
        st.header("View History")

