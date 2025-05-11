from neo4j import GraphDatabase
from config import SANDBOX_URI, SANDBOX_USER, SANDBOX_PASSWORD
from models import Person, Relationship
import logging
from typing import List, Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Neo4jCRUD:
    def __init__(self):
        """Inicializa a conexão com o banco de dados"""
        try:
            self.driver = GraphDatabase.driver(
                SANDBOX_URI,
                auth=(SANDBOX_USER, SANDBOX_PASSWORD),
                encrypted=False,  
                connection_timeout=15,
                max_connection_pool_size=5
            )
            logger.info("✅ Driver configurado com sucesso!")
        except Exception as e:
            logger.error(f"❌ Falha na configuração: {str(e)}")
            raise

    def create_person(self, person: Person) -> Optional[Person]:
        """Cria uma nova pessoa no banco"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    """CREATE (p:Person {
                        name: $name, 
                        age: $age, 
                        profession: $profession,
                        email: $email
                    }) RETURN p""",
                    **person.to_dict()
                )
                created = result.single()[0]
                logger.info(f"✅ Pessoa criada: {created['name']}")
                return Person.from_dict(created)
        except Exception as e:
            logger.error(f"❌ Erro ao criar pessoa: {str(e)}")
            return None

    def get_person(self, name: str) -> Optional[Person]:
        """Obtém uma pessoa pelo nome"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    "MATCH (p:Person {name: $name}) RETURN p",
                    name=name
                )
                record = result.single()
                return Person.from_dict(record['p']) if record else None
        except Exception as e:
            logger.error(f"❌ Erro ao buscar pessoa: {str(e)}")
            return None

    def get_all_people(self) -> List[Person]:
        """Retorna todas as pessoas"""
        try:
            with self.driver.session() as session:
                result = session.run("MATCH (p:Person) RETURN p")
                return [Person.from_dict(record['p']) for record in result]
        except Exception as e:
            logger.error(f"❌ Erro ao listar pessoas: {str(e)}")
            return []

    def update_person(self, name: str, updates: Dict[str, Any]) -> Optional[Person]:
        """Atualiza os dados de uma pessoa"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    """MATCH (p:Person {name: $name})
                    SET p += $updates
                    RETURN p""",
                    name=name,
                    updates=updates
                )
                record = result.single()
                return Person.from_dict(record['p']) if record else None
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar pessoa: {str(e)}")
            return None

    def delete_person(self, name: str) -> bool:
        """Remove uma pessoa do banco"""
        try:
            with self.driver.session() as session:
                session.run(
                    "MATCH (p:Person {name: $name}) DELETE p",
                    name=name
                )
                logger.info(f"✅ Pessoa {name} removida")
                return True
        except Exception as e:
            logger.error(f"❌ Erro ao deletar pessoa: {str(e)}")
            return False

    def create_relationship(
        self, 
        from_name: str, 
        to_name: str, 
        relationship: Relationship
    ) -> bool:
        """Cria um relacionamento entre duas pessoas"""
        try:
            with self.driver.session() as session:
                session.run(
                    f"""MATCH (a:Person {{name: $from_name}}), 
                        (b:Person {{name: $to_name}})
                    MERGE (a)-[r:{relationship.type}]->(b)
                    SET r += $properties""",
                    from_name=from_name,
                    to_name=to_name,
                    properties=relationship.properties
                )
                logger.info(f"✅ Relacionamento criado: {from_name} -> {to_name}")
                return True
        except Exception as e:
            logger.error(f"❌ Erro ao criar relacionamento: {str(e)}")
            return False

    def get_relationships(self, name: str) -> List[Dict]:
        """Obtém todos os relacionamentos de uma pessoa"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    """MATCH (p:Person {name: $name})-[r]->(other)
                    RETURN type(r) as type, properties(r) as props, other.name as name""",
                    name=name
                )
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"❌ Erro ao buscar relacionamentos: {str(e)}")
            return []

    def find_people_by_profession(self, profession: str) -> List[Person]:
        """Encontra pessoas por profissão"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    "MATCH (p:Person {profession: $profession}) RETURN p",
                    profession=profession
                )
                return [Person.from_dict(record['p']) for record in result]
        except Exception as e:
            logger.error(f"❌ Erro ao buscar por profissão: {str(e)}")
            return []

    def get_friends_of_friends(self, name: str) -> List[Dict]:
        """Encontra amigos de amigos (2º grau)"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    """MATCH (p:Person {name: $name})-[:KNOWS*2]->(fof)
                    WHERE NOT (p)-[:KNOWS]->(fof)
                    RETURN DISTINCT fof.name as name, fof.profession as profession""",
                    name=name
                )
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"❌ Erro ao buscar amigos de amigos: {str(e)}")
            return []

    def close(self):
        """Fecha a conexão com o banco"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.close()
            logger.info("🔌 Conexão encerrada")