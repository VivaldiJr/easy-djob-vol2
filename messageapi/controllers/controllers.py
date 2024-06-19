# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.tools import json


class Messageapi(http.Controller):
    @http.route('/message_send/', type='json', auth='none', methods=['POST'], csrf=False)
    def send_message(self, **kwargs):
        body = kwargs.get('body')
        sender_id = kwargs.get('sender_id')
        recipient_id = kwargs.get('recipient_id')

        print(kwargs)

        message = request.env['custom.message'].create({
            'body': body,
            'sender_id': sender_id,
            'recipient_id': recipient_id,
        })

        return {'status': 'success', 'message': 'Message sent successfully', 'message_id': message.id}

    @http.route('/message_inbox/', type='json', auth='none', methods=['GET'], csrf=False)
    def get_inbox(self):

        messages = request.env['custom.message'].sudo().search([])

        conversations = {}

        for msg in messages:

            participants = {msg.sender_id.id, msg.recipient_id.id}

            conversation_id = '_'.join(sorted(map(str, participants)))

            if conversation_id not in conversations:
                conversations[conversation_id] = {
                    'id': conversation_id,
                    'participants': list(participants),
                    'messages': []
                }

            conversations[conversation_id]['messages'].append({
                'id': msg.id,
                'sender': msg.sender_id.id,
                'timestamp': msg.date_sent,
                'sender_name': msg.sender_id.name,
                'content': msg.body,
            })

        result = {'conversations': list(conversations.values())}

        return {'status': 'success', 'data': result}

    @http.route('/internal_users/', auth='public', csrf=False, cors='*', methods=['GET'])
    def get_users(self):
        try:
            records = request.env['res.users'].sudo().search([])

            users_data = []

            for record in records:
                users_data.append({
                    'id': record.id,
                    'login': record.login,
                    'name': record.name,
                })

            return json.dumps(users_data)

        except Exception as e:
            return json.dumps({'error': str(e)})
