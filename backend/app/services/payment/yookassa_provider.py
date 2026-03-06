import uuid
import asyncio
from yookassa import Configuration, Payment
from ...models.order import Order
from ...config.config import settings

class YookassaProvider:
    """
    Integration provider for Yookassa payment gateway.
    Handles payment session creation and configuration using the official SDK.
    """

    def __init__(self):
        # Initialize credentials from application settings
        Configuration.account_id = settings.ecommerce.ACCOUNT_ID
        Configuration.secret_key = settings.ecommerce.SECRET_KEY

    async def create_payment_link(self, order: Order) -> tuple[str]:
        """
        Registers a payment in Yookassa and generates a checkout URL.
        
        Args:
            order: The Order model instance containing total price and ID.
            
        Returns:
            tuple: (confirmation_url, payment_id)
            
        Note:
            Uses thread executor to run synchronous SDK calls in an async environment.
        """

        idempotency_key = str(uuid.uuid4())

        payment_data = {
            'amount': {
                'value': f'{order.total_price:.2f}',
                'currency': f'{settings.ecommerce.PAYMENT_CURRENCY}',
            },
            
            'confirmation':{
                'type': 'redirect',
                'return_url': f'{settings.ecommerce.RETURN_URL}'
            },

            'capture' : True,
            'description': f'Payment for the order №{order.id}',
            'metadata': {
                'order_id': order.id
            }
        }

        # SDK is synchronous, so we offload it to a thread to avoid blocking the event loop
        loop = asyncio.get_running_loop()
        payment = await loop.run_in_executor(
            None,
            lambda: Payment.create(payment_data, idempotency_key)
        )

        return payment.confirmation.confirmation_url, payment.id