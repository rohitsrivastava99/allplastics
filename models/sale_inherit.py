# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Company(models.Model):
    _inherit = 'res.company' 

    term_one = fields.Text('Terms And Conditon', default="This Quote is based upon information supplied at the time of quotation any design changes or additional information supplied after this quote is submitted will requires re-quotation")
    term_two = fields.Text('Notes.', default="Payment by visa or mastercard incurrs a processing fee of 1.5%  (incl GST) and and Amex Card incurs a processing fee of 4%(Incl. GST) of the total invoice amount. " )
   

class SaleOrderline(models.Model):
    _inherit = 'sale.order.line'

    drawing = fields.Char('Drawing No')
    # drawing_attach = fields.Binary('Attachment')

class SaleOrder(models.Model):
    _inherit = 'sale.order'    

    @api.model
    def _default_terms_one(self):
        return self.env.user.company_id.term_one

    @api.model
    def _default_terms_two(self):
        return self.env.user.company_id.term_two



    production_id = fields.Many2one('mrp.production', string="Manfacturing")
    quote_valid = fields.Selection([(num, num) for num in range(0, 32)], 'Quote Valid')
    lead_time = fields.Selection([(num, num) for num in range(0, 32)], 'Lead Time')
    freight = fields.Boolean('Freight')
    term_one = fields.Text('Terms And Conditon', default=_default_terms_one)
    term_two = fields.Text('Notes.', default=_default_terms_two )


    @api.multi
    def action_view_mo(self):
        action = self.env.ref('mrp.mrp_production_action').read()[0]
        pickings = self.mapped('production_id')
        action['views'] = [(self.env.ref('mrp.mrp_production_form_view').id, 'form')]
        action['res_id'] = pickings.id
        return action
