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
        "Address": ["Please state your address.", address_re, None]
    },
    "Education":
        {
            "Education_history": ["Please state your educational steps in the form of a "
                                  "continuous text. For each educational step please enter a time frame, "
                                  "the educational step and the name of the teaching institution", educ_re, None]
        },
    "Experience":
        {
            "Experience_history": ["Please state your work experience steps in bullet points or in the form of a "
                                   "continuous text.", exper_re, None]
        },
    "Social Engagement":
        {
            "Social_history": ["Please state your social engagements steps in bullet points or in the form of a "
                               "continuous text.", social_re, None]
        },
    "Skills":
        {
            "Skills": ["Please state your work experience steps in bullet points or in the form of a "
                       "continuous text.", skills_re, None]
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
            "Education_history": "This is where the education history is going to be stated, in the format of a time"
                                 "frame, the educational step and the teaching institution"
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
debug = False
