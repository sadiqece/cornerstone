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

global class_create
class_create = False
 
class class_info(osv.osv):
	
	def _property_expense_preset_expenses(self, cr, uid, ids, expenses, arg, context):
		spus = self.browse(cr, uid, ids)
		module_ids =[]
		parent_id = spus[0]['parent_id']
		if parent_id > 0:
			prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
			prog_mod_ids.append(parent_id)
		else:
			prog_mod_ids = self.search(cr, uid, [('parent_id', '=', spus[0].id)])
			prog_mod_ids.append(spus[0].id)
			
		for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
			if prog_module_line['sess_issues'] != 'None' :
					module_ids.append(prog_module_line.id)
		
		value_ids = self.search(cr, uid, [('id', 'in', module_ids)])
		return dict([(id, value_ids) for id in ids])
		
		
	def _property_expense_preset_expenses1(self, cr, uid, ids, expenses, arg, context):
		spus = self.browse(cr, uid, ids)
		module_ids =[]
		parent_id = spus[0]['parent_id']
		if parent_id > 0:
			prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
			prog_mod_ids.append(parent_id)
		else:
			prog_mod_ids = self.search(cr, uid, [('parent_id', '=', spus[0].id)])
			prog_mod_ids.append(spus[0].id)
			
		for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
			if prog_module_line['sess_issues'] == 'None' :
					module_ids.append(prog_module_line.id)
		
		value_ids = self.search(cr, uid, [('id', 'in', module_ids)])
		return dict([(id, value_ids) for id in ids])	
		
	def _property_expense_preset_expenses2(self, cr, uid, ids, expenses, arg, context):
		trainer_ids =[]
		for trainer_obj in  self.browse(cr, uid, ids).trainers_line or [] :
			if trainer_obj.t_status == "Confirmed" :
				trainer_ids.append(trainer_obj.id)
		return dict([(id, trainer_ids) for id in ids])
	
	
	
	
	def _calculate_total_learners(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = line.learner_line or []
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
		return res

	def move_learner(self, cr, uid, ids, context=None): 
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'move_form')
		view_id = view_ref and view_ref[1] or False,
		ctx = dict(context)
		learner_move_array =[]
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		for le_obj in self_obj.learner_line:
			if le_obj['move'] == True :
				learner_move_array.append(le_obj.learner_id.id)
				
		if len(learner_move_array) == 0 :
			raise osv.except_osv(_('Error!'),_("Please select learners to move"))

		
		parent_id = self_obj['parent_id']
		if parent_id == 0:
			parent_id = self_obj.id
				
		ctx.update({'class_id': ids[0],'learner_id': learner_move_array,'active_module':self_obj.module_id.id,'active_parent_id':parent_id})
	
		return {
			'type': 'ir.actions.act_window',
			'name': 'Move Learner',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': view_id,
			'res_model': 'learner.move',
			'res_id':0,
			'nodestroy': True,
			'target':'new',
			'context': ctx,
		}
		
	def close_class(self, cr, uid, ids, context=None): 
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'move_form')
		view_id = view_ref and view_ref[1] or False,
		learner_move_array =[]
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		for le_obj in self_obj.learner_line:
			learner_move_array.append(le_obj.learner_id.id)
				
		if len(learner_move_array) > 0 :
			raise osv.except_osv(_('Error!'),_("Please move the learners before closing the class"))
	
	def _check_unique_name(self, cr, uid, ids, context=None):
		new_class = self.browse(cr, uid, ids, context=context)
		sr_ids = self.search(cr, 1, [('parent_id', '=', 0)])
		
		if new_class[0].parent_id == 0 :
			for x in self.browse(cr, uid, sr_ids, context=context) : 
				if new_class[0].parent_id == 0 and new_class[0].id != x.id and new_class[0].name.lower() == x.name.lower() :
					return False
		else :
			for x in self.browse(cr, uid, sr_ids, context=context) : 
				if new_class[0].parent_id  != x.id and new_class[0].name.lower() == x.name.lower() :
					return False
		return True
   
	def trainer_broadcast(self, cr, uid, ids, context=None): 
		learner_move_array = []
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		trainers = []
		for le_obj in self_obj.trainers_line:
			if le_obj.t_status == None or le_obj.t_status == False :
				learner_move_array.append(le_obj.trainer_id.id)
				trainers.append(le_obj.id)
		
				
		for er in trainers:
			self.pool.get('trainers.line').update_status(cr, uid, er,{'t_status':'Awaiting Response'}, context=context)
				
		if len(learner_move_array) > 0 :
			sub_lines = []
			values = {}
			sub_lines.append( (0,0, {'class':self_obj['id'],'class_code_avaliable':self_obj['class_code'],
				'start_date_avaliable':self_obj['start_date'],'status':'Awaiting'}) )
			values.update({'assignment_avaliable': sub_lines})
			trainer_obj = self.pool.get("trainer.profile.info")
			for x in trainer_obj.browse(cr, uid, learner_move_array, context=context):
				trainer_obj.write(cr, uid, x.id,values, context=context)
		
		
	
	
	def _check_unique_code(self, cr, uid, ids, context=None):
		new_class = self.browse(cr, uid, ids, context=context)
		sr_ids = self.search(cr, 1, [('parent_id', '=', 0)])
		if new_class[0].parent_id == 0 :
			for x in self.browse(cr, uid, sr_ids, context=context) : 
				if new_class[0].parent_id == 0 and new_class[0].id != x.id and new_class[0].class_code.lower() == x.class_code.lower() :
					return False
		else :
			for x in self.browse(cr, uid, sr_ids, context=context) : 
				if new_class[0].parent_id  != x.id and new_class[0].class_code.lower() == x.class_code.lower() :
					return False
		return True


	_name = "class.info"
	_description = "This table is for keeping location data"
	_columns = {
		'class_id': fields.integer('Id',size=20),
		'parent_id': fields.integer('Parent Id',size=20),
		'name': fields.char('Class Name', size=100,required=True, select=True),
		'class_code': fields.char('Class Code',size=40,required=True, select=True), 
		'location_id':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'room_id':fields.many2one('room', 'Room', ondelete='cascade', help='Room', select=True, required=True),
		'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
		'start_date': fields.datetime('Start Date', required=True),
		'end_date': fields.datetime('End Date'),
		'duration': fields.float('Duration(Hrs)'),
		'sessions_per_week': fields.integer('Number of Sessions Per Week', size=7),
		'sessions_duration_in_hrs': fields.float('Sessions Durations in Hours'),
		'total_hrs': fields.integer('Total Hours', readonly=1),
		'total_sessions': fields.integer('Total Sessions', readonly=1),
		'total_weeks': fields.integer('Total Weeks', readonly=1),
		'sess_info_line': fields.function(_property_expense_preset_expenses,type='one2many',obj="class.info",method=True,string='Session'),
		'sess_info_line1': fields.function(_property_expense_preset_expenses1,type='one2many',obj="class.info",method=True,string='Session'),
		'include_1':fields.boolean('Include'),
		'include_2':fields.boolean('Include'),
		'include_3':fields.boolean('Include'),
		'include_4':fields.boolean('Include'),
		'include_5':fields.boolean('Include'),
		'include_6':fields.boolean('Include'),
		'include_7':fields.boolean('Include'),
		'day_1':fields.char('Day 1',readonly=1),
		'day_2':fields.char('Day 2',readonly=1),
		'day_3':fields.char('Day 3',readonly=1),
		'day_4':fields.char('Day 4',readonly=1),
		'day_5':fields.char('Day 5',readonly=1),
		'day_6':fields.char('Day 6',readonly=1),
		'day_7':fields.char('Day 7',readonly=1),
		'start_date1': fields.datetime(),
		'start_date2': fields.datetime(),
		'start_date3': fields.datetime(),
		'start_date4': fields.datetime(),
		'start_date5': fields.datetime(),
		'start_date6': fields.datetime(),
		'start_date7': fields.datetime(),
		'end_date1': fields.datetime(),
		'end_date2': fields.datetime(),
		'end_date3': fields.datetime(),
		'end_date4': fields.datetime(),
		'end_date5': fields.datetime(),
		'end_date6': fields.datetime(),
		'end_date7': fields.datetime(),
		'room1': fields.char('Rooms', readonly=1),
		'room2': fields.char('Rooms', readonly=1),
		'room3': fields.char('Rooms', readonly=1),
		'room4': fields.char('Rooms', readonly=1),
		'room5': fields.char('Rooms', readonly=1),
		'room6': fields.char('Rooms', readonly=1),
		'room7': fields.char('Rooms', readonly=1),
		'trainers_line': fields.one2many('trainers.line', 'trainers_line_id', 'Broadcast'),
		'trainer_history': fields.one2many('trainers.history', 'trainers_hist_id', 'Broadcast'),
		'delivery_mode': fields.selection((('English','English'),('Singli','Singli'),('Malyi','Malyi')),'Delivery Mode'),
		'learner_line': fields.one2many('learner.line', 'learner_mod_id', 'Order Lines', select=True, required=True),
		'binder_in_use':fields.boolean('Binder'),
		'tablet_in_use':fields.boolean('Tablet'),
		'primary': fields.selection((('Binder','Binder'),('Tablet','Tablet')),'Primary'),
		'moi_eq_line': fields.one2many('class.moi','class_moi_id','Equipment List'),
		'room_arr': fields.selection((('Default','Default'),('Active','Active')),'Room Arrangment'),
		'learner_asset': fields.one2many('learner.asset','learner_asset_id','Asset'),
		'non_std_items': fields.selection((('Food','Food'),('Materials','Materials'),('Learning Assets','Learning Assets'),('Rooms','Rooms')),'Items'),
		'trainer_po_listing': fields.one2many('trainers.po.listing', 's_no', 'PO Listing'),
		'history_line': fields.one2many('class.history', 'history_id', 'History'),
		'sess_no':fields.integer('Session No'),
		'week_no':fields.integer('Week No'),
		'sess_issues':fields.char('Conflict Issues'),
		'apply_all':fields.boolean('Apply to All'),
		'apply_to_future':fields.boolean('Apply to Future'),
		'no_of_learners':fields.function(_calculate_total_learners, relation="class.info",readonly=1,string='No. Learners',type='integer'),
		'status':fields.char('Status')
	}
	_defaults = { 
		'status': 'Draft',
	} 
	_order = "start_date"
	
	_constraints = [(_check_unique_name, 'Error: Class Name Already Exists', ['name']),(_check_unique_code, 'Error: Class Code Already Exists', ['class_code'])]
	 
	def create(self,cr, uid, values, context=None):
		global class_create
		class_create = True
		
		if 'duration' in values and values['duration'] < 0:
			raise osv.except_osv(_('Error!'),_("Duration cannot be negative value"))
				
		if datetime.strptime(values['start_date'],"%Y-%m-%d %H:%M:%S")  < datetime.now() :
			raise osv.except_osv(_('Error!'),_("Start Date cannot be in past"))
		
		'''validate sessions now'''
		include_arr_list = 0
		for i in range(1,8):
			if values['include_'+str(i)] == True:
				include_arr_list = include_arr_list + 1
				
		if include_arr_list > values['total_sessions'] :
			raise osv.except_osv(_('Error!'),_("Selected Days are greater than Number of sessions"))
			return
		
		no_of_sess = 0
		parent_id =0
		include_array = []
		value_array =[]
		values['status'] = 'Edit'
		sub_lines = []
		current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
		sub_lines.append( (0,0, {'date_created':fields.date.today(),'created_by':current_user['name'],
		'last_update':'-','last_update_by':'-','date_status_change':fields.date.today(),'status_change_by':current_user['name']}) )
		values.update({'history_line': sub_lines})
		
		''' check for conflict now'''
		holiday = self.pool.get('holiday')
		holiday_obj_id = holiday.search(cr, uid, [('year', '=', datetime.now().year)])
		holiday_list = []
		if len(holiday_obj_id) > 0 :
			holiday_obj = holiday.browse(cr,uid,holiday_obj_id,context)
			holiday_line = self.pool.get('holiday.line')
			if len(holiday_obj) > 0 :
				holiday_line_obj_id = holiday_line.search(cr, uid, [('holiday_line_id', '=',holiday_obj[0]['id'])])
				for holiday_line_obj in holiday_line.browse(cr,uid,holiday_line_obj_id,context) :
					holiday_list.append(holiday_line_obj['date_start']+";"+holiday_line_obj['date_end']+";"+holiday_line_obj['description'])
				
		''' room conflicts'''
		room_conflict_ids = self.search(cr,uid,[('room_id',"=",values['room_id']),('start_date',">=",values['start_date'])])	
		for room_line_obj in self.browse(cr,uid,room_conflict_ids,context) :
			holiday_list.append(room_line_obj['start_date']+";"+room_line_obj['end_date']+";RoomConflict")
			
		for i in range(1,8):
			if values['include_'+str(i)] : 
				new_array = values
				new_array['start_date'] = values['start_date'+str(i)]
				new_array['end_date']= values['end_date'+str(i)]
				no_of_sess = no_of_sess + 1
				new_array['sess_no'] = no_of_sess
				new_array['week_no'] = 1
				new_array['parent_id'] = parent_id
				t1start  = new_array['start_date']
				t1end = new_array['end_date']
				overlap = False
				new_array['sess_issues'] = 'None'
				for u in holiday_list :
					t2start = u.split(";")[0]
					t2end = u.split(";")[1]
					if (t1start <= t2start <= t2end <= t1end):
						new_array['sess_issues'] = u.split(";")[2]
						continue
					elif (t1start <= t2start <= t1end):
						new_array['sess_issues'] = u.split(";")[2]
						continue
					elif (t1start <= t2end <= t1end):
						new_array['sess_issues'] = u.split(";")[2]
						continue
					elif (t2start <= t1start <= t1end <= t2end):
						new_array['sess_issues'] = u.split(";")[2]
						continue
					else:
						overlap = False
				
					
				id = super(class_info, self).create(cr, uid, new_array, context=context)
				if(no_of_sess == 1):
					parent_id = id
				include_array.append(str(new_array['start_date']) + ";" + str(new_array['end_date']))
				
				value_array.append(new_array)
	
		no_of_days =7 
		for k in range(1,(values['total_weeks'])) :
			new_array['week_no'] = new_array['week_no'] + 1
			for j in range(0,len(include_array)):
			   if no_of_sess < values['total_sessions']:
					new_array = value_array[j]
					newStartDate,newEndDate =  include_array[j].split(';')
					newStartDate = datetime.strptime(str(newStartDate),"%Y-%m-%d %H:%M:%S") + relativedelta(days=no_of_days)
					newEndDate = datetime.strptime(str(newEndDate),"%Y-%m-%d %H:%M:%S") + relativedelta(days=no_of_days)
					new_array['start_date'] = newStartDate
					new_array['end_date']= newEndDate
					no_of_sess = no_of_sess+1
					new_array['sess_no'] = no_of_sess
					new_array['parent_id'] = parent_id
					t1start  = new_array['start_date']
					t1end = new_array['end_date']
					overlap = False
					new_array['sess_issues'] = 'None'
					for u in holiday_list :
					
						t2start =datetime.strptime(str(u.split(";")[0]),"%Y-%m-%d %H:%M:%S")
						t2end =datetime.strptime(str(u.split(";")[1]),"%Y-%m-%d %H:%M:%S")
						if (t1start <= t2start <= t2end <= t1end):
							new_array['sess_issues'] = u.split(";")[2]
							continue
						elif (t1start <= t2start <= t1end):
							new_array['sess_issues'] = u.split(";")[2]
							continue
						elif (t1start <= t2end <= t1end):
							new_array['sess_issues'] = u.split(";")[2]
							continue
						elif (t2start <= t1start <= t1end <= t2end):
							new_array['sess_issues'] = u.split(";")[2]
							continue
						else:
							overlap = False
					
					
					id = super(class_info, self).create(cr, uid, new_array, context=context)
					
			no_of_days = no_of_days + 7
			
		global class_create
		class_create = False
		
		return id
		
	def apply_to_all(self,cr, uid, ids, values, context=None):
			class_info_obj = self.browse(cr, uid, ids[0])
			parent_id = class_info_obj['parent_id']
			self.record_class_history(cr, uid, ids, values, context)
			
			if 'start_date' in values :
				duration  = 1.00
				if 'duration' in values :
				   duration = values['duration']
				else :
					duration = class_info_obj['duration']
			
				user = self.pool.get('res.users').browse(cr, uid, uid)
				tz = pytz.timezone(user.tz) if user.tz else pytz.utc
			
				new_date_time = datetime.strptime(values['start_date'],"%Y-%m-%d %H:%M:%S")
				if new_date_time  < datetime.now() :
					raise osv.except_osv(_('Error!'),_("Start Date cannot be in past"))

				new_date_time_utc = pytz.utc.localize(new_date_time).astimezone(tz)
				new_time = str(new_date_time_utc.time())
				local =pytz.timezone(user.tz)
	
				date_array = {}
				date_array['start_date'] = new_date_time 
				date_array['end_date'] = date_array['start_date']  + timedelta(hours=duration)
				
				for j in range(1,8) :
					if class_info_obj['start_date'+str(j)] != None and class_info_obj['start_date'+str(j)] !=  False:
						local_value = datetime.strptime(class_info_obj['start_date'+str(j)],"%Y-%m-%d %H:%M:%S")
						local_date_time_utc = pytz.utc.localize(local_value).astimezone(tz)
						changed_date_time = datetime.strptime(str(local_date_time_utc.date()) +" "+new_time,"%Y-%m-%d %H:%M:%S")
						local_dt = local.localize(changed_date_time, is_dst=None)
						utc_dt = local_dt.astimezone (pytz.utc)
						date_array['start_date'+str(j)] =utc_dt.strftime ("%Y-%m-%d %H:%M:%S")
						date_array['end_date'+str(j)] = str(datetime.strptime(date_array['start_date'+str(j)],"%Y-%m-%d %H:%M:%S") + timedelta(hours=duration))
						
			
				holiday = self.pool.get('holiday')
				holiday_obj_id = holiday.search(cr, uid, [('year', '=', datetime.now().year)])
				holiday_list = []
				if len(holiday_obj_id) > 0 :
					holiday_obj = holiday.browse(cr,uid,holiday_obj_id,context)
					holiday_list = []
					holiday_line = self.pool.get('holiday.line')
					holiday_line_obj_id = holiday_line.search(cr, uid, [('holiday_line_id', '=',holiday_obj[0]['id'])])
					for holiday_line_obj in holiday_line.browse(cr,uid,holiday_line_obj_id,context) :
						holiday_list.append(holiday_line_obj['date_start']+";"+holiday_line_obj['date_end']+";"+holiday_line_obj['description'])
					
				
					'''check for first holiday conflicts'''
					t1start  = date_array['start_date']
					t1end = date_array['end_date']
					overlap = False
					date_array['sess_issues'] = 'None'
					for u in holiday_list :
						t2start =datetime.strptime(str(u.split(";")[0]),"%Y-%m-%d %H:%M:%S")
						t2end =datetime.strptime(str(u.split(";")[1]),"%Y-%m-%d %H:%M:%S")
						if (t1start <= t2start <= t2end <= t1end):
							date_array['sess_issues'] = u.split(";")[2]
							continue
						elif (t1start <= t2start <= t1end):
							date_array['sess_issues'] = u.split(";")[2]
							continue
						elif (t1start <= t2end <= t1end):
							date_array['sess_issues'] = u.split(";")[2]
							continue
						elif (t2start <= t1start <= t1end <= t2end):
							date_array['sess_issues'] = u.split(";")[2]
							continue
						else:
							overlap = False
					
				date_array['history_line'] = values['history_line']
				super(class_info, self).write(cr, uid, ids,date_array, context=context)
					
				if parent_id == 0 :
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
					prog_mod_ids.append(parent_id)
		
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					if prog_module_line.id != class_info_obj.id :
						local_value = datetime.strptime(prog_module_line['start_date'],"%Y-%m-%d %H:%M:%S")
						local_date_time_utc = pytz.utc.localize(local_value).astimezone(tz)
						changed_date_time = datetime.strptime(str(local_date_time_utc.date()) +" "+new_time,"%Y-%m-%d %H:%M:%S")
						local_dt = local.localize(changed_date_time, is_dst=None)
						utc_dt = local_dt.astimezone (pytz.utc)
						date_array['start_date'] =utc_dt.strftime ("%Y-%m-%d %H:%M:%S")
						date_array['end_date'] = str(datetime.strptime(date_array['start_date'],"%Y-%m-%d %H:%M:%S") + timedelta(hours=duration))
						
						t1start  = datetime.strptime(date_array['start_date'],"%Y-%m-%d %H:%M:%S")
						t1end = datetime.strptime(date_array['end_date'],"%Y-%m-%d %H:%M:%S")
						overlap = False
						date_array['sess_issues'] = 'None'
						for u in holiday_list :
							t2start =datetime.strptime(str(u.split(";")[0]),"%Y-%m-%d %H:%M:%S")
							t2end =datetime.strptime(str(u.split(";")[1]),"%Y-%m-%d %H:%M:%S")
							if (t1start <= t2start <= t2end <= t1end):
								date_array['sess_issues'] = u.split(";")[2]
								continue
							elif (t1start <= t2start <= t1end):
								date_array['sess_issues'] = u.split(";")[2]
								continue
							elif (t1start <= t2end <= t1end):
								date_array['sess_issues'] = u.split(";")[2]
								continue
							elif (t2start <= t1start <= t1end <= t2end):
								date_array['sess_issues'] = u.split(";")[2]
								continue
						date_array['history_line'] = values['history_line']
						super(class_info, self).write(cr, uid, prog_module_line.id,date_array, context=context)
							
			if 'room_id' in values :
				room_obj = self.pool.get('room').browse(cr, uid, values['room_id'])
				values['room1'] = room_obj.name
				values['room2'] = room_obj.name
				values['room3'] = room_obj.name
				values['room4'] = room_obj.name
				values['room5'] = room_obj.name
				values['room6'] = room_obj.name
				values['room7'] = room_obj.name
				'''check room conflicts'''
				room_conflict_ids = self.search(cr,uid,[('room_id',"=",values['room_id'])])
				holiday_list =[]
				for room_line_obj in self.browse(cr,uid,room_conflict_ids,context) :
					holiday_list.append(room_line_obj['start_date']+";"+room_line_obj['end_date']+";RoomConflict")
					
				t1start  = datetime.strptime(str(class_info_obj['start_date']),"%Y-%m-%d %H:%M:%S")
				t1end = datetime.strptime(str(class_info_obj['end_date']),"%Y-%m-%d %H:%M:%S")
				overlap = False
				values['sess_issues'] = 'None'
				for u in holiday_list :
					t2start =datetime.strptime(str(u.split(";")[0]),"%Y-%m-%d %H:%M:%S")
					t2end =datetime.strptime(str(u.split(";")[1]),"%Y-%m-%d %H:%M:%S")
					if (t1start <= t2start <= t2end <= t1end):
						values['sess_issues'] = u.split(";")[2]
						continue
					elif (t1start <= t2start <= t1end):
						values['sess_issues'] = u.split(";")[2]
						continue
					elif (t1start <= t2end <= t1end):
						values['sess_issues'] = u.split(";")[2]
						continue
					elif (t2start <= t1start <= t1end <= t2end):
						values['sess_issues'] = u.split(";")[2]
						continue
					else:
						overlap = False
				values['history_line'] = values['history_line']
				super(class_info, self).write(cr, uid, parent_id,values, context=context)
				
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
					
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					if prog_module_line.id != parent_id:
						room_array = {'room1': room_obj.name, 'room2': room_obj.name, 'room3': room_obj.name, 'room4': room_obj.name, 'room5': room_obj.name, 'room6': room_obj.name, 'room7': room_obj.name}
						room_array['room_id'] = values['room_id']
						
						t1start  = datetime.strptime(str(prog_module_line['start_date']),"%Y-%m-%d %H:%M:%S")
						t1end = datetime.strptime(str(prog_module_line['end_date']),"%Y-%m-%d %H:%M:%S")
						overlap = False
						room_array['sess_issues'] = 'None'
						for u in holiday_list :
							t2start =datetime.strptime(str(u.split(";")[0]),"%Y-%m-%d %H:%M:%S")
							t2end =datetime.strptime(str(u.split(";")[1]),"%Y-%m-%d %H:%M:%S")
							if (t1start <= t2start <= t2end <= t1end):
								room_array['sess_issues'] = u.split(";")[2]
								continue
							elif (t1start <= t2start <= t1end):
								room_array['sess_issues'] = u.split(";")[2]
								continue
							elif (t1start <= t2end <= t1end):
								room_array['sess_issues'] = u.split(";")[2]
								continue
							elif (t2start <= t1start <= t1end <= t2end):
								room_array['sess_issues'] = u.split(";")[2]
								continue
							else:
								overlap = False
						room_array['history_line'] = values['history_line']
						super(class_info, self).write(cr, uid, prog_module_line.id,room_array, context=context)
						
						
			if 'location_id' in values :
				super(class_info, self).write(cr, uid, parent_id,{'location_id': values['location_id'],'history_line':values['history_line']}, context=context)
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
				
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					super(class_info, self).write(cr, uid, prog_module_line.id,{'location_id': values['location_id'],'history_line':values['history_line']}, context=context)
						
			if 'module_id' in values :
				super(class_info, self).write(cr, uid, parent_id,{'module_id': values['module_id'],'history_line':values['history_line']}, context=context)
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
					
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					super(class_info, self).write(cr, uid, prog_module_line.id,{'module_id': values['module_id'],'history_line':values['history_line']}, context=context)
			
			if 'duration' in values :
				data_array = {}
				data_array['duration'] = values['duration']
				data_array['end_date'] = datetime.strptime(class_info_obj['start_date'],"%Y-%m-%d %H:%M:%S") + timedelta(hours=values['duration'])
				for j in range(1,8) :
					if class_info_obj['start_date'+str(j)] != None and class_info_obj['start_date'+str(j)] !=  False:
						data_array['end_date'+str(j)] = datetime.strptime(class_info_obj['start_date'+str(j)],"%Y-%m-%d %H:%M:%S") + timedelta(hours=values['duration'])
				data_array['history_line'] = values['history_line']
				super(class_info, self).write(cr, uid, parent_id,data_array, context=context)
			
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])	
					
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					if prog_module_line['start_date'] != None and prog_module_line['start_date'] !=  False:
						data_array['end_date'] = datetime.strptime(prog_module_line['start_date'],"%Y-%m-%d %H:%M:%S") + timedelta(hours=values['duration'])
						super(class_info, self).write(cr, uid, prog_module_line.id,data_array, context=context)
	
	def apply_to_future(self,cr, uid, ids, values, context=None):
			class_info_obj = self.browse(cr, uid, ids[0])
			parent_id = class_info_obj['parent_id']
			self.record_class_history(cr, uid, ids, values, context)
			
			if 'start_date' in values :
				duration  = 1.00
				if 'duration' in values :
				   duration = values['duration']
				else :
					duration = class_info_obj['duration']
			
				user = self.pool.get('res.users').browse(cr, uid, uid)
				tz = pytz.timezone(user.tz) if user.tz else pytz.utc
			
				new_date_time = datetime.strptime(values['start_date'],"%Y-%m-%d %H:%M:%S")
				if new_date_time  < datetime.now() :
					raise osv.except_osv(_('Error!'),_("Start Date cannot be in past"))
				
				new_date_time_utc = pytz.utc.localize(new_date_time).astimezone(tz)
				new_time = str(new_date_time_utc.time())
				local =pytz.timezone(user.tz)
				date_array = {}
				date_array['start_date'] = new_date_time 
				date_array['end_date'] = date_array['start_date']  + timedelta(hours=duration)
				old_time = class_info_obj['start_date'] 
				for j in range(1,8) :
					if class_info_obj['start_date'+str(j)] != None and class_info_obj['start_date'+str(j)] !=  False:
						local_value = datetime.strptime(class_info_obj['start_date'+str(j)],"%Y-%m-%d %H:%M:%S")
						if local_value >= new_date_time or class_info_obj['start_date'] == class_info_obj['start_date'+str(j)]:
							local_date_time_utc = pytz.utc.localize(local_value).astimezone(tz)
							changed_date_time = datetime.strptime(str(local_date_time_utc.date()) +" "+new_time,"%Y-%m-%d %H:%M:%S")
							local_dt = local.localize(changed_date_time, is_dst=None)
							utc_dt = local_dt.astimezone (pytz.utc)
							date_array['start_date'+str(j)] =utc_dt.strftime ("%Y-%m-%d %H:%M:%S")
							date_array['end_date'+str(j)] = str(datetime.strptime(date_array['start_date'+str(j)],"%Y-%m-%d %H:%M:%S") + timedelta(hours=duration))
						
			
				holiday = self.pool.get('holiday')
				holiday_obj_id = holiday.search(cr, uid, [('year', '=', datetime.now().year)])
				holiday_list = []
				if len(holiday_obj_id) > 0 :
					holiday_obj = holiday.browse(cr,uid,holiday_obj_id,context)
					holiday_line = self.pool.get('holiday.line')
					holiday_line_obj_id = holiday_line.search(cr, uid, [('holiday_line_id', '=',holiday_obj[0]['id'])])
					for holiday_line_obj in holiday_line.browse(cr,uid,holiday_line_obj_id,context) :
						holiday_list.append(holiday_line_obj['date_start']+";"+holiday_line_obj['date_end']+";"+holiday_line_obj['description'])
					
					
					'''check for first holiday conflicts'''
					t1start  = date_array['start_date']
					t1end = date_array['end_date']
					overlap = False
					date_array['sess_issues'] = 'None'
					for u in holiday_list :
						t2start =datetime.strptime(str(u.split(";")[0]),"%Y-%m-%d %H:%M:%S")
						t2end =datetime.strptime(str(u.split(";")[1]),"%Y-%m-%d %H:%M:%S")
						if (t1start <= t2start <= t2end <= t1end):
							date_array['sess_issues'] = u.split(";")[2]
							continue
						elif (t1start <= t2start <= t1end):
							date_array['sess_issues'] = u.split(";")[2]
							continue
						elif (t1start <= t2end <= t1end):
							date_array['sess_issues'] = u.split(";")[2]
							continue
						elif (t2start <= t1start <= t1end <= t2end):
							date_array['sess_issues'] = u.split(";")[2]
							continue
						else:
							overlap = False
					
				date_array['history_line'] = values['history_line']
				super(class_info, self).write(cr, uid, ids,date_array, context=context)
					
				if parent_id == 0 :
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
					prog_mod_ids.append(parent_id)
		
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					if prog_module_line.id != class_info_obj.id :
						local_value = datetime.strptime(prog_module_line['start_date'],"%Y-%m-%d %H:%M:%S")
						if local_value >= new_date_time :
							local_date_time_utc = pytz.utc.localize(local_value).astimezone(tz)
							changed_date_time = datetime.strptime(str(local_date_time_utc.date()) +" "+new_time,"%Y-%m-%d %H:%M:%S")
							local_dt = local.localize(changed_date_time, is_dst=None)
							utc_dt = local_dt.astimezone (pytz.utc)
							date_array['start_date'] =utc_dt.strftime ("%Y-%m-%d %H:%M:%S")
							date_array['end_date'] = str(datetime.strptime(date_array['start_date'],"%Y-%m-%d %H:%M:%S") + timedelta(hours=duration))
							
							t1start  = datetime.strptime(date_array['start_date'],"%Y-%m-%d %H:%M:%S")
							t1end = datetime.strptime(date_array['end_date'],"%Y-%m-%d %H:%M:%S")
							overlap = False
							date_array['sess_issues'] = 'None'
							for u in holiday_list :
								t2start =datetime.strptime(str(u.split(";")[0]),"%Y-%m-%d %H:%M:%S")
								t2end =datetime.strptime(str(u.split(";")[1]),"%Y-%m-%d %H:%M:%S")
								if (t1start <= t2start <= t2end <= t1end):
									date_array['sess_issues'] = u.split(";")[2]
									continue
								elif (t1start <= t2start <= t1end):
									date_array['sess_issues'] = u.split(";")[2]
									continue
								elif (t1start <= t2end <= t1end):
									date_array['sess_issues'] = u.split(";")[2]
									continue
								elif (t2start <= t1start <= t1end <= t2end):
									date_array['sess_issues'] = u.split(";")[2]
									continue
							date_array['history_line'] = values['history_line']
							super(class_info, self).write(cr, uid, prog_module_line.id,date_array, context=context)
							
			if 'room_id' in values :
				room_obj = self.pool.get('room').browse(cr, uid, values['room_id'])
				new_date_time = datetime.strptime(class_info_obj['start_date'],"%Y-%m-%d %H:%M:%S")
				for j in range(1,8) :
					if class_info_obj['start_date'+str(j)] != None and class_info_obj['start_date'+str(j)] !=  False:
						local_value = datetime.strptime(class_info_obj['start_date'+str(j)],"%Y-%m-%d %H:%M:%S")
						if local_value >= new_date_time :
							values['room'+str(j)] = room_obj.name

				'''check room conflicts'''
				room_conflict_ids = self.search(cr,uid,[('room_id',"=",values['room_id'])])
				holiday_list =[]
				for room_line_obj in self.browse(cr,uid,room_conflict_ids,context) :
					holiday_list.append(room_line_obj['start_date']+";"+room_line_obj['end_date']+";RoomConflict")
					
				t1start  = datetime.strptime(str(class_info_obj['start_date']),"%Y-%m-%d %H:%M:%S")
				t1end = datetime.strptime(str(class_info_obj['end_date']),"%Y-%m-%d %H:%M:%S")
				overlap = False
				values['sess_issues'] = 'None'
				for u in holiday_list :
					t2start =datetime.strptime(str(u.split(";")[0]),"%Y-%m-%d %H:%M:%S")
					t2end =datetime.strptime(str(u.split(";")[1]),"%Y-%m-%d %H:%M:%S")
					if (t1start <= t2start <= t2end <= t1end):
						values['sess_issues'] = u.split(";")[2]
						continue
					elif (t1start <= t2start <= t1end):
						values['sess_issues'] = u.split(";")[2]
						continue
					elif (t1start <= t2end <= t1end):
						values['sess_issues'] = u.split(";")[2]
						continue
					elif (t2start <= t1start <= t1end <= t2end):
						values['sess_issues'] = u.split(";")[2]
						continue
					else:
						overlap = False
				values['history_line'] = values['history_line']
				super(class_info, self).write(cr, uid, parent_id,values, context=context)
				
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
					
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					if prog_module_line.id != parent_id:
						local_value = datetime.strptime(prog_module_line['start_date'],"%Y-%m-%d %H:%M:%S")
						if local_value >= t1start :
							room_array = {'room1': room_obj.name, 'room2': room_obj.name, 'room3': room_obj.name, 'room4': room_obj.name, 'room5': room_obj.name, 'room6': room_obj.name, 'room7': room_obj.name}
							room_array['room_id'] = values['room_id']
							
							t1start  = datetime.strptime(str(prog_module_line['start_date']),"%Y-%m-%d %H:%M:%S")
							t1end = datetime.strptime(str(prog_module_line['end_date']),"%Y-%m-%d %H:%M:%S")
							overlap = False
							room_array['sess_issues'] = 'None'
							for u in holiday_list :
								t2start =datetime.strptime(str(u.split(";")[0]),"%Y-%m-%d %H:%M:%S")
								t2end =datetime.strptime(str(u.split(";")[1]),"%Y-%m-%d %H:%M:%S")
								if (t1start <= t2start <= t2end <= t1end):
									room_array['sess_issues'] = u.split(";")[2]
									continue
								elif (t1start <= t2start <= t1end):
									room_array['sess_issues'] = u.split(";")[2]
									continue
								elif (t1start <= t2end <= t1end):
									room_array['sess_issues'] = u.split(";")[2]
									continue
								elif (t2start <= t1start <= t1end <= t2end):
									room_array['sess_issues'] = u.split(";")[2]
									continue
								else:
									overlap = False
							room_array['history_line'] = values['history_line']
							super(class_info, self).write(cr, uid, prog_module_line.id,room_array, context=context)
							
						
			if 'location_id' in values :
				super(class_info, self).write(cr, uid, parent_id,{'location_id': values['location_id'],'history_line':values['history_line']}, context=context)
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
				
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					local_value = datetime.strptime(prog_module_line['start_date'],"%Y-%m-%d %H:%M:%S")
					t1start  = datetime.strptime(class_info_obj['start_date'],"%Y-%m-%d %H:%M:%S")
					if local_value >= t1start :
						super(class_info, self).write(cr, uid, prog_module_line.id,{'location_id': values['location_id'],'history_line':values['history_line']}, context=context)
						
			if 'module_id' in values :
				super(class_info, self).write(cr, uid, parent_id,{'module_id': values['module_id'],'history_line':values['history_line']}, context=context)
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
					
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					local_value = datetime.strptime(prog_module_line['start_date'],"%Y-%m-%d %H:%M:%S")
					t1start  = datetime.strptime(class_info_obj['start_date'],"%Y-%m-%d %H:%M:%S")
					if local_value >= t1start :
						super(class_info, self).write(cr, uid, prog_module_line.id,{'module_id': values['module_id'],'history_line':values['history_line']}, context=context)
			
			if 'duration' in values :
				data_array = {}
				data_array['duration'] = values['duration']
				data_array['end_date'] = datetime.strptime(class_info_obj['start_date'],"%Y-%m-%d %H:%M:%S") + timedelta(hours=values['duration'])
				for j in range(1,8) :
					if class_info_obj['start_date'+str(j)] != None and class_info_obj['start_date'+str(j)] !=  False:
						data_array['end_date'+str(j)] = datetime.strptime(class_info_obj['start_date'+str(j)],"%Y-%m-%d %H:%M:%S") + timedelta(hours=values['duration'])
				data_array['history_line'] = values['history_line']
				super(class_info, self).write(cr, uid, parent_id,data_array, context=context)
			
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
				else:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])	
					
				for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
					if prog_module_line['start_date'] != None and prog_module_line['start_date'] !=  False:
						local_value = datetime.strptime(prog_module_line['start_date'],"%Y-%m-%d %H:%M:%S")
						t1start  = datetime.strptime(class_info_obj['start_date'],"%Y-%m-%d %H:%M:%S")
						if local_value >= t1start :
							data_array['end_date'] = local_value + timedelta(hours=values['duration'])
							super(class_info, self).write(cr, uid, prog_module_line.id,data_array, context=context)
		
		
	def write(self,cr, uid, ids, values, context=None,holidays=False):
		if holidays ==  False :
			if 'duration' in values and values['duration'] < 0:
				raise osv.except_osv(_('Error!'),_("Duration cannot be negative value"))
			
			apply = False;
			apply_to_future = False;
			location_obj = self.browse(cr, uid, ids[0])
			parent_id = location_obj['parent_id']
			parent_obj = self.browse(cr, uid, parent_id,context=context)
			
			if 'apply_all' not in values :
				apply = location_obj['apply_all']
			else :
				apply = values['apply_all']
				
			if 'apply_to_future' not in values :
				apply_to_future = location_obj['apply_to_future']
			else :
				apply_to_future = values['apply_to_future']
			
			
			if apply == True :
				self.apply_to_all(cr, uid, ids, values, context)
			elif apply_to_future == True :
				self.apply_to_future(cr, uid, ids, values, context)
			else:
				if 'delivery_mode' in values or 'binder_in_use' in values or 'tablet_in_use' in values or 'primary'in values or 'room_arr' in 	values :
					super(class_info, self).write(cr, uid, parent_id,values, context=context)
					if parent_id > 0:
						prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
						for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
							super(class_info, self).write(cr, uid, prog_module_line.id,values, context=context)
				elif 'start_date' in values :
					t1start  = datetime.strptime(str(values['start_date']),"%Y-%m-%d %H:%M:%S")
					if t1start  < datetime.now() :
						raise osv.except_osv(_('Error!'),_("Start Date cannot be in past"))
					if 'duration' in values :
						duration = values['duration'] 
					else :
						duration = location_obj['duration']
						
					values['end_date'] = t1start + timedelta(hours=duration)
					t1end = values['end_date']
					holiday_list = []
					holiday = self.pool.get('holiday')
					holiday_obj_id = holiday.search(cr, uid, [('year', '=', datetime.now().year)])
					if len(holiday_obj_id) > 0:
						holiday_obj = holiday.browse(cr,uid,holiday_obj_id,context)
						holiday_line = self.pool.get('holiday.line')
						holiday_line_obj_id = holiday_line.search(cr, uid, [('holiday_line_id', '=',holiday_obj[0]['id'])])
						for holiday_line_obj in holiday_line.browse(cr,uid,holiday_line_obj_id,context) :
							t2start =datetime.strptime(holiday_line_obj['date_start'],"%Y-%m-%d %H:%M:%S")
							t2end =datetime.strptime(holiday_line_obj['date_end'],"%Y-%m-%d %H:%M:%S")
							if (t1start <= t2start <= t2end <= t1end):
								values['sess_issues'] = holiday_line_obj['description']
								continue
							elif (t1start <= t2start <= t1end):
								values['sess_issues'] = holiday_line_obj['description']
								continue
							elif (t1start <= t2end <= t1end):
								values['sess_issues'] = holiday_line_obj['description']
								continue
							elif (t2start <= t1start <= t1end <= t2end):
								values['sess_issues'] = holiday_line_obj['description']
								continue
					
				
					for j in range(1,8) :
						if location_obj['start_date'+str(j)] != None and location_obj['start_date'+str(j)] !=  False:
							compare_time = datetime.strptime(location_obj['start_date'+str(j)],"%Y-%m-%d %H:%M:%S")
							if compare_time == datetime.strptime(location_obj['start_date'],"%Y-%m-%d %H:%M:%S") :
								values['start_date'+str(j)] = values['start_date']
								values['end_date'+str(j)] = datetime.strptime(values['start_date'+str(j)],"%Y-%m-%d %H:%M:%S") + timedelta(hours=location_obj['duration'])
								super(class_info, self).write(cr, uid, ids,values, context=context)
								if parent_id > 0:
									prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
									prog_mod_ids.append(parent_id)
								else :
									prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
									
								for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
									if prog_module_line.id != ids[0] :
										super(class_info, self).write(cr, uid, prog_module_line.id,{'start_date'+str(j):values['start_date'+str(j)],'end_date'+str(j):values['end_date'+str(j)]}, context=context)
										
				elif 'duration' in values :
					t1start = datetime.strptime(location_obj['start_date'],"%Y-%m-%d %H:%M:%S")
					values['end_date'] = t1start + timedelta(hours=values['duration'])
					t1end	= values['end_date'] 
					holiday = self.pool.get('holiday')
					holiday_list = []
					holiday_obj_id = holiday.search(cr, uid, [('year', '=', datetime.now().year)])
					if len(holiday_obj_id) > 0 :
						holiday_obj = holiday.browse(cr,uid,holiday_obj_id,context)
						holiday_line = self.pool.get('holiday.line')
						holiday_line_obj_id = holiday_line.search(cr, uid, [('holiday_line_id', '=',holiday_obj[0]['id'])])
						for holiday_line_obj in holiday_line.browse(cr,uid,holiday_line_obj_id,context) :
							t2start =datetime.strptime(holiday_line_obj['date_start'],"%Y-%m-%d %H:%M:%S")
							t2end =datetime.strptime(holiday_line_obj['date_end'],"%Y-%m-%d %H:%M:%S")
							if (t1start <= t2start <= t2end <= t1end):
								values['sess_issues'] = holiday_line_obj['description']
								continue
							elif (t1start <= t2start <= t1end):
								values['sess_issues'] = holiday_line_obj['description']
								continue
							elif (t1start <= t2end <= t1end):
								values['sess_issues'] = holiday_line_obj['description']
								continue
							elif (t2start <= t1start <= t1end <= t2end):
								values['sess_issues'] = holiday_line_obj['description']
								continue
					
					for j in range(1,8) :
						if location_obj['end_date'+str(j)] != None and location_obj['end_date'+str(j)] !=  False:
							compare_time = datetime.strptime(location_obj['end_date'+str(j)],"%Y-%m-%d %H:%M:%S")
							if compare_time == datetime.strptime(location_obj['end_date'],"%Y-%m-%d %H:%M:%S") :
								values['end_date'+str(j)] =  datetime.strptime(location_obj['start_date'+str(j)],"%Y-%m-%d %H:%M:%S") + timedelta(hours=values['duration'])
								super(class_info, self).write(cr, uid, ids,values, context=context)
								
								if parent_id > 0:
									prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
									prog_mod_ids.append(parent_id)
								else :
									prog_mod_ids = self.search(cr, uid, [('parent_id', '=', ids[0])])
									
								for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
									if prog_module_line.id != ids[0] :
										super(class_info, self).write(cr, uid, prog_module_line.id,{'end_date'+str(j):values['end_date'+str(j)]}, context=context)
				
			module_id = super(class_info, self).write(cr, uid, ids,values, context=context)
		else:
			module_id = super(class_info, self).write(cr, uid, ids,values, context=context)
		return module_id

	def record_class_history (self, cr, uid, ids, values, context) :
		sub_lines = []
		
		current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
		for line in self.browse(cr, uid, ids, context=context):
			history_line_id = self.browse(cr, uid, ids[0], context=context).history_line or []
		
		
		num_of_his = len(history_line_id)-1 
		staus_changed_by =   history_line_id[num_of_his]['status_change_by']
		staus_changed_date =   history_line_id[num_of_his]['date_status_change']
		
		changes = values.keys()
		class_list ={'name':'Class Name','class_code': 'Class Code','location_id': 'Location','room_id':'Rooms', 
						'module_id': 'Module','start_date': 'Start Date','duration':'Duration(Hrs)',
						'include_1':'Include Day 1','include_2':'Include Day 2','include_3':'Include Day 3',
						'include_4':'Include Day 4','include_5':'Include Day 5','include_6':'Include Day 6',
						'include_7':'Include Day 7','trainers_line':'Trainer','trainer_history':  'Trainer Assigment History',
						'delivery_mode': 'Delivery Mode','learner_line': 'Learner Lines','binder_in_use':'Binder',
						'tablet_in_use':'Tablet','primary': 'Primary','moi_eq_line': 'Equipment List','room_arr': 'Room Arrangment',
						'learner_asset': 'Asset','non_std_items': 'Non Standard Items','trainer_po_listing': 'PO Listing',
						'apply_all':'Apply to All','apply_to_future':'Apply to Future','status':'Status'}
		arr={}
		for i in range(len(changes)):
			if changes[i] in class_list:
				arr[i] = class_list[changes[i]]
		
		sub_lines.append( (0,0, {'date_created':history_line_id[0]['date_created'],'created_by':history_line_id[0]['created_by'],
			'last_update':fields.date.today(),'last_update_by':current_user['name'],'date_status_change':staus_changed_date,'status_change_by':staus_changed_by,'changes':arr.values()}) )
		values.update({'history_line': sub_lines})

	def onchange_apply_to_all(self, cr, uid, ids, apply_to_all):
		
		if apply_to_all  == True :
			
			return {'value': {'apply_to_future': False}}
		else : 
			return {'value': {}}
		
	def onchange_apply_to_future(self, cr, uid, ids, apply_to_future):
		
		if apply_to_future  == True :
			return {'value': {'apply_all': False}}
		else : 
			return {'value': {}}
   
   
	def on_change_module_id(self, cr, uid, ids, module_id):
		module_obj = self.pool.get('cs.module').browse(cr, uid, module_id)
		return {'value': {'total_hrs': module_obj.module_duration,'location_id':False,'room_id':False}}
	
	def on_change_location_id(self, cr, uid, ids, location_id):
		return {'value': {'room_id': False}}
		
	def on_change_tot_sess(self, cr, uid, ids, sessions_duration_in_hrs,total_hrs):
	   
		if sessions_duration_in_hrs > 0 :
			if total_hrs % sessions_duration_in_hrs == 0 :
				return {'value': {'total_sessions': total_hrs/sessions_duration_in_hrs}}
			else:
				return {'value': {'total_sessions': (total_hrs/sessions_duration_in_hrs)+1}}
		else :
			return {'value': {'total_sessions': 0}}
		
	def on_change_tot_week(self, cr, uid, ids, total_sessions,sessions_per_week):
	   
		if sessions_per_week > 0 :
			if total_sessions % sessions_per_week == 0 :
				return {'value': {'total_weeks': total_sessions/sessions_per_week}}
			else:
				return {'value': {'total_weeks': (total_sessions/sessions_per_week)+1}}
		else :
			return {'value': {'total_weeks': 0}}

	def on_change_sess_week(self, cr, uid, ids, include_1,include_2,include_3,include_4,include_5,include_6,include_7):
		sessions_per_week = 0
		if include_1 :
			sessions_per_week+=1
		if include_2 :
			sessions_per_week+=1
		if include_3 :
			sessions_per_week+=1
		if include_4 :
			sessions_per_week+=1
		if include_5 :
			sessions_per_week+=1
		if include_6 :
			sessions_per_week+=1
		if include_7 :
			sessions_per_week+=1
		
		return {'value': {'sessions_per_week': sessions_per_week}}
		
	def onchange_dates(self, cr, uid, ids, start_date, duration=False, end_date=False, total_hrs=False, context=None):
		value = {}
		
		if len(ids) == 0:
			apply_include = False
			if not start_date:
				return value
			if not end_date and not duration:
				duration = 1.00
				value['duration'] = duration
				apply_include = True
				
			
			start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
			
			if not end_date:
				end = start + timedelta(hours=duration)
				value['end_date'] = end.strftime("%Y-%m-%d %H:%M:%S")
				
			if duration and total_hrs:
				sessions_duration_in_hrs = duration
				if sessions_duration_in_hrs > 0 :
					if total_hrs % sessions_duration_in_hrs == 0 :
						value['total_sessions'] = total_hrs/sessions_duration_in_hrs
					else:
						value['total_sessions'] = (total_hrs/sessions_duration_in_hrs)+1
				else :
					value['total_sessions'] = 0
				
			user = self.pool.get('res.users').browse(cr, uid, uid)
			tz = pytz.timezone(user.tz) if user.tz else pytz.utc
			ran = 7 - pytz.utc.localize(start).astimezone(tz).weekday()
			value['sessions_per_week'] = ran
			for i in range(1,8):  
				inr = 'start_date'+str(i) 
				inr_1 = 'end_date'+str(i)	
				value[inr_1] = ''
				value[inr] = ''
				value['day_'+str(i)] = ''
				value['include_'+str(i)] = False
			value['start_date1'] = start_date
			value['end_date1'] = end.strftime("%Y-%m-%d %H:%M:%S")
			value['day_1'] = pytz.utc.localize(start).astimezone(tz).strftime("%A")[:3]
			value['include_1'] = True
			for i in range(2,ran+1): 
				start_date = datetime.strptime(str(start_date),"%Y-%m-%d %H:%M:%S") + relativedelta(days=1)
				end = datetime.strptime(str(end),"%Y-%m-%d %H:%M:%S") + relativedelta(days=1)
				inr = 'start_date'+str(i)
				inr_1 = 'end_date'+str(i)
				value[inr] = start_date.strftime("%Y-%m-%d %H:%M:%S")
				value[inr_1] = end.strftime("%Y-%m-%d %H:%M:%S")
				value['day_'+str(i)] = pytz.utc.localize(start_date).astimezone(tz).strftime("%A")[:3]
				value['include_'+str(i)] = True
			return {'value': value}
		else:
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
		
	
	def onchange_duration(self, cr, uid, ids, start_date, duration=False, end_date=False, total_hrs=False, context=None):
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
			
		if duration and total_hrs:
			sessions_duration_in_hrs = duration
			if sessions_duration_in_hrs > 0 :
				if total_hrs % sessions_duration_in_hrs == 0 :
					value['total_sessions'] = total_hrs/sessions_duration_in_hrs
				else:
					value['total_sessions'] = (total_hrs/sessions_duration_in_hrs)+1
			else :
				value['total_sessions'] = 0
			
		
		return {'value': value}
	
	def on_change_room_id(self, cr, uid, ids, room_id):
		if room_id == False :
			return{}
		room_obj = self.pool.get('room').browse(cr, uid, room_id)
		if len(ids) <= 0 :
			return {'value': {'room1': room_obj.name, 'room2': room_obj.name, 'room3': room_obj.name, 'room4': room_obj.name, 'room5': room_obj.name, 'room6': room_obj.name, 'room7': room_obj.name}}
		else :
			location_obj = self.browse(cr, uid, ids[0])
			if location_obj['week_no'] == 1 :
				user = self.pool.get('res.users').browse(cr, uid, uid)
				tz = pytz.timezone(user.tz) if user.tz else pytz.utc
				day = pytz.utc.localize(datetime.strptime(str(location_obj['start_date']),"%Y-%m-%d %H:%M:%S")).astimezone(tz).strftime("%A")[:3]
				for k in range(1,8):
					if location_obj['include_'+str(k)] == True:
						if location_obj['day_'+str(k)] == day:
							return {'value': {'room'+str(k): room_obj.name}}
			else :
			 return {'value': {'room_id': room_obj.id}}
		
class_info


class move_learner(osv.osv):

	def move_learner_save(self, cr, uid, ids, context=None): 
		learner_array = context.get('learner_id')
		for self_obj in self.browse(cr,uid,ids):
			if self_obj.available_seats > len(learner_array) :
				class_info = self.pool.get('class.info')
				
				for learner_id in context.get('learner_id') :
					self.pool.get('learner.line').create(cr, uid,{'learner_mod_id':self_obj.class_id.id,'learner_id':learner_id}, context=context)
			
				class_obj = class_info.browse(cr,uid,context.get('class_id'))
				parent_id = class_obj['parent_id']
				if parent_id > 0:
					prog_mod_ids = class_info.search(cr, uid, [('parent_id', '=', parent_id)])
					prog_mod_ids.append(parent_id)
				else:
					prog_mod_ids = class_info.search(cr, uid, [('parent_id', '=', class_obj.id)])
					prog_mod_ids.append(class_obj.id)
			
				from_to_ids = self.pool.get('learner.line').search(cr,uid,[('learner_mod_id','in',prog_mod_ids),('learner_id','in',context.get('learner_id'))])
				
				self.pool.get('learner.line').unlink(cr, uid, from_to_ids, context)
			else:
				raise osv.except_osv(_('Error!'),_("Cannot move learners as available seats are low"))
		
		
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'class_form')
		view_id = view_ref and view_ref[1] or False,
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'active_id': ids[0]
		})
		return {
			'type': 'ir.actions.act_window',
			'name': 'Class',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': view_id,
			'res_model': 'class.info',
			'res_id':context.get('active_id'),
			'nodestroy': True,
			'target':'current',
			'context': ctx,
		}
	
	def move_learner_cancel(self, cr, uid, ids, context=None): 
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'class_form')
		view_id = view_ref and view_ref[1] or False,
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'active_id': ids[0]
		})
		return {
			'type': 'ir.actions.act_window',
			'name': 'Class',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': view_id,
			'res_model': 'class.info',
			'res_id':context.get('active_id'),
			'nodestroy': True,
			'target':'current',
			'context': ctx,
		}
	
	
	def default_get(self, cr, uid, fields, context=None):
		data = super(move_learner, self).default_get(cr, uid, fields, context=context)
		data['module_id']=context.get('active_module')
		return data
	
	_name = "learner.move"
	_description = "Move Learner Line"
	_columns = {
		'name':fields.char('Name'),
		'learner_move_id': fields.many2one('class.info', 'Class', ondelete='cascade', help='Class', select=True),
		'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
		'class_id':fields.many2one('class.info', 'Class', ondelete='cascade', help='Learner', select=True, required=True),
		'parent_id': fields.related('class_id','parent_id',type="integer",relation="class.info",string="Parent Id", readonly=1, required=True),
		'class_code': fields.related('class_id','class_code',type="char",relation="class.info",string="Class Code", readonly=1, required=True),
		'start_date': fields.related('class_id','start_date',type="datetime",relation="class.info",string="Start Date", readonly=1, required=True),
		'end_date': fields.related('class_id','start_date',type="datetime",relation="class.info",string="End Date", readonly=1, required=True),
		'available_seats':fields.integer('Available Slots', readonly=1),
	}
	
	def onchange_class(self, cr, uid, ids, class_id,module_id):
		class_obj = self.pool.get('class.info').browse(cr, uid, class_id)
		module_obj = self.pool.get('cs.module').browse(cr, uid, module_id)
		avail = module_obj.max_num_ppl_class - class_obj.no_of_learners
		return {'value': {'class_code': class_obj.class_code,'start_date': class_obj.start_date,'end_date': class_obj.end_date,'available_seats': avail}}
	
	def onchange_module(self, cr, uid, ids, module_id,class_id):
		module_obj = self.pool.get('cs.module').browse(cr, uid, module_id)
		class_obj = self.pool.get('class.info').browse(cr, uid, class_id)
		avail = module_obj.max_num_ppl_class - class_obj.no_of_learners
		return {'value': {'available_seats': avail}}
		

move_learner

class learner_mod_line(osv.osv):
	def _check_unique_learner(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.learner_mod_id == self_obj.learner_mod_id and x.learner_id == self_obj.learner_id:
						return False
		return True
	
	def create(self,cr, uid, values, context=None):
		global class_create
		if class_create == True :
			id = super(learner_mod_line, self).create(cr, uid, values, context=context)
			return id
		id = super(learner_mod_line, self).create(cr, uid, values, context=context)
		class_id = values['learner_mod_id']
		class_info_obj = self.pool.get('class.info')
		class_info_obj_id = class_info_obj.browse(cr,uid,class_id)
		parent_id = class_info_obj_id['parent_id']
		if parent_id > 0:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', parent_id)])
			ids = class_info_obj.search(cr, uid, [('id', '=', parent_id)])
			prog_mod_ids.append(ids[0])
		else:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', class_info_obj_id.id)])
			prog_mod_ids.append(class_info_obj_id.id)
			
		for prog_module_line in prog_mod_ids:
			if prog_module_line != class_id:
				new_array = values
				new_array['learner_mod_id'] = prog_module_line
				new_array['attendance'] = False
				super(learner_mod_line, self).create(cr, uid, new_array, context=context)
		return id
		
	def write(self,cr, uid, ids, values, context=None):
		id = super(learner_mod_line, self).write(cr, uid, ids,values, context=context)
		values_obj = self.browse(cr,uid,ids,context)[0]
		class_id = values_obj['learner_mod_id']
		
		parent_id = class_id['parent_id']
		if parent_id > 0:
			prog_mod_ids = self.pool.get('class.info').search(cr, uid, [('parent_id', '=', parent_id)])
			ids_1 = self.pool.get('class.info').search(cr, uid, [('id', '=', parent_id)])
			prog_mod_ids.append(ids_1[0])
		else:
			prog_mod_ids = self.pool.get('class.info').search(cr, uid, [('parent_id', '=', class_id.id)])
			prog_mod_ids.append(class_id.id)
		line_ids = self.search(cr,uid,[('learner_mod_id','in',prog_mod_ids)])
		for prog_module_line in self.browse(cr,uid,line_ids,context):
			if prog_module_line.id != class_id.id:
				if 'attendance' in values :
					del values['attendance']
				
				super(learner_mod_line, self).write(cr, uid, prog_module_line.id,values, context=context)
		return id
		
	def on_change_learner_id(self, cr, uid, ids, learner_id):
		module_obj = self.pool.get('learner.info').browse(cr, uid, learner_id)
		return {'value': {'name': module_obj.name, 'learner_nric': module_obj.learner_nric}}
	
	_name = "learner.line"
	_description = "Learner Line"
	_columns = {
		'learner_mod_id': fields.many2one('class.info', 'Class', ondelete='cascade', help='Class', select=True),
		'learner_id':fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner', select=True, required=True),
		'learner_nric': fields.related('learner_id','learner_nric',type="char",relation="learner.info",string="Learner NRIC", readonly=1, required=True),
		'binder':fields.boolean('Binder'),
		'tablet':fields.boolean('Tablet'),
		'blended':fields.boolean('Blended'),
		'primary_mode':fields.selection((('Binder','Binder'),('Tablet','Tablet'),('Blended','Blended')),'Primary Mode'),
		'attendance':fields.boolean('Attendance'),
		'move':fields.boolean('Move'),
	}
	_constraints = [(_check_unique_learner, 'Error: Learner Already Exists', ['learner_id'])]
		
learner_mod_line()

class session_info(osv.osv):
	_name ='sess.info'
	_description ="Class Session Information"
	_columns = {
		'class_sess_id': fields.many2one('class.info', 'Class', ondelete='cascade', help='Class', select=True),
		'sess_no':fields.integer('Session No'),
		'week_no':fields.integer('Week No'),
		'sess_date':fields.char('Date'),
		'sess_issues':fields.char('Conflict Issues')
	}
session_info()

class trainers_line(osv.osv):
	
	def _check_unique_trainer(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.trainers_line_id == self_obj.trainers_line_id and x.trainer_id == self_obj.trainer_id:
						return False
		return True
	def update_status(self,cr, uid, ids, values, context=None):
		super(trainers_line, self).write(cr, uid, ids,values, context=context)
	
	def create(self,cr, uid, values, context=None):
		global class_create
		if class_create == True :
			id = super(trainers_line, self).create(cr, uid, values, context=context)
			return id
		id = super(trainers_line, self).create(cr, uid, values, context=context)
		class_id = values['trainers_line_id']
		class_info_obj = self.pool.get('class.info')
		class_info_obj_id = class_info_obj.browse(cr,uid,class_id)
		parent_id = class_info_obj_id['parent_id']
		if parent_id > 0:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', parent_id)])
			ids = class_info_obj.search(cr, uid, [('id', '=', parent_id)])
			prog_mod_ids.append(ids[0])
		else:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', class_info_obj_id.id)])
			prog_mod_ids.append(class_info_obj_id.id)
			
		for prog_module_line in prog_mod_ids:
			if prog_module_line != class_id:
				new_array = values
				new_array['trainers_line_id'] = prog_module_line
				super(trainers_line, self).create(cr, uid, new_array, context=context)
				
		return id
		
	def write(self,cr, uid, ids, values, context=None):
		id = super(trainers_line, self).write(cr, uid, ids,values, context=context)
		values_obj = self.browse(cr,uid,ids,context)[0]
		class_id = values_obj['trainers_line_id']
		
		parent_id = class_id['parent_id']
		if parent_id > 0:
			prog_mod_ids = self.pool.get('class.info').search(cr, uid, [('parent_id', '=', parent_id)])
			ids_1 = self.pool.get('class.info').search(cr, uid, [('id', '=', parent_id)])
			prog_mod_ids.append(ids_1[0])
		else:
			prog_mod_ids = self.pool.get('class.info').search(cr, uid, [('parent_id', '=', class_id.id)])
			prog_mod_ids.append(class_id.id)
		
		line_ids = self.search(cr,uid,[('trainers_line_id','in',prog_mod_ids)])
		for prog_module_line in self.browse(cr,uid,line_ids,context):
			if prog_module_line.id != class_id.id:
				super(trainers_line, self).write(cr, uid, prog_module_line.id,values, context=context)
		return id
		
	def trainer_confirm(self, cr, uid, ids, context=None): 
		super(trainers_line, self).write(cr, uid, ids[0],{'t_status':'Confirmed'}, context=context)
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		trainer_obj = self_obj['trainer_id']
		prog_mod_ids = []
		for le_obj in trainer_obj.assignment_avaliable:
			if le_obj.trainer_avail_id == trainer_obj.id :
				self.pool.get("trainers.assignment.avaliable").write(cr, uid, le_obj.id,{'status':'Confirmed'}, context=context)
		
		class_info_obj = self.pool.get('class.info')
		class_info_obj_id = class_info_obj.browse(cr,uid,self_obj['trainers_line_id'].id)
		parent_id = class_info_obj_id['parent_id']
		if parent_id > 0:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', parent_id)])
			ids = class_info_obj.search(cr, uid, [('id', '=', parent_id)])
			prog_mod_ids.append(ids[0])
		else:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', class_info_obj_id.id)])
			prog_mod_ids.append(class_info_obj_id.id)
		
		sub_lines = []
		values = {}
		sub_lines.append( (0,0, {'trainer':trainer_obj.name,'session_assigned':class_info_obj_id.sess_no,
			'date_of_assignment':class_info_obj_id.start_date,'single_session':True}) )
		values.update({'trainer_history': sub_lines})
		for prog_module_line in class_info_obj.browse(cr,uid,prog_mod_ids):
			self.pool.get("class.info").write(cr, uid, prog_module_line.id,values, context=context,holidays=True)
				
		
		
	def _calculate_total_session(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = 5
		return res
		
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(trainers_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	_name ='trainers.line'
	_description ="Trainer Line Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'trainers_line_id': fields.many2one('class.info', 'Class', ondelete='cascade', help='Class', select=True),
	'trainer_id':fields.many2one('trainer.profile.info', 'Trainer', ondelete='cascade', help='Trainer', select=True, required=True),
	't_status':fields.char('Status'),
	}
	_constraints = [(_check_unique_trainer, 'Error: Trainer Already Exists', ['trainers_line_id'])]
trainers_line()

class trainer_hist(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(trainer_hist, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	_name ='trainers.history'
	_description ="Trainer History Tab"
	_columns = {
	's_no' : fields.integer('S. No',size=20,readonly=1),
	'trainers_hist_id' : fields.integer('Id'),
	'trainer':fields.char('Trainer',size=25),
	'session_assigned':fields.char('Session Assigned',size=25),
	'date_of_assignment':fields.char('Date of Assignment',size=25),
	'single_session': fields.boolean('Single Session')
	}
trainer_hist()

class class_moi(osv.osv):
	def _check_unique_equp(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.class_moi_id.id == self_obj.class_moi_id.id and x.equip_list.id == self_obj.equip_list.id:
						return False
		return True
		
	def create(self,cr, uid, values, context=None):
		global class_create
		if class_create == True :
			id = super(class_moi, self).create(cr, uid, values, context=context)
			return id
		id = super(class_moi, self).create(cr, uid, values, context=context)
		class_id = values['class_moi_id']
		class_info_obj = self.pool.get('class.info')
		class_info_obj_id = class_info_obj.browse(cr,uid,class_id)
		parent_id = class_info_obj_id['parent_id']
		if parent_id > 0:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', parent_id)])
			ids = class_info_obj.search(cr, uid, [('id', '=', parent_id)])
			prog_mod_ids.append(ids[0])
		else:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', class_info_obj_id.id)])
			prog_mod_ids.append(class_info_obj_id.id)
			
		for prog_module_line in prog_mod_ids:
			if prog_module_line != class_id:
				new_array = values
				new_array['class_moi_id'] = prog_module_line
				super(class_moi, self).create(cr, uid, new_array, context=context)
				
		return id
		
	def write(self,cr, uid, ids, values, context=None):
		id = super(class_moi, self).write(cr, uid, ids,values, context=context)
		values_obj = self.browse(cr,uid,ids,context)[0]
		class_id = values_obj['class_moi_id']
		
		parent_id = class_id['parent_id']
		if parent_id > 0:
			prog_mod_ids = self.pool.get('class.info').search(cr, uid, [('parent_id', '=', parent_id)])
			ids_1 = self.pool.get('class.info').search(cr, uid, [('id', '=', parent_id)])
			prog_mod_ids.append(ids_1[0])
		else:
			prog_mod_ids = self.pool.get('class.info').search(cr, uid, [('parent_id', '=', class_id.id)])
			prog_mod_ids.append(class_id.id)
		line_ids = self.search(cr,uid,[('class_moi_id','in',prog_mod_ids)])
		for prog_module_line in self.browse(cr,uid,line_ids,context):
			if prog_module_line.id != class_id.id:
				super(learner_mod_line, self).write(cr, uid, prog_module_line.id,values, context=context)
		return id
		
	_name ='class.moi'
	_description ="People and Facilites Tab"
	_columns = {
	'equip_list':fields.many2one('master.equip', 'Equipment', ondelete='cascade', help='Equipments', select=True,required=True),
	'class_moi_id': fields.many2one('class.info', 'Class', ondelete='cascade', help='Class', select=True),
	}
	_constraints = [(_check_unique_equp, 'Error: Equipment Already Exists', ['equip_list'])]
class_moi()

class learner_asset(osv.osv):

	def _check_unique_learner(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.learner_asset_id == self_obj.learner_asset_id and x.learner_id == self_obj.learner_id:
						return False
		return True
		
	def on_change_learner_id(self, cr, uid, ids, learner_id):
		module_obj = self.pool.get('learner.info').browse(cr, uid, learner_id)
		return {'value': {'name': module_obj.name,'learner_nric': module_obj.learner_nric}}
		
	def create(self,cr, uid, values, context=None):
		id = super(learner_asset, self).create(cr, uid, values, context=context)
		class_id = values['learner_asset_id']
		class_info_obj = self.pool.get('class.info')
		class_info_obj_id = class_info_obj.browse(cr,uid,class_id)
		parent_id = class_info_obj_id['parent_id']
		if parent_id > 0:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', parent_id)])
			ids = class_info_obj.search(cr, uid, [('id', '=', parent_id)])
			prog_mod_ids.append(ids[0])
		else:
			prog_mod_ids = class_info_obj.search(cr, uid, [('parent_id', '=', class_info_obj_id.id)])
			prog_mod_ids.append(class_info_obj_id.id)
			
		for prog_module_line in prog_mod_ids:
			if prog_module_line != class_id:
				new_array = values
				new_array['learner_asset_id'] = prog_module_line
				super(learner_asset, self).create(cr, uid, new_array, context=context)
				
		return id
		
	def write(self,cr, uid, ids, values, context=None):
		id = super(learner_asset, self).write(cr, uid, ids,values, context=context)
		values_obj = self.browse(cr,uid,ids,context)[0]
		class_id = values_obj['learner_asset_id']
		
		parent_id = class_id['parent_id']
		if parent_id > 0:
			prog_mod_ids = self.pool.get('class.info').search(cr, uid, [('parent_id', '=', parent_id)])
			ids_1 = self.pool.get('class.info').search(cr, uid, [('id', '=', parent_id)])
			prog_mod_ids.append(ids_1[0])
		else:
			prog_mod_ids = self.pool.get('class.info').search(cr, uid, [('parent_id', '=', class_id.id)])
			prog_mod_ids.append(class_id.id)
		line_ids = self.search(cr,uid,[('learner_asset_id','in',prog_mod_ids)])
		for prog_module_line in self.browse(cr,uid,line_ids,context):
			if prog_module_line.id != class_id.id:
				super(learner_asset, self).write(cr, uid, prog_module_line.id,values, context=context)
		return id
	_name ='learner.asset'
	_description ="Learner Asset Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'learner_asset_id': fields.many2one('class.info', 'Class', ondelete='cascade', help='Class', select=True),
	'learner_id':fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner', select=True, required=True),
	'learner_nric': fields.related('learner_id','learner_nric',type="char",relation="learner.info",string="NRIC/FIN", readonly=1, required=True),
	'binder_issue_date':fields.date('Binder Issue Date'),
	'tablet_type': fields.char('Tablet Type',size=20),
	'tablet_serial_num': fields.char('Tablet Serial Number',size=20),
	'tablet_issue_date': fields.date('Tablet Issue Date'),
	'blended_type': fields.char('Blended Type',size=20),
	'blended_serial_number': fields.char('Blended Serial Number',size=20),
	'blended_issue_date': fields.date('Blended Issue Date'),
	}
	_constraints = [(_check_unique_learner, 'Error: Learner Already Exists', ['learner_id'])]
learner_asset()

class po_listing(osv.osv):
	_name ='trainers.po.listing'
	_description ="Trainer PO Listing Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'po_no':fields.char('PO NO',size=25),
	'item_type':fields.char('Item Type',size=25),
	'po_create_date':fields.date('PO Create Date'),
	'tablet_type': fields.char('Tablet Type',size=20),
	'supplier': fields.char('Supplier',size=20),
	'total': fields.float('Total',size=10),
	'by_whom': fields.char('By Whom',size=20),
	}
po_listing()

class class_history(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(class_history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	_name ='class.history'
	_description ="Class History"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'history_id':fields.integer('Id',size=20),
	'date_created':fields.char('Date Created',size=20),
	'created_by':fields.char('Created By',size=20),
	'last_update':fields.char('Last Update',size=20),
	'last_update_by':fields.char('Last Update By',size=20),
	'date_status_change':fields.char('Date Of Status Change',size=20),
	'status_change_by':fields.char('Status Change By',size=20),
	'changes':fields.char('Changes',size=200)
	}
class_history()