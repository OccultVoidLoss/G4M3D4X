
from abc import ABC, abstractmethod

class User:

    def __init__(self, nome, email, senha, id=None):
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__id = id
    
    @abstractmethod
    def to_dict(self):
        pass
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, v):
        self.__nome = (v)


    @property
    def email(self):
        return (self.__email)
    
    
    @email.setter
    def email(self, valor):
        self.__email = valor


    @property 
    def senha(self):
        return self.__senha
    
    @senha.setter
    def dev(self, valor):
        self.__senha = (valor)

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, v):
        self.__id = (v)



    @abstractmethod
    def tipo(self):
        pass
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, v):
        self.__id = (v)
class Comum(User):
    def __init__(self, nome, email, senha, id=None):
        super().__init__(nome,email,senha, id)
    def tipo(self):
        return "comum"
    def to_dict(self):
            return {
            "nome": self.__nome,
            "email": self.__email,
            "senha": self.__senha,
            "id":self.__id,
            "tipo":self.tipo()
        }
    

class Admin(User):
    def __init__(self, nome, email, senha, id=None):
        super().__init__(nome,email,senha, id)
    def tipo(self):
        return "admin"
    def to_dict(self):
            return {
            "nome": self.__nome,
            "email": self.__email,
            "senha": self.__senha,
            "id":self.__id,
            "tipo":self.tipo()
        }
    