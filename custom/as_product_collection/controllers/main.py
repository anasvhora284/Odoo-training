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

    @http.route('/product_collection/get_collection_products', type='json', auth='public', website=True)
    def get_collection_products(self, collection_id):
        try:
            collection = request.env['website.product.collection'].sudo().browse(int(collection_id))
            if not collection.exists():
                _logger.warning(f"Collection {collection_id} not found")
                return []

            products_data = collection.get_collection_products()
            _logger.info(f"Found {len(products_data)} products for collection {collection_id}")
            return products_data
        except Exception as e:
            _logger.error(f"Error fetching products for collection {collection_id}: {str(e)}")
            return [] 