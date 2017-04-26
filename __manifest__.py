# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'AllPlastics Engineering PTY LTD',
    'version': '1.0',
    'website': 'http://www.sdsoftware.in',
    'sequence': 1,
    'summary': 'Customsing and adding new features for AllPlastics',
    'depends': ['sale', 'procurement', 'mrp'],
    # 'l10n_au'
    'description': """    """,
    'data': [
        'views/account_view.xml',
 	    'views/sale_view.xml',
 	    'views/mrp_view.xml',
        'report/paper_format.xml',
        'report/report_view.xml',
        'report/report_saleorder_new.xml',
        'report/report_job_sheet.xml',
        'report/report_invoice.xml',
    ],
    'demo': [ ],
    'qweb': [ ],
    'test': [ ],
    'application': True,
}
