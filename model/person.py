from neo4j import GraphDatabase

uri = "neo4j+s://cd4757c6.databases.neo4j.io"
user = "neo4j"
password = "E-iOH0_IbCgU0BoBwfJUFaqPwsGz53THx6vG9Sr_Bb4"

driver = GraphDatabase.driver(uri,auth=(user,password))
session = driver.session()

class Person():
    def __init__(self, session):
        self.session = session

    def create_person(self,name,surname,birthday,profil,pseudo):
        query = (
            "CREATE (p1:Person { name: $name, surname: $surname, birthday: $birthday, profil: $profil, pseudo: $pseudo }) "
            "RETURN p1"
        )
        self.session.run(query, name=name, surname=surname, birthday=birthday, profil=profil,pseudo=pseudo)
    
    def findPersons(self,pseudo):
        request ="MATCH (n:Person { pseudo: $pseudo }) RETURN n" # Request with relationship
        # get data from database, we got an object
        result = self.session.run(request, pseudo=pseudo)
        result = result.data()
        return result[0]['n']
    
    def allPersons(self):
        request ="MATCH (n) RETURN n" # Request with relationship
        # get data from database, we got an object
        result = self.session.run(request)
        liste_persons=[]
        for item in result.data():
            liste_persons.append(item['n'])
        return liste_persons
    

    # def set_person(self,name,attribute,value):
    #     val="MATCH (n { surname: $name })"
    #     print(val)
    #     val1="SET n.{attribute} = {value}".format(attribute,value)
    #     print(val1)
    #     query = (val+val1)
    #     # print(query)
    #     self.session.run(query, name=name)