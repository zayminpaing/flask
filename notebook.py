from flask import Flask, request, render_template
import sqlite3

DATABASE_NAME = "notebook.db"
TABLE_ACCOUNT = "account"
COLUMN_USERNAME = "username"
COLUMN_PASSWORD = "password"

TABLE_NOTES = "notes"
COLUMN_NOTE = "note"

app = Flask(__name__)

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    new_acc = request.form
    if create_acc(new_acc):
        return render_template("login.html")
    else:
        return render_template("signup.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    acc = request.form
    username = acc["username"]
    password = acc["password"]
    if validate_acc(username , password):
        note = get_note(username)
        return render_template("main.html", user = username, n = note)
    else:
        return render_template("fail_login.html")


@app.route("/index")
def vlogin():
    conn = open_database()
    create_tables(conn)
    return render_template("login.html")


@app.route("/exit", methods=['GET', 'POST'])
def exit():
    values = request.form
    if update_notes(values["txt"], values["user"]):
        return render_template("login.html")
    else:
        return render_template("main.html", user = values["user"])
    # return render_template("view.html", v = values)


@app.route("/v_signup")
def vsignup():
    return render_template("vsignup.html")


def drop_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("DROP TABLE {}".format(TABLE_ACCOUNT))
    conn.execute("DROP TABLE {}".format(TABLE_NOTES))
    conn.close()


def open_database():
    conn = sqlite3.connect(DATABASE_NAME)
    print("Opened database successfully")
    return conn


def get_note(username):
    conn = open_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM {} WHERE {} = '{}'".format(TABLE_NOTES, COLUMN_USERNAME, username))
    notes = dict(cur.fetchall())
    if len(notes) != 0:
        return notes[username]
    else:
        return ""



def update_notes(note, username):
    status = False
    try:
        sqliteConnection = sqlite3.connect(DATABASE_NAME)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # sql_update_query = """UPDATE notes SET note = 'note' WHERE username = 'zayminpaing'"""
        sql_update_query = "UPDATE {} SET {} = '{}' WHERE {} = '{}'".format(TABLE_NOTES, COLUMN_NOTE, note, COLUMN_USERNAME, username)
        cursor.execute(sql_update_query)
        sqliteConnection.commit()
        print("Record Updated successfully ")
        status = True
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return status


def validate_acc(username, pwd):
    conn = open_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM {} WHERE {} = '{}'".format(TABLE_ACCOUNT, COLUMN_USERNAME, username))
    # cur.execute("SELECT * FROM account WHERE username = '{}'".format(username))
    accs = dict(cur.fetchall())
    conn.close()
    if len(accs) == 0:
        return False
    else:
        if accs[username] == pwd:
            return True
    return False


def create_tables(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS {} ({} TEXT, {} TEXT, PRIMARY KEY({}))".format(TABLE_ACCOUNT, COLUMN_USERNAME, COLUMN_PASSWORD, COLUMN_USERNAME))
    print("{} is created successfully.".format(TABLE_ACCOUNT))
    conn.execute("CREATE TABLE IF NOT EXISTS {} ({} TEXT, {} TEXT, PRIMARY KEY({}))".format(TABLE_NOTES, COLUMN_USERNAME, COLUMN_NOTE, COLUMN_USERNAME))
    print("{} is creared successfully.".format(TABLE_NOTES))
    conn.close()


def create_acc(new_acc):
    username = ""
    password = ""
    status = False
    username = new_acc["username"]
    password = new_acc["password"]
    try:
        with sqlite3.connect(DATABASE_NAME) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO {} ({},{}) VALUES (?,?)".format(TABLE_ACCOUNT, COLUMN_USERNAME, COLUMN_PASSWORD),(username, password) )
            cur.execute("INSERT INTO {} ({},{}) VALUES (?,?)".format(TABLE_NOTES, COLUMN_USERNAME, COLUMN_NOTE),(username, ""))
            con.commit()
            status = True
    except:
        con.rollback()
    finally:
        con.close()
        return status



if __name__ == "__main__":
    # login()
    app.run(debug=True)
    # drop_tables()
    # update_test()