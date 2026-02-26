from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Prompt for document analysis
document_analysis_prompt = ChatPromptTemplate.from_template("""
You are an intelligent document understanding system.

Your task is to analyze the document and produce structured metadata.

IMPORTANT RULES:
1. The Summary must be GENERATED, not copied.
2. Do NOT repeat sentences from the document.
3. Compress information into high-level insights.
4. Each bullet should capture a concept, not a sentence.
5. If information is missing, write "Not Available".
6. Detect tone: Academic, Neutral, Positive, Negative, Opinionated.

{format_instructions}

DOCUMENT:
{document_text}
""")

# Central dictionary to register prompts
PROMPT_REGISTRY = {
    "document_analysis": document_analysis_prompt
}