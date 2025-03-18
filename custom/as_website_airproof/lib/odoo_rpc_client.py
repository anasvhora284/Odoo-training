#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Odoo RPC Client for Odoo 18.0
This script demonstrates how to interact with Odoo using both XML-RPC and JSON-RPC protocols.
It shows common operations like authentication, CRUD operations, and calling model methods.
"""

import xmlrpc.client
import json
import random
import requests
import sys
from pprint import pprint


class OdooXMLRPC:
    """XML-RPC client for Odoo 18.0"""
    
    def __init__(self, host, port=8069, db=None, username=None, password=None):
        """Initialize the XML-RPC connection to Odoo server"""
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.url = f'http://{host}:{port}'
        self.uid = None
        
        # XML-RPC endpoints
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        self.db_service = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/db')
        
    def authenticate(self):
        """Authenticate user and get user id"""
        self.uid = self.common.authenticate(self.db, self.username, self.password, {})
        if not self.uid:
            raise Exception("Authentication failed")
        print(f"Authentication successful (uid: {self.uid})")
        return self.uid
    
    def version(self):
        """Get the Odoo server version information"""
        return self.common.version()
    
    def list_databases(self):
        """List available databases on the server"""
        return self.db_service.list()
    
    def create_record(self, model, values):
        """Create a record in the specified model"""
        record_id = self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'create', [values]
        )
        return record_id
    
    def read_records(self, model, ids, fields=None):
        """Read records by ID from the specified model"""
        if fields is None:
            fields = []
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'read', [ids], {'fields': fields}
        )
    
    def search_records(self, model, domain, limit=None, offset=0, order=None):
        """Search for records that match the domain"""
        kwargs = {
            'offset': offset,
        }
        if limit is not None:
            kwargs['limit'] = limit
        if order:
            kwargs['order'] = order
            
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'search', [domain], kwargs
        )
    
    def search_read(self, model, domain, fields=None, limit=None, offset=0, order=None):
        """Search and read records in a single call"""
        if fields is None:
            fields = []
            
        kwargs = {
            'fields': fields,
            'offset': offset,
        }
        if limit is not None:
            kwargs['limit'] = limit
        if order:
            kwargs['order'] = order
            
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'search_read', [domain], kwargs
        )
    
    def update_record(self, model, id, values):
        """Update a record by ID"""
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'write', [[id], values]
        )
    
    def delete_record(self, model, ids):
        """Delete record(s) by ID"""
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'unlink', [ids]
        )
    
    def call_method(self, model, method, args=None, kwargs=None):
        """Call any method on a model"""
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
            
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, method, args, kwargs
        )
    
    def get_fields(self, model):
        """Get field details of a model"""
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'fields_get', [], {'attributes': ['string', 'help', 'type']}
        )


class OdooJSONRPC:
    """JSON-RPC client for Odoo 18.0"""
    
    def __init__(self, host, port=8069, db=None, username=None, password=None):
        """Initialize the JSON-RPC connection to Odoo server"""
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.url = f'http://{host}:{port}/jsonrpc'
        self.uid = None
        self.session_id = None
        
    def _json_rpc(self, service, method, params):
        """Make a JSON-RPC request to the Odoo server"""
        headers = {'Content-Type': 'application/json'}
        
        data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'service': service,
                'method': method,
                'args': params
            },
            'id': random.randint(0, 1000000000)
        }
        
        response = requests.post(
            self.url,
            data=json.dumps(data),
            headers=headers,
            cookies={'session_id': self.session_id} if self.session_id else {}
        )
        
        response.raise_for_status()
        result = response.json()
        
        if 'error' in result:
            error = result['error']
            raise Exception(f"JSON-RPC error: {error['message']}\n{error.get('data', {}).get('debug', '')}")
        
        return result.get('result')
    
    def authenticate(self):
        """Authenticate user and get user id"""
        params = [self.db, self.username, self.password, {}]
        result = self._json_rpc('common', 'authenticate', params)
        self.uid = result
        
        if not self.uid:
            raise Exception("Authentication failed")
        
        print(f"Authentication successful (uid: {self.uid})")
        return self.uid
    
    def version(self):
        """Get the Odoo server version information"""
        return self._json_rpc('common', 'version', [])
    
    def list_databases(self):
        """List available databases on the server"""
        return self._json_rpc('db', 'list', [])
    
    def create_record(self, model, values):
        """Create a record in the specified model"""
        params = [self.db, self.uid, self.password, model, 'create', [values]]
        return self._json_rpc('object', 'execute_kw', params)
    
    def read_records(self, model, ids, fields=None):
        """Read records by ID from the specified model"""
        if fields is None:
            fields = []
        params = [self.db, self.uid, self.password, model, 'read', [ids], {'fields': fields}]
        return self._json_rpc('object', 'execute_kw', params)
    
    def search_records(self, model, domain, limit=None, offset=0, order=None):
        """Search for records that match the domain"""
        kwargs = {'offset': offset}
        if limit is not None:
            kwargs['limit'] = limit
        if order:
            kwargs['order'] = order
            
        params = [self.db, self.uid, self.password, model, 'search', [domain], kwargs]
        return self._json_rpc('object', 'execute_kw', params)
    
    def search_read(self, model, domain, fields=None, limit=None, offset=0, order=None):
        """Search and read records in a single call"""
        if fields is None:
            fields = []
            
        kwargs = {
            'fields': fields,
            'offset': offset,
        }
        if limit is not None:
            kwargs['limit'] = limit
        if order:
            kwargs['order'] = order
            
        params = [self.db, self.uid, self.password, model, 'search_read', [domain], kwargs]
        return self._json_rpc('object', 'execute_kw', params)
    
    def update_record(self, model, id, values):
        """Update a record by ID"""
        params = [self.db, self.uid, self.password, model, 'write', [[id], values]]
        return self._json_rpc('object', 'execute_kw', params)
    
    def delete_record(self, model, ids):
        """Delete record(s) by ID"""
        params = [self.db, self.uid, self.password, model, 'unlink', [ids]]
        return self._json_rpc('object', 'execute_kw', params)
    
    def call_method(self, model, method, args=None, kwargs=None):
        """Call any method on a model"""
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
            
        params = [self.db, self.uid, self.password, model, method, args, kwargs]
        return self._json_rpc('object', 'execute_kw', params)
    
    def get_fields(self, model):
        """Get field details of a model"""
        params = [self.db, self.uid, self.password, model, 'fields_get', [], {'attributes': ['string', 'help', 'type']}]
        return self._json_rpc('object', 'execute_kw', params)


def demo_xml_rpc():
    """Demonstrate XML-RPC functionality"""
    print("\n" + "="*50)
    print("XML-RPC DEMO")
    print("="*50)
    
    # Configuration
    host = 'localhost'
    port = 8069
    db = 'theme_try'
    username = 'admin'
    password = 'admin'
    
    try:
        # Initialize client
        client = OdooXMLRPC(host, port, db, username, password)
        
        # Get server version
        version = client.version()
        print("\nServer version:")
        pprint(version)
        
        # List databases
        databases = client.list_databases()
        print("\nAvailable databases:")
        pprint(databases)
        
        # Authenticate
        client.authenticate()
        
        # Get partner fields
        print("\nPartner model fields:")
        fields = client.get_fields('res.partner')
        # Print just a few fields to avoid too much output
        print(f"Number of fields: {len(fields)}")
        for field_name in list(fields.keys())[:5]:
            print(f"- {field_name}: {fields[field_name]['type']}")
        
        # Search and read partners
        print("\nPartners (limit 5):")
        partners = client.search_read(
            'res.partner', 
            [], 
            ['id', 'name', 'email', 'phone'], 
            limit=5
        )
        pprint(partners)
        
        # Create a new partner
        new_partner = {
            'name': f'Test Partner XML-RPC {random.randint(1, 1000)}',
            'email': 'xml-rpc-test@example.com',
            'phone': '+1234567890',
        }
        partner_id = client.create_record('res.partner', new_partner)
        print(f"\nCreated new partner with ID: {partner_id}")
        
        # Read the new partner
        partner = client.read_records('res.partner', [partner_id], ['name', 'email', 'phone'])
        print("\nNew partner details:")
        pprint(partner)
        
        # Update the partner
        client.update_record('res.partner', partner_id, {'name': partner[0]['name'] + ' (Updated)'})
        print("\nUpdated partner name")
        
        # Read the updated partner
        updated_partner = client.read_records('res.partner', [partner_id], ['name', 'email', 'phone'])
        print("\nUpdated partner details:")
        pprint(updated_partner)
        
        # Count total partners
        total = client.call_method('res.partner', 'search_count', [[]])
        print(f"\nTotal partners in the system: {total}")
        
        # Delete the test partner
        client.delete_record('res.partner', [partner_id])
        print(f"\nDeleted partner with ID: {partner_id}")
        
    except Exception as e:
        print(f"Error: {e}")
        
    print("="*50)


def demo_json_rpc():
    """Demonstrate JSON-RPC functionality"""
    print("\n" + "="*50)
    print("JSON-RPC DEMO")
    print("="*50)
    
    # Configuration
    host = 'localhost'
    port = 8069
    db = 'theme_try'
    username = 'admin'
    password = 'admin'
    
    try:
        # Initialize client
        client = OdooJSONRPC(host, port, db, username, password)
        
        # Get server version
        version = client.version()
        print("\nServer version:")
        pprint(version)
        
        # List databases
        databases = client.list_databases()
        print("\nAvailable databases:")
        pprint(databases)
        
        # Authenticate
        client.authenticate()
        
        # Get partner fields
        print("\nPartner model fields:")
        fields = client.get_fields('res.partner')
        # Print just a few fields to avoid too much output
        print(f"Number of fields: {len(fields)}")
        for field_name in list(fields.keys())[:5]:
            print(f"- {field_name}: {fields[field_name]['type']}")
        
        # Search and read partners
        print("\nPartners (limit 5):")
        partners = client.search_read(
            'res.partner', 
            [], 
            ['id', 'name', 'email', 'phone'], 
            limit=5
        )
        pprint(partners)
        
        # Create a new partner
        new_partner = {
            'name': f'Test Partner JSON-RPC {random.randint(1, 1000)}',
            'email': 'json-rpc-test@example.com',
            'phone': '+0987654321',
        }
        partner_id = client.create_record('res.partner', new_partner)
        print(f"\nCreated new partner with ID: {partner_id}")
        
        # Read the new partner
        partner = client.read_records('res.partner', [partner_id], ['name', 'email', 'phone'])
        print("\nNew partner details:")
        pprint(partner)
        
        # Update the partner
        client.update_record('res.partner', partner_id, {'name': partner[0]['name'] + ' (Updated)'})
        print("\nUpdated partner name")
        
        # Read the updated partner
        updated_partner = client.read_records('res.partner', [partner_id], ['name', 'email', 'phone'])
        print("\nUpdated partner details:")
        pprint(updated_partner)
        
        # Count total partners
        total = client.call_method('res.partner', 'search_count', [[]])
        print(f"\nTotal partners in the system: {total}")
        
        # Delete the test partner
        client.delete_record('res.partner', [partner_id])
        print(f"\nDeleted partner with ID: {partner_id}")
        
    except Exception as e:
        print(f"Error: {e}")
        
    print("="*50)


if __name__ == '__main__':
    """Main entry point"""
    
    if len(sys.argv) > 1 and sys.argv[1] == 'json':
        # Run JSON-RPC demo
        demo_json_rpc()
    elif len(sys.argv) > 1 and sys.argv[1] == 'xml':
        # Run XML-RPC demo
        demo_xml_rpc()
    else:
        # Run both demos
        demo_xml_rpc()
        demo_json_rpc() 