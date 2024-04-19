# https://python.langchain.com/docs/get_started/quickstart/#llm-chain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

question = 'how can langsmith help with testing?'

# Load Environment variables
load_dotenv()

# Create llm object
llm = ChatOpenAI()

# Call LLM - simple approach
# output = llm.invoke(question)

# Create prompt  - to get better answer
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

# Create Chain - aka Pipeline
chain = prompt | llm
# Call Chain - first create prompt and then call LLM
chain.invoke({'input': question})


# Create Output Parser - to convert chat message to string easily
output_parser = StrOutputParser()
# Create Chain - aka Pipeline
chain = prompt | llm | output_parser

# Call Chain - first create prompt, call LLM and then output parser
chain.invoke({'input': question})