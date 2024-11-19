from odoo import fields, models
class EstateTags(models.Model):
    _name = "estate_tags"
    _description = 'This is Estate Tags Modules'
    name = fields.Char("Name", size = 100)