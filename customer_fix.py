from odoo import api, fields, models, _
import requests
from ..tool import api_meet
from datetime import datetime
import logging
import urllib.parse

logger = logging.getLogger(__name__)

auth_header = {
    "Accept": "application/json"
}

class Customer(models.Model):
    _name = 'rikai.customer'
    _description = 'Rikai Customers'
    _order = 'last_update DESC'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string="Customer Name", readonly=True, track_visibility='onchange')
    customer_id = fields.Char(string="Customer Id", readonly=True) # Backlog id
    backlog_key = fields.Char(string="Backlock Key" , readonly=True)
    backlog_link = fields.Char(string="Backlog", widget='html', compute="_compute_backlog_link", readonly=True)
    ticket_status = fields.Char(string="Ticket Status", readonly=True, track_visibility='onchange')
    assignee = fields.Char(string="Assignee", readonly=True, track_visibility='onchange')
    last_update = fields.Datetime(string="Last Update", readonly=True, track_visibility='onchange')
    update_by = fields.Char(string="Updater", readonly=True, track_visibility='onchange')
    stage = fields.Char(string="Stage", readonly=True, track_visibility='onchange')
    deleted = fields.Boolean(string="Deleted", readonly=True)

    channel = fields.Char(string="Channel", readonly=True, track_visibility='onchange')

    projects = fields.One2many('project','customer', string="Projects", readonly=True, track_visibility='onchange')
    project_count = fields.Integer(string="Project Count", store=True, readonly=True, compute="_compute_project_count", track_visibility='onchange')
    life_time_value = fields.Float(string='LTV', readonly=True, store=True, compute="_compute_ltv", track_visibility='onchange')

    opportunities = fields.One2many('rikai.opportunity','customer', string="Opps", readonly=True, track_visibility='onchange')
    opportunity_count = fields.Integer(string="Opps Count", store=True, readonly=True, compute="_compute_opportunity_count", track_visibility='onchange')
    
    # Create backlog link
    @api.depends('backlog_key')
    def _compute_backlog_link(self):
        for record in self:
            if record.backlog_key:
                link = "https://rikai.backlog.com/view/{}".format(record.backlog_key)
                record.backlog_link = "<a href=\"{}\" target=\"_blank\">{}</a>".format(link, record.backlog_key)

    #Load all customer from backlog
    def loadCustomer(self):
        url = "https://rikai.backlog.com/api/v2/issues?apiKey=0p1ahLtfAF4Gric24ALErorYXs3FK4Wjw4Nr84g5pQl1q0otjGypnCMoJVdQlacB&projectId[]=90792&issueTypeId[]=386821&count=100&offset="

        offset = 0
        count = 100
        
        # Get the records you want to update
        records = self.env['rikai.customer'].search([])
        # Update the 'deleted' field to True for each record
        records.write({'deleted': True})

        while count == 100:
            result = requests.get(
                url + str(offset), headers=auth_header).json()
            count = len(result)
            offset += count

            if "errors" in result:
                logger.error(result)
                return

            for payload in result:
                # If issue is not child issue then return
                if payload["parentIssueId"]:
                    continue
                
                # Create Customer Data from Payload
                data = self._createData(payload)

                # Search customer in database
                # customer = self.search(
                #     [("backlog_key", "=", "RIKAI_AM-979")])
                customer = self.search([("backlog_key", "=", data["backlog_key"])])
                TEMP=1
                for child in customer:
                    if(TEMP==1):
                        customer1=child
                    TEMP=2
                # Update customer information from backlog
                if customer1:
                    customer1.write(data)
                else:
                    customer1 = self.create(data)

                # Allocate projects to customer
                #rikai.customer(2,7,4,6) _allocate_projects can receive lots of ids handle that case
                self._allocate_projects(customer1)

                # Allocate opps to customer
                self._allocate_opportunities(customer1)
        
        view_id_tree = self.env.ref('rikai_kintai.rikai_customer_view_tree')
        view = [(view_id_tree[0].id, 'list')]
        domain = []
        return {
            'name': _('/'),
            'res_model': 'rikai.customer',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'views': view,
            'target': 'current',
            'domain': domain,
        }  
    
    # This method is call by controller (API)
    def updateTicket(self, updatedItem):
        if "errors" in updatedItem:
            return
        # Url to get infomation from backlog
        url = "https://rikai.backlog.com/api/v2/issues/{}?apiKey=0p1ahLtfAF4Gric24ALErorYXs3FK4Wjw4Nr84g5pQl1q0otjGypnCMoJVdQlacB"

        # get issue data from backlog
        payload = requests.get(url.format(
            updatedItem["content"]["id"]), headers=auth_header).json()  
        
        # Search issue is already in model or not
        record = self.search([("customer_id", "=", updatedItem["content"]["id"])])

        if "errors" in payload and record:
            record.deleted = True
            record.unlink()
            return
        
        # create model data to insert/update
        data = self._createData(payload)

        # If issue is not parrent issue then return
        if payload["parentIssueId"]:
            if record:
                record.deleted = True
                record.unlink()
            return

        # If issue is not customer then return
        if payload["issueType"]["id"] != 386821:
            if record:
                record.deleted = True
                record.unlink()
            return

        # Create or update data
        if record:
            record.write(data)
        else:
            record = self.create(data)
            
        # Allocate projects to customer
        self._allocate_projects(record)

        # Allocate opps to customer
        self._allocate_opportunities(record)

    # Allocate projects to customer
    def _allocate_projects(self, customer):
            projects = self.env["project"].search([("customer_id","=",customer.customer_id)])
            customer.projects = projects

    def _allocate_opportunities(self, customer):
        opportunities = self.env["rikai.opportunity"].search([("customer_id","=",customer.customer_id)])
        customer.opportunities = opportunities
    
    # Calculate number of projects
    @api.depends('projects')
    def _compute_project_count(self):
        for record in self:
            record.project_count = len(record.projects)

    # Calculate number of opportunity
    @api.depends('opportunities')
    def _compute_opportunity_count(self):
        for record in self:
            record.opportunity_count = len(record.opportunities)
    
    @api.depends('projects')
    def _compute_ltv(self):
        for record in self:
            record.life_time_value = sum(record.projects.mapped('total_revenue'))
        
    # Create data from backlog payload
    def _createData(self, payload):

        data = {
            "deleted": False,
            "customer_id":payload["id"],
            "name": payload["summary"],
            "backlog_key": payload["issueKey"],
            "ticket_status": payload["status"]["name"],
            "assignee": payload["assignee"]["name"] if payload["assignee"] else None,
            "last_update": payload["created"],
            "update_by": payload["updatedUser"]["name"],
            "stage": next((field['value']['name'] if field['value'] else None for field in payload["customFields"] if field['id'] == 11058), None),
            "channel": next((field['value']['name'] if field['value'] else None for field in payload["customFields"] if field['id'] == 11056), None),
        }
        return data
            
