from odoo import models, fields, api,_
import logging
import json

_logger = logging.getLogger(__name__)
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    contact_person=fields.Many2one("hr.employee",string="Contact Person")
    contact_phone=fields.Char(related="contact_person.work_phone",string="Contact Phone")


class ResCompany(models.Model):
    _inherit = 'res.company'

    paybill=fields.Char(string="Paybill Number")
    account=fields.Char(string="Paybill Account")