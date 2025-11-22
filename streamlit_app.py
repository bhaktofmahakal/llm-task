import streamlit as st
from app import FactCheckingPipeline
import json
from datetime import datetime


st.set_page_config(
    page_title="LLM Fact Checker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .verdict-true { color: #2ecc71; font-weight: bold; }
        .verdict-false { color: #e74c3c; font-weight: bold; }
        .verdict-unverifiable { color: #f39c12; font-weight: bold; }
        .confidence-bar { margin: 10px 0; }
        .fact-box { 
            background-color: #f0f2f6; 
            padding: 10px; 
            border-radius: 5px; 
            margin: 5px 0;
        }
        .claim-box {
            background-color: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 10px 0;
            border-radius: 5px;
        }
        .verdict-box {
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .verdict-box.true {
            background-color: #d5f4e6;
            border-left: 4px solid #2ecc71;
        }
        .verdict-box.false {
            background-color: #fadbd8;
            border-left: 4px solid #e74c3c;
        }
        .verdict-box.unverifiable {
            background-color: #fef5e7;
            border-left: 4px solid #f39c12;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_pipeline():
    pipeline = FactCheckingPipeline()
    pipeline.initialize_database()
    return pipeline


def get_verdict_color(verdict):
    if verdict == "True":
        return "true"
    elif verdict == "False":
        return "false"
    else:
        return "unverifiable"


def display_result(result):
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**Claim:** {result['claim']}")
        
        with col2:
            verdict = result.get('verdict', 'Unverifiable')
            confidence = result.get('confidence', 0.0)
            st.markdown(f"**Verdict:** <span class='verdict-{verdict.lower()}'>{verdict}</span>", 
                       unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"**Confidence:** {confidence:.1%}")

        reasoning = result.get('reasoning', 'No reasoning available')
        st.markdown(f"**Reasoning:** {reasoning}")

        evidence = result.get('evidence', [])
        if evidence:
            with st.expander("📚 Retrieved Evidence", expanded=False):
                for i, fact in enumerate(evidence, 1):
                    st.markdown(f"<div class='fact-box'><b>{i}.</b> {fact}</div>", 
                               unsafe_allow_html=True)

        supporting = result.get('supporting_facts', [])
        if supporting:
            with st.expander("✅ Supporting Facts", expanded=False):
                for fact in supporting:
                    st.markdown(f"- {fact}")

        conflicting = result.get('conflicting_facts', [])
        if conflicting:
            with st.expander("❌ Conflicting Facts", expanded=False):
                for fact in conflicting:
                    st.markdown(f"- {fact}")


def main():
    st.title("🔍 LLM-Powered Fact Checker")
    st.markdown("Verify claims and statements using AI-powered fact-checking with RAG")

    with st.sidebar:
        st.header("⚙️ Settings")
        
        use_sample = st.checkbox("Use sample input", value=False)
        
        if st.button("🔄 Reset Database", key="reset_db"):
            with st.spinner("Resetting database..."):
                pipeline = load_pipeline()
                pipeline.reset_database()
                st.success("Database reset successfully!")
                st.rerun()

    pipeline = load_pipeline()

    sample_statements = [
        "The Indian government has announced free electricity to all farmers starting July 2025.",
        "PM-KISAN provides Rs. 6000 per year to all landholding farmers.",
        "The KUSUM scheme offers free solar panels for all agricultural use.",
        "MNREGA guarantees 365 days of employment per year to rural households.",
    ]

    col1, col2 = st.columns([3, 1])
    
    with col1:
        if use_sample:
            user_input = st.selectbox(
                "Select a sample statement:",
                sample_statements,
                key="sample_select"
            )
        else:
            user_input = st.text_area(
                "Enter a statement or news post to fact-check:",
                placeholder="E.g., 'The Indian government has announced free electricity to all farmers starting July 2025.'",
                height=100
            )
    
    with col2:
        st.write("")
        st.write("")
        check_button = st.button("🚀 Check Facts", use_container_width=True, type="primary")

    if check_button and user_input:
        with st.spinner("🔍 Analyzing statement and retrieving facts..."):
            result = pipeline.check_statement(user_input)

        if "error" in result:
            st.error(f"Error during fact-checking: {result['error']}")
        else:
            st.markdown("---")
            st.markdown("### 📊 Fact-Check Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Claims Analyzed", result['total_claims'])
            
            with col2:
                overall_verdict = result['overall_verdict']
                verdict_emoji = "✅" if overall_verdict == "True" else "❌" if overall_verdict == "False" else "❓"
                st.metric("Overall Verdict", f"{verdict_emoji} {overall_verdict}")
            
            with col3:
                avg_confidence = sum(r.get('confidence', 0) for r in result['results']) / max(len(result['results']), 1)
                st.metric("Avg. Confidence", f"{avg_confidence:.1%}")

            st.markdown("---")
            
            for i, claim_result in enumerate(result['results'], 1):
                with st.container():
                    st.markdown(f"### Claim {i}")
                    display_result(claim_result)
                    st.markdown("---")

            with st.expander("📋 Raw JSON Output", expanded=False):
                st.json(result)

            with st.expander("💾 Save Result", expanded=False):
                filename = f"fact_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(result, indent=2),
                    file_name=filename,
                    mime="application/json"
                )

    st.markdown("---")
    st.markdown("### ℹ️ About This Tool")
    st.markdown("""
    This fact-checker uses:
    - **Retrieval-Augmented Generation (RAG)** to find relevant facts
    - **ChromaDB** for vector storage and semantic search
    - **Sentence-Transformers** for text embeddings
    - **Groq LLM** for intelligent fact verification
    
    The system extracts claims and verifies them against a database of verified facts.
    """)

    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📚 Database Info")
        
        try:
            db_count = pipeline.retriever.collection.count() if pipeline.retriever.collection else 0
            st.metric("Facts in Database", db_count)
        except:
            st.metric("Facts in Database", "N/A")

        st.markdown("### 🎯 Verdicts")
        st.markdown("- **✅ True**: Claim is supported by retrieved facts")
        st.markdown("- **❌ False**: Claim contradicts retrieved facts")
        st.markdown("- **❓ Unverifiable**: Insufficient information to verify")


if __name__ == "__main__":
    main()
