from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import time
from datetime import datetime
from datetime import date,timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools.translate import _
from lxml import etree
from openerp.osv.orm import setup_modifiers

class wakf_registration(osv.osv):
 
 
    #_name = 'customer.inherit.'
    _inherit = 'res.partner'
    _order = "id desc"
    #_table = 'res_partner'
    
    def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        if context is None:
            context = {}
        #if (not view_id) and (view_type=='form') and context and context.get('force_email', False):
        #    view_id = self.pool.get('ir.model.data').get_object_reference(cr, user, 'base', 'view_partner_simple_form')[1]
        res = super(wakf_registration,self).fields_view_get(cr, user, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            res['arch'] = self.fields_view_get_address(cr, user, res['arch'], context=context)
         
         
        doc = etree.XML(res['arch'])
         
        if view_type == 'search':
            if not context.get('default_supplier'):   ## Customer
                for node in doc.xpath("//group[@name='extended filter']"):
                    doc.remove(node)
                for node in doc.xpath("//field[@string='Application Number']"):
                    doc.remove(node)
                for node in doc.xpath("//field[@string='Applicant Name']"):
                    doc.remove(node)
                for node in doc.xpath("//group[@string='SWS - Filter By...']"):
                    doc.remove(node)
                for node in doc.xpath("//group[@string='SWS - Group By...']"):
                   doc.remove(node)
                for node in doc.xpath("//filter[@string='Companies']"):
                    node.set('string', 'Wakf Office')
                    doc.remove(node)
                for node in doc.xpath("//filter[@string='Suppliers']"):
                    doc.remove(node)
            if context.get('default_supplier'):       ## Supplier
                for node in doc.xpath("//field[@name='wakf_reg_no']"):
                    doc.remove(node)
                for node in doc.xpath("//field[@string='Wakf Name']"):
                    doc.remove(node)
                for node in doc.xpath("//group[@string='Location-Filter By...']"):
                    doc.remove(node)
                for node in doc.xpath("//filter[@string='Customers']"):
                    doc.remove(node)
                for node in doc.xpath("//filter[@string='Suppliers']"):
                    node.set('string', 'Applicants')
                for node in doc.xpath("//filter[@string='Companies']"):
                    doc.remove(node)
                 
            res['arch'] = etree.tostring(doc)
         
        if view_type == 'tree':
            if not context.get('default_supplier'):
                for node in doc.xpath("//field[@name='appli_no']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='district_sws_id']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='email']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='appli_date']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='head']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='category']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='state1']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='amount_sanction']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
            if context.get('default_supplier'):
                for node in doc.xpath("//field[@name='wakf_reg_no']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='district_id']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='email']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='type_id']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='wakf_registration_date']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='classification']"):
                    node.set('invisible', 'True')
                    #doc.remove(node)
                for node in doc.xpath("//field[@name='taluk_id']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
                for node in doc.xpath("//field[@name='village_id']"):
                    node.set('invisible', 'True')
                    doc.remove(node)
            res['arch'] = etree.tostring(doc)
        return res
    
    def on_change_wakf_village_to_taluk(self, cr, uid, ids, village_id, context=None):
        values = {}
        if village_id:
            cust = self.pool.get('wakf.village').browse(cr, uid, village_id, context=context).taluk_id.id
            cust1 = self.pool.get('wakf.village').browse(cr, uid, village_id, context=context).district_id.id
            values = {
                'wakf_taluk_id': cust,
                'district_id': cust1
            }
        else:
            values = {
                'wakf_taluk_id': False,
                'district_id': False
            }
        return {'value' : values}
    
    def on_change_name(self, cr, uid, ids, is_wakf, context=None):
        values = {}
        if not is_wakf:
            values = {
                'is_person': True,
                
            }
            return {'value' : values}
        return False
    def on_change_category(self, cr, uid, ids, category_id, context=None):
        values = {}
        if category_id:
            cust = self.pool.get('product.category').browse(cr, uid, category_id, context=context).name
            values = {
                'categ_name': cust,
                'category':False
            }
        else:
            values = {
                'categ_name': False,
                'category':False
            }
        return {'value' : values}
    
    def on_change_tick_same(self, cr, uid, ids, tick,datas, context=None):
        values = {}
        if tick and datas:
            values = {
                'comm_address': datas,
            }
        if not tick:
            values = {
                'comm_address': False
            }
        return {'value' : values}
    
    def reg_type_wakf(self, cr, uid, ids,is_wakf, context=None):
        if not is_wakf:
            return{'value':{'details':False,'postoffice':False,'rule_succession':False,'phone':False,'wakf_old_name':False,
                             'sumoto':False,'classification':False,'wakf_objectives':False,'wakf_reg_no':False,'wakf_registration_date':False,
                             'creation_date':False,'gazetted':False,'gazetted_date':False,'comm_addr':False,'waquif_name':False,'waquif_uid':False,
                              'waquif_father_name':False,'waquif_father_uid':False,'waquif_address':False,'type_id':False,'district_id':False,'taluk_id':False,'village_id':False,
                              'wakf_immovable_property_id':False,'wakf_movable_property_id':False,'company_id':False,'is_wakf':False,'is_person':False,'reg_type':False
                             
                             }}
        if is_wakf:
            return{'value':{'reg_type':'wakf'}}
    def reg_type_person(self, cr, uid, ids,is_person, context=None):
        if not is_person:
            return{'value':{'appli_no':False,'category':False,'appli_date':False,'full_name':False,'address':False,
                             'comm_address':False,'tick_same':False,'village':False,'panchayath':False,'taluk_id':False,
                             'district_id':False,'reg_no':False,'wakf_id':False,'sws_pension_id':False,'sws_education_id':False,'sws_orphans_id':False,
                              'sws_firms_id':False,'sws_widow_id':False,'sws_marriage_id':False,'sws_disease_id':False,'sws_maintenance_id':False,'sws_handicapped_id':False,'sws_destitute_id':False,
                              'state1':False,'amount_sanction':False,'meeting_place':False,'acc_no':False,'bank':False
                             }}
        if is_person:
            return{'value':{'reg_type':'person'}}
    
    def on_change_wakf_regno_to_name(self, cr, uid, ids, reg_no, context=None):
        values = {}
        if reg_no:
            id_res_partner=self.pool.get('res.partner')
            search_condition = [('wakf_reg_no', '=', reg_no)]
            search_ids = id_res_partner.search(cr, uid, search_condition, context=context)
            if search_ids:
                similar_objs = id_res_partner.browse(cr, uid, search_ids, context=context)[0]
                values={'wakf_id':similar_objs.id,
                        'district_sws_id':similar_objs.district_id.id,
                        }
                return {'value' :values}
            else:
                values={'wakf_id':False,
                        'district_sws_id':False}
                return {'value' :False}
        return {'value' :False}
    
    def on_change_wakf_name1_to_regno(self, cr, uid, ids, wakf_id, context=None):
        values = {}
        id_res_partner=self.pool.get('res.partner')
        if wakf_id:
            similar_objs = id_res_partner.browse(cr, uid, wakf_id, context=context)
            if similar_objs:
                values={'reg_no':similar_objs.wakf_reg_no,
                        'district_sws_id':similar_objs.district_id.id,
                            }
                return {'value' :values}
            else:
                values={'reg_no':False,
                        'district_sws_id':False
                            }
                return {'value' :values}
        return False
    
    def action_reject1(self, cr, uid, ids, context=None):
        cancel_list =[]
        cancel_dict = {
              'name':"Rejection Summary", 
              'over_income':False,  
              'grant_sanctioned':False, 
              'after_marriage':False, 
              'age_not_specified':False, 
              'under_age':False, 
              'exp_not_spcfed':False, 
              'under_experience':False, 
              'job_income_not':False, 
              'no_reason':True, 
              'no_annual_income':False, 
              'mahal_not_regd':False, 
              'undefined_ctgry':False, 
              'certificate_not':False, 
              'institue_not':False, 
                }
        for rec in self.browse(cr, uid, ids, context=context):
            cancel_list.append((0,0,cancel_dict))
            self.write(cr, uid, ids, {'state1':'rejected','date_cancelled':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'cancelled_by':uid,'sws_popup_id':cancel_list})
        return {'warning': {
                    'title': _('Warning!'),
                    'message':  _('Please add properties for assessment'),                 
                    }
                }
        #return True
    
    def action_verify1(self, cr, uid, ids, context=None):
        criteria_id = self.pool.get('sws.criteria')
        education_criteria_id = self.pool.get('sws.scholar.criteria')
        key = "PASS"
        cancel_list =[]
        cancel_dict = {
              'name':"Rejection Summary", 
              'over_income':False,  
              'grant_sanctioned':False, 
              'after_marriage':False, 
              'age_not_specified':False, 
              'under_age':False, 
              'exp_not_spcfed':False, 
              'under_experience':False, 
              'job_income_not':False, 
              'no_reason':False, 
              'no_annual_income':False, 
              'mahal_not_regd':False, 
              'undefined_ctgry':False, 
              'certificate_not':False, 
              'institue_not':False, 
                }
        for rec in self.browse(cr, uid, ids, context=context):
            category = rec.category.id
            search_condition = [('active_is','=',True),]
            search_ids = criteria_id.search(cr,uid,search_condition, context=context)
            search_condition = [('active_is','=',True),]
            search_ids2 = education_criteria_id.search(cr,uid,search_condition, context=context)
            if search_ids: # active criteria
                criteria_active = criteria_id.browse(cr, uid, search_ids, context=context)[0]
                for items in criteria_active.criteria_line_id: # fetch from one2many list
                    if items.category.id == category:
                        lower_age = items.lower_age 
                        higher_income = items.higher_income
                        min_exp = items.min_exp
                        min_work_gap = items.min_work_gap
########################################################################################################
########################################## Pension ######################################################
##########################################################################################################
                if rec.categ_name == 'Pension':
                    for pension_line in rec.sws_pension_id:   
                        if pension_line.date_of_birth == False:
                            cancel_dict['age_not_specified'] = True
                            key = "FAIL"
                        if pension_line.in_year < min_exp:
                            cancel_dict['under_experience'] = True
                            key = "FAIL"
                        if pension_line.total_annual_income == 0:    
                            cancel_dict['no_annual_income'] = True
                            key = "FAIL"
                        #if pension_line.total_annual_income > higher_income:    ### No Annual Income check for Pension
                        #    cancel_dict['over_income'] = True
                        #    key = "FAIL"
                    
                    if key == "PASS":
                        self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
                    if key == "FAIL":
                        cancel_list.append((0,0,cancel_dict))
                        self.write(cr, uid, ids, {'state1':'rejected','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid,'sws_popup_id':cancel_list})
    ########################################################################################################################
   ############################################## Marriage  ##############################################################
   #########################################################################################################################            
                for items in criteria_active.criteria_line_id: # fetch from one2many list
                    if items.category.id == category:
                        lower_age = items.lower_age 
                        higher_income = items.higher_income
                        min_exp = items.min_exp
                        min_work_gap = items.min_work_gap
                if rec.categ_name == 'Marriage':
                    for marriage_line in rec.sws_marriage_id:   
                        if marriage_line.date_of_birth == False:
                            cancel_dict['age_not_specified'] = True
                            key = "FAIL"
                        if marriage_line.total_income > higher_income:
                            cancel_dict['over_income'] = True
                            key = "FAIL"
                        if marriage_line.total_income == 0:
                            cancel_dict['no_annual_income'] = True
                            key = "FAIL"
                        if marriage_line.check_required:
                            if marriage_line.date_of_birth:
                                dt_birth = marriage_line.date_of_birth
                                dt_today = datetime.now()
                                dt_birth = datetime.strptime(dt_birth,"%Y-%m-%d")
                                dt_mrg = datetime.strptime(dt_today,"%Y-%m-%d")
                                r = relativedelta(dt_mrg, dt_birth)
                                age = r.years
                                if age < lower_age:
                                    cancel_dict['under_age'] = True
                                    key = "FAIL"
                        else:   
                            if marriage_line.date_of_birth and marriage_line.date_marriage :
                                dt_birth = marriage_line.date_of_birth
                                dt_mrg = marriage_line.date_marriage
                                dt_birth = datetime.strptime(dt_birth,"%Y-%m-%d")
                                dt_mrg = datetime.strptime(dt_mrg,"%Y-%m-%d")
                                r = relativedelta(dt_mrg, dt_birth)
                                age_mrg = r.years
                                if age_mrg <= lower_age:
                                    cancel_dict['under_age'] = True
                                    key = "FAIL"
                        if rec.appli_date and marriage_line.date_marriage :
                            dt_appli = rec.appli_date
                            dt_mrg = marriage_line.date_marriage
                            if dt_mrg >= dt_appli:
                                cancel_dict['after_marriage'] = True
                                key = "FAIL"
                    
                    if key == "PASS":
                        self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
                    if key == "FAIL":
                        cancel_list.append((0,0,cancel_dict))
                        self.write(cr, uid, ids, {'state1':'rejected','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid,'sws_popup_id':cancel_list})
 ###################################################################################################################################
 ###################################################  Disease  #########################################################################3
 ######################################################################################################################################
                for items in criteria_active.criteria_line_id: # fetch from one2many list
                    if items.category.id == category:
                        lower_age = items.lower_age 
                        higher_income = items.higher_income
                        min_exp = items.min_exp
                        min_work_gap = items.min_work_gap
                if rec.categ_name == 'Disease':
                    for disease_line in rec.sws_disease_id:   
                        if disease_line.date_of_birth == False:
                            cancel_dict['age_not_specified'] = True
                            key = "FAIL"
                        if disease_line.total_income == 0:
                            cancel_dict['no_annual_income'] = True
                            key = "FAIL"
                        if disease_line.total_income > higher_income:
                            cancel_dict['over_income'] = True
                            key = "FAIL"
                    
                    if key == "PASS":
                        self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
                    if key == "FAIL":
                        cancel_list.append((0,0,cancel_dict))
                        self.write(cr, uid, ids, {'state1':'rejected','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid,'sws_popup_id':cancel_list})           
 ####################################################################################################################################
 ##################################################### Destitute  ######################################################################
 #####################################################################################################################################
                for items in criteria_active.criteria_line_id: # fetch from one2many list
                    if items.category.id == category:
                        lower_age = items.lower_age 
                        higher_income = items.higher_income
                        min_exp = items.min_exp
                        min_work_gap = items.min_work_gap
                if rec.categ_name == 'Destitute':
                    for destitute_line in rec.sws_destitute_id:   
                        if destitute_line.date_of_birth == False:
                            cancel_dict['age_not_specified'] = True
                            key = "FAIL"
                        if destitute_line.total_income == 0:
                            cancel_dict['no_annual_income'] = True
                            key = "FAIL"
                        if destitute_line.total_income > higher_income:
                            cancel_dict['over_income'] = True
                            key = "FAIL"
                    
                    if key == "PASS":
                        self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
                    if key == "FAIL":
                        cancel_list.append((0,0,cancel_dict))
                        self.write(cr, uid, ids, {'state1':'rejected','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid,'sws_popup_id':cancel_list})           
####################################################################################################################################
 ##################################################### Handicapped  ######################################################################
 #####################################################################################################################################
                for items in criteria_active.criteria_line_id: # fetch from one2many list
                    if items.category.id == category:
                        lower_age = items.lower_age 
                        higher_income = items.higher_income
                        min_exp = items.min_exp
                        min_work_gap = items.min_work_gap
                if rec.categ_name == 'Handicapped':
                    for handicapped_line in rec.sws_handicapped_id:   
                        if handicapped_line.date_of_birth == False:
                            cancel_dict['age_not_specified'] = True
                            key = "FAIL"
                        if handicapped_line.total_income == 0:
                            cancel_dict['no_annual_income'] = True
                            key = "FAIL"
                        if handicapped_line.total_income > higher_income:
                            cancel_dict['over_income'] = True
                            key = "FAIL"
                    
                    if key == "PASS":
                        self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
                    if key == "FAIL":
                        cancel_list.append((0,0,cancel_dict))
                        self.write(cr, uid, ids, {'state1':'rejected','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid,'sws_popup_id':cancel_list})
####################################################################################################################################
 ##################################################### Maintenance  ######################################################################
 #####################################################################################################################################
                for items in criteria_active.criteria_line_id: # fetch from one2many list
                    if items.category.id == category:
                        lower_age = items.lower_age 
                        higher_income = items.higher_income
                        min_exp = items.min_exp
                        min_work_gap = items.min_work_gap
                if rec.categ_name == 'Maintenance':
                    for maintenance_line in rec.sws_maintenance_id:   
                        if maintenance_line.date_of_birth == False:
                            cancel_dict['age_not_specified'] = True
                            key = "FAIL"
                        if maintenance_line.total_income == 0:
                            cancel_dict['no_annual_income'] = True
                            key = "FAIL"
                        if maintenance_line.total_income > higher_income:
                            cancel_dict['over_income'] = True
                            key = "FAIL"
                    
                    if key == "PASS":
                        self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
                    if key == "FAIL":
                        cancel_list.append((0,0,cancel_dict))
                        self.write(cr, uid, ids, {'state1':'rejected','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid,'sws_popup_id':cancel_list})
####################################################################################################################################
 ##################################################### Orphans  ######################################################################
 #####################################################################################################################################
                for items in criteria_active.criteria_line_id: # fetch from one2many list
                    if items.category.id == category:
                        lower_age = items.lower_age 
                        higher_income = items.higher_income
                        min_exp = items.min_exp
                        min_work_gap = items.min_work_gap
                if rec.categ_name == 'Orphans':
                    for orphans_line in rec.sws_orphans_id:   
                        if orphans_line.date_of_birth == False:
                            cancel_dict['age_not_specified'] = True
                            key = "FAIL"
                        if orphans_line.total_income == 0:
                            cancel_dict['no_annual_income'] = True
                            key = "FAIL"
                        if orphans_line.total_income > higher_income:
                            cancel_dict['over_income'] = True
                            key = "FAIL"
                    
                    if key == "PASS":
                        self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
                    if key == "FAIL":
                        cancel_list.append((0,0,cancel_dict))
                        self.write(cr, uid, ids, {'state1':'rejected','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid,'sws_popup_id':cancel_list})
####################################################################################################################################
 ##################################################### Widow  ######################################################################
 #####################################################################################################################################
                for items in criteria_active.criteria_line_id: # fetch from one2many list
                    if items.category.id == category:
                        lower_age = items.lower_age 
                        higher_income = items.higher_income
                        min_exp = items.min_exp
                        min_work_gap = items.min_work_gap
                if rec.categ_name == 'Widow':
                    for widow_line in rec.sws_widow_id:   
                        if widow_line.date_of_birth == False:
                            cancel_dict['age_not_specified'] = True
                            key = "FAIL"
                        if widow_line.total_income == 0:
                            cancel_dict['no_annual_income'] = True
                            key = "FAIL"
                        if widow_line.total_income > higher_income:
                            cancel_dict['over_income'] = True
                            key = "FAIL"
                    
                    if key == "PASS":
                        self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
                    if key == "FAIL":
                        cancel_list.append((0,0,cancel_dict))
                        self.write(cr, uid, ids, {'state1':'rejected','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid,'sws_popup_id':cancel_list})
####################################################################################################################################
 ##################################################### Firms  ######################################################################
 #####################################################################################################################################
                if rec.categ_name == 'Firms':
                    self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
            
            
            #else:      
                #  no active criteria
####################################################################################################################################
 ##################################################### Education  ######################################################################
 #####################################################################################################################################
 
            if search_ids2 and rec.categ_name == 'Education Loan':
                criteria_active = education_criteria_id.browse(cr, uid, search_ids2, context=context)[0]
                for edu in rec.sws_education_id:
                    id_course = edu.course_name.id
                for items in criteria_active.criteria_line_id: # fetch from one2many list
                    if items.category_course.id == id_course:
                        course = items.category_course 
                        higher_income = items.min_annual_income
                        if rec.categ_name == 'Education Loan':
                            for education_line in rec.sws_education_id:   
                                if education_line.date_of_birth == False:
                                    cancel_dict['age_not_specified'] = True
                                    key = "FAIL"
                                if education_line.total_annual_income == 0:
                                    cancel_dict['no_annual_income'] = True
                                    key = "FAIL"
                                if education_line.total_annual_income > higher_income:
                                    cancel_dict['over_income'] = True
                                    key = "FAIL"
                            
                            if key == "PASS":
                                self.write(cr, uid, ids, {'state1':'verified','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid})
                            if key == "FAIL":
                                cancel_list.append((0,0,cancel_dict))
                                self.write(cr, uid, ids, {'state1':'rejected','date_verified':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'verified_by':uid,'sws_popup_id':cancel_list})
        return True
    
    def action_submit(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            sequence=self.pool.get('ir.sequence').get(cr, uid, 'SWS')
        self.write(cr, uid, ids, {'appli_no':sequence,'state1':'submitted','date_submitted':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'submitted_by':uid})
        return True
    
    def action_approve1(self, cr, uid, ids, context=None):
        invoice_ids = []
        for rec in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, ids, {'state1':'approved','date_approved':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'approved_by':uid})
        return True
    
    def action_stop_pension(self, cr, uid, ids, context=None):
        invoice_ids = []
        for rec in self.browse(cr, uid, ids, context=context):
            finish_pension = rec.finish_pension
            if finish_pension:
                self.write(cr, uid, ids, {'state1':'finished','date_approved':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'approved_by':uid})
        return True
    
    def action_stop_education(self, cr, uid, ids, context=None):
        invoice_ids = []
        for rec in self.browse(cr, uid, ids, context=context):
            finish_pension = rec.finish_edu
            if finish_pension:
                self.write(cr, uid, ids, {'state1':'paid'})
        return True
    
    def sanction_education_loan(self,cr,uid,ids):
        line_list = []
        for rec in self.browse(cr,uid,ids):
            course_id = rec.sws_education_id[0].course_name.id
            date_start = rec.date_sanction
            date_to = rec.date_sanction
        search_list = self.pool.get('sws.scholar.sanction.criteria').search(cr,uid,[('active_is','=',True)])
        if not saerch_list:
            raise osv.except_osv(_('Warning!'), _('Please set criteria for this course first'))
        browse_list = self.pool.get('sws.scholar.sanction.criteria').browse(cr,uid,search_list)
        for values in browse_list:
            for vals in values.criteria_line_id:
                if vals.category_course.id == course_id:  ##  Fetching Records from Master Table 
                    lines = vals.total_year
                    amount_year = vals.amount_per_year
                    total_amount = vals.amount_sanction
        if lines and amount_year:
            for i in range(lines):
                #date_to = date_to + relativedelta.relativedelta(year=+1))
                date_to = datetime.strptime(date_to,"%Y-%m-%d")+ relativedelta(years=1)
                date_to = date_to.strftime("%Y-%m-%d")
                line_list.append((0,0,{'year':i+1,'date_from':date_start,'date_to':date_to,'amount':amount_year,'state':'pending'}))
                date_start = date_to
                
            self.write(cr,uid,ids,{'education_byyear':line_list,'amount_sanction':total_amount})
        return False
    
    def action_sanction(self, cr, uid, ids, context=None):
        invoice_ids = []
        transaction_list = []
        invoice_obj = self.pool.get('account.invoice')
        for rec in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, ids, {'state1':'sanctioned','date_sanctioned':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),'sanctioned_by':uid})
            output = rec.id
            product = rec.category.id
            name = "SWS"+"-"+rec.category.name
            quantity = 1
            head = rec.head.id
            #price_subtotal = 100
            price_unit = rec.amount_sanction
            new_amount = rec.amount_sanction
            appli_no = rec.appli_no
            date_sanction = rec.date_sanction
            ############################
            date_today = date.today()
            month = date_today.month
            year = date_today.year
            if month == 1: 
                month = 'JAN'
            if month == 2: 
                month = 'FEB'
            if month == 3: 
                month = 'MAR'
            if month == 4: 
                month = 'APR'
            if month == 5: 
                month = 'MAY'
            if month == 6: 
                month = 'JUN'
            if month == 7: 
                month = 'JUL'
            if month == 8: 
                month = 'AUG'
            if month == 9: 
                month = 'SEP'
            if month == 10: 
                month = 'OCT'
            if month == 11: 
                month = 'NOV'
            if month == 12: 
                month = 'DEC'
            #############################
            invoice_ids.append((0,0,{'product_id':product,'name':name,'quantity':quantity,'price_unit':price_unit,'new_amount':new_amount,'sws':True}))
        if rec.category.name == "Education":
            ###############################################################################################
            search_ids = self.pool.get('account.account').search(cr,uid,[('name','=',"Accounts Receivable")])
            if not search_ids:
                raise osv.except_osv(_('Warning!'), _('Please create an account "Accounts Receivable" first'))
            account_id = self.pool.get('account.account').browse(cr,uid,search_ids)[0].id
            
            search_ids = self.pool.get('account.journal').search(cr,uid,[('name','=',"Assessment Journal")])
            if not search_ids:
                raise osv.except_osv(_('Warning!'), _('Please create "Assessment Journal" First'))
            journal_id = self.pool.get('account.journal').browse(cr,uid,search_ids)[0].id
            ###############################################################################################
            date_today = date_today.strftime("%Y-%m-%d")
            #if date_sanction < date_today:
            #    self.pool.get('account.invoice').create(cr,uid,{'date_sanction':date_sanction,'head':head,'journal_type':'sale','type':'out_invoice','is_sws':True,'appli_no':appli_no,'account_id':account_id,'journal_id':journal_id,'partner_id':output,'invoice_line':invoice_ids})
            #transaction_list.append((0,0,{'date_sanction':date_sanction,'for_month':month,'year':year,'amount':price_unit,'status':'pending'}))
            self.sanction_education_loan(cr,uid,ids)
            self.write(cr,uid,ids,{'state1':'sanctioned'})
        if rec.head.name == "Pension":
            ###########################################################################
            search_ids = self.pool.get('account.account').search(cr,uid,[('name','=',"Accounts Payable")])
            if not search_ids:
                raise osv.except_osv(_('Warning!'), _('Please create an account "Accounts Payable" first'))
            account_id = self.pool.get('account.account').browse(cr,uid,search_ids)[0].id
            
            search_ids = self.pool.get('account.journal').search(cr,uid,[('name','=',"SWS Journal")])
            if not search_ids:
                raise osv.except_osv(_('Warning!'), _('Please create "SWS Journal" First'))
            journal_id = self.pool.get('account.journal').browse(cr,uid,search_ids)[0].id
            ##############################################################################
            date_today = date_today.strftime("%Y-%m-%d")
            ########################## TEMPORARY COMMENT  ########################
            ######################################################################
            #if date_sanction < date_today:
                #self.pool.get('account.invoice').create(cr,uid,{'date_sanction':date_sanction,'key':"pension",'head':head,'for_month':month,'year':year,'amount':price_unit,'journal_type':'purchase','type':'in_invoice','is_sws':True,'appli_no':appli_no,'account_id':account_id,'journal_id':journal_id,'partner_id':output,'invoice_line':invoice_ids})   
            transaction_list.append((0,0,{'date_sanction':date_sanction,'for_month':month,'year':year,'amount':price_unit,'status':'pending'}))
            #self.write(cr,uid,ids,{'state1':'sanctioned','history_transaction':transaction_list})
            self.write(cr,uid,ids,{'state1':'sanctioned','history_transaction':transaction_list})
        if not (rec.head.name == "Pension" or rec.category.name == "Education"):
        #else:
            ###########################################################################
            search_ids = self.pool.get('account.account').search(cr,uid,[('name','=',"Accounts Payable")])
            if not search_ids:
                raise osv.except_osv(_('Warning!'), _('Please create an account "Accounts Payable" first'))
            account_id = self.pool.get('account.account').browse(cr,uid,search_ids)[0].id
            
            search_ids = self.pool.get('account.journal').search(cr,uid,[('name','=',"Purchase Journal")])
            if not search_ids:
                raise osv.except_osv(_('Warning!'), _('Please create "Purchase Journal" First'))
            journal_id = self.pool.get('account.journal').browse(cr,uid,search_ids)[0].id
            ##############################################################################
            date_today = date_today.strftime("%Y-%m-%d")
            if date_sanction <= date_today:
                self.pool.get('account.invoice').create(cr,uid,{'date_sanction':date_sanction,'head':head,'for_month':month,'year':year,'amount':price_unit,'journal_type':'purchase','type':'in_invoice','is_sws':True,'is_assessment':False,'appli_no':appli_no,'account_id':account_id,'journal_id':journal_id,'partner_id':output,'invoice_line':invoice_ids})   
            transaction_list.append((0,0,{'date_sanction':date_sanction,'for_month':month,'year':year,'amount':price_unit,'status':'pending'}))
            self.write(cr,uid,ids,{'state1':'sanctioned','history_transaction':transaction_list})
        return True
    
    
 
    _columns = {
            #'name':fields.char('Wakf Name', size=128, required=False),
            'details':fields.char('Details', size=128, required=False),
            'postoffice':fields.char('Rule of Succession', size=128, required=False),
            'rule_succession':fields.char('Post Office', size=128, required=False),
            'phone':fields.char('Phone Number', size=64, required=False),
            'wakf_old_name':fields.char('Wakf old name', size=128, required=False),
            'suomoto':fields.boolean('Suomoto',required=False),        
            'classification':fields.selection((('sunni','Sunni'), ('shia','Shia')),'Classification',required=False),
            'wakf_objectives':fields.text('Remarks',required=False),
            'wakf_reg_no':fields.integer('Registration No',size=8,required=False),
            'wakf_registration_date':fields.date('Registration Date',required=False),
            'creation_date':fields.date('Wakf Creation Date',required=False),
            'gazetted':fields.boolean('Gazetted'),
            'gazetted_date':fields.date('Gazetted Date',required=False),
            'comm_addr':fields.text('Communication address',help='Address for communication of wakf',required=False),
            'waquif_name':fields.char('Waquif Name',size=128,required=False),
            'waquif_uid':fields.char('Waquif UID',size=32,required=False,help='Unique Identification to be assigned from the Aadhar Project'),
            'waquif_father_name':fields.char("Father/Husband's Name",size=128,required=False),
            'waquif_father_uid':fields.char("Father/Husband's UID",size=32,required=False,help='Unique Identification to be assigned from the Aadhar Project'),
            'waquif_address':fields.text('Waquif Address',required=False),
            'type_id':fields.many2one('wakf.type','Wakf Type',ondelete='set null',required=False),
            'district_id':fields.many2one('wakf.district','Wakf District',ondelete='set null'),
            'wakf_taluk_id':fields.many2one('wakf.taluk','Taluk',ondelete='set null'),
            'village_id':fields.many2one('wakf.village','Village',ondelete='set null'), 
            'wakf_immovable_property_id':fields.one2many('wakf.immovableproperty','wakf_id','Immovable Properties'),
            'wakf_movable_property_id':fields.one2many('wakf.movableproperty','wakf_id','Movable Properties'),
            'wakf_management_id':fields.one2many('wakf.management','wakf_id','Management Details'),
            #'company_id': fields.many2one('res.company', 'Company', required=False),
            'is_wakf':fields.boolean('Is a wakf ?'),
            'is_person':fields.boolean('Is a person ?'),
            'reg_type':fields.selection([('wakf','Wakf'),('person','Person')],'Registration type'),
            #======================================= SWS ======================================#
            
            'appli_no':fields.char('Application Number:', size=64, required=False),
            'category': fields.many2one('product.product','Category',domain=['&',('income','!=',True),('expense','!=',True)], ondelete='set null'),
            'categ_name':fields.char('Category Name', size=128, required=False),
             
            'appli_date':fields.date('Application Date:'),
            'full_name':fields.char('Full Name:', size=64),
            'address':fields.text('Address:', size=64),
            'comm_address':fields.text('Communication Address:', size=256, required=False),
            'tick_same':fields.boolean('Tick, if same as above', required=False),
            'village':fields.char('Village:', size=256, required=False),
            'panchayath':fields.char('Pan/Mun/Corp:', size=64, required=False),
            'taluk_id':fields.many2one('wakf.taluk','Taluk',ondelete='set null'),
            'district_sws_id':fields.many2one('wakf.district','District',ondelete='set null'),
            'reg_no':fields.integer('Wakf Reg No', size=8),
            'wakf_id':fields.many2one('res.partner','Wakf Name',ondelete='set null'),
            'sws_pension_id':fields.one2many('sws.category.pension','sws_id1','Pension Details',limit=1),
            'sws_education_id':fields.one2many('sws.category.education','sws_id1','Education Details'),
            'sws_orphans_id':fields.one2many('sws.category.orphans','sws_id1','Orphans Details'),
            'sws_firms_id':fields.one2many('sws.category.firms','sws_id1','Firms Details'),
            'sws_widow_id':fields.one2many('sws.category.widow','sws_id1','Widow Details'),
            'sws_marriage_id':fields.one2many('sws.category.marriage','sws_id1','Marriage Details'),
            'sws_disease_id':fields.one2many('sws.category.disease','sws_id1','Disease Details'),
            'sws_maintenance_id':fields.one2many('sws.category.maintenance','sws_id1','Maintenance Details'),
            'sws_handicapped_id':fields.one2many('sws.category.handicaped','sws_id1','Handicapped Details'),
            'sws_destitute_id':fields.one2many('sws.category.destitute','sws_id1','Destitute Details'),
            'sws_popup_id':fields.one2many('pop.up.cancel','sws_id1','POP up Details'),
            'history_transaction':fields.one2many('pension.disease.history','main_id','History of Trnsctn Details'),
            'education_byyear':fields.one2many('education.loan.byyearp','education_loan_byyear_id','By year Trnsctn Details'),
            'popup_id': fields.many2one('pop.up.cancel', 'POPUP', required=False),
            'submitted_by': fields.many2one('res.users', 'Submitted by', readonly=True),
            'date_submitted': fields.datetime('Date Submitted', readonly=True),
            'verified_by': fields.many2one('res.users', 'Verified by', readonly=True),
            'date_verified': fields.datetime('Date Verified', readonly=True),
            'approved_by': fields.many2one('res.users', 'Approved by', readonly=True),
            'date_approved': fields.datetime('Date Approved', readonly=True),
            'cancelled_by': fields.many2one('res.users', 'Rejected by', readonly=True),
            'date_cancelled': fields.datetime('Date Rejected', readonly=True),
            'sanctioned_by': fields.many2one('res.users', 'Sanctioned by', readonly=True),
            'date_sanctioned': fields.datetime('Date Sanctioned', readonly=True),
            'refunded_by': fields.many2one('res.users', 'Re-Fund by', readonly=True),
            'date_refund': fields.datetime('Date Refund', readonly=True),
            'state1': fields.selection([
                ('submitted', 'Submitted'),
                ('verified', 'Verified'),
                ('approved', 'Board Approved'),
                ('sanctioned', 'Amount Sanctioned'),
                ('revolving', 'Revolving'),
                ('finished', 'Finished'),
                ('rejected', 'Rejected'),
                ('re_payment', 'Ready for Refund'),
                ('paid', 'Refund Completed'),
                ],'status', readonly=False),
            'amount_sanction':fields.float('Amount Sanction'),
            'sanction_details':fields.char('Sanction Details',size=256),
            'board_approved_date':fields.date('Board Approved Date'),
            'date_sanction':fields.date('Starting Date'),
            'meeting_place':fields.char('Meeting Place'),
            'meeting_date':fields.date('Meeting Date'),
            ##########################################################
            'finish_pension':fields.boolean('Stop Pension Cycle'),
            'reason': fields.selection([
                ('death', 'Death'),
                ('disqualify', 'Disqualified'),
                ],'Reason', readonly=False),
            'date_death':fields.date('Date of Death'),
            ##########################################################
            'finish_edu':fields.boolean('Stop Loan'),
            'reason_edu': fields.selection([
                ('death', 'Death'),
                ('disqualify', 'Disqualified'),
                ],'Reason', readonly=False),
            'date_death_edu':fields.date('Date of Cancellation'),
               
            'course_end':fields.date('Course Ending Date'),
            'amount_balance':fields.float('Balance Amount'),
            'amount_received':fields.char('Amount Received'),
              
            'head': fields.many2one('product.category', 'Head',domain=[('parent_id','!=',1)]),
              
            
              
        }
    _defaults = {
                 'is_wakf':lambda *a:True,
                 #'company_id': lambda self,cr,uid,ctx: self.pool['res.company']._company_default_get(cr,uid,object='res.partner',context=ctx) 
                 #'company_id': lambda self, cr, uid, ctx: self.pool.get('res.company')._company_default_get(cr, uid, 'res.partner', context=ctx),
                #'state1':lambda *a:'submitted',
                #'submitted_by': lambda obj, cr, uid, context: uid,
                #'date_submitted':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                  }
    
    #===========================================================================
    # _sql_constraints = [
    #     ('wakf_reg_uniq', 'Check(wakf_reg_no=wakf_reg_no)', 'Register Number already exists !'),
    # ]
    #===========================================================================
    
wakf_registration()    

class pension_disease_history(osv.osv):
 
 
    _name = 'pension.disease.history'
    _columns = {
            'year':fields.char('Year'),
            #'for_month': fields.char('For Month'),
            'for_month': fields.selection([
                ('JAN', 'January'),
                ('FEB', 'February'),
                ('MAR', 'March'),
                ('APR', 'April'),
                ('MAY', 'May'),
                ('JUN', 'June'),
                ('JUL', 'July'),
                ('AUG', 'August'),
                ('SEP', 'September'),
                ('OCT', 'October'),
                ('NOV', 'November'),
                ('DEC', 'December'),
                ],'For Month of', readonly=True),
            'date_sanction':fields.date('Date of Sanction'),
            'amount':fields.float('Amount'),
            'dd_no':fields.char('Cheque/DD No'),
            'transaction_no':fields.char('Transaction No'),
            'status': fields.selection([
                ('paid', 'Paid'),
                ('pending', 'Pending'),
                ('invoiced', 'Invoiced'),
                ('returned', 'Returned'),
                ('closed', 'Closed'),
                ],'Status', readonly=True),
            'main_id': fields.many2one('res.partner', 'History of Transaction', readonly=False),
                }   

pension_disease_history()
    
