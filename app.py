from flask import Flask, escape, request,abort,make_response
app = Flask(__name__)
DB = {
    "students" : [],
    "classes" : []
}
student_id = 1234456
class_id = 1122334

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.errorhandler(404)
def not_found(error):
    return make_response({"error": "Not found"}, 404)

#Create a new student
@app.route('/students',methods = ['POST'])
def creat_student():
    req = request.json
    global student_id
    DB["students"].append({"id": student_id,"name":req["name"]})
    student_id = student_id + 1
    return DB["students"][-1],201


#Retrieve an existing student
@app.route('/students/<int:s_id>',methods = ['GET'])
def retrieve_student(s_id):
    for i in range(len(DB["students"])):
        temp = DB["students"][i]
        if temp["id"] == s_id:
            return temp,200
    abort(404)
    


#Create a class
@app.route('/classes',methods = ['POST'])
def create_class():
    req = request.json
    global class_id
    DB["classes"].append({"id": class_id,"name":req["name"],"students":[]})
    class_id = class_id + 1
    return DB["classes"][-1],201

#Retrieve a class
@app.route('/classes/<int:c_id>',methods = ['GET'])
def retrieve_class(c_id):
    for i in range(len(DB["classes"])):
        temp = DB["classes"][i]
        if temp["id"] == c_id:
            return temp,200
    abort(404)

#Add students to a class
@app.route('/classes/<int:c_id>',methods = ['PATCH'])
def add_student(c_id):
    req = request.json
    s_id = request.json["student_id"]
    flag = False
    for i in range(len(DB["students"])):
        temp = DB["students"][i]
        if temp["id"] == s_id:
            student = temp
            flag = True
    if flag == False:
        abort(404)

    for i in range(len(DB["classes"])):
        temp = DB["classes"][i]
        if temp["id"] == c_id:
            temp["students"].append(student)
            return temp
    abort(404)

