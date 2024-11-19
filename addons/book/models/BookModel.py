from odoo import fields, models

class BookModel(models.Model):
    _name = "book.management"
    _description = "This is Book Management Module"
    
    name = fields.Char("Tên sách", size=100, required=True)
    description = fields.Text("Mô tả")
    author = fields.Char("Tác giả", size=100, required=True)
    price = fields.Float("Giá")
    quantity = fields.Integer("Số lượng")
    
    category = fields.Selection(
        selection=[("horror", "Kinh Dị"), ("cartoon", "Hoạt Hình"), ("love", "Tình cảm")],
        string="Thể loại",
        help="Select kind of book"
    )
    def copy(self, default=None):
        # Tạo dictionary để chứa giá trị mặc định cho các trường cần thay đổi
        default = dict(default or {})
        
        # Bạn có thể sao chép tất cả các trường khác và thay đổi các trường cần thiết
        default['price'] = 100
        default['category'] = False  # Loại bỏ thể loại khi sao chép
        
        # Gọi phương thức `copy` của lớp cha để tạo bản sao với các giá trị mặc định đã thay đổi
        return super(BookModel, self).copy(default=default)