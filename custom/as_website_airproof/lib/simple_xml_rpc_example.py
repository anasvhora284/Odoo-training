#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple XML-RPC example for Odoo 18.0
This script demonstrates how to use XML-RPC to get product list from Odoo
"""

import xmlrpc.client
import pprint

# Connection parameters - modify these to match your Odoo server setup
URL = 'http://localhost:8069'
DB = 'theme_try'  # Your database name
USERNAME = 'admin'
PASSWORD = 'admin'

def main():
    print("=" * 70)
    print(" SIMPLE XML-RPC EXAMPLE - PRODUCT LIST ".center(70, "="))
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
    
    # Call method to get products
    print("4. Calling get_product_list method...")
    products = models.execute_kw(
        DB, uid, PASSWORD,
        'as_website_airproof.rpc_demo',
        'get_product_list',
        [[5]]  # Limit to 5 products
    )
    
    # Display results
    print("\n5. Results:")
    print("-" * 70)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(products)

if __name__ == '__main__':
    main() 