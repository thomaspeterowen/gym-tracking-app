
import streamlit as st

st.title("Gym Tracking App")

exercises = [
    "Bench Press", "Push-Ups", "Incline Dumbbell Press", "Chest Fly",
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


st.write("What are you looking to do today?")

option = st.radio("What would you like to do?", ["Log a Workout", "View History"])

if option == "Log a Workout":
    st.header("Log a Workout")
    exercise = st.selectbox("Select an exercise:", ["Select an option","Bench Press", "Squats", "Deadlifts"])

    if exercise != "Select an option":
        st.write(exercise)
        sets = st.number_input("Insert a number", value=None, placeholder="Type a number...")
        number = st.number_input("Insert a number", value=None, placeholder="Type a number...")
        st.write("The current number is ", number)


elif option == "View History":
    st.header("View History")


#select_exercise = select_exercise()

#selection = input("Which exercise would you like to select? ")







