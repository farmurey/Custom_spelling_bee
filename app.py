import streamlit as st
import pandas as pd
import io
from gtts import gTTS
import tempfile
import os
import base64

# Set page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Spelling Bee Practice",
    page_icon="🐝",
    layout="centered"
)

# Initialize text-to-speech functionality
def pronounce_word(word):
    """Function to pronounce the given word using gTTS and auto-play audio"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            # Generate speech
            tts = gTTS(text=word, lang='en', slow=False)
            tts.save(fp.name)
            
            # Read and encode audio as base64
            audio_file = open(fp.name, 'rb')
            audio_bytes = audio_file.read()
            b64 = base64.b64encode(audio_bytes).decode()
            audio_html = f'''<audio autoplay="true" style="display:none;">
                                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3" />
                                Your browser does not support the audio element.
                            </audio>'''
            st.markdown(audio_html, unsafe_allow_html=True)
            
            # Clean up
            audio_file.close()
            os.unlink(fp.name)
    except Exception as e:
        st.error(f"Error pronouncing word: {str(e)}")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        margin: 0.5rem 0;
    }
    .word-container {
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and instructions
st.title("🐝 Spelling Bee Practice")
st.markdown("""
    Practice your spelling with the predefined word list!
    Each word will be pronounced for you to practice spelling.
""")

# Initialize session state variables
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'words_df' not in st.session_state:
    st.session_state.words_df = None
if 'show_spelling' not in st.session_state:
    st.session_state.show_spelling = False
if 'pronounce_flag' not in st.session_state:
    st.session_state.pronounce_flag = False

def load_words():
    """Function to load the word list from CSV"""
    try:
        # Read the clean CSV file
        df = pd.read_csv('spelling_words_clean.csv')
        
        if df.empty:
            st.error("Error: The word list is empty")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error loading word list: {str(e)}")
        return None

# Load words if not already loaded
if st.session_state.words_df is None:
    st.session_state.words_df = load_words()
    
if st.session_state.words_df is not None:
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # All buttons in one row: Next, Show Spelling, Previous
        col_next, col_spelling, col_prev = st.columns([1, 1, 1])

        with col_next:
            if st.button("➡️ Next", key="next_btn"):
                if st.session_state.current_index < len(st.session_state.words_df) - 1:
                    st.session_state.current_index += 1
                    st.session_state.show_spelling = False
                    st.session_state.pronounce_flag = True
                    st.rerun()

        with col_spelling:
            if st.button("🆎 Show Spelling", key="spelling_btn"):
                st.session_state.show_spelling = not st.session_state.show_spelling
                st.rerun()

        with col_prev:
            if st.button("⬅️ Previous", key="prev_btn"):
                if st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
                    st.session_state.show_spelling = False
                    st.session_state.pronounce_flag = True
                    st.rerun()

        # Automatically pronounce the word if flag is set
        current_word = st.session_state.words_df.iloc[st.session_state.current_index]['Word']
        if st.session_state.pronounce_flag:
            pronounce_word(current_word)
            st.session_state.pronounce_flag = False

        # Display current word after buttons only if show_spelling is True
        if st.session_state.show_spelling:
            st.markdown(f"### {current_word}")
    
    with col2:
        # Progress indicator
        st.progress((st.session_state.current_index + 1) / len(st.session_state.words_df))
        st.markdown(f"Word {st.session_state.current_index + 1} of {len(st.session_state.words_df)}")