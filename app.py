import os
import requests
import streamlit as st

# Configure page layout and style
st.set_page_config(
    page_title="BMW Service Knowledge Assistant",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .source-card {
        background-color: #F3F4F6;
        border-left: 4px solid #1E3A8A;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 4px;
    }
    .badge-score {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


def check_backend_health():
    """Fetches backend health status."""
    try:
        res = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if res.status_code == 200:
            return True, res.json()
        return False, None
    except Exception:
        return False, None


def fetch_documents():
    """Fetches list of indexed documents."""
    try:
        res = requests.get(f"{BACKEND_URL}/documents", timeout=3)
        if res.status_code == 200:
            return res.json().get("documents", [])
        return []
    except Exception:
        return []


# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/bmw.png", width=64)
    st.title("System Status & Docs")

    backend_online, health_info = check_backend_health()

    if backend_online:
        st.success("🟢 Backend API: Online")
        st.info(f"🤖 LLM Model: `{health_info.get('ollama_model', 'qwen2.5:1.5b')}`")
        if health_info.get("vector_store_status") == "ready":
            st.caption("⚡ Vector Store: Ready")
        else:
            st.caption("⚠️ Vector Store: Empty / Not Ingested")
    else:
        st.error("🔴 Backend API: Offline")
        st.caption(f"Cannot reach `{BACKEND_URL}`. Make sure Uvicorn backend is running.")

    st.divider()

    # Document Upload Section
    st.subheader("📁 Upload Service Documents")
    uploaded_file = st.file_uploader(
        "Choose PDF, TXT, or DOCX file",
        type=["pdf", "txt", "docx"],
        help="Upload BMW service manuals or procedures to index"
    )

    if uploaded_file is not None:
        if st.button("Upload & Ingest File", type="primary", use_container_width=True):
            with st.spinner("Indexing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    res = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=60)
                    if res.status_code == 200:
                        data = res.json()
                        st.success(f"Ingested `{data.get('filename')}` into {data.get('chunks_count')} chunks!")
                        st.rerun()
                    else:
                        st.error(f"Error: {res.json().get('detail', 'Upload failed')}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")

    st.divider()

    # Ingest Sample Data Button
    st.subheader("⚙️ Sample Knowledge Base")
    if st.button("Ingest Sample Documents", use_container_width=True):
        with st.spinner("Ingesting sample documents..."):
            try:
                res = requests.post(f"{BACKEND_URL}/ingest", timeout=60)
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"Ingested {data.get('documents_count')} files into {data.get('chunks_count')} vector chunks!")
                    st.rerun()
                else:
                    st.error(f"Failed to ingest: {res.text}")
            except Exception as e:
                st.error(f"Failed to connect: {e}")

    # Currently Indexed Documents List
    docs_list = fetch_documents()
    if docs_list:
        st.write("---")
        st.subheader("Indexed Documents")
        for d in docs_list:
            st.text(f"• {d['filename']} ({d['total_chunks']} chunks)")

    st.divider()

    # Preferences & Debug Mode
    st.subheader("Settings")
    debug_mode = st.toggle("Enable Debug Mode", value=False, help="Show retrieval similarity scores and chunk IDs")


# --- MAIN CONTENT AREA ---
st.markdown('<div class="main-header">BMW Service Knowledge Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered grounded service documentation assistant for BMW technicians</div>', unsafe_allow_html=True)

# Preset Questions Shortcuts
st.write("##### 💡 Example Diagnostic Questions")
col1, col2, col3 = st.columns(3)

preset_question = None
if col1.button("EV Battery Overheating Checks", use_container_width=True):
    preset_question = "What should be checked when an EV reports repeated battery overheating?"

if col2.button("Charging System Faults", use_container_width=True):
    preset_question = "What are the recommended checks for a charging system fault?"

if col3.button("Thermal Management Checks", use_container_width=True):
    preset_question = "What diagnostic steps are listed for a battery thermal management issue?"

# Question Input Form
with st.form(key="qa_form", clear_on_submit=False):
    default_text = preset_question if preset_question else ""
    user_query = st.text_area(
        "Ask a service or technical diagnostic question:",
        value=default_text,
        height=100,
        placeholder="e.g. What should be checked when an EV reports repeated battery overheating?"
    )
    submit_button = st.form_submit_button("Submit Question", type="primary", use_container_width=True)

if submit_button or preset_question:
    query_text = user_query.strip() if user_query else preset_question
    if not query_text:
        st.warning("Please enter a technical service question.")
    elif not backend_online:
        st.error("Backend service is offline. Please start the Uvicorn FastAPI server.")
    else:
        with st.spinner("Searching BMW service documentation & generating answer via local Ollama LLM..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/query",
                    json={"question": query_text},
                    timeout=90
                )
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "")
                    sources = data.get("sources", [])

                    st.markdown("### 📋 Answer")
                    st.markdown(answer)

                    st.write("---")
                    st.markdown("### 📚 Supporting Sources")

                    if sources:
                        for idx, src in enumerate(sources, start=1):
                            doc_name = src.get("document", "Unknown")
                            page_num = src.get("page", 1)
                            score = src.get("score", 0.0)

                            score_html = f'<span class="badge-score">Score: {score:.2f}</span>' if debug_mode else ''

                            with st.expander(f"Source {idx}: {doc_name} — Page {page_num}", expanded=True):
                                st.markdown(f"**Document**: `{doc_name}` | **Page**: `{page_num}` {score_html}", unsafe_allow_html=True)
                                if debug_mode:
                                    st.caption(f"Chunk ID: `{src.get('chunk_id')}` | Format: `{src.get('document_type')}`")
                    else:
                        st.info("No explicit source citations were returned for this question.")

                else:
                    st.error(f"Error from server: {res.json().get('detail', 'Unknown error')}")

            except requests.exceptions.Timeout:
                st.error("Request timed out. Please verify local Ollama LLM response time.")
            except Exception as e:
                st.error(f"Failed to submit question: {e}")
