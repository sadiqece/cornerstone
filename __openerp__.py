{
"name" : "cornerstone",
"version" : "0.1",
"author" : "ASZ Technologies",
"website" : "http://asztechnologies.com/",
"category" : "General",
"depends" : ["base"],
"description" : "Simple demo module",
"init_xml" : [],
"demo_xml" : [],
'data' : [
        'cornerstone_view.xml',
        'location_view.xml',
		'security/cornerstone_security.xml',
        'security/ir.model.access.csv',
		'report/cornerstone_report_view.xml',
		'wizard/add_program_wizard.xml',
		'test_view.xml',
		'asset_view.xml',
		'holiday_closure_view.xml',
		'business_structure_view.xml',
		'commisions_view.xml',
		'class_info_view.xml',
		'test_scheduling_view.xml',
		'learner_view.xml',
		'class_status_dashboard.xml',
		'trainer_enrollment.xml',
		'client_enrollment.xml',
		'user_profile_view.xml',
		'reports_view.xml',
		'payment_report.xml',
    ],
'js': [
        'static/src/js/form.js',
		'static/src/js/accordian.js',
    ],
"active": False,
"installable": True
}