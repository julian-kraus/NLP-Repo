from utils import *
import keyboard
import numpy as np
from numpy.linalg import norm
import Levenshtein

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
            return self.handle_error("", no_prev_error)

    def add_new_stage(self, position):
        self.history.append((position, []))

    def get_current_question_name(self):
        _, questions = self.history[-1]
        return questions[-1]

    def get_current_question_data(self):
        return data[self.get_current_stage_name()][self.get_current_question_name()]

    def get_previous_question_name(self):
        _, questions = self.history[-1]
        if len(questions) > 1:
            return questions[-2]
        else:
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
        else:
            print("I didn't found any data to show you")

    def handle_error(self, user_input, type):
        if type == check_data_error:
            print("Sorry unfortunately we couldn't find the data you were looking for.")
            new_input = input("Do you want to continue or try again? \n")
            if any(ele in new_input for ele in ["again", "Again"]):
                return self.classify(input("Please state your request again. \n"))
            else:
                return None
        elif type == no_prev_error:
            raise Exception("Tried to look at previous data, without any existing")

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
            print("Now we are going to go to your " + position)
            # get the value of the dict of the current stage (eg, Name, Birthdate ...)
            current_stage = self.get_current_stage_data()
            # go through all questions for the current stage, e.g. What is your name?
            for question in list(current_stage):
                # get processed input by user
                self.add_question_to_history(question)
                processed_input = self.understanding(self.ask(question))

                if debug:
                    print('processed input')
                    print(processed_input)

                # store data
                current_question = self.get_current_question_data()
                data_dict = current_question[data_store]

                for key, value in data_dict.items():
                    for inp in list(processed_input):
                        if inp[0] in key:
                            data_dict[key] = inp[1]
                            processed_input.remove(inp)
                            break;

                if debug:
                    self.print_data("")

                # education and working experience
                self.sev_bullet_points()

    def understanding(self, user_input):
        input_type = self.classify(user_input)
        if not input_type or input_type != "answer":
            self.print_data(input_type)
            return self.understanding(self.ask(self.get_current_question_name()))
        elif input_type == "answer":
            return self.get_data(user_input)

    # Possible returns are "answer" or the stage that is supposed to get printed
    def classify(self, user_input):
        if self.similar(user_input, check_data_questions, 0.4):
            if any(e in user_input for e in check_prev):
                return self.get_previous_stage()
            else:
                return self.get_most_similar(user_input, data_keys)
                # for key in self.data.keys():
                #     if self.similar(key, user_input, 0.25):
                #         return key
                #     for q in self.data[key].keys():
                #         if self.similar(q, user_input, 0.25):
                #             return q

        return "answer"

    def get_most_similar(self, input, compare):
        d = {}
        for elem in compare:
            d[elem] = Levenshtein.distance(input, elem) #self.similarity(input, elem)
        max_val = max(d.values())
        for key, value in d.items():
            if max_val == value:
                return key
        return self.handle_error(input, check_data_error)
    def similarity(self, elem, ls):
        elem_vec = np.array(nlp(elem).vector)
        if type(ls) == type([]):
            ls_vec = self.compute_avg_vec(ls)
        else:
            ls_vec = np.array(nlp(ls).vector)
        cosine = np.dot(elem_vec, ls_vec) / (norm(elem_vec) * norm(ls_vec))
        return cosine
    def similar(self, elem, ls, threshold):
        return self.similarity(elem, ls) > threshold


    def get_data(self, input): # TODO add regex for address and email
        user_data = []
        if self.get_current_question_name() == "Adress":
            return [("Adress", re.search(address_re, input).group())]
        elif self.get_current_question_name() == "E-Mail":
            return [("E-Mail", re.search(mail_re, input).group())]

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

                    stage = self.get_current_stage_data()
                    stage[('Step' + str(counter + 2))] = [None,
                                                          {("DATE", "CARDINAL", '1'): None,
                                                           ("DATE", "CARDINAL", '2'): None,
                                                           ("ORG", ""): None}]
                    self.add_question_to_history(('Step' + str(counter + 2)))
                    current_question = self.get_current_question_data()
                    data_dict = current_question[data_store]

                    if debug:
                        print(self.get_current_stage_data())
                        print(self.get_current_question_name())
                        print(data_dict)
                        print(current_question)

                    for key, value in data_dict.items():
                        for inp in list(processed_input):
                            if inp[0] in key:
                                data_dict[key] = inp[1]
                                processed_input.remove(inp)
                                break;
                if debug:
                    print(data)
