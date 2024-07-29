from crewai import Crew,Process
from tasks import categorize_email,research_info_for_email,draft_email
from agents import email_categorizer_agent, email_researcher_agent, email_writer_agent
import sqlite3

conn = sqlite3.connect('company.db')
cursor = conn.cursor

email = """
        Subject: Inquiry about Camera Availability

        Dear Film Equipment Rental,

        I am interested in renting a Canon EOS C300 Mark III for an upcoming project. Can you please let me know if it is available and the rental price?

        Best regards,
        John Doe
        johndoe@example.com"""

# email = """
#         Subject: Excellent Service!

# Dear Film Equipment Rental,

# I recently rented the Sony FS7 camera, and I was extremely satisfied with the service and the equipment quality. Thank you for a great experience!

# Best,
# John Doe
# johndoe@example.com
# """

# email = """
#         Subject: Disappointed with the Equipment

# Dear Film Equipment Rental,

# I rented the Dedolight DLED7 last week, and it did not function properly. The light was flickering and caused issues during my shoot. I am very disappointed with this experience.

# Sincerely,
# John Doe
# johndoe@example.com

# """


########### Assistance type info not present
# email = """
#         Subject: Need Help with Microphone Setup

# Hi,

# I am having trouble setting up the Rode NTG3 microphone I rented from your service. Can you provide me with some guidance or a manual to help me out?

# Thanks,
# John Doe
# johndoe@example.com
# """


############### General Handling
# email = """
#         Subject: Collaboration Inquiry

# Dear Film Equipment Rental,

# I am reaching out to discuss a potential collaboration between our companies. We are interested in exploring how we can work together for mutual benefit.

# Looking forward to your response.

# Best,
# John Doe
# johndoe@example.com

# """

############# Assistance - Info is present
# email = """
#         Subject: Need to know about different camera lenses

# Hi,

# I want to buy a new camera for filming. Can you suggest me different types of camera lenses used? 

# Thanks,
# John Doe
# johndoe@example.com
# """

############# Assistance - Info is present
# email = """
#         Subject: Need to know about audio levels

# Hi,

# Can anyone help me adjust the audio levels?

# Thanks,
# John Doe
# johndoe@example.com
# """



## Forming the tech focused crew with some enhanced configuration
categorize_email_task=categorize_email(email)
research_task=research_info_for_email(email)
writing_task=draft_email(email)

crew=Crew(
    agents=[email_categorizer_agent, email_researcher_agent, email_writer_agent],
    tasks=[categorize_email_task,research_task,writing_task],
    process=Process.sequential,

)

## starting the task execution process wiht enhanced feedback

result=crew.kickoff()
print(result)