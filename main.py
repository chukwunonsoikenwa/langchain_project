from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch

load_dotenv()


search = TavilySearch(
    max_results=5,
    topic="general"
)
tools = [search]
class Source(BaseModel):
    """Search the internet for information using Tavily."""
    url:str = Field(description="The URL of the search result")

class AgentRespond(BaseModel):
    """Structured response by the agent."""
    answer:str = Field(description="The messages from the agent")     
    sources:List[Source] = Field(default_factory=list, description="The sources used by the agent to answer the question")



llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


agent = create_agent(
    model=llm,
    tools=tools,response_format=AgentRespond
)

def main():
    result = agent.invoke({
        "messages": [HumanMessage(content="""Find 3 LinkedIn job postings for AI Engineer roles in Canada.
                     
Requirements:
- Only return LinkedIn job listing URLs
- URLs must follow this format:
  https://www.linkedin.com/jobs/view/...
- Summarize the job title, company, and location""")]
    })

    print(result["structured_response"])


# def main():
#     print("Hello, World!")

#     information = """Elon Reeve Musk (born June 28, 1971) is a businessman and entrepreneur known for his leadership of Tesla, SpaceX, X, and xAI..."""

#     summary_template = """
#     Given the following information:

#     {information}

#     Create:
#     1. A short summary
#     2. Two interesting facts about the person
#     """

#     summary_prompt = PromptTemplate(
#         template=summary_template,
#         input_variables=["information"]
#     )

#     # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
#     llm = ChatOllama(model="gemma3:270m", temperature=0)

#     chain = summary_prompt | llm

#     response = chain.invoke({"information": information})

#     print(response.content)

if __name__ == "__main__":
    main()
