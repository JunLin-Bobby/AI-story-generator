from typing import List,Dict,Any,Optional
from pydantic import BaseModel, Field

class StoryOptionLLM(BaseModel):
    text:str = Field(description="Text for the option shown to the user")
    nextNode:Dict[str,Any] = Field(description="The next node content and its options")

class StoryNodeLLM(BaseModel):
    content:str = Field(description="The content of the story node")
    isEnding:bool = Field(description="Whether this node is an ending")
    isGoodEnding:bool = Field(description="Whether this node is a good ending")
    options:List[StoryOptionLLM] = Field(default_factory=list,description="List of options from this node")

class StoryLLMResponse(BaseModel):
    title:str = Field(description="The title of the story")
    rootNode:StoryNodeLLM = Field(description="The root node of the story")
