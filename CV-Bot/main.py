# This is a sample Python script.
import re
from utils import *

def check_for_alphabet(string):
    return True

def check_answer(answer, regex):
    print(answer)
    if regex:
        val = re.search(regex, answer)
    return answer


def ask_question(stage):
    current_stage = data[stage]
    for attr in current_stage.keys():
        answer = input(current_stage[attr][question_num] + "\n") if not debug else debug_data[stage][attr]
        current_stage[attr][data_num] = check_answer(answer, current_stage[attr][re_num])


def print_results():
    indent = "   "
    cv = "C I R R I C U L U M   V I T A E\n"
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
    for stage in data.keys():
        ask_question(stage)
    print_results()

run()
