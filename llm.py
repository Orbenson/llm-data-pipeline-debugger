# pipeline_debugger/llm.py

import os
from typing import List, Optional
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.llms.base import LLM
from pydantic import Field

try:
    import google.generativeai as palm
except ImportError:
    palm = None

# DummyLLM for testing purposes.
class DummyLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "dummy"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return "Dummy analysis: This is a simulated response for testing purposes."


# GoogleGemeniLLM: Wrapper for the Google Gemini Free Model.
class GoogleGemeniLLM(LLM):
    api_key: str = Field(..., description="API key for Google Gemini")
    model: str = Field("gemini-2.0-flash", description="Model name for generation")
    temperature: float = Field(0.0, description="Temperature for generation")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if palm is None:
            raise ImportError(
                "The 'google-generativeai' package is not installed. Please install it via 'pip install google-generativeai'."
            )
        # Configure the client with the API key.
        palm.configure(api_key=self.api_key)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = palm.generate_text(
            model=self.model,
            prompt=prompt,
            temperature=self.temperature
        )
        return response.result

    @property
    def _llm_type(self) -> str:
        return "google_gemeni"


# Define the prompt template for log analysis.
prompt_template = """You are a Data Pipeline Debugger AI. 
You have access to the pipeline's error log and a data quality report.
{context} 
The pipeline error log is as follows:
{error_log}

kotlin
Copy
The data quality report is as follows:
{data_report}

pgsql
Copy
Analyze these inputs to determine the most likely cause of the pipeline failure. 
If data issues are present, consider how they relate to the error. 
Suggest a concrete solution or next step to fix the issue. 
Respond with a concise analysis explaining the cause and your recommended fix.
"""

_prompt = PromptTemplate(
    input_variables=["error_log", "data_report", "context"],
    template=prompt_template
)

def get_llm_chain(config: dict) -> LLMChain:
    """
    Initialize the LangChain LLMChain with the specified LLM provider and model.
    Falls back to the Google Gemini free model if no OpenAI API key is provided.
    """
    provider = config.get("llm_provider", "openai").lower()  # Default to openai.
    model_name = config.get("llm_model", "gpt-4")
    temperature = config.get("llm_temperature", 0)

    # If provider is openai but no API key is provided, switch to google_gemini.
    if provider == "openai":
        openai_api_key = config.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            provider = "google_gemini"

    if provider == "openai":
        from langchain.llms import OpenAI
        llm = OpenAI(model_name=model_name, temperature=temperature, openai_api_key=config.get("openai_api_key"))
    elif provider == "vertex":
        from langchain.llms import VertexAI
        llm = VertexAI(model_name=model_name, temperature=temperature)
    elif provider == "google_gemini":
        gemini_api_key = config.get("gemini_api_key")
        if not gemini_api_key:
            gemini_api_key = "AIzaSyAr_1zH1-NUtCMzfi5pReyCccsJqoaLV7g"
        llm = GoogleGemeniLLM(api_key=gemini_api_key, model="gemini-2.0-flash", temperature=temperature)
    else:
        llm = DummyLLM()

    chain = LLMChain(llm=llm, prompt=_prompt)
    return chain