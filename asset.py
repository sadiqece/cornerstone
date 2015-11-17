from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import datetime
import time
from dateutil import relativedelta

_logger = logging.getLogger(__name__)

global dupliacte_model_found
dupliacte_model_found = False

global dupliacte_model_found_create
dupliacte_model_found_create = False

global dupliacte_serial_found
dupliacte_serial_found = False

global dupliacte_serial_found_create
dupliacte_serial_found_create = False

class asset(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(asset, self).read(cr, uid,ids, fields, context, load)
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
				x.asset_code.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.asset_code and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.asset_code and self_obj.asset_code.lower() in  lst:
				return False
		return True
		
	# Room mandatory
	def _make_mandatory1(self, cr, uid, ids, context=None):
			pl = self.pool.get('asset.line')
			isFound = False
			for progline in self.browse(cr, uid, ids, context=None):
					for line in progline.asset_line:
						isFound = True
					if isFound:
						return True
					else:
						return False
			return True
			
	def create(self,cr, uid, values, context=None):
	
		global dupliacte_model_found_create
		dupliacte_model_found_create = False
		
		global dupliacte_serial_found_create
		dupliacte_serial_found_create = False
		
		if 'asset_line' in values :
			if values['asset_line']  > 1:
				ids_test_lear = self.pool.get('asset.line').search(cr,1,[])
				table_ids = []
				new_table_ids = []
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('asset.line').browse(cr,1,ids_test_lear):
					if dd.asset_line_id.id == True:
						table_ids.append(dd.model)	
				for x in values['asset_line'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('asset.line').browse(cr,uid,x[1])
						deleted_ids.append(obj.model)
					elif x[0] == 0 and 'model' in x[2]:
						added_ids.append(x[2]['model'])
						if x[2]['model'] in table_ids :
							new_table_ids.append(dd.model)
					elif x[0] == 1  and 'model' in x[2]:
						updated_ids.append(x[2]['model'])

				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_model_found_create
					dupliacte_model_found_create = True
				else:

					for c in added_ids :
						if (c in new_table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_model_found_create
							dupliacte_model_found_create = True

					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_model_found_create
						dupliacte_model_found_create = True
					else :
						found = 0
						for u in updated_ids :
							if u in new_table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_model_found_create
							dupliacte_model_found_create = True
							
		if 'asset_line' in values :
			if values['asset_line']  > 1:
				ids_test_lear = self.pool.get('asset.line').search(cr,1,[])
				table_ids = []
				new_table_ids = []
				added_ids = []
				deleted_ids =[]
				updated_ids = []
				for dd in self.pool.get('asset.line').browse(cr,1,ids_test_lear):
					if dd.asset_line_id.id == True:
						table_ids.append(dd.serial_number)	
				for x in values['asset_line'] :
					if x[0] == 2 and x[2] ==  False :
						obj = self.pool.get('asset.line').browse(cr,uid,x[1])
						deleted_ids.append(obj.serial_number)
					elif x[0] == 0 and 'serial_number' in x[2]:
						added_ids.append(x[2]['serial_number'])
						if x[2]['serial_number'] in table_ids :
							new_table_ids.append(dd.serial_number)
					elif x[0] == 1  and 'serial_number' in x[2]:
						updated_ids.append(x[2]['serial_number'])

				if len(added_ids) - len(set(added_ids)) >  0 :
					global dupliacte_serial_found_create
					dupliacte_serial_found_create = True
				else:

					for c in added_ids :
						if (c in new_table_ids and c not in deleted_ids) or (c in updated_ids):
							global dupliacte_serial_found_create
							dupliacte_serial_found_create = True

					if len(updated_ids) - len(set(updated_ids)) >  0 :
						global dupliacte_serial_found_create
						dupliacte_serial_found_create = True
					else :
						found = 0
						for u in updated_ids :
							if u in new_table_ids and  u not in deleted_ids :
								found = found +1
						if found == 1 :
							global dupliacte_serial_found_create
							dupliacte_serial_found_create = True
	
		sub_lines = []
		today = datetime.date.today()
		current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
		sub_lines.append( (0,0, {'date_created':today.strftime('%d-%m-%Y'),'created_by':current_user['name'],
			'last_update':'-','last_update_by':'-','date_status_change':today.strftime('%d-%m-%Y'),'status_change_by':current_user['name']}) )
		values.update({'history_line': sub_lines})
		name = super(asset, self).create(cr, uid, values, context=context)
		return name
		
		module_id = super(asset, self).create(cr, uid, values, context=context)
		return module_id
		
	def write(self,cr, uid, ids, values, context=None):
	
		global dupliacte_model_found
		dupliacte_model_found = False
		
		global dupliacte_serial_found
		dupliacte_serial_found = False
	
		if 'asset_line' in values :
				if values['asset_line']  > 1:
					ids_test_lear = self.pool.get('asset.line').search(cr,1,[])
					table_ids = [] 
					added_ids = []
					deleted_ids =[]
					updated_ids = []
					for dd in self.pool.get('asset.line').browse(cr,1,ids_test_lear):
						if dd.asset_line_id.id == ids[0]:
							table_ids.append(dd.serial_number)
					for x in values['asset_line'] :
						if x[0] == 2 and x[2] ==  False :
							obj = self.pool.get('asset.line').browse(cr,uid,x[1])
							deleted_ids.append(obj.serial_number)
						elif x[0] == 0 and 'serial_number' in x[2]:
							added_ids.append(x[2]['serial_number'])
						elif x[0] == 1  and 'serial_number' in x[2]:
							updated_ids.append(x[2]['serial_number'])
					'''create check'''		
					if len(added_ids) - len(set(added_ids)) >  0 :
						global dupliacte_serial_found
						dupliacte_serial_found = True
					else:
						'''check create in table'''
						for c in added_ids :
							if (c in table_ids and c not in deleted_ids) or (c in updated_ids):
								global dupliacte_serial_found
								dupliacte_serial_found = True
						'''check for update ids '''
						if len(updated_ids) - len(set(updated_ids)) >  0 :
							global dupliacte_serial_found
							dupliacte_serial_found = True
						else :
							found = 0
							for u in updated_ids :
								if u in table_ids and  u not in deleted_ids :
									found = found +1
							if found == 1 :
								global dupliacte_serial_found
								dupliacte_serial_found = True
								
		if 'asset_line' in values :
				if values['asset_line']  > 1:
					ids_test_lear = self.pool.get('asset.line').search(cr,1,[])
					table_ids = [] 
					added_ids = []
					deleted_ids =[]
					updated_ids = []
					for dd in self.pool.get('asset.line').browse(cr,1,ids_test_lear):
						if dd.asset_line_id.id == ids[0]:
							table_ids.append(dd.model)
					for x in values['asset_line'] :
						if x[0] == 2 and x[2] ==  False :
							obj = self.pool.get('asset.line').browse(cr,uid,x[1])
							deleted_ids.append(obj.model)
						elif x[0] == 0 and 'model' in x[2]:
							added_ids.append(x[2]['model'])
						elif x[0] == 1  and 'model' in x[2]:
							updated_ids.append(x[2]['model'])
					'''create check'''		
					if len(added_ids) - len(set(added_ids)) >  0 :
						global dupliacte_model_found
						dupliacte_model_found = True
					else:
						'''check create in table'''
						for c in added_ids :
							if (c in table_ids and c not in deleted_ids) or (c in updated_ids):
								global dupliacte_model_found
								dupliacte_model_found = True
						'''check for update ids '''
						if len(updated_ids) - len(set(updated_ids)) >  0 :
							global dupliacte_model_found
							dupliacte_model_found = True
						else :
							found = 0
							for u in updated_ids :
								if u in table_ids and  u not in deleted_ids :
									found = found +1
							if found == 1 :
								global dupliacte_model_found
								dupliacte_model_found = True
	
		sub_lines = []
		
		current_user = self.pool.get('res.users').browse(cr, uid,uid, context=context)
		for line in self.browse(cr, uid, ids, context=context):
			history_line_id = self.browse(cr, uid, ids[0], context=context).history_line or []

		num_of_his = len(history_line_id)-1 
		staus_changed_by = history_line_id[num_of_his]['status_change_by']
		staus_changed_date = history_line_id[num_of_his]['date_status_change']
 
		if 'asset_code' in values:
			staus_changed_date = fields.date.today()
			staus_changed_by  = current_user['name']

		changes = values.keys()
		test_list ={'name': 'Asset Type Name','asset_code': 'Asset Code','asset_line':'Asset Lines','choose_asset_model':'Choose Asset Model',
				'stock_line': 'Stock Level' }
		arr={}
		for i in range(len(changes)):
			if changes[i] in test_list:
				arr[i] = test_list[changes[i]]
		today = datetime.date.today()
		sub_lines.append( (0,0, {'date_created':history_line_id[0]['date_created'],'created_by':history_line_id[0]['created_by'],
			'last_update':today.strftime('%d-%m-%Y'),'last_update_by':current_user['name'],'date_status_change':staus_changed_date,'status_change_by':staus_changed_by,'changes':arr.values()}) )
		values.update({'history_line': sub_lines})
		name = super(asset, self).write(cr, uid, ids,values, context=context)
		return name
		
		module_id = super(asset, self).write(cr, uid, ids,values, context=context)
		return module_id

	_name = "asset"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.integer('S.No', size=100),
		'name': fields.char('Asset Type Name', size=100,required=True, select=True),
		'asset_code': fields.char('Asset Code', size=20),
		'asset_line': fields.one2many('asset.line', 'asset_line_id','Asset Lines', select=True, required=True),
		'choose_asset_model': fields.many2one('asset', 'Choose Asset Model', ondelete='cascade', help='Description', select=True),
		'stock_line': fields.one2many('stock.level', 's_no','Stock Level', select=True, required=True),
		'history_line': fields.one2many('asset.history','asset_id','History', limit=None),
	}
	
	_constraints = [(_check_unique_name, 'Error: Asset Name Already Exists', ['Name']),(_check_unique_code, 'Error: Asset Code Already Exists', ['Asset Code']),(_make_mandatory1, 'Error: Atleast One Brand should be entried', ['Brand']),]
asset()

class master_brand(osv.osv):
	
	_name ='master.brand'
	_description ="People and Facilites Tab"
	_columns = {
	#'brand_id':fields.integer('ID', size=3, readonly=1),
	'name':fields.char('Brand',size=20),
	'model':fields.char('Model',size=20),
	}
	#_constraints = [(_check_unique_bname, 'Error: Brand name Already Exists', ['Name'])]
#EOF	
	
master_brand()

class master_asset_model(osv.osv):
	
	_name ='master.asset.model'
	_description ="Asset Model"
	_columns = {
	'name':fields.char('Choose Asset Model',size=20),
	}	
	
master_asset_model()


class asset_line(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(asset_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['sr_no'] = seq_number
		
		return res

	def months_between(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
		
	def months_between2(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date11, date12)
		return r.days
	   
# Zeya 9-1-15	   
	   
	def onchange_issuedate(self, cr, uid, ids, issue, stop, context=None):
			if issue:
				d = self.months_between(issue, str(datetime.datetime.now().date())) 
				res = {'value':{}}
				#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(d))
				if d > 0:
					res['value']['date_issue'] = ''
					#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
					res.update({'warning': {'title': _('Warning !'), 'message': _('Please Check the Date, Invalid Date not Allowed.')}})
					return res
				elif stop and issue:
					c = self.months_between2(str(stop), str(issue))
					if c < 0:
						res['value']['date_issue'] = ''
						#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
						res.update({'warning': {'title': _('Warning !'), 'message': _('Please Check the Date, Invalid Date not Allowed.')}})
						return res
				return issue
				
	def onchange_stopeddate(self, cr, uid, ids, stop, issue, context=None):
		if stop:
			d = self.months_between(stop, str(datetime.datetime.now().date()))
			#c = self.months_between2(stop, str(sd))
			res = {'value':{}}
			if d > 0:
				res['value']['date_stopped'] = ''
				#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please Check the Date, Invalid Date not Allowed.')}})
				return res
			elif stop and issue:
					c = self.months_between2(str(stop), str(issue))
					if c < 0:
						res['value']['date_stopped'] = ''
						#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
						res.update({'warning': {'title': _('Warning !'), 'message': _('Please Check the Date, Invalid Date not Allowed.')}})
						return res
			return issue
			
	def _check_unique_model(self, cr, uid, ids, context=None):
		if dupliacte_model_found == True:
			return False
		elif dupliacte_model_found_create == True:
			return False
		else :
			return True	

	def _check_unique_serial(self, cr, uid, ids, context=None):
		if dupliacte_serial_found == True:
			return False
		elif dupliacte_serial_found_create == True:
			return False
		else :
			return True

	_name = "asset.line"
	_description = "This table is for keeping location data"
	_columns = {
		'sr_no': fields.integer('S.No', size=100, readonly=1),
		#'line_id': fields.integer('Id',size=20),
		'brand':fields.many2one('master.brand', 'Brand', ondelete='cascade', help='Description', select=True,required=True),
		'model': fields.char('Model', size=20, required=True),
		'serial_number': fields.char('Serial Number', size=25, required=True),
		'cost': fields.integer('Cost ($)', size=7),
		'specs': fields.char('Specs & Description', size=20),
		'date_issue': fields.date('Date of First Issue'),
		'date_stopped': fields.date('Date Stopped Issuing'),
		'asset_line_id': fields.many2one('asset', 'Asset', ondelete='cascade', help='Test', select=True),
	}
	_constraints = [(_check_unique_model, 'Error: Model Already Exists', ['Brand']), (_check_unique_serial, 'Error: Serial Number Already Exists', ['Serial'])]
asset_line ()

class stock_level(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(stock_level, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def _check_unique_location(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.location for x in self.browse(cr, uid, sr_ids, context=context)
				if x.location and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.location and self_obj.location in  lst:
				return False
		return True

	_name = "stock.level"
	_description = "This table is for stock level"
	_columns = {
		's_no': fields.integer('S.No', size=100, readonly=1),
		'location': fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'stock_level_date': fields.date('Stock Level Date'),
		'update_by': fields.char('Update By', size=20, required=True),
		'current_stock': fields.integer('Current Stock', size=20),	
	}
	_constraints = [(_check_unique_location, 'Error: Location Already Exists', ['Location'])]
stock_level()

class test_history(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(test_history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	_name ='asset.history'
	_description ="History Tab"
	_columns = {
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'history_id':fields.integer('Id',size=20),
	'date_created':fields.char('Date Created',size=20),
	'created_by':fields.char('Created By',size=20),
	'last_update':fields.char('Last Update',size=20),
	'last_update_by':fields.char('Last Update By',size=20),
	'date_status_change':fields.char('Date Of Status Change',size=20),
	'status_change_by':fields.char('Status Change By',size=20),
	'changes':fields.char('Changes',size=200),
	'asset_id': fields.many2one('asset', 'Test', ondelete='cascade', help='Test', select=True),
	}
test_history	()

