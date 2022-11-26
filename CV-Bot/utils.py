import re
import spacy


# currently loading spacy during every execution


# checks if the given input of the user actually contains the necessary information


def format_data(data, all_data, types):
    formated_data = []
    if len(data) % len(types) != 0:
        all_data_text = " ".join([d.text for d in all_data])
        data_text = " ".join([d.text for d in data])
        types_text = ", ".join([t for t in types])
        raise Exception("format_data: Looked for " + types_text + " Found " + str(
            len(data)) + " data, which isn't possible to put into " + len(
            types) + " fields." + "\n data: " + data_text + "\n all data: " + all_data_text)

    for i in range(len(data) % len(types)):
        current_data_set = data[(i * len(types)):((i + 1) * len(types))]

        formated_data.append(data[(i * len(types)):((i + 1) * len(types))])


# filter for valid inputs by user
name_re = "([A-Z]|[a-z])[a-z]+ ([A-Z]|[a-z])[a-z]+( ([A-Z]|[a-z])[a-z]+)*"
date_re = "([0-3]?[0-9].[0-1]?[0-9].[1-2][0-9][0-9][0-9])|([0-3]?[0-9]/[0-1]?[0-9]/[1-2][0-9][0-9][0-9])"
mail_re = ".+@.+\..+"
address_re = "[A-Z][a-z]*.? [0-9]*"
educ_re = None
exper_re = None
social_re = None
skills_re = None
interests_re = None


def to_string(t):
    return " ".join(t)


def print_cv(user_data):
    indent = "   "
    cv = "C I R R I C U L U M   V I T A E\n"
    for stage in data.keys():
        contains_data = False
        stage_text = stage + ":\n"
        for sub_headline in user_data[stage].keys():
            if user_data[stage][sub_headline][data_num] != None:
                contains_data = True
                stage_text += indent + sub_headline + ":\n"
                stage_text += indent + indent + user_data[stage][sub_headline][data_num] + "\n"
        if contains_data:
            cv += stage_text + "\n"
    print(cv)


data = {"Personal Data":
    {
        "Name": ["What is your full name?", {("PERSON", ""): None}],
        "Birthdate": ["What is your date of birth?", {("DATE", "CARDINAL"): None}],
        "E-Mail": ["Please tell me your email.", {("E-Mail", ""): None}],
        "Address": ["Please state your address.", {("Address", "CARDINAL"): None}]
    },
    "Education":
        {
            "Step 1": ["Please state an education step containing the teaching institution, a start date "
                       "and a end date.",
                       {("DATE", "CARDINAL", '1'): None,
                        ("DATE", "CARDINAL", '2'): None,
                        ("ORG", ""): None}]
        },
    "Experience":
        {
            "Step 1": ["Please state your work experience steps in bullet points or in the form of a "
                       "continuous text.",
                       {("DATE", "CARDINAL"): None}]
        },
    "Social Engagement":
        {
            "Step 1": ["Please state your social engagements steps in bullet points or in the form of a "
                               "continuous text.",
                               {("DATE", "CARDINAL"): None}]
        },
    "Skills":
        {
            "Skills": ["Please state your work experience steps in bullet points or in the form of a "
                       "continuous text.",
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
debug_data = {"Personal Data":
    {
        "Name": "Max Mustermann",
        "Birthdate": "20.12.2017",
        "E-Mail": "abc@gmail.com",
        "Address": "Bauerstr. 4"
    },
    "Education":
        {
            "Education_history": "From 2010 to 2019 I went to the Louise Schroeder School in Germany. After that, "
                                 "starting in 2020 I started my studies at the Technical University of Munich until 2023. "
                                 "From 2022 to 2022 it did an exchange abroad at the University Pompue Fabra"
        },
    "Experience":
        {
            "Experience_history": "asdfasdfasdfasdfasdf"
        },
    "Social Engagement":
        {
            "Social_history": "asdfasdfasdfasdf"
        },
    "Skills":
        {
            "Skills": "asdfjashdfkajsdhf"
        },
    "Interests":
        {
            "Interests": "asdhfakjsdhfasdf"
        },
}

check_data_questions = ["Can you show me what I entered for X?",
                        "What did you put as?", "Show me my X.",
                        "What are my X?"
                        ]
check_prev = ["Last", "last", "previous", "Previous"]

def print_data(stage):
    print("Requested to print the stage " + stage)

check_data_error = "check_data_not_found"

question_num = 0
fun_num = 1
data_num = 2
debug = False
data_store = 1
