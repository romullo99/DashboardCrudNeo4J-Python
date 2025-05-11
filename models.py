class Person:
    def __init__(self, name, age, profession, email=None):
        self.name = name
        self.age = age
        self.profession = profession
        self.email = email
    
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "profession": self.profession,
            "email": self.email
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            age=data['age'],
            profession=data['profession'],
            email=data.get('email')
        )

class Relationship:
    def __init__(self, type, properties=None):
        self.type = type
        self.properties = properties or {}
    
    def to_dict(self):
        return {
            "type": self.type,
            "properties": self.properties
        }