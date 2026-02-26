# # Test code for document ingestion and analysis using a PDFHandler and DocumentAnalyzer
from src.DataAnalysis.Data_Analysis import DocumentAnalyzer  # Your DocumentAnalyzer class

def main():
    try:
        text_content = """
        Artificial Intelligence in Supply Chain Optimization

Authors:
Dr. Arjun Menon, IIT Madras
Priya Kannan, Data Scientist – LogiNext Solutions

Published in: International Journal of Applied Machine Learning
First published online: 14 March 2022
Revised version: 02 August 2023

Abstract:
Modern supply chains suffer from unpredictable demand patterns, vendor delays, and inefficient routing.
This paper proposes a hybrid deep learning and operations research approach to demand forecasting and
dynamic routing. Experiments conducted across three logistics providers in India show a reduction of 18%
in fuel consumption and 26% faster delivery times.

The study also evaluates real-world deployment challenges including resistance to adoption and integration
with legacy ERP systems.
        """

        # ---------- STEP 2: DATA ANALYSIS ----------
        print("Starting metadata analysis...")
        analyzer = DocumentAnalyzer()  # Loads LLM + parser
        
        analysis_result = analyzer.analyze_document(text_content)

        # ---------- STEP 3: DISPLAY RESULTS ----------
        print("\n=== METADATA ANALYSIS RESULT ===")
        for key, value in analysis_result.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    main()
