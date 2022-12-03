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

!!!! Check if date checking is important (32.12.2001)
!!!! First check if it contains answer?
!!!! Get email fails with @ or @gmail.com
!!!! Doesn't recognize 05/11/2001
!!!! Make adress question more detailed, only street and number
!!!! Typo in education -> a end date => an end date
!!!! Typo in Educationstep (another step) => also a comma after it
!!!! Add to check question Can you repeat my X?
!!!! What is my adress again?  
Sorry unfortunately we couldn't find the data you were looking for.
Do you want to continue or try again?
What is my address again? 
Please state your request again. 
What is my address again?
=> Leads to an error
!!! Doesn't find anything to print -> say something?
!!! Only recognizes two name
!!! Which day was i born? for check data
!!! What to do about 2000/2000 as birthdate
Show me everything/Show me all -> leads error



The goal is to create, based on the information the user has given with the input fields, to create a CV containing all 
necessary personal information. Therefore, the CV has a defined structure which can be viewed in the utils.py File.
Part of the project is using trained pipelines/models

#### Execution: 
You need to have the package spaCy. Here is the installation guide https://spacy.io/usage 
To execute the CV-Bot you can either set the debug variable in utils.py to True and then run the main class (There is already example input and you dont need to enter any information via the input field). 
Or you can set the variable to False and the enter your own input. 


