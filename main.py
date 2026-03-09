from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from openai import api_key

load_dotenv()

tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general"
)

@tool
def search(query: str) -> str:
    """Search the internet for information using Tavily."""
    print(f"Searching for: {query}")
    return tavily_search_tool.invoke({"query": query})



llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

tools = [search]

agent = create_agent(
    model=llm,
    tools=tools
)

def main():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather like in Tokyo?")]
    })

    final_answer = result["messages"][-1].content
    print(final_answer)


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
