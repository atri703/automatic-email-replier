from dotenv import load_dotenv
from crewai_tools import PDFSearchTool
from langchain_google_genai import ChatGoogleGenerativeAI
from composio_langchain import App, ComposioToolSet
from PyPDF2 import PdfReader
import requests
from langchain.tools import tool
import re
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", 
                             api_key=os.environ['GOOGLE_API_KEY']
                          )

# Initialize the ComposioToolSet
toolset = ComposioToolSet(api_key=os.environ["COMPOSIO_API_KEY"])

# sql_tools = toolset.get_tools([App.SQLTOOL])

# pdf_search_tool = PDFSearchTool(
#     config=dict(
#         llm=dict(
#             provider="google", # or google, openai, anthropic, llama2, ...
#             config=dict(
                
#                 model="gemini-1.5-flash",
#                 # temperature=0.5,
#                 # top_p=1,
#                 # stream=true,
#             ),
#         ),
#         embedder=dict(
#             provider="google", # or openai, ollama, ...
#             config=dict(
#                 model="gemini-1.5-flash",
#                 task_type="retrieval_document",
#                 # title="Embeddings",
#             ),
#         ),
#     ),
#     pdf="src/user_manual_short.pdf"
# )

@tool
def fetch_pdf_content():
  """
    Fetches and preprocesses content from a PDF given its path.
    Returns the text of the PDF.
    """
  with open("src/user_manual.pdf", 'rb') as f:
    pdf = PdfReader(f)
    text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
    # Optional preprocessing of text
    processed_text = re.sub(r'\s+', ' ', text).strip()
    return processed_text