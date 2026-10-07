"""Deliberately over-layered, but contract-equivalent teaching example."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Username:
    value: str

    @classmethod
    def parse(cls, value):
        if not isinstance(value, str):
            raise TypeError("username must be a string")
        if not 1 <= len(value) <= 64 or "\x00" in value:
            raise ValueError("username must contain 1..64 characters without NUL")
        return cls(value)

@dataclass(frozen=True)
class Query:
    statement: str
    parameters: tuple

class UserQueryBuilder:
    def build(self, username):
        return Query(
            "SELECT id, username, email FROM users WHERE username = ?",
            (username.value,),
        )

class SQLiteGateway:
    def __init__(self, connection):
        self.connection = connection

    def fetch_one(self, query):
        row = self.connection.execute(query.statement, query.parameters).fetchone()
        return tuple(row) if row is not None else None

class UserRepository:
    def __init__(self, gateway, builder):
        self.gateway = gateway
        self.builder = builder

    def find(self, username):
        return self.gateway.fetch_one(self.builder.build(username))

def get_user(conn, username):
    name = Username.parse(username)
    repository = UserRepository(SQLiteGateway(conn), UserQueryBuilder())
    return repository.find(name)
