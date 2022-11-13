# This is a sample Python script.
import re
from utils import *

def check_for_alphabet(string):
    return True

def ask_question(stage):
    current_stage = data[stage]
    for attr in current_stage.keys():
        # get the answer from the user or from the debug data
        answer = input(current_stage[attr][question_num] + "\n") if not debug else debug_data[stage][attr]
        # call check answer with the answer and the formatation function
        check_answer = current_stage[attr][fun_num]
        current_stage[attr][data_num] = check_answer(answer)


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
    # go through all sections of the CV 
    for stage in data.keys():
        # for each section ask the accordingly stored questions
        ask_question(stage)
    print_results()

run()
