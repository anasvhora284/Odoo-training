from odoo import http
from odoo.http import request

class CounterController(http.Controller):

    @http.route('/counter', type='http', auth='public', website=True)
    def counter_page(self, **kw):
        return request.render('as_website_airproof.counter_template', {})
        
    @http.route('/notification', type='http', auth='public', website=True)
    def notification_page(self, **kw):
        return request.render('as_website_airproof.notification_template', {})
        
    @http.route('/rainbow', type='http', auth='public', website=True)
    def rainbow_page(self, **kw):
        return request.render('as_website_airproof.rainbow_template', {})
        
    @http.route('/calculator', type='http', auth='public', website=True)
    def calculator_page(self, **kw):
        return request.render('as_website_airproof.calculator_template', {})