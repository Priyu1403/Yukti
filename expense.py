from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ExpenseRecord(models.Model):
    _name = 'expense.record'
    _description = 'Expense Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    category = fields.Selection([
        ('travel', 'Travel'),
        ('meals', 'Meals'),
        ('stationery', 'Stationery'),
        ('accommodation', 'Accommodation'),
        ('other', 'Other'),
    ], string='Category', required=True, tracking=True)
    amount = fields.Float(string='Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    receipt = fields.Binary(string='Receipt')
    receipt_name = fields.Char(string='Receipt Filename')
    description = fields.Text(string='Description')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('manager_approved', 'Manager Approved'),
        ('finance_approved', 'Finance Approved'),
        ('reimbursed', 'Reimbursed'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)

    manager_id = fields.Many2one('hr.employee', string='Approving Manager')
    finance_id = fields.Many2one('res.users', string='Finance Approver')
    journal_entry_id = fields.Many2one('account.move', string='Journal Entry')

    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('expense.record') or _('New')
            vals['name'] = vals.get('name') or vals['sequence']
        return super().create(vals)

    def action_submit(self):
        for rec in self:
            if rec.amount <= 0:
                raise UserError(_('Amount must be positive.'))
            rec.state = 'submitted'
            rec.message_post(body=_('Expense submitted for approval'))

    def action_manager_approve(self):
        for rec in self:
            rec.state = 'manager_approved'
            rec.message_post(body=_('Manager approved this expense'))

    def action_finance_approve(self):
        for rec in self:
            rec.state = 'finance_approved'
            rec.message_post(body=_('Finance approved this expense'))

    def action_reimburse(self):
        for rec in self:
            rec.state = 'reimbursed'
            rec.message_post(body=_('Expense reimbursed'))

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'
            rec.message_post(body=_('Expense rejected'))
