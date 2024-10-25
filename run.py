import streamlit as st
import pandas as pd
import random

# Streamlit Flashcard App
def main():
    st.title("Flashcard App")

    # File uploader to upload CSV
    uploaded_file = st.file_uploader("Upload your flashcards CSV file", type=["csv"])

    # Option to use example CSV
    use_example = st.checkbox("Use example flashcards.csv from the repository")

    if use_example:
        data = pd.read_csv("flashcards.csv")
    elif uploaded_file is not None:
        # Load the uploaded CSV file
        data = pd.read_csv(uploaded_file)
    else:
        data = None

    if data is not None:
        flashcards = list(data.itertuples(index=False, name=None))
        random.shuffle(flashcards)

        # Initialize session state for the current card index
        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0

        # Display the current flashcard question
        current_card = flashcards[st.session_state.current_index]
        st.write(f"### {current_card[0]}")

        # Reveal answer button
        if st.button("Reveal Answer"):
            st.write(f"**Answer:** {current_card[1]}")

        # Next card button
        if st.button("Next Card"):
            st.session_state.current_index = (st.session_state.current_index + 1) % len(flashcards)
            st.experimental_rerun()

if __name__ == "__main__":
    main()
