import raft_pb2_grpc
import raft_pb2
import sqlite3
import os
import hashlib
import grpc

def replicate_action(action, db_path):
    """
    Replicate the action to the database
    """
    if action.action == raft_pb2.REGISTER:
        sqlcon = sqlite3.connect(db_path)
        sqlcur = sqlcon.cursor()

        # check to make sure username is not already in use
        sqlcur.execute(
            "SELECT * FROM users WHERE username=?", (action.username,)
        )
        if sqlcur.fetchone():
            pass
        else:
            # add new user to database
            action.passhash = hashlib.sha256(
                action.passhash.encode()
            ).hexdigest()
            sqlcur.execute(
                "INSERT INTO users (username, passhash) VALUES (?, ?)",
                (action.username, action.passhash),
            )
            sqlcon.commit()
        sqlcon.close()
    elif action.action == raft_pb2.SEND_MESSAGE:
        sender = action.sender
        recipient = action.recipient
        message = action.message
        sqlcon = sqlite3.connect(db_path)
        sqlcur = sqlcon.cursor()

        try:
            sqlcur.execute(
                "INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)",
                (sender, recipient, message),
            )
            sqlcon.commit()

        except Exception as e:
            message_id = None

        sqlcon.close()
    elif action.action == raft_pb2.PING:
        action = action.action
        sender = action.sender
        sent_message = action.sent_message
        message_id = action.message_id

        sqlcon = sqlite3.connect(db_path)
        sqlcur = sqlcon.cursor()

        sqlcur.execute(
            "UPDATE messages SET delivered=1 WHERE message_id=?",
            (message_id,),
        )
        sqlcon.commit()

        sqlcon.close()

    elif action.action == raft_pb2.VIEW_UNDELIVERED:
        sqlcon = sqlite3.connect(db_path)
        sqlcur = sqlcon.cursor()
        
        username = action.username
        
        sqlcur.execute(
            "UPDATE messages SET delivered=1 WHERE recipient=?",
            (username,),
        )

        sqlcon.commit()
        sqlcon.close()
    elif action.action == raft_pb2.DELETE_MESSAGE:
        sqlcon = sqlite3.connect(db_path)
        sqlcur = sqlcon.cursor()

        message_id = action.message_id
        sqlcur.execute(
            "DELETE FROM messages WHERE message_id=?", (message_id,)
        )
        sqlcon.commit()

        sqlcon.close()
    elif action.action == raft_pb2.DELETE_ACCOUNT:
        sqlcon = sqlite3.connect(db_path)
        sqlcur = sqlcon.cursor()

        username = action.username
        passhash = action.passhash

        passhash = hashlib.sha256(passhash.encode()).hexdigest()
        sqlcur.execute(
            "SELECT passhash FROM users WHERE username=?", (username,)
        )

        result = sqlcur.fetchone()
        if result:
            # username exists and passhash matches
            if result[0] == passhash:
                sqlcur.execute(
                    "DELETE FROM users WHERE username=?", (username,)
                )
                sqlcur.execute(
                    "DELETE FROM messages WHERE sender=? OR recipient=?",
                    (username, username),
                )
                sqlcon.commit()

        sqlcon.close()