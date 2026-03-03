from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langsmith import traceable

load_dotenv()

def main():
    print("Hello, World!")

    information = """Elon Reeve Musk (born June 28, 1971) is a businessman and entrepreneur known for his leadership of Tesla, SpaceX, X, and xAI..."""

    summary_template = """
    Given the following information:

    {information}

    Create:
    1. A short summary
    2. Two interesting facts about the person
    """

    summary_prompt = PromptTemplate(
        template=summary_template,
        input_variables=["information"]
    )

    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm = ChatOllama(model="gemma3:270m", temperature=0)

    chain = summary_prompt | llm

    response = chain.invoke({"information": information})

    print(response.content)


if __name__ == "__main__":
    main()