import json

from abc import ABC, abstractmethod
from src.agents.llm import (
    GroqGPT,
    GeminiFlash,
    GroqQwen
)
from src.tools.tools import(
    read_evidence_requirements,
    get_user_history,
    get_images_paths
)
from src.models.models import (
    UserData,
    AnalysisData,
    ReviewData
)
from src.prompts.prompt import (
    DATA_AGENT_SYS_PROMPT,
    ANALYSIS_AGENT_SYS_PROMPT,
    REVIEW_AGENT_PROMPT
)
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents.structured_output import ToolStrategy
from google import genai
from pathlib import Path
import base64

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
    
    def get_messages(self) -> list[HumanMessage, SystemMessage]:
        human_message = HumanMessage(content=self.get_human_content())
        system_message = SystemMessage(content=ANALYSIS_AGENT_SYS_PROMPT)
        return [system_message, human_message]

    def run(self) -> dict:
        structured_model = self.__llm.with_structured_output(AnalysisData)
        messages = self.get_messages()
        resp = structured_model.invoke(messages)
        return resp.model_dump()

class ReviewAgent(AgentBase):

        def __init__(self, state:dict):
            self.agent = create_agent(
                    model=GroqQwen().get_llm(),
                    tools=[],
                    system_prompt=REVIEW_AGENT_PROMPT,
                    response_format=ToolStrategy(ReviewData)
                    )
            self.state = state

        def get_image_paths(self) -> list[Path]:
            image_path = list(map(lambda x: Path(x), self.state["images"]))
            return image_path

        def convert_2_image_data_url(self, path) -> str:
            image_mime_type = {
                ".png":"image/png",
                ".jpg":"image/jpeg",
                ".jpeg":"image/jpeg",
                ".webp": "image/webp",
            }

            with open(path, "rb") as f:
                image_b64 = base64.b64encode(f.read()).decode("ascii")
            return f"data:{image_mime_type[path.suffix.lower()]};base64,{image_b64}"

        def get_image_data_urls(self) -> list:
            image_paths = self.get_image_paths()
            image_data_urls = list(map(self.convert_2_image_data_url, image_paths))
            return image_data_urls

        def get_human_content(self) -> list:
            content = []
            image_data_urls = self.get_image_data_urls()
            image_data = [{'type':'image_url',
                               'image_url': {'url':image_data_url}
                               } for image_data_url in image_data_urls]
            content.extend(image_data)
            content.append({'type':'text', 
                                'text':f'###Analyser Output##\n{self.state['analyzer_output']}'})
            return content

        def get_messages(self) -> dict:
            human_message = {"role":"user", "content":self.get_human_content()}
            return human_message

        def run(self)-> dict:
            messages = self.get_messages()
            result = self.agent.invoke({"messages":[messages]})
            result['structured_response'].agent = self.__class__.__name__
            return result['structured_response'].model_dump()