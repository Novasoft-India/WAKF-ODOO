from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _


class wakf_type(osv.osv):
    
    _name='wakf.type'
    _description = 'wakf.type'
    
    
    _columns = {
                'name':fields.char('Type',size=16,required=True),
                'description':fields.text('Description',required=False),
                'wakf_id':fields.one2many('res.partner','type_id','Wakf')                
                
                }

wakf_type()
