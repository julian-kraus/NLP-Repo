# Readme
## Cv-Bot

### Current status
Current features: 
- Entered wrong format? 
    - Ask question for missing information
- Ask for data to be displayed
  - Previous or specific or all works, regardless whether it is a question or stage
  - If it doesn't get recognized, user gets the possibility to enter again or continue
- Multiple continuous points for education and work experience

#### Goal:

The goal is to create, based on the information the user has given with the input fields, to create a CV containing all 
necessary personal information. Therefore, the CV has a defined structure which can be viewed in the utils.py File.
Part of the project is using trained pipelines/models

#### Execution: 
You need to have the package spaCy. Here is the installation guide https://spacy.io/usage 
To execute the CV-Bot you can either set the debug variable in utils.py to True and then run the main class (There is already example input and you dont need to enter any information via the input field). 
Or you can set the variable to False and the enter your own input. 


