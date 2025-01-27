from flask import request, jsonify
from models import db, Message, User
from . import message_bp

# =====SEND A MESSAGE OR REPLY TO A MESSAGE======
@message_bp.route('/', methods=['POST'])
def send_or_reply_message():
    data = request.json

    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    reply_to_message_id = data.get('reply_to_message_id')

    # Validate required fields
    if not sender_id or not receiver_id or not content:
        return jsonify({'message': 'Sender ID, Receiver ID, and content are required'}), 400

    # Check if the receiver exists
    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({'message': 'Receiver not found'}), 404

    # If replying to an existing message
    if reply_to_message_id:
        original_message = Message.query.get(reply_to_message_id)
        if not original_message:
            return jsonify({'message': 'Original message not found'}), 404

        # Create a reply message
        reply_message = Message(content=content, sender_id=sender_id, receiver_id=receiver_id)
        db.session.add(reply_message)
        db.session.commit()

        return jsonify({'message': 'Reply sent successfully'}), 201

    # If sending a new message
    message = Message(content=content, sender_id=sender_id, receiver_id=receiver_id)
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully'}), 201


# =====GET MESSAGES FOR A USER======
@message_bp.route('/<int:user_id>', methods=['GET'])
def get_messages(user_id):
   
    received = Message.query.filter_by(receiver_id=user_id).all()
    sent = Message.query.filter_by(sender_id=user_id).all()

    # Helper function to format messages
    def message_to_dict(message):
        return {
            'message_id': message.message_id,
            'content': message.content,
            'sent_at': message.sent_at,
            'sender': {'user_id': message.sender_id, 'email': message.sender.email},
            'receiver': {'user_id': message.receiver_id, 'email': message.receiver.email}
        }

    return jsonify({
        'received': [message_to_dict(msg) for msg in received],
        'sent': [message_to_dict(msg) for msg in sent]
    })

# =====UPDATE A MESSAGE======
@message_bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    data = request.json
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'message': 'Message not found'}), 404

    sender_id = data.get('sender_id')
    content = data.get('content')

    if message.sender_id != sender_id:
        return jsonify({'message': 'You can only update your own messages'}), 403

    if not content:
        return jsonify({'message': 'Message content cannot be empty'}), 400

    message.content = content
    db.session.commit()
    
    return jsonify({'message': 'Message updated successfully'}), 200

# =====DELETE A MESSAGE======
@message_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    data = request.json
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'message': 'Message not found'}), 404

    sender_id = data.get('sender_id')
    
    if message.sender_id != sender_id and message.receiver_id != sender_id:
        return jsonify({'message': 'You can only delete your own messages'}), 403

    db.session.delete(message)
    db.session.commit()
    
    return jsonify({'message': 'Message deleted successfully'}), 200
