import datetime
from dateutil import relativedelta
from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools


_logger = logging.getLogger(__name__)

class holidays(osv.osv):
	
	def _populate_year(self, cursor, user_id, context=None):
		return ( 
		   ('2014', '2014'),
		   ('2015', '2015'),
		   ('2016', '2016'),
		   ('2017', '2017'),
		   ('2018', '2018'),
		   ('2019', '2019'),
		   ('2020', '2020'),
		   ('2021', '2021'),
		   ('2022', '2022'),
		   ('2023', '2023'))
		
	def populate_year(self, cursor, user_id, context=None):
		val = {}
		i = 0
		for year_dropdown in range(2014, (datetime.datetime.now().year + 10)):
			val[i] = ('choice'+str(i), str(year_dropdown))
			i = i+1
		return val
		
# Zeya 5-1-15			

	def _check_unique_year(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.holiday_id == self_obj.holiday_id and x.year == self_obj.year:
						return False
		return True
		
	'''def on_change(self, cr, uid, ids, t_date, duration):
			res = {'end_date': False}
		if t_date:
			now = datetime.strptime(t_date, '%Y-%m-%d %H:%M:%S')

			e_date = now + timedelta(hours=duration)
			print e_date
			f_date = datetime.strftime(e_date, '%Y-%m-%d %H:%M:%S')
			res['end_date'] = f_date
		return {'value': res}'''
		
	def _calculate_total_holiday(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		#_logger.info('Adding rooms %s', mod_line_ids)
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = self.browse(cr, uid, line.id, context=context).holiday_line or []
			_logger.info('Adding rooms %s', mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
				
		return res
	
	
	_name = "holiday"
	_description = "This table is for keeping location data"
	_columns = {
		'holiday_id': fields.char('Id',size=20),
		'year': fields.selection(_populate_year,'Year', required=True),
		'holiday_line': fields.one2many('holiday.line', 'holiday_line_id', 'Holiday Lines', select=True, required=True),
		'no_of_holidays': fields.function(_calculate_total_holiday, relation="holiday",readonly=1,string='No. of Holidays',type='integer'),
	}
	_constraints = [(_check_unique_year, 'Error: Year Already Exists', ['year'])]
holidays


class holiday_line(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(holiday_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def _check_unique_start_date(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.holiday_line_id == self_obj.holiday_line_id and x.date_start == self_obj.date_start:
						return False
		return True
		
	def _check_unique_end_date(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.holiday_line_id == self_obj.holiday_line_id and x.date_end == self_obj.date_end:
						return False
		return True

#Zeya 6-1-15		
	def months_between1(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
		
	def months_between2(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date11, date12)
		return r.days
	   
# EOF
	
# Zeya 9-1-15

	
	def onchange_date(self, cr, uid, ids, issue, stop, context=None):
			if issue:
				d = self.months_between1(issue, str(datetime.datetime.now().date())) 
				res = {'value':{}}
				#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(d))
				if d > 0:
					res['value']['date_start'] = ''
					#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
					res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, Past date not allowed.')}})
					return res
				elif stop and issue:
					c = self.months_between2(str(stop), str(issue))
					if c < 0:
						res['value']['date_start'] = ''
						#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
						res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, Past date not allowed.')}})
						return res
				return issue


	def onchange_dateend(self, cr, uid, ids, stop, issue, context=None):
		if stop:
			d = self.months_between1(stop, str(datetime.datetime.now().date()))
			#c = self.months_between2(stop, str(sd))
			res = {'value':{}}
			if d > 0:
				res['value']['date_end'] = ''
				#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, Past date not allowed.')}})
				return res
			elif stop and issue:
					c = self.months_between2(str(stop), str(issue))
					if c < 0:
						res['value']['date_end'] = ''
						#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
						res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date,  OR Past date not allowed.')}})
						return res
			return issue

				 
	   
# EOF
		
	def _check_unique_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.holiday_line_id == self_obj.holiday_line_id and x.description == self_obj.description:
						return False
		return True

			
	_name = "holiday.line"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.char('S.No',size=20, readonly=1),
		'description': fields.char('Description', size=100,required=True, select=True),
		# Zeya 6-1-15
		'date_start': fields.date('Date Start', required=True),
		'date_end': fields.date('Date End', required=True),
		#EOF
		'holiday_line_id': fields.many2one('holiday', 'Holidays', ondelete='cascade', help='Holiday', select=True),
	}
	_constraints = [(_check_unique_start_date, 'Error: Start Date Already Exists', ['date_start']),(_check_unique_end_date, 'Error: End Date Already Exists', ['date_end']),(_check_unique_name, 'Error: Holiday Already Exists', ['description'])]
holiday_line
