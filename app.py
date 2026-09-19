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
EVALUATION_TIMEOUT = int(os.getenv("EVALUATION_TIMEOUT", "35"))

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .source-card {
        background-color: #F8FAFC;
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
    .badge-status-online {
        color: #15803D;
        font-weight: 600;
    }
    .badge-status-offline {
        color: #B91C1C;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

if "preset_input" not in st.session_state:
    st.session_state.preset_input = ""


def fetch_health():
    """Fetches backend health status."""
    try:
        res = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if res.status_code == 200:
            return True, res.json()
        return False, {}
    except Exception:
        return False, {}


def fetch_documents():
    """Fetches list of indexed documents."""
    try:
        res = requests.get(f"{BACKEND_URL}/documents", timeout=3)
        if res.status_code == 200:
            return res.json().get("documents", [])
        return []
    except Exception:
        return []


def fetch_query_history():
    """Fetches local query history."""
    try:
        res = requests.get(f"{BACKEND_URL}/history", timeout=3)
        if res.status_code == 200:
            return res.json().get("history", [])
        return []
    except Exception:
        return []


# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/bmw.png", width=56)
    st.title("System Monitor")

    backend_online, health_data = fetch_health()

    # SYSTEM STATUS
    st.subheader("SYSTEM STATUS")
    if backend_online:
        st.markdown("• **API**: 🟢")
        v_status = health_data.get("vector_store", "no_index")
        v_symbol = "🟢" if v_status == "ready" else "🔴"
        st.markdown(f"• **FAISS**: {v_symbol} (`{v_status}`)")

        e_status = health_data.get("embeddings", "ready")
        e_symbol = "🟢" if e_status == "ready" else "🔴"
        st.markdown(f"• **Embeddings**: {e_symbol}")

        o_status = health_data.get("ollama", "disconnected")
        o_symbol = "🟢" if o_status == "connected" else "🔴"
        st.markdown(f"• **Ollama**: {o_symbol} (`{o_status}`)")

        st.markdown(f"• **LLM**: 🟢 `{health_data.get('llm', 'qwen2.5:1.5b')}`")
    else:
        st.markdown("• **API**: 🔴")
        st.markdown("• **FAISS**: 🔴")
        st.markdown("• **Embeddings**: 🔴")
        st.markdown("• **Ollama**: 🔴")
        st.markdown("• **LLM**: 🔴")
        st.caption(f"Cannot connect to backend `{BACKEND_URL}`")

    st.divider()

    # KNOWLEDGE BASE METRICS
    st.subheader("KNOWLEDGE BASE")
    doc_count = health_data.get("documents_count", 0) if backend_online else 0
    chunk_count = health_data.get("chunks_count", 0) if backend_online else 0

    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Documents", doc_count)
    col_m2.metric("Chunks", chunk_count)

    if st.button("🔄 Refresh Knowledge Base", use_container_width=True):
        st.rerun()

    st.divider()

    # DOCUMENT MANAGEMENT QUICK ACTION
    st.subheader("DOCUMENT MANAGEMENT")
    uploaded_files = st.file_uploader(
        "Upload BMW Documentation",
        type=["pdf", "txt", "docx", "csv"],
        accept_multiple_files=True,
        help="Supported formats: PDF, TXT, DOCX, CSV"
    )

    if uploaded_files and st.button("Ingest Uploaded File(s)", type="primary", use_container_width=True):
        with st.spinner("Ingesting & indexing files..."):
            success_count = 0
            for file in uploaded_files:
                try:
                    files_payload = {"file": (file.name, file.getvalue(), file.type)}
                    res = requests.post(f"{BACKEND_URL}/upload", files=files_payload, timeout=60)
                    if res.status_code == 200:
                        success_count += 1
                except Exception as e:
                    st.error(f"Failed to ingest {file.name}: {e}")
            if success_count > 0:
                st.success(f"Successfully ingested {success_count} file(s)!")
                st.rerun()

    st.caption("Supported Formats: `.pdf`, `.txt`, `.docx`, `.csv`")

    st.divider()

    # SETTINGS
    st.subheader("SETTINGS")
    top_k_param = st.slider("Top K Chunks Retrieval", min_value=1, max_value=10, value=5)
    similarity_threshold_param = st.slider("Similarity Threshold", min_value=0.0, max_value=1.0, value=0.35, step=0.05)
    eval_timeout_param = st.number_input("Evaluation Per-Test Timeout (sec)", min_value=10, max_value=180, value=EVALUATION_TIMEOUT)
    debug_retrieval_mode = st.toggle("Debug Retrieval Mode", value=False)


# --- MAIN HEADER ---
st.markdown('<div class="main-header">BMW Service Knowledge Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered service documentation retrieval and diagnostic assistance</div>', unsafe_allow_html=True)

# TAB NAVIGATION
tab_chat, tab_dashboard, tab_history, tab_eval = st.tabs([
    "💬 Diagnostic Assistant",
    "📚 Knowledge Base Dashboard",
    "📜 Query History",
    "🧪 RAG Evaluation Benchmark"
])


# ==============================================================================
# TAB 1: DIAGNOSTIC ASSISTANT (CHAT INTERFACE)
# ==============================================================================
with tab_chat:
    col_hdr1, col_hdr2 = st.columns([4, 1])
    with col_hdr2:
        if st.button("🧹 Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.write("##### 💡 Suggested Diagnostic Questions")
    preset_col1, preset_col2, preset_col3 = st.columns(3)

    if preset_col1.button("EV Battery Overheating Checks", use_container_width=True):
        st.session_state.preset_input = "What should be checked when an EV reports repeated battery overheating?"

    if preset_col2.button("Charging System Faults", use_container_width=True):
        st.session_state.preset_input = "What are the recommended checks for a charging system fault?"

    if preset_col3.button("CP & PP Signal Verification", use_container_width=True):
        st.session_state.preset_input = "How should CP and PP signals be verified?"

    preset_col4, preset_col5 = st.columns(2)
    if preset_col4.button("Battery Cooling Circuit Checks", use_container_width=True):
        st.session_state.preset_input = "What checks should be performed on the battery cooling circuit?"

    if preset_col5.button("HV Insulation Test Prerequisites", use_container_width=True):
        st.session_state.preset_input = "What should be checked before performing an HV insulation test?"

    st.write("---")

    # Render Chat History
    for m_idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                grounding_val = msg.get("grounding", "HIGH")
                sources_cnt = len(msg.get("sources", []))
                g_color = "🟢" if grounding_val == "HIGH" else ("🟡" if grounding_val == "MEDIUM" else "🔴")
                st.caption(f"**Grounding**: {g_color} `{grounding_val}` | **Sources**: `{sources_cnt}`")

            if "sources" in msg and msg["sources"]:
                st.markdown("#### 📚 Supporting Sources")
                for idx, src in enumerate(msg["sources"], start=1):
                    doc_name = src.get("document", "Unknown")
                    page_num = src.get("page", 1)
                    score = src.get("score", 0.0)
                    doc_type = src.get("document_type", "TXT")
                    score_html = f'<span class="badge-score">Relevance: {score:.2f}</span>'

                    with st.expander(f"Source {idx}: {doc_name} — Page {page_num}", expanded=False):
                        st.markdown(f"**Document**: `{doc_name}` | **Type**: `{doc_type}` | **Page**: `{page_num}` {score_html}", unsafe_allow_html=True)
                        if debug_retrieval_mode:
                            st.caption(f"Chunk ID: `{src.get('chunk_id')}`")
                            if src.get("snippet"):
                                st.caption(f"Snippet: {src.get('snippet')}")

            if msg["role"] == "assistant" and backend_online and "sources" in msg:
                # Feedback widget
                fb_key = f"fb_{m_idx}"
                col_f1, col_f2, col_f3 = st.columns([1, 1, 8])
                if col_f1.button("👍", key=f"up_{fb_key}", help="Was this answer helpful?"):
                    try:
                        requests.post(f"{BACKEND_URL}/feedback", json={
                            "query": st.session_state.messages[m_idx - 1]["content"] if m_idx > 0 else "Query",
                            "answer": msg["content"],
                            "helpful": True
                        }, timeout=3)
                        st.toast("Thank you for your feedback! 👍")
                    except Exception:
                        pass
                if col_f2.button("👎", key=f"down_{fb_key}", help="Was this answer unhelpful?"):
                    try:
                        requests.post(f"{BACKEND_URL}/feedback", json={
                            "query": st.session_state.messages[m_idx - 1]["content"] if m_idx > 0 else "Query",
                            "answer": msg["content"],
                            "helpful": False,
                            "reason": "Needs improvement"
                        }, timeout=3)
                        st.toast("Feedback recorded! 👎")
                    except Exception:
                        pass

    # Chat Input Box
    default_text = st.session_state.preset_input
    user_query = st.chat_input("Ask a service diagnostic question...", key="chat_input_widget")

    if not user_query and default_text:
        user_query = default_text
        st.session_state.preset_input = ""

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            if not backend_online:
                err_msg = "Backend API service is offline. Please start Uvicorn backend server."
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})
            else:
                with st.spinner("Searching BMW service documentation & generating answer via local Ollama LLM..."):
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/query",
                            json={
                                "question": user_query,
                                "top_k": top_k_param,
                                "similarity_threshold": similarity_threshold_param
                            },
                            timeout=90
                        )
                        if res.status_code == 200:
                            data = res.json()
                            answer = data.get("answer", "")
                            sources = data.get("sources", [])
                            grounding_val = data.get("grounding", "HIGH")

                            st.markdown(answer)
                            g_color = "🟢" if grounding_val == "HIGH" else ("🟡" if grounding_val == "MEDIUM" else "🔴")
                            st.caption(f"**Grounding**: {g_color} `{grounding_val}` | **Sources**: `{len(sources)}`")

                            if sources:
                                st.markdown("#### 📚 Supporting Sources")
                                for idx, src in enumerate(sources, start=1):
                                    doc_name = src.get("document", "Unknown")
                                    page_num = src.get("page", 1)
                                    score = src.get("score", 0.0)
                                    doc_type = src.get("document_type", "TXT")
                                    score_html = f'<span class="badge-score">Relevance: {score:.2f}</span>'

                                    with st.expander(f"Source {idx}: {doc_name} — Page {page_num}", expanded=True):
                                        st.markdown(f"**Document**: `{doc_name}` | **Type**: `{doc_type}` | **Page**: `{page_num}` {score_html}", unsafe_allow_html=True)
                                        if debug_retrieval_mode:
                                            st.caption(f"Chunk ID: `{src.get('chunk_id')}`")
                                            if src.get("snippet"):
                                                st.caption(f"Snippet: {src.get('snippet')}")

                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer,
                                "sources": sources,
                                "grounding": grounding_val
                            })
                        else:
                            err_text = f"Server error: {res.json().get('detail', 'Unknown error')}"
                            st.error(err_text)
                            st.session_state.messages.append({"role": "assistant", "content": err_text})

                    except requests.exceptions.Timeout:
                        err_text = "Request timed out. Please verify local Ollama LLM response time."
                        st.error(err_text)
                        st.session_state.messages.append({"role": "assistant", "content": err_text})
                    except Exception as e:
                        err_text = f"Error communicating with backend: {e}"
                        st.error(err_text)
                        st.session_state.messages.append({"role": "assistant", "content": err_text})


# ==============================================================================
# TAB 2: KNOWLEDGE BASE DASHBOARD
# ==============================================================================
with tab_dashboard:
    st.subheader("Knowledge Base Overview & Documents Table")

    kb_docs = fetch_documents()

    col_kb1, col_kb2, col_kb3, col_kb4 = st.columns(4)
    col_kb1.metric("Total Documents", len(kb_docs))
    col_kb2.metric("Total Chunks", chunk_count)
    col_kb3.metric("Vector Index", "Ready" if v_status == "ready" else "Empty")
    col_kb4.metric("Formats Supported", "PDF, TXT, DOCX, CSV")

    st.write("---")
    st.subheader("Indexed Documents")

    if kb_docs:
        for idx, doc in enumerate(kb_docs, start=1):
            col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns([3, 1, 1, 1, 1])
            col_d1.write(f"📄 **{doc['filename']}**")
            col_d2.write(f"Type: `{doc['document_type']}`")
            col_d3.write(f"Pages: `{doc['pages_count']}`")
            col_d4.write(f"Chunks: `{doc['total_chunks']}`")

            if col_d5.button("🗑️ Delete", key=f"del_doc_{idx}"):
                with st.spinner(f"Deleting '{doc['filename']}'..."):
                    try:
                        res = requests.delete(f"{BACKEND_URL}/documents/{doc['filename']}", timeout=10)
                        if res.status_code == 200:
                            st.success(f"Deleted {doc['filename']}")
                            st.rerun()
                        else:
                            st.error(f"Delete failed: {res.text}")
                    except Exception as e:
                        st.error(f"Error deleting: {e}")
    else:
        st.info("No documents are currently indexed in the FAISS vector store.")

    st.write("---")
    st.subheader("Bulk Ingestion / Sample Re-indexing")
    if st.button("Re-index Sample Knowledge Base Directory", type="secondary"):
        with st.spinner("Re-indexing sample documents..."):
            try:
                res = requests.post(f"{BACKEND_URL}/ingest", timeout=60)
                if res.status_code == 200:
                    st.success("Re-indexed sample knowledge base!")
                    st.rerun()
            except Exception as e:
                st.error(f"Re-index failed: {e}")


# ==============================================================================
# TAB 3: QUERY HISTORY
# ==============================================================================
with tab_history:
    st.subheader("Recent Technician Query Log")

    history_records = fetch_query_history()

    if history_records:
        for idx, item in enumerate(history_records, start=1):
            ts = item.get("timestamp", "").replace("T", " ")[:19]
            q = item.get("question", "")
            status_val = item.get("status", "success")
            sources_cnt = item.get("sources_count", 0)

            status_badge = "🟢 Success" if status_val == "success" else "🟡 Fallback"

            with st.expander(f"Query #{idx}: '{q[:60]}...' | {ts} | {status_badge}", expanded=False):
                st.markdown(f"**Timestamp**: `{ts}`")
                st.markdown(f"**Technician Question**: {q}")
                st.markdown(f"**Grounded Answer**: {item.get('answer')}")
                st.markdown(f"**Retrieved Sources Count**: {sources_cnt}")
                if item.get("retrieved_documents"):
                    st.markdown(f"**Retrieved Documents**: `{', '.join(item.get('retrieved_documents'))}`")
    else:
        st.info("No query history recorded yet.")


# ==============================================================================
# TAB 4: RAG EVALUATION BENCHMARK (ITEM-BY-ITEM WITH REAL-TIME PROGRESS)
# ==============================================================================
with tab_eval:
    st.subheader("Automated RAG Evaluation & Grounding Benchmark")
    st.write("Executes the RAG benchmark test suite item-by-item against the production `/query` pipeline with live progress reporting and graceful per-test timeout handling.")

    if st.button("🚀 Run RAG Benchmark Suite", type="primary"):
        # Step 1: Fetch benchmark dataset
        dataset = []
        try:
            ds_res = requests.get(f"{BACKEND_URL}/evaluate/dataset", timeout=5)
            if ds_res.status_code == 200:
                dataset = ds_res.json().get("dataset", [])
        except Exception:
            pass

        if not dataset:
            from src.ai.evaluation import BENCHMARK_DATASET
            dataset = BENCHMARK_DATASET

        total_tests = len(dataset)
        results = []
        passed_count = 0
        timeout_count = 0
        failed_count = 0

        # UI Progress elements
        progress_bar = st.progress(0.0)
        status_box = st.empty()

        for idx, test_case in enumerate(dataset, start=1):
            tc_id = test_case.get("id", f"TC-00{idx}")
            q = test_case.get("question", "")

            # Update status box
            status_box.info(
                f"**Evaluating Test {idx}/{total_tests}** (`{tc_id}`)\n\n"
                f"**Question**: *{q}*\n\n"
                f"Completed: **{idx-1}/{total_tests}** | Passed: **{passed_count}** | Timed out: **{timeout_count}** | Failed: **{failed_count}**"
            )

            test_result = None

            # Execute single test case with timeout handling
            try:
                tc_res = requests.post(
                    f"{BACKEND_URL}/evaluate/test-case",
                    json=test_case,
                    timeout=eval_timeout_param
                )
                if tc_res.status_code == 200:
                    test_result = tc_res.json()
                else:
                    test_result = {
                        "id": tc_id,
                        "question": q,
                        "expected_document": test_case.get("expected_document") or "N/A",
                        "retrieved_documents": [],
                        "retrieval_success": False,
                        "number_of_sources": 0,
                        "answer_generated": f"ERROR: HTTP {tc_res.status_code}",
                        "fallback_expected": test_case.get("expect_fallback", False),
                        "fallback_returned": False,
                        "status": "ERROR",
                        "passed": False,
                        "error": tc_res.text,
                        "evaluation_note": f"Server error HTTP {tc_res.status_code}"
                    }

            except requests.exceptions.Timeout:
                test_result = {
                    "id": tc_id,
                    "question": q,
                    "expected_document": test_case.get("expected_document") or "N/A",
                    "retrieved_documents": [],
                    "retrieval_success": False,
                    "number_of_sources": 0,
                    "answer_generated": f"TIMEOUT: Request timed out after {eval_timeout_param}s.",
                    "fallback_expected": test_case.get("expect_fallback", False),
                    "fallback_returned": False,
                    "status": "TIMEOUT",
                    "passed": False,
                    "error": f"Read timed out after {eval_timeout_param}s",
                    "evaluation_note": f"Test timed out after {eval_timeout_param}s during LLM generation."
                }

            except Exception as e:
                test_result = {
                    "id": tc_id,
                    "question": q,
                    "expected_document": test_case.get("expected_document") or "N/A",
                    "retrieved_documents": [],
                    "retrieval_success": False,
                    "number_of_sources": 0,
                    "answer_generated": f"ERROR: {str(e)}",
                    "fallback_expected": test_case.get("expect_fallback", False),
                    "fallback_returned": False,
                    "status": "ERROR",
                    "passed": False,
                    "error": str(e),
                    "evaluation_note": f"Exception: {str(e)}"
                }

            results.append(test_result)

            if test_result["status"] == "PASSED":
                passed_count += 1
            elif test_result["status"] == "TIMEOUT":
                timeout_count += 1
            else:
                failed_count += 1

            # Update progress bar
            progress_bar.progress(idx / total_tests)

        # Clear progress indicators
        status_box.empty()
        progress_bar.progress(1.0)

        # Final Summary Calculation
        acc_pct = round((passed_count / total_tests) * 100, 2) if total_tests > 0 else 0.0

        st.markdown("### 📊 Benchmark Summary")
        e_col1, e_col2, e_col3, e_col4, e_col5 = st.columns(5)
        e_col1.metric("Total Tests", total_tests)
        e_col2.metric("Passed", passed_count)
        e_col3.metric("Timed Out", timeout_count)
        e_col4.metric("Failed", failed_count)
        e_col5.metric("Overall Accuracy", f"{acc_pct}%")

        if acc_pct >= 80.0:
            st.success("🟢 Benchmark Suite Result: PASSED (Target Accuracy ≥ 80%)")
        else:
            st.warning("🟡 Benchmark Suite Result: NEEDS ATTENTION")

        st.write("---")
        st.markdown("### 📋 Detailed Test Case Results")

        for res_item in results:
            t_id = res_item.get("id")
            t_q = res_item.get("question")
            t_status = res_item.get("status", "FAILED")
            t_note = res_item.get("evaluation_note", "")

            if t_status == "PASSED":
                icon_badge = "✅ PASSED"
            elif t_status == "TIMEOUT":
                icon_badge = "⏳ TIMEOUT"
            else:
                icon_badge = "❌ FAILED"

            with st.expander(f"{t_id}: {t_q} — {icon_badge}", expanded=True):
                st.markdown(f"**Question**: {t_q}")
                st.markdown(f"**Expected Document**: `{res_item.get('expected_document')}`")
                st.markdown(f"**Retrieved Documents**: `{', '.join(res_item.get('retrieved_documents', [])) or 'None'}`")
                st.markdown(f"**Retrieval Success**: `{res_item.get('retrieval_success')}` | **Sources Count**: `{res_item.get('number_of_sources')}`")
                st.markdown(f"**Fallback Expected**: `{res_item.get('fallback_expected')}` | **Fallback Returned**: `{res_item.get('fallback_returned')}`")
                st.markdown(f"**Generated Answer Preview**: *{res_item.get('answer_generated')}*")
                if res_item.get("error"):
                    st.error(f"Error Details: {res_item.get('error')}")
                st.caption(f"Evaluation Note: {t_note}")
