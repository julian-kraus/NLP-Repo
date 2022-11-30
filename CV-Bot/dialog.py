from utils import *
import keyboard
import numpy as np
from numpy.linalg import norm
import Levenshtein
import sys



class Dialog:

    def __init__(self):
        self.data = data.copy()
        self.history = []
        self.check_data_vec = self.compute_vec_list(input_possible_values(check_data_questions))
        self.repeat_question_vec = self.compute_vec_list(repeat_info_questions)
        self.goodbye_question_vec = self.compute_vec_list(stop_statements)
        print("Hello, I am CV-Bot. I am here to help you create your CV.")
        self.speak()

    def compute_vec_list(self, list):
        return [nlp(elem).vector for elem in list]

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
            return self.handle_error("", no_prev_error)

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
            return self.handle_error("", no_prev_error)

    def add_question_to_history(self, question):
        self.history[-1][1].append(question)

    def print_data(self, elem):
        if elem is None:
            return
        text = ""
        show = False
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
        if text != "":
            print(text, end="")

    def goodbye(self): # Todo add some more prints
        print("C I R R I C U L U M   V I T A E\n")
        self.print_data("")
        sys.exit("Goodbye")
    def handle_error(self, user_input, type):
        if type == check_data_error:
            print("Sorry unfortunately we couldn't find the data you were looking for.")
            new_input = input("Do you want to continue or try again? \n")
            if self.check_input_for_words(new_input, check_again):
                return self.classify(input("Please state your request again. \n"))
            else:
                return None
        elif type == no_prev_error:
            print("Sorry i didn't find any previous data.")
            return None

    # ask according to the current position
    def ask(self, question, data_missing):
        # get the answer from the user or from the debug data
        current_question = self.get_current_question_data()
        if debug_text:
            print(current_question[question_num])
            answer = debug_text_data[debug_text_num].pop(0)
            print("Debug -- User: " + answer)
        else:
            if data_missing is not None:
                answer = input(str(data_missing) + ' - question: ' + current_question[question_num] + "\n")
            else:
                answer = input(current_question[question_num] + "\n")
        if debug_info:
            print("Debug -- received answer: " + answer)
        return answer

    # agent starts to speak with user
    def speak(self):
        for position in self.data.keys():
            # add the new stage to the history
            self.add_new_stage(position)
            print("Now we are going to go to your " + position)
            # get the value of the dict of the current stage (eg, Name, Birthdate ...)
            current_stage = self.get_current_stage_data()
            # go through all questions for the current stage, e.g. What is your name?
            for question in list(current_stage):
                # get processed input by user
                self.add_question_to_history(question)
                processed_input = self.understanding(self.ask(question, None))

                if debug_info:
                    print('Debug -- processed input: ' + str(processed_input))

                # store data
                current_question = self.get_current_question_data()
                data_dict = current_question[data_store]

                self.map_data(data_dict, processed_input, question)

                # education and working experience
                self.sev_bullet_points(question)

        self.goodbye()
    def understanding(self, user_input):
        type, data = self.classify(user_input)
        if debug_info:
            print("Debug -- classified input type:" + type)
        if type == "check_data":
            self.print_data(data)
            return self.understanding(self.ask(self.get_current_question_name(), None))
        elif type == "goodbye":
            self.goodbye()
        elif type == "repeat":
            return self.understanding(self.ask(self.get_current_question_name(), None))
        else:
            return self.get_data(data)

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
            return self.handle_error(user_input, check_data_error)

    def classify(self, user_input):
        user_vec = nlp(user_input).vector
        check_sim = self.similarity(user_vec, self.check_data_vec)
        repeat_sim = self.similarity(user_vec, self.repeat_question_vec)
        goodbye_sim = self.similarity(user_vec, self.goodbye_question_vec)
        max_sim = max(check_sim, repeat_sim, goodbye_sim)
        if max_sim < threshold:
            max_sim = 0
        if debug_info:
            print("Debug -- Similarities \ncheck_sim: " + str(check_sim) + ", repeat_sim: " + str(repeat_sim) + " goodbye_sim: " + str(goodbye_sim))
        if max_sim == 0:
            return "answer", user_input
        elif max_sim == check_sim:
            return "check_data", self.get_check_data(user_input)
        elif max_sim == repeat_sim:
            return "repeat", None
        else:
            return "goodbye", None

    def check_input_for_words(self, user_input, words):
        return any(str.lower(ele) in str.lower(user_input) for ele in words)
    def similarity(self, elem_vec, ls_vec):
        # Computes the max cosine similarity of the elem_vec to one of the ls_vecs
        max_sim = 0.0
        for vec in ls_vec:
            new_sim = np.dot(elem_vec, vec) / (norm(elem_vec) * norm(vec))
            if new_sim > max_sim:
                max_sim = new_sim
        return max_sim

    def get_data(self, input):
        user_data = []
        if self.get_current_question_name() == "Address":
            try:
                test = re.search(address_re, input).group()
                return [("Address", re.search(address_re, input).group())]
            except AttributeError:
                return None
        elif self.get_current_question_name() == "E-Mail":
            try:
                return [("E-Mail", re.search(mail_re, input).group())]
            except AttributeError:
                return None

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
            # value missing?
            if value == None:
                # until we have fitting input keep asking
                while True:
                    question_missing_info = 'The following information seems to be missing: ' + str(key[0]) + ' Please enter the information: \n'
                    processed_input = self.understanding(self.ask(question, question_missing_info))
                    if len(processed_input) != 0:
                        data_dict[key] = processed_input[0][1]
                        break;
    def sev_bullet_points(self, question):
        counter = 0
        position = self.get_current_stage_name()
        if position == 'Education' or position == 'Experience':
            while True:
                q = 'If you would like to add another ' + str(position) + 'step enter the information in the same ' \
                                                                          'format as already done. Otherwise press ' \
                                                                          'Enter \n '
                if debug_text:
                    inp = debug_text_data[debug_text_num].pop()
                else:
                    inp = input(q)

                if inp == "":
                    break
                else:
                    # process the given input
                    processed_input = self.understanding(inp)

                    # create new dictionary element

                    stage = self.get_current_stage_data()
                    stage[(str(counter + 2))] = [q,
                                                          {("DATE", "CARDINAL", '1'): None,
                                                           ("DATE", "CARDINAL", '2'): None,
                                                           ("ORG", ""): None}]
                    self.add_question_to_history((str(counter + 2)))
                    current_question = self.get_current_question_data()
                    data_dict = current_question[data_store]

                    if debug_info:
                        print(self.get_current_question_name())
                        print(data_dict)
                        print(current_question)
                        print(self.get_current_stage_data())

                    self.map_data(data_dict, processed_input, question)
                if debug_info:
                    print(data)
