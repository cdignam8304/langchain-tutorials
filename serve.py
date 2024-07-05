#!/usr/bin/env python

from typing import (
    Any,
    Literal,
    Optional,
    Sequence,
    Type,
    Union,
    List,
)

from fastapi import FastAPI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv('OPENAI_API_KEY')
langsmith_api_key = os.getenv('LANGSMITH_API_KEY')


# 1. Create Prompt Template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")    
])

# 2. Create model
model = ChatOpenAI(model="gpt-4o")

# 3. Create parser
parser = StrOutputParser

# 4. Create chain
chain = prompt_template | model | parser

# 5. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

# 6. Add chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8000)

