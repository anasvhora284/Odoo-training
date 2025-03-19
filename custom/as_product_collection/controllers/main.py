from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class ProductCollectionController(http.Controller):
    @http.route('/product_collection/get_collections', type='json', auth='public', website=True)
    def get_collections(self):
        try:
            collections = request.env['website.product.collection'].sudo().search_read(
                [], ['id', 'name']
            )
            _logger.info(f"Found {len(collections)} collections")
            return collections
        except Exception as e:
            _logger.error(f"Error fetching collections: {str(e)}")
            return []

    @http.route('/product_collection/get_collection_info', type='json', auth='public', website=True)
    def get_collection_info(self, collection_id):
        try:
            collection_id = int(collection_id)
            collection = request.env['website.product.collection'].sudo().search_read(
                [('id', '=', collection_id)], ['id', 'name']
            )
            if collection:
                _logger.info(f"Found collection info for collection {collection_id}")
                return collection[0]
            else:
                _logger.warning(f"Collection {collection_id} not found")
                return {'name': 'Product Collection'}
        except Exception as e:
            _logger.error(f"Error fetching collection info for collection {collection_id}: {str(e)}")
            return {'name': 'Product Collection'}

    @http.route('/product_collection/get_collection_products', type='json', auth='public', website=True)
    def get_collection_products(self, collection_id):
        try:
            collection_id = int(collection_id)
            collection = request.env['website.product.collection'].sudo().browse(collection_id)
            if not collection.exists():
                _logger.warning(f"Collection {collection_id} not found")
                return []

            # Use the model method to get formatted product data
            products_data = collection.get_collection_products()
            _logger.info(f"Found {len(products_data)} products for collection {collection_id}")
            return products_data
        except Exception as e:
            _logger.error(f"Error fetching products for collection {collection_id}: {str(e)}")
            return []
            
    @http.route('/product_collection/get_snippet_data', type='json', auth='public', website=True)
    def get_snippet_data(self, collection_id=None):
        """Return both collections and products for a selected collection"""
        try:
            # Get all available collections
            collections = request.env['website.product.collection'].sudo().search_read(
                [], ['id', 'name']
            )
            
            # Get products for the selected collection
            products = []
            if collection_id:
                collection = request.env['website.product.collection'].sudo().browse(int(collection_id))
                if collection.exists():
                    products = collection.get_collection_products()
            
            return {
                'collections': collections,
                'products': products
            }
        except Exception as e:
            _logger.error(f"Error fetching snippet data: {str(e)}")
            return {
                'collections': [],
                'products': [],
                'error': str(e)
            }