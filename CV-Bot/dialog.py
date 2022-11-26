from utils import *
import keyboard
import numpy as np
from numpy.linalg import norm

spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')


class Dialog:

    def __init__(self):
        self.data = data.copy()
        self.history = []
        self.check_data_vec = self.compute_avg_vec(check_data_questions)
        print("Hello, I am CV-Bot. I am here to help you create your CV.")
        self.speak()

    def compute_avg_vec(self, list):
        vector = np.array([nlp(elem).vector for elem in list]).mean(axis=0)
        return vector

    def get_current_stage(self):
        stage, _ = self.history[-1]
        return stage

    def get_previous_stage(self):
        if len(self.history) > 1:
            stage, _ = self.history[-1]
            return stage
        else:
            return None  # Todo add error handling

    def add_new_stage(self, position):
        self.history.append((position, []))

    def get_current_question(self):
        _, questions = self.history[-1]
        if questions:
            return questions[-1]
        else:
            None  # Todo add error handling

    def get_previous_question(self):
        _, questions = self.history[-1]
        if len(questions) > 1:
            return questions[-2]
        else:
            None  # Todo add error handling

    def add_question_to_history(self, question):
        self.history[-1][1].append(question)

    # ask the question according to the current position
    def ask(self, question):
        # get the answer from the user or from the debug data
        current_question = self.data[self.get_current_stage()][self.get_current_question()]
        if debug:
            print(current_question[question_num])
            answer = debug_data[self.get_current_stage()][question]
        else:
            answer = input(current_question[question_num] + "\n")
        if debug:
            print(answer)
        return answer

    def listen(self, input):
        ...
        # wait as long as keyboard is pressed

    # agent starts to speak with user
    def speak(self):
        for position in self.data.keys():
            # add the new stage to the history
            self.add_new_stage(position)
            # get the value of the dict of the current stage (eg, Name, Birthdate ...)
            current_stage = self.data[self.get_current_stage()]
            # go through all questions for the current stage, e.g. What is your name?
            for question in current_stage:
                self.add_question_to_history(question)
                current_question = current_stage[question]
                if question == "E-Mail" or question == "Address":
                    processed_input = current_question[fun_num](self.ask(question))
                else:
                    processed_input = self.understanding(self.ask(question))
                    self.map_input_to_data(processed_input)

    def understanding(self, user_input):
        input_type = self.classify(user_input)
        if input_type == "answer":
            return self.get_data(input_type, user_input)
        else:
            print_data(input_type)
            self.ask(self.get_current_question())

    # Possible returns are "answer" or the stage that is supposed to get printed
    def classify(self, user_input):
        user_input_vec = np.array(nlp(user_input).vector)
        cosine = np.dot(user_input_vec, self.check_data_vec) / (norm(user_input_vec) * norm(self.check_data_vec))
        if cosine > 0.3:
            if any(e in user_input for e in check_prev):
                return self.get_previous_stage()
            else:
                for key in self.data.keys():
                    if user_input.__contains__(key):
                        print("Found stage " + key)
                        return self.data[key]
        return "answer"

    def get_data(self, input):
        user_data = []
        # check if we are only looking for regex and not the SpaCy model
        current_question = self.data[self.get_current_stage()][self.get_current_question()]
        necessary_entities = [element for innerList in current_question[fun_num].keys() for element in
                              innerList]
        doc = nlp(input)
        for entity in doc.ents:
            for type in necessary_entities:
                if entity.label_ == type:
                    user_data.append(entity.text)
        print(user_data)
        return user_data

    # if "DATE" in types:
    #     answer = answer.replace(".", "/")
    #     answer = answer.replace(",", "/")
    #
    # doc = nlp(answer)
    # data = []
    # # filter all entities that are our searched type
    # for entity in doc.ents:
    #     for t in types:
    #         if entity.label_ == t:
    #             data.append(entity.text)
    # # check if we found the correct data
    # if 0 < numData != len(data):
    #     data_text = " ".join([d.text for d in data])
    #     types_text = ", ".join([t for t in types])
    #     doc_data_text = " ".join(["(" + d.text + ", " + d.label_ + ") " for d in doc.ents])
    #     raise Exception("get_data: Looked for " + types_text + " Found " + str(
    #         len(data)) + "data, while expecting " + str(
    #         numData) + " \n The found data are " + data_text + "\n the data in the doc is " + doc_data_text)
    # else:
    #     return format_fun(data)

    def map_input_to_data(self, user_data):
        print("Needs to mapped")
