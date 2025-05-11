from crud_operations import Neo4jCRUD
from models import Person, Relationship
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("\n=== DEMONSTRAÇÃO COMPLETA DE CRUD ===")
    
    try:
        db = Neo4jCRUD()
        
        logger.info("\n1. Criando pessoas...")
        alice = Person("Alice", 28, "Engenheira", "alice@email.com")
        bob = Person("Bob", 32, "Designer", "bob@email.com")
        carol = Person("Carol", 25, "Cientista de Dados", "carol@email.com")
        
        db.create_person(alice)
        db.create_person(bob)
        db.create_person(carol)

        logger.info("\n2. Listando todas as pessoas:")
        for person in db.get_all_people():
            logger.info(f"- {person.name} ({person.age} anos), {person.profession}")

        logger.info("\n3. Atualizando Bob...")
        db.update_person("Bob", {"age": 33, "profession": "Designer Sênior"})
        updated_bob = db.get_person("Bob")
        logger.info(f"Bob atualizado: {updated_bob.profession}, {updated_bob.age} anos")

        logger.info("\n4. Criando relacionamentos...")
        db.create_relationship("Alice", "Bob", Relationship("KNOWS", {"since": 2020}))
        db.create_relationship("Bob", "Carol", Relationship("KNOWS", {"since": 2021}))
        
        logger.info("\n5. Relacionamentos de Alice:")
        for rel in db.get_relationships("Alice"):
            logger.info(f"- Conhece {rel['name']} desde {rel['props'].get('since', '?')}")

        logger.info("\n6. Buscando amigos de amigos (Alice):")
        for fof in db.get_friends_of_friends("Alice"):
            logger.info(f"- {fof['name']} ({fof['profession']})")

        logger.info("\n7. Removendo Carol...")
        db.delete_person("Carol")
        
    except Exception as e:
        logger.error(f"\n💥 ERRO: {str(e)}")
    finally:
        if 'db' in locals():
            db.close()
        logger.info("\n=== FIM DA DEMONSTRAÇÃO ===")

if __name__ == "__main__":
    main()