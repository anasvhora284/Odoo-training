#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple JSON-RPC example for Odoo 18.0
This script demonstrates how to use JSON-RPC to get product list from Odoo
"""

import requests
import json
import pprint

# Connection parameters - modify these to match your Odoo server setup
URL = 'http://localhost:8069'
DB = 'theme_try'  # Your database name
USERNAME = 'admin'
PASSWORD = 'admin'

def main():
    print("=" * 70)
    print(" SIMPLE JSON-RPC EXAMPLE - PRODUCT LIST ".center(70, "="))
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
    
    # Get products using direct endpoint
    print("\n2. Fetching products using direct endpoint...")
    rpc_url = f'{URL}/simple_rpc/products'
    data = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {
            'limit': 5  # Limit to 5 products
        },
        'id': 1
    }
    
    response = session.post(
        rpc_url,
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    
    # Display results
    print("\n3. Results:")
    print("-" * 70)
    pp = pprint.PrettyPrinter(indent=2)
    result = response.json()
    pp.pprint(result)

if __name__ == '__main__':
    main() 