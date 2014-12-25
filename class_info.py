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
		
	_name = "class.info"
	_description = "This table is for keeping location data"
	_columns = {
		'class_id': fields.integer('Id',size=20),
		'parent_id': fields.integer('Parent Id',size=20),
		'name': fields.char('Class Name', size=100,required=True, select=True),
		'class_code': fields.char('Class Code',size=40), 
		'location_id':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'room_id':fields.many2one('room', 'Rooms', ondelete='cascade', help='Room', select=True, required=True),
		'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
		'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module'),
		'start_date': fields.datetime('Start Date'),
		'end_date': fields.datetime('End Date'),
		'duration': fields.float('Duration(Hrs)'),
		'location_schedule': fields.one2many('schedule.location','s_no',type='integer'),
		'sessions_per_week': fields.integer('Number of Sessions Per Week', size=7),
		'sessions_duration_in_hrs': fields.float('Sessions Durations in Hours'),
		'total_hrs': fields.integer('Total Hours', readonly=1),
		'total_sessions': fields.integer('Total Sessions', readonly=1),
		'total_weeks': fields.integer('Total Weeks', readonly=1),
		'sess_info_line': fields.function(_property_expense_preset_expenses,type='one2many',obj="class.info",method=True,string='Expenses'),
		'sess_info_line1': fields.function(_property_expense_preset_expenses1,type='one2many',obj="class.info",method=True,string='Expenses'),
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
		'trainer_broadcast': fields.one2many('trainers.broadcast', 's_no', 'Broadcast'),
		'trainer_history': fields.one2many('trainers.history', 's_no', 'Trainer Assigment History'),
		'delivery_mode': fields.selection((('English','English'),('Singli','Singli'),('Malyi','Malyi')),'Delivery Mode'),
		'learner_line': fields.one2many('learner.line', 'learner_mod_id', 'Order Lines', select=True, required=True),
		'binder_in_use':fields.boolean('Binder'),
		'tablet_in_use':fields.boolean('Tablet'),
		'primary': fields.selection((('Binder','Binder'),('Tablet','Tablet')),'Primary'),
		'pf_line': fields.one2many('pf.module','mod_id','Equipment List'),
		'room_arr': fields.selection((('Default','Default'),('Active','Active')),'Room Arrangment'),
		'trainer_learner': fields.one2many('trainers.learner', 's_no', 'Learner'),
		'trainer_asset': fields.one2many('trainers.asset','s_no','Asset'),
		'non_std_items': fields.selection((('Food','Food'),('Materials','Materials'),('Learning Assets','Learning Assets'),('Rooms','Rooms')),'Items'),
		'trainer_po_listing': fields.one2many('trainers.po.listing', 's_no', 'PO Listing'),
		'history_tab': fields.one2many('history', 's_no', 'History'),
		'sess_no':fields.integer('Session No'),
		'week_no':fields.integer('Week No'),
		'sess_issues':fields.char('Conflict Issues'),
		'apply_all':fields.boolean('Apply to All'),
	}
	_order = "start_date"
	
	def create(self,cr, uid, values, context=None):
		no_of_sess = 0
		parent_id =0
		include_array = []
		value_array =[]
		values['create_mode'] = False
		''' check for conflict now'''
		holiday = self.pool.get('holiday')
		holiday_obj_id = holiday.search(cr, uid, [('year', '=', datetime.now().year)])
		holiday_obj = holiday.browse(cr,uid,holiday_obj_id,context)
		
		holiday_list = []
		holiday_line = self.pool.get('holiday.line')
		holiday_line_obj_id = holiday_line.search(cr, uid, [('holiday_line_id', '=',holiday_obj[0]['id'])])
		for holiday_line_obj in holiday_line.browse(cr,uid,holiday_line_obj_id,context) :
			holiday_list.append(holiday_line_obj['date_start']+";"+holiday_line_obj['date_end']+";"+holiday_line_obj['description'])
			
		''' room conflicts'''
		room_conflict_ids = self.search(cr,uid,[('room_id',"=",values['room_id']),('start_date',">=",values['start_date'])])	
		for room_line_obj in self.browse(cr,uid,room_conflict_ids,context) :
			_logger.info('Installing chart of edit_class_confirm %s', room_line_obj)
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
						_logger.info('Installing chart of t1start %s', t1start)
						_logger.info('Installing chart of t1end %s', t1end)
						_logger.info('Installing chart of t2start %s', t2start)
						_logger.info('Installing chart of t2end %s', t2end)
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
			
		
		return id
		
	def write(self,cr, uid, ids, values, context=None):
		apply = False;
		location_obj = self.browse(cr, uid, ids[0])
		if 'apply_all' not in values :
			apply = location_obj['apply_all']
		else :
			apply = values['apply_all']
		
		if apply == True :
			parent_id = location_obj['parent_id']
			parent_obj = self.browse(cr, uid, parent_id,context=context)
			if 'start_date' in values :
				duration  = 1.00
				if 'duration' in values :
				   duration = values['duration']
				else :
					duration = location_obj['duration']
					
				st_time = str(values['start_date']).split()[1]
				str_dt = str(parent_obj['start_date']).split()[0]
				start = datetime.strptime(str(str_dt)+' '+str(st_time),"%Y-%m-%d %H:%M:%S")
				end = start + timedelta(hours=duration)
				end_dt = end.strftime("%Y-%m-%d %H:%M:%S")
				date_array = {}
				date_array['start_date'] = str(str_dt)+' '+str(st_time) 
				date_array['end_date'] = end_dt 
				date_array['start_date1'] = str(str_dt)+' '+str(st_time) 
				date_array['end_date1'] = end_dt 
				
				user = self.pool.get('res.users').browse(cr, uid, uid)
				tz = pytz.timezone(user.tz) if user.tz else pytz.utc
				ran = 7 - pytz.utc.localize(start).astimezone(tz).weekday()
				
				for j in range(2,ran+1) :
					date_array['start_date'+str(j)] = str(start + relativedelta(days=j-1))
					date_array['end_date'+str(j)] = str(end + relativedelta(days=j-1))
				
				
				super(class_info, self).write(cr, uid, parent_id,date_array, context=context)
				
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
					for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
						str_dt = str(prog_module_line['start_date']).split()[0]
						start = datetime.strptime(str(str_dt)+' '+str(st_time),"%Y-%m-%d %H:%M:%S")
						end = start + timedelta(hours=duration)
						end_dt = end.strftime("%Y-%m-%d %H:%M:%S")
						date_array['start_date'] = str(str_dt)+' '+str(st_time)
						date_array['end_date'] = end_dt 
						super(class_info, self).write(cr, uid, prog_module_line.id,date_array, context=context)
						
			if 'room_id' in values :
				room_obj = self.pool.get('room').browse(cr, uid, values['room_id'])
				room_array = {'room1': room_obj.name, 'room2': room_obj.name, 'room3': room_obj.name, 'room4': room_obj.name, 'room5': room_obj.name, 'room6':room_obj.name, 'room7': room_obj.name}
				room_array['room_id'] = values['room_id']
				super(class_info, self).write(cr, uid, parent_id,room_array, context=context)
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
					for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
						room_array = {'room1': room_obj.name, 'room2': room_obj.name, 'room3': room_obj.name, 'room4': room_obj.name, 'room5': room_obj.name, 'room6': room_obj.name, 'room7': room_obj.name}
						room_array['room_id'] = values['room_id']
						super(class_info, self).write(cr, uid, prog_module_line.id,room_array, context=context)
						_logger.info('Installing chart of str_date %s', prog_module_line['room_id'])
						
			if 'location_id' in values :
				super(class_info, self).write(cr, uid, parent_id,{'location_id': values['location_id']}, context=context)
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
					for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
						super(class_info, self).write(cr, uid, prog_module_line.id,{'location_id': values['location_id']}, context=context)
						
			if 'module_id' in values :
				super(class_info, self).write(cr, uid, parent_id,{'module_id': values['module_id']}, context=context)
				if parent_id > 0:
					prog_mod_ids = self.search(cr, uid, [('parent_id', '=', parent_id)])
					for prog_module_line in self.browse(cr, uid, prog_mod_ids,context=context):
						super(class_info, self).write(cr, uid, prog_module_line.id,{'module_id': values['module_id']}, context=context)
					
		module_id = super(class_info, self).write(cr, uid, ids,values, context=context)
		return module_id
    
		
	
	
	def on_change_module_id(self, cr, uid, ids, module_id):
		module_obj = self.pool.get('cs.module').browse(cr, uid, module_id)
		return {'value': {'total_hrs': module_obj.module_duration}}
	
	
	
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
				if apply_include == True :
					value['include_'+str(i)] = False
			value['start_date1'] = start_date
			value['end_date1'] = end.strftime("%Y-%m-%d %H:%M:%S")
			value['day_1'] = pytz.utc.localize(start).astimezone(tz).strftime("%A")[:3]
			if apply_include== True :
				value['include_1'] = True
			for i in range(2,ran+1): 
				start_date = datetime.strptime(str(start_date),"%Y-%m-%d %H:%M:%S") + relativedelta(days=1)
				end = datetime.strptime(str(end),"%Y-%m-%d %H:%M:%S") + relativedelta(days=1)
				inr = 'start_date'+str(i)
				inr_1 = 'end_date'+str(i)
				value[inr] = start_date.strftime("%Y-%m-%d %H:%M:%S")
				value[inr_1] = end.strftime("%Y-%m-%d %H:%M:%S")
				value['day_'+str(i)] = pytz.utc.localize(start_date).astimezone(tz).strftime("%A")[:3]
				if apply_include == True :
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

class edit_class_confirm(osv.osv):

	_name = "edit.class.confirm"
	_description = "Edit Class Confirm"

	def action_confirm(self,cr,uid,ids,context=None):
		#print'lol wut?'
		_logger.info('Installing chart of edit_class_confirm %s', ids)
		data={'Message': 'Vous avez depasse le nombre de jour max a detailler!','value':1}
		if context is None: context = {}
		#print 'wizard_id : ', wizard_id
		return {
			'name':_("Attention"),
			'view_mode': 'form',
			'view_id': False,
			'view_type': 'form',
			'res_model': 'edit.class.confirm',
			'type': 'ir.actions.act_window',
			'nodestroy': True,
			'target': 'new',
			'domain': '[]',
			'context': context
		}
edit_class_confirm()


class learner_mod_line(osv.osv):
	def _check_unique_learner(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.learner_mod_id == self_obj.learner_mod_id and x.learner_id == self_obj.learner_id:
						return False
		return True
	
	_name = "learner.line"
	_description = "Learner Line"
	_columns = {
		'learner_mod_id': fields.many2one('class.info', 'Class', ondelete='cascade', help='Class', select=True),
		'learner_id':fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner', select=True, required=True),
		'learner_nric': fields.related('learner_id','learner_nric',type="char",relation="learner.info",string="Learner NRIC", readonly=1, required=True),
	}
	_constraints = [(_check_unique_learner, 'Error: Learner Already Exists', ['learner_id'])]
	
	
		
	def on_change_learner_id(self, cr, uid, ids, learner_id):
		module_obj = self.pool.get('learner.info').browse(cr, uid, learner_id)
		return {'value': {'learner_nric': module_obj.learner_nric}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'learner_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('learner.line')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['learner_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'name': _('Module'),
		'res_model': 'learner.info',
		'view_type': 'form',
		'res_id': module_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,
		}

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



class trainer_broad(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(trainer_broad, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	_name ='trainers.broadcast'
	_description ="Assignment Available Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'trainer':fields.char('Trainer',size=25),
	'attendance':fields.boolean('Attendance'),
	'confirmation':fields.boolean('Confirmation')
	}
trainer_broad()

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
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'trainer':fields.char('Trainer',size=25),
	'session_assigned':fields.char('Session Assigned',size=25),
	'date_of_assignment':fields.char('Date of Assignment',size=25),
	'single_session': fields.boolean('Single Session')
	}
trainer_hist()

class master_equip(osv.osv):
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
	_name ='master.equip'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Equipment',size=20),
	}
	_constraints = [(_check_unique_name, 'Error: This Equipment Already Exists', ['name'])]
master_equip()   

class peoplefac(osv.osv):
	def _check_unique_equp(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.equip_list == self_obj.equip_list:
						return False
		return True
	_name ='pf.module'
	_description ="People and Facilites Tab"
	_columns = {
	'pf_id':fields.integer('S.No',size=20),
	'equip_list':fields.many2one('master.equip', 'Equipment', ondelete='cascade', help='Equipments', select=True,required=True),
	'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
	}
	_constraints = [(_check_unique_equp, 'Error: Equipment Already Exists', ['equip_list'])]
peoplefac()

class learner(osv.osv):
	_name ='trainers.learner'
	_description ="Trainer Learner Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'name':fields.char('Name',size=25),
	'nric_fin':fields.char('NRIC/FIN',size=25),
	'learning_mode':fields.char('Learning Mode',size=25),
	'attendance': fields.boolean('Attendance'),
	'move': fields.boolean('Move'),
	}
learner()

class asset(osv.osv):
	_name ='trainers.asset'
	_description ="Trainer Asset Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'name':fields.char('Name',size=25),
	'nric_fin':fields.char('NRIC/FIN',size=25),
	'blinder_issue_date':fields.date('Blinder issue Date'),
	'tablet_type': fields.char('Tablet Type',size=20),
	'tablet_serial_num': fields.char('Tablet Serial Number',size=20),
	'tablet_issue_date': fields.date('Tablet Issue Date'),
	'blended_type': fields.char('Blended Type',size=20),
	'blended_serial_number': fields.char('Blended Serial Number',size=20),
	'blended_issue_date': fields.date('Blended Issue Date'),
	}
asset()

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

class history(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	_name ='history'
	_description ="Trainer History"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'action':fields.char('Action',size=25),
	'date_time':fields.datetime('Date/Time'),
	'action_by':fields.char('Action By',size=20),
	}
history()