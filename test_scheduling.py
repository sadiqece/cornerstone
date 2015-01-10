from openerp import addons
from datetime import datetime, timedelta, date
from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _



import logging
import pytz
import re
import time
from openerp import tools
_logger = logging.getLogger(__name__)

class test_info(osv.osv):

	
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(test_info, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def default_get(self, cr, uid, fields, context=None):
		data = super(test_info, self).default_get(cr, uid, fields, context=context)
		invoice_lines = []
		modality_ids = self.pool.get('test.master.modality').search(cr, uid, [],limit=5)
		for p in self.pool.get('test.master.modality').browse(cr, uid, modality_ids):
			invoice_lines.append((0,0,{'master_modality':p.id,}))
		data['test_modality'] = invoice_lines
		return data
		
	def _calculate_total_learners(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = self.browse(cr, uid, ids[0], context=context).learner_line or []
		total_mod = len(mod_line_ids)
		res[line.id] = total_mod
		return res
	

	_name = "test.info"
	_description = "This table is for keeping Test Schedules"
	_columns = {
		's_no': fields.integer('S_No', size=100),
		'test_def_id': fields.many2one('test', 'Test Definition',  ondelete='cascade', help='Test', select=True, required=True),
		'name': fields.related('test_def_id','name',type="char",relation="test",string="Name", readonly=1,),
		'test_type_id':fields.integer('Test Type Id'),
		'test_pre_type':fields.selection((('Pre Test','Pre Test'),),'Test Type', ),
		'test_type':fields.selection((('Pre Test','Pre Test'),('Post Test','Post Test')),'Test Type', ),
		'test_post_type':fields.selection((('Post Test','Post Test'),),'Test Type', ),
		'test_type_char':fields.char('Test Type'),
		'class_info': fields.many2one('class.info', 'Select Class',  ondelete='cascade', help='Module', select=True, ),
		'test_code': fields.char('Test Code', size=20, readonly=1),
		'test_code_compliance': fields.char('Test Code (Compliance)', size=20),
		'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True, required=True),
		'module_ids': fields.char('Module_Ids'),
		'module_code': fields.char('Module Code', size=20, readonly=1),
		'start_date': fields.datetime('Start Date', required=True),
		'end_date': fields.datetime('End Date'),
		'duration': fields.float('Duration(Hrs)'),
		'location_id':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'room_id':fields.many2one('room', 'Rooms', ondelete='cascade', help='Room', select=True, required=True),
		'test_modality': fields.one2many('test.modality','test_modality_id', 'Test Modality'),
		'delivery_mode': fields.selection((('English','English'),('Singli','Singli'),('Malyi','Malyi')),'Delivery Mode'),
		'learner_line': fields.one2many('test.learner', 'learner_mod_id', 'Learner Lines', select=True, required=True),
		'test_scores': fields.one2many('test.scores','test_scores_id','Test Scores'),
		'status': fields.related('test_def_id','test_status',type="char",relation="test",string="Status", readonly=1,),
		'capacity':fields.related('test_def_id','test_max_Pax',type="integer",relation="test",string="Capacity", readonly=1,),
		'actual_number':fields.function(_calculate_total_learners, relation="test.info",readonly=1,string='No. Learners',type='integer'),
	}


	def create(self,cr, uid, values, context=None):
	
		if 'test_pre_type' in values  and values['test_pre_type'] != False :
			values['test_type_char']  = values['test_pre_type'] 
		elif 'test_post_type' in values  and values['test_post_type'] != False :
			values['test_type_char']  = values['test_post_type'] 
		elif 'test_type' in values  and values['test_type'] != False :
			values['test_type_char']  = values['test_type'] 
		
		for x in values['learner_line'] : 
			learner = self.pool.get('learner.info').browse(cr,uid,x[2]['learner_id'])
			learner_mod_obj = self.pool.get('enroll.module.line')
			learner_mod_obj_ids = learner_mod_obj.search(cr,uid,[('learner_info_id','=',learner.id)])
			lear_module_ids=[]
			for x in learner_mod_obj.browse(cr,uid,learner_mod_obj_ids):
				lear_module_ids.append(x['module_id'].id)
				
			if values['module_id'] not in lear_module_ids:
					raise osv.except_osv(_('Error!'),_("Learner Module Does Not Match Selected Module - "+str(learner.name)))
		
		_logger.info("Create Values %s",values)
		module_id = super(test_info, self).create(cr, uid, values, context=context)
		return module_id

	def write(self,cr, uid, ids, values, context=None):
		if 'test_pre_type' in values  and values['test_pre_type'] != False :
			values['test_type_char']  = values['test_pre_type'] 
		elif 'test_post_type' in values  and values['test_post_type'] != False :
			values['test_type_char']  = values['test_post_type'] 
		elif 'test_type' in values  and values['test_type'] != False :
			values['test_type_char']  = values['test_type'] 

		if 'module_id' in values :
			if 'learner_line' in values :
				for x in values['learner_line'] :
					learner = self.pool.get('learner.info').browse(cr,uid,x[2]['learner_id'])
					learner_mod_obj = self.pool.get('enroll.module.line')
					learner_mod_obj_ids = learner_mod_obj.search(cr,uid,[('learner_info_id','=',learner.id)])
					lear_module_ids = []
					for y in learner_mod_obj.browse(cr,uid,learner_mod_obj_ids):
						lear_module_ids.append(y['module_id'].id)
					
					if values['module_id'] not in lear_module_ids:
						raise osv.except_osv(_('Error!'),_("Learner Module Does Not Match Selected Module - "+str(learner.name)))
			
			else :
				test_info_obj = self.browse(cr,uid,ids)
				for x in test_info_obj :
						for y in x['learner_line'] :
							learner_mod_obj = self.pool.get('enroll.module.line')
							learner_mod_obj_ids = learner_mod_obj.search(cr,uid,[('learner_info_id','=',y['learner_id'].id)])
							lear_module_ids = []
							for z in learner_mod_obj.browse(cr,uid,learner_mod_obj_ids):
								lear_module_ids.append(z['module_id'].id)
							if z['module_id'].id not in lear_module_ids :
									raise osv.except_osv(_('Error!'),_("Learner Module Does Not Match Selected Module - "+str(y['learner_id'].name)))
		

			
		if 'class_info' in values and values['class_info'] != False :
			class_obj =self.pool.get("class.info").browse(cr,uid,values['class_info'])
			learner_obj = self.pool.get('test.learner')
			learner_ids = learner_obj.search(cr,uid,[('learner_mod_id' ,'=',ids[0])])
			for x in learner_ids :
				learner_obj.write(cr,uid,x,{'class_code':class_obj.class_code})

		module_id = super(test_info, self).write(cr, uid, ids,values, context=context)
		return module_id

	
	
	
	def on_change_test_definition(self, cr, uid, ids, test,context):
		code = ""
		module_info  = {} 
		module_id_array  = []
		test_obj = self.pool.get('test')
		test_obj_id = test_obj.browse(cr, uid, test) 
		code = test_obj_id.test_code
		for y in test_obj_id.test_mod_line or [] :
			module_id_array.append(y.module_id.id)
			
		return {'domain':{'module_id':[('id','in',module_id_array)]},'value': {'test_code':code,'name':test_obj_id.name,'capacity':test_obj_id.test_max_Pax,'status':test_obj_id.test_status,'module_id':False}}
	
	def onchange_dates(self, cr, uid, ids, start_date, duration=False, end_date=False,context=None):
		value = {}
		if not start_date:
			return value
		if not end_date and not duration:
			duration = 1.00
			value['duration'] = duration
		start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
		if not end_date:
			end = start + timedelta(hours=duration)
			value['end_date'] = end.strftime("%Y-%m-%d %H:%M:%S")
		return {'value': value}

	def on_change_module_id(self, cr, uid, ids, module_id,test_name,context):
		test_obj = self.pool.get('test')
		test_obj_id = test_obj.browse(cr, uid, test_name) 
		type_id = -1
		for y in test_obj_id.test_mod_line or [] :
			if y.module_id.id  == module_id :
				if y.pre_test and y.post_test :
					type_id = 1
				elif y.pre_test :
					type_id = 2
				elif y.post_test :
					type_id = 3
		
		module_obj = self.pool.get('cs.module').browse(cr, uid, module_id)
		module_id
		learners = [] 
		learner_ids = self.pool.get('enroll.module.line').search(cr,uid,[('module_id','=',module_id)])
		for j in self.pool.get('enroll.module.line').browse(cr,uid,learner_ids):
			learners.append(j['learner_info_id'].id)
		
		return {'value': {'module_code': module_obj.module_code,'no_of_hrs':module_obj.module_duration,'test_type_id':type_id,'test_type':False,'test_pre_type':False,'test_post_type':False,}}

	def on_change_location_id(self, cr, uid, ids, location_id):
		return {'value': {'room_id': False}}
	
	
test_info()

class test_modality(osv.osv):
	_name ='test.modality'
	_description ="Trainer Learner Tab"
	_columns = {
	'test_modality_id' : fields.integer('Id',size=20,readonly=1),
	'master_modality':fields.many2one('test.master.modality', 'Modality', ondelete='cascade', help='Modality', select=True, required=True),
	'active':fields.boolean('Active'),

	}
	
test_modality()

class test_matser_modality(osv.osv):
	def _check_unique_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
		
	_name ='test.master.modality'
	_description ="Trainer Learner Tab"
	_columns = {
		'name':fields.char('Test Modality'),
	}
	_constraints = [(_check_unique_name, 'Error: Modality Already Exists', ['name'])]
test_matser_modality()


class test_learner(osv.osv):
	def _get_learner_id(self, cr, uid, ids, field_name, arg, context=None):
		_logger.info("Hello There")
		return result
	def view_learner_modality(self, cr, uid, ids, context=None): 
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'learner_modality_form')
		view_id = view_ref and view_ref[1] or False,
		ctx = dict(context)
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		ctx.update({'class_id': ids[0],'active_learner':self_obj.learner_id.id})
	
		return {
			'type': 'ir.actions.act_window',
			'name': 'Modality Form',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': view_id,
			'res_model': 'test.learner',
			'res_id':ids[0],
			'nodestroy': True,
			'target':'new',
			'context': ctx,
		}
	
	def save_modality(self, cr, uid, ids, context=None): 
		obj = self.browse(cr,uid,ids)
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'test_listing_page_form')
		view_id = view_ref and view_ref[1] or False,
		
		return {
			'type': 'ir.actions.act_window',
			'name': 'Test',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': False,
			'res_model': 'test.info',
			'res_id':obj[0]['learner_mod_id'].id,
			'nodestroy': True,
			'target':'current',
			'context': context,
		}
	
	def cancel_modality(self, cr, uid, ids, context=None): 
		obj = self.browse(cr,uid,ids)
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'test_listing_page_form')
		view_id = view_ref and view_ref[1] or False,
		
		return {
			'type': 'ir.actions.act_window',
			'name': 'Test',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': False,
			'res_model': 'test.info',
			'res_id':obj[0]['learner_mod_id'].id,
			'nodestroy': True,
			'target':'current',
			'context': context,
		}
	
	 
	def _check_unique_learner(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.learner_mod_id == self_obj.learner_mod_id and x.learner_id == self_obj.learner_id:
						return False
		return True
	def on_change_learner_id(self, cr, uid, ids, learner_id,context):
		module_obj = self.pool.get('learner.info').browse(cr, uid, learner_id)
		class_code = "N/A"
		if context.get('class_id') != False:
			class_obj = self.pool.get('class.info').browse(cr, uid, context.get('class_id'))
			class_code = class_obj.class_code
		return {'value': {'learner_nric': module_obj.learner_nric,'class_code':class_code,'compliance_code':context.get('test_code')}}
		
	def create(self,cr, uid, values, context=None):
		id = super(test_learner, self).create(cr, uid, values, context=context)
		self.pool.get('test.scores').create(cr, uid,{'test_scores_id':values['learner_mod_id'],'learner_id':values['learner_id'],'learner_nric':values['learner_nric']}, context=context)
		return id
		
	def write(self,cr, uid, ids, values, context=None):
		id = super(test_learner, self).write(cr, uid, ids,values, context=context)
		return id

	def unlink(self, cr, uid, ids, context=None):
		learner_obj = self.browse(cr, uid, ids)
		learner_id = learner_obj[0]['learner_id']
		score_leraner_id = self.pool.get('test.scores').search(cr, uid, [('learner_id', '=', learner_id.id)])
		self.pool.get('test.scores').unlink(cr, uid, score_leraner_id, context=context)
		return super(test_learner, self).unlink(cr, uid, ids, context=context)
	
	
	_name ='test.learner'
	_description ="Learner Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'learner_mod_id': fields.many2one('test.info', 'Test', ondelete='cascade', help='Class', select=True),
	'learner_id':fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner', select=True),
	'learner_nric': fields.related('learner_id','learner_nric',type="char",relation="learner.info",string="Learner NRIC", readonly=1,),
	'class_code':fields.char('Class Code',size=25),
	'compliance_code':fields.char('Compliance Code',size=25),
	'level':fields.char('Level',size=25),
	'attendance':fields.boolean('Attendance'),
	'reading':fields.boolean('Reading'),
	'listening':fields.boolean('Listening'),
	'speaking':fields.boolean('Speaking'),
	'writing':fields.boolean('Writing'),
	'numeracy':fields.boolean('Numeracy'),
	}
	_constraints = [(_check_unique_learner,'Error: Learner Already Exists', ['learner_id'])]
	
	
test_learner()

class test_scores(osv.osv):
	def view_scores(self, cr, uid, ids, context=None): 
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'scores_form')
		view_id = view_ref and view_ref[1] or False,
		ctx = dict(context)
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		ctx.update({'class_id': ids[0],'active_learner':self_obj.learner_id.id})
	
		return {
			'type': 'ir.actions.act_window',
			'name': 'Scores Form',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': view_id,
			'res_model': 'test.scores',
			'res_id':ids[0],
			'nodestroy': True,
			'target':'new',
			'context': ctx,
		}
	
	def save_scores(self, cr, uid, ids, context=None): 
		obj = self.browse(cr,uid,ids)
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'test_listing_page_form')
		view_id = view_ref and view_ref[1] or False,
		
		return {
			'type': 'ir.actions.act_window',
			'name': 'Test',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': False,
			'res_model': 'test.info',
			'res_id':obj[0]['test_scores_id'].id,
			'nodestroy': True,
			'target':'current',
			'context': context,
		}
	
	def cancel_scores(self, cr, uid, ids, context=None): 
		obj = self.browse(cr,uid,ids)
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'test_listing_page_form')
		view_id = view_ref and view_ref[1] or False,
		
		return {
			'type': 'ir.actions.act_window',
			'name': 'Test',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': False,
			'res_model': 'test.info',
			'res_id':obj[0]['test_scores_id'].id,
			'nodestroy': True,
			'target':'current',
			'context': context,
		}
		
	_name ='test.scores'
	_description ="Test Scores Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'test_scores_id': fields.many2one('test.info', 'Test', ondelete='cascade', help='Class', select=True),
	'learner_id':fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner', select=True),
	'learner_nric': fields.related('learner_id','learner_nric',type="char",relation="learner.info",string="Learner NRIC", readonly=1,),
	'compr':fields.char('Compr',size=25),
	'conv':fields.char('Conv',size=25),
	'r_level':fields.integer('Reading(Level)',size=1),
	'r_scores':fields.integer('Readng(Scores)',size=2),
	'l_level':fields.integer('Listening(Level)',size=1),
	'l_scores':fields.integer('Listening(Scores)',size=2),
	's_level':fields.integer('Speaking(Level)',size=1),
	's_scores':fields.integer('Speaking(Soures)',size=2),
	'w_level':fields.integer('Writing(Level)',size=1),
	'w_scores':fields.integer('Writing(Scores)',size=2),
	'w_outcome':fields.char('W(Outcomes)',size=20),
	'n_level':fields.integer('Numeracy(Level)',size=1),
	'n_scores':fields.integer('Numeracy(Scores)',size=2),
	'n_outcome':fields.char('N(Outcomes)',size=20),
	
	}
test_scores()