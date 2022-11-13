import re
import spacy
# currently loading spacy during every execution
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

# checks if the given input of the user actually contains the necessary information
def get_data(numData, types, answer, format_fun):
    if "DATE" in types:
        answer = answer.replace(".", "/")
        answer = answer.replace(",", "/")


    doc = nlp(answer)
    data = []
    # filter all entities that are our searched type
    for entity in doc.ents:
        for t in types:
            if entity.label_ == t:
                data.append(entity.text)
    # check if we found the correct data
    if 0 < numData != len(data):
        data_text = " ".join([d.text for d in data])
        types_text = ", ".join([t for t in types])
        doc_data_text = " ".join(["(" + d.text + ", " + d.label_ + ") " for d in doc.ents])
        raise Exception("get_data: Looked for " + types_text + " Found " + str(
            len(data)) + "data, while expecting " + str(numData) + " \n The found data are " + data_text + "\n the data in the doc is " + doc_data_text)
    else:
        return format_fun(data)


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

data = {"Personal Data":
    {
        "Name": ["What is your full name?", lambda doc: get_data(1, ["PERSON"], doc, to_string), None],
        "Birthdate": ["What is your date of birth?", lambda doc: get_data(1, ["DATE", "CARDINAL"], doc, to_string), None],
        "E-Mail": ["Please tell me your email.", lambda t: re.search(mail_re, t).group(), None],
        "Address": ["Please state your address.", lambda t: re.search(address_re, t).group(), None] # TODO Train spaCY on adresses
    },
    "Education":
        {
            "Education_history": ["Please state your educational steps in the form of a "
                                  "continuous text. For each educational step please enter a time frame, "
                                  "the educational step and the name of the teaching institution", lambda doc: get_data(-1, ["DATE", "ORG"], doc, to_string), None]
        },
    "Experience":
        {
            "Experience_history": ["Please state your work experience steps in bullet points or in the form of a "
                                   "continuous text.", lambda x: x, None]
        },
    "Social Engagement":
        {
            "Social_history": ["Please state your social engagements steps in bullet points or in the form of a "
                               "continuous text.", lambda x: x, None]
        },
    "Skills":
        {
            "Skills": ["Please state your work experience steps in bullet points or in the form of a "
                       "continuous text.", lambda x: x, None]
        },
    "Interests":
        {
            "Interests": ["If you would like to state any personal interests in your CV please enter them here: ",
                          lambda x: x, None]
        },
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
            "Education_history": "2017 i worked at Samsung and then 2019 i switched to Apple"
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
question_num = 0
fun_num = 1
data_num = 2
debug = True
