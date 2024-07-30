from crewai import Agent
from tools import fetch_pdf_content, sql_tools, pdf_search_tool, check_sql, execute_sql, list_tables, tables_schema

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import os

load_dotenv()

# Call the llm model
llm_model = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 
llm_groq = ChatGroq(
    # This is the default and can be omitted
    model="llama-3.1-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Agent 1 - Decides the category of the email
email_categorizer_agent = Agent(
    role='Email Categorizer Agent',
    goal="""take in a email from a human that has emailed out company email address and categorize it \
            into one of the following categories: 
            inquiry_type - used when someone is asking for an item 
            review_type - used when someone is providing review or feedback about something 
            assistance_request_type - used when someone is asking questions about film equipment  \\
            general_handling when it doesnt relate to any other category  """,
    backstory="""You are a master at understanding what a customer wants when they write an email and are able to categorize it in a useful way""",
    llm=llm_model,
    # llm=llm_groq,
    allow_delegation=False,
    verbose=True,
)

# Agent 2 - Researcher Agent
email_researcher_agent=Agent(
    role='Info Researcher Agent',
    goal="""take in a email from a human that has emailed out company email address and the category \
            that the email_categorizer agent gave it and decide what information you need to search for the email_writer_agent to reply to \
            the email in a thoughtful and helpful way.
            if category is 'inquiry_type' then run SQL queries on 'company.db' to find its price, if film equipment is not available \
            then recommend similar item (This will be the items that will have the same category_type as of the asked item, column name is category), \
            state that asked item is not there but something similar is available (only suggest something similar if you find anything with the same category \
            if you do not find anything in database just say NOT AVAILABLE BUT NEVER MAKE RANDOM ITEMS).
            if category is 'review_type' then analyse if review is positive or negative.
            if category is 'assistance_request_type' search through 'film_equipement.pdf', if you find relevant information pass it on email_writer_agent \
            but if you do not find it 'NO USEFUL RESESARCH FOUND' and never make information on your own.
            if it is "general_handling" do not do anything.
            ONLY GIVE INFO THAT IS PRESENT IN DATABASE OR MANUAL in case of inquiry_type, assistance_type respectively NOTHING MORE.
            """,
    backstory="""You are a SQL expert as well as great researcher who can read long documents easily and understand and analyze what information our email writer needs to write a reply that \
                will help the customer""",
    # tools=[fetch_pdf_content, sql_tools],
    # tools=[sql_tools, pdf_search_tool],
    tools=[pdf_search_tool, list_tables, tables_schema, execute_sql, check_sql],
    # llm=llm_model,
    # llm=llm_groq,
    allow_delegation=False,
    verbose=True,
)

# Agent 3 - Email Agent
email_writer_agent=Agent(
    role='Email Writer Agent',
    goal="""take in a email from a human that has emailed out company email address, the category \
            that the email_categorizer_agent gave it and the research from the email_researcher_agent and \
            write a helpful email in a thoughtful and friendly way. You NEVER make up information. that hasn't been provided by the researcher or in the email.
            If the customer email is 'Inquiry_type' then based on information from email_researcher_agent \
            state equipment's price if available else suggest similar items (that will also be given by researcher).
            If the customer email is 'review_type' then based on information from email_researcher_agent if the review is positive the customer and request them to share their \
            experience on social media, however in case of negative review apologise to the customer and offer gist voucher to them as well as \
            escalate the email to CRM system for follow-up with a phone call from customer service; so write a email to the customer service as well.
            If the customer email is 'assistance_request_type' then based on information from email_researcher_agent \
            write the email but if "NO RESEARCH FOUND" then escalate the issue to customer service (so write a email to the customer service as well.) \
            with email id {csr@csr.com} but never make anything on your own. 
            If the customer email is 'general_handling' then forward email to customer service (so write a email to the customer service as well.).
            STRICTLY WRITE EVERYTHING BASED on the INFO of RESEARCHER.
            Always sign off the emails in appropriate manner and from Atri.
            """,
    backstory="""You are a master at synthesizing a variety of information and writing a helpful email \
            that will address the customer's issues and provide them with helpful information""",
    llm=llm_model,
    # llm=llm_groq,
    allow_delegation=False,
    verbose=True,
)
