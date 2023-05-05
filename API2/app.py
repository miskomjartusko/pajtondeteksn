from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from marshmallow import Schema, fields
import random
import datetime


app = Flask(__name__)
scheduler = APScheduler()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://data_xesl_user:ihaN2ocXoqa5frgpSSPitqaPENLVW8eu@dpg-ch9qpb2k728hts45jpjg-a.frankfurt-postgres.render.com/data_xesl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    photo_url = db.Column(db.String, nullable=False)
    fing_seq = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserSchema(Schema):
    id = fields.Integer()      
    name = fields.String()
    photo_url = fields.String()
    fing_seq = fields.String()




class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class LogSchema(Schema):
    id = fields.Integer()      
    person = fields.String()
    added_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S+02:00')


@app.route('/')
def hello():
    return "ssssss"

@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.get_all()

    serializer = UserSchema(many=True)

    data = serializer.dump(users)

    return jsonify(
        data
    )

@app.route('/api/users', methods=['POST'])
def create_a_user():
    s = ''
    for i in range(5):
        s += str(random.randint(1, 5))
    data = request.get_json()
    new_user = User(
        name=data.get('name'),
        photo_url=data.get('photo_url'),
        fing_seq=s
    )

    new_user.save()

    serializer = UserSchema()

    data = serializer.dump(new_user)

    return jsonify(
        data
    ), 201

@app.route('/api/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.get_by_id(id)

    serializer = UserSchema()

    data = serializer.dump(user)

    return jsonify(
        data
    ), 200

@app.route('/api/user/<int:id>', methods=['PUT'])
def update_user(id):
    user_to_update = User.get_by_id(id)

    data = request.get_json()

    user_to_update.name = data.get('name')
    user_to_update.photo_url = data.get('photo_url')

    db.session.commit()

    serializer = UserSchema()

    user_data = serializer.dump(user_to_update)

    return jsonify(
        user_data
    ), 200



@app.route('/api/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user_to_delete = User.get_by_id(id)

    user_to_delete.delete()

    return jsonify({"message": "Deleted"}), 204


@app.route('/api/logs', methods=['GET'])
def get_logs():
    logs = Log.get_all()

    serializer = LogSchema(many=True)

    data = serializer.dump(logs)

    return jsonify(
        data
    )

@app.route('/api/logs', methods=['POST'])
def add_log():
    data = request.get_json()
    new_log = Log(
        person=data.get('person')
    )

    new_log.save()

    serializer = LogSchema()

    data = serializer.dump(new_log)

    return jsonify(
        data
    ), 201



def updatovac():
    with app.app_context():
        users = User.get_all()
        for user in users:
            seq = ''
            for i in range(5):
                seq += str(random.randint(1, 5))

            user.fing_seq = seq

        db.session.commit()
    
scheduler.add_job(id = 'Scheduled Task', func=updatovac, trigger="interval", seconds=600)
scheduler.start()