from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

class location(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(location, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	def _calculate_total_room(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		#_logger.info('Adding rooms %s', mod_line_ids)
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = self.browse(cr, uid, line.id, context=context).location_room_line or []
			_logger.info('Adding rooms %s', mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
				
		return res
		
		

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
		
	def _check_unique_code(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.location_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.location_code and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.location_code and self_obj.location_code.lower() in  lst:
				return False
		return True
		
	def on_change_location_type(self, cr, uid, ids, location_type):
		val = {}
		val['location_type_permanent'] = False
		val['location_type_temporary'] = False		
		if location_type == 'Permanent':
			val['location_type_permanent'] = True
		elif location_type == 'Temporary':
			val['location_type_temporary'] = True
			
		return {'value': val}
		
	def on_change_postalcode(self, cr, uid, ids, location_postal_code):
		if location_postal_code < 0:
			raise osv.except_osv(_('Error!'),_("Value - Cannot be negative value"))
		return location_postal_code
		
	def on_change_contactnum(self, cr, uid, ids, location_contact_no):
		if location_contact_no < 0:
			raise osv.except_osv(_('Error!'),_("Value - Cannot be negative value"))
		return location_contact_no
	
	_name = "location"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100),
		'location_id': fields.char('Id',size=20),
		'name': fields.char('Location Name', size=100,required=True, select=True),
		'location_code': fields.char('Location Code', size=20),
		'location_type': fields.selection((('Permanent','Permanent'),('Temporary','Temporary')),'Type'),
		'location_type_permanent': fields.boolean('Permanent'),
		'location_type_temporary': fields.boolean('Temporary'),
		'location_address':fields.text('Location', size=150, select=True),
		'location_postal_code':fields.integer('Postal Code', size=6),
		'location_contact_no':fields.integer('Contact', size=9),
		'location_room_line': fields.one2many('room', 'location_id', 'Room Lines', select=True, required=True),
		'no_of_rooms': fields.function(_calculate_total_room, relation="room", readonly=1, string='Number of Rooms', type='integer'),
	}
	_defaults = {
		'location_type': 'Permanent'
	}
	_constraints = [(_check_unique_name, 'Error: Location Name Already Exists', ['name']),(_check_unique_code, 'Error: Location Code Already Exists', ['location_code'])]
location()


class room(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(room, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
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
		
	def _check_unique_code(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.room_number.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.room_number and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.room_number and self_obj.room_number.lower() in  lst:
				return False
		return True
		
	def on_change_location_id(self, cr, uid, ids, location_id):
		location_obj = self.pool.get('location').browse(cr, uid, location_id)
		return {'value': {'name':location_obj.name,'location_code':location_obj.location_code}}
		
	def _load_loc_line(self, cr, uid, ids, field_names, args,  context=None):
		prog_mod_obj = self.pool.get('location.room.line')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('location_id', '=', ids[0])])
		module_ids =[]
		for location_room_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(location_room_line['location_id'].id)
		
		value_ids = self.pool.get('location').search(cr, uid, [('location_id', 'in', module_ids)])
		return dict([(id, value_ids) for id in ids])
		
	def on_change_maxcap(self, cr, uid, ids, room_max_cap):
		if room_max_cap < 0:
			raise osv.except_osv(_('Error!'),_("Value - Cannot be negative value"))
		return room_max_cap
		
	def on_change_floorarea(self, cr, uid, ids, room_floor_area):
		if room_floor_area < 0:
			raise osv.except_osv(_('Error!'),_("Value - Cannot be negative value"))
		return room_floor_area
		
		
	_name = "room"
	_description = "This table is for keeping room data"
	_columns = {
		's_no': fields.integer('S.No', size=100),
		'room_id': fields.integer('Id',size=20),
		'name': fields.char('Room Name', size=100,required=True, select=True),
		'room_number': fields.char('Room Number', size=20),
		'location_id':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, readonly=1),
		'location_name': fields.function(_load_loc_line, relation="location_room_line",readonly=1,type='one2many', string='Module'),
		'room_setup':fields.selection((('Cluster','Cluster'),('Class Room','Class Room'),('Theater','Theater'),('Test Only Room','Test Only Room')),'Setup'),
		'room_floor_area':fields.integer('Floor Area (sqm)', size=5,required=True, select=True),
		'room_max_cap':fields.integer('Maximum Capacity', size=7,required=True, select=True),
		'room_equip': fields.one2many('room.equip', 'equip_id', 'Equipments', select=True, required=True),
	}
	
	def on_change_location_id(self, cr, uid, ids, location_id):
		location_obj = self.pool.get('location').browse(cr, uid, location_id)
		return {'value': {'name':location_obj.name, 'location_code': location_obj.location_code}}
		
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
	
	_defaults = {
		'room_setup': 'Class Room',
	}
	
	def on_change_location_id(self, cr, uid, ids, location_id):
		location_obj = self.pool.get('location').browse(cr, uid, location_id)
		return {'value': {'name':location_obj.name,'location_code':location_obj.location_code}}
	
	_constraints = [(_check_unique_name, 'Error: Room Name Already Exists', ['name']),(_check_unique_code, 'Error: Room Code Already Exists', ['room_number'])]
room()

class location_room_line(osv.osv):
	def _check_unique_room(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.location_room_id == self_obj.location_room_id and x.room_id == self_obj.room_id:
						return False
		return True
		
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(location_room_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def on_change_maxcap(self, cr, uid, ids, room_max_cap):
		if room_max_cap < 0:
			raise osv.except_osv(_('Error!'),_("Value - Cannot be negative value"))
		return room_max_cap
		
	def on_change_floorarea(self, cr, uid, ids, room_floor_area):
		if room_floor_area < 0:
			raise osv.except_osv(_('Error!'),_("Value - Cannot be negative value"))
		return room_floor_area

	
	_name = "location.room.line"
	_description = "Room Line"
	_columns = {
		'location_room_id': fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True),
		's_no': fields.integer('S.No', size=100,readonly=1),
		'name': fields.related('room_id','name',type="char",relation="room",string="Room Name", readonly=1),
		'room_id':fields.many2one('room', 'Rooms', ondelete='cascade', help='Room', select=True, required=True),
		'room_number': fields.related('room_id','room_number',type="integer",relation="room",string="Room Code", readonly=1),
		'room_floor_area': fields.related('room_id','room_floor_area',type="integer",relation="room",string="Size(SqM)", readonly=1),
		'room_setup': fields.related('room_id','room_setup',type="char",relation="room",string="Default Setup", readonly=1),
		'room_max_cap': fields.related('room_id','room_max_cap',type="integer",relation="room",string="Max Capacity", readonly=1),
		#'room_equipmnt': fields.one2many('room.equip', 'equip_id', 'Equipments', select=True, required=True),
	}
	_constraints = [(_check_unique_room, 'Error: Room Already Exists', ['room_id'])]
		
	def on_change_room_id(self, cr, uid, ids, room_id):
		room_obj = self.pool.get('room').browse(cr, uid, room_id)
		return {'value': {'room_number': room_obj.room_number,'room_floor_area': room_obj.room_floor_area,'room_setup':room_obj.room_setup,'room_max_cap':room_obj.room_max_cap}}
		
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
location_room_line() 

class equip(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(equip, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		

	'''def _check_unique_equp(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.mod_id == self_obj.mod_id and x.equip_list == self_obj.equip_list:
						return False
		return True	'''

	def _check_unique_equip(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.equip_id == self_obj.equip_id and x.equip_list == self_obj.equip_list:
						return False
		return True	

			
	_name = "room.equip"
	_description = "Room Line"
	_columns = {
		'equip_id': fields.integer('Id', size=100, readonly=1),
		's_no': fields.integer('S.No', size=100, readonly=1),
		'equip_list':fields.many2one('master.equip', 'Equipment', ondelete='cascade', help='Equipments', select=True, required=True),
		'mod_id': fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
	}
	_constraints = [(_check_unique_equip, 'Error: Equipment Already Exists', ['equip_list'])]
equip()

