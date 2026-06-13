import sqlite3
import os

# Define the absolute path to where our database file will live
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'policy_data.db')

def get_db_connection():
    """Establishes and returns a direct connection to our SQLite database file."""
    conn = sqlite3.connect(DB_PATH)
    # This configuration line allows us to interact with rows like dictionaries (by column name)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Creates the structural policy tables inside the database if they don't exist yet."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Table 1: Stores the baseline metadata of parsed AI regulatory policy files
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compliance_documents (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_title TEXT NOT NULL,
            jurisdiction TEXT NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Table 2: Stores individual data segments (chunks) mapped back to the parent document
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_chunks (
            chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            chunk_index INTEGER NOT NULL,
            raw_text TEXT NOT NULL,
            risk_flag_count INTEGER DEFAULT 0,
            FOREIGN KEY (doc_id) REFERENCES compliance_documents (doc_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database structures successfully verified/initialized.")

def audit_text_for_risks(text):
    """
    Scans a string of text for specific policy risk keywords.
    Returns the total count of risk terms found.
    """
    # A list of regulatory keywords an AI compliance officer would track
    risk_keywords = ["liability", "penalty", "restriction", "violation", "non-compliance", "prohibited", "fine"]
    
    count = 0
    # Clean up the text to lowercase so we don't miss words capitalized at the start of sentences
    lower_text = text.lower()
    
    for word in risk_keywords:
        # Count how many times each word appears in this specific chunk
        count += lower_text.count(word)
        
    return count

def ingest_policy_document(title, jurisdiction, full_text):
    """
    Takes a raw policy text document, breaks it down into structured paragraphs (chunks),
    audits each chunk for safety risks, and saves everything to the SQLite database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Insert the parent document metadata into our compliance_documents table
    cursor.execute('''
        INSERT INTO compliance_documents (doc_title, jurisdiction)
        VALUES (?, ?)
    ''', (title, jurisdiction))
    
    # Grab the automatically generated doc_id assigned to this new file row
    doc_id = cursor.lastrowid
    
    # 2. Split the text into logical chunks (we will split on double-newlines to isolate paragraphs)
    paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
    
    print(f"\n--- Processing Document: '{title}' ({len(paragraphs)} paragraphs detected) ---")
    
    # 3. Loop through every paragraph, audit it, and insert it as a distinct segment
    for index, paragraph in enumerate(paragraphs):
        # Run our auditing scanner to count risk flags
        risk_flags = audit_text_for_risks(paragraph)
        
        # Insert into our document_chunks table, linking it to the parent doc via foreign key
        cursor.execute('''
            INSERT INTO document_chunks (doc_id, chunk_index, raw_text, risk_flag_count)
            VALUES (?, ?, ?, ?)
        ''', (doc_id, index, paragraph, risk_flags))
        
        print(f" -> Chunk {index} processed. Risk flags found: {risk_flags}")
        
    # Save the database transactions and close our connection securely
    conn.commit()
    conn.close()
    print(f"Successfully committed document transaction to policy_data.db.\n")

if __name__ == "__main__":
    # Ensure our structural tables are created first
    init_database()
    
    # This mock string simulates a messy, multi-paragraph AI policy brief
    mock_policy_document = (
        "The Frontier Artificial Intelligence Safety Framework establishes basic operational rules. "
        "Companies building foundation systems must maintain absolute data integrity records.\n\n"
        
        "Any strict restriction placed on data mining protocols will trigger an internal review. "
        "Failure to register high-risk models constitutes a severe compliance violation, "
        "potentially resulting in a significant financial penalty or a massive fine for the organization.\n\n"
        
        "Operational parameters require cross-functional stakeholder transparency. "
        "If non-compliance occurs, external legal liability clauses will take structural effect."
    )
    
    # Run our ingestion pipeline using the mock policy text
    ingest_policy_document(
        title="US Executive Order on Frontier AI Development",
        jurisdiction="United States",
        full_text=mock_policy_document
    )