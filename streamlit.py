import streamlit as st
from src.DataAnalysis.Data_Analysis import DocumentAnalyzer
from utils.pdf_handler import PDFHandler
import io
import json

st.set_page_config(page_title="AI Document Analyzer", page_icon="📄", layout="wide")

# ---------------- LOAD MODEL (ONCE) ----------------

@st.cache_resource
def get_analyzer():
    return DocumentAnalyzer()

analyzer = get_analyzer()

# ---------------- DISPLAY FUNCTION ----------------

def display_metadata(result: dict):
    st.success("Analysis Complete")

# ---------------- UI HEADER ----------------

st.title("📄 AI Document Metadata Analyzer")
st.caption("Upload or paste a document and extract structured metadata using LLMs")

tab1, tab2 = st.tabs(["📝 Analyze Text", "📤 Upload PDF"])

# =========================================================

# TEXT ANALYSIS TAB

# =========================================================

with tab1:
    st.subheader("Paste Document Text")


    document_text = st.text_area(
        "Enter document content",
        height=350,
        placeholder="Paste article, invoice, agreement, research paper..."
    )

    if st.button("Analyze Text", type="primary", key="text_btn"):
        if not document_text.strip():
            st.warning("Please paste some text first")
        else:
            with st.spinner("Analyzing document..."):
                try:
                    result = analyzer.analyze_document(document_text)
                    display_metadata(result)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("📌 General Information")
                        st.write("**Title:**", result.get("Title"))
                        st.write("**Authors:**", ", ".join(result.get("Author", [])))
                        st.write("**Publisher:**", result.get("Publisher"))
                        st.write("**Language:**", result.get("Language"))
                        st.write("**Pages:**", result.get("PageCount"))

                    with col2:
                        st.subheader("📅 Dates & Tone")
                        st.write("**Created:**", result.get("DateCreated"))
                        st.write("**Modified:**", result.get("LastModifiedDate"))
                        st.write("**Tone:**", result.get("SentimentTone"))

                    st.divider()

                    st.subheader("🧠 Summary")
                    for point in result.get("Summary", []):
                        st.markdown(f"- {point}")

                    st.divider()

                    # Download JSON
                    st.download_button(
                        label="⬇️ Download Metadata JSON",
                        data=json.dumps(result, indent=2),
                        file_name="document_metadata.json",
                        mime="application/json"
                    )

                    with st.expander("🔍 Raw JSON Output"):
                        st.json(result)


                except Exception as e:
                    st.error("Analysis failed")
                    st.code(str(e))


# =========================================================

# PDF UPLOAD TAB

# =========================================================

with tab2:
    st.subheader("Upload a PDF document")

    uploaded_file = st.file_uploader("Choose PDF file", type=["pdf"])

    if uploaded_file is not None:
        st.info(f"Selected file: {uploaded_file.name}")

        if st.button("Analyze PDF", type="primary", key="pdf_btn"):
            with st.spinner("Extracting and analyzing PDF..."):
                try:
                    pdf_bytes = uploaded_file.read()
                    text = PDFHandler.extract_text(io.BytesIO(pdf_bytes))

                    if not text.strip():
                        st.error("Could not extract text from PDF")
                    else:
                        result = analyzer.analyze_document(text)
                        display_metadata(result)

                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("📌 General Information")
                            st.write("**Title:**", result.get("Title"))
                            st.write("**Authors:**", ", ".join(result.get("Author", [])))
                            st.write("**Publisher:**", result.get("Publisher"))
                            st.write("**Language:**", result.get("Language"))
                            st.write("**Pages:**", result.get("PageCount"))

                        with col2:
                            st.subheader("📅 Dates & Tone")
                            st.write("**Created:**", result.get("DateCreated"))
                            st.write("**Modified:**", result.get("LastModifiedDate"))
                            st.write("**Tone:**", result.get("SentimentTone"))

                        st.divider()

                        st.subheader("🧠 Summary")
                        for point in result.get("Summary", []):
                            st.markdown(f"- {point}")

                        st.divider()

                        # Download JSON
                        st.download_button(
                            label="⬇️ Download Metadata JSON",
                            data=json.dumps(result, indent=2),
                            file_name="document_metadata.json",
                            mime="application/json"
                        )

                        with st.expander("🔍 Raw JSON Output"):
                            st.json(result)

                except Exception as e:
                    st.error("PDF processing failed")
                    st.code(str(e))






