import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.setting import get_settings
from abc import ABC, abstractmethod

setttings = get_settings()

os.environ["GROQ_API_KEY"]=setttings.GROQ_API_KEY
os.environ['GOOGLE_API_KEY']=setttings.GL_GEN_AI_API_KEY

class LLM(ABC):
    
    @abstractmethod
    def get_llm(self):
        pass


class GroqGPT(LLM):

    def __init__(self):
        self.__model = setttings.GROQ_GPT

    def get_llm(self):
        llm = ChatGroq(model=self.__model)
        return llm
    
class GeminiFlash(LLM):

    def __init__(self):
        self.__model = setttings.GOOGLE_GEM

    def get_llm(self):
        llm = ChatGoogleGenerativeAI(model=setttings.GOOGLE_GEM)
        return llm