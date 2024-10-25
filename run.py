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

        # Initialize session state for the current card
        if 'current_card' not in st.session_state:
            st.session_state.current_card = random.choice(flashcards)

        # Display the current flashcard question
        st.write(f"### {st.session_state.current_card[0]}")

        # Reveal answer button
        if st.button("Reveal Answer"):
            st.write(f"**Answer:** {st.session_state.current_card[1]}")

        # Next card button
        if st.button("Next Card"):
            st.session_state.current_card = random.choice(flashcards)
            st.experimental_rerun()

if __name__ == "__main__":
    main()
