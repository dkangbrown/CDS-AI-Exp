from openai import OpenAI
from dotenv import load_dotenv
import csv
import sys

load_dotenv()
client = OpenAI(api_key="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")
csv.field_size_limit(sys.maxsize)

sr_data = list(csv.reader(open('data/SR_Referents.csv', newline=''), delimiter=',', quotechar='"'))

prompt1_header = 'I will give you a transcription of a text about an enslaved native American. A human coder extracted information about an individual in the text into the entries below the transcription. NULL indicates that the data for the entry was not found in the text. Check any error, spelling mistake, or missing information of the human structured data. Here is an example.\
                  Example Text Transcription———\n\
                  3011	Court records	Other	1677-12-13 00:00:00	<p dir="ltr">[173] Zebulon Udall bound over to this Court being accused for getting Dr. Taylors Indyan mayde with Child. Shee not being yet brought to bed both to bee bound over to the next Court. [&hellip;] [174] Dr. Taylour saith hee heard Roger Toweenesend confesse the same on his death bed.</p>\n\n\
                  Example Data———\n\
                  First name: Dr.\n\
                  Last name: Traylor\n\
                  Tribes: NULL\n\
                  Sex: Male\n\
                  Age: \n\
                  Age category: NULL\n\
                  Occupation: Plumber\n\
                  Race: White\n\
                  Enslavement Status: free person ▸ enslaver or owner\n\
                  Enslavement Relationship: "owner of": {"id": 8299, "last": "", "name": " ", "first": ""}\n\n\
                  Example Answer———\n\
                  First name: "Dr." is not a first name\n\
                  Last name: "Traylor" is a misspelling of the data in the source, "Taylour"\n\
                  Tribes: Correct\n\
                  Sex: Correct\n\
                  Age: Correct\n\
                  Age category: Correct\n\
                  Occupation: Doctor, not plumber\n\
                  Race: Correct, although there is no explicit evidence that the person is white, we can infer from the historical context\n\
                  Enslavement status: correct\n\
                  Enslavement relationship: correct\n\n\
                  Now check the error for the transcription and data below.\n\n\
                  Task Text Transcription———\n'

def get_prompt(row) -> str:
    return prompt1_header + row[16] + "\n\nTask Data———" + \
      "\nFirst name: " + row[1] + "\nLast name: " + row[2] + "\nTribes: " + row[3] + "\nSex: " + row[4] + "\nAge: " + row[5] + "\nAge category: " + row[6] + "\Origins: " + row[7] + "\nOccupations: " + row[8] +  "\nRaces: " + row[9] + "\Enslavement status: " + row[10] + "\nEnslavement relationships: " + row[11]\
      + "\n\nTask Answer———\n"

# print(get_prompt(sr_data[1]))

def get_review(row) -> str:
  p1_response = client.chat.completions.create(
    model = "gpt-3.5-turbo-0125",
    temperature = 0.8,
    max_tokens = 3000,
    messages = [
      {"role": "user", "content": get_prompt(row)}
    ]
  )

  prompt2_header = 'Below is a review of a data field. Could you use the information to create a JSON file? It must have fields "First name", "Last name", "Tribes", "Sex", "Age", "Age Category", "Origins", "Occupation", "Races", "Enslavement status", "Enslavement relationships", and have values either -1 if the field is empty or NULL, 0 if it is correct, and 1 if it needs review or change.\n\n'

  p2_response = client.chat.completions.create(
    model = "gpt-3.5-turbo-0125",
    temperature = 0.8,
    max_tokens = 3000,
    messages = [
      {"role": "user", "content": prompt2_header + p1_response.choices[0].message.content}
    ]
  )

  return p2_response.choices[0].message.content

print(get_review(sr_data[2]))