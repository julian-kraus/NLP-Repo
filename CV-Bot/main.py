# This is a sample Python script.
import re


def check_for_alphabet(string):
    return True

name_re = "([A-Z]|[a-z])[a-z]+ ([A-Z]|[a-z])[a-z]+( ([A-Z]|[a-z])[a-z]+)*"
date_re = "([0-3]?[0-9].[0-1]?[0-9].[1-2][0-9][0-9][0-9])|([0-3]?[0-9]/[0-1]?[0-9]/[1-2][0-9][0-9][0-9])"
data = {"Personal Data":
            {"Name": ["What is your full name?", name_re, None, None],
             "Birthdate": ["What is your date of birth?", date_re, None]}
        }
question_num = 0
re_num = 1
data_num = 2
def check_answer(answer, regex):
    if regex:
        val = re.search(regex, answer)
        print(val)
    return answer
def ask_question(stage):
    current_stage = data[stage]
    for attr in current_stage.keys():
        answer = input(current_stage[attr][question_num] + "\n")
        current_stage[attr][data_num] = check_answer(answer, current_stage[attr][re_num])

def run():

    for stage in data.keys():
        ask_question(stage)
        print(data[stage]["Name"])

run()


