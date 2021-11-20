from flask import Flask, jsonify, request
import lib_controller
from db import create_tables

app = Flask(__name__)


@app.route('/library', methods=["POST"])
def insert_library():
    """
    This method is used to insert a record in the library table
    :return: json object
    """
    lib_details = request.get_json(force=True)
    print(lib_details)
    name = lib_details["name"]
    city = lib_details["city"]
    state = lib_details["state"]
    postal_code = lib_details["postal_code"]
    result = lib_controller.add_library(name, city, state, postal_code)
    return "success"


@app.route('/book', methods=["POST"])
def insert_book():
    """
    This method is used to insert a record in the books table
    :return: json object
    """
    book_details = request.get_json(force=True)
    title = book_details["title"]
    author_name = book_details["author_name"]
    isbn_num = book_details["isbn_num"]
    genre = book_details["genre"]
    description = book_details["description"]
    lib_controller.add_book(title, author_name, isbn_num, genre, description)
    return "success"


@app.route('/user', methods=["POST"])
def insert_user():
    """
    This method is used to insert a record in the user table
    :return: json object
    """
    user_details = request.get_json(force=True)
    name = user_details["name"]
    lib_controller.add_user(name)
    return "success"


@app.route('/checked_out', methods=["POST"])
def book_checked_out():
    """
    This method is used to insert a record in the library_activities table and
    insert / update a record in the library_book table based on the criteria
    :return: json object
    """
    details = request.get_json(force=True)
    library_id = details["library_id"]
    book_id = details["book_id"]
    user_id = details["user_id"]
    activity_type = "checked out"
    library_book_id = lib_controller.get_library_book_id(library_id, book_id, user_id)
    if not library_book_id:
        library_book_id = lib_controller.add_library_books(library_id, book_id)
    library_activity_id = lib_controller.add_library_activities(activity_type, user_id, library_book_id)
    lib_controller.update_library_books(library_activity_id, library_book_id)
    return "success"


@app.route('/checked_in', methods=["PUT"])
def book_checked_in():
    """
    This method is used to modify a record in the library_activities table
    :return: json object
    """
    details = request.get_json(force=True)
    library_id = details["library_id"]
    book_id = details["book_id"]
    user_id = details["user_id"]
    activity_type = "checked in"
    library_book_id = lib_controller.get_library_book_id(library_id, book_id, user_id)
    library_activity_id = lib_controller.get_library_book_library_activity_id(library_book_id)
    lib_controller.update_library_activities(library_activity_id, activity_type)
    return "success"


@app.route('/checkout_book_list_by_user', methods=["POST"])
def checkout_book_list_by_user():
    """
    This method is used to fetch the checked out book records by the user
    :return: json object
    """
    details = request.get_json(force=True)
    user_id = details["user_id"]
    result = lib_controller.get_checkout_book_list_of_user(user_id)
    return jsonify(result)


@app.route('/checkout_book_list_on_library', methods=["POST"])
def checkout_book_list_on_library():
    """
    This method is used to fetch the checked out book records on a library
    :return:
    """
    details = request.get_json(force=True)
    library_id = details["library_id"]
    result = lib_controller.get_checkout_book_list_by_library(library_id)
    return jsonify(result)


"""
Enable CORS. Disable it if you don't need CORS
"""
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, " \
                                                       "X-CSRF-Token, Authorization"
    return response


if __name__ == "__main__":
    create_tables()
    app.run(host='0.0.0.0', port=5000, debug=True)
