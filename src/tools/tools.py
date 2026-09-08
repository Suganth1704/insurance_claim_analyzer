import os
import pandas as pd

from src.config.setting import get_settings

settings = get_settings()
print(f"Settings - {__name__} {id(settings)}")

from langchain.tools import tool

@tool("read_evidence_required", 
        description="Read the evidence_requirements.csv file and retrieve the evidence requirements. Return the data as a dictionary that can be used to determine what evidence is required for each requirement.")
def read_evidence_requirements() -> dict:
    evid_req_csv = "evidence_requirements.csv"
    evid_req_path = os.path.join(settings.DATA_DIR, evid_req_csv)
    df = pd.read_csv(evid_req_path)
    return df.to_markdown(index=False)

@tool("get_user_history", 
        description="Retrieves a user's historical data from user_history.csv and returns it as a structured dictionary for analysis and decision-making.")
def get_user_history(user_id:str) -> dict | str :
    user_hist_csv = "user_history.csv"
    user_hist_path = os.path.join(settings.DATA_DIR, user_hist_csv)
    df = pd.read_csv(user_hist_path)
    user_df = df[df["user_id"] == user_id]
    if not user_df.empty:
        return user_df.to_markdown(index=False)
    else:
        return "User Histroy Not Found"

@tool("get_images",
        description="Retrieve the relevant claim image from the image directory using the available claim or user information. The retrieved image will be used to validate the user's statement against the visual evidence provided in the claim.")
def get_images_paths(user_id:str) -> list:
    user_dir =  os.path.join(settings.IMAGE_DIR, user_id)
    for root, dirs, files in os.walk(user_dir):
        image_paths = list(map(lambda x: os.path.join(user_dir, x), files))
        return image_paths
    return []
