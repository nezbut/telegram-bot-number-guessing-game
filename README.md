## Hello everyone, this is my first telegram bot using aiogram
___
#### To make everything work, you need to do 5 things
1. Create and get a telegram bot token from @BotFather.
2. Create a ".env" file in the project and enter your telegram bot token obtained from @BotFather as indicated in ".env.example".
3. Create a "db.db" file in the "database" folder. You will thus create a sqlite database.
4. In this database, create 2 tables with the queries specified below (These queries can be executed in any sqlite database management program, these are the ones I know: https://sqlitebrowser.org/ and https://sqlitestudio.pl/).
5. Run the main.py file
#### Everything is ready!

### First query:
```
CREATE TABLE users (
    username TEXT    NOT NULL
                     UNIQUE,
    chat_id  INTEGER UNIQUE
                     NOT NULL,
    in_game  BOOL    NOT NULL
                     DEFAULT (0),
    attempt  INTEGER NOT NULL
                     DEFAULT (0),
    num      INTEGER NOT NULL
                     DEFAULT (0) 
);
```

### Second query:

```
CREATE TABLE users_stat (
    user        TEXT    REFERENCES users (username) ON DELETE CASCADE
                        NOT NULL,
    count_games INTEGER NOT NULL,
    wins        INTEGER NOT NULL
);
```
