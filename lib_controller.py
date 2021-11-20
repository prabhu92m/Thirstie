from db import get_db


def add_library(name, city, state, postal_code):
    db = get_db()
    cursor = db.cursor()
    statement = 'INSERT INTO libraries(name, city, state, postal_code) VALUES (?, ?, ?, ?)'
    cursor.execute(statement, [name, city, state, postal_code])
    row_id = cursor.lastrowid
    db.commit()
    return row_id


def add_book(title, author_name, isbn_num, genre, description):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO books(title, author_name, isbn_num, genre, description) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(statement, [title, author_name, isbn_num, genre, description])
    row_id = cursor.lastrowid
    db.commit()
    return row_id


def add_library_books(library_id, book_id):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO library_books(library_id, book_id) VALUES (?, ?)"
    cursor.execute(statement, [library_id, book_id])
    row_id = cursor.lastrowid
    db.commit()
    return row_id


def add_user(name):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO users(name) VALUES (?)"
    cursor.execute(statement, [name])
    row_id = cursor.lastrowid
    db.commit()
    return row_id


def add_library_activities(activity_type, user_id, library_book_id):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO library_activities(activity_type, library_book_id, user_id, checked_out_at) " \
                "VALUES (?, ?, ?, date('now'))"
    cursor.execute(statement, [activity_type, user_id, library_book_id])
    row_id = cursor.lastrowid
    db.commit()
    return row_id


def get_library_book_id(library_id, book_id, user_id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT lb.library_book_id FROM library_books lb  " \
                "left join library_activities la on la.user_id = ?" \
                "WHERE lb.library_id = ? and lb.book_id = ?"
    cursor.execute(statement, [user_id, library_id, book_id])
    return cursor.fetchone()


def get_library_book_library_activity_id(library_book_id):
    db = get_db()
    cursor = db.cursor()
    print(library_book_id)
    statement = "SELECT last_library_activity_id FROM library_books WHERE library_book_id = ?"
    cursor.execute(statement, library_book_id)
    return cursor.fetchone()


def update_library_activities(library_activity_id, activity_type):
    db = get_db()
    cursor = db.cursor()
    date_column = "checked_in_at"
    if activity_type == "checked out":
        date_column = "checked_out_at"
    statement = "UPDATE library_activities SET activity_type = ?, " + date_column + " = datetime('now') WHERE" \
                                                                                    " library_activity_id = ?"
    print(statement)
    cursor.execute(statement, [activity_type, library_activity_id[0]])
    db.commit()
    return True


def update_library_books(last_library_activity_id, library_book_id):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE library_books SET last_library_activity_id = ? WHERE library_book_id = ?"
    cursor.execute(statement, [last_library_activity_id, library_book_id])
    db.commit()
    return True


def get_checkout_book_list_of_user(user_id):
    db = get_db()
    cursor = db.cursor()
    query = """SELECT   B.title "Title", 
                        B.author_name "Author Name", 
                        B.isbn_num "ISBN Number", 
                        B.genre "Genre", 
                        B.description "Description" 
                FROM library_activities LA
                    INNER JOIN library_books LB ON LB.library_book_id = LA.library_book_id
                    INNER JOIN books B ON B.book_id = LB.book_id
                WHERE LA.user_id = ? AND LA.activity_type = "checked out"
                """
    column = cursor.execute(query, [user_id])
    return get_dict_val_from_cursor(column, cursor)


def get_checkout_book_list_by_library(library_id):
    db = get_db()
    cursor = db.cursor()
    query = """select   B.title "Title", 
                        B.author_name "Author Name", 
                        B.isbn_num "ISBN Number", 
                        B.genre "Genre", 
                        B.description "Description" 
                from library_activities LA
                    left join library_books LB on LB.library_book_id = LA.library_book_id
                    left join books B on B.book_id = LB.book_id
                where LB.library_id = ? and LA.activity_type = "checked out"
            """
    column = cursor.execute(query, [library_id])
    return get_dict_val_from_cursor(column, cursor)


def get_dict_val_from_cursor(column, cursor):
    column = [i[0] for i in column.description]
    data = cursor.fetchall()
    result = []
    for i in range(len(data)):
        result.append(dict(zip(column, data[i])))
    return result
