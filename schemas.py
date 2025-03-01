from typing import Dict, Any
from pydantic import BaseModel

class TaskStatus(BaseModel):
    """
    Represents default task's status
    """
    task_id: str
    status: str
    data: Dict[str, Any]
