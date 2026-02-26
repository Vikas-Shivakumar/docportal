import fitz  # PyMuPDF

class PDFHandler:

    @staticmethod
    def extract_text(file_stream) -> str:
        """
        Extract text from uploaded PDF file
        """
        text = []

        with fitz.open(stream=file_stream.read(), filetype="pdf") as doc:
            for page in doc:
                page_text = page.get_text("text")
                if page_text:
                    text.append(page_text)

        return "\n".join(text)

