from odoo import http
from odoo.http import request
from odoo.tools import json


class MailChatController(http.Controller):
    @http.route('/mail_inbox/', type='json', auth='none', methods=['GET'], csrf=False)
    def get_mail_inbox(self):
        messages = request.env['mail.mail'].sudo().search([])

        messages_list = [{
            'id': msg.id,
            'body': msg.body_html,
            'email_to': msg.email_to,
            'email_cc': msg.email_cc,
            'recipient_ids': msg.recipient_ids.name,
        } for msg in messages]

        return {'status': 'success', 'messages': messages_list}

    @http.route('/get_messages/', type='json', auth='none', methods=['GET'], csrf=False)
    def get_mail_inbox(self):
        messages = request.env['mail.message'].sudo().search(['|', ('author_id', '=', 261),('author_id', '=', 3)], limit=10)

        participants = {}

        for msg in messages:
            if msg.author_id.id not in participants:
                participants[msg.author_id.id] = {
                    'id': msg.author_id.id,
                    'author': msg.author_id.name,
                    'participants': {
                        'record_name': msg.record_name,
                        'messages': []
                    }
                }
            participants[msg.author_id.id]['participants']['messages'].append({
                'id': msg.id,
                'author_id': msg.author_id.id,
                'author': msg.author_id.name,
                'email_from': msg.email_from,
                'subject': msg.subject,
                'body': msg.body,
                'date': msg.date,
                'record_name': msg.record_name
            })


        participants_list = list(participants.values())

        return {'status': 'success', 'participants': participants_list}
