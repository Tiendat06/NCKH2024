from flask import session, request
from flask_socketio import join_room, emit
from app.middlewares.ChatMiddleWare import ChatMiddleware
import redis

admin_sid = None
redis_store = redis.StrictRedis(host='host.docker.internal', port=6379, decode_responses=True)
def chat_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        global admin_sid
        user_type = request.args.get('user_type')
        # if 'user_sid' not in session:
        #     session['user_sid'] = {}
        if user_type == 'admin':
            admin_sid = request.sid
            # print('hi world admin')
            join_room('admin_room')
            print(f"Admin connected with SID: {admin_sid}")
        else:
            # PID = request.args.get('PID')
            # user_sid = request.sid
            # user_list = session.get('user_sid')
            # new_list = user_list
            # new_list[PID] = user_sid
            # session['user_sid'] = new_list
            # redis_store.set('user_sid', {})
            # print(session['user_sid'])
            print(f"User connected with SID: {request.sid}")

    @socketio.on('message to admin')
    def message_to_admin(data):
        # print(session.get('user_sid'))
        result = ChatMiddleware().message_to_admin(data)
        # print(result)
        if result['status']:
            emit('private message from client', {'message': data['message'], 'data': result['patients_data'], 'from': request.sid}, to='admin_room')
        else:
            emit('error', {'message': result['msg']}, room=request.sid)

    @socketio.on('message to client')
    def message_to_client(data):
        patient_id = data['patient_id']
        user_id = data['user_id']
        patient_request_id = data['patient_request_id']
        chat_content = data['chat_content']

        datas = {
            'patient_id': patient_id,
            'user_id': user_id,
            'chat_content': chat_content,
            'patient_request_id': (patient_request_id),
        }
        result = ChatMiddleware().message_to_client(datas)
        chat_data = result['data'][0]
        chat_data_PID = chat_data['patient_id']['PID']

        if patient_request_id == '-1':
            redis_patient_request = redis_store.get(chat_data_PID)
            if redis_patient_request:
                datas['patient_request_id'] = redis_patient_request
                patient_request_id = redis_patient_request

        if result['status']:
            emit('load current admin chat', {'message': result['msg'], 'data': result['data'][0], 'raw_data': datas, 'from': request.sid}, to='admin_room')
            emit('message from admin', {'message': chat_content, 'data': result['data'][0]}, to=patient_request_id)
        else:
            emit('error', {'message': result['msg']}, room=request.sid)

    @socketio.on('click patient chat')
    def click_patient_chat(data):
        patient_id = data['patient_id']
        patient_request_id = data['patient_request_id']
        datas = {
            'patient_id': patient_id,
            'patient_request_id': patient_request_id
        }
        result = ChatMiddleware().click_patient_chat(datas)
        if result['status']:
            emit('load patient chat',
                 {'patient_chats': result['patient_chats'], 'patient_request_id': patient_request_id},
                 to=request.sid)
        else:
            emit('error', {'message': result['msg']}, to=request.sid)

    @socketio.on('user_login')
    def handle_user_login(data):
        PID = data['PID']
        user_id = request.sid
        redis_store.set(PID, user_id)
        result = ChatMiddleware().handle_user_login(PID)
        if result['status']:
            emit('load current client chat', {'data': result['patient_chats']}, to=request.sid)
        else:
            emit('error', {'message': result['msg']}, room=request.sid)


    @socketio.on('client message')
    def handle_client_message(data):
        client_id = request.sid
        # print(f'client_id:{client_id}, {data}')

    @socketio.on_error()
    def handle_error(error):
        print(error)

    @socketio.on('disconnect')
    def handle_disconnect():
        for key in redis_store.keys():
            if redis_store.get(key) == request.sid:
                redis_store.delete(key)
                break
        # redis_store.delete(request.sid)
        print('Client disconnected')