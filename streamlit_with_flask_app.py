import streamlit as st
import requests
import json

# ---------------- CONFIG ----------------

API_TEXT_URL = "http://127.0.0.1:5000/analyze"
API_FILE_URL = "http://127.0.0.1:5000/upload"

st.set_page_config(
page_title="AI Document Analyzer",
page_icon="📄",
layout="wide"
)

# ---------------- UI HEADER ----------------

st.title("📄 AI Document Metadata Analyzer")
st.caption("Extract structured metadata from any document using LLMs")

tab1, tab2 = st.tabs(["📝 Analyze Text", "📤 Upload PDF"])

def display_metadata(data):


    st.success("Analysis Complete")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 General Information")
        st.write("**Title:**", data.get("Title"))
        st.write("**Authors:**", ", ".join(data.get("Author", [])))
        st.write("**Publisher:**", data.get("Publisher"))
        st.write("**Language:**", data.get("Language"))
        st.write("**Pages:**", data.get("PageCount"))

    with col2:
        st.subheader("📅 Dates & Tone")
        st.write("**Created:**", data.get("DateCreated"))
        st.write("**Modified:**", data.get("Last ModifiedDate"))
        st.write("**Tone:**", data.get("SentimentTone"))

    st.divider()

    st.subheader("🧠 Summary")
    for point in data.get("Summary", []):
        st.markdown(f"- {point}")

    st.divider()

    with st.expander("🔍 Raw JSON Output"):
        st.json(data)



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

    if st.button("Analyze Text", type="primary"):

        if not document_text.strip():
            st.warning("Please paste some text first")
            st.stop()

        with st.spinner("Analyzing document..."):

            try:
                response = requests.post(
                    API_TEXT_URL,
                    json={"text": document_text},
                    timeout=300
                )

                if response.status_code != 200:
                    st.error("API returned an error")
                    st.code(response.text)
                    st.stop()

                data = response.json()["metadata"]
                display_metadata(data)

            except Exception as e:
                st.error("Could not connect to backend API")
                st.code(str(e))


# =========================================================

# PDF UPLOAD TAB

# =========================================================

with tab2:


    st.subheader("Upload a PDF document")

    uploaded_file = st.file_uploader("Choose PDF file", type=["pdf"])

    if uploaded_file is not None:

        st.info(f"Selected file: {uploaded_file.name}")

        if st.button("Analyze PDF", type="primary"):

            with st.spinner("Uploading and analyzing PDF..."):

                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            "application/pdf"
                        )
                    }

                    response = requests.post(
                        API_FILE_URL,
                        files=files,
                        timeout=600
                    )

                    if response.status_code != 200:
                        st.error("API returned an error")
                        st.code(response.text)
                        st.stop()

                    data = response.json()["metadata"]
                    display_metadata(data)

                except Exception as e:
                    st.error("Failed to connect to API")
                    st.code(str(e))


# =========================================================

# METADATA DISPLAY FUNCTION

# =========================================================

