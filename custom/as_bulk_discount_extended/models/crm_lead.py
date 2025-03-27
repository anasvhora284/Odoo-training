# -*- coding: utf-8 -*-

from odoo import models, fields

class CRMLead(models.Model):
    _inherit = "crm.lead"

    sbodr_description = fields.Text("SBODR Description")
    sbodr_discount = fields.Float("SBODR Discount %", default=0.0)
    sbodr_quantity = fields.Integer("SBODR Quantity", default=0)
