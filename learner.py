import datetime
from dateutil import relativedelta
from openerp import addons
import logging
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import re
import base64
from content_index_learner import cntIndex
from openerp.tools.misc import ustr

_logger = logging.getLogger(__name__)

####################
#LEARNER ENROLLMENT
####################

#Class Learner Info
###############

class learner_info(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):		
		res = super(learner_info, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+100
			r['s_no'] = seq_number		
		return res
		
		
		
#Load Module Groups
	def load_module_groups(self, cr, uid, ids, progid, context=None):

		val ={}	
		sub_lines = []
		set_group_as_sel_1 = False
		set_group_as_sel_2 = False
		set_group_as_sel_3 = False
		set_group_as_sel_4 = False
		set_group_as_sel_5 = False
		set_group_as_sel_6 = False
		
		
		set_module_as_1 =''
		set_module_as_2 = ''
		set_module_as_3 = ''
		set_module_as_4 = ''
		set_module_as_5 = ''
		set_module_as_6 = ''
		
		for program in self.pool.get('lis.program').browse(cr,uid, [progid], context=context):
			if program.no_of_mod_gp:
				no_of_mod_gp = program.no_of_mod_gp
			#Group Selectable
			if program.set_group_as_sel_1:
				set_group_as_sel_1 = program.set_group_as_sel_1
			if program.set_group_as_sel_2:
				set_group_as_sel_2 = program.set_group_as_sel_2
			if program.set_group_as_sel_3:
				set_group_as_sel_3 = program.set_group_as_sel_3
			if program.set_group_as_sel_4:
				set_group_as_sel_4 = program.set_group_as_sel_4
			if program.set_group_as_sel_5:
				set_group_as_sel_5 = program.set_group_as_sel_5
			if program.set_group_as_sel_6:
				set_group_as_sel_6 = program.set_group_as_sel_6
			#Group Name
			if program.mod_gp_name_1:
				val.update({'mod_gp_name_1': program.mod_gp_name_1})
			if program.mod_gp_name_2:
				val.update({'mod_gp_name_2': program.mod_gp_name_2})
			if program.mod_gp_name_3:
				val.update({'mod_gp_name_3': program.mod_gp_name_3})
			if program.mod_gp_name_4:
				val.update({'mod_gp_name_4': program.mod_gp_name_4})
			if program.mod_gp_name_5:
				val.update({'mod_gp_name_5': program.mod_gp_name_5})
			if program.mod_gp_name_6:
				val.update({'mod_gp_name_6': program.mod_gp_name_6})
			#Module Selectable
			if program.set_module_as_1:
				set_module_as_1 = program.set_module_as_1
			if program.set_module_as_2:
				set_module_as_2 = program.set_module_as_2
			if program.set_module_as_3:
				set_module_as_3 = program.set_module_as_3
			if program.set_module_as_4:
				set_module_as_4 = program.set_module_as_4
			if program.set_module_as_5:
				set_module_as_5 = program.set_module_as_5
			if program.set_module_as_6:
				set_module_as_6 = program.set_module_as_6
			#Min Value
			if program.min_no_modules_1:
				val.update({'min_no_modules_1': program.min_no_modules_1})
			if program.min_no_modules_2:
				val.update({'min_no_modules_2': program.min_no_modules_2})
			if program.min_no_modules_3:
				val.update({'min_no_modules_3': program.min_no_modules_3})
			if program.min_no_modules_4:
				val.update({'min_no_modules_4': program.min_no_modules_4})
			if program.min_no_modules_5:
				val.update({'min_no_modules_5': program.min_no_modules_5})
			if program.min_no_modules_6:
				val.update({'min_no_modules_6': program.min_no_modules_6})
			#Max Value
			if program.max_no_modules_1:
				val.update({'max_no_modules_1': program.max_no_modules_1})
			if program.max_no_modules_2:
				val.update({'max_no_modules_2': program.max_no_modules_2})
			if program.max_no_modules_3:
				val.update({'max_no_modules_3': program.max_no_modules_3})
			if program.max_no_modules_4:
				val.update({'max_no_modules_4': program.max_no_modules_4})
			if program.max_no_modules_5:
				val.update({'max_no_modules_5': program.max_no_modules_5})
			if program.max_no_modules_6:
				val.update({'max_no_modules_6': program.max_no_modules_6})
				
#Module Group Selectable
		#1			
		if set_group_as_sel_1 == True:
			val.update({'set_group_as_sel_1': True})
		elif set_group_as_sel_1 == False:
			val.update({'set_group_as_sel_1': False})
		#2
		if set_group_as_sel_2 == True:
			val.update({'set_group_as_sel_2': True})
		elif set_group_as_sel_2 == False:
			val.update({'set_group_as_sel_2': False})
		#3
		if set_group_as_sel_3 == True:
			val.update({'set_group_as_sel_3': True})
		elif set_group_as_sel_3 == False:
			val.update({'set_group_as_sel_3': False})
		#4
		if set_group_as_sel_4 == True:
			val.update({'set_group_as_sel_4': True})
		elif set_group_as_sel_4 == False:
			val.update({'set_group_as_sel_4': False})
		#5
		if set_group_as_sel_5 == True:
			val.update({'set_group_as_sel_5': True})
		elif set_group_as_sel_5 == False:
			val.update({'set_group_as_sel_5': False})
		#6
		if set_group_as_sel_6 == True:
			val.update({'set_group_as_sel_6': True})
		elif set_group_as_sel_6 == False:
			val.update({'set_group_as_sel_6': False})
			
#No Of Module Groups
		if no_of_mod_gp == '1':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': False})
			val.update({'no_module_box3': False})
			val.update({'no_module_box4': False})
			val.update({'no_module_box5': False})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '2':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': False})
			val.update({'no_module_box4': False})
			val.update({'no_module_box5': False})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '3':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': True})
			val.update({'no_module_box4': False})
			val.update({'no_module_box5': False})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '4':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': True})
			val.update({'no_module_box4': True})
			val.update({'no_module_box5': False})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '5':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': True})
			val.update({'no_module_box4': True})
			val.update({'no_module_box5': True})
			val.update({'no_module_box6': False})
		elif no_of_mod_gp == '6':
			val.update({'no_module_box1': True})
			val.update({'no_module_box2': True})
			val.update({'no_module_box3': True})
			val.update({'no_module_box4': True})
			val.update({'no_module_box5': True})
			val.update({'no_module_box6': True})

#Set Module Selectable
		#1
		if set_module_as_1 == 'Selectable':
			val.update({'set_module_select_1': True})
			
		elif set_module_as_1 != 'Selectable':
			val.update({'set_module_select_1': False})
			
		#2
		if set_module_as_2 == 'Selectable':
			val.update({'set_module_select_2': True})
		elif set_module_as_2 != 'Selectable':
			val.update({'set_module_select_2': False})
		#3
		if set_module_as_3 == 'Selectable':
			val.update({'set_module_select_3': True})
		elif set_module_as_3 != 'Selectable':
			val.update({'set_module_select_3': False})
		#4
		if set_module_as_4 == 'Selectable':
			val.update({'set_module_select_4': True})
		elif set_module_as_4 != 'Selectable':
			val.update({'set_module_select_4': False})
		#5
		if set_module_as_5 == 'Selectable':
			val.update({'set_module_select_5': True})
		elif set_module_as_5 != 'Selectable':
			val.update({'set_module_select_5': False})
		#6
		if set_module_as_6 == 'Selectable':
			val.update({'set_module_select_6': True})
		elif set_module_as_6 != 'Selectable':
			val.update({'set_module_select_6': False})
			
# 1=====	
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id', '=', progid)])	
		sub_lines = []		
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_1 != 'Selectable':
				sub_lines.append({'module_id':prog_line['module_id'].id, 'check_module_select_1':False})
			else:
				sub_lines.append({'module_id':prog_line['module_id'].id, 'check_module_select_1':True})
		val.update({'learner_mod_line': sub_lines})
# 2 ====		
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_2', '=', progid)])
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_2 != 'Selectable':
				sub_lines.append({'module_id_2':prog_line['module_id_2'].id, 'check_module_select_2':False})
			else:
				sub_lines.append({'module_id_2':prog_line['module_id_2'].id, 'check_module_select_2':True})
		val.update({'learner_mod_line_2': sub_lines})
# 3 ====
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_3', '=', progid)]) 
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_3 != 'Selectable':
				sub_lines.append({'module_id_3':prog_line['module_id_3'].id, 'check_module_select_3':False})
			else:
				sub_lines.append({'module_id_3':prog_line['module_id_3'].id, 'check_module_select_3':True})
		val.update({'learner_mod_line_3': sub_lines})
# 4 ======		
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_4', '=', progid)]) 
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_4 != 'Selectable':
				sub_lines.append({'module_id_4':prog_line['module_id_4'].id, 'check_module_select_4':False})
			else:
				sub_lines.append({'module_id_4':prog_line['module_id_4'].id, 'check_module_select_4':True})
		val.update({'learner_mod_line_4': sub_lines})		
# 5 ======		
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_5', '=', progid)]) 
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_5 != 'Selectable':
				sub_lines.append({'module_id_5':prog_line['module_id_5'].id, 'check_module_select_5':False})
			else:
				sub_lines.append({'module_id_5':prog_line['module_id_5'].id, 'check_module_select_5':True})
		val.update({'learner_mod_line_5': sub_lines})
# 6 =======
		p_obj = self.pool.get('program.module.line')
		value_ids = p_obj.search(cr, uid, [('prog_mod_id_6', '=', progid)]) 
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			if set_module_as_6 != 'Selectable':
				sub_lines.append({'module_id_6':prog_line['module_id_6'].id, 'check_module_select_6':False})
			else:
				sub_lines.append({'module_id_6':prog_line['module_id_6'].id, 'check_module_select_6':True})
		val.update({'learner_mod_line_6': sub_lines})
		#return {'value': val}	
		
# Zeya 24-1-15 Checklist		
		
		#val ={}		
		p_obj = self.pool.get('program.show.do.module')
		value_ids = p_obj.search(cr, uid, [('program_id', '=', progid)])
		#val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'item':prog_line['master_show_do'].id, 'confirmation':prog_line['supp_doc_req']})
			
		val.update({'checklist_tab': sub_lines})
		#return {'value': val}	
# Zeya 24-1-15
# Payment
		learner_id = 0
		for self_obj in self.browse(cr, uid, ids, context=context):
			learner_id = self_obj.id
			
		sql = "select distinct pl.module_id, m.module_fee from lis_program p, program_module_line pl, cs_module m, \
			learner_info l, learner_mode_line ll \
			where p.id = pl.prog_mod_id and pl.module_id = m.id and l.program_learner = p.id \
			and ll.qualification_module_id_1 = l.id \
			and ((select_mod_gp_1 = 't' and p.set_module_as_1 != 'Selectable' or p.set_group_as_sel_1 = 'f' and p.set_module_as_1 != 'Selectable') \
			or (p.set_group_as_sel_1 = 'f' and p.set_module_as_1 = 'Selectable' and ll.select_mod_1 = 't' ) \
			or (p.set_module_as_1 = 'Selectable' and ll.select_mod_1 = 't') \
			or (select_mod_gp_1 = 't' and p.set_module_as_1 = 'Selectable' and ll.select_mod_1 = 't' )) \
			and p.id = %s and l.id = %s \
		union all \
		select distinct pl.module_id_2, m.module_fee from lis_program p, program_module_line pl, cs_module m, learner_info l, \
			learner_mode_line ll \
			where p.id = pl.prog_mod_id_2 and pl.module_id_2 = m.id and l.program_learner = p.id \
			and ll.qualification_module_id_2 = l.id \
			and ((select_mod_gp_2 = 't' and p.set_module_as_2 != 'Selectable' or p.set_group_as_sel_2 = 'f' and p.set_module_as_2 != 'Selectable') \
			or (p.set_group_as_sel_2 = 'f' and p.set_module_as_2 = 'Selectable' and ll.select_mod_2 = 't' ) \
			or (p.set_module_as_2 = 'Selectable' and ll.select_mod_2 = 't') \
			or (select_mod_gp_2 = 't' and p.set_module_as_2 = 'Selectable' and ll.select_mod_2 = 't' )) \
			and p.id = %s and l.id = %s \
		union all \
		select distinct pl.module_id_3, m.module_fee from lis_program p, program_module_line pl, cs_module m, learner_info l, \
			learner_mode_line ll \
			where p.id = pl.prog_mod_id_3 and pl.module_id_3 = m.id and l.program_learner = p.id \
			and ll.qualification_module_id_3 = l.id \
			and ((select_mod_gp_3 = 't' and p.set_module_as_3 != 'Selectable' or p.set_group_as_sel_3 = 'f' and p.set_module_as_3 != 'Selectable') \
			or (p.set_group_as_sel_3 = 'f' and p.set_module_as_3 = 'Selectable' and ll.select_mod_3 = 't' ) \
			or (p.set_module_as_3 = 'Selectable' and ll.select_mod_3 = 't') \
			or (select_mod_gp_3 = 't' and p.set_module_as_3 = 'Selectable' and ll.select_mod_3 = 't' )) \
			and p.id = %s and l.id = %s \
		union all \
		select distinct pl.module_id_4, m.module_fee from lis_program p, program_module_line pl, cs_module m, learner_info l, \
			learner_mode_line ll \
			where p.id = pl.prog_mod_id_4 and pl.module_id_4 = m.id and l.program_learner = p.id \
			and ll.qualification_module_id_4 = l.id  \
			and ((select_mod_gp_4 = 't' and p.set_module_as_4 != 'Selectable' or p.set_group_as_sel_4 = 'f' and p.set_module_as_4 != 'Selectable') \
			or (p.set_module_as_4 = 'Selectable' and ll.select_mod_4 = 't') \
			or (select_mod_gp_4 = 't' and p.set_module_as_4 = 'Selectable' and ll.select_mod_4 = 't' )) \
			and p.id = %s and l.id = %s \
		union all \
		select distinct pl.module_id_5, m.module_fee from lis_program p, program_module_line pl, cs_module m, learner_info l, \
			learner_mode_line ll \
			where p.id = pl.prog_mod_id_5 and pl.module_id_5 = m.id and l.program_learner = p.id \
			and ll.qualification_module_id_5 = l.id \
			and ((select_mod_gp_5 = 't' and p.set_module_as_5 != 'Selectable' or p.set_group_as_sel_5 = 'f' and p.set_module_as_5 != 'Selectable') \
			or (p.set_group_as_sel_5 = 'f' and p.set_module_as_5 = 'Selectable' and ll.select_mod_5 = 't' ) \
			or (p.set_module_as_5 = 'Selectable' and ll.select_mod_5 = 't') \
			or (select_mod_gp_5 = 't' and p.set_module_as_5 = 'Selectable' and ll.select_mod_5 = 't' )) \
			and p.id = %s and l.id = %s \
		union all \
		select distinct pl.module_id_6, m.module_fee from lis_program p, program_module_line pl, cs_module m, learner_info l, \
			learner_mode_line ll \
			where p.id = pl.prog_mod_id_6 and pl.module_id_6 = m.id and l.program_learner = p.id \
			and ll.qualification_module_id_6 = l.id \
			and ((select_mod_gp_6 = 't' and p.set_module_as_6 != 'Selectable' or p.set_group_as_sel_6 = 'f' and p.set_module_as_6 != 'Selectable') \
			or (p.set_group_as_sel_6 = 'f' and p.set_module_as_6 = 'Selectable' and ll.select_mod_6 = 't' ) \
			or (p.set_module_as_6 = 'Selectable' and ll.select_mod_6 = 't') \
			or (select_mod_gp_6 = 't' and p.set_module_as_6 = 'Selectable' and ll.select_mod_6 = 't' )) \
			and p.id = %s and l.id = %s" % (progid, learner_id, progid, learner_id, progid, learner_id, progid, learner_id, progid, learner_id, progid, learner_id)
		cr.execute(sql)
		pay_recs = cr.fetchall()		

		sub_lines = []
		for i in pay_recs:
			sub_lines.append({'item_name':i[0], 'cost':i[1]})
			
		val.update({'payment_learner': sub_lines})
		return {'value': val}	
		
# EOF	
		
#Image
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

#Learner 11 Tabs Display		
	def views_enroll(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'learner_form')
		view_id = view_ref and view_ref[1] or False
		#self.onchange_class_hist(self,cr,uid,ids,'Learner 1')
		return {
		'type': 'ir.actions.act_window',
		'name': _('Learner'),
		'res_model': 'learner.info',
		'view_type': 'form',
		'res_id': ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		}

#Schedule Tab Info
	def _onchange_populate_schedule(self, cr, uid,  context=None):
		obj = self.pool.get('class.info')
		ids = obj.search(cr, uid, [('parent_id','=',0)])
		res = obj.read(cr, uid, ids, ['start_date'], context)
		res = [(r['start_date'], r['start_date']) for r in res]
		return res
		
	def onchange_populate_schedule2(self, cr, uid, ids, i_centre, i_mod, s_date, context=None):
		'''obj = self.pool.get('class.info')
		ids = obj.search(cr, uid, [('location_id','=',i_centre)])
		res = obj.read(cr, uid, ids, ['start_date'], context)
		res = [(r['start_date'], r['start_date']) for r in res]
		return {'value':{'sch_date':res}}'''
		
		val2 ={}
		sub_lines = []
		val2.update({'session_no':''})
		val2.update({'week_no': ''})
		val2.update({'date_schd': ''})
		#raise osv.except_osv(_('Warning!'),_('Nationality %s %s %s ')%(i_centre,i_mod,s_date))
		if i_centre and i_mod and s_date:
			sql = "select class_code, start_date, end_date from class_info where location_id = %s and module_id = %s and start_date = '%s'" % (i_centre,i_mod,s_date) 
			cr.execute(sql)
			itm = cr.fetchall()
			sub_lines = []
			val2.update({'class_code': ''})
			val2.update({'start_date': ''})
			val2.update({'end_date': ''})
			val2.update({'schedule_line': sub_lines})
			for s in itm:
				
				val2.update({'class_code': s[0]})
				val2.update({'start_date': s[1]})
				val2.update({'end_date': s[2]})
			
				p_obj = self.pool.get('class.info')
				value_ids = p_obj.search(cr, uid, [('module_id', '=', i_mod)])
				
				#sub_lines.append({'session_no':'', 'week_no':'', 'date_schd':''})
				
				for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
					sub_lines.append({'session_no':prog_line['sess_no'], 'week_no':prog_line['week_no'], 'date_schd':prog_line['start_date']})
					
				val2.update({'schedule_line': sub_lines})
			
			return {'value': val2}
		else:
			return val2

	def _load_prog_mod_line(self, cr, uid, ids, field_names, args,  context=None):
		prog_mod_obj = self.pool.get('calling.test.line')
		#_logger.info('Mod G1 =============================== = %s', prog_mod_obj[0].test_mod_id)
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('testing_id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['test_mod_id'].id)
			
		value_ids = self.pool.get('test.info').search(cr, uid, [('test_def_id', 'in', module_ids)])
		return dict([(id, value_ids) for id in ids])
			
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

	'''def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):

		res = super(learner_info, self).read(cr, uid, ids, fields, context, load)
		val = {}
		sub_lines = []
		i_learner = 'Learner 1'
		if i_learner:
			sql = "select distinct c.name, cm.name, c.start_date, c.end_date from class_info c, learner_line l, cs_module cm, learner_info li where l.learner_mod_id = c.id and cm.id =  c.module_id	 and l.learner_id = li.id and li.name = '%s'" % (i_learner) 
			cr.execute(sql)
			itm = cr.fetchall()
			
			sub_lines = []
			for s in itm:
				sub_lines.append({'class_code':s[0], 'module_name':s[1], 'start_date':s[2], 'end_date':s[3]})
				
			val.update({'class_history_line': sub_lines})
			return res'''

#Class History Tab, Test History Tab & Test Scores Info			
	'''def onchange_class_hist(self, cr, uid, ids, i_learner, i_test_history, i_test_score, context=None):
		val ={}
		sub_lines = []
#Class History Tab
		if i_learner:
			sql = "select distinct c.name, cm.name, c.start_date, c.end_date from class_info c, learner_line l, cs_module cm, learner_info li where l.learner_mod_id = c.id and cm.id =  c.module_id and l.learner_id = li.id and li.name = '%s'" % (i_learner) 
			cr.execute(sql)
			itm = cr.fetchall()
			
			sub_lines = []
			for s in itm:
				sub_lines.append({'class_code':s[0], 'module_name':s[1], 'start_date':s[2], 'end_date':s[3]})
				
			val.update({'class_history_line': sub_lines})
# Test History Tab			
		if i_test_history:
			sql = "select distinct t.name, ti.test_code, ti.start_date, t.test_status from test t, test_info ti, test_learner tl, learner_info li where tl.learner_mod_id = tl.id and li.name = '%s'" % (i_test_history) 
			cr.execute(sql)
			itm = cr.fetchall()
			
			sub_lines = []
			for s in itm:
				sub_lines.append({'test_type':s[0], 'test_code':s[1], 'test_date':s[2], 'test_status':s[3]})
			val.update({'test_history_line': sub_lines})
# Test Scores Tab			
		if i_test_score:
			sql = "select distinct t.name, ti.test_code, ti.start_date from test t, test_info ti, test_learner tl, learner_info li where tl.learner_mod_id = tl.id and li.name = '%s'" % (i_test_score) 
			cr.execute(sql)
			itm = cr.fetchall()
			
			sub_lines = []
			for s in itm:
				sub_lines.append({'test_score_type':s[0], 'test_sc_code':s[1], 'test_sc_date':s[2]})
			val.update({'test_score_line': sub_lines})
			
			return {'value': val}'''
			
	'''def self_call(self, cr, uid, ids, context=None):
		raise osv.except_osv(_('Warning!'),_('qualification award %s')%(1))
		self.onchange_class_hist(cr, uid, ids, 'Learner 1',context=context)
		return True'''
		
	def _calculate_total_checklist(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = line.checklist_tab or []
			_logger.info("total id %s",mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
		return res
		
		
#dob
	def months_between(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
	
	def onchange_dob(self, cr, uid, ids, dob, context=None):
		if dob:
			d = self.months_between(dob, str(datetime.datetime.now().date()))
			res = {'value':{}}
			if d < 0:
				res['value']['birth_date'] = ''
				res.update({'warning': {'title': _('Warning !'), 'message': _('Please enter correct date, future date not allowed.')}})
				return res
			return dob		
		
#Module Status
	def _learner_status_display_1(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['learner_status']
		return res

	def _learner_status_display_2(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['learner_status']
		return res
		
	def _learner_status_display_3(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}

		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line['learner_status']
		return res
		
	def  ValidateEmail(self, cr, uid, ids, email_id):
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email_id) != None:
			return True
		else:
			raise osv.except_osv('Invalid Email', 'Please enter a valid email address')
			
	def _mobile_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.mobile_no < 0:
				return False
		return True
		
	def _landline_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.landline_no < 0:
				return False
		return True
		
	def _office_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.office_no < 0:
				return False
		return True
		
	def _salary_range(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.salary < 0:
				return False
		return True
		
	
	def _check_email(self, cr, uid, ids, context=None):
		rec = self.browse(cr, uid, ids)
		cnt = 0
		for data in rec:
			xcv = data['email_id']
			if xcv:
				if len(str(xcv)) < 7:
					raise osv.except_osv(_('Warning!'),_('Email id not valid. %s') % (xcv))

				if xcv:
					for i in xcv:
						if i=='@' or i=='.':
							cnt = cnt + 1

		if xcv and cnt < 2:
			raise osv.except_osv(_('Warning!'),_('Email id not valid. %s') % (xcv))
		else:
			return True
	
#Table Learner Info
	_name = "learner.info"
	_description = "This table is for keeping location data"
	_columns = {
		'learner_id': fields.char('Id',size=20),
		'name': fields.char('Name', size=100,required=True, select=True),
		'learnerfull_name': fields.char('Name as in NRIC/FIN', size=20),
		'learner_nric': fields.char('NRIC', size=20),
		'learner_status': fields.selection((('Active','Active'),('InActive','InActive'),('Complete','Complete'),('InComplete','InComplete'),('Blocked','Blocked')),'Status'),
		'learner_status_display_1': fields.function(_learner_status_display_1, readonly=1, type='char'),
		'learner_status_display_2': fields.function(_learner_status_display_2, readonly=1, type='char'),
		'learner_status_display_3': fields.function(_learner_status_display_3, readonly=1, type='char'),
		'date1': fields.date('Date Created', readonly='True'),
		'date2': fields.date('Date Created', readonly='True'),
		'program_learner': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True),
		'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True, store=True),
		'image': fields.binary("Photo",
            help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized photo", type="binary", multi="_get_image",
            store = {
                'learner.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the employee. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Smal-sized photo", type="binary", multi="_get_image",
            store = {
                'learner.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized photo of the employee. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."), 
		#checklist Tab
		'checklist_tab': fields.one2many('checklist.module','checklist_id','checklist'),
		#Schedule Tab
		'schedule_line': fields.one2many('schedule.module','session_no','schedule'),
		'select_center':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True),
		'select_module':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
		'class_code':fields.char('Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly=1),
		'end_date':fields.date('End Date', readonly=1),
		'sch_date':fields.selection((_onchange_populate_schedule), 'Select Date', type='char'),
		#'sch_date':fields.many2one('class.info', 'start_date'),
		#payment
		'payment_learner':fields.one2many('payment.module','pay_id','Payment', readonly=1),
		'Grand_total':fields.integer('Grand Total', readonly=1),
		#Personal Tab Fields
		'nationality':fields.many2one('res.country', 'Nationality'),
		'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
		'race':fields.selection((('Race1','Race1'),('Race2','Race2')),'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		#Education
		'high_qualification':fields.selection((('No Formal Qualification & Lower Primary','No Formal Qualification & Lower Primary'),('Primary PSLE','Primary PSLE'),('Lower Secondary','Lower Secondary'),('N Level or equivalent','N Level or equivalent'),
		('O Level or equivalent','O Level or equivalent'),('A Level or equivalent','A Level or equivalent'),('ITE Skills Certification (ISC)','ITE Skills Certification (ISC)'),('Higher NITEC','Higher NITEC'),('NITEC/Post Nitec','NITEC/Post Nitec'),
		('Polytechnic Diploma','Polytechnic Diploma'),('WSQ Diploma','WSQ Diploma'),('Professional Qualification & Other Diploma','Professional Qualification & Other Diploma'),('University First Degree','University First Degree'),
		('University Post-graduate Diploma & Degree/Master/Doctorate','University Post-graduate Diploma & Degree/Master/Doctorate'),('WSQ Certificate','WSQ Certificate'),('WSQ Higher Certificate','WSQ Higher Certificate'),('WSQ Advance Certificate','WSQ Advance Certificate'),
		('WSQ Diploma','WSQ Diploma'),('WSQ Specialist Diploma','WSQ Specialist Diploma'),('WSQ Graduate Diploma','WSQ Graduate Diploma'),('Others','Others'),('Not Reported','Not Reported')),'Highest Qualification'),
		'language_proficiency':fields.boolean('Language Proficiency'),
		#Work
		'salary':fields.char('Salary Range'),
		#Contact
		'email_id': fields.char('Email'),
		'addr_1': fields.text('Address'),
		'mobile_no': fields.integer('Mobile No', size=9),
		'landline_no': fields.integer('Home Number', size=9),
		'office_no': fields.integer('Office', size=9),
		#Modules
		'learner_mod_line': fields.one2many('learner.mode.line', 'qualification_module_id_1', 'Order Lines', select=True),
		'learner_mod_line_2': fields.one2many('learner.mode.line', 'qualification_module_id_2', 'Order Lines', select=True),
		'learner_mod_line_3': fields.one2many('learner.mode.line', 'qualification_module_id_3', 'Order Lines', select=True),
		'learner_mod_line_4': fields.one2many('learner.mode.line', 'qualification_module_id_4', 'Order Lines', select=True),
		'learner_mod_line_5': fields.one2many('learner.mode.line', 'qualification_module_id_5', 'Order Lines', select=True),
		'learner_mod_line_6': fields.one2many('learner.mode.line', 'qualification_module_id_6', 'Order Lines', select=True),
		# Module No.
		'no_module_box1': fields.boolean('1'),
		'no_module_box2': fields.boolean('2'),
		'no_module_box3': fields.boolean('3'),
		'no_module_box4': fields.boolean('4'),
		'no_module_box5': fields.boolean('5'),
		'no_module_box6': fields.boolean('6'),
		#1
		'mod_gp_name_1': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_1': fields.boolean('Select Group'),
		#'set_group_as_sel_1': fields.many2one('lis.program', 'Selectable', ondelete='cascade', help='Program'),
		'set_group_as_sel_1': fields.boolean('Select Group'),
		'set_module_select_1': fields.boolean('Select'),
		'min_no_modules_1': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_1': fields.integer('Maximum Modules', readonly=1),
		#2
		'mod_gp_name_2': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_2': fields.boolean('Select Group'),
		'set_group_as_sel_2': fields.boolean('Select Group'),
		'set_module_select_2': fields.boolean('Select'),
		'min_no_modules_2': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_2': fields.integer('Maximum Modules', readonly=1),
		#3
		'mod_gp_name_3': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_3': fields.boolean('Select Group'),
		'set_group_as_sel_3': fields.boolean('Select Group'),
		'set_module_select_3': fields.boolean('Selectable'),
		'min_no_modules_3': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_3': fields.integer('Maximum Modules', readonly=1),
		#4
		'mod_gp_name_4': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_4': fields.boolean('Select Group'),
		'set_group_as_sel_4': fields.boolean('Select Group'),
		'set_module_select_4': fields.boolean('Selectable'),
		'min_no_modules_4': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_4': fields.integer('Maximum Modules', readonly=1),
		#5
		'mod_gp_name_5': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_5': fields.boolean('Select Group'),
		'set_group_as_sel_5': fields.boolean('Select Group'),
		'set_module_select_5': fields.boolean('Selectable'),
		'min_no_modules_5': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_5': fields.integer('Maximum Modules', readonly=1),
		#6
		'mod_gp_name_6': fields.char('Module Group Name', readonly=1),
		'select_mod_gp_6': fields.boolean('Select Group'),
		'set_group_as_sel_6': fields.boolean('Select Group'),
		'set_module_select_6': fields.boolean('Selectable'),
		'min_no_modules_6': fields.integer('Minimum Module', readonly=1),
		'max_no_modules_6': fields.integer('Maximum Modules', readonly=1),
		'outstanding_line': fields.one2many('outstanding.module','outstanding_id','outstanding'),
		'action_learn_line': fields.one2many('action.learn.module','action_id','Action'),
		'class_history_line': fields.one2many('class.history.module','class_id','Class History', readonly=1),
		'test_history_line': fields.one2many('test.history.module', 'test_id', 'Test'),
		#'calling_fun_info': fields.function(_load_prog_mod_line, relation="calling.test.line",readonly=1,type='one2many', string='Test'),
		'test_score_line': fields.one2many('test.score.module','test_score_id','Test Scores',readonly=1),
		'qualification_line': fields.one2many('qualification.module','qualify_id','Qualification & Awards',readonly=1),
		'assets_line': fields.one2many('assets.learner.module','asset_id','Assets'),
		'feedback_line': fields.one2many('feedback.module','feedback_id','Feedback'),
		'remarks_line': fields.one2many('remarks.module','remarks_id','Remarks'),
		'race':fields.many2one('race', 'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		'emp_staus': fields.many2one('employee.status', 'Employee Status'),
		'company_name':fields.many2one('company', 'Company'),
		'desig_detail':fields.many2one('designation', 'Designation'),
		'sponsor_ship':fields.many2one('sponsership', 'Sponsership'),
		'actual_number':fields.function(_calculate_total_checklist, relation="learner.info",readonly=1,string='No. Checklist',type='integer'),
		#'calling_fun_info': fields.one2many('calling.test.line', 'testing_id'),
	}
	
	_defaults = { 
	   'date1': fields.date.context_today,
	   'date2': fields.date.context_today,
	}
	
	_constraints = [(_check_unique_name, 'Error: Learner Already Exists', ['name']),(_mobile_no, 'Error: Mobile Number Cannot be Negative', ['Mobile']), (_landline_no, 'Error: Landline Number Cannot be Negative', ['Landline']), (_office_no, 'Error: Office Number Cannot be Negative', ['Office']), (_salary_range, 'Error: Salary Range Number Cannot be Negative', ['Salary']), (_check_email, 'Error! Email is invalid.', ['work_email'])]

	'''def on_change_module_name2(self, cr, uid, ids, module_name, s_name):
		#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(s_name))
		val ={}
		sub_lines = []
		if s_name:
			sql = "select distinct c.name, cm.name, c.start_date, c.end_date from class_info c, learner_line l, cs_module cm, learner_info li where l.learner_mod_id = c.id and cm.id =  c.module_id	 and l.learner_id = li.id and li.name = '%s'" % (s_name) 
			cr.execute(sql)
			itm = cr.fetchall()
			
			sub_lines = []
			for s in itm:
				sub_lines.append({'class_code':s[0], 'module_name':s[1], 'start_date':s[2], 'end_date':s[3]})
			val.update({'class_history_line': sub_lines})
			
			return {'value': val}'''	
			
learner_info ()

class calling_fun(osv.osv):
	_name = "calling.test.line"
	_description = "Module Line"
	_columns = {
		'testing_id': fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Program', select=True),
		'test_mod_id': fields.many2one('test.info', 'Test', ondelete='cascade', help='Test', select=True),
		'test_name': fields.related('test_mod_id','name',type="char",relation="test.info",string="Test Name", readonly=1),
		'tests_code': fields.related('test_mod_id','test_code',type="char",relation="test.info",string="Test Code", readonly=1),
		'tests_status': fields.related('test_mod_id','test_status',type="char",relation="test.info",string="Test Status", readonly=1),
	}
calling_fun()


#Class Program Module Line
###############
globvar = 0
class program_mod_line(osv.osv):
	_name = "learner.mode.line"
	_description = "Module Line"
	_columns = {
		'qualification_module_id': fields.many2one('learner.info'),
	#1
		'prog_mod_id': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', readonly=1),
		'qualification_module_id_1': fields.many2one('learner.info'),
		'name': fields.related('qualification_module_id', 'name', relation='learner.info'),
		'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', readonly=1),
		'check_module_select_1': fields.boolean('Selectable'),
		'select_mod_1': fields.boolean('Select', select=True, store=True),		
	#2
		'prog_mod_id_2': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', readonly=1),
		'qualification_module_id_2': fields.many2one('learner.info'),
		'module_id_2':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', readonly=1),
		'check_module_select_2': fields.boolean('Selectable'),
		'select_mod_2': fields.boolean('Select'),
	#3
		'prog_mod_id_3': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', readonly=1),
		'qualification_module_id_3': fields.many2one('learner.info'),
		'module_id_3':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', readonly=1),
		'check_module_select_3': fields.boolean('Selectable'),
		'select_mod_3':fields.boolean('Select'),
	#4
		'prog_mod_id_4': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', readonly=1),
		'qualification_module_id_4': fields.many2one('learner.info'),
		'module_id_4':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', readonly=1),
		'check_module_select_4': fields.boolean('Selectable'),
		'select_mod_4': fields.boolean('Select'),
	#5
		'prog_mod_id_5': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', readonly=1),
		'qualification_module_id_5': fields.many2one('learner.info'),
		'module_id_5':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', readonly=1),
		'check_module_select_5': fields.boolean('Selectable'),
		'select_mod_5': fields.boolean('Select'),
	#6
		'prog_mod_id_6': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', readonly=1),
		'qualification_module_id_6': fields.many2one('learner.info'),
		'module_id_6':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', readonly=1),
		'check_module_select_6': fields.boolean('Selectable'),
		'select_mod_6': fields.boolean('Select'),
    }
program_mod_line()	

#Class Enrollment Info
###############

class enroll_info(osv.osv):

#Image
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	def true_false_control(self, cr, uid, ids, context=None):
		if val:
			raise osv.except_osv(_('Warning', _('Test')))

#Validate Email			
	def  ValidateEmail(self, cr, uid, ids, email_id):
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email_id) != None:
			return True
		else:
			raise osv.except_osv('Invalid Email', 'Please enter a valid email address')
				
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
		
#Nationality Info				
	def _nationality_get(self, cr, uid, ids, context=None):
		ids = self.pool.get('res.country').search(cr, uid, [('name', '=', 'Singapore')], context=context)
		#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(ids[0]))
		if ids:
			return ids[0]
		return False			
	_name = "enroll.info"
	_description = "This table is for keeping location data"
	_columns = {
	    'location_id': fields.char('Id',size=20),
		'name': fields.char('Name', size=30,required=True, select=True),
		'full_name': fields.char('Name as in NRIC/FIN', size=30),
		'nric': fields.char('NRIC', size=30),
		'program_info': fields.selection((('prog A','Prog A'),('prog B','prog B')),'Program'),
		'program_learner': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True),
		'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True, store=True),
		'module_line': fields.one2many('enroll.module.line','module_id','Module'),
		'check_line': fields.one2many('checklist.module','en_checklist_id','checklist'),
		'schedule_line': fields.one2many('schedule.module','session_no','schedule'),
		'select_center':fields.selection((('Center A','Center A'),('Center B','Center B'),('Center C','Center C'),),'Select Center'),
		'select_module':fields.selection((('Module 1','Module 1'),('Module 2','Module 2'),('Module 3','Module 3'),),'Select Module'),
		'date_1':fields.date('Date', readonly='True'),
		'class_code':fields.char('Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly='True'),
		'end_date':fields.date('End Date', readonly='True'),
		'personal_line': fields.one2many('personal.module','personal_id','Personal Details'),
		'nationality':fields.many2one('res.country', 'Nationality'),
		'marital_status':fields.selection((('Single','Single'),('Married','Married')),'Marital Status'),
		'race':fields.selection((('Race1','Race1'),('Race2','Race2')),'Race'),
		'gender':fields.selection((('Male','Male'),('Female','Female')),'Gender'),
		'birth_date':fields.date('Birth Date'),
		'high_qualification':fields.selection((('No Formal Qualification & Lower Primary','No Formal Qualification & Lower Primary'),('Primary PSLE','Primary PSLE'),('Lower Secondary','Lower Secondary'),('N Level or equivalent','N Level or equivalent'),
		('O Level or equivalent','O Level or equivalent'),('A Level or equivalent','A Level or equivalent'),('ITE Skills Certification (ISC)','ITE Skills Certification (ISC)'),('Higher NITEC','Higher NITEC'),('NITEC/Post Nitec','NITEC/Post Nitec'),
		('Polytechnic Diploma','Polytechnic Diploma'),('WSQ Diploma','WSQ Diploma'),('Professional Qualification & Other Diploma','Professional Qualification & Other Diploma'),('University First Degree','University First Degree'),
		('University Post-graduate Diploma & Degree/Master/Doctorate','University Post-graduate Diploma & Degree/Master/Doctorate'),('WSQ Certificate','WSQ Certificate'),('WSQ Higher Certificate','WSQ Higher Certificate'),('WSQ Advance Certificate','WSQ Advance Certificate'),
		('WSQ Diploma','WSQ Diploma'),('WSQ Specialist Diploma','WSQ Specialist Diploma'),('WSQ Graduate Diploma','WSQ Graduate Diploma'),('Others','Others'),('Not Reported','Not Reported')),'Highest Qualification'),
		'language_proficiency':fields.boolean('Language Proficiency'),
		#'emp_staus':fields.selection((('Employed','Employed'),('Unemployed','Unemployed'),('Self Emp','Self Emp')),'Employement Status'),
		#'company_name':fields.selection((('ASZ','ASZ'),('HCL','HCL'),('CGI','CGI')),'Company'),
		'desig_detail':fields.selection('designation', 'Designation'),
		#'salary_range':fields.integer('Salary Range', size=14),
		'sponsor_ship':fields.selection((('LG','LG'),('DELL','DELL'),('THUMPS UP','THUMPS UP')),'Sponsorship'),
		'email_id': fields.char('Email', size=30),
		'addr_1': fields.text('Address'),	
		'mobile_no': fields.integer('Mobile No'),
		'landline_no': fields.integer('Home Number'),
		'office_no': fields.integer('Office'),
		#'payment_history': fields.one2many('payment.history.module','payment_id','Payment History'),
		'history_line': fields.one2many('history.learner.module','history_id','history'),
		'image': fields.binary("Photo",
			help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
			string="Medium-sized photo", type="binary", multi="_get_image",
			store = {
				'enroll.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Medium-sized photo of the employee. It is automatically "\
				"resized as a 128x128px image, with aspect ratio preserved. "\
					"Use this field in form views or some kanban views."),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
			string="Smal-sized photo", type="binary", multi="_get_image",
			store = {
				'enroll.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Small-sized photo of the employee. It is automatically "\
				"resized as a 64x64px image, with aspect ratio preserved. "\
				"Use this field anywhere a small image is required."),
	}
	_constraints = [(_check_unique_name, 'Error: Learner Already Exists', ['name'])]
enroll_info ()

#Class Enroll Module Line
###############

class enroll_module_line(osv.osv):
	_name = "enroll.module.line"
	_description = "Module Tab"
	_columns = {
	'enroll_id' : fields.many2one('enroll.info', 'Id'), 
	'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
	'enroll_code': fields.related('module_id','module_code',type="char",relation="cs.module",string="Module Code", readonly=1),	
	}
	
enroll_module_line()

#Class Checklist
###############

class checklist(osv.osv):

	def import_file(self, cr, uid, ids, context=None):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(data)) 
	 # your treatment
		return
		
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(checklist, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	 
	_name ='checklist.module'
	_description ="checklist Tab"
	_columns = {
		'checklist_id' : fields.many2one('learner.info'),
		'en_checklist_id' : fields.many2one('enroll.info'),
		's_no' : fields.integer('S.No',size=20, readonly=1),
		'item':fields.many2one('master.show.do', 'Item', ondelete='cascade'),
		'confirmation':fields.boolean('Confirmation' , readonly=1),
		'upload_docs':fields.binary('Upload Documents'),
		'datas_fname': fields.char('File Name'),
		'file_type': fields.char('Content Type'),
		'index_content': fields.text('Indexed Content'),
	}
	
	def _index(self, cr, uid, data, datas_fname, file_type):
		mime, icont = cntIndex.doIndex(data, datas_fname,  file_type or None, None)
		icont_u = ustr(icont)
		return mime, icont_u
        
	def create(self, cr, uid, vals, context=None):
		if context is None:
			context = {}
		if vals.get('upload_docs', False):
			vals['file_type'], vals['index_content'] = self._index(cr, uid, vals['upload_docs'].decode('base64'), vals.get('datas_fname', False), None)
		return super(checklist, self).create(cr, uid, vals, context)

	def write(self, cr, uid, ids, vals, context=None):
		if context is None:
			context = {}
		if vals.get('upload_docs', False):
			vals['file_type'], vals['index_content'] = self._index(cr, uid, vals['upload_docs'].decode('base64'), vals.get('datas_fname', False), None)
		return super(checklist, self).write(cr, uid, ids, vals, context)
checklist()

#Class Schedule
###############
class schedule(osv.osv):

	_name ='schedule.module'
	_description ="schedule Tab"
	_columns = {
		'session_no' : fields.integer('Session No', size=10, readonly=1),
		'week_no' : fields.integer('Week No', size=20, readonly=1),
		'date_schd': fields.date('Date', readonly='True'),
	}
schedule ()

#Personal Details Race Field

class master_race1(osv.osv):
	def _check_unique_race(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='race'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Race'),
	}
	_constraints = [(_check_unique_race, 'Error: Race Already Exists', ['Race'])]
master_race1()

#Employement Status Company Field
class employee_status(osv.osv):
	def _check_employee_status(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='employee.status'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Employee Status'),
	}
	_constraints = [(_check_employee_status, 'Error: Employee Status Already Exists', ['Status'])]
employee_status()

#Personal Details Company Field
class master_company(osv.osv):
	def _check_master_company(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='company'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Company'),
	}
	_constraints = [(_check_master_company, 'Error: Company Status Already Exists', ['Company'])]
master_company()

#Personal Details Designation Field
class master_desig(osv.osv):
	def _check_master_desig(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='designation'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Designation'),
	}
	_constraints = [(_check_master_desig, 'Error: Designation Status Already Exists', ['Designation'])]
master_desig()

#Personal Details Sponsership Field
class master_sponser(osv.osv):
	def _check_unique_sponser(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
		
	_name ='sponsership'
	_description ="People and Facilites Tab"
	_columns = {
	'name':fields.char('Sponsership'),
	}	
	_constraints = [(_check_unique_sponser, 'Error: Sponsership Already Exists', ['Sponsership'])]	
master_sponser()

# With 5 tab Payment (Learner info)
class payment(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(payment, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	_name ='payment.module'
	_description ="payment Tab"
	_columns = {
		'pay_id':fields.integer('Id',size=20, readonly=1),
		's_no' : fields.integer('S.No', size=50, readonly=1),
		'item_name' : fields.many2one('cs.module', 'Module Name'),
		'cost': fields.float('Cost', size=9),
	}
payment ()

#Learner Outstanding Tab
class outstanding(osv.osv):	

	def import_Upload_Documents1(self, cr, uid, ids, context=None):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(outs_upload_docs)) 

		# your treatment
		return		

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(outstanding, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	_name = "outstanding.module"
	_description = "outstanding Tab"
	_columns = {
	'outstanding_id' : fields.integer('Id',size=20, readonly=1), 
	's_no' : fields.integer('S.No',size=20, readonly=1),
	#'outs_item':fields.char('Item'),
	'outs_item':fields.many2one('master.show.do', 'Item', ondelete='cascade', readonly=1),
	'outs_confirmation':fields.boolean('Confirmation', readonly=1),
	'outs_upload_docs':fields.binary('Upload Documents', size=20),
	}
	
	def on_change_program_id(self, cr, uid, ids, program_id):
		module_obj = self.pool.get('lis.program').browse(cr, uid, program_id)
		return {'value': {'outs_item': module_obj.outs_item, 'outs_confirmation': module_obj.outs_confirmation}}
		
	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'learner_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('outstanding.module')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['program_id'].id)
		ctx = dict(context)
		#this will return product tree view and form view. 
		ctx.update({
			'ctx': True
		})
		return {
		'type': 'ir.actions.act_window',
		'item': _('outs_item'),
		'res_model': 'lis.program',
		'view_type': 'form',
		'res_id': module_ids[0], # this will open particular product,
		'view_id': view_id,
		'view_mode': 'form',
		'target': 'new',
		'nodestroy': True,
		'context': ctx,	
		}	
	
outstanding()

#Learner Personal Details Tab
class personal_details(osv.osv):
	_name = "personal.module"
	_description = "Personal Detail Tab"
	_columns = {
	'personal_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
personal_details()

#Learner Action Tab
class action_learn(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(action_learn, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
				
	def _current_user(self, cr, uid, ids, context=None):
		return uid		
				
		
	def import_file(self, cr, uid, ids, context=None):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(data)) 
	 # your treatment
		return
		
	_name = "action.learn.module"
	_description = "Action Tab"
	_columns = {
	'action_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'action_learner': fields.selection((('Withdrawal','Withdrawal'),('Reassignment','Reassignment'),('Call','Call'),),'Action'),
	'remarks_learner': fields.char('Remarks'),
	'support_docs_learner': fields.char('Supported Documents'),
	'date_action':fields.date('Date of Action'),
	'action_taken_learner': fields.many2one('res.users','Action Taken By'),
	'upload_learner':fields.binary('Upload Documents'),
	'datas_fname': fields.char('File Name'),
	'index_content': fields.text('Indexed Content'),
	}	
	_defaults = {
	   'action_taken_learner': _current_user,
	   }
action_learn()

#Learner Payment History Tab


#Learner Class History Tab
class class_history(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(class_history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
	
	'''def onchange_populate_class_history(self, cr, uid, ids, mod_id, context=None):
		sched_obj = self.pool.get('class.info')
		value_ids = sched_obj.search(cr, uid, [('module_id', '=', mod_id)])
		res = {'value':{}}
		res['value']['class_code'] = 0
		res['value']['Date_Commenced'] = ''
		res['value']['Date_Completed'] = ''
		for sched_line in sched_obj.browse(cr, uid, value_ids,context=context):
			res['value']['class_code'] = sched_line.id
			res['value']['Date_Commenced'] = sched_line.Date_Commenced
			res['value']['Date_Completed'] = sched_line.Date_Completed
		return res '''
		
		
	_name = "class.history.module"
	_description = "Class History Tab"
	_columns = {
	'class_id' : fields.many2one('learner.info', ondelete='cascade'), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'program_name': fields.many2one('lis.program','Program', 'program_learner', ondelete='cascade', help='Program', select=True),
	'module_name':fields.many2one('cs.module', 'Module', ondelete='cascade'),
	'class_code':fields.char('Class Code'),
	'start_date': fields.date('Date Commenced'),
	'end_date': fields.date('Date Completed'),
	'empl_staus': fields.selection((('Employed','Employed'),('Unemployed','Unemployed'),('Self Emp','Self Emp')),'Employement Status'),
	'designa_detail':fields.selection((('Developer','Developer'),('Tester','Tester'),('HR','HR')),'Designation'),
	'sponsors_ship':fields.selection((('LG','LG'),('DELL','DELL'),('THUMPS UP','THUMPS UP')),'Sponsorship'),
	}
	
	def on_change_prog_name(self, cr, uid, ids, program_name):
		module_obj = self.pool.get('lis.program').browse(cr, uid, program_name)
		return {'value': {'program_name': module_obj.program_name}}	
		
		
	#def on_change_module_name(self, cr, uid, ids, module_name, name):
		#self.onchange_class_hist(cr, uid, ids, name, context=context)
		#return True
		#module_obj = self.pool.get('cs.module').browse(cr, uid, module_name)
		#return {'value': {'module_name': module_obj.module_name}}	

class_history()

#Learner Test History Tab
class test_history(osv.osv):
	_name = "test.history.module"
	_description = "Test History Tab"
	_columns = {
	'test_id' : fields.many2one('learner.info', ondelete='cascade'), 
	'test_type' : fields.many2one('test','Test', ondelete='cascade'),
	'test_code' : fields.char('Test Code',),
	'test_date' : fields.date('Test Date'),
	'test_status' : fields.char('Test Status',),
	
	}	
test_history()

#Learner Test Scores Tab
class test_score(osv.osv):
	_name = "test.score.module"
	_description = "Test Score Tab"
	_columns = {
	'test_score_id' : fields.integer('Id',size=20), 
	'test_score_type' : fields.many2one('test','Test', ondelete='cascade'),
	'test_sc_code' : fields.char('Test Code',),
	'test_sc_date' : fields.date('Test Date'),
	'test_compre' : fields.char('Compr',),
	'test_conv' : fields.char('Conv',),
	'r_level' : fields.integer('R(Level)',),
	'r_score' : fields.integer('R(Score)',),
	'l_level' : fields.integer('L(Level)'),
	'l_score' : fields.integer('L(Score)'),
	's_level' : fields.integer('S(Level)'),
	's_score' : fields.integer('S(Score)'),
	'w_level' : fields.integer('W(Level)'),
	'w_score' : fields.integer('W(Score)'),
	'w_outcomes' : fields.char('W(Outcomes)'),
	'n_level' : fields.integer('N(Level)'),
	'n_score' : fields.integer('N(Score)'),
	'w_outcome1' : fields.char('W(Outcomes)'),
	
	}	
test_score()

#Learner Qualification Tab
class qualification(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(qualification, self).read(cr, uid, ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res		
	_name = "qualification.module"
	_description = "Qualifications & Awards Tab"
	_columns = {
	'qualify_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20),
	#'qual_award_name' : fields.many2one('lis.program', 'Qualification /Award Name', ondelete='cascade', readonly=1),
	'qual_award_name' : fields.char('Qualification /Award Name', size=30),
	'prog_name' : fields.one2many('lis.program', 'qualification_module_id', 'Program Name', ondelete='cascade', help='Program', select=True),
	'module_name':fields.many2one('cs.module','Module Name', ondelete='cascade', help='Module', select=True),
	'class_code':fields.many2one('class.info', 'Class Code'),
	'date_award' : fields.date('Date Awarded'),
	}	
qualification()

class lis_program(osv.Model):
	_inherit = 'lis.program'
	
	_columns = {
		'qualification_module_id':fields.many2one('qualification.module', 'Qualification Module'),
	}

#Learner Assets Tab
class assets(osv.osv):
	_name = "assets.learner.module"
	_description = "Assets Tab"
	_columns = {
	'asset_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	
	}	
assets()

#Learner Feedback Tab
class feedback(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(feedback, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	#def _current_user(self, cr, uid, ids, context=None):
	#	return self.pool.get('res.users').browse(cr, uid,uid, context=context),

	def _current_user(self, cr, uid, ids, context=None):
		return uid
		#ids = self.pool.get('res.users').search(cr, uid, context=context)
		#if ids:
		#	return ids[0]
		#return False
		
	_name = "feedback.module"
	_description = "Feedback Tab"
	_columns = {
	'feedback_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'feedback_type': fields.selection((('Negative','Negative'),('Complaint','Complaint'),('Positive','Positive')),'Feedback Type'),
	'description' : fields.text('Description'),
	'date_of_feedback' : fields.date('Date of Feedback'),
	'entered_by' : fields.many2one('res.users','Entered By'),
	}	
	
	_defaults = {
	   'entered_by': _current_user,
	   'date_of_feedback': fields.date.context_today,
	}
	
	_order = "date_of_feedback desc"
feedback()

#Learner Remarks Tab
class remarks(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(remarks, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	def _current_user(self, cr, uid, ids, context=None):
		return uid
		#ids = self.pool.get('res.users').search(cr, uid, context=context)
		#if ids:
		#	return ids[0]
		#return False
		
	_name = "remarks.module"
	_description = "Remarks Tab"
	_columns = {
	'remarks_id' : fields.integer('Id',size=20), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'descriptions' : fields.char('Description'),
	'date_of_remarks' : fields.date('Date of Remarks'),
	'enter_by' :  fields.many2one('res.users','Entered By'),
	
	}	
	
	_defaults = {
	   'enter_by': _current_user,
	   'date_of_remarks': fields.date.context_today,
	   }
	_order = "date_of_remarks desc"
remarks()
	
