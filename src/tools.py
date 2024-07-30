from dotenv import load_dotenv
from crewai_tools import PDFSearchTool
from langchain_google_genai import ChatGoogleGenerativeAI
from composio_langchain import App, ComposioToolSet
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools.sql_database.tool import InfoSQLDatabaseTool, ListSQLDatabaseTool, QuerySQLCheckerTool, QuerySQLDataBaseTool
from PyPDF2 import PdfReader
from langchain.tools import tool
import re
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", 
                             api_key=os.environ['GOOGLE_API_KEY']
                          )

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

db = SQLDatabase.from_uri("sqlite:///src/company.db")

@tool("list_tables")
def list_tables() -> str:
    """List the available tables in the database"""
    return ListSQLDatabaseTool(db=db).invoke("")


@tool("tables_schema")
def tables_schema(tables: str) -> str:
    """
    Input is a comma-separated list of tables, output is the schema and sample rows
    for those tables. Be sure that the tables actually exist by calling `list_tables` first!
    Example Input: table1, table2, table3
    """
    tool = InfoSQLDatabaseTool(db=db)
    return tool.invoke(tables)


@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """Execute a SQL query against the database. Returns the result"""
    return QuerySQLDataBaseTool(db=db).invoke(sql_query)

@tool("check_sql")
def check_sql(sql_query: str) -> str:
    """
    Use this tool to double check if your query is correct before executing it. Always use this
    tool before executing a query with `execute_sql`.
    """
    return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})

