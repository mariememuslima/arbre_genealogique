from flask import Flask, render_template, request, jsonify
from flask_cors import CORS 
import jwt
from model.genealogie import *
from model.person import *
from model.relationship import *

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "luvRT8YHB82*%YBvhikblnvb$ln!=*m"

# db = SQLAlchemy(app)
uri = "neo4j+s://cd4757c6.databases.neo4j.io"
user = "neo4j"
password = "E-iOH0_IbCgU0BoBwfJUFaqPwsGz53THx6vG9Sr_Bb4"




@app.route('/')
def home():
    return render_template("hello, world")


@app.route('/connect/<pseudo>/')
def connect(pseudo):
    find_person = Person(session)
    person = find_person.findPersons(pseudo)
    data = {"username":person["pseudo"],"password":person["password"],"profil":person["profil"]}
    token = jwt.encode(data,app.secret_key,algorithm="HS256")
    return token


@app.route('/persons/<pseudo>/')
def findPerson(pseudo):
    find_person = Person(session)
    person = find_person.findPersons(pseudo)
    return person


@app.route('/persons/', methods=['POST'])
def postPerson():
    person = request.get_json()
    allPerson = Person(session)
    allPerson.create_person(person['name'],person['surname'],person['birthday'],person['profil'])
    # app.find_person("Alice")
    return person

@app.route('/persons/')
def getPersons():
    allPerson = Person(session)
    result = allPerson.allPersons()
    return jsonify(result)


@app.route('/set/person/', methods=['POST'])
def setPerson():
    person = request.get_json()
    allPerson = Person(session)
    allPerson.set_person(person['name'],person['attribute'],person['value'])
    # app.find_person("Alice")
    return person



@app.route('/relations/', methods=['POST'])
def postRelation():
    relation = request.get_json()
    relat = Relationship(session)
    relat.create_relation(relation['person1'],relation['relation'],relation['relationship'],relation['person2'])
    return relation

@app.route('/relations/')
def getRelations():
    allPerson = Person(session)
    result = allPerson.allPersons()
    return jsonify(result)



if __name__=='__main__':
    app.run(debug=True)
