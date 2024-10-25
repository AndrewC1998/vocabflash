import streamlit as st
import pandas as pd
import random
import os

# Streamlit Flashcard App
def main():
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
                random.shuffle(st.session_state.flashcards)
        else:
            # Immersive view when a specific language and level are selected
            current_card = st.session_state.flashcards[st.session_state.current_index]
            question, answer = current_card[0], current_card[1]

            # Layout for flashcard display
            st.markdown(f"""
                <style>
                .flashcard-box {{
                    background-color: {card_background_color};
                    padding: 40px;
                    border-radius: 15px;
                    text-align: center;
                    font-size: 28px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s;
                }}
                .flashcard-box:hover {{
                    transform: scale(1.05);
                }}
                </style>

                <div class="flashcard-box">
                    <p><strong>Question:</strong> {question}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.session_state.reveal:
                st.markdown(f"""
                    <style>
                    .flashcard-box {{
                        background-color: {answer_background_color};
                        padding: 40px;
                        border-radius: 15px;
                        text-align: center;
                        font-size: 28px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        transition: transform 0.3s;
                    }}
                    .flashcard-box:hover {{
                        transform: scale(1.05);
                    }}
                    </style>

                    <div class="flashcard-box">
                        <p><strong>Answer:</strong> {answer}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Buttons for correct and incorrect
                button_container = st.container() if st.session_state.reveal else st.empty()
                with button_container:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Correct") and st.session_state.reveal:
                            st.session_state.correct_count += 1
                            if st.session_state.current_index == len(st.session_state.flashcards) - 1:
                                st.session_state.session_ended = True
                            else:
                                st.session_state.current_index += 1
                                st.session_state.reveal = False
                    with col2:
                        if st.button("Incorrect") and st.session_state.reveal:
                            st.session_state.incorrect_count += 1
                            if st.session_state.current_index == len(st.session_state.flashcards) - 1:
                                st.session_state.session_ended = True
                            else:
                                st.session_state.current_index += 1
                                st.session_state.reveal = False
            else:
                if st.button("Reveal Answer") and not st.session_state.reveal:
                    st.session_state.reveal = True

            # End Session Button
            if st.button("End Session"):
                st.session_state.session_ended = True
                st.session_state.current_index = 0

        # Total display and Restart Button
        st.markdown("## Total")
        st.write(f"Total Correct: {st.session_state.correct_count}")
        st.write(f"Total Incorrect: {st.session_state.incorrect_count}")
        if st.button("Restart Session"):
            st.session_state.current_index = 0
            st.session_state.correct_count = 0
            st.session_state.incorrect_count = 0
            st.session_state.reveal = False
            st.session_state.session_ended = False
            random.shuffle(st.session_state.flashcards)

if __name__ == "__main__":
    main()
