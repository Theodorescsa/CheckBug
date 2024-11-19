from  odoo import models, fields
class EstateOffer(models.Model):
    _name = 'estate_offer'
    _description = 'This is Estate Offer Module'
    price = fields.Float("Price")
    partner_ids = fields.Many2one('res.partner', string="Partner")
    property_ids = fields.Many2one('estate_property','Property')
    status = fields.Selection(
        string='Status',
            selection=[
                ('resfuse', 'Refuse'),
                ('accepted', 'Accepted'),
          
            ]
    )