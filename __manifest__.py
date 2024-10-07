# -*- coding: utf-8 -*-
{
    'name': "Custom Payroll Upload",
    'summary': """
       Custom module for uploading payroll amounts for salary tags.""",
    'description': """
        This module allows the uploading of payroll amounts for each salary tag, 
        simplifying the payroll processing by dynamically updating salaries for employees.
        
        Key Features:
        - Upload payroll amounts for specific salary tags
        - Integration with the Odoo HR Payroll system
        - Streamlined management of salary uploads
    """,
    'author': "Dynamic Solution Maker (DSM)",
    'website': "http://www.dsmpk.com",
    'category': 'Human Resources',
    'version': '0.1',

    'depends': ['base', 'hr_payroll', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/template_view.xml'
    ],
}
