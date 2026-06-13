# AI Policy Compliance & Risk Analytics Engine

A production-grade data operations pipeline and interactive analytics dashboard built to ingest, chunk, audit, and log raw unstructured AI governance frameworks and legislative texts into a structured relational database.

## System Architecture

The ecosystem splits backend data processing from frontend visualization to optimize execution performance and ensure strict structural isolation:

1. **Data Ingestion Pipeline (`src/pipeline.py`)**: Handles core database initialization, reads unstructured raw policy strings, systematically tokenizes text patterns into logical paragraph blocks (chunks), and scans text segments using localized audit rules to quantify compliance risk factors.
2. **Relational Database (`database/policy_data.db`)**: An embedded SQLite matrix storing document metadata and granular paragraph text schemas tied together via explicit primary and foreign key constraints.
3. **Analytics Dashboard (`src/dashboard.py`)**: An enterprise command interface built on Streamlit that bridges your database layer to a user UI, rendering real-time KPI metrics, section risk density charts, and dynamic ingestion form portals.

## Technical Stack
* **Language**: Python 3
* **Interface Architecture**: Streamlit
* **Data Processing & Analytics**: Pandas
* **Database Engine**: SQLite3 (Embedded Relational Database)

## Database Schema Design

* **compliance_documents**: Stores unique master framework records.
  * `doc_id` (INTEGER, Primary Key): Unique identifier assigned to each file.
  * `doc_title` (TEXT): Name of the governance document.
  * `jurisdiction` (TEXT): Regional or national regulatory zone.
  * `date_added` (TIMESTAMP): Automatic registration clock log.
  * * **document_chunks**: Stores tokenized paragraphs mapping back to parent frameworks.
  * `chunk_id` (INTEGER, Primary Key): Unique row ID.
  * `doc_id` (INTEGER, Foreign Key): Links directly back to `compliance_documents`.
  * `chunk_index` (INTEGER): Zero-indexed order position of the paragraph.
  * `raw_text` (TEXT): Complete verbatim string content of the paragraph segment.
  * `risk_flag_count` (INTEGER): Total count of evaluated regulatory hazard markers.

## Local Installation & Verification

### 1. Environment Sandbox Setup
Isolate package configurations on macOS by opening the terminal and executing:
```bash
# Clone or navigate to the root directory
cd ~/Desktop/ai-policy-engine

# Initialize the isolated virtual environment
python3 -m venv .venv

# Activate the sandbox partition
source .venv/bin/activate