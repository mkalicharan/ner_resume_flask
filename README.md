# ner_resume_flask
Resume Parsing using Spacy NER and Flask Deployment. 

####
                
+ Install dependencies
`$ pip install -r requirements.txt`

+ Dataset Building
Collect the Resume samples in either .dox or .pdf formats. Create a [Dataturks](https://dataturks.com/) account and create a new Document annotation project. Specify the labels and start the project. [Tutorial on how to use Dataturks annotation tool](https://dataturks.com/help/document-annotation-POS-NER.php)

+ Training the model using Goolge colab 
 Run the Spacy NER training python notebook using google colab and download the trained model. For more information on [Spacy training](https://spacy.io/usage/training)

+ Flask Deployment 
First change the labels if you are using your own model in main.py and create_database.py. Next, create the sql database using create_database.py. Finally, run the main.py to launch the flask server. All the resume parsed details will get stored in the database. 
