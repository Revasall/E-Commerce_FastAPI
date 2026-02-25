import uuid
import asyncio
from yookassa import Configuration, Payment
from backend.app.models.order import Order
from backend.app.config.config import settings

class YookassaProvider:
    def __init__(self):
        Configuration.account_id = settings.ecommerce.ACCOUNT_ID
        Configuration.secret_key = settings.ecommerce.SECRET_KEY

    async def create_payment_link(self, order: Order) -> tuple[str]:
        '''
        Create sessionf of payment and return URL for redirect
        '''

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

        loop = asyncio.get_running_loop()
        payment = await loop.run_in_executor(
            None,
            lambda: Payment.create(payment_data, idempotency_key)
        )

        return payment.confirmation.confirmation_url, payment.id