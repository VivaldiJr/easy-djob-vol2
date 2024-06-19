from odoo import models, fields


class TesteHabilidades(models.Model):
    _name = 'ntizu.teste.skill'
    _description = 'Teste de Habilidades'
    _order = 'create_date desc'

    name = fields.Char(string='Título', required=True)
    icon = fields.Binary(string='Ícone')
    description = fields.Text(string='Descrição')
    test_link = fields.Char(string='Link do Teste')
    is_new = fields.Boolean(string='É Novo', default=True)


class Formacao(models.Model):
    _name = 'ntizu.formacao'
    _description = 'Formação'
    _order = 'create_date desc'

    name = fields.Char(string='Título', required=True)
    icon = fields.Binary(string='Ícone')
    description = fields.Text(string='Descrição')
    link = fields.Char(string='Link de Formação')
    is_new = fields.Boolean(string='É Novo', default=True)
