import db

db.execute_raw("""
    DROP TABLE IF EXISTS received_messages;
    DROP TABLE IF EXISTS messages_to_send;

    CREATE TABLE received_messages(
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_from      TEXT,
        msg_body        TEXT,
        created_at      TIMESTAMP,
        processed_at    TIMESTAMP
    );

    CREATE TABLE messages_to_send(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_to    TEXT,
        msg_body    TEXT,
        created_at  TIMESTAMP,
        sent_at     TIMESTAMP
    );
""")