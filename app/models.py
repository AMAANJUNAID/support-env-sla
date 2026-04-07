from pydantic import BaseModel
from typing import List

class Action(BaseModel):
    action_type: str
    content: str

class Observation(BaseModel):
    ticket_id: int
    message: str
    priority: str
    sentiment: str
    sla_hours_left: int
    customer_type: str
    issue_type: str
    history: List[str]
    step_count: int
    