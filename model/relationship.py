from neo4j import GraphDatabase

uri = "neo4j+s://cd4757c6.databases.neo4j.io"
user = "neo4j"
password = "E-iOH0_IbCgU0BoBwfJUFaqPwsGz53THx6vG9Sr_Bb4"

driver = GraphDatabase.driver(uri,auth=(user,password))
session = driver.session()

class Relationship():
    def __init__(self, session):
        self.session = session

    def create_relation(self,person1,relation,relationship,person2):
        query = ("MATCH (a:Person),(b:Person) " 
                "WHERE a.surname = $person1 AND b.surname = $person2 " 
                "CREATE (a)-[r:relation { name: $relationship }]->(b) "
            )
        self.session.run(query, person1=person1, relation=relation,relationship=relationship, person2=person2)
    
    
    def allPersons(self):
        request ="MATCH (a)-[r]->(b) RETURN a,r,b" # Request with relationship
        # get data from database, we got an object
        result = self.session.run(request)
        liste_persons=[]
        for item in result.data():
            print(item)
            liste_persons.append(item)
        return liste_persons