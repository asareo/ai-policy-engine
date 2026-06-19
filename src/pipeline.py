import sqlite3
import os

# Define universal project path routing
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'policy_data.db')
REPORT_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'compliance_report.txt')

def get_db_connection():
    """Establishes a connection to the SQLite database file."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initializes schema tables with model evaluation columns."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Master Table: Tracks legislative frameworks/model evaluation suites
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compliance_documents (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_title TEXT NOT NULL UNIQUE,
            jurisdiction TEXT NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Segment Table: Stores chunks along with automated evaluation tags
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_chunks (
            chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            chunk_index INTEGER NOT NULL,
            raw_text TEXT NOT NULL,
            risk_flag_count INTEGER DEFAULT 0,
            evaluation_status TEXT DEFAULT 'PASS',
            FOREIGN KEY (doc_id) REFERENCES compliance_documents (doc_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def evaluate_safety_tier(risk_count):
    """
    Model Evaluation Matrix (DeepMind Focus): Categorizes data segments
    based on internal risk density thresholds.
    """
    if risk_count == 0:
        return "PASS"
    elif 1 <= risk_count <= 2:
        return "NEEDS_REVIEW"
    else:
        return "FAIL"

def audit_text_for_risks(text):
    """Audits text strings for critical regulatory risk keywords with weighted scoring."""
    risk_keywords = {
        "prohibited": 3,
        "violation": 3,
        "penalty": 3,
        "liability": 1,
        "restriction": 1,
        "non-compliance": 1,
        "fine": 1
    }
    total_score = 0
    lower_text = text.lower()
    for word, weight in risk_keywords.items():
        total_score += lower_text.count(word) * weight
    return total_score

def ingest_policy_document(title, jurisdiction, full_text):
    """
    Robust Ingestion Engine: Slices text files, parses strings, executes
    evaluations, and enforces database transactional rollbacks if faults occur.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Enforce transaction boundary isolation
        cursor.execute("BEGIN TRANSACTION")
        
        # Insert parent file metadata
        cursor.execute('''
            INSERT INTO compliance_documents (doc_title, jurisdiction)
            VALUES (?, ?)
        ''', (title, jurisdiction))
        
        doc_id = cursor.lastrowid
        
        # Advanced Slicing: Split on newlines, clean whitespace, and filter out blank spacing lines
        paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
        
        for index, paragraph in enumerate(paragraphs):
            risk_flags = audit_text_for_risks(paragraph)
            
            # Run model evaluation classification rule
            eval_status = evaluate_safety_tier(risk_flags)
            
            # Write structured chunk row linked to foreign key parent
            cursor.execute('''
                INSERT INTO document_chunks (doc_id, chunk_index, raw_text, risk_flag_count, evaluation_status)
                VALUES (?, ?, ?, ?, ?)
            ''', (doc_id, index, paragraph, risk_flags, eval_status))
            
        # If all steps complete successfully, commit changes to disk
        conn.commit()
        print(f"Transaction Success: Ingested '{title}' successfully.")
        
    except sqlite3.IntegrityError:
        conn.rollback()
        print(f"Transaction Aborted: Duplicate framework conflict detected for '{title}'.")
        raise Exception("Database conflict: Framework title already exists.")
    except Exception as e:
        conn.rollback()
        print(f"System Rollback Executed due to internal pipeline exception: {e}")
        raise e
    finally:
        conn.close()

def export_compliance_report():
    """
    Generates a compliance report by querying all document chunks,
    grouping them by evaluation status, and writing a summary to a text file.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query all chunks grouped by evaluation status
        cursor.execute('''
            SELECT evaluation_status, COUNT(*) as count
            FROM document_chunks
            GROUP BY evaluation_status
        ''')

        status_counts = cursor.fetchall()

        # Create report directory if it doesn't exist
        os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

        # Write the report to file
        with open(REPORT_PATH, 'w') as report_file:
            report_file.write("COMPLIANCE EVALUATION REPORT\n")
            report_file.write("============================\n\n")
            report_file.write("Summary of Document Chunk Evaluations:\n\n")

            total_chunks = 0
            for row in status_counts:
                status = row['evaluation_status']
                count = row['count']
                total_chunks += count
                report_file.write(f"{status}: {count} chunks\n")

            report_file.write("\n")
            report_file.write(f"Total chunks evaluated: {total_chunks}\n")
            report_file.write(f"Report generated on: {sqlite3.datetime.datetime.now()}\n")

        print(f"Compliance report generated successfully at {REPORT_PATH}")

    except Exception as e:
        print(f"Error generating compliance report: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
    print("Database system structures verified.")
    # Execute the automated compilation report
    export_compliance_report()