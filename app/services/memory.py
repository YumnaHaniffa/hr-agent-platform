import sqlite3
#1.The function first looks at the score (importance) assigned by the AI.
#2.Connecting to the Database
#3.It checks if a "Long-Term Memory" (LTM) table exists. If it doesn’t, it creates one automatically

#4.Recording the Fact: It writes three things into the database:
#Who: who this memory belongs to
#What: the actual information to remember
#When: A timestamp (when it happened)

#5. It prints a message saying "Memory promoted to LTM," letting you know the transition from temporary chat to permanent memory was successful.

def save_to_ltm(user_id: str, content: str, score: float):
    """
    Saves information to the Long-Term Memory table if significance is high.
    """
    # Requirement: Sound and justified significance scoring logic
    if score < 0.8:
        return  # Do not save low-importance chatter

    conn = sqlite3.connect("data/hr_platform.db")
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS ltm 
                     (user_id TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    cursor.execute("INSERT INTO ltm (user_id, content) VALUES (?, ?)", (user_id, content))
    conn.commit()
    conn.close()
    print("Memory promoted to LTM.")