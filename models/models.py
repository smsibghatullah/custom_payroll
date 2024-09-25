from odoo import models, fields, api

class HrSalaryUpload(models.Model):
    _name = 'hr.salary.upload'
    _description = 'Monthly Salary Upload'

    # name = fields.Char(string="Employee Name", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)

    month = fields.Selection(
        [('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), 
         ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), 
         ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        string="Month", required=True
    )
    year = fields.Char(string="Year", required=True)
    
    base_salary = fields.Float(string="Base Salary")
    non_taxable_income = fields.Float(string="Non-taxable Income")
    sick_pay = fields.Float(string="Sick Pay")
    bonus = fields.Float(string="Bonus")
    vacation_pay = fields.Float(string="Vacation Pay")
    additional_leave_pay = fields.Float(string="Additional Leave Pay")
    total_gross_salary = fields.Float(string="Total Gross Salary", compute="_compute_total_gross_salary")
    tax_relief = fields.Float(string="Tax Relief")
    deductions = fields.Float(string="Deductions")
    employee_social_contributions = fields.Float(string="Employee Social Insurance Contributions")
    employer_social_contributions = fields.Float(string="Employer Social Insurance Contributions")
    income_tax = fields.Float(string="Income Tax")
    advance_payments = fields.Float(string="Advance Payments/Garnishments")
    net_salary = fields.Float(string="Net Salary", compute="_compute_net_salary")
    occupation_code = fields.Char(string="Occupation Code111")
    
    @api.depends('base_salary', 'non_taxable_income', 'sick_pay', 'bonus', 'vacation_pay', 'additional_leave_pay')
    def _compute_total_gross_salary(self):
        for record in self:
            record.total_gross_salary = (record.base_salary + record.non_taxable_income + record.sick_pay +
                                         record.bonus + record.vacation_pay + record.additional_leave_pay)
    
    @api.depends('total_gross_salary', 'tax_relief', 'deductions', 'employee_social_contributions', 'income_tax')
    def _compute_net_salary(self):
        for record in self:
            record.net_salary = (record.total_gross_salary - record.deductions - 
                                 record.employee_social_contributions - record.income_tax)





class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


    @api.multi
    def compute_sheet(self):
        # Call the original method to compute the payslip
        super(HrPayslip, self).compute_sheet()

        # After calling the original method, you can apply your custom logic
        for payslip in self:
            salary_upload = self.env['hr.salary.upload'].search([('employee_id', '=', payslip.employee_id.id)], order='id desc',  limit=1)
            # Access the salary rules
            for line in payslip.line_ids:
                if line.salary_rule_id.code == 'SICK':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.sick_pay
                if line.salary_rule_id.code == 'BASIC':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.base_salary
                if line.salary_rule_id.code == 'NONTAXINC':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.non_taxable_income 
                if line.salary_rule_id.code == 'BONUS':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.bonus
                if line.salary_rule_id.code == 'VACPAY':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.vacation_pay  
                if line.salary_rule_id.code == 'ADDLEAVE':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.additional_leave_pay  
                if line.salary_rule_id.code == 'GROSS':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.total_gross_salary
                if line.salary_rule_id.code == 'TAXRELIEF':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.tax_relief 
                if line.salary_rule_id.code == 'DEDUCT':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.deductions
                if line.salary_rule_id.code == 'EMP_SOC':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.employee_social_contributions
                if line.salary_rule_id.code == 'EMPLOYER_SOC':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.employee_social_contributions
                if line.salary_rule_id.code == 'TAX':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.income_tax
                if line.salary_rule_id.code == 'ADVANCE':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.advance_payments
                if line.salary_rule_id.code == 'NET':
                    # Fetch the custom value from hr.salary.upload
                    if salary_upload:
                        line.amount = salary_upload.net_salary
                         
    
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    external_id = fields.Char(string='External ID', readonly=True, compute='_compute_external_id')

    def _compute_external_id(self):
       for record in self:
            external_id_record = self.env['ir.model.data'].search([
                ('model', '=', 'hr.employee'),
                ('res_id', '=', record.id)
            ], limit=1)  
            record.external_id = external_id_record.name if external_id_record else False
