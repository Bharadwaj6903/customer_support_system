import os
from dotenv import load_dotenv
from utils.config_loader import load_config

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings


class ModelLoader:
    """
    Utility class to load embedding models and LLM models.
    """

    def __init__(self):
        load_dotenv()
        self.config = load_config()
        self._validate_env()

    def _validate_env(self):
        """
        Validate necessary environment variables.
        """
        required_vars = ["GROQ_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

        self.groq_api_key = os.getenv("GROQ_API_KEY")

    def load_embeddings(self):
        """
        Load embedding model based on provider.
        """
        provider = self.config["embedding_model"]["provider"]
        model_name = self.config["embedding_model"]["model_name"]

        print(f"Loading embedding model: {provider} -> {model_name}")

        if provider == "google":
            return GoogleGenerativeAIEmbeddings(model=model_name)

        elif provider == "huggingface":
            return HuggingFaceEmbeddings(model_name=model_name)

        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")

    def load_llm(self):
        """
        Load LLM model.
        """
        print("LLM loading...")

        model_name = self.config["llm"]["model_name"]

        llm = ChatGroq(
            model=model_name,
            api_key=self.groq_api_key
        )

        return llm