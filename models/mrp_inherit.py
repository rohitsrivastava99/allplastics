# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError
from datetime import datetime

class Product(models.Model):
    _inherit = 'product.template'

    workcenter_id = fields.Many2one('mrp.workcenter', string="Work Center")

class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.multi
    def make_mo(self):
        res = super(ProcurementOrder, self).make_mo()
        line_obj =  self.search([('origin', '=', self.origin.rsplit(':')[0]), ('product_id','=',self.product_id.id)]).sale_line_id
        mo_id = res[self.id]
        mo = self.env['mrp.production'].search([('id','=',mo_id)])
        routing_id = mo.bom_id.routing_id
        line_obj.order_id.production_id = mo_id
        lines = line_obj.order_id.order_line
        centers = line_obj.order_id.order_line.filtered(lambda self: self.product_id.workcenter_id).mapped('product_id').mapped('workcenter_id')
        rworkcenter = self.env['mrp.routing.workcenter']
        if not routing_id:
            route = self.env['mrp.routing']
            routing_id = route.create({'name':'first'})
        routing_id.operation_ids.unlink()
        for c in centers:
            print 'c ', c
            rworkcenter.create({'name':c.name,'workcenter_id':c.id,'routing_id':routing_id.id})
        print "=======================",routing_id
        mo.bom_id.routing_id = routing_id
        #import pudb;pudb.set_trace()
        # print "=============lines",lines
        # for line in line_obj:
        #     mo.write({'length': line.length,'width':line.width})
        #     print "=======================mo",mo
        # return False
        # mo > bom > routing_id > work_center_ids 
        return res

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
 
    packaging_instruction = fields.Text("Packaging Instruction")
    job_for = fields.Char('Job is For')
    job_header = fields.Char('Job Header')
    due_date = fields.Date('Due Date')
    pickup = fields.Char('Pick Up')



    def get_name(self,obj):
        return self.env['sale.order'].search([('production_id','=',obj.id)],limit=1)

    def get_drawing(self,obj):
        sale_id =  self.env['sale.order'].search([('production_id','=',obj.id)],limit=1)
        sale_order = self.env['sale.order.line'].search([('product_id','=',obj.product_id.id),('order_id','=',sale_id.id)])
        print "---------sale",sale_order.drawing
        return sale_order