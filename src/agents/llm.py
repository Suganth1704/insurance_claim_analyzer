import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.setting import get_settings
from abc import ABC, abstractmethod

setttings = get_settings()

os.environ["GROQ_API_KEY"]=setttings.GROQ_API_KEY
os.environ['GOOGLE_API_KEY']=setttings.GL_GEN_AI_API_KEY
os.environ['NVIDIA_API_KEY']=setttings.NV_KIMI_K3_API_KEY

class LLM(ABC):
    
    @abstractmethod
    def get_llm(self):
        pass


class GroqGPT(LLM):

    def __init__(self):
        self.__model = setttings.GROQ_GPT

    def get_llm(self):
        llm = ChatGroq(model=self.__model,
                        max_retries=2)
        return llm
    
class GeminiFlash(LLM):

    def __init__(self):
        self.__model = setttings.GOOGLE_GEM

    def get_llm(self):
        llm = ChatGoogleGenerativeAI(
            model=self.__model,
            temperature=0.5,
            max_retries=2
            )
        return llm

class GroqQwen(LLM):

    def __init__(self):
        self.__model =setttings.GROQ_QWEN

    def get_llm(self):
        llm = ChatGroq(
            model=self.__model,
            temperature=0.5,
            max_retries=2,
        )
        return llm
