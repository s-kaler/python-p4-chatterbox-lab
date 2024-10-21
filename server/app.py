from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_asc = [message.to_dict() for message in messages]
        return make_response(messages_asc, 200)
    
    elif request.method == 'POST':
        form_data = request.get_json()
        new_message = Message(
            body=form_data['body'],
            username=form_data['username']
        )

        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)
    

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == 'GET':
        message_serialized = message.to_dict()
        response = make_response(message_serialized, 200)
        
        return response
    

    elif request.method == 'PATCH':
        form_data = request.get_json()
        message.body=form_data['body']

        db.session.add(message)
        db.session.commit()
        response = make_response(message.to_dict(), 200)
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Baked Good deleted."
        }
        response = make_response(response_body, 200)
        return response


if __name__ == '__main__':
    app.run(port=5555)
