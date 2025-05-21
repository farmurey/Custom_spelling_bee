# Spelling Bee Practice App

A Streamlit application for practicing spelling words. The app provides pronunciation, spelling display, and navigation features. This one is customized for a specific list of words for my child. 

As a parent and a non-native English speaker, I often found it challenging to confidently pronounce certain words while helping my child with spelling. I built this app to give my child a fun, independent way to practice spelling with accurate, AI-generated pronunciation and an interactive interface they can use at their own pace.

## Features
- Word pronunciation using text-to-speech
- Show/hide spelling functionality
- Navigation between words
- Progress tracking
- Clean, modern interface

## Local Development
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

## Deployment
This app is deployed on Streamlit Community Cloud.  
You can access it at: [https://customspellingbee.streamlit.app](https://customspellingbee.streamlit.app)

## Files
- `app.py`: Main application file
- `extract_words.py`: Script to extract and clean words from Numbers file
- `spelling_words_clean.csv`: Cleaned word list
- `requirements.txt`: Project dependencies 
