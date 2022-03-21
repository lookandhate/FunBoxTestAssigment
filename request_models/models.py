from pydantic import BaseModel


class PostRequestBodyModel(BaseModel):
    links: list[str]
