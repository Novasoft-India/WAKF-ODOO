from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _

class sws_scholar_criteria(osv.osv):
 
    _name = 'sws.scholar.criteria'
    _description = 'sws.scholar.criteria'
    _order = "id desc"
 
    _columns = {
            'name':fields.char('Criteria Name:', required=False),
            'criteria_no':fields.integer('Criteria Number:', required=False), 
            'active_is':fields.boolean('Active',required=False),
            'date_valid':fields.date('Date valid From',required=False),
            'criteria_line_id':fields.one2many('sws.scholar.criteria.line','criteria1_id'),  
            'company_id': fields.many2one('res.company', 'Company', required=False),
                }
    _defaults = {
            'company_id': lambda self,cr,uid,ctx: self.pool['res.company']._company_default_get(cr,uid,object='sws.scholar.criteria',context=ctx)
                 }
sws_scholar_criteria()

class sws_scholar_criteria_line(osv.osv):
 
    _name = 'sws.scholar.criteria.line'
    _description = 'sws.scholar.criteria.line'
 
    _columns = {
            'category_course':fields.many2one('sws.scholar.criteria.course','Course', required=True), 
            'min_annual_income':fields.integer('Maximum Annual Income',required=False),
            'scholar_allowed':fields.boolean('Scholarship Allowed Course',required=False),
            'criteria1_id':fields.many2one('sws.scholar.criteria','Category', required=False),   
            
                }
sws_scholar_criteria_line()

class sws_scholar_course(osv.osv):  
 
    _name = 'sws.scholar.criteria.course'
    _description = 'sws.scholar.criteria.course'
 
    _columns = {
                'name':fields.char('Course Name'),
                'duration':fields.char('Course Duration'),
                'allowed':fields.boolean('Allowed Course'),
                'course_id':fields.one2many('sws.category.education','course_name'),
                
                }
    
sws_scholar_course()

class sws_scholar_institution(osv.osv):  
 
    _name = 'sws.scholar.criteria.institution'
    _description = 'sws.scholar.criteria.institution'
 
    _columns = {
                'name':fields.char('Institution Name'),
                'address':fields.text('Institution Address'),
                'university':fields.char('University'),
                'join_date':fields.date('Join Date'),
                'course_many2one_id':fields.many2one('sws.scholar.criteria.course','Course Name'),
                'course_id':fields.one2many('sws.category.education','course_name'),    
                }
    
sws_scholar_institution()

class sws_scholar_qualification(osv.osv):
 
    _name = 'sws.scholar.criteria.qualification'
    _description = 'sws.scholar.criteria.qualification'
 
    _columns = {
                'name':fields.char('Qualification Name',required=True),
                'allowed':fields.boolean('Allowed Qualification'),
                'qualification_id':fields.one2many('sws.category.education','qualification'),
                }
    
sws_scholar_qualification()