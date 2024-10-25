import streamlit as st
import pandas as pd
import random
import os

# Streamlit Flashcard App
def main():
    st.set_page_config(page_title="Flashcard App", layout="wide")
    st.title("Flashcard App")

    # Print current working directory for debugging
    st.write(f"Current working directory: {os.getcwd()}")

    # Dropdown menu for selecting example CSVs
    language = st.selectbox("Language", ["None", "French", "German", "Spanish"])
    level = None
    theme_colors = {
        "French": "#f0e68c",
        "German": "#ffcccb",
        "Spanish": "#f5deb3"
    }

    if language != "None":
        level = st.selectbox("Level", ["A1", "A2", "B1", "B2", "C1", "C2"])

    # Load the appropriate CSV
    data = None
    if language in ["French", "German", "Spanish"] and level is not None:
        file_path = os.path.abspath(os.path.join(os.getcwd(), "Data", language, f"{language}_{level}.csv"))
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
        else:
            st.error(f"File not found: {file_path}. Please check the path and try again.")
    else:
        uploaded_file = st.file_uploader("Upload your flashcards CSV file", type=["csv"])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)

    if data is not None:
        flashcards = list(data.itertuples(index=False, name=None))
        random.shuffle(flashcards)

        # Initialize session state for the current card index, reveal state, and score tracking
        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0
        if 'reveal' not in st.session_state:
            st.session_state.reveal = False
        if 'correct_count' not in st.session_state:
            st.session_state.correct_count = 0
        if 'incorrect_count' not in st.session_state:
            st.session_state.incorrect_count = 0
        if 'session_ended' not in st.session_state:
            st.session_state.session_ended = False

        # Set themed color for the selected language
        card_background_color = theme_colors.get(language, "#f0f0f5")
        answer_background_color = "#dff0d8"

        # End session summary
        if st.session_state.session_ended:
            st.header("Session Summary")
            st.write(f"Total Correct: {st.session_state.correct_count}")
            st.write(f"Total Incorrect: {st.session_state.incorrect_count}")
            if st.button("Restart Session"):
                st.session_state.current_index = 0
                st.session_state.correct_count = 0
                st.session_state.incorrect_count = 0
                st.session_state.reveal = False
                st.session_state.session_ended = False
                random.shuffle(flashcards)
        else:
            # Immersive view when a specific language and level are selected
            current_card = flashcards[st.session_state.current_index]
            question, answer = current_card[0], current_card[1]
