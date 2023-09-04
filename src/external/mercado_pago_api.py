import json

import httpx

from src.config.errors import RepositoryError
from src.controllers.order_controller import OrderController
from src.controllers.product_controller import ProductController
from src.config.config import settings


class MercadoPagoAPI:
    @staticmethod
    async def create_order_on_mercado_pago(order: dict):
        user_id = settings.MERCADO_PAGO_USER_ID
        external_pos_id = settings.MERCADO_PAGO_EXTERNAL_POS_ID
        access_token = settings.MERCADO_PAGO_ACCESS_TOKEN
        webhook_base_url = settings.WEBHOOK_BASE_URL
        api_url = f"https://api.mercadopago.com/instore/orders/qr/seller/collectors/{user_id}/pos/{external_pos_id}/qrs"

        items = []
        for item in order["result"]["orderItems"]:
            product = await ProductController.get_product_by_id(item["productId"])
            order_item = {
                "sku_number": str(product["productId"]),
                "category": product["category"],
                "title": product["name"],
                "description": product["description"],
                "unit_price": float(product["price"]),
                "quantity": item["productQuantity"],
                "unit_measure": "unit",
                "total_amount": float(product["price"] * item["productQuantity"])
            }
            items.append(order_item)

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        params = {
            "external_reference": str(order["result"]["orderId"]),
            "total_amount": float(order["result"]["orderTotal"]),
            "items": items,
            "title": str(order["result"]["orderId"]),
            "description": f"Pedido {order['result']['orderId']}",
            "notification_url": f"{webhook_base_url}/webhook"
        }

        r = httpx.post(api_url, headers=headers, json=params)
        json_response = json.loads(r.content)

        return json_response["qr_data"]

    @staticmethod
    async def check_payment_approval(json_req: dict, params: list):
        if params[1] == 'merchant_order':
            url = json_req["resource"]
            headers = {
                "Authorization": "Bearer APP_USR-2598238696055751-090212-6c7c340484abe79170a7037e08467d22-1467637782"}
            r = httpx.get(url, headers=headers)

            result = json.loads(r.content)
            if result["status"] == "closed":
                order_id = result["external_reference"]
                payment_status = result["payments"][0]["status"]

                try:
                    await OrderController.confirm_payment(order_id, payment_status)
                except Exception:
                    raise RepositoryError.get_operation_failed()
