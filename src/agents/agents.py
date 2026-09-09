import json

from abc import ABC, abstractmethod
from src.agents.llm import (
    GroqGPT,
    GeminiFlash
)
from src.tools.tools import(
    read_evidence_requirements,
    get_user_history,
    get_images_paths
)
from src.models.models import (
    UserData,
    AnalysisData
)
from src.prompts.prompt import (
    DATA_AGENT_SYS_PROMPT,
    ANALYSIS_AGENT_SYS_PROMPT
)
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents.structured_output import ToolStrategy
from google import genai

class AgentBase(ABC):

    @abstractmethod
    def run(self, query:str):
        """Execute the agent"""
        pass


class DataAgent(AgentBase):
    
    def __init__(self):
        self.agent = create_agent(
                    model=GroqGPT().get_llm(),
                    tools=[read_evidence_requirements, 
                            get_user_history,
                            get_images_paths],
                    system_prompt=DATA_AGENT_SYS_PROMPT,
                    response_format=ToolStrategy(UserData)
                    )

    def run(self,user_id:str,user_claim:str) -> dict:
        result = self.agent.invoke(
            {
                "messages":[
                    ("user", f"User_id : {user_id}\n {user_claim}")
                ]
            }
        )

        #data = json.loads(result["messages"][-1].content)
        result['structured_response'].agent = self.__class__.__name__

        #user_claim_data = UserData.model_validate(data)
        return result['structured_response'].model_dump()


class AnalysisAgent(AgentBase):
    
    def __init__(self, state:dict):
        self.__client = genai.Client()
        self.state = state
        self.__llm = GeminiFlash().get_llm()


    def get_image_files(self) -> list:
        image_files = list(map(lambda x: self.__client.files.upload(file=x), self.state["images"]))
        return image_files

    def get_human_content(self) -> list[dict]:
        content = []
        image_files = self.get_image_files()
        image_content = [{'type':"media",
                            'file_uri':image_file.uri,
                            'mime_type':image_file.mime_type,} for image_file in image_files]
        content.extend(image_content)
        content.append({'type':'text', 'text': f'User claim\n{self.state['user_claim']}'})
        return content
    
    def get_messages(self) -> HumanMessage:
        human_message = HumanMessage(content=self.get_human_content())
        system_message = SystemMessage(content=ANALYSIS_AGENT_SYS_PROMPT)
        return [system_message, human_message]

    def run(self):
        structured_model = self.__llm.with_structured_output(AnalysisData)
        messages = self.get_messages()
        resp = structured_model.invoke(messages)
        return resp.model_dump()


    
        
            