from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

_logger = logging.getLogger(__name__)

global dupliacte_order_priority_found
dupliacte_order_priority_found = False	

global dupliacte_unit_found
dupliacte_unit_found = False

global dupliacte_order_priority_found_create
dupliacte_order_priority_found_create = False	

global dupliacte_unit_found_create
dupliacte_unit_found_create = False

class business(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(business, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	def _calculate_total_mod(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		#_logger.info('Adding rooms %s', mod_line_ids)
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = self.browse(cr, uid, line.id, context=context).people_line or []
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
				x.business_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.business_code and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.business_code and self_obj.business_code.lower() in  lst:
				return False
		return True
		
# Room mandatory
	def _make_mandatory_people(self, cr, uid, ids, context=None):
			pl = self.pool.get('people.line')
			isFound = False
			for progline in self.browse(cr, uid, ids, context=None):
					for line in progline.people_line:
						isFound = True
					if isFound:
						return True
					else:
						return False
			return True
			
	'''def copy(self, cr, uid, id, default=None, context=None):
		group_name = self.read(cr, uid, [id], ['name'])[0]['name']
		group_name_one = self.read(cr, uid, [id], ['unit_line'])[0]['unit_line']
		group_name_two = self.read(cr, uid, [id], ['business_code'])[0]['business_code']
		default.update({'name': _('%s (copy)')%group_name})
		default.update({'unit_line': _('%s (copy)')%group_name_one})
		default.update({'business_code': _('%s (copy)')%group_name_two})
		module_id =  super(business, self).copy(cr, uid, id, default, context)
		return module_id'''
		
	def copy(self, cr, uid, id, default=None, context=None):
		raise osv.except_osv(_('Forbbiden to duplicate'), _('Is not possible to duplicate the record, please create a new one.'))
	
		
	_name = "business"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100,readonly=1),
		'business_id': fields.char('Id',size=20),
		'name': fields.char('Business Unit Name', size=100,required=True, select=True),
		'business_code': fields.char('Business Code', size=20),
		'bussiness_id':fields.many2one('business', 'Parent', ondelete='cascade', help='Bussiness', select=True),
		'segment_line_code': fields.selection((('CP (Corporate Public)','CP (Corporate Public)'),('CI (Corporate In-House)','CI (Corporate In-House)'),('RP (Retail Public)','RP (Retail Public)'),('HP (HE Public)','HP (HE Public)'),('HI  (HE In-House)','HI  (HE In-House)')),'Segment Code'),
		'unit_line': fields.one2many('unit.line', 'unit_line_id', 'Unit Lines', select=True, required=True),
		'people_line': fields.one2many('people.line', 'people_business_id', 'People Lines', select=True, required=True),
		'people_count': fields.function(_calculate_total_mod, relation="business",readonly=1,string='People Count',type='integer'),
	}
	
	def create(self,cr, uid, values, context=None):
	
		global dupliacte_order_priority_found_create
		dupliacte_order_priority_found_create = False	

		global dupliacte_unit_found_create
		dupliacte_unit_found_create = False
		
		if 'unit_line' in values :
			if values['unit_line']  > 1:
				ids_test_lear = self.pool.get('unit.line').search(cr,1,[])
				table_ids = []
				new_table_ids = []
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('unit.line').browse(cr,1,ids_test_lear):
					if dd.unit_line_id.id == True:
						table_ids.append(dd.order_priority)	
				for x in values['unit_line'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('unit.line').browse(cr,uid,x[1])
						deleted_ids.append(obj.order_priority)
					elif x[0] == 0 and 'order_priority' in x[2]:
						added_ids.append(x[2]['order_priority'])
						if x[2]['order_priority'] in table_ids :
							new_table_ids.append(dd.order_priority)
					elif x[0] == 1  and 'order_priority' in x[2]:
						updated_ids.append(x[2]['order_priority'])

				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_order_priority_found_create
					dupliacte_order_priority_found_create = True
				else:

					for c in added_ids :
						if (c in new_table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_order_priority_found_create
							dupliacte_order_priority_found_create = True

					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_order_priority_found_create
						dupliacte_order_priority_found_create = True
					else :
						found = 0
						for u in updated_ids :
							if u in new_table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_order_priority_found_create
							dupliacte_order_priority_found_create = True
							
		if 'unit_line' in values :
			if values['unit_line']  > 1:
				ids_test_lear = self.pool.get('unit.line').search(cr,1,[])
				table_ids = []
				new_table_ids = []
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('unit.line').browse(cr,1,ids_test_lear):
					if dd.unit_line_id.id == True:
						table_ids.append(dd.unit)	
				for x in values['unit_line'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('unit.line').browse(cr,uid,x[1])
						deleted_ids.append(obj.unit)
					elif x[0] == 0 and 'unit' in x[2]:
						added_ids.append(x[2]['unit'])
						if x[2]['unit'] in table_ids :
							new_table_ids.append(dd.unit)
					elif x[0] == 1  and 'unit' in x[2]:
						updated_ids.append(x[2]['unit'])

				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_unit_found_create
					dupliacte_unit_found_create = True
				else:

					for c in added_ids :
						if (c in new_table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_unit_found_create
							dupliacte_unit_found_create = True

					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_unit_found_create
						dupliacte_unit_found_create = True
					else :
						found = 0
						for u in updated_ids :
							if u in new_table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_unit_found_create
							dupliacte_unit_found_create = True
	
		module_id = super(business, self).create(cr, uid, values, context=context)
		return module_id
	
	def write(self,cr, uid, ids, values, context=None):
	
		global dupliacte_order_priority_found
		dupliacte_order_priority_found = False	
		
		global dupliacte_unit_found
		dupliacte_unit_found = False
	
		if 'unit_line' in values :
				if values['unit_line']  > 1:
					ids_test_lear = self.pool.get('unit.line').search(cr,1,[])
					table_ids = [] 
					added_ids = []
					deleted_ids =[]
					updated_ids = []
					for dd in self.pool.get('unit.line').browse(cr,1,ids_test_lear):
						if dd.unit_line_id.id == ids[0]:
							table_ids.append(dd.order_priority)
					for x in values['unit_line'] :
						if x[0] == 2 and x[2] ==  False :
							obj = self.pool.get('unit.line').browse(cr,uid,x[1])
							deleted_ids.append(obj.order_priority)
						elif x[0] == 0 and 'order_priority' in x[2]:
							added_ids.append(x[2]['order_priority'])
						elif x[0] == 1  and 'order_priority' in x[2]:
							updated_ids.append(x[2]['order_priority'])
					'''create check'''		
					if len(added_ids) - len(set(added_ids)) >  0 :
						global dupliacte_order_priority_found
						dupliacte_order_priority_found = True
					else:
						'''check create in table'''
						for c in added_ids :
							if (c in table_ids and c not in deleted_ids) or (c in updated_ids):
								global dupliacte_order_priority_found
								dupliacte_order_priority_found = True
						'''check for update ids '''
						if len(updated_ids) - len(set(updated_ids)) >  0 :
							global dupliacte_order_priority_found
							dupliacte_order_priority_found = True
						else :
							found = 0
							for u in updated_ids :
								if u in table_ids and  u not in deleted_ids :
									found = found +1
							if found == 1 :
								global dupliacte_order_priority_found
								dupliacte_order_priority_found = True
		if 'unit_line' in values :
				if values['unit_line']  > 1:
					ids_test_lear = self.pool.get('unit.line').search(cr,1,[])
					table_ids = [] 
					added_ids = []
					deleted_ids =[]
					updated_ids = []
					for dd in self.pool.get('unit.line').browse(cr,1,ids_test_lear):
						if dd.unit_line_id.id == ids[0]:
							table_ids.append(dd.unit)
					for x in values['unit_line'] :
						if x[0] == 2 and x[2] ==  False :
							obj = self.pool.get('unit.line').browse(cr,uid,x[1])
							deleted_ids.append(obj.unit)
						elif x[0] == 0 and 'unit' in x[2]:
							added_ids.append(x[2]['unit'])
						elif x[0] == 1  and 'unit' in x[2]:
							updated_ids.append(x[2]['unit'])
					'''create check'''		
					if len(added_ids) - len(set(added_ids)) >  0 :
						global dupliacte_unit_found
						dupliacte_unit_found = True
					else:
						'''check create in table'''
						for c in added_ids :
							if (c in table_ids and c not in deleted_ids) or (c in updated_ids):
								global dupliacte_unit_found
								dupliacte_unit_found = True
						'''check for update ids '''
						if len(updated_ids) - len(set(updated_ids)) >  0 :
							global dupliacte_unit_found
							dupliacte_unit_found = True
						else :
							found = 0
							for u in updated_ids :
								if u in table_ids and  u not in deleted_ids :
									found = found +1
							if found == 1 :
								global dupliacte_unit_found
								dupliacte_unit_found = True
								
		module_id = super(business, self).write(cr, uid, ids,values, context=context)
		return module_id
	
	
	def on_change_bussiness_id(self, cr, uid, ids, bussiness_id):
		bussiness_obj = self.pool.get('business').browse(cr, uid, bussiness_id)
		return {'value': {'s_no': bussiness_obj.s_no, 'name': bussiness_obj.name,'business_code':bussiness_obj.business_code,'unit_line':bussiness_obj.unit_line}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'bussiness_form')
		view_id = view_ref and view_ref[1] or False
		loc_room_obj = self.pool.get('business')
		loc_room_ids = loc_room_obj.search(cr, uid, [('id', '=', ids[0])])
		room_ids =[]
		for loc_room_line in loc_room_obj.browse(cr, uid, loc_room_ids,context=context):
			room_ids.append(loc_room_line['bussiness_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'name': _('Bussiness'),
		'res_model': 'bussiness',
		'view_type': 'form',
		'res_id': room_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,
		}
	_constraints = [(_check_unique_name, 'Error: Name already exist', ['Business Unit Name']),(_check_unique_code, 'Error: Code already exist', ['Business Code']),(_make_mandatory_people, 'Error: Atleast One People should be added', ['People'])]
business

class segment_code(osv.osv):

	def _check_segment_code(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				raise osv.except_osv(_('Error:'),_("Segment Code Already Exists")%(self_obj))
		return True
	
	_name ='segment.code'
	_description ="Business Segment Code"
	_columns = {
	'name':fields.selection((('CP (Corporate Public)','CP (Corporate Public)'),('CI (Corporate In-House)','CI (Corporate In-House)'),('RP (Retail Public)','RP (Retail Public)'),('HP (HE Public)','HP (HE Public)'),('HI  (HE In-House)','HI  (HE In-House)')),'Segment Code'),
	}
	_constraints = [(_check_segment_code, 'Error: Segment Code Already Exists', ['Segment Code'])]
segment_code()


class unit_line(osv.osv):
	
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(unit_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	
	def _check_unique_order_id(self, cr, uid, ids, context=None):
		if dupliacte_order_priority_found == True:
			return False
		elif dupliacte_order_priority_found_create == True:
			return False
		else :
			return True	
		
	def _check_unique_unit(self, cr, uid, ids, context=None):
		if dupliacte_unit_found == True:
			return False
		elif dupliacte_unit_found_create == True:
			return False
		else :
			return True			

	def _check_orderprior(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.order_priority < 0:
				return False
		return True
	
	_name = "unit.line"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100,readonly=1),
		'order_priority': fields.integer('Order Of Priority', size=2,required=True, select=True),  
		'unit': fields.char('Unit', size=30, required=True),
		'unit_line_id': fields.many2one('business', 'Business', ondelete='cascade', help='Test', select=True),
	}
	_constraints = [(_check_orderprior, 'Error: Order of Priority Value Cannot be negative', ['Order Of Priority']),(_check_unique_order_id, 'Error: Order of Priority should be unique', ['Order Of Priority']),(_check_unique_unit, 'Error: Unit should be unique', ['Unit'])]
unit_line

class people_line(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(people_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	def _check_unique_order_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.people_business_id == self_obj.people_business_id and x.name == self_obj.name:
						return False
		return True	
		
	_name = "people.line"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100,readonly=1),
		'p_line_id': fields.char('Id',size=20),
		'people_business_id': fields.many2one('business', 'Business', ondelete='cascade', help='Test', select=True),
		'name': fields.many2one('user.profiles', 'Name as in NRIC', ondelete='cascade', help='Description', select=True),
		'nric_name': fields.related('name','name_nric',type="char",relation="user.profiles",string="Name", readonly=1),
		'unit': fields.related('name','status',type="char",relation="user.profiles",string="Status", readonly=1),
		'title': fields.related('name','given_name',type="char",relation="user.profiles",string="Title", readonly=1),
		'role': fields.related('name','role',type="many2one",relation="manage.role",string="Role", readonly=1),
	}
	_constraints = [(_check_unique_order_name, 'Error: People Name already exist', ['People'])]
people_line



