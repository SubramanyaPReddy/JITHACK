import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
import signup  # Import the signup module

# Load environment variables
load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Generative AI
genai.configure(api_key=API_KEY)

# Initialize Generative Model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
instruction = """Give a score out of 10 based on the correctness and quality of the following code."""

# Function to evaluate the coding answers using Gemini
def evaluate_code(problem, answer):
    try:
        response = chat.send_message(problem + "\n\n" + answer + "\n\n" + instruction)
        score_text = response.text.strip()
        score = int(re.findall(r'\d+', score_text)[0])
        return score
    except Exception as e:
        st.error(f"Error evaluating code: {e}")
        return 0

# Questions bank for each language
questions_bank = {
    "C": {
        "mcqs": [
            {"question": "What is the size of int in C?", "options": ["2 bytes", "4 bytes", "8 bytes", "Depends on compiler"], "answer": "Depends on compiler"},
            {"question": "Which is used to terminate a C statement?", "options": [".", ";", ":", "None"], "answer": ";"},
            {"question": "What is the output of printf(\"%d\", -1 << 1)?", "options": ["-1", "0", "1", "Undefined"], "answer": "0"},
            {"question": "What does the function fgets() in C do?", "options": ["Reads a line from the specified stream", "Writes a line to the specified stream", "Formats a string", "None of the above"], "answer": "Reads a line from the specified stream"},
            {"question": "What does the % operator do in C?", "options": ["Modulus", "Division", "Multiplication", "Exponentiation"], "answer": "Modulus"},
        ],
        "problems": [
            "Write a program in C to find the factorial of a number.",
            "Write a C program to check if a number is prime.",
            "Write a C program to reverse a given string.",
            "Write a C program to find the sum of all elements in an array.",
        ],
        "basic": [
            {"question": "What is a variable in C?", "answer": "A variable is a named space in memory where data is stored."},
            {"question": "How do you declare an integer variable in C?", "answer": "int variable_name;"},
            {"question": "What is a pointer in C?", "answer": "A pointer is a variable that stores the memory address of another variable."}
        ]
    },
    "C++": {
        "mcqs": [
            {"question": "What is the default access level for members of a class in C++?", "options": ["public", "private", "protected", "none"], "answer": "private"},
            {"question": "Which of the following is a feature of C++?", "options": ["Encapsulation", "Inheritance", "Polymorphism", "All of the above"], "answer": "All of the above"},
            {"question": "What is the output of cout << (5 == 5)?", "options": ["1", "True", "False", "Compiler Error"], "answer": "1"},
            {"question": "Which operator is used to allocate memory in C++?", "options": ["new", "malloc", "alloc", "create"], "answer": "new"},
            {"question": "What is the function of the destructor in C++?", "options": ["To destruct an object", "To create an object", "To allocate memory", "To deallocate memory"], "answer": "To deallocate memory"},
        ],
        "problems": [
            "Write a C++ program to implement a simple calculator.",
            "Write a C++ program to find the largest of three numbers.",
            "Write a C++ program to swap two numbers without using a temporary variable.",
            "Write a C++ program to count the number of vowels and consonants in a string.",
        ],
        "basic": [
            {"question": "What is a class in C++?", "answer": "A class is a user-defined data type that represents a blueprint for objects."},
            {"question": "How do you declare an integer variable in C++?", "answer": "int variable_name;"},
            {"question": "What is inheritance in C++?", "answer": "Inheritance is a feature that allows a class to inherit properties and behaviors from another class."}
        ]
    },
    "Java": {
        "mcqs": [
            {"question": "Which of the following is not a Java feature?", "options": ["Object-oriented", "Use of pointers", "Portable", "Dynamic"], "answer": "Use of pointers"},
            {"question": "Which keyword is used to prevent inheritance in Java?", "options": ["sealed", "final", "static", "constant"], "answer": "final"},
            {"question": "What is the output of System.out.println(\"2\" + \"2\") in Java?", "options": ["4", "22", "Compilation Error", "Runtime Error"], "answer": "22"},
            {"question": "Which Java keyword is used to define a constant?", "options": ["const", "constant", "final", "define"], "answer": "final"},
            {"question": "What is the Java equivalent of the C switch statement?", "options": ["switch", "case", "if-else", "for"], "answer": "switch"},
        ],
        "problems": [
            "Write a Java program to check if a string is a palindrome.",
            "Write a Java program to sort an array of integers.",
            "Write a Java program to find the sum of all elements in an array.",
            "Write a Java program to convert Celsius to Fahrenheit.",
        ],
        "basic": [
            {"question": "What is a class in Java?", "answer": "A class is a blueprint from which individual objects are created."},
            {"question": "How do you declare an integer variable in Java?", "answer": "int variable_name;"},
            {"question": "What is an object in Java?", "answer": "An object is an instance of a class."}
        ]
    },
    "Python": {
        "mcqs": [
            {"question": "What is the output of print(2 ** 3)?", "options": ["5", "6", "8", "9"], "answer": "8"},
            {"question": "Which of the following is used to define a block of code in Python?", "options": ["{}", "[]", "()", "Indentation"], "answer": "Indentation"},
            {"question": "What is the result of the expression 10 // 3 in Python?", "options": ["3", "3.333", "3.0", "4"], "answer": "3"},
            {"question": "What does the built-in function len() do in Python?", "options": ["Returns the length of an object", "Returns the absolute value of a number", "Returns the largest item in an iterable", "Returns the smallest item in an iterable"], "answer": "Returns the length of an object"},
            {"question": "Which data type is mutable in Python?", "options": ["List", "Tuple", "String", "Dictionary"], "answer": "List"},
        ],
        "problems": [
            "Write a Python program to find the Fibonacci sequence up to a given number.",
            "Write a Python program to find the factorial of a number.",
            "Write a Python program to check if a number is prime.",
            "Write a Python program to reverse a given string.",
        ],
        "basic": [
            {"question": "What is a variable in Python?", "answer": "A variable is a reserved memory location to store values."},
            {"question": "How do you declare an integer variable in Python?", "answer": "variable_name = value"},
            {"question": "What is a list in Python?", "answer": "A list is a collection which is ordered and changeable. Allows duplicate members."}
        ]
    }
}

# Function to handle the signup page
def signup_page():
    st.title("Signup Page")
    
    # Collect user details
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Signup"):
        if password == confirm_password:
            # Call the signup function from signup.py
            success = signup.signup(
                username, email, password,
                host='localhost',
                port=3306,
                database='app',
                mysql_user='root',
                mysql_password='Subbu2003#'
            )
            if success:
                st.success("Signup successful! You can now login.")
            else:
                st.error("Signup failed. Please try again.")
        else:
            st.error("Passwords do not match.")

# Function to handle the login page
def login_page():
    st.title("Login Page")
    
    # Collect user details
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Call the login function from signup.py
        success = signup.login(
            email, password,
            host='localhost',
            port=3306,
            database='app',
            mysql_user='root',
            mysql_password='password'
        )
        if success:
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.success("Login successful! Redirecting to home page...")
        else:
            st.error("Login failed. Please check your credentials.")

# Function to handle the main app
def main_app():
    st.title("Coding Practice Platform")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    selected = st.sidebar.radio("Go to", ["Home", "Learn", "Take Test", "Coding", "Results", "Log out"])

    if selected == "Home":
        st.header("Welcome to the Coding Practice Platform")
        st.write("Navigate through the options to start learning and testing your coding skills.")

    elif selected == "Learn":
        language = st.selectbox("Select a language", ["C", "C++", "Java", "Python"])
        st.header(f"Basics of {language}")
        basics = questions_bank[language]["basic"]
        for question in basics:
            st.subheader(question["question"])
            st.write(question["answer"])

    elif selected == "Take Test":
        language = st.selectbox("Select a language", ["C", "C++", "Java", "Python"])
        st.header(f"MCQs for {language}")
        questions = questions_bank[language]["mcqs"]
        user_answers = []
        for question in questions:
            st.write(question["question"])
            user_answer = st.radio("", question["options"], key=question["question"])
            user_answers.append(user_answer)

        if st.button("Submit Answers"):
            correct_count = 0
            for i, question in enumerate(questions):
                if user_answers[i] == question["answer"]:
                    correct_count += 1

            # Plotting the results
            fig, ax = plt.subplots()
            ax.pie([correct_count, len(questions) - correct_count], labels=['Correct', 'Incorrect'], autopct='%1.1f%%')
            st.pyplot(fig)

            # Store the results
            user_id = signup.get_user_id(st.session_state["email"], 'localhost', 3306, 'app', 'root', 'Subbu2003#')
            signup.store_mcq_result(user_id, language, correct_count, len(questions), 'localhost', 3306, 'app', 'root', 'password')

    elif selected == "Coding":
        language = st.selectbox("Select a language", ["C", "C++", "Java", "Python"])
        st.header(f"Coding Problems for {language}")
        problems = questions_bank[language]["problems"]
        for problem in problems:
            st.write(problem)
            solution = st.text_area("Write your solution here", key=problem)
            if st.button("Submit Solution", key=f"submit_{problem}"):
                score = evaluate_code(problem, solution)
                user_id = signup.get_user_id(st.session_state["email"], 'localhost', 3306, 'app', 'root', 'password')
                signup.store_coding_result(user_id, language, problem, solution, score, 'localhost', 3306, 'app', 'root', 'password')
                st.success(f"Your solution has been submitted for review. Score: {score}/10")

    elif selected == "Results":
        st.header("Your Results")
        user_id = signup.get_user_id(st.session_state["email"], 'localhost', 3306, 'app', 'root', 'password')
        
        st.subheader("MCQ Results")
        mcq_results = signup.get_mcq_results(user_id, 'localhost', 3306, 'app', 'root', 'password')
        if mcq_results:
            mcq_df = pd.DataFrame(mcq_results, columns=["Language", "Correct Answers", "Total Questions", "Date"])
            st.dataframe(mcq_df)
        else:
            st.write("No MCQ results found.")

        st.subheader("Coding Results")
        coding_results = signup.get_coding_results(user_id, 'localhost', 3306, 'app', 'root', 'password')
        if coding_results:
            coding_df = pd.DataFrame(coding_results, columns=["Language", "Problem", "Solution", "Score", "Date"])
            st.dataframe(coding_df)
        else:
            st.write("No coding results found.")

    elif selected == "Log out":
        st.session_state["logged_in"] = False
        st.success("You have been logged out.")
        st.experimental_rerun()

# Main application flow
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    options = ["Signup", "Login"]
    choice = st.sidebar.radio("Go to", options)
    if choice == "Signup":
        signup_page()
    elif choice == "Login":
        login_page()

# Improve aesthetics
st.markdown("""
    <style>
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 10rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .css-1d391kg {
        text-align: center;
    }
    .css-1cpxqw2 {
        padding: 3rem 1rem;
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
