# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SBODRRequest(models.Model):
    _name = "sbodr.request"
    _description = "Special Bulk Order Discount Request"
    
    name = fields.Char(string="Request Name", required=True)
    full_name = fields.Char(string="Full Name", required=True)
    email = fields.Char(string="Email", required=True)
    quantity = fields.Integer(string="Quantity", required=True)
    discount = fields.Float(string="Discount (%)", required=True)
    description = fields.Text(string="Description")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", default='draft')
