import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import customLogger
from exception.custom_exception import customException
from custom_models.model import Metadata
from langchain_core.output_parsers import JsonOutputParser
#from langchain.output_parsers import OutputFixingParser
from prompts.prompt_library import PROMPT_REGISTRY # type: ignore

log = customLogger().get_logger(__file__)

class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model.
    Automatically logs all actions and supports session-based organization.
    """
    def __init__(self):
        try:
            self.loader=ModelLoader()
            self.llm=self.loader.load_llm()
            
            # Prepare parsers
            self.parser = JsonOutputParser(pydantic_object=Metadata)
            #self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)
            
            self.prompt = PROMPT_REGISTRY["document_analysis"]
            
            log.info("DocumentAnalyzer initialized successfully")
            
            
        except Exception as e:
            log.info(f"Error initializing DocumentAnalyzer: {e}")
            raise customException("Error in DocumentAnalyzer initialization", sys)
        
        
    
    def analyze_document(self, document_text:str)-> dict:
        """
        Analyze a document's text and extract structured metadata & summary.
        """
        try:
            chain = self.prompt | self.llm | self.parser
            
            log.info("Meta-data analysis chain initialized")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })

            log.info(f"Metadata extraction successful")
            
            return response

        except Exception as e:
            log.error(f"Metadata analysis failed {str(e)}")
            raise customException("Metadata extraction failed", sys)
        
    