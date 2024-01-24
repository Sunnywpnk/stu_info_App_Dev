from pymongo import MongoClient
from flask import Flask, jsonify, request
from flask_basicauth import BasicAuth

app = Flask(__name__)

# uri = "mongodb+srv://mongo:mongo@cluster0.2owdljr.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://for_work:sunny_wpnk140646@cluster0.wytpqnu.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client['students']      
collection = db['std_info']   

app.config['BASIC_AUTH_USERNAME']='username'
app.config['BASIC_AUTH_PASSWORD']='password'
basic_auth = BasicAuth(app)


try:
    client.admin.command('ping')
   
    db = client["students"]
    collection = db["std_info"]
    @app.route("/")
    def Greet():
        return "<p> Welcome to Student Management API </p>"

@app.route('/')
def welcome():
    return "Welcome to Student Management API"

#โชว์ข้อมูลลของทุกคน
@app.route('/students', methods=['GET'])
@basic_auth.required
def get_all_students():
    return jsonify(formatted_students)

#โชว์แค่ข้อมูลของนักเรียนที่ต้องการดู
@app.route('/students/<int:std_id>', methods=['GET'])
@basic_auth.required
def get_student(std_id):
    student = next((s for s in formatted_students if s['id'] == std_id), None)
    if student:
        return jsonify(student)
    
    else:
        return jsonify({"error": "Student not found"}),404
    

#เพิ่มข้อมูลของนักเรียน
@app.route('/students', methods=['POST'])
@basic_auth.required
def create_student():
    new_student_data = request.json

    
    existing_student = collection.find_one({"id": new_student_data["id"]})
    if existing_student:
        return jsonify({"error":"Cannot create new student"}),500

    
    collection.insert_one(new_student_data)

    return jsonify(new_student_data),200

#PUT(update info)
@app.route('/students/<int:std_id>', methods=['PUT'])
@basic_auth.required
def update_student(std_id): 
    student = collection.find_one({"id": std_id})
    if student:
        new_student_data = request.json
        print(f"Received data for update: {new_student_data}")
        collection.update_one({"id": std_id}, {"$set": new_student_data})
        updated_student = collection.find_one({"id": std_id})
        print(f"Updated student data: {updated_student}")
        return jsonify(updated_student), 200
    
    else:
        return jsonify({"error": "Student not found"}), 404

#ลบนักเรียนออกโดยเช็คจาก id
    @app.route("/students/<std_id>" , methods = ["DELETE"])
    @basic_auth.required 
    def delete_student(std_id):
        try:
            collection.delete_one({"id": std_id})
            return jsonify({"message":"deleted successfully"}),200
        except Exception as e:
            print(e)
            return jsonify({"error":"Student not found"}),404
   

if __name__ == '__main__':
        app.run(host="0.0.0.0", port=5000, debug=True)
    
    
