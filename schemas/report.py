from pydantic import BaseModel
from typing import Optional

class Report(BaseModel):
    report_id: int
    report_reason: str
    report_desc: str
