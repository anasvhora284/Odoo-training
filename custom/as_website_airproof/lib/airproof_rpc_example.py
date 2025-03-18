#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Airproof Odoo RPC Example

This script demonstrates how to use the Odoo XML-RPC API to interact with 
the Airproof website module in Odoo 18.0.
"""

import xmlrpc.client
import json
import random
import sys
from pprint import pprint

# Import the RPC clients
sys.path.append('.')
from lib.odoo_rpc_client import OdooXMLRPC, OdooJSONRPC


def airproof_xml_rpc_demo():
    """Demonstrate XML-RPC interactions with Airproof module"""
    print("\n" + "="*50)
    print("AIRPROOF XML-RPC DEMO")
    print("="*50)
    
    # Configuration - Update these with your Odoo server settings
    host = 'localhost'
    port = 8069
    db = 'theme_try'  # Update this with your actual database name
    username = 'admin'
    password = 'admin'  # Update this with your actual password
    
    try:
        # Initialize client
        client = OdooXMLRPC(host, port, db, username, password)
        
        # Authenticate
        uid = client.authenticate()
        
        # Check if website module is installed
        print("\nChecking installed modules...")
        modules = client.search_read(
            'ir.module.module',
            [('state', '=', 'installed'), ('name', '=', 'website')],
            ['name', 'state']
        )
        if modules:
            print("Website module is installed")
        else:
            print("Website module is not installed")
            return
        
        # List website menus
        print("\nWebsite menus for Airproof:")
        menus = client.search_read(
            'website.menu',
            [('website_id', '=', 1)],  # Assuming website ID 1
            ['name', 'url', 'parent_id', 'sequence']
        )
        
        for menu in menus:
            parent = "Root" if not menu.get('parent_id') else menu['parent_id'][1]
            print(f"- {menu['name']} (URL: {menu['url']}, Parent: {parent}, Sequence: {menu['sequence']})")
        
        # Get snippets information
        print("\nWebsite snippets:")
        snippets = client.call_method(
            'ir.model.data',
            'search_read',
            [[('model', '=', 'ir.ui.view'), ('module', '=', 'as_website_airproof')]],
            {'fields': ['name', 'res_id', 'model']}
        )
        
        snippet_ids = [s['res_id'] for s in snippets if s['model'] == 'ir.ui.view']
        if snippet_ids:
            views = client.search_read(
                'ir.ui.view',
                [('id', 'in', snippet_ids), ('type', '=', 'qweb')],
                ['name', 'key', 'type', 'website_id']
            )
            for view in views:
                print(f"- {view['name']} (Key: {view['key']}, Type: {view['type']})")
        
        # Create a test page using RPC
        page_name = f"RPC Test Page {random.randint(1, 1000)}"
        page_values = {
            'name': page_name,
            'website_id': 1,  # Main website
            'url': f'/rpc-test-{random.randint(1, 1000)}',
            'view_id': False,  # Will be created automatically
            'is_published': True,
            'website_indexed': True,
            'menu_ids': [(0, 0, {
                'name': page_name,
                'website_id': 1,
                'parent_id': False,  # Root menu
                'sequence': 50,
            })],
            'content': f"""
            <div class="oe_structure">
                <section class="pt32 pb32">
                    <div class="container">
                        <h1 class="text-center">{page_name}</h1>
                        <p class="text-center">This page was created using XML-RPC API.</p>
                        <div class="row">
                            <div class="col-lg-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h3>XML-RPC</h3>
                                        <p>XML-RPC is a remote procedure call protocol which uses XML to encode its calls and HTTP as a transport mechanism.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-lg-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h3>JSON-RPC</h3>
                                        <p>JSON-RPC is a remote procedure call protocol encoded in JSON. It is a very simple protocol.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
            """
        }
        
        # Check if we can create pages with the current user
        can_create = client.call_method(
            'website.page',
            'check_access_rights',
            ['create'],
            {'raise_exception': False}
        )
        
        if can_create:
            print("\nCreating a test page...")
            page_id = client.create_record('website.page', page_values)
            print(f"Created new page with ID: {page_id}")
            
            # Get details of the created page
            page = client.read_records('website.page', [page_id], ['name', 'url', 'website_id', 'is_published'])
            print("\nNew page details:")
            pprint(page)
            
            # Get the associated view
            view_id = client.search_records('ir.ui.view', [('page_id', '=', page_id)])
            if view_id:
                view = client.read_records('ir.ui.view', view_id, ['name', 'key', 'type'])
                print("\nPage view details:")
                pprint(view)
                
            # Delete the test page
            print("\nDeleting the test page...")
            client.delete_record('website.page', [page_id])
            print(f"Deleted page with ID: {page_id}")
        else:
            print("\nCurrent user doesn't have permission to create website pages")
        
    except Exception as e:
        print(f"Error: {e}")
        
    print("="*50)


def airproof_json_rpc_demo():
    """Demonstrate JSON-RPC interactions with Airproof module"""
    print("\n" + "="*50)
    print("AIRPROOF JSON-RPC DEMO")
    print("="*50)
    
    # Configuration - Update these with your Odoo server settings
    host = 'localhost'
    port = 8069
    db = 'theme_try'  # Update this with your actual database name
    username = 'admin'
    password = 'admin'  # Update this with your actual password
    
    try:
        # Initialize client
        client = OdooJSONRPC(host, port, db, username, password)
        
        # Authenticate
        uid = client.authenticate()
        
        # Get website configuration
        print("\nWebsite configuration:")
        websites = client.search_read(
            'website',
            [],
            ['name', 'domain', 'company_id', 'default_lang_id']
        )
        pprint(websites)
        
        # Get specific templates from the Airproof module
        print("\nAirproof templates:")
        templates = client.search_read(
            'ir.ui.view',
            [('key', 'like', 'as_website_airproof%'), ('type', '=', 'qweb')],
            ['name', 'key', 'website_id', 'active']
        )
        
        for template in templates:
            website = template.get('website_id') and template['website_id'][1] or 'All websites'
            print(f"- {template['name']} (Key: {template['key']}, Website: {website})")
        
        # Work with calculator component settings
        print("\nCalculator component functionality:")
        
        # Simulate making a calculation through RPC
        # This shows how you can call Odoo model methods directly
        
        # Define calculation inputs
        inputs = {
            'first_number': 10.5,
            'second_number': 5.25,
            'operation': 'add'  # 'add', 'subtract', 'multiply', 'divide'
        }
        
        # Here, we're calling a hypothetical method 'perform_calculation' that could exist in our model
        # NOTE: This is an example - you would need to implement this method in your Odoo module
        print(f"\nPerforming calculation: {inputs['first_number']} + {inputs['second_number']}")
        
        # In real usage, you'd call your module's method:
        # result = client.call_method('as_website_airproof.calculator', 'perform_calculation', [inputs])
        
        # For demonstration, we'll calculate it manually
        result = inputs['first_number'] + inputs['second_number']
        print(f"Result: {result}")
        
        # Create a custom log entry to track RPC usage
        log_entry = {
            'name': f"JSON-RPC Calculator Usage {random.randint(1, 1000)}",
            'type': 'rpc',
            'function': 'perform_calculation',
            'params': json.dumps(inputs),
            'result': str(result),
            'user_id': uid,
        }
        
        # This would log to a hypothetical model for tracking RPC calls
        # client.create_record('as_website_airproof.rpc_log', log_entry)
        
        print("\nJSON-RPC calculation complete and logged.")
        
    except Exception as e:
        print(f"Error: {e}")
        
    print("="*50)


if __name__ == '__main__':
    """Main entry point"""
    
    if len(sys.argv) > 1 and sys.argv[1] == 'json':
        # Run JSON-RPC demo
        airproof_json_rpc_demo()
    elif len(sys.argv) > 1 and sys.argv[1] == 'xml':
        # Run XML-RPC demo
        airproof_xml_rpc_demo()
    else:
        # Run both demos
        airproof_xml_rpc_demo()
        airproof_json_rpc_demo() 