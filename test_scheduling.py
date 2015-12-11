from openerp import addons
from datetime import datetime, timedelta, date
from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from lxml import etree
from collections import namedtuple
from openerp.osv import fields, osv
from openerp.tools.translate import _

import logging
import pytz
import re
import time
from openerp import tools
_logger = logging.getLogger(__name__)

global dupliacte_found
dupliacte_found = False

global dupliacte_mod_found
dupliacte_mod_found = False

global dupliacte_found_create
dupliacte_found_create = False

global dupliacte_mod_found_create
dupliacte_mod_found_create = False


class test_info(osv.osv):

	
	'''def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		_logger.info("Value in read %s",ids)
		res = super(test_info, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res'''
		
	def default_get(self, cr, uid, fields, context=None):
		_logger.info("Calleing Default %s",fields)
		data = super(test_info, self).default_get(cr, uid, fields, context=context)
		invoice_lines = []
		_logger.info("Calleing Default %s",fields)
		modality_ids = self.pool.get('test.master.modality').search(cr, uid, [],limit=5)
		for p in self.pool.get('test.master.modality').browse(cr, uid, modality_ids):
			invoice_lines.append((0,0,{'master_modality':p.id,}))
		data['test_modality'] = invoice_lines
		return data
		
	def _calculate_total_learners(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = line.learner_line or []
			_logger.info("total id %s",mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
		return res
	
#Test Status
	def _test_status_display_1(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['test_status']
		return res
		
	def _test_status_display_2(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['test_status']
		return res
		
	def _test_status_display_3(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['test_status']
		return res
		
	def _test_status_display_4(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['test_status']
		return res
		
	def _test_status_display_5(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['test_status']
		return res
		
	def _check_modality(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.min_modality > self_obj.max_modality:
				raise osv.except_osv(_('Error:'),_('Max Modality should be greater')%(self_obj))
		return True

	_name = "test.info"
	_description = "This table is for keeping Test Schedules"
	_columns = {
		'test_id': fields.integer('Id',size=20),
		's_no': fields.integer('S_No', size=100),
		'parent_id': fields.integer('Parent Id',size=20),
		'name': fields.char('Test Name', size=100,required=True, select=True),
		'test_code': fields.char('Test Code', size=999),
		'test_status': fields.selection((('Open','Open'),('Closed','Closed'),('Completed','Completed'),('Cancelled','Cancelled'),('Postponed','Postponed')),'Status',required=True, select=True, help='Status show wheather the Program is on going.'),
		'test_type_id':fields.integer('Test Type Id'),
		'test_pre_type':fields.selection((('Pre Test','Pre Test'),),'Test Type', ),
		'test_type':fields.selection((('Pre Test','Pre Test'),('Post Test','Post Test')),'Test Type', ),
		'test_post_type':fields.selection((('Post Test','Post Test'),),'Test Type', ),
		'test_type_char':fields.char('Test Type'),
		'class_info': fields.many2one('class.info', 'Select Class',  ondelete='cascade', help='Module', select=True, ),
		'test_code_compliance': fields.char('Test Code (Compliance)', size=20),
		'module_ids': fields.char('Module_Ids'),
		'module_code': fields.char('Module Code', size=20, readonly=1),
		'start_date': fields.datetime('Start Date', required=True),
		'end_date': fields.datetime('End Date'),
		'duration': fields.float('Duration(Hrs)'),
		'location_id':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'room_id':fields.many2one('room', 'Room', ondelete='cascade', help='Room', select=True, required=True),
		'test_modality': fields.one2many('test.modality','test_modality_id', 'Test Modality'),
		'delivery_mode': fields.selection((('English','English'),('Singli','Singli'),('Malyi','Malyi')),'Delivery Mode'),
		'learner_line': fields.one2many('test.learner', 'learner_mod_id', 'Learner Lines', select=True, required=True),
		'test_scores': fields.one2many('test.scores','test_scores_id','Test Scores'),
		'actual_number':fields.function(_calculate_total_learners, relation="test.info",readonly=1,string='No. Learners',type='integer'),
		't_status':fields.char('Status'),
		'max_modality': fields.integer('Max Modality', size=1),
		'min_modality': fields.integer('Min Modality', size=1),
		'max_people': fields.integer('Max People', size=3),
		'test_status_display_1': fields.function(_test_status_display_1, readonly=1, type='char'),
		'test_status_display_2': fields.function(_test_status_display_2, readonly=1, type='char'),
		'test_status_display_3': fields.function(_test_status_display_3, readonly=1, type='char'),
		'test_status_display_4': fields.function(_test_status_display_4, readonly=1, type='char'),
		'test_status_display_5': fields.function(_test_status_display_5, readonly=1, type='char'),
		'date1': fields.date('Date Created', readonly='True'),
		'date2': fields.date('Date Created', readonly='True'),
		'date3': fields.date('Date Created', readonly='True'),
		'date4': fields.date('Date Created', readonly='True'),
		'date5': fields.date('Date Created', readonly='True'),
	}
	_defaults = { 
		't_status': 'Draft',
		'date1': fields.date.context_today,
		'date2': fields.date.context_today,
		'date3': fields.date.context_today,
		'date4': fields.date.context_today,
		'date5': fields.date.context_today,
	} 
	_constraints = [(_check_modality, 'Error: Max Modality should be greater', ['Modality'])]

	def create(self,cr, uid, values, context=None):
		values['t_status'] = 'Edit'
		if 'duration' in values and values['duration'] < 0:
				raise osv.except_osv(_('Error!'),_("Duration cannot be negative value"))
		
		t1start= datetime.strptime(values['start_date'],"%Y-%m-%d %H:%M:%S")
		t1end = datetime.strptime(values['end_date'],"%Y-%m-%d %H:%M:%S")
		
		if datetime.strptime(values['start_date'],"%Y-%m-%d %H:%M:%S")  < datetime.now() :
			raise osv.except_osv(_('Error!'),_("Start Date cannot be in past"))
		
		Range = namedtuple('Range', ['start', 'end'])
		r1 = Range(start=t1start, end=t1end)
	
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			r2 = Range(start=datetime.strptime(x['start_date'], "%Y-%m-%d %H:%M:%S"), end=datetime.strptime(x['end_date'], "%Y-%m-%d %H:%M:%S"))
			latest_start = max(r1.start, r2.start)
			earliest_end = min(r1.end, r2.end)
			overlap = (earliest_end - latest_start)
			if overlap.days == 0 and x.room_id.id == values['room_id']:
				raise osv.except_osv(_('Error!'),_("Room Conflicts with other test schedule"))
			#if overlap.days == 0 and x.learner_line.id == values['learner_line']:
				#raise osv.except_osv(_('Error!'),_("Learner Conflicts with other test schedule"))

		holiday = self.pool.get('holiday')
		holiday_obj_id = holiday.search(cr, uid, [('year', '=', datetime.now().year)])
		if len(holiday_obj_id) > 0 :
			holiday_obj = holiday.browse(cr,uid,holiday_obj_id,context)
			holiday_list = []
			holiday_line = self.pool.get('holiday.line')
			holiday_line_obj_id = holiday_line.search(cr, uid, [('holiday_line_id', '=',holiday_obj[0]['id'])])
			for holiday_line_obj in holiday_line.browse(cr,uid,holiday_line_obj_id,context) :
				t2start =datetime.strptime(holiday_line_obj['date_start'],"%Y-%m-%d %H:%M:%S")
				t2end =datetime.strptime(holiday_line_obj['date_end'],"%Y-%m-%d %H:%M:%S")
				if (t1start <= t2start <= t2end <= t1end):
					raise osv.except_osv(_('Error!'),_("Holiday/Closure Found - "+holiday_line_obj['description']))
				elif (t1start <= t2start <= t1end):
					raise osv.except_osv(_('Error!'),_("Holiday/Closure Found - "+holiday_line_obj['description']))
				elif (t1start <= t2end <= t1end):
					raise osv.except_osv(_('Error!'),_("Holiday/Closure Found - "+holiday_line_obj['description']))
				elif (t2start <= t1start <= t1end <= t2end):
					raise osv.except_osv(_('Error!'),_("Holiday/Closure Found - "+holiday_line_obj['description']))
	
		
		if 'test_pre_type' in values  and values['test_pre_type'] != False :
			values['test_type_char']  = values['test_pre_type'] 
		elif 'test_post_type' in values  and values['test_post_type'] != False :
			values['test_type_char']  = values['test_post_type'] 
		elif 'test_type' in values  and values['test_type'] != False :
			values['test_type_char']  = values['test_type']
			
		global dupliacte_found_create
		dupliacte_found_create = False	
		
		global dupliacte_mod_found_create
		dupliacte_mod_found_create = False
			
		if 'learner_line' in values :
			if values['learner_line']  > 1:
				ids_test_lear = self.pool.get('test.learner').search(cr,1,[])
				table_ids = []
				new_table_ids = []
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('test.learner').browse(cr,1,ids_test_lear):
					if dd.learner_mod_id.id == True:
						table_ids.append(dd.learner_id.id)	
				for x in values['learner_line'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('test.learner').browse(cr,uid,x[1])
						deleted_ids.append(obj.learner_id.id)
					elif x[0] == 0 and 'learner_id' in x[2]:
						added_ids.append(x[2]['learner_id'])
						if x[2]['learner_id'] in table_ids :
							new_table_ids.append(dd.learner_id.id)
					elif x[0] == 1  and 'learner_id' in x[2]:
						updated_ids.append(x[2]['learner_id'])

				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_found_create
					dupliacte_found_create = True
				else:

					for c in added_ids :
						if (c in new_table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_found_create
							dupliacte_found_create = True

					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_found_create
						dupliacte_found_create = True
					else :
						found = 0
						for u in updated_ids :
							if u in new_table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_found_create
							dupliacte_found_create = True
							
		if 'test_modality' in values :
			if values['test_modality']  > 1:
				ids_test_lear = self.pool.get('test.modality').search(cr,1,[])
				table_ids = []
				new_table_ids = []
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('test.modality').browse(cr,1,ids_test_lear):
						table_ids.append(dd.master_modality.id)	
				for x in values['test_modality'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('test.modality').browse(cr,uid,x[1])
						deleted_ids.append(obj.master_modality.id)
					elif x[0] == 0 and 'master_modality' in x[2]:
						added_ids.append(x[2]['master_modality'])
						if x[2]['master_modality'] in table_ids :
							new_table_ids.append(dd.master_modality.id)
					elif x[0] == 1  and 'master_modality' in x[2]:
						updated_ids.append(x[2]['master_modality'])

				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_mod_found_create
					dupliacte_mod_found_create = True
				else:

					for c in added_ids :
						if (c in new_table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_mod_found_create
							dupliacte_mod_found_create = True

					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_mod_found_create
						dupliacte_mod_found_create = True
					else :
						found = 0
						for u in updated_ids :
							if u in new_table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_mod_found_create
							dupliacte_mod_found_create = True
		
		
		_logger.info("Create Values %s",values)
		module_id = super(test_info, self).create(cr, uid, values, context=context)
		return module_id

	def write(self,cr, uid, ids, values, context=None):
		_logger.info("write write Called %s",values)
		if 'duration' in values and values['duration'] < 0:
			raise osv.except_osv(_('Error!'),_("Duration cannot be negative value"))
			
			
		if 'room_id' in values :
			Range = namedtuple('Range', ['start', 'end'])
			test_obj = self.browse(cr,uid,ids[0])
			if 'start_date' in values :
				t1start = values['start_date']
			else :
				t1start = test_obj['start_date']
			
			if 'end_date' in values :
				t1end = values['end_date']
			else :
				t1end = test_obj['end_date']
				
				
			r1 = Range(start=datetime.strptime(t1start, "%Y-%m-%d %H:%M:%S"), end=datetime.strptime(t1end, "%Y-%m-%d %H:%M:%S"))
	
			sr_ids = self.search(cr, 1 ,[], context=context)
			for x in self.browse(cr, uid, sr_ids, context=context):
				r2 = Range(start=datetime.strptime(x['start_date'], "%Y-%m-%d %H:%M:%S"), end=datetime.strptime(x['end_date'], "%Y-%m-%d %H:%M:%S"))
				latest_start = max(r1.start, r2.start)
				earliest_end = min(r1.end, r2.end)
				overlap = (earliest_end - latest_start)
				if overlap.days == 0 and x.room_id.id == values['room_id']:
					raise osv.except_osv(_('Error!'),_("Room Conflicts with other test schedule"))
			
				
		if 'start_date' in values :
			t1start= datetime.strptime(values['start_date'],"%Y-%m-%d %H:%M:%S")
			if t1start < datetime.now() :
				raise osv.except_osv(_('Error!'),_("Start Date cannot be in past"))
			
			if 'duration' in values :
				duration = values['duration']
			else :
				test_info_obj = self.browse(cr,uid,ids[0])
				duration = test_info_obj['duration']
			
						
			t1end = t1start + timedelta(hours=duration)
			Range = namedtuple('Range', ['start', 'end'])
		
			r1 = Range(start=t1start, end=t1end)
	
			sr_ids = self.search(cr, 1 ,[], context=context)
			for x in self.browse(cr, uid, sr_ids, context=context):
				r2 = Range(start=datetime.strptime(x['start_date'], "%Y-%m-%d %H:%M:%S"), end=datetime.strptime(x['end_date'], "%Y-%m-%d %H:%M:%S"))
				latest_start = max(r1.start, r2.start)
				earliest_end = min(r1.end, r2.end)
				overlap = (earliest_end - latest_start)
				if overlap.days == 0 and x.room_id.id == test_info_obj['room_id'].id:
					raise osv.except_osv(_('Error!'),_("Room Conflicts with other test schedule"))
			
			holiday = self.pool.get('holiday')
			holiday_obj_id = holiday.search(cr, uid, [('year', '=', datetime.now().year)])
			if len(holiday_obj_id) > 0 :
				holiday_obj = holiday.browse(cr,uid,holiday_obj_id,context)
				holiday_list = []
				holiday_line = self.pool.get('holiday.line')
				holiday_line_obj_id = holiday_line.search(cr, uid, [('holiday_line_id', '=',holiday_obj[0]['id'])])
				for holiday_line_obj in holiday_line.browse(cr,uid,holiday_line_obj_id,context) :
					t2start =datetime.strptime(holiday_line_obj['date_start'],"%Y-%m-%d %H:%M:%S")
					t2end =datetime.strptime(holiday_line_obj['date_end'],"%Y-%m-%d %H:%M:%S")
					if (t1start <= t2start <= t2end <= t1end):
						raise osv.except_osv(_('Error!'),_("Holiday/Closure Found - "+holiday_line_obj['description']))
					elif (t1start <= t2start <= t1end):
						raise osv.except_osv(_('Error!'),_("Holiday/Closure Found - "+holiday_line_obj['description']))
					elif (t1start <= t2end <= t1end):
						raise osv.except_osv(_('Error!'),_("Holiday/Closure Found - "+holiday_line_obj['description']))
					elif (t2start <= t1start <= t1end <= t2end):
						raise osv.except_osv(_('Error!'),_("Holiday/Closure Found - "+holiday_line_obj['description']))
		
		if 'test_pre_type' in values  and values['test_pre_type'] != False :
			values['test_type_char']  = values['test_pre_type'] 
		elif 'test_post_type' in values  and values['test_post_type'] != False :
			values['test_type_char']  = values['test_post_type'] 
		elif 'test_type' in values  and values['test_type'] != False :
			values['test_type_char']  = values['test_type'] 

		if 'class_info' in values and values['class_info'] != False :
			class_obj =self.pool.get("class.info").browse(cr,uid,values['class_info'])
			learner_obj = self.pool.get('test.learner')
			learner_ids = learner_obj.search(cr,uid,[('learner_mod_id' ,'=',ids[0])])
			for x in learner_ids :
				learner_obj.write(cr,uid,x,{'class_code':class_obj.class_code})
		global dupliacte_found
		dupliacte_found = False	
		
		global dupliacte_mod_found
		dupliacte_mod_found = False	
		
		if 'learner_line' in values :
			if values['learner_line']  > 1:
				ids_test_lear = self.pool.get('test.learner').search(cr,1,[])
				table_ids = [] 
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('test.learner').browse(cr,1,ids_test_lear):
					if dd.learner_mod_id.id == ids[0]:
						table_ids.append(dd.learner_id.id)
				for x in values['learner_line'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('test.learner').browse(cr,uid,x[1])
						deleted_ids.append(obj.learner_id.id)
					elif x[0] == 0 and 'learner_id' in x[2]:
						added_ids.append(x[2]['learner_id'])
					elif x[0] == 1  and 'learner_id' in x[2]:
						updated_ids.append(x[2]['learner_id'])
				'''create check'''		
				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_found
					dupliacte_found = True
				else:
					'''check create in table'''
					for c in added_ids :
						if (c in table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_found
							dupliacte_found = True
					'''check for update ids '''
					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_found
						dupliacte_found = True
					else :
						found = 0
						for u in updated_ids :
							if u in table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_found
							dupliacte_found = True
		if 'test_modality' in values :
			if values['test_modality']  > 1:
				ids_test_lear = self.pool.get('test.modality').search(cr,1,[])
				table_ids = [] 
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('test.modality').browse(cr,1,ids_test_lear):
					if dd.test_modality_id.id == ids[0]:
						table_ids.append(dd.master_modality.id)
				for x in values['test_modality'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('test.modality').browse(cr,uid,x[1])
						deleted_ids.append(obj.master_modality.id)
					elif x[0] == 0 and 'master_modality' in x[2]:
						added_ids.append(x[2]['master_modality'])
					elif x[0] == 1  and 'master_modality' in x[2]:
						updated_ids.append(x[2]['master_modality'])
				'''create check'''		
				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_mod_found
					dupliacte_mod_found = True
				else:
					'''check create in table'''
					for c in added_ids :
						if (c in table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_mod_found
							dupliacte_mod_found = True
					'''check for update ids '''
					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_mod_found
						dupliacte_mod_found = True
					else :
						found = 0
						for u in updated_ids :
							if u in table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_mod_found
							dupliacte_mod_found = True


								
			_logger.info("dupliacte_found %s",dupliacte_found)	
		module_id = super(test_info, self).write(cr, uid, ids,values, context=context)
		return module_id
	
	'''def on_change_test_definition(self, cr, uid, ids, test,context):
		code = ""
		module_info  = {} 
		module_id_array  = []
		test_obj = self.pool.get('test')
		test_obj_id = test_obj.browse(cr, uid, test) 
		code = test_obj_id.test_code
		for y in test_obj_id.test_mod_line or [] :
			module_id_array.append(y.module_id.id)
			
		return {'domain':{'module_id':[('id','in',module_id_array)]},'value': {'test_code':code,'name':test_obj_id.name,'capacity':test_obj_id.test_max_Pax,'status':test_obj_id.test_status,'module_id':False}}'''
	
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
		if module_id != False :
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
			
			return {'value': {'module_code': module_obj.module_code,'no_of_hrs':module_obj.module_duration,'test_type_id':type_id,'test_type':False,'test_pre_type':False,'test_post_type':False,}}
		else:
			return{}

	def on_change_location_id(self, cr, uid, ids, location_id):
		return {'value': {'room_id': False}}
	
	
test_info()

class test_modality(osv.osv):
	def _check_unique_test_modality(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.test_modality_id == self_obj.test_modality_id and x.master_modality == self_obj.master_modality:
						return False
		return True
	
	
	_name ='test.modality'
	_description ="Trainer Learner Tab"
	_columns = {
	'test_modality_id' :  fields.many2one('test.info', 'Test', ondelete='cascade', help='Test', select=True),
	'master_modality':fields.many2one('test.master.modality', 'Modality', ondelete='cascade', help='Modality', select=True, required=True),	
	'm_active':fields.boolean('Active'),

	}
	_constraints = [(_check_unique_test_modality, 'Error: Item Already Exists', ['master_modality'])]
	
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
		if dupliacte_found == True:
			return False
		elif dupliacte_found_create == True:
			return False
		else :
			return True
			
	def on_change_learner_id(self, cr, uid, ids, learner_id,context):
		module_obj = self.pool.get('learner.info').browse(cr, uid, learner_id)
		class_code = "N/A"
		if context.get('class_id') != False:
			class_obj = self.pool.get('class.info').browse(cr, uid, context.get('class_id'))
			class_code = class_obj.class_code
		return {'value': {'learner_nric': module_obj.learner_nric,'class_code':class_code,'compliance_code':context.get('test_code')}}
	
	def _test_hist(self, cr, uid, sd, mn, cc, values, context=None):
			obj_res_hist = self.pool.get('test.history.module')
			#raise osv.except_osv(_('Error!'),_("Duration cannot be negative value %s %s %s %s")%(ed, sd, mn, cc,))
			for ch in values:
				vals = {
					#'test_type':ed,
					'test_id':ch['learner_id'],
					'test_code':cc,
					'test_date': sd,
					'test_status':mn
				}
				obj_res_hist.create(cr, uid, vals, context=context)
			return True
			
	def _payment_test(self, cr, uid, mon, csc, mc, values, context=None):
			obj_res_hist = self.pool.get('payment.test')
			
			for ch in values:
			
				sql="select program_learner from learner_info where id = %s " % (ch['learner_id'])
				cr.execute(sql)
				itm = cr.fetchall()
				for s in itm:
					pna = s[0]
				
				vals = {
					'program_name': pna,
					'pay_id':ch['learner_id'],
					'module_name': mon,
					'test_name':csc,
					'test_cost': mc,
				}
				obj_res_hist.create(cr, uid, vals, context=context)
			return True
	
	def create(self,cr, uid, values, context=None):
		_logger.info("create Called %s",values)
		id = super(test_learner, self).create(cr, uid, values, context=context)
		self.pool.get('test.scores').create(cr, uid,{'test_scores_id':values['learner_mod_id'],'learner_id':values['learner_id'],'learner_nric':values['learner_nric']}, context=context)
		#Masih
		test_id = values['learner_mod_id']
		class_info_obj = self.pool.get('test.info')
		class_info_obj_id = class_info_obj.browse(cr,uid,test_id)
		#ed = class_info_obj_id.name
		sd = class_info_obj_id.start_date
		mn = class_info_obj_id.test_status
		cc = class_info_obj_id.test_code
		#Supreeth
		test_id = values['learner_mod_id']
		class_info_obj = self.pool.get('test.info')
		class_info_obj_id = class_info_obj.browse(cr,uid,test_id)
		mon = values['module_id']
		mc = values['modality_cost']
		csc = class_info_obj_id.test_code
		#raise osv.except_osv(_('Error!'),_("Duration cannot be negative value %s")%(class_info_obj_id.test_code))
		#self._create_hist(cr, uid, ed, sd, mn, cc,[values], context=context)
		#Masih
		self._test_hist(cr, uid, sd, mn, cc,[values], context=context)
		self._payment_test(cr, uid, mon, csc, mc,[values], context=context)
		return id
		return id
		
	def write(self,cr, uid, ids, values, context=None):
		_logger.info("write Called %s",ids)
		learner_obj = self.browse(cr,uid,ids[0])
		if 'learner_id' in values :
			scores_obj = self.pool.get('test.scores')
			scores_obj_id = scores_obj.search(cr,uid,[('learner_id','=',learner_obj['learner_id'].id)])
			scores_obj.write(cr,uid,scores_obj_id,values)
		#Masih
		test_id = values['learner_mod_id']
		class_info_obj = self.pool.get('test.info')
		class_info_obj_id = class_info_obj.browse(cr,uid,test_id)
		#ed = class_info_obj_id.name
		sd = class_info_obj_id.start_date
		mn = class_info_obj_id.test_status
		cc = class_info_obj_id.test_code
		id = super(test_learner, self).write(cr, uid, ids,values, context=context)
		#Supreeth
		test_id = values['learner_mod_id']
		class_info_obj = self.pool.get('test.info')
		class_info_obj_id = class_info_obj.browse(cr,uid,test_id)
		csc = class_info_obj_id.test_code
		mon = values['module_id']
		mc = values['modality_cost']
		self._test_hist(cr, uid, sd, mn, cc,[values], context=context)
		self._payment_test(cr, uid, mon, csc, mc,[values], context=context)
		return id
		return id

	def unlink(self, cr, uid, ids, context=None):
		_logger.info("Unlink Called %s",ids)
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
	'learner_non_nric': fields.related('learner_id','learner_non_nric',type="char",relation="learner.info",string="Learner Non-NRIC", readonly=1),
	'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True, required=True),
	'modality':fields.many2one('master.modality', 'Modality', ondelete='cascade', help='Description', required=True),
	'modality_cost': fields.related('modality', 'cost', type="float",relation="master.modality",string="Cost", readonly=1,),
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
		
	def _test_scores(self, cr, uid, values, context=None):
		obj_res_hist = self.pool.get('test.score.module')
		#raise osv.except_osv(_('Error!'),_("Duration cannot be negative value %s %s %s %s")%(ed, sd, mn, cc,))
		for ch in values:
			raise osv.except_osv(_('Error!'),_("Duration cannot be negative value %s ")%(ch['compr']))
			sql="select test_compre, test_conv, r_level, r_score, l_level, l_score, s_level, s_score, w_level, w_score, w_outcomes, n_level, n_score, w_outcome1, from test_score_module where id = %s " % (ch['learner_id'])
			cr.execute(sql)
			itm = cr.fetchall()
			cc=""
			co=""
			rl=""
			rs=""
			ll=""
			ls=""
			sl=""
			ss=""
			wl=""
			ws=""
			wo=""
			nl=""
			ns=""
			woe=""
			
			for s in itm:
				cc = s[0]
				co = s[1]
				rl = s[2]
				rs = s[3]
				ll = s[4]
				ls = s[5]
				sl = s[6]
				ss = s[7]
				wl = s[8]
				ws = s[9]
				wo = s[10]
				nl = s[11]
				ns = s[12]
				woe = s[13]
				
			
			vals = {
				'test_compre': cc,
				'test_conv': co,
				'r_level': rl,
				'r_score': rs,
				'l_level':ll,
				'l_score':ls,
				's_level':sl,
				's_score':ss,
				'w_level':wl,
				'w_score':ws,
				'w_outcomes':wo,
				'n_level':nl,
				'n_score':ns,
				'w_outcome1':woe,
				'test_score_type':ed,
				'test_score_id':ch['learner_id'],
				'test_sc_date': sd,
				'test_sc_code':mn
			}
			obj_res_hist.create(cr, uid, vals, context=context)
		return True
	
	def write(self,cr, uid, ids, values, context=None):
		if 'r_scores' in values and values['r_scores'] < 0:
			raise osv.except_osv(_('Error!'),_("Scores - Cannot be negative"))
		if 'l_scores' in values and values['l_scores'] < 0:
			raise osv.except_osv(_('Error!'),_("Scores - Cannot be negative"))
		if 's_scores' in values and values['s_scores'] < 0:
			raise osv.except_osv(_('Error!'),_("Scores - Cannot be negative"))
		if 'w_scores' in values and values['w_scores'] < 0:
			raise osv.except_osv(_('Error!'),_("Scores - Cannot be negative"))
		if 'n_scores' in values and values['n_scores'] < 0:
			raise osv.except_osv(_('Error!'),_("Scores - Cannot be negative"))
		if 'compr' in values and values['compr'] < 0:
			raise osv.except_osv(_('Error!'),_("Scores - Cannot be negative"))
		if 'conv' in values and values['conv'] < 0:
			raise osv.except_osv(_('Error!'),_("Scores - Cannot be negative"))

		id = super(test_scores, self).write(cr, uid, ids,values, context=context)
		#self.pool.get('test.scores').create(cr, uid,{'test_scores_id':values['learner_mod_id'],'learner_id':values['learner_id'],'learner_nric':values['learner_nric']}, context=context)
		id = super(test_scores, self).write(cr, uid, ids,values, context=context)
		
		ts = self.browse(cr, uid, ids)
		for i in ts:
			lid = i.learner_id.id
			cc = values['compr']
			co = values['conv']
			rl = values['r_level']
			rs = values['r_scores']
			ll = values['l_level']
			ls = values['l_scores']
			sl = values['s_level']
			ss = values['s_scores']
			wl = values['w_level']
			ws = values['w_scores']
			#wo = values['w_outcome']
			nl = values['n_level']
			ns = values['n_scores']
			#woe = values['n_outcome']
			
			#raise osv.except_osv(_('Error!'),_("fffgfdfdf %s")%(ddd))
			
		obj_res_hist = self.pool.get('test.score.module')
		sql="select ti.start_date, t.id, ti.test_code  \
			from test_info ti, test_scores ts, test t \
			where ti.id = ts.test_scores_id and t.id = ti.name and ts.learner_id = %s" % (lid)
			
		cr.execute(sql)
		itm = cr.fetchall()
	
		for i in itm:
			vals = {
					'test_compre': cc,
					'test_conv': co,
					'r_level': rl,
					'r_score': rs,
					'l_level':ll,
					'l_score':ls,
					's_level':sl,
					's_score':ss,
					'w_level':wl,
					'w_score':ws,
					#'w_outcomes':wo,
					'n_level':nl,
					'n_score':ns,
					#'w_outcome1':woe,
					'test_score_type': i[1],
					'test_score_id':lid,
					'test_sc_date': i[0],
					'test_sc_code': i[2]
				}
		obj_res_hist.create(cr, uid, vals, context=context)
		return id
	_name ='test.scores'
	_description ="Test Scores Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'test_scores_id': fields.many2one('test.info', 'Test', ondelete='cascade', help='Class', select=True),
	'learner_id':fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner', select=True),
	'learner_nric': fields.related('learner_id','learner_nric',type="char",relation="learner.info",string="Learner NRIC", readonly=1,),
	'compr':fields.integer('Compr',size=2),
	'conv':fields.integer('Conv',size=2),
	'r_level':fields.integer('Reading(Level)',size=1),
	'r_scores':fields.integer('Readng(Scores)',size=2),
	'l_level':fields.integer('Listening(Level)',size=1),
	'l_scores':fields.integer('Listening(Scores)',size=2),
	's_level':fields.integer('Speaking(Level)',size=1),
	's_scores':fields.integer('Speaking(Scores)',size=2),
	'w_level':fields.integer('Writing(Level)',size=1),
	'w_scores':fields.integer('Writing(Scores)',size=2),
	'w_outcome':fields.char('W(Outcomes)',size=20),
	'n_level':fields.integer('Numeracy(Level)',size=1),
	'n_scores':fields.integer('Numeracy(Scores)',size=2),
	'n_outcome':fields.char('N(Outcomes)',size=20),
	}
test_scores()