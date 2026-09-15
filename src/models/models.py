from pydantic import BaseModel
from typing import Literal, List


class UserData(BaseModel):
    user_id:str
    evidence_required:str | list
    user_history:str
    image_paths:list
    user_claim:str
    agent:str = None

class AnalysisData(BaseModel):
    user_id: str
    image_paths: str
    user_claim: str
    claim_object: Literal["car","laptop", "package"]
    evidence_stander_met: bool
    evidence_standard_met_reason: str
    risk_flags: List[str]
    issue_type: str
    object_part: str
    claim_status: Literal["supported","contradicted","not_enough_information"]
    supporting_image_ids: List[str]
    valid_image: bool
    severity: Literal["none","low","medium","high","unknown"]
    #agent:str

class ReviewData(BaseModel):
    discrepancies: str | None
    decision: Literal["Approved", "Rejected", "Human Intervention"]
    reason: str
    agent:str