import streamlit as st
import pandas as pd
import random
import os

# Streamlit Flashcard App
def main():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
            body {
                background-color: #f5f5f5;
                font-family: 'Arial', sans-serif;
            }
            .main-container {
                max-width: 700px;
                margin: auto;
            }
            .flashcard {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 20px;
                text-align: center;
                font-size: 24px;
                margin: 20px 0;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                transition: transform 0.4s;
            }
            .flashcard:hover {
                transform: translateY(-5px);
            }
            .answer {
                background-color: #dff0d8;
                padding: 30px;
                border-radius: 20px;
                text-align: center;
                font-size: 24px;
                margin: 20px 0;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                transition: transform 0.4s;
            }
            .center-button {
                display: flex;
                justify-content: center;
                margin: 20px 0;
            }
            .side-buttons {
                display: flex;
                justify-content: space-between;
                margin: 20px 0;
            }
            .bottom-buttons {
                position: fixed;
                bottom: 20px;
                left: 20px;
                right: 20px;
                display: flex;
                justify-content: space-between;
            }
            .accuracy {
                text-align: center;
                font-size: 20px;
                margin-top: 20px;
                color: #333;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Main Container
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # Dropdown menu for selecting example CSVs
    language = st.selectbox("Language", ["None", "French", "German", "Spanish"])
    level = None
    theme_colors = {
        "French": "#ffdfba",
        "German": "#d4a5a5",
        "Spanish": "#ffe6e6"
    }

    if language != "None":
        level = st.selectbox("Level", ["A1", "A2", "B1", "B2", "C1", "C2"])

    # Load the appropriate CSV
    if language in ["French", "German", "Spanish"] and level is not None:
        file_path = os.path.join(os.getcwd(), "Data", language, f"{language}_{level}.csv")
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
        else:
            st.error(f"File not found: {file_path}. Please check the path and try again.")
            data = None
    else:
        data = None
        uploaded_file = st.file_uploader("Upload your flashcards CSV file", type=["csv"])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)

    if data is not None:
        # Shuffle flashcards only once and store in session state
        if 'flashcards' not in st.session_state:
            flashcards = list(data.itertuples(index=False, name=None))
            random.shuffle(flashcards)
            st.session_state.flashcards = flashcards

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

        # End session summary
        if st.session_state.session_ended:
            st.header("Session Summary")
            accuracy = 100 * st.session_state.correct_count / (st.session_state.correct_count + st.session_state.incorrect_count)
            st.markdown(f"<div class='accuracy'>Your current accuracy is <strong>{accuracy:.2f}%</strong></div>", unsafe_allow_html=True)
                        if st.button("Restart Session"):
                st.session_state.current_index = 0
                st.session_state.correct_count = 0
                st.session_state.incorrect_count = 0
                st.session_state.reveal = False
                st.session_state.session_ended = False
                random.shuffle(st.session_state.flashcards)
        else:
            # Immersive view when a specific language and level are selected
            current_card = st.session_state.flashcards[st.session_state.current_index]
            question, answer = current_card[0], current_card[1]

            # Display Question
            st.markdown(f"<div class='flashcard'><strong>Question:</strong> {question}</div>", unsafe_allow_html=True)

            # Reveal answer if requested
            if st.session_state.reveal:
                st.markdown(f"<div class='answer'><strong>Answer:</strong> {answer}</div>", unsafe_allow_html=True)

                # Buttons for correct and incorrect
                st.markdown("<div class='side-buttons'>", unsafe_allow_html=True)
                if st.button("Correct", key='correct_button', help="Click if your answer was correct"):
                    st.session_state.correct_count += 1
                    if st.session_state.current_index == len(st.session_state.flashcards) - 1:
                        st.session_state.session_ended = True
                    else:
                        st.session_state.current_index += 1
                        st.session_state.reveal = False
                if st.button("Incorrect", key='incorrect_button', help="Click if your answer was incorrect"):
                    st.session_state.incorrect_count += 1
                    if st.session_state.current_index == len(st.session_state.flashcards) - 1:
                        st.session_state.session_ended = True
                    else:
                        st.session_state.current_index += 1
                        st.session_state.reveal = False
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='center-button'>", unsafe_allow_html=True)
                if st.button("Reveal Answer", key='reveal_button', help="Click to reveal the answer"):
                    st.session_state.reveal = True
                st.markdown("</div>", unsafe_allow_html=True)

            # Bottom Buttons for Restart and End Session
            st.markdown("<div class='bottom-buttons'>", unsafe_allow_html=True)
            if st.button("Restart Session", key='restart_button', help="Click to restart the session"):
                st.session_state.current_index = 0
                st.session_state.correct_count = 0
                st.session_state.incorrect_count = 0
                st.session_state.reveal = False
                st.session_state.session_ended = False
                random.shuffle(st.session_state.flashcards)
            if st.button("End Session", key='end_button', help="Click to end the session"):
                st.session_state.session_ended = True
                st.session_state.current_index = 0
            st.markdown("</div>", unsafe_allow_html=True)

    # Close Main Container
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
