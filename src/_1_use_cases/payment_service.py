from typing import Dict, Optional
from datetime import datetime
from src._2_adapters.mollie_adapter import MollieAdapter

class PaymentService:
    def __init__(self):
        self.mollie_adapter = MollieAdapter()
        self.platform_fee_rate = 0.20  # 20% platform fee
    
    def create_payment(self, amount: float, description: str, mvp_id: str, backer_id: str) -> Dict:
        """Create a payment for MVP funding"""
        platform_fee = amount * self.platform_fee_rate
        creator_amount = amount - platform_fee
        
        payment_data = {
            "amount": amount,
            "description": description,
            "mvp_id": mvp_id,
            "backer_id": backer_id,
            "platform_fee": platform_fee,
            "creator_amount": creator_amount,
            "redirect_url": "https://vibratonic.app/payment/success",
            "webhook_url": "https://vibratonic.app/webhook/mollie"
        }
        
        # Create payment through Mollie
        mollie_payment = self.mollie_adapter.create_payment(payment_data)
        
        return {
            "payment_id": mollie_payment.get("id"),
            "checkout_url": mollie_payment.get("checkout_url"),
            "status": mollie_payment.get("status"),
            "amount": amount,
            "platform_fee": platform_fee,
            "creator_amount": creator_amount,
            "created_at": datetime.now().isoformat()
        }
    
    def get_payment_status(self, payment_id: str) -> Dict:
        """Get payment status from Mollie"""
        return self.mollie_adapter.get_payment_status(payment_id)
    
    def handle_webhook(self, payment_id: str) -> Dict:
        """Handle Mollie webhook for payment updates"""
        payment_status = self.get_payment_status(payment_id)
        
        # Process payment completion
        if payment_status.get("status") == "paid":
            # Update MVP funding
            # Send notifications
            # Update user balances
            pass
        
        return payment_status
    
    def calculate_fees(self, amount: float) -> Dict[str, float]:
        """Calculate platform and processing fees"""
        platform_fee = amount * self.platform_fee_rate
        creator_amount = amount - platform_fee
        
        return {
            "amount": amount,
            "platform_fee": platform_fee,
            "creator_amount": creator_amount,
            "fee_percentage": self.platform_fee_rate * 100
        }
