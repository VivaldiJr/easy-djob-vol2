from odoo import models, Command


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    @staticmethod
    def getOrCreateUser(request, email, name, password):
        TABLE_USER = request.env['res.users']
        TABLE_GROUPS = request.env['res.groups']
        TABLE_COMPANY = request.env['res.company']
        public_group = TABLE_GROUPS.sudo().search([("name", "=", "Public")], limit=1)
        exist = TABLE_USER.sudo().search([("email", "=", email)], limit=1)
        firstCompany = TABLE_COMPANY.sudo().search([], order='id', limit=1)
        jsonMapUser = {
            'login': email,
            'email': email,
            'name': name,
            "password": password,
            "new_password": password,
            'groups_id': [Command.link(public_group.id)] if public_group else [Command.link(group_id) for group_id in [0, 4]],
            'company_ids': [Command.link(firstCompany.id)],
            'company_id': firstCompany.id
        }
        context = request.env.context.copy()
        context['company_id'] = firstCompany.id
        if exist:
            exist.with_context(context).sudo().update(jsonMapUser)
            return exist
        return TABLE_USER.with_context(context).sudo().create(jsonMapUser)

    @property
    def candidate_id(self):
        return self.env['hr.candidate'].sudo().search([("email", "=", self.login)], limit=1)