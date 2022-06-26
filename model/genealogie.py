from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    # def create_friendship(self, name, surname, birthday):
    #     with self.driver.session() as session:
    #         # Write transactions allow the driver to handle retries and transient errors
    #         result = session.write_transaction(
    #             self._create_and_return_friendship, name, surname, birthday)
    #         # # for row in result:
    #         # print(result)
    # def create_friendsh(self, name, surname, birthday):
    #     with self.driver.session() as session:
    #         # Write transactions allow the driver to handle retries and transient errors
    #         result = session.write_transaction(
    #             self._create_and_return_friendship, name, surname, birthday)
    #         # # for row in result:
    #         # print(result)

    @staticmethod
    def _create_and_return_friendship(tx, name, surname, birthday):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $name, surname: $surname, birthday: $birthday }) "
            "RETURN p1"
        )
        result = tx.run(query, name=name, surname=surname, birthday=birthday)
        try:
            return result
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]


# if __name__ == "__main__":
#     # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
#     uri = "neo4j+s://cd4757c6.databases.neo4j.io"
#     user = "<Username for Neo4j Aura instance>"
#     password = "<Password for Neo4j Aura instance>"
#     app = App(uri, user, password)
#     app.create_friendship("Alice", "David")
#     app.find_person("Alice")
#     app.close()