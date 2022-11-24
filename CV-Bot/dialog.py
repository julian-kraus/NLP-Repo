from utils import *
import keyboard

spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')


class Dialog:

    def __init__(self):
        self.state = "asd"
        self.position = "Personal Data"
        self.data = data.copy()
        self.current_stage = self.data[self.position]
        self.current_question = None
        print("Hello, I am CV-Bot. I am here to help you create your CV.")
        self.speak()

    # ask the question according to the current position
    def ask(self, question):
        # get the answer from the user or from the debug data
        #self.current_question = self.current_stage[question]
        if debug:
            print(self.current_question[question_num])
            answer = debug_data[self.position][question]
        else:
            answer = input(self.current_question[question_num] + "\n")
        if debug:
            print(answer)
        return answer

    def listen(self, input):
        ...
        # wait as long as keyboard is pressed

    # agent starts to speak with user
    def speak(self):
        for position in self.data.keys():
            self.position = position
            self.current_stage = self.data[position]
            # go throuh all questions for the current stage, e.g. What is your name?
            for question in self.current_stage:
                self.current_question = self.current_stage[question]
                if question == "E-Mail" or question == "Address":
                    processed_input = self.current_question[fun_num](self.ask(question))
                else:
                    processed_input = self.understanding(self.ask(question))
                    self.map_input_to_data(processed_input)

    def understanding(self, user_input):
        input_type = self.classify(user_input)
        return self.get_data(input_type, user_input)

    def classify(self, user_input):
        # Todo Use a model to decide
        return "answer"

    def get_data(self, input_type, input):
        user_data = []
        if input_type == 'answer':
            # check if we are only looking for regex and not the SpaCy model
            necessary_entities = [element for innerList in self.current_question[fun_num].keys() for element in innerList]
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

