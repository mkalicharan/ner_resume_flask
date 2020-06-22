from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import spacy
import os
import numpy as np
import docx2txt
import fitz
import mysql.connector

def unique_text(list1):
    arr = np.array(list1)
    arr1 = np.unique(arr)
    out = arr1.tolist()
    return out


def unique_entity(list1):
    arr = np.array(list1)
    arr1 = np.unique(arr)
    out = arr1.tolist()
    for ele in out:
        return ele


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


def store_database(in_text):
    nlp = spacy.load('my_model')
    model = nlp(in_text)
    labels = ["NAME", "DOB", "PHONENO", "EMAIL", "LOCATION", "EDUCATION", "UNIVERSITY", "COMPANIES WORKED AT",
              "PRIMARY SKILLS", "SECONDARY SKILLS"]
    entity = []
    text = []
    for ent in model.ents:
        entity.append(ent.label_.upper())
        text.append(ent.text)
    final_entity = []
    final_text = []
    for label in labels:
        sh_entity = []
        sh_text = []
        for i in range(len(entity)):
            if label == entity[i]:
                sh_entity.append(entity[i])
                sh_text.append(text[i])
        final_entity.append(unique_entity(sh_entity))
        final_text.append(unique_text(sh_text))

    for i in range(len(final_text)):
        my_str = ', '.join(final_text[i])
        final_text[i] = my_str
        if final_text[i] == '':
            final_text[i] = 'Not available'

    #print(final_text)
    return final_text


def db_update(input_text):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="mydatabase"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO api_test (NAME,DOB,PHONENO,EMAIL,LOCATION,EDUCATION,UNIVERSITY,COMPANIES,PRIMARY_SKILLS,SECONDARY_SKILLS) VALUES (%s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)"
    val = tuple(input_text)
    mycursor.execute(sql, val)

    mydb.commit()



UPLOAD_FOLDER = "uploader"
ALLOWED_EXTENSIONS = set(['pdf', 'docx'])
app = Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def postsPage():
    return render_template("about.html")


@app.route("/uploader", methods=["POST"])
def processReq():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        if filename.endswith('.pdf'):
            file_open = fitz.open(os.path.join(UPLOAD_FOLDER, filename))
            in_text = ""
            for page in file_open:
                in_text = in_text + str(page.getText())
                f_arr = store_database(in_text)
        elif filename.endswith('.docx'):
            in_text = docx2txt.process(os.path.join(UPLOAD_FOLDER, filename))
            f_arr = store_database(in_text)
    db_update(f_arr)
    return "Submitted!"



if __name__ == "__main__":
    app.run(debug=True)
