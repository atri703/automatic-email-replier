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

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", 
#                              api_key=os.environ['GOOGLE_API_KEY']
#                           )

# Initialize the ComposioToolSet
toolset = ComposioToolSet(api_key=os.environ["COMPOSIO_API_KEY"])

@tool
def sql_tools():
  """
    Searches a sql database.
    """
  return toolset.get_tools([App.SQLTOOL])

# BY OPENAI
pdf_search_tool = PDFSearchTool(pdf="src/user_manual.pdf")

# By GROQ
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