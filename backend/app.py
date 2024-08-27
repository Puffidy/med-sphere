from flask import *
from pony.orm import *
from datetime import datetime, date

app = Flask(__name__)
db = Database()

class Patient(db.Entity):
    first_name = Required(str)
    last_name = Required(str)
    date_of_birth = Required(datetime)
    reason_for_admission = Required(str)
    decursus = Set('Decursus')
    time_of_admission = Required(datetime)
    time_of_release = Optional(datetime)
    department = Required(str)
    room = Required(int)

class Decursus(db.Entity):
    text = Required(str)
    created_at = Required(datetime)
    patient = Required(Patient)

db.bind(provider='sqlite', filename='hospital_data.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

@app.route("/")
def index():
    return "Hello!"

# =========================== #
# CRUD OPERATIONS FOR PATIENT #
# =========================== #

@app.route("/patients", methods=['POST'])
@db_session
def create_patient():
    data = request.get_json()
    new_patient = Patient(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        date_of_birth=datetime.strptime(data.get('date_of_birth'), "%d.%m.%Y"),
        reason_for_admission=data.get('reason_for_admission'),
        time_of_admission=datetime.now(),
        department=data.get('department'),
        room=data.get('room')
    )
    return new_patient.to_dict(), 201

@app.route("/patients", methods=['GET'])
@db_session
def get_patients():
    patients = select(p for p in Patient)[:]
    return jsonify([p.to_dict() for p in patients])

@app.route("/patients/<int:id>", methods=['GET'])
@db_session
def get_patient(id):
    patient = Patient.get(id=id)
    if patient:
        return patient.to_dict()
    else:
        return jsonify({"error": "Patient not found"}), 404
    
@app.route("/patients/<int:id>", methods=['PUT'])
@db_session
def update_patient(id):
    data = request.get_json()
    patient = Patient.get(id=id)
    
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    patient.first_name = data.get('first_name', patient.first_name)
    patient.last_name = data.get('last_name', patient.last_name)
    patient.date_of_birth = datetime.strptime(data.get('date_of_birth'), "%d.%m.%Y") if data.get('date_of_birth') else patient.date_of_birth
    patient.reason_for_admission = data.get('reason_for_admission', patient.reason_for_admission)
    patient.time_of_release = datetime.now() if data.get('time_of_release') else patient.time_of_release
    patient.department = data.get('department', patient.department)
    patient.room = data.get('room', patient.room)
    
    return patient.to_dict()

@app.route("/patients/<int:id>", methods=['DELETE'])
@db_session
def delete_patient(id):
    patient = Patient.get(id=id)
    
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    patient.delete()
    return jsonify({"message": "Patient deleted successfully"}), 200

# ===================== #
# ADDITIONAL OPERATIONS #
# ===================== #
@app.route("/patients/<int:id>/decursus", methods=['GET'])
@db_session
def get_decursus(id):
    decursus = Patient.get(id=id).decursus
    return jsonify([d.to_dict() for d in decursus])

@app.route("/patients/<int:id>/decursus", methods=['POST'])
@db_session
def add_decursus(id):
    patient = Patient.get(id=id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    data = request.get_json()
    new_decursus = Decursus(
        text=data.get('text'),
        created_at=datetime.now(),
        patient=patient
    )
    return new_decursus.to_dict(), 201

@app.route("/patients/without-decursus", methods=['GET'])
@db_session
def get_without_decursus():
    today = date.today()
    patients = select(p for p in Patient if not p.decursus.exists(lambda d: d.created_at.date() == today))

    return jsonify([p.to_dict() for p in patients])

@app.route("/patients/lowest-free", methods=['POST'])
@db_session
def create_patient_in_lowest_free_room():
    occupied_rooms = select(p.room for p in Patient)
    lowest_free_room = min(set(range(1, max(occupied_rooms) + 2)) - set(occupied_rooms))
    data = request.get_json()
    
    new_patient = Patient(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        date_of_birth=datetime.strptime(data.get('date_of_birth'), "%d.%m.%Y"),
        reason_for_admission=data.get('reason_for_admission'),
        time_of_admission=datetime.now(),
        department=data.get('department'),
        room=lowest_free_room
    )
    return new_patient.to_dict(), 201

@app.route("/patients/<int:id>/release", methods=['PUT'])
@db_session
def release_patient(id):
    patient = Patient.get(id=id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    patient.time_of_release = datetime.now()
    return patient.to_dict()

@app.route("/patients/<int:id>/move/<int:new_room>", methods=['PUT'])
@db_session
def move_patient(id, new_room):
    patient = Patient.get(id=id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    patient.room = new_room
    return patient.to_dict()