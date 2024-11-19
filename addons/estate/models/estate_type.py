from odoo import fields, models
class EstateType(models.Model):
    _name = "estate_type"
    _description = "This is estate property type module"
    name = fields.Char("Estate Type",size = 100)
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
