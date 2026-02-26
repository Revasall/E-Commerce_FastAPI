from fastapi import APIRouter, Request, Depends, HTTPException
from backend.app.services.order_service import OrderServiceDep
import logging

router = APIRouter(prefix='/webhooks', tags=["Payments"])

@router.post('/yookassa')
async def yookassa_webhook(request: Request,
                           service: OrderServiceDep):
    try:
        data = request.json()
        logging.info(f'Webhook received: {data}')

        if data.get('event') == 'payment.succeeded':
            payment_obj = data.get('object')

            metadata = payment_obj.get('metadata', {})
            order_id = metadata.get('order_id')

            if order_id:
                await service.order_payment_update(
                    order_id=int(order_id),
                    external_id=payment_obj.get('id'),
                    payment_details=payment_obj
                )

                logging.info(f'Order {order_id} marked as PAID')
            
        return {'status':'ok'}
    
    except Exception as e:
        logging.error(f'Webhook error: {str(e)}')

        return {'status': 'error', 'message':str(e)}