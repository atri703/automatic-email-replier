from crewai import Task
from agents import email_categorizer_agent, email_researcher_agent, email_writer_agent


def categorize_email(email_content):
        return Task(
            description=f"""Conduct a comprehensive analysis of the email provided and categorize into \
            one of the following categories:
            inquiry_type - used when someone is asking for an item 
            review_type - used when someone is providing review or feedback about something 
            assistance_request_type - used when someone is asking questions about film equipment 
            general_handling when it doesnt relate to any other category

            EMAIL CONTENT:\n\n {email_content} \n\n
            Output a single cetgory only""",
            expected_output="""A single categtory for the type of email from the types ('inquiry_type', 'review_type', 'assistance_request_type', 'general_handling') \
            eg:
            'review_type' \
            """,
            output_file=f"email_category.txt",
            agent=email_categorizer_agent
            )

def research_info_for_email(email_content):
        return Task(
            description=f"""Conduct a comprehensive analysis of the email provided and the category \
            provided and search the database or user_manual.pdf based on category to find info needed to respond to the email

            EMAIL CONTENT:\n\n {email_content} \n\n
            Only provide the info needed DONT try to write the email""",
            expected_output="""A set of bullet points of useful info for the email writer \
            or clear instructions that no useful material was found.""",
            # context = {"categorize_email": categorize_email},
            output_file=f"research_info.txt",
            agent=email_researcher_agent
            )

def draft_email(email_content):
        return Task(
            description=f"""Conduct a comprehensive analysis of the email provided, the category provided\
            and the info provided from the research specialist to write an email. \

            Write a simple, polite and too the point email which will respond to the customer's email. \
            If useful use the info provided from the research specialist in the email. \

            If no useful info was provided from the research specialist then escalate it to customer service, but don't make up info. \

            EMAIL CONTENT:\n\n {email_content} \n\n
            Output a single cetgory only""",
            expected_output="""A well crafted email for the customer that addresses their issues and concerns""",
            # context = {"categorize_email": categorize_email, "research_info_for_email":research_info_for_email},
            agent=email_writer_agent,
            output_file=f"draft_email.txt",
            )