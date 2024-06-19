from odoo import models, fields, api
from odoo.exceptions import ValidationError

from odoo.tools.translate import _


class AppUpdate(models.Model):
    _name = 'dlink.api.util.app.update'
    _description = 'Updates for the App'

    name = fields.Char(string=_('Name'), required=True)
    version = fields.Char(string=_('Version'), required=True)
    datetime = fields.Datetime(string=_('DateTime'))
    file = fields.Binary(string=_('File'), required=True)
    package_name = fields.Char(string=_("PackageName"), required=True)

    @api.model
    def create(self, vals_list):
        self._validateFields(vals_list)
        return super(AppUpdate, self).create(vals_list)

    @api.onchange('name', 'version', 'file', 'package_name')
    def updates(self):
        if self._origin:
            valid = self._validateFields({
                "name": self.name,
                "version": self.version,
                "file": self.file,
                "package_name": self.package_name,
            })
            if not valid:
                self.write({
                    "name": self._origin.name,
                    "version": self._origin.version,
                    "file": self._origin.file,
                    "package_name": self._origin.package_name,
                })

    def _validateFields(self, vals):
        fields_required = ['name', 'version', 'package_name', 'file']
        for fr in fields_required:
            if not vals.get(fr):
                raise ValidationError('The field "{field}" is required'.format(field=fr))
        return True
