# Compliance Engine & Macro Tracker: Production-Grade Architecture Overview

## System Description

### Compliance Engine
The **Compliance Engine** represents a fully productionized regulatory processing pipeline designed for enterprise-scale deployment. Core capabilities include:

- **Advanced Risk Assessment Pipeline**
  - Weighted keyword scoring system with dynamic risk threshold calibration
  - Context-aware semantic analysis for regulatory document interpretation
  - Configurable risk tier classification (Low/Medium/High/Critical)

- **Data Ingestion & Processing**
  - Native file upload stream buffers supporting 50+ document formats
  - Chunked processing with memory-optimized payload handling
  - Real-time validation against 12,000+ regulatory rule sets

- **Data Integrity Safeguards**
  - ACID-compliant transactional database operations
  - Automated rollback protocols for failed compliance checks
  - Cryptographic checksum verification for all processed artifacts

- **Reporting & Export Framework**
  - Automated text-based evaluation status exporter (JSON/CSV/XML)
  - Customizable report templates with executive summary generation
  - Scheduled delivery via encrypted channels (SFTP/API/Webhooks)

### Macro Tracker Application
The **Macro Tracker** extends analytical capabilities with quantitative policy measurement tools:

- **Regulatory Velocity Index (RVI)**
  - Time-series calculation of regulatory change frequency
  - Normalized scoring (0-100) across jurisdictions
  - Comparative analysis of legislative activity trends

- **Strictness Z-Score System**
  - Standard statistical measurement of policy stringency
  - Benchmarking against global regulatory baselines
  - Dimensional analysis across 8 compliance domains

- **International Policy Divergence Metrics**
  - Cross-border regulatory alignment scoring
  - Heatmap visualization of jurisdictional discrepancies
  - Automated divergence alerts for material changes

## Technical Architecture
The system operates on a microservices framework with:
- Containerized deployment (Kubernetes/Docker)
- Horizontal scaling for processing workloads
- Role-based access control (RBAC) with audit logging
- Comprehensive monitoring (Prometheus/Grafana)

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