"""
eBay Sell API Implementation (REST + OAuth 2.0)
Modern replacement for Trading API
"""
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class EbaySellAPI:
    def __init__(self, app_id=None, oauth_token=None, sandbox_mode=False):
        """
        Initialize eBay Sell API client with OAuth 2.0
        """
        self.app_id = app_id or os.getenv('EBAY_APP_ID', '')
        self.oauth_token = oauth_token or os.getenv('EBAY_AUTH_TOKEN', '')
        self.sandbox_mode = sandbox_mode or os.getenv('EBAY_SANDBOX', 'false').lower() == 'true'
        
        # eBay Sell API endpoints
        if self.sandbox_mode:
            self.base_url = "https://api.sandbox.ebay.com"
        else:
            self.base_url = "https://api.ebay.com"
        
        # Standard headers für alle REST-Calls
        self.headers = {
            'Authorization': f'Bearer {self.oauth_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-EBAY-C-MARKETPLACE-ID': 'EBAY_DE',  # Deutschland
            'User-Agent': 'eBayBot/2.0 (SellAPI; OAuth2.0; Python/3.13)'
        }
    
    def test_connection(self):
        """
        Test OAuth 2.0 connection with Account API
        """
        try:
            url = f"{self.base_url}/sell/account/v1/privilege"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': '🚀 eBay Sell API (OAuth 2.0) erfolgreich verbunden!',
                    'mode': 'sell_api_oauth',
                    'privileges': response.json()
                }
            elif response.status_code == 401:
                return {
                    'success': False,
                    'message': 'OAuth Token ungültig oder abgelaufen',
                    'error_code': 401
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'message': response.text}
                return {
                    'success': False,
                    'message': f'API Error {response.status_code}: {error_data.get("message", "Unknown error")}',
                    'error_code': response.status_code,
                    'error_data': error_data
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Netzwerkfehler: {str(e)}',
                'mode': 'network_error'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Unerwarteter Fehler: {str(e)}',
                'mode': 'unknown_error'
            }
    
    def get_inventory_items(self, limit=25, offset=0):
        """
        Get active inventory items (listings) using Inventory API
        """
        try:
            url = f"{self.base_url}/sell/inventory/v1/inventory_item"
            params = {
                'limit': limit,
                'offset': offset
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                items = []
                
                # Transform to our format
                for item in data.get('inventoryItems', []):
                    items.append({
                        'item_id': item.get('sku'),  # SKU als Item ID
                        'title': item.get('product', {}).get('title', 'Unbekannter Titel'),
                        'current_price': float(item.get('availability', {}).get('shipToLocationAvailability', {}).get('quantity', 0)),
                        'currency': 'EUR',
                        'listing_type': 'FixedPriceItem',
                        'listing_status': 'Active',
                        'best_offer_enabled': True  # Sell API unterstützt Best Offers
                    })
                
                return {
                    'success': True,
                    'message': f'{len(items)} aktive Listings abgerufen (Sell API)',
                    'items': items,
                    'total': data.get('total', len(items))
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'message': response.text}
                return {
                    'success': False,
                    'message': f'Inventory API Error {response.status_code}: {error_data.get("message", "Unknown error")}',
                    'items': []
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Fehler beim Abrufen der Listings: {str(e)}',
                'items': []
            }
    
    def get_orders(self, limit=25, offset=0):
        """
        Get recent orders (which may contain offers) using Fulfillment API
        """
        try:
            url = f"{self.base_url}/sell/fulfillment/v1/order"
            params = {
                'limit': limit,
                'offset': offset,
                'filter': 'orderfulfillmentstatus:{NOT_STARTED|IN_PROGRESS}'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                offers = []
                
                # Transform orders to our offer format
                for order in data.get('orders', []):
                    for line_item in order.get('lineItems', []):
                        offers.append({
                            'best_offer_id': order.get('orderId'),
                            'buyer_id': order.get('buyer', {}).get('username', 'Unknown'),
                            'buyer_message': 'Bestellung über Sell API',
                            'price': float(line_item.get('total', {}).get('value', 0)),
                            'currency': line_item.get('total', {}).get('currency', 'EUR'),
                            'offer_status': 'Active',
                            'created_time': order.get('creationDate', datetime.now().isoformat()),
                            'expires_time': '',
                            'item_id': line_item.get('legacyItemId', line_item.get('sku', ''))
                        })
                
                return {
                    'success': True,
                    'message': f'{len(offers)} Bestellungen/Angebote abgerufen (Sell API)',
                    'offers': offers
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'message': response.text}
                return {
                    'success': False,
                    'message': f'Orders API Error {response.status_code}: {error_data.get("message", "Unknown error")}',
                    'offers': []
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Fehler beim Abrufen der Bestellungen: {str(e)}',
                'offers': []
            }
    
    def respond_to_offer(self, order_id, action, message=None, counter_amount=None):
        """
        Respond to offers using Fulfillment API
        Note: Best Offer responses in Sell API are handled differently than Trading API
        """
        try:
            if action.lower() == 'accept':
                # For Sell API, we might need to fulfill the order
                url = f"{self.base_url}/sell/fulfillment/v1/order/{order_id}/shipping_fulfillment"
                data = {
                    "lineItems": [],  # Would be populated with actual line items
                    "shippedDate": datetime.now().isoformat(),
                    "shippingCarrierCode": "OTHER",
                    "trackingNumber": "MANUAL_ACCEPTANCE"
                }
            elif action.lower() == 'decline':
                # Cancellation might require different endpoint
                return {
                    'success': False,
                    'message': 'Order cancellation requires manual intervention in Sell API',
                    'action': action
                }
            else:
                return {
                    'success': False,
                    'message': 'Counter offers not directly supported in current Sell API implementation',
                    'action': action
                }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=30)
            
            if response.status_code in [200, 201]:
                return {
                    'success': True,
                    'message': f'Order {action}ed successfully via Sell API',
                    'action': action,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'message': response.text}
                return {
                    'success': False,
                    'message': f'Sell API Error {response.status_code}: {error_data.get("message", "Unknown error")}',
                    'action': action
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Fehler beim Antworten auf Angebot: {str(e)}',
                'action': action
            }

    # Compatibility methods to match Trading API interface
    def get_my_ebay_selling(self, active_list=True):
        """
        Get active listings using eBay Sell API + Browse API fallback
        """
        try:
            # Zuerst versuche Inventory API
            inventory_result = self._get_inventory_items()
            if inventory_result['success'] and inventory_result['total'] > 0:
                return inventory_result
            
            # Fallback: Browse API für traditionelle eBay Listings
            browse_result = self._get_browse_listings()
            if browse_result['success']:
                return browse_result
                
            # Wenn beides leer ist, gebe Inventory Ergebnis zurück
            return inventory_result
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Fehler beim Abrufen der Listings: {str(e)}',
                'items': []
            }
    
    def _get_inventory_items(self):
        """Original Inventory API Methode"""
        try:
            url = f"{self.base_url}/sell/inventory/v1/inventory_item"
            params = {
                'limit': 50,
                'offset': 0
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                items = []
                
                # Transform to our format
                for item in data.get('inventoryItems', []):
                    sku = item.get('sku', '')
                    product = item.get('product', {})
                    availability = item.get('availability', {})
                    
                    # Get price from shipToLocationAvailability
                    ship_availability = availability.get('shipToLocationAvailability', {})
                    if isinstance(ship_availability, list) and ship_availability:
                        ship_availability = ship_availability[0]
                    
                    # Extract price - handle both dict and list cases
                    current_price = 0.0
                    if isinstance(ship_availability, dict):
                        price_info = ship_availability.get('availabilityDistributions', [])
                        if price_info and isinstance(price_info, list) and len(price_info) > 0:
                            fulfillment_info = price_info[0].get('fulfillmentTime', {}) if isinstance(price_info[0], dict) else {}
                            if isinstance(fulfillment_info, dict):
                                try:
                                    current_price = float(fulfillment_info.get('value', 0))
                                except (ValueError, TypeError):
                                    current_price = 0.0
                    
                    items.append({
                        'item_id': sku,
                        'title': product.get('title', 'Unbekannter Titel'),
                        'current_price': current_price,
                        'currency': 'EUR',
                        'listing_type': 'FixedPriceItem',
                        'listing_status': 'Active',
                        'best_offer_enabled': True
                    })
                
                return {
                    'success': True,
                    'message': f'{len(items)} aktive Listings abgerufen (Inventory API)',
                    'items': items,
                    'total': data.get('total', len(items))
                }
            elif response.status_code == 204:
                return {
                    'success': True,
                    'message': 'Keine aktiven Listings gefunden (Inventory API)',
                    'items': [],
                    'total': 0
                }
            else:
                return {
                    'success': False,
                    'message': f'Inventory API Error {response.status_code}',
                    'items': []
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Inventory API Fehler: {str(e)}',
                'items': []
            }
    
    def _get_inventory_items_paginated(self, limit=200, max_pages=100):
        """
        Get inventory items with pagination for massive inventories (158k+ items)
        """
        all_items = []
        total_found = 0
        offset = 0
        pages_processed = 0
        
        try:
            while pages_processed < max_pages:
                url = f"{self.base_url}/sell/inventory/v1/inventory_item"
                params = {
                    'limit': min(limit, 200),  # eBay max is usually 200
                    'offset': offset
                }
                
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('inventoryItems', [])
                    
                    if not items:  # Keine weiteren Items
                        break
                    
                    # Transform items
                    for item in items:
                        sku = item.get('sku', '')
                        product = item.get('product', {})
                        availability = item.get('availability', {})
                        
                        ship_availability = availability.get('shipToLocationAvailability', {})
                        if isinstance(ship_availability, list) and ship_availability:
                            ship_availability = ship_availability[0]
                        
                        # Extract price - handle both dict and list cases
                        current_price = 0.0
                        if isinstance(ship_availability, dict):
                            price_info = ship_availability.get('availabilityDistributions', [])
                            if price_info and isinstance(price_info, list) and len(price_info) > 0:
                                fulfillment_info = price_info[0].get('fulfillmentTime', {}) if isinstance(price_info[0], dict) else {}
                                if isinstance(fulfillment_info, dict):
                                    try:
                                        current_price = float(fulfillment_info.get('value', 0))
                                    except (ValueError, TypeError):
                                        current_price = 0.0
                        
                        all_items.append({
                            'item_id': sku,
                            'title': product.get('title', 'Unbekannter Titel'),
                            'current_price': current_price,
                            'currency': 'EUR',
                            'listing_type': 'FixedPriceItem',
                            'listing_status': 'Active',
                            'best_offer_enabled': True
                        })
                    
                    total_found += len(items)
                    offset += len(items)
                    pages_processed += 1
                    
                    # Wenn weniger Items als Limit zurückgegeben werden, sind wir am Ende
                    if len(items) < limit:
                        break
                        
                elif response.status_code == 204:
                    break  # Keine Inhalte mehr
                else:
                    # Fehler, aber versuche vorhandene Daten zurückzugeben
                    break
            
            return {
                'success': True,
                'message': f'{total_found} Listings gefunden in {pages_processed} Seiten (Inventory API - Paginated)',
                'items': all_items,
                'total': total_found,
                'pages_processed': pages_processed,
                'pagination_complete': pages_processed < max_pages
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Paginated Inventory API Fehler: {str(e)}',
                'items': all_items,
                'total': total_found,
                'pages_processed': pages_processed
            }
    
    def _get_browse_listings(self):
        """
        Alternative: Use Browse API to find seller's own listings
        """
        try:
            # Account API um Seller-Informationen zu bekommen
            account_url = f"{self.base_url}/sell/account/v1/privilege"
            account_response = requests.get(account_url, headers=self.headers, timeout=30)
            
            if account_response.status_code != 200:
                return {
                    'success': False,
                    'message': 'Keine Account-Info verfügbar',
                    'items': []
                }
                
            # Da wir die Browse API von der Sell API aus nicht direkt nutzen können,
            # versuchen wir es mit der Fulfillment API (Orders)
            orders_result = self._get_recent_orders()
            return orders_result
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Browse API Fehler: {str(e)}',
                'items': []
            }
    
    def _get_recent_orders(self):
        """
        Get recent orders to infer active listings
        """
        try:
            url = f"{self.base_url}/sell/fulfillment/v1/order"
            params = {
                'limit': 50,
                'offset': 0
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                items = []
                seen_items = set()
                
                # Extract unique items from orders
                for order in data.get('orders', []):
                    for line_item in order.get('lineItems', []):
                        item_id = line_item.get('legacyItemId', '')
                        if item_id and item_id not in seen_items:
                            seen_items.add(item_id)
                            
                            price_info = line_item.get('total', {})
                            current_price = float(price_info.get('value', 0))
                            
                            items.append({
                                'item_id': item_id,
                                'title': line_item.get('title', 'Unbekannter Titel'),
                                'current_price': current_price,
                                'currency': price_info.get('currency', 'EUR'),
                                'listing_type': 'FixedPriceItem',
                                'listing_status': 'Active',
                                'best_offer_enabled': True
                            })
                
                return {
                    'success': True,
                    'message': f'{len(items)} aktive Listings aus Orders abgeleitet (Fulfillment API)',
                    'items': items,
                    'total': len(items)
                }
            elif response.status_code == 204:
                return {
                    'success': True,
                    'message': 'Keine Orders gefunden für Listing-Ableitung',
                    'items': [],
                    'total': 0
                }
            else:
                return {
                    'success': False,
                    'message': f'Fulfillment API Error {response.status_code}',
                    'items': []
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Fulfillment API Fehler: {str(e)}',
                'items': []
            }
    
    def get_best_offers(self, item_id):
        """
        Get Best Offers for specific item using eBay Sell Negotiation API + fallbacks
        """
        try:
            # Versuch 1: Negotiation API mit Item ID
            negotiation_result = self._get_negotiation_offers(item_id)
            if negotiation_result['success'] and len(negotiation_result['offers']) > 0:
                return negotiation_result
            
            # Versuch 2: Alle Negotiation Offers (ohne Item Filter)
            all_offers_result = self._get_all_negotiation_offers()
            if all_offers_result['success']:
                # Filter nach Item ID
                filtered_offers = [offer for offer in all_offers_result['offers'] 
                                 if offer.get('item_id') == item_id]
                return {
                    'success': True,
                    'message': f'{len(filtered_offers)} Angebote für Item {item_id} gefunden (Negotiation API - gefiltert)',
                    'offers': filtered_offers,
                    'item_id': item_id
                }
            
            # Versuch 3: Legacy Approach über Orders
            orders_result = self._get_offers_from_orders(item_id)
            if orders_result['success']:
                return orders_result
                
            # Wenn nichts gefunden, gebe erstes Ergebnis zurück
            return negotiation_result
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Fehler beim Abrufen der Angebote für Item {item_id}: {str(e)}',
                'offers': []
            }
    
    def _get_negotiation_offers(self, item_id):
        """Original Negotiation API mit Item ID"""
        try:
            url = f"{self.base_url}/sell/negotiation/v1/offer"
            params = {
                'item_id': item_id,
                'status': 'PENDING',
                'limit': 50
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                offers = []
                
                for offer in data.get('offers', []):
                    offers.append({
                        'best_offer_id': offer.get('offerId', ''),
                        'buyer_id': offer.get('buyerId', 'unknown'),
                        'price': float(offer.get('amount', {}).get('value', 0)),
                        'message': offer.get('message', ''),
                        'quantity': int(offer.get('quantity', 1)),
                        'created_time': offer.get('creationDate', ''),
                        'status': offer.get('status', 'PENDING'),
                        'item_id': item_id
                    })
                
                return {
                    'success': True,
                    'message': f'{len(offers)} Angebote für Item {item_id} gefunden (Negotiation API)',
                    'offers': offers,
                    'item_id': item_id
                }
            elif response.status_code == 204:
                return {
                    'success': True,
                    'message': f'Keine Angebote für Item {item_id} gefunden (Negotiation API)',
                    'offers': [],
                    'item_id': item_id
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'message': response.text}
                return {
                    'success': False,
                    'message': f'Negotiation API Error {response.status_code}: {error_data.get("message", "Unknown error")}',
                    'offers': []
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Negotiation API Fehler: {str(e)}',
                'offers': []
            }
    
    def _get_all_negotiation_offers(self):
        """Get all Negotiation Offers ohne Item Filter"""
        try:
            url = f"{self.base_url}/sell/negotiation/v1/offer"
            params = {
                'status': 'PENDING',
                'limit': 50
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                offers = []
                
                for offer in data.get('offers', []):
                    offers.append({
                        'best_offer_id': offer.get('offerId', ''),
                        'buyer_id': offer.get('buyerId', 'unknown'),
                        'price': float(offer.get('amount', {}).get('value', 0)),
                        'message': offer.get('message', ''),
                        'quantity': int(offer.get('quantity', 1)),
                        'created_time': offer.get('creationDate', ''),
                        'status': offer.get('status', 'PENDING'),
                        'item_id': offer.get('itemId', '')
                    })
                
                return {
                    'success': True,
                    'message': f'{len(offers)} Gesamt-Angebote gefunden (Negotiation API)',
                    'offers': offers
                }
            elif response.status_code == 204:
                return {
                    'success': True,
                    'message': 'Keine Angebote gefunden (Negotiation API)',
                    'offers': []
                }
            else:
                return {
                    'success': False,
                    'message': f'Negotiation API Error {response.status_code}',
                    'offers': []
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'All Negotiation API Fehler: {str(e)}',
                'offers': []
            }
    
    def _get_offers_from_orders(self, item_id):
        """Alternative: Extract Best Offers from Orders"""
        try:
            url = f"{self.base_url}/sell/fulfillment/v1/order"
            params = {
                'limit': 50,
                'offset': 0,
                'filter': 'orderfulfillmentstatus:{NOT_STARTED|IN_PROGRESS}'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                offers = []
                
                # Suche nach Best Offer Patterns in Orders
                for order in data.get('orders', []):
                    order_id = order.get('orderId', '')
                    if 'offer' in order_id.lower() or order.get('orderFulfillmentStatus') == 'NOT_STARTED':
                        for line_item in order.get('lineItems', []):
                            if line_item.get('legacyItemId') == item_id:
                                offers.append({
                                    'best_offer_id': order_id,
                                    'buyer_id': order.get('buyer', {}).get('username', 'unknown'),
                                    'price': float(line_item.get('total', {}).get('value', 0)),
                                    'message': '',
                                    'quantity': int(line_item.get('quantity', 1)),
                                    'created_time': order.get('creationDate', ''),
                                    'status': 'PENDING',
                                    'item_id': item_id
                                })
                
                return {
                    'success': True,
                    'message': f'{len(offers)} Angebote für Item {item_id} aus Orders extrahiert',
                    'offers': offers,
                    'item_id': item_id
                }
            else:
                return {
                    'success': False,
                    'message': f'Orders API Error {response.status_code}',
                    'offers': []
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Orders API Fehler: {str(e)}',
                'offers': []
            }
    
    def respond_to_best_offer(self, item_id, offer_id, action, message=None, counter_offer_amount=None):
        """
        Respond to Best Offer using eBay Sell Negotiation API
        """
        try:
            url = f"{self.base_url}/sell/negotiation/v1/offer/{offer_id}/respond"
            
            # Prepare request data
            response_data = {
                'action': action.upper()  # ACCEPT, DECLINE, COUNTER
            }
            
            if message:
                response_data['message'] = message
                
            if action.upper() == 'COUNTER' and counter_offer_amount:
                response_data['counterOffer'] = {
                    'amount': {
                        'value': str(counter_offer_amount),
                        'currency': 'EUR'
                    }
                }
            
            response = requests.post(url, headers=self.headers, json=response_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'message': f'Angebot {offer_id} erfolgreich {action}ed (Sell API)',
                    'offer_id': offer_id,
                    'action': action,
                    'response_data': data
                }
            elif response.status_code == 204:
                # No content but successful
                return {
                    'success': True,
                    'message': f'Angebot {offer_id} erfolgreich {action}ed (Sell API)',
                    'offer_id': offer_id,
                    'action': action
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'message': response.text}
                return {
                    'success': False,
                    'message': f'Negotiation API Error {response.status_code}: {error_data.get("message", "Unknown error")}',
                    'offer_id': offer_id,
                    'action': action
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Fehler beim Antworten auf Angebot {offer_id}: {str(e)}',
                'offer_id': offer_id,
                'action': action
            }

    def get_all_best_offers_direct(self, limit=200, include_counters=True):
        """
        Optimierte Methode: Holt direkt alle Best Offers und Gegenvorschläge 
        ohne zuerst alle Listings abzurufen (viel effizienter für große Inventare)
        """
        try:
            # Direkt alle offenen Angebote abrufen
            url = f"{self.base_url}/sell/negotiation/v1/offer"
            params = {
                'status': 'PENDING,COUNTERED',  # Sowohl neue als auch Gegenvorschläge
                'limit': min(limit, 200)  # eBay Limit beachten
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                offers = []
                
                for offer in data.get('offers', []):
                    offer_status = offer.get('status', 'PENDING')
                    offer_data = {
                        'best_offer_id': offer.get('offerId', ''),
                        'buyer_id': offer.get('buyerId', 'unknown'),
                        'price': float(offer.get('amount', {}).get('value', 0)),
                        'message': offer.get('message', ''),
                        'quantity': int(offer.get('quantity', 1)),
                        'created_time': offer.get('creationDate', ''),
                        'status': offer_status,
                        'item_id': offer.get('itemId', ''),
                        'offer_type': 'counter' if offer_status == 'COUNTERED' else 'initial'
                    }
                    
                    # Zusätzliche Informationen für Gegenvorschläge
                    if offer_status == 'COUNTERED':
                        counter_info = offer.get('counterOffer', {})
                        if counter_info:
                            offer_data['counter_amount'] = float(counter_info.get('amount', {}).get('value', 0))
                            offer_data['counter_message'] = counter_info.get('message', '')
                    
                    offers.append(offer_data)
                
                # Optional: Item-Details zu den Angeboten hinzufügen
                offers_with_details = self._enrich_offers_with_item_details(offers)
                
                return {
                    'success': True,
                    'message': f'{len(offers_with_details)} Best Offers/Gegenvorschläge direkt abgerufen (Optimiert)',
                    'offers': offers_with_details,
                    'total': len(offers_with_details),
                    'method': 'direct_negotiation_api'
                }
                
            elif response.status_code == 204:
                return {
                    'success': True,
                    'message': 'Keine aktiven Best Offers gefunden',
                    'offers': [],
                    'total': 0,
                    'method': 'direct_negotiation_api'
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'message': response.text}
                return {
                    'success': False,
                    'message': f'Negotiation API Error {response.status_code}: {error_data.get("message", "Unknown error")}',
                    'offers': []
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Fehler beim direkten Abruf der Best Offers: {str(e)}',
                'offers': []
            }
    
    def _enrich_offers_with_item_details(self, offers):
        """
        Ergänzt Best Offers mit Item-Details (Titel, Preis) durch gezielte API-Calls
        """
        enriched_offers = []
        item_cache = {}  # Cache für bereits abgerufene Items
        
        for offer in offers:
            item_id = offer.get('item_id', '')
            if not item_id:
                # Offer ohne Item ID - behalten aber markieren
                offer['item_title'] = 'Unbekannter Artikel'
                offer['list_price'] = 0.0
                enriched_offers.append(offer)
                continue
            
            # Prüfe Cache
            if item_id in item_cache:
                item_details = item_cache[item_id]
            else:
                # Item-Details abrufen (effizienter als alle Listings)
                item_details = self._get_single_item_details(item_id)
                item_cache[item_id] = item_details
            
            # Angebot mit Item-Details ergänzen
            offer['item_title'] = item_details.get('title', 'Unbekannter Artikel')
            offer['list_price'] = item_details.get('current_price', 0.0)
            offer['currency'] = item_details.get('currency', 'EUR')
            
            enriched_offers.append(offer)
        
        return enriched_offers
    
    def _get_single_item_details(self, item_id):
        """
        Holt Details für ein einzelnes Item (effizienter als alle Listings)
        """
        try:
            # Versuch 1: Inventory API für spezifisches Item
            url = f"{self.base_url}/sell/inventory/v1/inventory_item/{item_id}"
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                product = data.get('product', {})
                availability = data.get('availability', {})
                
                ship_availability = availability.get('shipToLocationAvailability', {})
                if isinstance(ship_availability, list) and ship_availability:
                    ship_availability = ship_availability[0]
                
                # Preis extrahieren (komplexe Struktur in Sell API)
                current_price = 0.0
                if isinstance(ship_availability, dict):
                    price_info = ship_availability.get('availabilityDistributions', [])
                    if price_info and isinstance(price_info, list) and len(price_info) > 0:
                        fulfillment_info = price_info[0].get('fulfillmentTime', {}) if isinstance(price_info[0], dict) else {}
                        if isinstance(fulfillment_info, dict):
                            try:
                                current_price = float(fulfillment_info.get('value', 0))
                            except (ValueError, TypeError):
                                current_price = 0.0
                
                return {
                    'title': product.get('title', 'Unbekannter Titel'),
                    'current_price': current_price,
                    'currency': 'EUR'
                }
            
            # Versuch 2: Fallback über Browse API (falls Legacy Item ID)
            # Für Legacy Items ist ein anderer Ansatz nötig
            return self._get_legacy_item_details(item_id)
            
        except Exception as e:
            return {
                'title': f'Item {item_id}',
                'current_price': 0.0,
                'currency': 'EUR'
            }
    
    def _get_legacy_item_details(self, item_id):
        """
        Fallback für Legacy Item IDs über Orders oder andere APIs
        """
        try:
            # Suche in bisherigen Orders nach diesem Item
            url = f"{self.base_url}/sell/fulfillment/v1/order"
            params = {
                'limit': 50,
                'offset': 0
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Suche nach Item in Orders
                for order in data.get('orders', []):
                    for line_item in order.get('lineItems', []):
                        if line_item.get('legacyItemId') == item_id:
                            price_info = line_item.get('total', {})
                            return {
                                'title': line_item.get('title', f'Legacy Item {item_id}'),
                                'current_price': float(price_info.get('value', 0)),
                                'currency': price_info.get('currency', 'EUR')
                            }
            
            # Fallback
            return {
                'title': f'Legacy Item {item_id}',
                'current_price': 0.0,
                'currency': 'EUR'
            }
            
        except Exception as e:
            return {
                'title': f'Legacy Item {item_id}',
                'current_price': 0.0,
                'currency': 'EUR'
            }    