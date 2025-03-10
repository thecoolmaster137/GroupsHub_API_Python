from pydantic import BaseModel
from typing import Optional

class AddReport(BaseModel):
    report_reason: str
    report_desc: Optional[str] = None
