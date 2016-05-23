from flask import jsonify

def exception_not_implemented():
    message = { 'error' : { 'code' : 0, 'message' : "Error : not implemented"}}
    return jsonify(message)

def build_error_response(code, message):
    j_message = { 'error' : { 'code' : code, 'message' : message}}
    return jsonify(j_message)

def build_error_object(code, message):
    error_object = { 'code' : code, 'message' : message }
    return error_object