import streamlit as st
import pandas as pd
import sqlite3
from pipeline import ingest_policy_document
import os

# Define the absolute path to your active database file
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'policy_data.db')

def load_dashboard_data():
    """
    Connects to SQLite and pulls aggregated metrics and tables
    using Pandas to feed our visual components directly.
    """
    conn = sqlite3.connect(DB_PATH)
    
    # Query 1: Join both tables to see our text chunks along with their parent document title
    query_chunks = """
        SELECT c.doc_title, c.jurisdiction, d.chunk_index, d.raw_text, d.risk_flag_count
        FROM document_chunks d
        JOIN compliance_documents c ON d.doc_id = c.doc_id
    """
    df_chunks = pd.read_sql_query(query_chunks, conn)
    
    # Query 2: Get total summary stats across all ingested files
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

# --- STREAMLIT UI LAYOUT ---
# Set up a professional widescreen web page layout
st.set_page_config(page_title="AI Policy Compliance Analytics", layout="wide")

st.title("AI Policy Compliance & Risk Analytics Engine")
st.markdown("This operational command center displays structural risk auditing metrics compiled from ingested AI governance legislation.")

# --- SIDEBAR REGULATORY INGESTION HUB ---
with st.sidebar:
    st.header("Ingest New Legislation")
    st.markdown("Upload raw regulatory text frameworks directly to the data pipeline.")
    
    # Wrap elements inside a Streamlit Form so it waits for the click event before triggering a rerun
    with st.form(key="ingestion_form", clear_on_submit=True):
        new_title = st.text_input("Document Framework Title", placeholder="e.g., EU AI Act Safety Draft")
        new_jurisdiction = st.text_input("Regulatory Jurisdiction", placeholder="e.g., European Union")
        new_text = st.text_area("Paste Raw Policy Text", placeholder="Paste regulation text strings here...", height=200)
        
        submit_button = st.form_submit_button(label="Execute Pipeline Processing")
        
    # Form Processing Logic
    if submit_button:
        if new_title and new_jurisdiction and new_text:
            with st.spinner("Executing pipeline automation... cleaning text, chunking paragraphs, and auditing risk indices..."):
                # Call the core backend function you built yesterday!
                ingest_policy_document(title=new_title, jurisdiction=new_jurisdiction, full_text=new_text)
            st.success(f"Framework '{new_title}' successfully committed to SQLite storage matrix!")
            # Force Streamlit to rerun the entire script immediately so the tables update instantly on the screen
            st.rerun()
        else:
            st.warning("Operational Halt: Please verify all metadata and text content fields are populated.")


st.divider()

# 1. Load data from our background SQLite pipeline
try:
    df_chunks, df_summary = load_dashboard_data()
    
    # Extract baseline operational numbers from our summary dataframe
    total_docs = int(df_summary['total_docs'].iloc[0]) if not df_summary.empty else 0
    total_chunks = int(df_summary['total_chunks'].iloc[0]) if not df_summary.empty else 0
    total_risks = int(df_summary['total_risks'].iloc[0]) if not df_summary.empty else 0

    # 2. Display High-Level KPI Metric Cards side-by-side using Streamlit Columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Ingested Policy Frameworks", value=total_docs)
    with col2:
        st.metric(label="Total Paragraph Chunks Parsed", value=total_chunks)
    with col3:
        st.metric(label="Identified Regulatory Risk Flags", value=total_risks, delta="Action Required" if total_risks > 0 else "Clear")

    st.divider()

    # 3. Create a two-column dashboard splitting a visual chart from raw database lookups
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("Risk Flag Density by Paragraph Index")
        if not df_chunks.empty:
            # Create a simple bar chart showing which specific sections contain heavy risk concentrations
            chart_data = df_chunks.set_index('chunk_index')['risk_flag_count']
            st.bar_chart(chart_data)
        else:
            st.info("No paragraph tracking data available.")

    with right_col:
        st.subheader("Jurisdictional Breakdown")
        if not df_chunks.empty:
            # Render a clean summary table counting total rows per area
            jurisdiction_counts = df_chunks['jurisdiction'].value_counts()
            st.dataframe(jurisdiction_counts, use_container_width=True)
        else:
            st.info("No regional distribution metrics.")

    st.divider()

    # 4. Display the entire granular database grid at the bottom of the system
    st.subheader("Audited Compliance Database Logs")
    if not df_chunks.empty:
        # Render the full master dataframe inside an interactive spreadsheet UI component
        st.dataframe(df_chunks, use_container_width=True, hide_index=True)
    else:
        st.warning("The pipeline database is currently completely empty.")

except Exception as e:
    st.error(f"Error establishing interface bridge to data lake layer: {e}")

