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

# Payment Module Function for Grand Total
	#_inherit = "payment.module"
	def _amount(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_learner:
				total += line.cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
# Payment Test Function for Grand Total
	#_inherit = "payment.module"
	def _amount_test(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_test_learner:
				total += line.test_cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
	def _total(self, cr, uid, ids, field_names, args, context=None):
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line.Grand_total + line.Grand_test_total
			
		return res
		
# Serial number for Learner_info Profile file
	'''def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):		
		res = super(learner_info, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+100
			r['s_no'] = seq_number		
		return res'''
		
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
		

#Checklist Items				
		#val ={}		
		p_obj = self.pool.get('program.show.do.module')
		value_ids = p_obj.search(cr, uid, [('program_id', '=', progid)])
		#val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'item':prog_line['master_show_do'].id})
		val.update({'checklist_tab': sub_lines})
		
# Payment Program to fetch the detailed Programs
		learner_id = 0
		for self_obj in self.browse(cr, uid, ids, context=context):
			learner_id = self_obj.id

		sql="select program_learner from learner_info where id = %s " % (learner_id)
		cr.execute(sql)
		pay_recs = cr.fetchall()
		
		sub_lines = []
		for i in pay_recs:
			sub_lines.append({'program_name':i[0]})
			
		val.update({'payment_learner': sub_lines})
		return {'value': val}

# Payment Module to fetch the detailed Modules
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

# Payment Module to fetch the detailed Modules	
	def populate_payments_write(self, cr, uid, ids, iid):
		iid = ids[0]
		#raise osv.except_osv(_('Warning!'),_('xxxxxxxxxxxxx. %s') % (iid))
		#for self_obj in self.browse(cr, uid, ids):
		#	learner_id = self_obj.id
		#	progid = self_obj.program_learner.id
		#	pay_id = self_obj.id
		#raise osv.except_osv(_('Warning!'),_('ssssssssssss. %s') % (pay_id))
		#raise osv.except_osv(_('Warning!'),_('ssssssssssss. %s %s') % (learner_id, progid))
		#raise osv.except_osv(_('Warning!'),_('aaaaaaaaa %s')%(iid))
		sql = "select l.program_learner, ll.module_id, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_1 = l.id and ll.module_id = m.id \
			and l.select_mod_gp_1 = 't' and ll.select_mod_1 = 't' \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id, m.module_fee from cs_module m, learner_info l, learner_mode_line ll, lis_program lp \
			where ll.qualification_module_id_1 = l.id and ll.module_id = m.id and lp.id = l.program_learner \
			and l.select_mod_gp_1 = 't' and lp.set_module_as_1 = 'Block' \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id_2, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_2 = l.id and ll.module_id_2 = m.id \
			and l.select_mod_gp_2 = 't' and ll.select_mod_2 = 't' \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id_2, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_2 = l.id and ll.module_id_2 = m.id \
			and l.select_mod_gp_2 = 't' and min_no_modules_2 = 0 \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id_3, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_3 = l.id and ll.module_id_3 = m.id \
			and l.select_mod_gp_3 = 't' and ll.select_mod_3 = 't' \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_3, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_3 = l.id and ll.module_id_3 = m.id \
			and l.select_mod_gp_3= 't' and min_no_modules_3 = 0 \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id_4, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_4 = l.id and ll.module_id_4 = m.id \
			and l.select_mod_gp_4 = 't' and ll.select_mod_4 = 't' \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_4, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_4 = l.id and ll.module_id_4 = m.id \
			and l.select_mod_gp_4= 't' and min_no_modules_4 = 0 \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_5, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_5 = l.id and ll.module_id_5 = m.id \
			and l.select_mod_gp_5 = 't' and ll.select_mod_5 = 't' \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_5, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_5 = l.id and ll.module_id_5 = m.id \
			and l.select_mod_gp_5= 't' and min_no_modules_5 = 0 \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_6, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_6 = l.id and ll.module_id_6 = m.id \
			and l.select_mod_gp_6 = 't' and ll.select_mod_6 = 't' \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_6, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_6 = l.id and ll.module_id_6 = m.id \
			and l.select_mod_gp_6= 't' and min_no_modules_6 = 0 \
			 and l.id = %s" % (iid, iid, iid, iid, iid, iid, iid, iid, iid, iid, iid, iid)
		cr.execute(sql)
		pay_recs = cr.fetchall()		

		obj_pay = self.pool.get('payment.module')
		#raise osv.except_osv(_('Error!'),_("qwwewew %s %s")%(1, 2))
		sql="delete from payment_module where pay_id = %s " % (iid)
		cr.execute (sql)
		for i in pay_recs:
			#raise osv.except_osv(_('Error!'),_("qwwxxxxxxxewew %s %s")%(i[0], i[1]))
			#sql="insert into "
			vals = {
				'program_name': i[0],
				'item_name': i[1],
				'cost': i[2],
				'pay_id': iid
			}
			obj_pay.create(cr, uid, vals)
		
		return True

# Payment Module to fetch the detailed Modules		
	def populate_payments_create(self, cr, uid, values, iid):	
		
		sql = "select l.program_learner, ll.module_id, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_1 = l.id and ll.module_id = m.id \
			and l.select_mod_gp_1 = 't' and ll.select_mod_1 = 't' \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_1 = l.id and ll.module_id = m.id \
			and l.select_mod_gp_1 = 't' and min_no_modules_1 = 0 \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id_2, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_2 = l.id and ll.module_id_2 = m.id \
			and l.select_mod_gp_2 = 't' and ll.select_mod_2 = 't' \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id_2, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_2 = l.id and ll.module_id_2 = m.id \
			and l.select_mod_gp_2 = 't' and min_no_modules_2 = 0 \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id_3, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_3 = l.id and ll.module_id_3 = m.id \
			and l.select_mod_gp_3 = 't' and ll.select_mod_3 = 't' \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_3, m.module_fee from cs_module m, learner_info l, learner_mode_line ll\
			where ll.qualification_module_id_3 = l.id and ll.module_id_3 = m.id \
			and l.select_mod_gp_3= 't' and min_no_modules_3 = 0 \
			and l.id = %s \
			union \
		select l.program_learner, ll.module_id_4, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_4 = l.id and ll.module_id_4 = m.id \
			and l.select_mod_gp_4 = 't' and ll.select_mod_4 = 't' \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_4, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_4 = l.id and ll.module_id_4 = m.id \
			and l.select_mod_gp_4= 't' and min_no_modules_4 = 0 \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_5, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_5 = l.id and ll.module_id_5 = m.id \
			and l.select_mod_gp_5 = 't' and ll.select_mod_5 = 't' \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_5, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_5 = l.id and ll.module_id_5 = m.id \
			and l.select_mod_gp_5= 't' and min_no_modules_5 = 0 \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_6, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_6 = l.id and ll.module_id_6 = m.id \
			and l.select_mod_gp_6 = 't' and ll.select_mod_6 = 't' \
			 and l.id = %s \
			 union \
		select l.program_learner, ll.module_id_6, m.module_fee from cs_module m, learner_info l, learner_mode_line ll \
			where ll.qualification_module_id_6 = l.id and ll.module_id_6 = m.id \
			and l.select_mod_gp_6= 't' and min_no_modules_6 = 0 \
			 and l.id = %s" % (iid, iid, iid, iid, iid, iid, iid, iid, iid, iid, iid, iid)
		cr.execute(sql)
		pay_recs = cr.fetchall()

		obj_pay = self.pool.get('payment.module')

		for i in pay_recs:
			vals = {
				'program_name': i[0],
				'item_name': i[1],
				'cost': i[2],
				'pay_id': iid
			}
			obj_pay.create(cr, uid, vals)
		
		return True
		
# Payment Module to fetch the Program name
	def populate_payments_program_create(self, cr, uid, values, iid):
		sql = "select program_learner from learner_info where id = %s " % (iid)
		cr.execute(sql)
		pay_recs = cr.fetchall()
		
		obj_pay = self.pool.get('payment.module')
		
		for i in pay_recs:
			vals = {
				'program_name': i[0],
				'pay_id': iid
			}
			obj_pay.create(cr, uid, vals)
		
		return True

# Payment Module to fetch the Program name
	def populate_payments_program_write(self, cr, uid, ids, iid):
		iid = ids[0]
		sql = "select program_learner from learner_info where id = %s " % (iid)
		cr.execute(sql)
		pay_recs = cr.fetchall()
		
		obj_pay = self.pool.get('payment.module')
		sql="delete from payment_module where pay_id = %s " % (iid)
		cr.execute (sql)
		for i in pay_recs:
			vals = {
				'program_name': i[0],
				'pay_id': iid
			}
			obj_pay.create(cr, uid, vals)
		
		return True
		
	def buttonClick():
		self.submitButton = Button(master, text="Submit", command=buttonClick)

	def create(self, cr, uid, ids, context=None):
		
		#values['status'] = 'Edit'
		id = super(learner_info, self).create(cr, uid, ids, context)
		
#--------1-----------
		
		sql="select li.max_no_modules_1 max, li.min_no_modules_1 min, count(lm.select_mod_1) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_1 \
			and lm.select_mod_1 = 't' and li.id = %s group by li.min_no_modules_1, li.max_no_modules_1" % (id)

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table"))
				
#--------2-----------
		
		sql="select li.max_no_modules_2 max, li.min_no_modules_2 min, count(lm.select_mod_2) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_2 \
			and lm.select_mod_2 = 't' and li.id = %s group by li.min_no_modules_2, li.max_no_modules_2" % (id)

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table")) 				

#--------3-----------
		
		sql="select li.max_no_modules_3 max, li.min_no_modules_3 min, count(lm.select_mod_3) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_3 \
			and lm.select_mod_3 = 't' and li.id = %s group by li.min_no_modules_3, li.max_no_modules_3" % (id)

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table")) 

#--------4-----------
		
		sql="select li.max_no_modules_4 max, li.min_no_modules_4 min, count(lm.select_mod_4) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_4 \
			and lm.select_mod_4 = 't' and li.id = %s group by li.min_no_modules_4, li.max_no_modules_4" % (id)

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table"))

#--------5-----------
		
		sql="select li.max_no_modules_5 max, li.min_no_modules_5 min, count(lm.select_mod_5) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_5 \
			and lm.select_mod_5 = 't' and li.id = %s group by li.min_no_modules_5, li.max_no_modules_5" % (id)

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table")) 				
				
#--------6-----------
		
		sql="select li.max_no_modules_6 max, li.min_no_modules_6 min, count(lm.select_mod_6) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_6 \
			and lm.select_mod_6 = 't' and li.id = %s group by li.min_no_modules_6, li.max_no_modules_6" % (id)

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table")) 	
		
		#raise osv.except_osv(_('Warning!'),_('wwwwwww %s')%(id))
		self.populate_payments_create( cr, uid, ids, id)
		self.populate_payments_program_create( cr, uid, ids, id)
		return id
		return id

	

	def write(self, cr, uid, ids, vals, context=None):
				
		id = super(learner_info, self).write(cr, uid, ids, vals, context)

#--------1-----------
		
		sql="select li.max_no_modules_1 max, li.min_no_modules_1 min, count(lm.select_mod_1) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_1 \
			and lm.select_mod_1 = 't' and li.id = %s group by li.min_no_modules_1, li.max_no_modules_1" % (ids[0])

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table"))

#--------2-----------
		
		sql="select li.max_no_modules_2 max, li.min_no_modules_2 min, count(lm.select_mod_2) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_2 \
			and lm.select_mod_2 = 't' and li.id = %s group by li.min_no_modules_2, li.max_no_modules_2" % (ids[0])

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table")) 				
				
		self.populate_payments_write(cr, uid, ids, id)

#--------3-----------
		
		sql="select li.max_no_modules_3 max, li.min_no_modules_3 min, count(lm.select_mod_3) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_3 \
			and lm.select_mod_3 = 't' and li.id = %s group by li.min_no_modules_3, li.max_no_modules_3" % (ids[0])

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table")) 

#--------4-----------
		
		sql="select li.max_no_modules_4 max, li.min_no_modules_4 min, count(lm.select_mod_4) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_4 \
			and lm.select_mod_4 = 't' and li.id = %s group by li.min_no_modules_4, li.max_no_modules_4" % (ids[0])

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table"))

#--------5-----------
		
		sql="select li.max_no_modules_5 max, li.min_no_modules_5 min, count(lm.select_mod_5) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_5 \
			and lm.select_mod_5 = 't' and li.id = %s group by li.min_no_modules_5, li.max_no_modules_5" % (ids[0])

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table")) 				
				
#--------6-----------
		
		sql="select li.max_no_modules_6 max, li.min_no_modules_6 min, count(lm.select_mod_6) \
			from learner_info li, learner_mode_line lm where li.id = lm.qualification_module_id_6 \
			and lm.select_mod_6 = 't' and li.id = %s group by li.min_no_modules_6, li.max_no_modules_6" % (ids[0])

		#sql="select count(lm.select_mod_1) from learner_info li, learner_mode_line lm where li.id = ll.qualification_module_id_1 and li.id = %s group by lp.max_no_modules_1" % (ids[0])
		cr.execute(sql)
		recs = cr.fetchall()
		obj_ml = self.pool.get('learner.mode.line')
		for i in recs:
			if i[2] < i[1]:
				#raise osv.except_osv(_('Warning!'),_('dddddd %s %s')%(i[2], i[1]))
				raise osv.except_osv(_('Error!'),_("Minimum Modules should be equal or greater than below table"))
				
			if i[2] > i[0]:
				raise osv.except_osv(_('Error!'),_("Max Modules should be equal or greater than below table")) 							
				
		self.populate_payments_write(cr, uid, ids, id)
		#self.populate_payments_program_write(cr, uid, ids, id)
		#return id
		return id
		
#Image
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		#raise osv.except_osv(_('Warning!'),_('dddddd %s')%(123456))
		return self.pool.get('learner.info').write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		'''obj_write = self.pool.get('learner.info')
		for i in pay_recs:
			vals = {
				'image': i[0],
				'cost': i[1],
				'pay_id': iid
			}
			obj_pay.create(cr, uid, vals)
		
		return True
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)'''

#Learner 11 Tabs Display		
	def views_enroll(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'learner_form')
		view_id = view_ref and view_ref[1] or False
		return {
		'type': 'ir.actions.act_window',
		'name': _('Learner'),
		'res_model': 'learner.info',
		'view_type': 'form',
		'res_id': ids[0], # this will open particular Learner Details,
		'view_id': view_id,
		'view_mode': 'form',
		'nodestroy': True,
		}

#Schedule Tab Info
	def _onchange_populate_schedule(self, cr, uid,  context=None):
		obj = self.pool.get('class.info')
		ids = obj.search(cr, uid, [('parent_id','=',0)])
		res = obj.read(cr, uid, ids, ['start_date'], context)
		res = [(r['start_date'], r['start_date']) for r in res]
		return res
		
	def onchange_populate_schedule2(self, cr, uid, ids, i_centre, i_mod, s_date, context=None):
		#raise osv.except_osv(_('Warning!'),_('Nationality %s %s %s ')%(s_date.id[name]))
		#self.program_select_date(self, cr, uid, ids, i_mod, i_centre)
		val2 ={}
		sub_lines = []
		val2.update({'session_no':''})
		val2.update({'week_no': ''})
		val2.update({'date_schd': ''})
		
		val2.update({'class_name':''})
		val2.update({'class_code':''})
		val2.update({'start_date': ''})
		val2.update({'end_date': ''})	
		val2.update({'sch_date2': ''})
		s_date2 = ''
		#raise osv.except_osv(_('Warning!'),_('Nationality %s ')%(i_mod))
		
		'''if i_mod:
			sql="select module_id from temp_module where id = %s" % (i_mod)
			cr.execute(sql)
			r = cr.fetchall()
			for i in r:
				if i[0]:
					val2.update({'select_module2': i[0]})
					i_mod2=i[0]
		if not i_centre and i_mod: 
			res['value']['i_mod'] = ''
			res.update({'warning': {'title': _('Warning !'), 'message': _('Please Select Center first.')}})	'''
					
		if s_date:
			sql="select name from test_date where id = %s" % (s_date)
			cr.execute(sql)
			r = cr.fetchall()
			for i in r:
				if i[0]:
					val2.update({'sch_date2': i[0]})
					s_date2=i[0]

					
		if i_centre and i_mod and s_date2:
			sql = "select name, class_code, start_date, end_date from class_info where location_id = %s and module_id = %s and start_date = '%s'" % (i_centre,i_mod,s_date2) 
			cr.execute(sql)
			itm = cr.fetchall()
			sub_lines = []
			val2.update({'class_name': ''})
			val2.update({'class_code': ''})
			val2.update({'start_date': ''})
			val2.update({'end_date': ''})
			val2.update({'class_schedule_line': sub_lines})
			for s in itm:
			
				val2.update({'class_name':s[0]})
				val2.update({'class_code': s[1]})
				val2.update({'start_date': s[2]})
				val2.update({'end_date': s[3]})
			
				p_obj = self.pool.get('class.info')
				value_ids = p_obj.search(cr, uid, [('module_id', '=', i_mod)])
				
				#sub_lines.append({'session_no':'', 'week_no':'', 'date_schd':''})
				
				for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
					sub_lines.append({'session_no':prog_line['sess_no'], 'week_no':prog_line['week_no'], 'date_schd':prog_line['start_date']})
					
				val2.update({'class_schedule_line': sub_lines})
			
			return {'value': val2}
		else:
			return {'value': val2}
			
	def onchange_populate_schedule3(self, cr, uid, ids, i_centre, i_mod, context=None):
		#raise osv.except_osv(_('Warning!'),_('Nationality %s %s %s ')%(s_date.id[name]))
		val ={}
		sub_lines = []
		val.update({'session_no':''})
		val.update({'week_no': ''})
		val.update({'date_schd': ''})
		val.update({'sch_date': ''})
		val.update({'sch_date2': ''})
		val.update({'class_name':''})
		val.update({'class_code':''})
		val.update({'start_date': ''})
		val.update({'end_date': ''})
		#val.update({'select_module2': ''})
		val.update({'select_module': ''})
		val.update({'class_schedule_line': sub_lines})
		
		'''if i_centre:
			cr.execute("delete from temp_module")
			sql="insert into temp_module (module_id, name) select distinct c.id, c.name from cs_module c, class_info ci where c.id=ci.module_id and location_id = %s" % (i_centre)
			cr.execute(sql)'''
					
		return  {'value': val}
		
		
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
			
# Negative Value should not accept			
	def _mobile_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.mobile_no < 0:
				return False
		return True

# Negative Value should not accept			
	def _landline_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.landline_no < 0:
				return False
		return True
		
# Negative Value should not accept	
	def _office_no(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.office_no < 0:
				return False
		return True
		
# Negative Value should not accept		
	def _salary_range(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.salary < 0:
				return False
		return True
		
# Validate Email-ID

	def _check_unique_id(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.email_id.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.email_id and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.email_id and self_obj.email_id.lower() in  lst:
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
			
	def _check_unique_learnerfull_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.learnerfull_name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.learnerfull_name and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.learnerfull_name and self_obj.learnerfull_name.lower() in  lst:
				return False
		return True
		
	def _check_unique_learner_nric(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.learner_nric.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.learner_nric and x.id not in ids
			]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.learner_nric and self_obj.learner_nric.lower() in  lst:
				return False
		return True
		
	def learner_move(self, cr, uid, ids, context=None): 
		learner_move_array = []
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		learners = []
		for le_obj in self_obj.class_schedule_line:
			if le_obj.class_info_id == True :
				learner_move_array.append(le_obj.class_info_id.id)
				learners.append(le_obj.id)
			
		if len(learner_move_array) > 0 :
			sub_lines = []
			values = {} 
			sub_lines.append( (0,0, {'learner_id':self_obj['session_no'],'learner_nric':self_obj['week_no']}) )
			values.update({'learner_line': sub_lines})
			learner_obj = self.pool.get("class.info")
		
	def on_change_scheduling(self, cr, uid, ids, toggling):
		val = {}
		val['class_type_schedule'] = False
		val['test_type_schedule'] = False
		if toggling == 'Class Schedule':
			val['class_type_schedule'] = True
		if toggling == 'Test Schedule':
			val['test_type_schedule'] = True
		
		return {'value': val}
		
	'''def default_get(self, cr, uid, fields, context=None):
		data = super(learner_info, self).default_get(cr, uid, fields, context=context)
		data['name']=context.get('active_module')
		return data'''
		
	def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
		if not args:
			args = []
		if context is None:
			context = {}
		ids = []
		name = name + '%'
		cr.execute("SELECT id FROM learner_info WHERE name like %s", (name,))
		ids = cr.dictfetchall()
		return self.name_get(cr, uid, ids, context)
		
	def enroll_learner_program(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'enroll_program')
		view_id = view_ref and view_ref[1] or False
		return {
		'type': 'ir.actions.act_window',
		'name': _('If required add another Program for Learner'),
		'res_model': 'learner.info',
		'view_type': 'form',
		'res_id': ids[0], # this will open particular Learner Details,
		'view_id': view_id,
		'view_mode': 'form',
		'nodestroy': True,
		'target':'new',
		}
		
	def discard_learner_program(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'discard_program')
		view_id = view_ref and view_ref[1] or False
		return {
		'type': 'ir.actions.act_window',
		'name': _('Discard'),
		'res_model': 'discard.program.wizard',
		'view_type': 'form',
		'res_id': 0, # this will open particular Learner Details,
		'view_id': view_id,
		'view_mode': 'form',
		'nodestroy': True,
		'target':'new',
		}
		
	def default_get(self, cr, uid, fields, context=None):
		data = super(learner_info, self).default_get(cr, uid, fields, context=context)
		data['name']=context.get('active_module')
		data['learnerfull_name']=context.get('active_module_full_name')
		data['nationality']=context.get('active_module_nationality')
		data['learner_nric']=context.get('active_module_learner_nric')
		data['learner_non_nric']=context.get('active_module_learner_non_nric')
		data['select_center']=context.get('active_module_select_center')
		data['marital_status']=context.get('active_marital_status')
		data['race']=context.get('active_race')
		data['gender']=context.get('active_gender')
		data['birth_date']=context.get('active_birth_date')
		data['emp_staus']=context.get('active_emp_staus')
		data['company_name']=context.get('active_company_name')
		data['desig_detail']=context.get('active_desig_detail')
		data['salary']=context.get('active_salary')
		data['sponsor_ship']=context.get('active_sponsor_ship')
		data['high_qualification']=context.get('active_high_qualification')
		data['language_proficiency']=context.get('active_language_proficiency')
		data['email_id']=context.get('active_email_id')
		data['addr_1']=context.get('active_addr_1')
		data['addr_2']=context.get('active_addr_2')
		data['postal_code']=context.get('active_postal_code')
		data['mobile_no']=context.get('active_mobile_no')
		data['landline_no']=context.get('active_landline_no')
		data['office_no']=context.get('active_office_no')
		return data
		
	def enroll_views(self,cr,uid,ids,context=None):
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'enroll_form')
		view_id = view_ref and view_ref[1] or False
		ctx = dict(context)
		self_obj  = self.browse(cr, uid, ids[0], context=context)
		
		ctx.update({'learner_id': ids[0],'active_module':self_obj.name,'active_module_full_name':self_obj.learnerfull_name,'active_module_nationality':self_obj.nationality,
			'active_module_learner_nric':self_obj.learner_nric,'active_module_learner_non_nric':self_obj.learner_non_nric,'active_module_select_center':self_obj.select_center.id,
			'active_marital_status':self_obj.marital_status,'active_race':self_obj.race.id,'active_gender':self_obj.gender,'active_birth_date':self_obj.birth_date, 'active_emp_staus':self_obj.emp_staus.id,
			'active_company_name':self_obj.company_name.id, 'active_desig_detail':self_obj.desig_detail.id, 'active_salary':self_obj.salary.id, 'active_sponsor_ship':self_obj.sponsor_ship.id, 'active_high_qualification':self_obj.high_qualification, 
			'active_language_proficiency':self_obj.language_proficiency, 'active_email_id':self_obj.email_id, 'active_addr_1':self_obj.addr_1, 'active_addr_2':self_obj.addr_2, 'active_postal_code':self_obj.postal_code, 
			'active_mobile_no':self_obj.mobile_no, 'active_landline_no':self_obj.landline_no, 'active_office_no':self_obj.office_no})
		
		return {
		'type': 'ir.actions.act_window',
		'name': _('Add Program'),
		'res_model': 'learner.info',
		'view_type': 'form',
		'res_id': 0,
		'view_id': view_id,
		'view_mode': 'form',
		'nodestroy': True,
		'context': ctx,
		#'target':'new',
		}
		
#Table Learner Info
	_name = "learner.info"
	_description = "This table is for keeping location data"
	_columns = {
		'learner_id': fields.char('Id',size=20),
		'name': fields.char('Name', size=100,required=True, select=True),
		'learnerfull_name': fields.char('Name as in NRIC/FIN', size=100,required=True),
		'nationality':fields.selection((('Singapore','Singapore'),('Malaysia','Malaysia'),('South Korea','South Korea'),('North Korea','North Korea'),('India','India'),('Indonesia','Indonesia'),('Vietnam','Vietnam')),'Nationality',required=True),
		'learner_nric': fields.char('NRIC', size=9,  help='Add one Prefix and one Suffix'),
		'learner_non_nric': fields.char('Non-NRIC', size=44,  help='Add one Prefix and one Suffix'),
		'learner_status': fields.selection((('Active','Active'),('InActive','InActive'),('Complete','Complete'),('InComplete','InComplete'),('Blocked','Blocked')),'Status', required=True),
		'learner_status_display_1': fields.function(_learner_status_display_1, readonly=1, type='char'),
		'learner_status_display_2': fields.function(_learner_status_display_2, readonly=1, type='char'),
		'learner_status_display_3': fields.function(_learner_status_display_3, readonly=1, type='char'),
		'date1': fields.date('Date Created', readonly='True'),
		'date2': fields.date('Date Created', readonly='True'),
		'program_learner': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True,required=True),
		'selected_program': fields.many2one('learner.info', 'Selected Programs by Learner', ondelete='cascade', help='Learner', Select=True),
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
		'toggling': fields.selection((('Class Schedule','Class Schedule'),('Test Schedule','Test Schedule')),'Select Schedule'),
		'class_type_schedule': fields.boolean('Class Schedule'),
		'test_type_schedule': fields.boolean('Test Schedule'),
		'select_center':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'class_schedule_line': fields.one2many('class.schedule.module','session_no','Class Schedule'),
		'test_schedule_line': fields.one2many('test.schedule.module','class_info_id','Test Schedule'),
		#'select_module':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
		'select_module':fields.many2one('temp.module', 'Module'),
		'select_module2':fields.integer('Module2'),
		
		'class_name':fields.char('Class Name', readonly=1),
		'class_code':fields.char('Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly=1),
		'end_date':fields.date('End Date', readonly=1),
		#'sch_date':fields.selection((_onchange_populate_schedule), 'Select Date', type='char'),
		'sch_date':fields.many2one('class.start.date', 'Select Date'),
		'sch_date2':fields.char('Select Date2'),
		#payment
		'payment_learner':fields.one2many('payment.module', 'pay_id','Payment Module', readonly=1, type='float'),
		'payment_test_learner':fields.one2many('payment.test', 'pay_id','Payment Test', readonly=1),
		'Grand_total':fields.function(_amount, 'Grand Total', readonly=1),
		'Grand_test_total':fields.function(_amount_test, 'Grand Total', readonly=1),
		'total_amt':fields.function(_total, 'Total', readonly=1),
		#Personal Tab Fields
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
		#Contact
		'email_id': fields.char('Email'),
		'addr_1': fields.char('Address Line 1'),
		'addr_2': fields.char('Address Line 2'),
		'postal_code': fields.char('Postal Code', size=6),
		'mobile_no': fields.integer('Mobile Number', size=9),
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
		'current_class_line': fields.one2many('current.class','class_id','Current Class', readonly=1),
		'class_history_line': fields.one2many('class.history.module','class_id','Class History', readonly=1),
		'test_history_line': fields.one2many('test.history.module', 'test_id', 'Test'),
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
		'salary':fields.many2one('salary.range', 'Salary Range'),
		'sponsor_ship':fields.many2one('sponsership', 'Sponsership'),
		't_status':fields.char('Status'),
		'actual_number':fields.function(_calculate_total_checklist, relation="learner.info",readonly=1,string='No. Checklist',type='integer'),
		'status':fields.char('Status'),
		'apply_all':fields.boolean('Apply to All'),
		'learner_name_id': fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner',type="char"),
	}
	
	_defaults = { 
	   'date1': fields.date.context_today,
	   'date2': fields.date.context_today,
	   'learner_status': 'Active',
	   'learner_nric': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'code'),
	   'nationality': 'Singapore',
	   'learner_id': 'default_learner_nric',
	   'status': 'Draft',
	}
	
	_constraints = [(_mobile_no, 'Error: Mobile Number Cannot be Negative', ['Mobile']), (_landline_no, 'Error: Landline Number Cannot be Negative', ['Landline']), (_office_no, 'Error: Office Number Cannot be Negative', ['Office']), (_check_email, 'Error! Email is invalid.', ['work_email']),(_check_unique_id, 'Error: Email Already Exist', ['Email'])]		
learner_info ()


class learner_profile(osv.osv):

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
		
		
# Payment Module Function for Grand Total
	#_inherit = "payment.module"
	def _amount(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_learner:
				total += line.cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
# Payment Test Function for Grand Total
	#_inherit = "payment.module"
	def _amount_test(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_test_learner:
				total += line.test_cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
	def _calculate_total_checklist(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = line.checklist_tab or []
			_logger.info("total id %s",mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
		return res
		
	def _amount(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_learner:
				total += line.cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
# Payment Test Function for Grand Total
	#_inherit = "payment.module"
	def _amount_test(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_test_learner:
				total += line.test_cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
	def _total(self, cr, uid, ids, field_names, args, context=None):
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line.Grand_total + line.Grand_test_total
			
		return res
		
	def copy(self, cr, uid, id, default=None, context=None):
		raise osv.except_osv(_('Forbbiden to duplicate'), _('Is not possible to duplicate the record, please create a new one.'))
		
#Table Learner Info
	_name = "learner.profile"
	_description = "This table is for keeping location data"
	_columns = {
		'learner_id': fields.char('Id',size=20),
		#'name': fields.many2one('learner.name', 'Name', required=True, size=100, type='char'),
		#'learnerfull_name': fields.many2one('learner.name.nric', 'Name as in NRIC/FIN', required=True, size=100),
		#'learner_nric': fields.many2one('learner.nric', 'NRIC', size=7,required=True, help='Add one Prefix and one Suffix'),
		'name': fields.char('Name', size=100,required=True, select=True),
		'learnerfull_name': fields.char('Name as in NRIC/FIN', size=100,required=True),
		'nationality':fields.selection((('Singapore','Singapore'),('Malaysia','Malaysia'),('South Korea','South Korea'),('North Korea','North Korea'),('India','India'),('Indonesia','Indonesia'),('Vietnam','Vietnam')),'Nationality',required=True),
		'learner_nric': fields.char('NRIC', size=9,  help='Add one Prefix and one Suffix'),
		'learner_non_nric': fields.char('Non-NRIC', size=44,  help='Add one Prefix and one Suffix'),
		'learner_status': fields.selection((('Active','Active'),('InActive','InActive'),('Complete','Complete'),('InComplete','InComplete'),('Blocked','Blocked')),'Status', required=True),
		'learner_status_display_1': fields.function(_learner_status_display_1, readonly=1, type='char'),
		'learner_status_display_2': fields.function(_learner_status_display_2, readonly=1, type='char'),
		'learner_status_display_3': fields.function(_learner_status_display_3, readonly=1, type='char'),
		'date1': fields.date('Date Created', readonly='True'),
		'date2': fields.date('Date Created', readonly='True'),
		'program_learner': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True,required=True),
		'selected_program': fields.many2one('learner.info', 'Selected Programs by Learner', ondelete='cascade', help='Learner', Select=True),
		'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True, store=True),
		#checklist Tab
		'checklist_tab': fields.one2many('checklist.module','checklist_id','checklist'),
		#Schedule Tab
		'toggling': fields.selection((('Class Schedule','Class Schedule'),('Test Schedule','Test Schedule')),'Select Schedule'),
		'class_type_schedule': fields.boolean('Class Schedule'),
		'test_type_schedule': fields.boolean('Test Schedule'),
		'select_center':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'class_schedule_line': fields.one2many('class.schedule.module','session_no','Class Schedule'),
		'test_schedule_line': fields.one2many('test.schedule.module','class_info_id','Test Schedule'),
		#'select_module':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', select=True),
		'select_module':fields.many2one('temp.module', 'Module'),
		'select_module2':fields.integer('Module2'),
		
		'class_name':fields.char('Class Name', readonly=1),
		'class_code':fields.char('Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly=1),
		'end_date':fields.date('End Date', readonly=1),
		#'sch_date':fields.selection((_onchange_populate_schedule), 'Select Date', type='char'),
		'sch_date':fields.many2one('class.start.date', 'Select Date'),
		'sch_date2':fields.char('Select Date2'),
		#payment
		'payment_learner':fields.one2many('payment.module', 'pay_id','Payment Module', readonly=1, type='float'),
		'payment_test_learner':fields.one2many('payment.test', 'pay_id','Payment Test', readonly=1),
		'Grand_total':fields.function(_amount, 'Grand Total', readonly=1),
		'Grand_test_total':fields.function(_amount_test, 'Grand Total', readonly=1),
		'total_amt':fields.function(_total, 'Total', readonly=1),
		#Personal Tab Fields
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
		#Contact
		'email_id': fields.char('Email'),
		'addr_1': fields.char('Address Line 1'),
		'addr_2': fields.char('Address Line 2'),
		'postal_code': fields.char('Postal Code', size=6),
		'mobile_no': fields.integer('Mobile Number', size=9),
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
		'current_class_line': fields.one2many('current.class','class_id','Current Class', readonly=1),
		'class_history_line': fields.one2many('class.history.module','class_id','Class History', readonly=1),
		'test_history_line': fields.one2many('test.history.module', 'test_id', 'Test'),
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
		'salary':fields.many2one('salary.range', 'Salary Range'),
		'sponsor_ship':fields.many2one('sponsership', 'Sponsership'),
		't_status':fields.char('Status'),
		'actual_number':fields.function(_calculate_total_checklist, relation="learner.info",readonly=1,string='No. Checklist',type='integer'),
		'status':fields.char('Status'),
		'apply_all':fields.boolean('Apply to All'),
	}
	
	_defaults = { 
	   'date1': fields.date.context_today,
	   'date2': fields.date.context_today,
	   'learner_status': 'Active',
	   'learner_nric': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'code'),
	   'nationality': 'Singapore',
	   'learner_id': 'default_learner_nric',
	   'status': 'Draft',
	}
	
	#_constraints = [(_mobile_no, 'Error: Mobile Number Cannot be Negative', ['Mobile']), (_landline_no, 'Error: Landline Number Cannot be Negative', ['Landline']), (_office_no, 'Error: Office Number Cannot be Negative', ['Office']), (_check_email, 'Error! Email is invalid.', ['work_email']),(_check_unique_id, 'Error: Email Already Exist', ['Email'])]

learner_profile()

class learner_name(osv.osv):
	def _check_learner_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='learner.name'
	_description ="Learner Name"
	_columns = {
	'name':fields.char('Learner Name'),
	}
	_constraints = [(_check_learner_name, 'Error: Learner Already Exists', ['Learner'])]
learner_name()

class learner_name_nric(osv.osv):
	def _check_learner_name(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='learner.name.nric'
	_description ="Learner Nric"
	_columns = {
	'name':fields.char('Learner Name'),
	}
	_constraints = [(_check_learner_name, 'Error: Learner Already Exists', ['Learner'])]
learner_name_nric()

class learner_nric(osv.osv):
	def _check_learner_nric(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='learner.nric'
	_description ="Learner NRIC"
	_columns = {
	'name':fields.char('Learner NRIC'),
	}
	_constraints = [(_check_learner_nric, 'Error: Learner NRIC Already Exists', ['Learner'])]
learner_nric()

class test_date(osv.osv):
	
	_name = "test.date"
	_description = "Test date"
	_columns = {
	'name' : fields.datetime('Start Date', readonly='True')
	}	
test_date()

class temp_module(osv.osv):
	
	_name = "temp.module"
	_description = "Test date"
	_columns = {
	'name' : fields.char('Module', readonly='True'),
	'module_id' : fields.integer('Module', readonly='True'),
	'date' : fields.datetime('Module', readonly='True'),
	}	
temp_module()

class class_start_date(osv.osv):
	
	_name = "class.start.date"
	_description = "Test date"
	_columns = {
	'name' : fields.datetime('Start Date', readonly='True')
	}	
class_start_date()

#Class Program Module Line
###############
globvar = 0
class program_mod_line(osv.osv):

	def check_box_value(self, cr, uid, ids, iId, abc, context=None):

		val = {}
		sql="select name from cs_module where id = ('%s') " % (iId)
		cr.execute(sql)
		modName = cr.fetchall()
		for i in modName:
			idd = i[0]
		
		if abc == False:
			cr.execute("delete from temp_module where module_id = %s " % (iId))
		if abc == True:
			cr.execute("delete from temp_module where module_id = %s " % (iId))
			sql="insert into temp_module (module_id,name) values (%s,'%s') " % (iId,idd)
			r = cr.execute(sql)
		return True
		return True
		
	def onchange_populate_schedule2(self, cr, uid, ids, i_centre, i_mod, s_date, context=None):
		val2 ={}
		sub_lines = []			
		if s_date:
			sql="select name from cs_module where module_id = %s" % (s_date)
			cr.execute(sql)
			r = cr.fetchall()
			for i in r:
				if i[0]:
					val2.update({'sch_date2': i[0]})
					s_date2=i[0]

					
		if i_centre and i_mod and s_date2:
			sql = "select name, class_code, start_date, end_date from class_info where location_id = %s and module_id = %s and start_date = '%s'" % (i_centre,i_mod,s_date2) 
			cr.execute(sql)
			itm = cr.fetchall()
			sub_lines = []
			val2.update({'class_name': ''})
			val2.update({'class_code': ''})
			val2.update({'start_date': ''})
			val2.update({'end_date': ''})
			val2.update({'class_schedule_line': sub_lines})
			for s in itm:
			
				val2.update({'class_name': s[0]})
				val2.update({'class_code': s[1]})
				val2.update({'start_date': s[2]})
				val2.update({'end_date': s[3]})
			
				p_obj = self.pool.get('class.info')
				value_ids = p_obj.search(cr, uid, [('module_id', '=', i_mod)])
				
				#sub_lines.append({'session_no':'', 'week_no':'', 'date_schd':''})
				
				for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
					sub_lines.append({'session_no':prog_line['sess_no'], 'week_no':prog_line['week_no'], 'date_schd':prog_line['start_date']})
					
				val2.update({'class_schedule_line': sub_lines})
			
			return {'value': val2}
		else:
			return {'value': val2}
			
	def on_change_payment_moule(self, cr, uid, ids, module_id) :
		i= {}
		mod_obj = self.pool.get('cs.module').search(cr, uid, [('id', '=', module_id)])
		for value_ids in self.pool.get('cs.module').browse(cr, uid, mod_obj):
			i[0] =  value_ids['module_fee']
		
		obj_pay = self.pool.get('payment.module')
		sql="delete from payment_module where pay_id = %s " % (module_id)
		cr.execute (sql)
		vals = {'pay_id': ids,'s_no': 0,'item_name': module_id,'cost': i[0], 'program_name': program_learner}
		obj_pay.create(cr, uid, vals)

	def views(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('learner.mode.line')
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
		
	def views2(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('learner.mode.line')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['module_id_2'].id)
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
		
	def views3(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('learner.mode.line')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['module_id_3'].id)
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
		
	def views4(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('learner.mode.line')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['module_id_4'].id)
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
		
	def views5(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('learner.mode.line')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['module_id_5'].id)
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
		
	def views5(self,cr,uid,ids,context=None):
		global globvar
		globvar = 1
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'module_form')
		view_id = view_ref and view_ref[1] or False
		prog_mod_obj = self.pool.get('learner.mode.line')
		prog_mod_ids = prog_mod_obj.search(cr, uid, [('id', '=', ids[0])])
		module_ids =[]
		for prog_module_line in prog_mod_obj.browse(cr, uid, prog_mod_ids,context=context):
			module_ids.append(prog_module_line['module_id_6'].id)
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

	_name = "learner.mode.line"
	_description = "Module Line"
	_columns = {
		'qualification_module_id': fields.many2one('learner.info', ondelete='cascade'),
	#1
		'prog_mod_id': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', readonly=1),
		'qualification_module_id_1': fields.many2one('learner.info'),
		'name': fields.related('qualification_module_id', 'name', relation='learner.info', readonly=1),
		'module_id':fields.many2one('cs.module', 'Module', ondelete='cascade', help='Module', readonly=1),
		'check_module_select_1': fields.boolean('Selectable'),
		'select_mod_1': fields.boolean('Select', select=True, store=True),
		'class_start_date_1':fields.many2one('class.info', 'Class Start Date', ondelete='cascade', help='Class Calendar', readonly=1),
	#2
		'prog_mod_id_2': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', readonly=1),
		'qualification_module_id_2': fields.many2one('learner.info'),
		'name': fields.related('qualification_module_id', 'name', relation='learner.info', readonly=1),
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
		's_no' : fields.integer('S.No',size=50, readonly=1),
		'item':fields.many2one('master.show.do', 'Item', ondelete='cascade', readonly=1),
		'subsidy_fee': fields.integer('% Of Module Fee', ondelete='cascade', readonly=1),
		'confirmation':fields.boolean('Confirmation'),
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

#Class Schedules
###############
class class_schedule(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(class_schedule, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['session_no'] = seq_number
		
		return res
		
	def update_status(self,cr, uid, ids, values, context=None):
		super(class_schedule, self).write(cr, uid, ids,values, context=context)

	_name ='class.schedule.module'
	_description ="Class Schedule Tab"
	_columns = {
		'learner_id':fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner', select=True),
		'class_info_id':fields.many2one('class.info', 'Learner', ondelete='cascade', help='Learner', select=True),
		'session_no' : fields.integer('Session No', size=10, readonly=1),
		'week_no' : fields.integer('Week No', size=20, readonly=1),
		'date_schd': fields.date('Date', readonly='True'),
		't_status':fields.char('Status'),
	}
class_schedule ()

#Test Schedules
###############
class test_schedule(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(test_schedule, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['test_name'] = seq_number
		
		return res

	_name ='test.schedule.module'
	_description ="Test schedule Tab"
	_columns = {
		'learner_id':fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner', select=True),
		'class_info_id':fields.many2one('class.info', 'Learner', ondelete='cascade', help='Learner', select=True),
		'test_name' : fields.char('Test Name', size=10, readonly=1),
		'test_code' : fields.char('Test Code', size=20, readonly=1),
		'start_date': fields.datetime('Start Date', readonly='True'),
		'end_date': fields.datetime('End Date', readonly='True'),
	}
test_schedule ()

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

class salary_range(osv.osv):
	def _check_salary_range(self, cr, uid, ids, context=None):
		sr_ids = self.search(cr, 1 ,[], context=context)
		lst = [
				x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context)
				if x.name and x.id not in ids
				]
		for self_obj in self.browse(cr, uid, ids, context=context):
			if self_obj.name and self_obj.name.lower() in  lst:
				return False
		return True
	_name ='salary.range'
	_description ="Salary Range"
	_columns = {
	'name':fields.char('Salary Range'),
	}
	_constraints = [(_check_salary_range, 'Error: Designation Status Already Exists', ['Designation'])]
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
	'''def _percentage_cal(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line.cost / 100.00
		return res'''
		
	def _percentage_cal(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line.cost + 1.07
		return res

	_name ='payment.module'
	_description ="payment Tab"
	_columns = {
		'pay_id':fields.many2one('learner.info','Id'),
		's_no' : fields.integer('S.No', size=50, readonly=1),
		'program_name': fields.many2one('lis.program', 'Program Name'),
		'item_name' : fields.many2one('cs.module', 'Module Name'),
		'cost': fields.float('Module Cost', size=9),
		'payment_required': fields.function(_percentage_cal, string='Payment Req (include 7% GST)', size=6, type='float',obj="payment.module",method=True,),
	}
payment ()

# With 5 tab Payment (Learner info)
class payment_test(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(payment_test, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res
		
	def _percentage_cal(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line.test_cost + 1.07
		return res
		
	_name ='payment.test'
	_description ="Payment Test Tab"
	_columns = {
		'pay_id':fields.many2one('learner.info','Learner', ondelete='cascade'),
		's_no' : fields.integer('S.No', size=50, readonly=1),
		'program_name': fields.many2one('lis.program','Program', 'program_learner', ondelete='cascade', help='Program', select=True),
		'module_name' : fields.char('Module Name'),
		'test_name' : fields.char('Test Code'),
		'test_cost': fields.float('Test Cost', size =9),
		'payment_required': fields.function(_percentage_cal, string='Payment Req (include 7% GST)', size=6, type='float',obj="payment.test",method=True,),
	}
payment_test ()

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

#Current Class
class current_class(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(current_class, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	_name = "current.class"
	_description = "Currents Class Details"
	_columns = {
		'class_id' : fields.many2one('learner.info', ondelete='cascade'),
		'class_iid': fields.many2one('class.info', ondelete='cascade'),
		's_no' : fields.integer('S.No',size=20,readonly=1),
		'program_name': fields.many2one('lis.program','Program', 'program_learner', ondelete='cascade', help='Program', select=True),
		'module_name':fields.many2one('cs.module', 'Module', ondelete='cascade'),
		'class_code':fields.char('Class Code'),
		'start_date': fields.date('Start Date'),
		'end_date': fields.date('End Date'),
		'session_timings': fields.char('Session Timings', size=20),
		'class_status': fields.char('Class Status'),
		'attendance': fields.integer('Attendance'),
		'no_of_sessions': fields.integer('No of Sessions', size=3),
		'class_schedule_paltform': fields.char('Class Schedule Pattern'),
	}
	
	def on_change_prog_name(self, cr, uid, ids, program_name):
		module_obj = self.pool.get('lis.program').browse(cr, uid, program_name)
		return {'value': {'program_name': module_obj.program_name}}	
		
current_class()
	
#Learner Class History Tab
class class_history(osv.osv):

	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		
		res = super(class_history, self).read(cr, uid,ids, fields, context, load)
		seq_number =0 
		for r in res:
			seq_number = seq_number+1
			r['s_no'] = seq_number
		
		return res

	_name = "class.history.module"
	_description = "Class History Tab"
	_columns = {
	'class_id' : fields.many2one('learner.info', ondelete='cascade'), 
	's_no' : fields.integer('S.No',size=20,readonly=1),
	'action': fields.char('Action'),
	'program_name': fields.many2one('lis.program','Program', 'program_learner', ondelete='cascade', help='Program', select=True),
	'module_name':fields.many2one('cs.module', 'Module', ondelete='cascade'),
	'class_code':fields.char('Class Code'),
	'start_date': fields.datetime('Date Commenced'),
	'action_by': fields.char('Action By'),
	'additional_info': fields.char('Additional Info'),
	'emp_staus': fields.many2one('employee.status', 'Employee Status'),
	'sponsor_ship':fields.many2one('sponsership', 'Sponsership'),
	}
	
	def on_change_prog_name(self, cr, uid, ids, program_name):
		module_obj = self.pool.get('lis.program').browse(cr, uid, program_name)
		return {'value': {'program_name': module_obj.program_name}}	

class_history()

#Learner Test History Tab
class test_history(osv.osv):
	_name = "test.history.module"
	_description = "Test History Tab"
	_columns = {
	'test_id' : fields.many2one('learner.info', 'Learner', ondelete='cascade'), 
	#'test_type' : fields.many2one('test','Test', ondelete='cascade'),
	'test_code' : fields.char('Test Code',),
	'test_date' : fields.date('Test Date'),
	'test_status' : fields.char('Test Status'),
	
	}	
test_history()

#Learner Test Scores Tab
class test_score(osv.osv):
	_name = "test.score.module"
	_description = "Test Score Tab"
	_columns = {
	'test_score_id' : fields.many2one('learner.info', 'Learner', ondelete='cascade'), 
	'test_score_type' : fields.many2one('test','Test', ondelete='cascade'),
	'test_sc_code' : fields.char('Test Code',),
	'test_sc_date' : fields.date('Test Date'),
	'test_compre' : fields.integer('Compr',),
	'test_conv' : fields.integer('Conv',),
	'r_level' : fields.integer('R(Level)',),
	'r_score' : fields.integer('R(Score)',),
	'l_level' : fields.integer('L(Level)'),
	'l_score' : fields.integer('L(Score)'),
	's_level' : fields.integer('S(Level)'),
	's_score' : fields.integer('S(Score)'),
	'w_level' : fields.integer('W(Level)'),
	'w_score' : fields.integer('W(Score)'),
	'w_outcomes' : fields.integer('W(Outcomes)'),
	'n_level' : fields.integer('N(Level)'),
	'n_score' : fields.integer('N(Score)'),
	'w_outcome1' : fields.integer('W(Outcomes)'),
	
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

	def _current_user(self, cr, uid, ids, context=None):
		return uid
		
	def months_between(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
	   
# Zeya 9-1-15	   
	   
	def onchange_issuedate(self, cr, uid, ids, issue, context=None):
			if issue:
				d = self.months_between(issue, str(datetime.datetime.now().date())) 
				res = {'value':{}}
				#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(d))
				if d > 0:
					res['value']['date_of_feedback'] = ''
					#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
					res.update({'warning': {'title': _('Warning !'), 'message': _('Please Check the Date, Past Date not Allowed.')}})
					return res
				return issue
		
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
		
	def months_between(self, date1, date2):
		date11 = datetime.datetime.strptime(date1, '%Y-%m-%d')
		date12 = datetime.datetime.strptime(date2, '%Y-%m-%d')
		r = relativedelta.relativedelta(date12, date11)
		return r.days
	   
# Zeya 9-1-15	   
	   
	def onchange_issuedateone(self, cr, uid, ids, issue, context=None):
			if issue:
				d = self.months_between(issue, str(datetime.datetime.now().date())) 
				res = {'value':{}}
				#raise osv.except_osv(_('Warning!'),_('Nationality %s')%(d))
				if d > 0:
					res['value']['date_of_remarks'] = ''
					#res['warning'][''] = {'title':'Error', 'messagge':'Insert 10 chars!'}
					res.update({'warning': {'title': _('Warning !'), 'message': _('Please Check the Date, Past Date not Allowed.')}})
					return res
				return issue
		
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

class enroll_program_wizard(osv.osv):

	_name = 'enroll.program.wizard'
	_description = 'Enroll Program Wizard'
	_columns = { 
		'name': fields.char('Name', size=100,required=True, select=True),
		#'learner_id':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, readonly=1),
	}
	
enroll_program_wizard()

class discard_program_wizard(osv.osv):

	def enroll_views(self,cr,uid,ids,context=None):
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'cornerstone', 'add_program')
		view_id = view_ref and view_ref[1] or False
		#ctx = dict(context)
		#self_obj  = self.browse(cr, uid, ids[0], context=context)
		
		#ctx.update({'discard_id': ids[0],'active_module':self_obj.learner_name.id})
		
		return {
		'type': 'ir.actions.act_window',
		'name': _('Add Program'),
		'res_model': 'add.program',
		'view_type': 'form',
		'res_id': 0,
		'view_id': view_id,
		'view_mode': 'form',
		'nodestroy': True,
		#'context': ctx,
		#'target':'new',
		}

	_name = 'discard.program.wizard'
	_description = 'Discard Program Wizard'
	_columns = { 
		'discard_id': fields.integer('Discard'),
		'name': fields.char('Name', size=100, select=True),
		'learner_name': fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner',type="char"),
	}
	
discard_program_wizard()

class add_program(osv.osv):

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
		

#Checklist Items				
		#val ={}		
		p_obj = self.pool.get('program.show.do.module')
		value_ids = p_obj.search(cr, uid, [('program_id', '=', progid)])
		#val ={}
		sub_lines = []
		for prog_line in p_obj.browse(cr, uid, value_ids,context=context):
			sub_lines.append({'item':prog_line['master_show_do'].id})
		val.update({'checklist_tab': sub_lines})
		
# Payment Program to fetch the detailed Programs
		learner_id = 0
		for self_obj in self.browse(cr, uid, ids, context=context):
			learner_id = self_obj.id

		sql="select program_learner from learner_info where id = %s " % (learner_id)
		cr.execute(sql)
		pay_recs = cr.fetchall()
		
		sub_lines = []
		for i in pay_recs:
			sub_lines.append({'program_name':i[0]})
			
		val.update({'payment_learner': sub_lines})
		return {'value': val}

# Payment Module to fetch the detailed Modules
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
		
		
# Payment Module Function for Grand Total
	#_inherit = "payment.module"
	def _amount(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_learner:
				total += line.cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
# Payment Test Function for Grand Total
	#_inherit = "payment.module"
	def _amount_test(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_test_learner:
				total += line.test_cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
	def _calculate_total_checklist(self, cr, uid, ids, field_names, args,  context=None):
		if not ids: return {}
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			mod_line_ids = line.checklist_tab or []
			_logger.info("total id %s",mod_line_ids)
			total_mod = len(mod_line_ids)
			res[line.id] = total_mod
		return res
		
	def _amount(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_learner:
				total += line.cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
# Payment Test Function for Grand Total
	#_inherit = "payment.module"
	def _amount_test(self, cr, uid, ids, field_name, arg, context=None):
		res= {}
		for claim in self.browse(cr, uid, ids, context=context):
			total = 0.0
			for line in claim.payment_test_learner:
				total += line.test_cost#line.unit_amount * line.unit_quantity
			res[claim.id] = total
		return res
		
	def _total(self, cr, uid, ids, field_names, args, context=None):
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = line.Grand_total + line.Grand_test_total
			
		return res

	def default_get(self, cr, uid, fields, context=None):
		data = super(add_program, self).default_get(cr, uid, fields, context=context)
		data['learner_name']=context.get('active_module')
		return data
	
	_name = 'add.program'
	_description = 'Add Program'
	_columns = { 
		'learner_id': fields.many2one('learner.info', 'Learner', ondelete='cascade', help='Learner',type="char"),
		'learner_name': fields.char('Learner'),
		'program_learner': fields.many2one('lis.program', 'Program', ondelete='cascade', help='Program', select=True,required=True),
		'module_id':fields.many2one('cs.module', 'Module Name', ondelete='cascade', help='Module', select=True, store=True),
		#Check-list Tab
		'checklist_tab': fields.one2many('checklist.module','checklist_id','checklist'),
		#Schedule Tab
		'toggling': fields.selection((('Class Schedule','Class Schedule'),('Test Schedule','Test Schedule')),'Select Schedule'),
		'class_type_schedule': fields.boolean('Class Schedule'),
		'test_type_schedule': fields.boolean('Test Schedule'),
		'select_center':fields.many2one('location', 'Location', ondelete='cascade', help='Location', select=True, required=True),
		'class_schedule_line': fields.one2many('class.schedule.module','session_no','Class Schedule'),
		'test_schedule_line': fields.one2many('test.schedule.module','class_info_id','Test Schedule'),
		'select_module':fields.many2one('temp.module', 'Module'),
		'select_module2':fields.integer('Module2'),
		'class_name':fields.char('Class Name', readonly=1),
		'class_code':fields.char('Class Code', readonly=1),
		'start_date':fields.date('Start Date', readonly=1),
		'end_date':fields.date('End Date', readonly=1),
		'sch_date':fields.many2one('class.start.date', 'Select Date'),
		'sch_date2':fields.char('Select Date2'),
		#payment
		'payment_learner':fields.one2many('payment.module', 'pay_id','Payment Module', readonly=1, type='float'),
		'payment_test_learner':fields.one2many('payment.test', 'pay_id','Payment Test', readonly=1),
		'Grand_total':fields.function(_amount, 'Grand Total', readonly=1),
		'Grand_test_total':fields.function(_amount_test, 'Grand Total', readonly=1),
		'total_amt':fields.function(_total, 'Total', readonly=1),
		#Modules Tab
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
		't_status':fields.char('Status'),
		'actual_number':fields.function(_calculate_total_checklist, relation="learner.info",readonly=1,string='No. Checklist',type='integer'),
		'status':fields.char('Status'),
		'apply_all':fields.boolean('Apply to All'),
	}
	
add_program()




	
