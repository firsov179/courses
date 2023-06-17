import json

from flask import Flask, Response
from flask_restful import Api, Resource, reqparse
from DatabaseConnector import select_from_db, insert_to_db

# initialization of app and RESTful api
app = Flask(__name__)
api = Api()

# add handlers

@app.route('/courses/<int:courseId>', methods=['GET'])
def get_course(courseId: int):
    # request to database - find course with courseId 
    query = f'''SELECT * FROM courses WHERE Id={courseId}'''
    info = select_from_db(query)    
    if len(info) != 1 or len(info[0]) != 4:
        return Response('Unxpected courseId.', status=409) # bad id
    # convert info to json format
    res = {
        'courseId': info[0][0],
        'description': info[0][1],
        'program': info[0][2],
        'studentReviews': info[0][3],
    }
    return Response(json.dumps(res), 200)

@app.route('/courses', methods=['GET'])
def get_all_courses():
    # request to database - get info about all courses
    query = f'''SELECT * FROM courses'''
    info = select_from_db(query)
    res = []
    for elem in info:
        res.append({
            'courseId': info[0][0],
            'description': info[0][1],
            'program': info[0][2],
            'studentReviews': info[0][3],
        })     
    
    return Response(json.dumps(res), 200)


@app.route('/enrollments', methods=['POST'])
def post_enrollment():
    if not request.json or 'courseId' not in request.json or 'studentId' not in request.json:
        return Response("There is no 'courseId' or 'studentId' in request.json", 400)
    
    # request to database - add new line
    query = f'''INSERT INTO enrollments(courseId, studentId)
                VALUES (
                {request.json['courseId']},
                {request.json['studentId']});'''
    
    info = insert_to_db(query)
    return Response("Added", 200)

@app.route('/enrollments/<int:studentId>', methods=['GET'])
def get_student_enrollment(studentId: int):  
    
    # request to database - get student enrollments
    query = f'''SELECT * FROM enrollments WHERE studentId={studentId}'''
    info = select_from_db(query)
    if len(info) == 0:
        return Response('Unxpected studentId.', status=409) # bad id
    res = []
    for elem in info:
        res.append(elem[2]) # add courseId
    return Response(json.dumps(res), 200)
    
@app.route('/enrollments/<int:enrollmentId>', methods=['DELETE'])
def delete_enrollment(studentId: int):  
    query = f'''SELECT * FROM enrollments WHERE enrollmentId={enrollmentId}'''
    info = select_from_db(query)   # check enrollmentId
    if len(info) == 0:
        return Response('Unxpected enrollmentId.', status=409) # bad id    
     
    query = f'''DELETE FROM enrollments WHERE enrollmentId={enrollmentId};'''
    insert_to_db(query)    # deleting
    return Response("Deleted", 200)
    
    
api.init_app(app)

# run server on localhost
app.run(debug=True, port=3000, host="localhost")
