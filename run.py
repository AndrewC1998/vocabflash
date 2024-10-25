import streamlit as st
import pandas as pd
import random

# Streamlit Flashcard App
def main():
    st.set_page_config(page_title="Flashcard App", layout="wide")
    st.title("Flashcard App")

    # Dark mode toggle
    dark_mode = st.button("🌙", key="dark_mode_toggle", help="Toggle Dark Mode")
    if dark_mode:
        st.markdown(
            """
            <style>
            .main, .sidebar-content {
                background-color: #333 !important;
                color: #f0f0f0 !important;
            }
            .flashcard-box {
                background-color: #444;
                color: #f0f0f0;
            }
            </style>
            """, unsafe_allow_html=True
        )

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
        data = pd.read_csv(f"Data/{language}/{language}_{level}.csv")
    else:
        data = None
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
        card_background_color = theme_colors.get(language, "#f0f0f5") if not dark_mode else "#444"
        answer_background_color = "#dff0d8" if not dark_mode else "#555"

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
                        if st.button("Correct", disabled=not st.session_state.reveal):
                            st.success("Great job!")
                            st.session_state.correct_count += 1
                            if st.session_state.current_index == len(flashcards) - 1:
                                st.session_state.session_ended = True
                            else:
                                st.session_state.current_index += 1
                                st.session_state.reveal = False
                    with col2:
                        if st.button("Incorrect", disabled=not st.session_state.reveal):
                            st.warning("Keep trying!")
                            st.session_state.incorrect_count += 1
                            if st.session_state.current_index == len(flashcards) - 1:
                                st.session_state.session_ended = True
                            else:
                                st.session_state.current_index += 1
                                st.session_state.reveal = False
            else:
                if st.button("Reveal Answer", disabled=st.session_state.reveal):
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
            random.shuffle(flashcards)

if __name__ == "__main__":
    main()
