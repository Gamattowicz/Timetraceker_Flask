import sqlite3

connection = sqlite3.connect('time_tracker.db')

cur = connection.cursor()

cur.execute('''CREATE TABLE projects (
            id integer primary key autoincrement,
            name text not null UNIQUE,
            shortcut text not null UNIQUE
            )''')
cur.execute('''create table hours (
            id integer primary key autoincrement,
            amount integer not null,
            work_date DATE NOT NULL DEFAULT CURRENT_DATE,
            project_shortcut text not null,
            FOREIGN KEY (project_shortcut) REFERENCES Projects(shortcut))''')


connection.commit()
connection.close()