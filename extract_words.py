import pandas as pd
import subprocess
import tempfile
import os

def extract_words():
    """Extract words from Numbers file and save to clean CSV with single column"""
    try:
        # Create a temporary file for the CSV
        temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_csv.close()
        
        # AppleScript to convert Numbers to CSV
        script = f'''
        tell application "Numbers"
            open POSIX file "{os.path.abspath('highlighted_spelling.numbers')}"
            delay 1
            tell document 1
                export to POSIX file "{temp_csv.name}" as CSV
                close saving no
            end tell
        end tell
        '''
        
        # Run the AppleScript
        subprocess.run(['osascript', '-e', script])
        
        # Read the CSV
        df = pd.read_csv(temp_csv.name)
        
        # Skip the first row (header)
        df = df.iloc[1:]
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Clean up the data
        # Remove any completely empty columns
        df = df.loc[:, (df != '').any()]
        
        # Clean up the words (remove any special characters, extra spaces)
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            # Remove any rows where all columns are empty
            df = df[df[col] != '']
        
        # Combine all columns into a single list of words, maintaining column order
        all_words = []
        # Process each column in order
        for col in df.columns:
            words = df[col].tolist()
            # Clean each word
            cleaned_words = []
            for word in words:
                word = word.strip()
                if word:
                    # Remove 'OR ' prefix if it exists
                    if word.startswith('OR '):
                        word = word[3:].strip()
                    # Remove asterisks
                    word = word.replace('*', '')
                    cleaned_words.append(word)
            all_words.extend(cleaned_words)
        
        # Create a new DataFrame with a single column
        words_df = pd.DataFrame(all_words, columns=['Word'])
        
        # Remove duplicates while preserving order
        words_df = words_df.drop_duplicates(keep='first')
        
        # Save to a new clean CSV
        words_df.to_csv('spelling_words_clean.csv', index=False)
        
        # Clean up the temporary file
        os.unlink(temp_csv.name)
        
        print("Successfully extracted words and saved to 'spelling_words_clean.csv'")
        print(f"Total unique words: {len(words_df)}")
        
    except Exception as e:
        print(f"Error extracting words: {str(e)}")

if __name__ == "__main__":
    extract_words() 