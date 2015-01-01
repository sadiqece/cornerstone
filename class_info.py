from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class class_info(osv.osv):
	_name = "class.info"
	_description = "This table is for keeping location data"
	_columns = {
		'asset_id': fields.char('Id',size=20),
		'name': fields.char('Class Name', size=100,required=True, select=True),
		'class_code': fields.char('Class Code', size=20, readonly=1),
		'location_id':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'loc_id': fields.many2one('location', 'Location', ondelete='cascade', help='Location'),
		'room_id':fields.many2one('room', 'Rooms', ondelete='cascade', help='Room', select=True, required=True),
		'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True, required=True),
		'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module'),
		'start_date': fields.date('Start Date'),
		'start_time': fields.float('Start Time', size=3),
		'end_date': fields.date('End Date'),
		'end_time': fields.float('End Time', size=3),
		'location_schedule': fields.one2many('schedule.location','s_no',type='integer'),
		'sessions_per_week': fields.integer('Number of Sessions Per Week', size=7),
		'sessions_duration_in_hrs': fields.integer('Sessions Durations in Hours',readonly=1),
		'total_hrs': fields.integer('Total Hours', readonly=1),
		'total_sessions': fields.integer('Total Sessions', readonly=1),
		'total_weeks': fields.integer('Total Weeks', readonly=1),
		'day_1':fields.char('Day 1',readonly=1),
		'day_2':fields.char('Day 2',readonly=1),
		'day_3':fields.char('Day 3',readonly=1),
		'day_4':fields.char('Day 4',readonly=1),
		'day_5':fields.char('Day 5',readonly=1),
		'day_6':fields.char('Day 6',readonly=1),
		'day_7':fields.char('Day 7',readonly=1),
		'start_date': fields.date(),
		'start_date2': fields.date(),
		'start_date3': fields.date(),
		'start_date4': fields.date(),
		'start_date5': fields.date(),
		'start_date6': fields.date(),
		'start_date7': fields.date(),
		'end_date1': fields.date(),
		'end_date2': fields.date(),
		'end_date3': fields.date(),
		'end_date4': fields.date(),
		'end_date5': fields.date(),
		'end_date6': fields.date(),
		'end_date7': fields.date(),
		'start_time1': fields.float(),
		'start_time2': fields.float(),
		'start_time3': fields.float(),
		'start_time4': fields.float(),
		'start_time5': fields.float(),
		'start_time6': fields.float(),
		'start_time7': fields.float(),
		'end_time1': fields.float(),
		'end_time2': fields.float(),
		'end_time3': fields.float(),
		'end_time4': fields.float(),
		'end_time5': fields.float(),
		'end_time6': fields.float(),
		'end_time7': fields.float(),
		'room1': fields.char('Room'),
		'room2': fields.char('Room'),
		'room3': fields.char('Room'),
		'room4': fields.char('Room'),
		'room5': fields.char('Room'),
		'room6': fields.char('Room'),
		'room7': fields.char('Room'),
		'trainer_broadcast': fields.one2many('trainers.broadcast', 's_no', 'Broadcast'),
		'trainer_history': fields.one2many('trainers.history', 's_no', 'Trainer Assigment History'),
		'delivery_mode': fields.selection((('English','English'),('Singli','Singli'),('Malyi','Malyi')),'Delivery Mode'),
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
	}
	_defaults = { 
		'class_code': 'XXX-XXX-XXX',
	}
	
	def on_change_module_id(self, cr, uid, ids, module_id):
		module_obj = self.pool.get('cs.module').browse(cr, uid, module_id)
		return {'value': {'module_code': module_obj.module_code,'no_of_hrs':module_obj.module_duration}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('program.module.line')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['module_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'name': _('Module'),
		'res_model': 'cs.module',
		'view_type': 'form',
		'res_id': module_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,
		}
		
	def on_change_room_id(self, cr, uid, ids, room_id):
		room_obj = self.pool.get('room').browse(cr, uid, room_id)
		return {'value': {'s_no': room_obj.s_no, 'room_floor_area': room_obj.room_floor_area,'room_setup':room_obj.room_setup,'room_max_cap':room_obj.room_max_cap}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'room_form')
		view_id = view_ref and view_ref[1] or False
		loc_room_obj = self.pool.get('location.room.line')
		loc_room_ids = loc_room_obj.search(cr, uid, [('id', '=', ids[0])])
		room_ids =[]
		for loc_room_line in loc_room_obj.browse(cr, uid, loc_room_ids,context=context):
			room_ids.append(loc_room_line['room_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'name': _('Room'),
		'res_model': 'room',
		'view_type': 'form',
		'res_id': room_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,
		}
		
	def on_change_location_id(self, cr, uid, ids, location_id):
		location_obj = self.pool.get('location').browse(cr, uid, location_id)
		return {'value': {'location_code': location_obj.location_code}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'location_form')
		view_id = view_ref and view_ref[1] or False
		loc_mod_obj = self.pool.get('location.room.line')
		loc_mod_ids = loc_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		location_ids =[]
		for loc_module_line in loc_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			location_ids.append(loc_module_line['location_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'name': _('Location'),
		'res_model': 'location',
		'view_type': 'form',
		'res_id': location_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,
		}
	
class_info

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