import os
import sys
import json
from dotenv import load_dotenv
from utils.config_loader import load_config
from logger.custom_logger import customLogger
from exception.custom_exception import customException
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

log = customLogger().get_logger(__file__)

class ApiKeyManager:
    REQUIRED_KEYS = ["OPENAI_API_KEY"]

    def __init__(self):
        self.api_keys = {}
        raw = os.getenv("API_KEYS")
        if raw:
            try:
                parsed = json.loads(raw)
                if not isinstance(parsed, dict):
                    raise ValueError("API_KEYS is not a valid JSON object")
                self.api_keys = parsed
                log.info("Loaded API_KEYS from ECS secret")
            except Exception as e:
                log.warning("Failed to parse API_KEYS as JSON", error=str(e))

        # Fallback to individual env vars
        for key in self.REQUIRED_KEYS:
            if not self.api_keys.get(key):
                env_val = os.getenv(key)
                if env_val:
                    self.api_keys[key] = env_val
                    log.info(f"Loaded {key} from individual env var")

        # Final check
        missing = [k for k in self.REQUIRED_KEYS if not self.api_keys.get(k)]
        if missing:
            log.error("Missing required API keys", missing_keys=missing)
            raise customException("Missing API keys", sys)

        log.info(f"API keys loaded: {list(self.api_keys.keys())}")



    def get(self, key: str) -> str:
        val = self.api_keys.get(key)
        if not val:
            raise KeyError(f"API key for {key} is missing")
        return val


class ModelLoader:
    """
    Loads OpenAI embedding and chat model
    """

    def __init__(self):
        if os.getenv("ENV", "local").lower() != "production":
            load_dotenv()
            log.info("Running in LOCAL mode: .env loaded")
        else:
            log.info("Running in PRODUCTION mode")

        self.api_key_mgr = ApiKeyManager()
        self.config = load_config()

        self.openai_key = self.api_key_mgr.get("OPENAI_API_KEY")

    # ---------- Embeddings ----------
    def load_embeddings(self):
        try:
            model_name = self.config["embedding_model"]["model_name"]

            log.info(f"Loading OpenAI embedding model {model_name}" )

            return OpenAIEmbeddings(
                model=model_name,
                api_key=self.openai_key
            )

        except Exception as e:
            log.error(str(e))
            raise customException("Failed to load embedding model", sys)

    # ---------- LLM ----------
    def load_llm(self):
        try:
            llm_config = self.config["llm"]["openai"]

            model_name = llm_config["model_name"]
            temperature = llm_config.get("temperature", 0.2)
            max_tokens = llm_config.get("max_output_tokens", 2048)

            log.info(f"Loading OpenAI LLM, {model_name}")

            return ChatOpenAI(
                model=model_name,
                api_key=self.openai_key,
                temperature=temperature,
                max_tokens=max_tokens
            )

        except Exception as e:
            log.error(f"Error loading LLM, {str(e)}")
            raise customException("Failed to load LLM", sys)



if __name__ == "__main__":
    loader = ModelLoader()

    # Test Embedding
    embeddings = loader.load_embeddings()
    print(f"Embedding Model Loaded: {embeddings}")
    result = embeddings.embed_query("Hello, how are you?")
    print(f"Embedding Result: {result[0:5]}")

    # Test LLM
    llm = loader.load_llm()
    print(f"LLM Loaded: {llm}")
    result = llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")