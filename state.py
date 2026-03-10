from typing import TypedDict, Optional

class EmailState(TypedDict):
    prompt: str
    draft: Optional[str]
    feedback: Optional[str]
    approved: Optional[bool]