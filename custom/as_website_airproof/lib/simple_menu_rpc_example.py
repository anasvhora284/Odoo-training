#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple RPC example for Odoo 18.0
This script demonstrates how to retrieve menu items from Odoo
"""

import xmlrpc.client
import requests
import json
import pprint

# Connection parameters - modify these to match your Odoo server setup
URL = 'http://localhost:8069'
DB = 'theme_try'  # Your database name
USERNAME = 'admin'
PASSWORD = 'admin'

def get_menus_xmlrpc():
    """Get menu items using XML-RPC"""
    print("\n" + "=" * 70)
    print(" MENU ITEMS USING XML-RPC ".center(70, "="))
    print("=" * 70)
    
    # Connect to Odoo XML-RPC interface
    print("\n1. Connecting to Odoo server...")
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    
    # Authenticate
    print("2. Authenticating with Odoo...")
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    if not uid:
        print("Authentication failed! Check your credentials.")
        return
    print(f"   Authentication successful (uid: {uid})")
    
    # Create object proxy
    print("3. Creating object proxy...")
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    
    # Call method to get backend menu items
    print("4. Calling get_menu_items method...")
    menus = models.execute_kw(
        DB, uid, PASSWORD,
        'as_website_airproof.rpc_demo',
        'get_menu_items',
        [],  # Empty list for args
        {'menu_type': 'backend'}  # Keyword arguments
    )
    
    # Display results
    print("\n5. Backend Menu Results:")
    print("-" * 70)
    pp = pprint.PrettyPrinter(indent=2)
    
    if menus.get('success'):
        # Print Airproof menus
        print("\nAirproof Module Menus:")
        for menu in menus['menu_items']['backend_menus']['airproof_menus']:
            print(f"  - {menu['name']} (ID: {menu['id']})")
        
        # Print a few main menus
        print("\nMain Backend Menus (top 5):")
        for i, menu in enumerate(menus['menu_items']['backend_menus']['main_menus']):
            if i < 5:
                print(f"  - {menu['name']} (ID: {menu['id']})")
            else:
                break
    else:
        print(f"Error: {menus.get('error', 'Unknown error')}")

def get_menus_jsonrpc():
    """Get menu items using JSON-RPC"""
    print("\n" + "=" * 70)
    print(" MENU ITEMS USING JSON-RPC ".center(70, "="))
    print("=" * 70)
    
    # Create a session for making requests
    session = requests.Session()
    
    # Authenticate with Odoo
    print("\n1. Authenticating with Odoo...")
    auth_url = f'{URL}/web/session/authenticate'
    auth_data = {
        'jsonrpc': '2.0',
        'params': {
            'db': DB,
            'login': USERNAME,
            'password': PASSWORD
        }
    }
    
    response = session.post(
        auth_url,
        data=json.dumps(auth_data),
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 200:
        print(f"Authentication failed with status code: {response.status_code}")
        return
    
    auth_result = response.json()
    if 'error' in auth_result:
        print(f"Authentication error: {auth_result['error']}")
        return
    
    print("   Authentication successful!")
    
    # Get frontend menu items using direct endpoint
    print("\n2. Fetching frontend menu items...")
    rpc_url = f'{URL}/simple_rpc/menus'
    data = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {
            'menu_type': 'frontend'
        },
        'id': 1
    }
    
    response = session.post(
        rpc_url,
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    
    # Display results
    print("\n3. Frontend Menu Results:")
    print("-" * 70)
    
    result = response.json()
    if 'result' in result and result['result'].get('success'):
        menus = result['result']['menu_items']['frontend_menus']
        
        # Print Airproof website menus
        print("\nAirproof Module Website Menus:")
        for menu in menus['airproof_menus']:
            print(f"  - {menu['name']} (URL: {menu['url']})")
        
        # Print a few website menus
        print("\nAll Website Menus (top 5):")
        for i, menu in enumerate(menus['all_menus']):
            if i < 5:
                print(f"  - {menu['name']} (URL: {menu['url']})")
            else:
                break
    else:
        error = result.get('error') or (result.get('result') or {}).get('error', 'Unknown error')
        print(f"Error: {error}")

def main():
    """Main function"""
    print("\n" + "*" * 70)
    print(" ODOO MENU ITEMS RPC EXAMPLES ".center(70, "*"))
    print("*" * 70)
    
    # Get menus using XML-RPC
    get_menus_xmlrpc()
    
    # Get menus using JSON-RPC
    get_menus_jsonrpc()
    
    print("\n" + "=" * 70)
    print(" END OF DEMONSTRATION ".center(70, "="))
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main() 