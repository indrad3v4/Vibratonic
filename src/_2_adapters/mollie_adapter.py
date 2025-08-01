import os
from typing import Dict, Optional
from datetime import datetime, timedelta

class MollieAdapter:
    def __init__(self):
        self.api_key = os.getenv("MOLLIE_API_KEY", "test_api_key")
        self.base_url = "https://api.mollie.com/v2"
        
        # Mock payment storage for demo purposes
        self._mock_payments = {}
    
    def create_payment(self, payment_data: Dict) -> Dict:
        """Create a payment through Mollie API"""
        # In production, this would make an actual API call to Mollie
        # For demo purposes, we'll simulate the response
        
        payment_id = f"tr_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        mock_payment = {
            "id": payment_id,
            "status": "open",
            "amount": {
                "value": f"{payment_data['amount']:.2f}",
                "currency": "EUR"
            },
            "description": payment_data.get("description", "MVP Funding"),
            "checkout_url": f"https://www.mollie.com/checkout/select-method/{payment_id}",
            "redirect_url": payment_data.get("redirect_url"),
            "webhook_url": payment_data.get("webhook_url"),
            "metadata": {
                "mvp_id": payment_data.get("mvp_id"),
                "backer_id": payment_data.get("backer_id"),
                "platform_fee": payment_data.get("platform_fee", 0.0),
                "creator_amount": payment_data.get("creator_amount", 0.0)
            },
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(minutes=15)).isoformat()
        }
        
        self._mock_payments[payment_id] = mock_payment
        return mock_payment
    
    def get_payment_status(self, payment_id: str) -> Dict:
        """Get payment status from Mollie API"""
        # In production, this would make an actual API call to Mollie
        # For demo purposes, we'll return mock data
        
        payment = self._mock_payments.get(payment_id)
        if not payment:
            return {"error": "Payment not found"}
        
        # Simulate payment progression
        created_time = datetime.fromisoformat(payment["created_at"].replace('Z', '+00:00').replace('+00:00', ''))
        time_elapsed = datetime.now() - created_time
        
        if time_elapsed.total_seconds() > 300:  # 5 minutes
            payment["status"] = "paid"
            payment["paid_at"] = datetime.now().isoformat()
        elif time_elapsed.total_seconds() > 60:  # 1 minute
            payment["status"] = "pending"
        
        return payment
    
    def get_payment_methods(self) -> list:
        """Get available payment methods"""
        return [
            {
                "id": "ideal",
                "description": "iDEAL",
                "image": {"size1x": "https://www.mollie.com/external/icons/payment-methods/ideal.png"}
            },
            {
                "id": "creditcard",
                "description": "Credit card",
                "image": {"size1x": "https://www.mollie.com/external/icons/payment-methods/creditcard.png"}
            },
            {
                "id": "paypal",
                "description": "PayPal",
                "image": {"size1x": "https://www.mollie.com/external/icons/payment-methods/paypal.png"}
            },
            {
                "id": "banktransfer",
                "description": "Bank transfer",
                "image": {"size1x": "https://www.mollie.com/external/icons/payment-methods/banktransfer.png"}
            }
        ]
    
    def refund_payment(self, payment_id: str, amount: Optional[float] = None) -> Dict:
        """Create a refund for a payment"""
        payment = self._mock_payments.get(payment_id)
        if not payment or payment["status"] != "paid":
            return {"error": "Cannot refund this payment"}
        
        refund_id = f"re_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        refund_amount = amount or float(payment["amount"]["value"])
        
        refund = {
            "id": refund_id,
            "payment_id": payment_id,
            "amount": {
                "value": f"{refund_amount:.2f}",
                "currency": "EUR"
            },
            "status": "processing",
            "created_at": datetime.now().isoformat()
        }
        
        return refund
