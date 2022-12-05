from datetime import datetime

from utils import *
import numpy as np
from numpy.linalg import norm
import sys
import os
import re


class Dialog:

    def __init__(self):
        self.data = data.copy()
        self.history = []
        self.check_data_vec = self.compute_vec_list(input_possible_values(check_data_questions))
        self.repeat_question_vec = self.compute_vec_list(repeat_info_questions)
        self.goodbye_question_vec = self.compute_vec_list(stop_statements)
        os.system('clear')
        os.system('cls')
        self.say("Hello, I am CV-Bot. I am here to help you create your CV.")
        self.converse()

    """ Used for interaction with the user"""

    def say(self, text):
        format_ = '\033[33;1m'
        end = '\033[0m'
        print(format_ + text + end)

    def request(self, text):
        format_ = '\033[33;1m'
        end = '\033[0m'
        return input(format_ + text + end)

    """ --------------------------------------- """

    def print_debug(self, text):
        if debug_info:
            format_ = '\033[31m'
            end = '\033[0m'
            print("DEBUG: " + format_ + text + end)

    def compute_vec_list(self, list):
        return [nlp(elem).vector for elem in list]

    """ Interact with the history """

    def get_current_stage_name(self):
        stage, _ = self.history[-1]
        return stage

    def get_current_stage_data(self):
        return self.data[self.get_current_stage_name()]

    def get_previous_stage(self):
        if len(self.history) > 1:
            stage, _ = self.history[-1]
            return stage
        else:
            self.say("Sorry i didn't find any previous data.")
            return None

    def add_new_stage(self, position):
        self.history.append((position, []))

    def get_current_question_name(self):
        _, questions = self.history[-1]
        return questions[-1]

    def get_current_question_data(self):
        return self.data[self.get_current_stage_name()][self.get_current_question_name()]

    def get_previous_question_name(self):
        _, questions = self.history[-1]
        if len(questions) > 1:
            return questions[-2]
        else:
            if len(self.history) > 1:
                return self.history[-2][1][-1]
            self.say("Sorry I didn't find any previous data.")
            return ""

    def add_question_to_history(self, question):
        self.history[-1][1].append(question)

    """ --------------------------------------- """

    def print_data(self, elem):
        string = self.get_data_as_string(elem)
        if string != "":
            print(string, end="")

    def get_data_as_string(self, elem):
        if elem is None:
            return
        text = ""
        for stage in self.data.keys():

            stage_text = ""
            if stage.__contains__(elem):
                stage_text += stage + ":\n"

            for sub_stage in self.data[stage]:
                if stage.__contains__(elem) or sub_stage.__contains__(elem):
                    sub_stage_text = sub_stage + ":"
                    for data in list(self.data[stage][sub_stage][1].values()):
                        if data:
                            sub_stage_text += " " + str(data)
                    if sub_stage_text != sub_stage + ":":
                        stage_text += sub_stage_text + "\n"
            if stage_text and stage_text != stage + ":\n":
                text += stage_text
        return text

    # agent starts to speak with user
    def converse(self):
        for position in self.data.keys():
            # add the new stage to the history
            self.add_new_stage(position)
            self.say("Now we are going to go to your " + position)
            # get the value of the dict of the current stage (eg, Name, Birthdate ...)
            current_stage = self.get_current_stage_data()
            # go through all questions for the current stage, e.g. What is your name?
            for question in list(current_stage):
                # get processed input by user
                self.add_question_to_history(question)

                processed_input = self.understand(self.ask(question, None))

                self.print_debug("Processed input: " + str(processed_input))

                while (processed_input == 'not valid'):
                    self.say(
                        'Sorry the entered input for ' + self.get_current_question_name() + ' was not valid. Please enter again. ')
                    processed_input = self.understand(self.ask(question, None))
                    self.print_debug("Processed input: " + str(processed_input))

                # store data
                current_question = self.get_current_question_data()
                data_dict = current_question[data_store]

                self.map_data(data_dict, processed_input, question)

                # education and working experience
                self.sev_bullet_points(question)

        self.goodbye()

    def ask(self, question, data_missing):
        # get the answer from the user or from the debug data
        current_question = self.get_current_question_data()
        if debug_text:
            self.say(current_question[question_num])
            answer = debug_text_data[debug_text_key].pop(0)
            print(answer)
        else:
            if data_missing is not None:
                answer = self.request(str(data_missing) + ' - question: ' + current_question[question_num] + "\n")
            else:
                answer = self.request(current_question[question_num] + "\n")

        self.print_debug("Received answer: " + answer)
        if answer == "":
            self.say("Sorry I didn't quite catch that.")
            return self.ask(question, data_missing)
        return answer

    def understand(self, user_input):
        type, data = self.classify(user_input)
        self.print_debug("Classified input type: " + type)
        if type == "check_data":
            text = self.get_data_as_string(data)
            if text == "":
                self.say("Sorry I didn't find any data to show you. I will continue with the CV.")
            return self.understand(self.ask(self.get_current_question_name(), None))
        elif type == "goodbye":
            self.goodbye()
        elif type == "repeat":
            self.say("Sure, no problem.")
            return self.understand(self.ask(self.get_current_question_name(), None))
        else:
            return self.get_data(data)

    def classify(self, user_input):
        user_vec = nlp(user_input).vector
        check_sim = self.similarity(user_vec, self.check_data_vec)
        repeat_sim = self.similarity(user_vec, self.repeat_question_vec)
        goodbye_sim = self.similarity(user_vec, self.goodbye_question_vec)
        max_sim = max(check_sim, repeat_sim, goodbye_sim)
        if max_sim < threshold:
            max_sim = 0

        self.print_debug("Similarities check_sim: " + str(check_sim) + ", repeat_sim: " + str(
            repeat_sim) + " goodbye_sim: " + str(goodbye_sim))

        if max_sim == 0:
            return "answer", user_input
        elif max_sim == check_sim:
            return "check_data", self.get_check_data(user_input)
        elif max_sim == repeat_sim:
            return "repeat", None
        else:
            return "goodbye", None

    def similarity(self, elem_vec, ls_vec):
        # Computes the max cosine similarity of the elem_vec to one of the ls_vecs
        max_sim = 0.0
        max_sim_lst = [(np.dot(elem_vec, vec) / (norm(elem_vec) * norm(vec)), vec) for vec in ls_vec]
        for vec in ls_vec:
            new_sim = np.dot(elem_vec, vec) / (norm(elem_vec) * norm(vec))
            if new_sim > max_sim:
                max_sim = new_sim
        return max_sim

    def get_check_data(self, user_input):
        # Check for previous
        if self.check_input_for_words(user_input, check_prev):
            # Check for previous stage
            if self.check_input_for_words(user_input, check_stage):
                return self.get_previous_stage()
            else:
                # Otherwise question
                return self.get_previous_question_name()
        # Check for all
        elif self.check_input_for_words(user_input, check_all):
            return ""
        else:
            # Check stage keys
            for key in self.data.keys():
                if self.check_input_for_words(user_input, data_keys[key]):
                    return key
                # Check question keys except the bulletpoints
                for q in self.data[key].keys():
                    if q == "1":
                        break
                    if self.check_input_for_words(user_input, data_keys[q]):
                        return q
            return self.noCheckDataFound()

    def noCheckDataFound(self):
        self.say("Sorry unfortunately we couldn't find the data you were looking for.")
        new_input = self.request("Do you want to continue or try again? \n")
        category, data = self.classify(new_input)
        if category == "answer" or "repeat":
            if self.check_input_for_words(new_input, check_again):
                return self.classify(self.request("Please state your request again. \n"))
            else:
                return None
        else:
            self.understand(new_input)
            self.noCheckDataFound()

    def check_input_for_words(self, user_input, words):
        return any(str.lower(ele) in str.lower(user_input) for ele in words)

    def get_data(self, input):
        user_data = []
        if self.get_current_question_name() == "Address":
            try:
                test = re.search(address_re, input).group()
                return [("Address", re.search(address_re, input).group())]
            except AttributeError:
                return 'not valid'
        elif self.get_current_question_name() == "E-Mail":
            try:
                return [("E-Mail", re.search(mail_re, input).group())]
            except AttributeError:
                return 'not valid'

        # check if we are only looking for regex and not the SpaCy model
        current_question = self.get_current_question_data()
        necessary_entities = [element for innerList in current_question[fun_num].keys() for element in
                              innerList]
        doc = nlp(input)
        for entity in doc.ents:
            for type in necessary_entities:
                if entity.label_ == type:
                    user_data.append(tuple((type, entity.text)))

        # when filtering dates remove possibly created duplicates
        user_data = list(set([i for i in user_data]))
        return user_data

    def map_data(self, data_dict, processed_input, question):
        for key, value in data_dict.items():
            for inp in list(processed_input):
                if inp[0] in key:
                    data_dict[key] = inp[1]
                    processed_input.remove(inp)
                    break
        # check if all necessary information are given
        for key, value in data_dict.items():
            question_missing_info = 'The following information seems to be missing: ' + str(
                key[0]) + ' Please enter the information: \n'

            self.bring_date_to_format(data_dict, key, value, question, question_missing_info)
            # value missing?
            if value == None:
                # until we have fitting input keep asking
                while True:
                    if key[0] is 'DATE' and (
                            self.get_current_stage_name() is 'Education' or self.get_current_stage_name() is 'Experience'):
                        processed_input = self.understand(self.ask(question, question_missing_info))
                    else:
                        processed_input = self.understand(self.ask(question, question_missing_info))

                    if len(processed_input) != 0:
                        self.bring_date_to_format(data_dict, key, processed_input, question, question_missing_info)
                        break;

    def bring_date_to_format(self, data_dict, key, processed_input, question, question_missing_info):
        if type(processed_input) == list:
            value = processed_input[0][1]
        else:value = processed_input
        if value is not None and key[0] is 'DATE':
            if not self.check_valid_date(value):
                date = False
                while date == False:
                    print('Unfortunately the format you entered your Date in seemed to be not correct. Please try '
                          'again.')
                    print('Currently not correct is your ' + key[2] + 'date.')
                    processed_input = self.understand(self.ask(question, question_missing_info))
                    if len(processed_input) != 0:
                        date = self.check_valid_date(processed_input[0][1])
                        data_dict[key] = date.strftime('%d/%m/%Y')
            else:
                data_dict[key] = self.check_valid_date(value).strftime('%d/%m/%Y')

    # code from https://code.activestate.com/recipes/578245-flexible-datetime-parsing/
    def check_valid_date(self, string):
        "Parse a string into a datetime object."
        for fmt in date_formats:
            try:
                return datetime.strptime(string, fmt)
            except ValueError:
                pass
        return False

    def sev_bullet_points(self, question):
        counter = 0
        position = self.get_current_stage_name()
        q = 'If you would like to add another ' + str(position) + 'step enter the information in the same ' \
                                                                  'format as already done. Otherwise press ' \
                                                                  'Enter \n '
        if position == 'Education' or position == 'Experience' or position == 'Skills':
            while True:
                if debug_text:
                    inp = debug_text_data[debug_text_key].pop(0)
                    print(inp)
                else:
                    inp = self.request(q)

                if inp == "":
                    break
                else:
                    # process the given input
                    processed_input = self.understand(inp)

                    # create new dictionary element

                    stage = self.get_current_stage_data()
                    if position == 'Skills':
                        stage[(str(counter + 2))] = [q,
                                                     {("GPE", 'PERSON'): None,}]
                    else: stage[(str(counter + 2))] = [q,
                                                 {("DATE", "CARDINAL", '1'): None,
                                                  ("DATE", "CARDINAL", '2'): None,
                                                  ("ORG", ""): None}]
                    self.add_question_to_history((str(counter + 2)))
                    current_question = self.get_current_question_data()
                    data_dict = current_question[data_store]

                    self.print_debug(
                        self.get_current_question_name() + "\n" + str(data_dict) + "\n" + str(current_question) + "\n" + str(
                            self.get_current_question_data()))

                    self.map_data(data_dict, processed_input, question)

                self.print_debug(str(data))

    def goodbye(self):
        self.say("I hope I could help you with your CV. Until another time.")
        cv = self.get_data_as_string("")
        if cv:
            self.say("I'll print your CV so you can use it for your next application.\n")
            print("C I R R I C U L U M   V I T A E\n")
            print(cv)
        self.say("Goodbye!\n")
        sys.exit()
