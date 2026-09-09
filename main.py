import os

from src.agents.agents import (
    DataAgent,
    AnalysisAgent)
from src.config.setting import get_settings

from langchain_groq import ChatGroq
from langchain.agents import create_agent

settings = get_settings()
print(f"Settings - {__name__} {id(settings)}")

def _main():

    user_claim = "Hi, I found new damage on my car after it was parked outside overnight.The back of the car has a dent now. It was not there before. Mostly the rear bumper area. I attached the photo I took this morning."
    resp = DataAgent().run(user_id="user_001", user_claim=user_claim)
    for k,v in resp.items():
        print(f"{k} : {v}")
    state = {'images':resp['image_paths'], 'user_claim':resp['user_claim']}
    agent = AnalysisAgent(state)
    resp = agent.run()
    print("###Analyser output###")
    for k,v in resp.items():
        print(f"{k} : {v}")

def loop():
    import time
    for i in range(5):
        print(f'loop: {i}')
        _main()
        time.sleep(20)

if __name__ == "__main__":
    loop()