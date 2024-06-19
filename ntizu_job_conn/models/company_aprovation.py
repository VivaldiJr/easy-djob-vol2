# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError

STATE_COMPANY_OPTIONS = [
    ('draft', 'Rascunho'),
    ('pending', 'Pendente de Aprovação'),
    ('approved', 'Aprovado'),
    ('rejected', 'Rejeitado')
]


class Company(models.Model):
    _name = 'ntizu.company.request'
    _description = 'Empresa'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    company_id = fields.Many2one('res.company', string='Real Company', required=False)

    name = fields.Char(string='Nome', required=True)
    website = fields.Char(string='Website', required=True)
    phone = fields.Char(string='Telefone', required=True)
    num_employees = fields.Integer(string='Número de Funcionários')
    has_hr_department = fields.Boolean(string='Possui Departamento de RH')
    representative_id = fields.One2many('representative.ntizu.company.request', 'company_id', string='Representatives',
                                        required=True)
    member_ids = fields.One2many('member.ntizu.company.request', 'company_id', string='Membros')

    states = fields.Selection(STATE_COMPANY_OPTIONS, string='Estado de Aprovação', default='draft')
    currency_id = fields.Many2one("res.currency", string="Currency")
    comment = fields.Html(string='Notes')

    @api.constrains('phone')
    def _check_valid_phone(self):
        for company in self:
            if company.phone and not re.match(r'^\+?\d+$', company.phone):
                raise ValidationError('Número de telefone inválido. Deve ser um número válido.')

    @api.constrains('website')
    def _check_valid_website(self):
        for company in self:
            if company.website and not re.match(r'^https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', company.website):
                raise ValidationError('URL de website inválida. Deve ser uma URL válida.')

    def action_submit_for_approval(self):
        self.states = 'pending'

    def action_approve(self):
        self.states = 'approved'

        # Crear la compañía
        company = self.env['res.company'].sudo().create({
            'name': self.name,
            'website': self.website,
            'phone': self.phone,
            'currency_id': self.currency_id.id,  # Cambia a la moneda deseada
        })
        self.sudo().update({"company_id": company.id})

        # Crear los usuarios representantes
        self.env['res.users'].sudo().create([
            {
                'name': r.name,
                'login': r.email,  # Cambiar al correo deseado
                'password': r.password,  # Cambiar a la contraseña deseada
                'company_ids': [(4, company.id)],
                'company_id': company.id
            }
            for r in self.representative_id
        ])

        return True

    def action_reject(self):
        self.states = 'rejected'


class Representative(models.Model):
    _name = 'representative.ntizu.company.request'
    _description = 'Representante da Empresa'

    name = fields.Char(string='Nome Completo', required=True)
    email = fields.Char(string='E-mail', required=True)
    password = fields.Char(string='Senha', required=True)
    position = fields.Char(string='Cargo')
    company_id = fields.Many2one('ntizu.company.request', string='Empresa')


class Member(models.Model):
    _name = 'member.ntizu.company.request'
    _description = 'Membro da Empresa'

    name = fields.Char(string='Nome', required=True)
    email = fields.Char(string='E-mail', required=True)
    company_id = fields.Many2one('ntizu.company.request', string='Empresa')
