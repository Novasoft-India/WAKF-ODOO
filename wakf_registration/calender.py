from openerp.osv import osv
from openerp.osv import fields

class calender_test(osv.osv):
 
    _name = 'calender.test'
    _description = 'calender.test'
    _order = "id desc"
    
    _columns = {
            'date_from':fields.date('Date From'),
            'date_to':fields.date('Date To'),
            'employee_id':fields.many2one('account.invoice','Employee'),
                }
calender_test()