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

    def get_current_stage_name(self):
        stage, _ = self.history[-1]
        return stage
    def get_current_stage_data(self):
        return data[self.get_current_stage_name()]
    def get_previous_stage(self):
        if len(self.history) > 1:
            stage, _ = self.history[-1]
            return stage
        else:
            return None  # Todo add error handling

    def add_new_stage(self, position):
        self.history.append((position, []))

    def get_current_question_name(self):
        _, questions = self.history[-1]
        if questions:
            return questions[-1]
        else:
            None  # Todo add error handling

    def get_current_question_data(self):
        return data[self.get_current_stage_name()][self.get_current_question_name()]

    def get_previous_question_name(self):
        _, questions = self.history[-1]
        if len(questions) > 1:
            return questions[-2]
        else:
            None  # Todo add error handling

    def add_question_to_history(self, question):
        self.history[-1][1].append(question)

    def handle_error(self, user_input, type):
        if type == check_data_error:
            print("Sorry unfortunately we couldn't find the data you were looking for.")
            new_input = input("Do you want to continue or try again?")
            if new_input.__contains__("again"):
                return self.classify(input("Please state your request again."))
            else:
                return None

    # ask according to the current position
    def ask(self, question):
        # get the answer from the user or from the debug data
        current_question = self.get_current_question_data()
        if debug:
            print(current_question[question_num])
            answer = debug_data[self.get_current_stage()][question]
        else:
            answer = input(current_question[question_num] + "\n")
        if debug:
            print(answer)
        return answer

    # agent starts to speak with user
    def speak(self):
        for position in self.data.keys():
            # add the new stage to the history
            self.add_new_stage(position)
            # get the value of the dict of the current stage (eg, Name, Birthdate ...)
            current_stage = self.get_current_stage_data()
            # go through all questions for the current stage, e.g. What is your name?
            for question in current_stage:
                # get processed input by user
                self.add_question_to_history(question)
                processed_input = self.understanding(self.ask(question))

                # store data
                current_question = self.get_current_question_data()
                data_dict = current_question[data_store]
                data_dict[list(data_dict)[0]] = processed_input

                print(data)

                # education and working experience
                self.sev_bullet_points()

    def understanding(self, user_input):
        input_type = self.classify(user_input)
        if input_type == "answer":
            return self.get_data(user_input)
        else:
            print_data(input_type)
            return self.understanding(self.ask(self.get_current_question_name()))

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
                        return key
                return self.handle_error(self, user_input, check_data_error)
        return "answer"

    def get_data(self, input):
        user_data = []
        # check if we are only looking for regex and not the SpaCy model
        current_question = self.get_current_question_data()
        necessary_entities = [element for innerList in current_question[fun_num].keys() for element in
                              innerList]
        doc = nlp(input)
        for entity in doc.ents:
            for type in necessary_entities:
                if entity.label_ == type:
                    user_data.append(entity.text)
        print(user_data)
        return user_data


    def sev_bullet_points(self):
        counter = 0
        position = self.get_current_stage_name()
        if position == 'Education' or position == 'Experience':
            while True:
                inp = input('If you would like to add another ' + str(position) + 'step enter the '
                                                                                       'information in '
                                                                                       'the same format '
                                                                                       'as already done. '
                                                                                       'Otherwise press '
                                                                                       'Enter' + "\n")

                if inp == "":
                    break;
                else:
                    # process the given input
                    processed_input = self.understanding(inp)

                    # create new dictionary element
                    print(self.get_current_stage_data())
                    stage = self.get_current_stage_data()
                    stage[('Step' + str(counter + 2))] = [None,
                                                                       {("DATE", "DATE", "CARDINAL", "ORG"): processed_input}]
                print(data)

