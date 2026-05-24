import sqlite3
import json

#Take in three pieces of information(Who/What/Which agent/What the system knows at that moment)
#connects to the SQLite database
#It checks if the audit_log table exists. If missing, it creates one
#Clean the state data by removing the long chat messages, keep the essential metadata, make the log easier to read and save
#Converting to Text
#The "Append-Only rule - only insert
#Save the entry permanently and closes the database connection

def log_event(request_id: str, node_name: str, state_snapshot: dict):
    """
    Records a snapshot of the graph state at a specific node.
    Enforced as append-only by only using INSERT.
    """
    conn = sqlite3.connect("data/hr_platform.db")
    cursor = conn.cursor()
    
    # 1. Create the Audit Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS audit_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        request_id TEXT,
                        node_name TEXT,
                        state_data TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                     )''')
    
    # 2. Convert state dictionary to a JSON string for storage
    clean_state = {k: v for k, v in state_snapshot.items() if k != "messages"}
    state_json = json.dumps(clean_state)
    
    # 3. Append the record (INSERT ONLY)
    cursor.execute(
        "INSERT INTO audit_log (request_id, node_name, state_data) VALUES (?, ?, ?)",
        (request_id, node_name, state_json)
    )
    
    conn.commit()
    conn.close()

""""
def leave_agent(state: dict):
    # Perform work...
    response = "Leave processed."
    
    # Log the action before returning
    log_event(state.get("request_id", "unknown"), "leave_agent", state)
    
    return {"final_output": response}
"""