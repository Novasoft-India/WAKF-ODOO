from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _

class product_inherit(osv.osv):
    
    _inherit = 'product.product'
    _columns ={
               'income': fields.boolean('Income', help="Specify if the product can be selected in a sales order line."),
               'expense': fields.boolean('Expense', help="Specify if the product can be selected in a sales order line."),
               'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the property without removing it."),
               'percentage_income':fields.float('Exempted %'),
               'deductable': fields.boolean('Wheather Related', help="Specify if the product can be selected in a sales order line."),
               'related_id': fields.many2one('product.product', 'Related Income',domain=[('income', '=', True)] ),             
               'percentage_expense':fields.float('Deducted %'),
               'remarks1':fields.text('Description:',size=164),
                             
               }
    _defaults = {
               'percentage_income':100
                 }
product_inherit()

class product_template_inherit(osv.osv):
    _inherit = "product.template"
  

    _columns = {
                'type': fields.selection([('consu', 'Assessable'),('service','Service')], 'Product Type', required=True),
                
                }
product_template_inherit()