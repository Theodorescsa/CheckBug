from odoo import models, fields, api

class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'Estate Property Model'
    
    name = fields.Char(string='Name', size=100, required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode', size=20)
    date_availability = fields.Date(string='Date Availability',default=fields.Date.today)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms',default = 3)  # Sửa từ Interger thành Integer
    living_area = fields.Integer(string='Living Area')  # Sửa từ Interger thành Integer
    facades = fields.Integer(string='Facades')  # Sửa từ Interger thành Integer
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')  # Sửa từ Interger thành Integer
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help='Select the orientation of the garden'
    )
    active = fields.Boolean(string="Active", default=False)  # Đặt mặc định là True
    state = fields.Selection(
            string='State',
            selection=[
                ('new', 'New'),
                ('offer_received', 'Offer Received'),
                ('offer_accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('canceled', 'Canceled')
            ],
            default='new',
            required=True,
            copy=False,  # Trường này sẽ không được sao chép khi bản ghi được dupliate
        )
    property_type_id = fields.Many2one("estate_type", string="Estate Type")
    buyer_id = fields.Many2one(related="property_type_id.buyer_id", string="Buyer", readonly=True, store=True)
    salesperson_id = fields.Many2one(related="property_type_id.salesperson_id", string="Salesperson", readonly=True, store=True)
    
    tag_ids = fields.Many2many("estate_tags", String = "Estate Tag")
    
    offer_ids = fields.One2many('estate_offer', 'property_ids', string="Offers")

    total_area = fields.Integer()
    

    @api.onchange('living_area','garden_area')
    def _onchange_living_area(self):
        for record in self:
        # Cập nhật giá trị trường total_area mỗi khi living_area thay đổi
            if record.living_area:
                record.total_area = record.living_area + record.garden_area  # Ví dụ tính tổng diện tích
            else:
                record.total_area = 0
    def copy(self, default=None):
        # Tạo dictionary để chứa giá trị mặc định cho các trường cần xóa
        default = dict(default or {})
        
        # Xóa giá trị của 'selling_price' và 'date_availability' khi sao chép
        default['selling_price'] = False
        default['date_availability'] = False
        
        # Gọi phương thức `copy` của lớp cha để tạo bản sao với các giá trị mặc định đã thay đổi
        return super(EstateProperty, self).copy(default=default)