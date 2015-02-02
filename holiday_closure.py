import datetime
from dateutil import relativedelta
from openerp import addons
import logging
import time
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from datetime import datetime
from collections import namedtuple
import pytz


_logger = logging.getLogger(__name__)

####################
#HOLIDAYS
####################

#Class Holidays
###############
class holidays(osv.osv):
#Year Dropdown	
	def _populate_year(self, cursor, user_id, context=None):
		return ( 
		   ('2010', '2010'),
		   ('2011', '2011'),
		   ('2012', '2012'),
		   ('2013', '2013'),
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

#Populate Year
	def populate_year(self, cursor, user_id, context=None):
		val = {}
		i = 0
		for year_dropdown in range(2012, (datetime.now().year + 10)):
			val[i] = ('choice'+str(i), str(year_dropdown))
			i = i+1
		return val
		
#Calculate Holidays
	def _calculate_total_holiday(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = self.browse(cr, uid, line.id, context=context).holiday_line or []
			_logger.info('Adding rooms %s', mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
				
		return res

#Validate Unique Year
	def _check_unique_year(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.holiday_id == self_obj.holiday_id and x.year == self_obj.year:
						return False
		return True
		
#Table For Year in Holiday
	_name = "holiday"
	_description = "This table is for keeping location data"
	_columns = {
		'holiday_id': fields.char('Id',size=20),
		'year': fields.selection(_populate_year, 'Year', required=True),
		'holiday_line': fields.one2many('holiday.line', 'holiday_line_id', 'Holiday Lines', select=True, required=True),
		'no_of_holidays': fields.function(_calculate_total_holiday, relation="holiday",readonly=1,string='No. of Holidays',type='integer'),
	}
	_constraints = [(_check_unique_year, 'Error: Year Already Exists', ['year'])]
holidays

#Class Holiday Line
###############
class holiday_line(osv.osv):
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(holiday_line, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

#Validate Date For Past		
	def months_between1(self, date1, date2):
		#current_date = datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT),
		#print "\n\n====current_date===", current_date
		#date11 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
		#date12 = datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date1, date2)
		return r.days
		
	def months_between2(self, date1, date2):
		date11 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
		date12 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')
		r = relativedelta.relativedelta(date12, date11)
		return r.days

#Validate Start Date: Past Date and Year Match
	def onchange_start_date_past(self, cr, uid, ids, start_date, eofdate, year2, context=None):
		res = {'value':{}}
			
		chng_year = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
		today = time.strftime('%Y-%m-%d %H:%M:%S')
		current_date = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
		if chng_year.year and year2:
			if str(chng_year.year) != str(year2):
				res['value']['date_start'] = ''
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct Year.')}})
				return res
			d = self.months_between1(chng_year, current_date) 
			if d < 0:
				res['value']['date_start'] = ''
				res.update({'warning': {'title': _('Warning !'), 'message': _('Past date not allowed.')}})
				return res
			'''elif eofdate and start_date:
				c = self.months_between2(str(start_date), str(eofdate))
				#raise osv.except_osv(_('Warning!'),_('sdasdfdsdfsf %s')%(c))
				if c < 0:
					res['value']['date_start'] = ''
					res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date.')}})
					return res'''
			return start_date
				
#Validate End Date : Past Date and Year Match
	def onchange_end_date_past(self, cr, uid, ids, eofdate, start_date, year2, context=None):
		res = {'value':{}}
		#chng_year = datetime.strptime(eofdate, "%Y-%m-%d %H:%M:%S")
		chng_year = datetime.strptime(eofdate, "%Y-%m-%d %H:%M:%S")
		today = time.strftime('%Y-%m-%d %H:%M:%S')
		current_date = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')				
		if not start_date and eofdate:
			res['value']['date_end'] = ''
			res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter start date first.')}})
			return res

		if chng_year.year and year2:
			if str(chng_year.year) != str(year2):
				res['value']['date_end'] = ''
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct Year.')}})
				return res
			
			#d = self.months_between1(eofdate, str(datetime.now().date()))
			d = self.months_between1(chng_year, current_date) 
			#raise osv.except_osv(_('Warning!'),_('sdasdfdsdfsf %s %s')%(d, eofdate))
			if d < 0:
				res['value']['date_end'] = ''
				res.update({'warning': {'title': _('Warning !'), 'message': _('Past date not allowed.')}})
				return res
			'''elif eofdate and start_date:
				c = self.months_between2(str(eofdate), str(start_date))
				d = self.months_between1(start_date, str(datetime.now().date())) 
				if c < 0:
					res['value']['date_end'] = ''
					res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date')}})
					return res'''
			return eofdate

#Validate Start/End Date	
	def _date_start_end_validate(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.date_start >= self_obj.date_end:
				return False
		return True

#Validate Unique Name	
	def _check_unique_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.s_no == self_obj.s_no and x.description == self_obj.description:
						return False
		return True
		
#Validate Unique Start Date
	def _check_unique_start_date(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.s_no == self_obj.s_no and x.date_start == self_obj.date_start:
						return False
		return True

#Validate Unique End Date		
	def _check_unique_end_date(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for x in self.browse(cr, uid, sr_ids, context=context):
			if x.id != ids[0]:
				for self_obj in self.browse(cr, uid, ids, context=context):
					if x.s_no == self_obj.s_no and x.date_end == self_obj.date_end:
						return False
		return True
		
#Sadiq - Check Class and Test Schedule for Holidays and Closures
	def create(self,cr, uid, values, context=None):
		id = super(holiday_line, self).create(cr, uid, values, context=context)
	
		Range = namedtuple('Range', ['start', 'end'])
		r1 = Range(start=datetime.strptime(values['date_start'], "%Y-%m-%d %H:%M:%S"), end=datetime.strptime(values['date_end'], "%Y-%m-%d %H:%M:%S"))
		
		class_obj =self.pool.get("class.info")
		class_obj_ids = class_obj.search(cr,uid,[])
		sess_issue = 'None'
		for u in class_obj.browse(cr,uid,class_obj_ids) :
			r2 = Range(start=datetime.strptime(u['start_date'], "%Y-%m-%d %H:%M:%S"), end=datetime.strptime(u['end_date'], "%Y-%m-%d %H:%M:%S"))
			latest_start = max(r1.start, r2.start)
			earliest_end = min(r1.end, r2.end)
			overlap = (earliest_end - latest_start)
			if overlap.days == 0:
				class_obj.write(cr, uid, [u.id],{'sess_issues':values['description']}, context,holidays= True)
		
		return id
	def write(self,cr, uid, ids, values, context=None):
		
		if 'date_start' in values :
			t1start = datetime.strptime(values['date_start'], "%Y-%m-%d %H:%M:%S") 
		else:
			t1start = datetime.strptime(self.browse(cr,uid,ids[0])['date_start'], "%Y-%m-%d %H:%M:%S") 
			
		if 'date_end' in values :
			t1end = datetime.strptime(values['date_end'], "%Y-%m-%d %H:%M:%S") 
		else:
			t1end = datetime.strptime(self.browse(cr,uid,ids[0])['date_end'], "%Y-%m-%d %H:%M:%S") 
		
		if 'description' in values:
			description = values['description']
		else:
			description = self.browse(cr,uid,ids[0])['description']
			
		Range = namedtuple('Range', ['start', 'end'])
		r1 = Range(start = t1start, end=t1end)
		
		class_obj =self.pool.get("class.info")
		class_obj_ids = class_obj.search(cr,uid,[])
		for u in class_obj.browse(cr,uid,class_obj_ids) :
			r2 = Range(start=datetime.strptime(u['start_date'], "%Y-%m-%d %H:%M:%S"), end=datetime.strptime(u['end_date'], "%Y-%m-%d %H:%M:%S"))
			latest_start = max(r1.start, r2.start)
			earliest_end = min(r1.end, r2.end)
			overlap = (earliest_end - latest_start)
			if overlap.days == 0:
				class_obj.write(cr, uid, [u.id],{'sess_issues':description}, context,holidays= True)
		
		id = super(holiday_line, self).write(cr, uid, ids,values, context=context)
		return id
			
			
#Table For Holiday And Closure
	_name = "holiday.line"
	_description = "This table is for keeping location data"
	_columns = {
		's_no': fields.char('S.No',size=20, readonly=1),
		'description': fields.char('Description', size=100,required=True, select=True),
		'date_start': fields.datetime('Date Start', required=True),
		'date_end': fields.datetime('Date End', required=True),
		'holiday_line_id': fields.many2one('holiday', 'Holidays', ondelete='cascade', help='Holiday', select=True),
	}
	_constraints = [(_check_unique_start_date, 'Error: Start Date Already Exists', ['Start Date']),(_check_unique_end_date, 'Error: End Date Already Exists', ['End Date']),(_check_unique_name, 'Error: Description Already Exists', ['Description']),(_date_start_end_validate, 'Error: Invalid Date', ['Date'])]
holiday_line
