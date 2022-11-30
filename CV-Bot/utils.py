import spacy
import re

import contextlib

with contextlib.redirect_stdout(None):
    spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')


# currently loading spacy during every execution



# filter for valid inputs by user
name_re = "([A-Z]|[a-z])[a-z]+ ([A-Z]|[a-z])[a-z]+( ([A-Z]|[a-z])[a-z]+)*"
date_re = "([0-3]?[0-9].[0-1]?[0-9].[1-2][0-9][0-9][0-9])|([0-3]?[0-9]/[0-1]?[0-9]/[1-2][0-9][0-9][0-9])"
mail_re = ".+@.+\..+"
address_re = "[A-Z]+[a-z]+.? [0-9]+"
educ_re = None
exper_re = None
social_re = None
skills_re = None
interests_re = None

data = {"Personal Data":
    {
        "Name": ["What is your full name?", {("PERSON", ""): None}],
        "Birthdate": ["What is your date of birth?", {("DATE", "CARDINAL"): None}],
        "E-Mail": ["Please tell me your email.", {("E-Mail", ""): None}],
        "Address": ["Please state your address.", {("Address", ""): None}]
    },
    "Education":
        {
            "1": ["Please state an education step containing the teaching institution, a start date "
                  "and a end date.",
                  {("DATE", "CARDINAL", '1'): None,
                   ("DATE", "CARDINAL", '2'): None,
                   ("ORG", ""): None}]
        },
    "Experience":
        {
            "1": ["Please state an step of your working experience containing the company, a start date "
                  "and a end date.",
                  {("DATE", "CARDINAL", '1'): None,
                   ("DATE", "CARDINAL", '2'): None,
                   ("ORG", ""): None}]
        },
    "Social Engagement":
        {
            "1": ["Please state a social engagement step containing the the institution, a start date "
                  "and a end date.",
                  {("DATE", "CARDINAL", '1'): None,
                   ("DATE", "CARDINAL", '2'): None,
                   ("ORG", ""): None}]
        },
    "Skills":
        {
            "Skills": ["Please state skills you would liked mentioned in your CV.",
                       {("DATE", "CARDINAL"): None,
                        ("DATE", "CARDINAL"): None,
                        ("ORG", ""): None}]
        },
    "Interests":
        {
            "Interests": ["If you would like to state any personal interests in your CV please enter them here: ",
                          {("DATE", "CARDINAL"): None,
                           ("DATE", "CARDINAL"): None,
                           ("ORG", ""): None}]
        }
}


check_data_questions = ["Can you show me what I entered for X?",
                        "What did you put as X?", "Show me my X.",
                        "What are my X?",
                        "Tell me about X."
                        "Show me the last questions stage."
                        "What was saved in the X?",
                        "What did I answer in the previous question?"
                        ]

repeat_info_questions = ["Can you please repeat that",
                         "State the question again",
                         "Can you repeat the question?"
                         ]

stop_statements = ["I want to stop",
                   "I am finished",
                   "Stop the dialog",
                   "Goodbye",
                   "Bye"
                   ]


def input_possible_values(lst):
    values = list(data_keys.values())
    result_list = []
    for elem in lst:
        if "X" in elem:
            for val in [i for sub in values for i in sub]:
                result_list.append(str.replace(elem, "X", val))
        else:
            result_list.append(elem)
    return result_list


check_prev = ["last", "previous", "before"]
check_stage = ["stage", "phase", "section"]
check_again = ["again", "more"]
check_all = ["all", "every", "full"]
data_keys = {
    "Personal Data": ["Personal", "Personal", "About me"],
    "Name": ["Name"],
    "Birthdate": ["Date"],
    "E-Mail": ["Mail"],
    "Address": ["Adress"],
    "Education": ["Education", "School", "University"],
    "Skills": ["Skill", "Action"],
    "Social Engagement": ["Social", "Engagement"],
    "Experience": ["Experience"],
    "Interests": ["Interests"]
}

# Error codes
check_data_error = "check_data_not_found"
no_prev_error = "prev"

question_num = 0
fun_num = 1
data_num = 2
debug_info = True
debug_text = False
debug_text_num = 0
data_store = 1
threshold = 0.6

debug_text_data = [
    ["Max Mustermann",
     "20/12/2017",
     "abc@gmail.com",
     "Bauerstr. 4",
     "From 2010 to 2019 I went to the Louise Schroeder School in Germany.",
     "After that starting in 2020 I started my studies at the Technical University of Munich until 2023.",
     "",
     "From 2010 to 2019 I went to the Louise Schroeder School in Germany.",
     "After that starting in 2020 I started my studies at the Technical University of Munich until 2023.",
     "From 2022 to 2022 it did an exchange abroad at the University Pompue Fabra",
     "",
     "Programming and Languages",
     "Programming and Languages",
     "",
     "Programming and Languages",
     "Programming and Languages",
     "",
     "Goodbye"]
]
