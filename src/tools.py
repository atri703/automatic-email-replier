from dotenv import load_dotenv
from crewai_tools import PDFSearchTool
from langchain_google_genai import ChatGoogleGenerativeAI
from composio_langchain import App, ComposioToolSet
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", 
                             api_key=os.environ['GOOGLE_API_KEY']
                          )

# Initialize the ComposioToolSet
toolset = ComposioToolSet(api_key=os.environ["COMPOSIO_API_KEY"])

# sql_tools = toolset.get_tools([App.SQLTOOL])

pdf_search_tool = PDFSearchTool(
    config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                
                model="gemini-1.5-flash",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="gemini-1.5-flash",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    ),
    pdf="src/user_manual_short.pdf"
)
