from typing import Optional
import sqlite3
import secrets

from utils.logger import logger


class Database:
    """
    Main database class, uses the `endpoints` set to efficiently
    manage the current existing urls.

    Database usage:

    The database is loaded only a single time on the application,
    after it the application uses the `endpoints` set to track
    the data and requests. Checking for items in a set is O(1).
    """
    endpoints = set()

    def __init__(self, db_path: str = "database/database.db"):
        # Connect to the database
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

        # Load or create the database table
        self.__load_endpoints()
        logger.info("Database started!")

    def create_paste(self, content: str, /) -> str:
        """
        Creates a new paste into the database

        Parameter
        ---------
        content: `str`
            The paste content that will be commited into the db

        Returns
        -------
        id : `str`
            This functions creates an id/url for the paste, commits
            both id and content into the database and returns the id.
        """
        id = self.create_url()
        self.endpoints.add(id)

        self.cursor.execute(
            "INSERT INTO pastes VALUES (?, ?)", (id, content)
        )
        self.connection.commit()

        return id

    def read_content(self, id: str, /) -> Optional[str]:
        """
        Tries to retrieve content into database given an id.

        Parameter
        ---------
        id : `str`
            The corresponding content id's that will be searched

        Returns
        -------
            The content string if exists else `None`.
        """
        fetch = self.cursor.execute(
            "SELECT content FROM pastes WHERE id == (?)", (id,)
        ).fetchone()

        return fetch[0] if fetch else None

    def delete_content(self, id: str, /) -> None:
        """
        Receives an id and deletes both id and the
        id related content from the database.
        """
        self.endpoints.remove(id)

        self.cursor.execute(
            "DELETE FROM pastes WHERE id == (?)", (id,)
        )
        self.connection.commit()

    @staticmethod
    def create_url() -> str:
        """
        Create and returns a string that is 
        used for the application urls/ids. 
        """
        return secrets.token_urlsafe(16)

    def __load_endpoints(self) -> None:
        """Tries to load the table 'pastes'. If it doesn't exist, create it."""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS pastes (id, content)")
        self.cursor.execute("SELECT id FROM pastes")

        self.endpoints = {e[0] for e in self.cursor.fetchall()}
        logger.info(f"{len(self.endpoints)} entries on the database!")
    
    def __contains__(self, item) -> bool:
        return item in self.endpoints
    
    def __getitem__(self, id) -> Optional[str]:
        return self.read_content(id) 
