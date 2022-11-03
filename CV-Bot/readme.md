# Readme
## Cv-Bot

### Current status
#### Goal:

The goal is to create, based on the information the user has given with the input fields, to create a CV containing all 
necessary personal information. Therefore, the CV has a defined structure which can be viewed in the utils.py File.
Part of the project is using trained pipelines/models (TODO: https://spacy.io/usage/models#download)

#### Questions: 
1. Valid approach on questioning, e.g. on Education history? 
   1. If these variables/requirements are not met then the next step would be to initialize a further dialog with the user
   2. How should we get a history about e.g. education? A text? A text with specified markers for each step? Questions for every step?
2. Which model would suit here bests? --> Spacy? What is the best approach on finding the correct model?
3. How much should the user drive the conversation? Should the user be the initator, with us giving suggestions for content, if the user asks for it? Should we give a guide on how the user can ask questions? 
4. Define scopes of the next step 

#### Next steps: 
1. Improve the structure of the CV 
2. Choose the model 
3. First attempt on implementing the model 
   1. Based on the model improve the dialog with the client. 


