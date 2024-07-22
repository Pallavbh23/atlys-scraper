from pydantic import BaseModel

class HTMLContent(BaseModel):
    html: str

class ScrapeSettings(BaseModel):
    pages: int
    proxy: str = None