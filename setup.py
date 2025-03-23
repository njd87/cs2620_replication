import os
import sqlite3

def reset_database(files) -> None:
    """
    Reset the database by deleting the file if it exists.
    """

    # check to make sure the "data" directory exists
    # database stored here
    os.makedirs("data/r1", exist_ok=True)
    os.makedirs("data/r2", exist_ok=True)
    os.makedirs("data/r3", exist_ok=True)
    os.makedirs("data/r4", exist_ok=True)
    os.makedirs("data/r5", exist_ok=True)

    # delete everything in the data directory, including subdirectories
    for file in files:
        if os.path.exists(file):
            os.remove(file)


def structure_tables(data_path="data/messenger.db") -> None:
    """
    Create the tables for the database.
    """

    with sqlite3.connect(data_path) as conn:
        cursor = conn.cursor()

        # set up users table in messenger.db file
        cursor.execute(
            """
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                passhash TEXT NOT NULL,
                online BOOLEAN DEFAULT 0
            );
        """
        )

        # set up messages table in messenger.db file
        cursor.execute(
            """
            CREATE TABLE messages (
                message_id INTEGER PRIMARY KEY,
                sender TEXT NOT NULL,
                recipient TEXT NOT NULL,
                message TEXT NOT NULL,
                delivered BOOLEAN DEFAULT 0,
                time DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        conn.commit()
        print(f"Created users table.")
        print(f"Created messages table.")


if __name__ == "__main__":
    reset_database([
        "data/r1/messenger.db",
        "data/r2/messenger.db",
        "data/r3/messenger.db",
        "data/r4/messenger.db",
        "data/r5/messenger.db"
    ])

    structure_tables("data/r1/messenger.db")
    structure_tables("data/r2/messenger.db")
    structure_tables("data/r3/messenger.db")
    structure_tables("data/r4/messenger.db")
    structure_tables("data/r5/messenger.db")