from odoo import http
from odoo.http import request

class CounterController(http.Controller):

    @http.route('/counter', type='http', auth='public', website=True)
    def counter_page(self, **kw):
        return request.render('as_website_airproof.counter_template', {})