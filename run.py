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
                color: #000;
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
                color: #000;
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
                color: #000;
            }
            .center-button {
                display: flex;
                justify-content: center;
                margin: 30px 0;
            }
            .side-buttons {
                display: flex;
                justify-content: space-between;
                margin: 30px 0;
            }
            .bottom-buttons {
                display: flex;
                justify-content: space-between;
                margin: 50px 0;
            }
            .accuracy {
                text-align: center;
                font-size: 20px;
                margin-top: 20px;
                color: #333;
            }
            .button-large {
                font-size: 20px;
                padding: 15px 30px;
                color: #000;
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

    # Load the appropriate CSV only after a level is selected
    data = None
    if language in ["French", "German", "Spanish"] and level is not None and 'data' not in st.session_state:
        if st.button("Confirm Selection", key='confirm_selection'):
            file_path = os.path.join(os.getcwd(), "Data", language, f"{language}_{level}.csv")
            if os.path.exists(file_path):
                data = pd.read_csv(file_path)
                st.session_state.data = data
            else:
                st.error(f"File not found: {file_path}. Please check the path and try again.")
    if 'data' in st.session_state:
        data = st.session_state.data
    else:
        uploaded_file = st.file_uploader("Upload your flashcards CSV file", type=["csv"], key='file_upload')
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.session_state.data = data

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
        if 'correct_answers' not in st.session_state:
            st.session_state.correct_answers = []
        if 'incorrect_answers' not in st.session_state:
            st.session_state.incorrect_answers = []

        # Set themed color for the selected language
        card_background_color = theme_colors.get(language, "#f0f0f5")

        # End session summary
        if st.session_state.session_ended:
            st.header("Session Summary")
            total_attempted = st.session_state.correct_count + st.session_state.incorrect_count
            if total_attempted == 0:
                accuracy = 0
            else:
                accuracy = 100 * st.session_state.correct_count / total_attempted
            st.markdown(f"<div class='accuracy' style='color: inherit;'><div class='accuracy'>You answered <strong>{total_attempted}</strong> questions in total.</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='accuracy' style='color: inherit;'><div class='accuracy'>Your accuracy was <strong>{accuracy:.2f}%</strong></div></div>", unsafe_allow_html=True)

            # Expandable sections for correct and incorrect answers
            with st.expander("View Correct Answers"):
                correct_df = pd.DataFrame(st.session_state.correct_answers, columns=["Question", "Answer"])
                st.table(correct_df)
            with st.expander("View Incorrect Answers"):
                incorrect_df = pd.DataFrame(st.session_state.incorrect_answers, columns=["Question", "Answer"])
                st.table(incorrect_df)

            if st.button("Restart Session", key='restart_summary'):
                st.session_state.current_index = 0
                st.session_state.correct_count = 0
                st.session_state.incorrect_count = 0
                st.session_state.reveal = False
                st.session_state.session_ended = False
                st.session_state.correct_answers = []
                st.session_state.incorrect_answers = []
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
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Correct", key='correct_button', use_container_width=True):
                        st.session_state.correct_count += 1
                        st.session_state.correct_answers.append((question, answer))
                        if st.session_state.current_index == len(st.session_state.flashcards) - 1:
                            st.session_state.session_ended = True
                        else:
                            st.session_state.current_index += 1
                            st.session_state.reveal = False
                with col2:
                    if st.button("Incorrect", key='incorrect_button', use_container_width=True):
                        st.session_state.incorrect_count += 1
                        st.session_state.incorrect_answers.append((question, answer))
                        if st.session_state.current_index == len(st.session_state.flashcards) - 1:
                            st.session_state.session_ended = True
                        else:
                            st.session_state.current_index += 1
                            st.session_state.reveal = False
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='center-button'>", unsafe_allow_html=True)
                if st.button("Reveal Answer", key='reveal_button', use_container_width=True):
                    st.session_state.reveal = True
                st.markdown("</div>", unsafe_allow_html=True)

            # Bottom Buttons for Restart and End Session
            st.markdown("<div class='bottom-buttons'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Restart Session", key='restart_button', use_container_width=True):
                    st.session_state.current_index = 0
                    st.session_state.correct_count = 0
                    st.session_state.incorrect_count = 0
                    st.session_state.reveal = False
                    st.session_state.session_ended = False
                    st.session_state.correct_answers = []
                    st.session_state.incorrect_answers = []
                    random.shuffle(st.session_state.flashcards)
            with col2:
                if st.button("End Session", key='end_button', use_container_width=True):
                    st.session_state.session_ended = True
            st.markdown("</div>", unsafe_allow_html=True)

    # Close Main Container
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
