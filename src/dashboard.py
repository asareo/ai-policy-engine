import streamlit as st
import pandas as pd
import sqlite3
import os
from pipeline import ingest_policy_document, init_database

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'policy_data.db')

def load_dashboard_data():
    """Pulls analytical summaries and dataframes from SQLite using Pandas joins."""
    conn = sqlite3.connect(DB_PATH)
    
    query_chunks = """
        SELECT c.doc_title, c.jurisdiction, d.chunk_index, d.raw_text, d.risk_flag_count, d.evaluation_status
        FROM document_chunks d
        JOIN compliance_documents c ON d.doc_id = c.doc_id
    """
    df_chunks = pd.read_sql_query(query_chunks, conn)
    
    query_summary = """
        SELECT 
            COUNT(DISTINCT doc_id) as total_docs,
            COUNT(chunk_id) as total_chunks,
            SUM(risk_flag_count) as total_risks
        FROM document_chunks
    """
    df_summary = pd.read_sql_query(query_summary, conn)
    
    conn.close()
    return df_chunks, df_summary

# Ensure tables are built prior to front-end canvas painting
init_database()

st.set_page_config(page_title="AI Policy Compliance & Eval Engine", layout="wide")
st.title("AI Policy Compliance & Model Evaluation Engine")
st.markdown("This interface serves as an operational monitoring system to parse legislative frameworks and execute automated safety evaluations.")

# --- SIDEBAR REGULATORY INGESTION PORTAL ---
with st.sidebar:
    st.header("Ingest Policy Framework")
    st.markdown("Upload raw data logs or compliance parameters to compile values.")
    
    with st.form(key="ingestion_form", clear_on_submit=True):
        new_title = st.text_input("Framework / Evaluation Suite Title")
        new_jurisdiction = st.text_input("Operational Jurisdiction")
        uploaded_file = st.file_uploader("Select Text File (.txt)", type=["txt"])
        
        submit_button = st.form_submit_button(label="Execute Pipeline Processing")
        
    if submit_button:
        if not new_title or not new_jurisdiction or not uploaded_file:
            st.sidebar.warning("Please populate all text configurations and file buffers.")
        else:
            try:
                # Process the file byte stream natively
                raw_text_content = uploaded_file.read().decode("utf-8")
                
                if not raw_text_content.strip():
                    st.sidebar.error("Upload Error: Target text file is completely empty.")
                else:
                    ingest_policy_document(title=new_title, jurisdiction=new_jurisdiction, full_text=raw_text_content)
                    st.sidebar.success(f"Successfully processed framework records.")
                    st.rerun()
            except Exception as e:
                st.sidebar.error(f"Pipeline Fault Encountered: {e}")

# --- ANALYTICS DISPLAY INTERFACE ---
try:
    df_chunks, df_summary = load_dashboard_data()
    
    total_docs = int(df_summary['total_docs'].iloc[0]) if not df_summary.empty else 0
    total_chunks = int(df_summary['total_chunks'].iloc[0]) if not df_summary.empty else 0
    total_risks = int(df_summary['total_risks'].iloc[0]) if not df_summary.empty else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Monitored Evaluation Suites", value=total_docs)
    with col2:
        st.metric(label="Total Paragraph Units Evaluated", value=total_chunks)
    with col3:
        st.metric(label="Aggregated Safety Risk Violations", value=total_risks)

    st.divider()

    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.subheader("Model Evaluation Status Metrics")
        if not df_chunks.empty:
            # Display breakdown metrics of model evaluation counts
            status_summary = df_chunks['evaluation_status'].value_counts()
            st.dataframe(status_summary, use_container_width=True)
        else:
            st.info("No active validation data metrics found.")

    with right_col:
        st.subheader("Regional Framework Distribution")
        if not df_chunks.empty:
            jurisdiction_counts = df_chunks['jurisdiction'].value_counts()
            st.dataframe(jurisdiction_counts, use_container_width=True)
        else:
            st.info("No jurisdictional datasets mapped.")

    st.divider()
    st.subheader("Granular Compliance & Evaluation Records Log")
    if not df_chunks.empty:
        st.dataframe(df_chunks, use_container_width=True, hide_index=True)
    else:
        st.warning("The operational relational log matrix is currently blank.")

except Exception as e:
    st.error(f"UI Interface Error accessing backend storage schema: {e}")