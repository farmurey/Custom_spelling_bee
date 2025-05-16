import pandas as pd
import subprocess
import tempfile
import os

def convert_numbers_to_csv():
    """Convert Numbers file to CSV using AppleScript"""
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
        
        # Read the CSV and save it as a new file
        df = pd.read_csv(temp_csv.name)
        df.to_csv('spelling_words.csv', index=False)
        
        # Clean up the temporary file
        os.unlink(temp_csv.name)
        
        print("Successfully converted Numbers file to CSV!")
        print("Saved as 'spelling_words.csv'")
        
    except Exception as e:
        print(f"Error converting file: {str(e)}")

if __name__ == "__main__":
    convert_numbers_to_csv() 