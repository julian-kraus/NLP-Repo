import spacy
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')


# To use for debugging
debug_info = False
debug_text = True
debug_text_key = "Standard" # Possible: Standard, Check_Repetition, False_Inputs, Mixed
debug_text_data = {
    "Standard": [
        # Personal Information
        "Hey, my name is Max Mustermann.",
        "Of course. It is the 5.11.2001",
        "max@mustermann.com",
        "My address is Baumstr. 123.",
        # Education
        "Oh yeah, sure. I was in Louise Schroeder School until 05.11.2019. I think I started in 05.11.2010.",
        "From 05.11.2020 to 05.11.2021 I went to the University Pompeu Fabra in Spain.",
        "",
        # Work Experience
        "From 05.11.2000 to 01.01.2008 I worked at Google in Germany.",
        "I worked at Siemens from 05.11.2005 until 05.11.2006",
        "I worked at Microsoft from 05.11.2006 until 05.11.2010",
        "",
        # Social Engagement
        "Oxfam International from 05.11.2006 until 05.11.2010",
        "",
        # Skills
        "Programming in Java is one of my biggest skills.",
        "I also like programming in Python",
        ""
    ],
    "Check_Repetition": [
        # Personal Information
        "Max Mustermann",
        "I was born on the 5.11.2001",
        "Please repeat the question.",
        "My email adress is max@mustermann.com.",
        "Baumstreet 123",
        "What did you put as my name?",
        # Education
        "I was in Louise Schroeder School from 2010 to 2019.",
        "",
        "Can you show me everything you saved so far?",
        # Work Experience
        "My first Job was at Google. I think I worked there 2000 - 2005.",
        "",
        # Social Engagement
        "From 2006 until 2009 I helped out at Oxfam International.",
        "",
        # Skills
        "Programming in Java is one of my biggest skills.",
        "I also like programming in Python",
        "Show me my address.",
        "",
        "Goodbye"
    ],
    "False_Inputs":[
        # Personal Information
        "asdf123",
        "Well... Hello to you too. You can call me Max Mustermann.",
        "The 35.11.2001",
        "My birthdate? It is the 5.11.2001",
        "It is max@mustermann.com. Here you go.",
        "I live in Baumstreet 123.",
        # Education
        "From 05.11.2010 until 29.04.2001 at Louise Schroeder School",
        "",
        # Work experience
        "From the 05.11.2011 until 12.04.2012",
        "Technical University of Munich",
        "I also worked at Siemens I think I worked there from 05.11.2011 until the 05.11.2016",
        # Social Engagement
        "Oxfam International 05.11.2006 until 05.11.2009",
        # Skills
        "I think I am finished",
    ],
    "Mixed": [
        # Personal Information
        "Hello Chat Bot. Nice to meet you. My name is Max Mustermann.",
        "What did you save for the last question?",
        "I was born on the 5.11.2001.",
        "It is the max@mustermann.com.",
        "",
        "I am currently living in Baumstreet 123.",
        # Education
        "I want to see what you put as Education.",
        "From 2010 to 2019 I went to the Louise Schroeder School in Germany.",
        "",
        # Work experience
        "I worked at Google from 2000 to 2005.",
        "From 2005 until 2006 Siemens",
        "Show me my Personal Data.",
        "From 2006 to 2009 I worked at Microsoft in Spain.",
        "Fromm 2010 until 2012 Siemens",
        "",
        # Social Engagement
        "I worked at Oxfam International from 2006 to 2009 to help end poverty.",
        "",
        # Skills
        "My main expertise is with Java",
        "And also a bit Python.",
        "I didn't catch that. Can you repeat it please?",
        ""
    ]

}

data = {
    "Personal Data":
    {
        "Name": ["What is your full name?", {("PERSON", ""): None}],
        "Birthdate": ["What is your date of birth?", {("DATE", "CARDINAL"): None}],
        "E-Mail": ["Please tell me your email.", {("E-Mail", ""): None}],
        "Address": ["Please state your address. Only the address is enough, no postal code etc.", {("Address", ""): None}]
    },
    "Education":
        {
            "1": ["Please state an education step containing the teaching institution, a start date "
                  "and an end date.",
                  {("DATE", 'Start'): None,
                   ("DATE", 'End'): None,
                   ("ORG", ""): None}]
        },
    "Experience":
        {
            "1": ["Please state a step of your working experience containing the company, a start date "
                  "and an end date.",
                  {("DATE", 'Start'): None,
                   ("DATE", 'End'): None,
                   ("ORG", ""): None}]
        },
    "Social Engagement":
        {
            "1": ["Please state a social engagement step containing the institution, a start date "
                  "and an end date.",
                  {("DATE", 'Start'): None,
                   ("DATE", 'End'): None,
                   ("ORG", ""): None}]
        },
    "Skills":
        {
            "1": ["Please state a skill that you would like mentioned in your CV.",
                       {("GPE", "PERSON"): None}]
        }
}

check_data_questions = ["Can you show me what I entered for X?",
                        "What did you put as X?", "Show me my X.",
                        "What are my X?",
                        "Tell me about X."
                        "Show me the last questions stage.",
                        "What did you put in last?"
                        "What was saved in the X?",
                        "What did I answer in the previous question?",
                        "I want to see X.",
                        "Which day was I born?",
                        "Can you repeat my X?",
                        "Show me everything.",
                        "Show me all data."
                        ]

repeat_info_questions = ["Please repeat the question.",
                        "Can you please repeat that.",
                         "State the question again.",
                         "Can you repeat the question?",
                         "I didn't catch that."
                         "I want to hear it once more."
                         "Show it once more.",
                         "I didn't understand that. Repeat it please?"
                         ]

stop_statements = ["I want to stop",
                   "I am finished",
                   "Stop the dialog",
                   "Goodbye",
                   "Bye",
                   "It is over"
                   ]

check_prev = ["last", "previous", "before"]
check_stage = ["stage", "phase", "section"]
check_again = ["again", "more"]
check_all = ["all", "every", "full"]

data_keys = {
    "Personal Data": ["Personal", "Personal", "About me"],
    "Name": ["Name", "called"],
    "Birthdate": ["Date", "Birth", "Born"],
    "E-Mail": ["Mail"],
    "Address": ["Address", "Residence", "Home", "live"],
    "Education": ["Education", "School", "University"],
    "Skills": ["Skill", "Action", "Capabilities"],
    "Social Engagement": ["Social", "Engagement"],
    "Experience": ["Experience"],
    "Interests": ["Interests"]
}

# filter for valid inputs by user other than spacy
mail_re = "[a-zA-Z0-9_.\-+]+@[a-zA-Z0-9]+\.[a-zA-Z]+"#".+@.+\..+"
address_re = "[A-Z]+[a-z]+.? [0-9]+"
date_formats = ['%Y-%m-%d', '%Y', '%Y.%m.%d', '%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d']


# Useful for getting data out of the data structure
question_num = 0
fun_num = 1
data_num = 2
data_store = 1
threshold = 0.7

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



