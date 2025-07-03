from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

from config import base_settings


class DBClient:
    """Client for interacting with the database"""

    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or base_settings.db_url
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        """Connect to the database"""
        if not self.connection:
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def close(self) -> None:
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.cursor = None
        self.connection = None

    def execute(self, query: str, params: tuple = None) -> None:
        """Execute a SQL query"""
        self.connect()
        self.cursor.execute(query, params or ())

    def execute_and_commit(self, query: str, params: tuple = None) -> None:
        """Execute a SQL query and commit the transaction"""
        self.connect()
        self.cursor.execute(query, params or ())
        self.connection.commit()

    def fetch_one(self, query: str, params: tuple = None) -> dict[str, Any] | None:
        """Execute a query and fetch one result"""
        self.connect()
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = None) -> list[dict[str, Any]]:
        """Execute a query and fetch all results"""
        self.connect()
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def insert(self, table: str, data: dict[str, Any]) -> int:
        """Insert data into a table and return the ID"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join("%s" for _ in data)
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"
        self.execute(query, values)
        result = self.cursor.fetchone()
        self.connection.commit()

        return result["id"]

    def update(self, table: str, data: dict[str, Any], condition: str, params: tuple = None) -> None:
        """Update data in a table"""
        set_clause = ", ".join(f"{key} = %s" for key in data)
        values = tuple(data.values())

        if params:
            values += params

        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        self.execute_and_commit(query, values)

    def delete(self, table: str, condition: str, params: tuple = None) -> None:
        """Delete data from a table"""
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_and_commit(query, params)

    def get_by_id(self, table: str, id: int) -> dict[str, Any] | None:
        """Get a record by ID"""
        return self.fetch_one(f"SELECT * FROM {table} WHERE id = %s", (id,))

    def get_all(self, table: str) -> list[dict[str, Any]]:
        """Get all records from a table"""
        return self.fetch_all(f"SELECT * FROM {table}")

    def execute_script(self, script_path: str) -> None:
        """Execute a SQL script file"""
        with open(script_path) as file:
            script = file.read()
            self.connect()
            self.cursor.execute(script)
            self.connection.commit()
