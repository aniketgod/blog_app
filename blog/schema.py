from pydantic import BaseModel

"""
The data model for blog
"""
class ProperModel(BaseModel):
    title: str = "Write Title"
    introduction: str ="Write Introduction"
    discussion: str = "Write Discussion"
    conclusion: str = "Write Conclusion"







