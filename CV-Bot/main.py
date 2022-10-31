# This is a sample Python script.
import re


def check_for_alphabet(string):
    return True


# filter for valid inputs by user
name_re = "([A-Z]|[a-z])[a-z]+ ([A-Z]|[a-z])[a-z]+( ([A-Z]|[a-z])[a-z]+)*"
date_re = "([0-3]?[0-9].[0-1]?[0-9].[1-2][0-9][0-9][0-9])|([0-3]?[0-9]/[0-1]?[0-9]/[1-2][0-9][0-9][0-9])"
mail_re = ".+@.+\..+"
address_re = None
educ_re = None
exper_re = None
social_re = None
skills_re = None
interests_re = None

data = {"Personal Data":
    {
        "Name": ["What is your full name?", name_re, None],
        "Birthdate": ["What is your date of birth?", date_re, None],
        "E-Mail": ["Please tell me your email.", mail_re, None],
        "Address": ["Where do you live?", address_re, None]
    },
    "Education":
        {
            "Education_history": ["Please state your educational steps in bullet points or in the form of a "
                                  "continuous text", educ_re, None]
        },
    "Experience":
        {
            "Experience_history": ["Please state your work experience steps in bullet points or in the form of a "
                                   "continuous text", exper_re, None]
        },
    "Social Engagement":
        {
            "Social_history": ["Please state your social engagements steps in bullet points or in the form of a "
                               "continuous text", social_re, None]
        },
    "Skills":
        {
            "Skills": ["Please state your work experience steps in bullet points or in the form of a "
                       "continuous text", skills_re, None]
        },
    "Interests":
        {
            "Interests": ["If you would like to state any personal interests in your CV please enter them here: ",
                          interests_re, None]
        },
}

debug_data = {"Personal Data":
    {
        "Name": "Max Mustermann",
        "Birthdate": "01.01.2001",
        "E-Mail": "abc@gmail.com",
        "Address": "Bauerstr. 4"
    },
    "Education":
        {
            "Education_history": "asdfasdfasdfasdfasdf"
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
re_num = 1
data_num = 2
debug = True



def check_answer(answer, regex):
    print(answer)
    if regex:
        val = re.search(regex, answer)
        print(val)
    return answer


def ask_question(stage):
    current_stage = data[stage]
    for attr in current_stage.keys():
        answer = input(current_stage[attr][question_num] + "\n") if not debug else debug_data[stage][attr]
        current_stage[attr][data_num] = check_answer(answer, current_stage[attr][re_num])


def print_results():
    indent = "   "
    cv = "curriculum vitae\n"
    for stage in data.keys():
        contains_data = False
        stage_text = stage + ":\n"
        for sub_headline in data[stage].keys():
            if data[stage][sub_headline][data_num] != None:
                contains_data = True
                stage_text += indent + sub_headline + ":\n"
                stage_text += indent + indent + data[stage][sub_headline][data_num] + "\n"
        if contains_data:
            cv += stage_text + "\n"
    print(cv)

def run():
    print()
    for stage in data.keys():
        ask_question(stage)
    print_results()


run()
