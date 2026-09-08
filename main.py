import os

from src.agents.agents import DataAgent
from src.config.setting import get_settings

from langchain_groq import ChatGroq
from langchain.agents import create_agent

settings = get_settings()
print(f"Settings - {__name__} {id(settings)}")

def main():

    user_claim = """Morning. I parked near office and later noticed something off in the front. 
    Two things,first one is the front bumper looks damaged and the left headlight also looks affected
    I am requesting claim for front bumper and left headlight together.
    """
    resp = DataAgent().run(user_id="user_001", user_claim=user_claim)
    print(resp.model_dump())

if __name__ == "__main__":
    main()