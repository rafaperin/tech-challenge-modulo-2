import json
import uuid
import httpx
from fastapi import APIRouter, Request, status

from src.config.errors import APIErrorMessage, RepositoryError, ResourceNotFound, DomainError
from src.controllers.order_controller import OrderController
from src.controllers.product_controller import ProductController
from src.entities.errors.order_item_error import OrderItemError
from src.entities.schemas.order_dto import OrderDTOListResponse, OrderDTOResponse, CreateOrderDTO, CreateOrderItemDTO, \
    UpdateOrderItemDTO, RemoveOrderItemDTO

router = APIRouter()


@router.post("/webhook")
async def webhook_received(request: Request):
    json_req = await request.json()
    params = list(request.query_params.values())

    if params[1] == 'merchant_order':
        url = json_req["resource"]
        headers = {"Authorization": "Bearer APP_USR-2598238696055751-090212-6c7c340484abe79170a7037e08467d22-1467637782"}
        r = httpx.get(url, headers=headers)

        result = json.loads(r.content)
        if result["status"] == "closed":
            order_id = result["external_reference"]
            payment_status = result["payments"][0]["status"]

            try:
                result = await OrderController.confirm_payment(order_id, payment_status)
            except Exception:
                raise RepositoryError.get_operation_failed()

            return result


@router.get(
    "/orders", tags=["Orders"],
    response_model=OrderDTOListResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_all_orders() -> dict:
    try:
        result = await OrderController.get_all_orders()
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/orders/ongoing", tags=["Orders"],
    response_model=OrderDTOListResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def list_ongoing_orders() -> dict:
    try:
        result = await OrderController.list_ongoing_orders()
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/orders/id/{order_id}", tags=["Orders"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_order_by_id(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderController.get_order_by_id(order_id)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No order with id: {order_id}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.post(
    "/orders",  tags=["Orders"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def create_order(
    request: CreateOrderDTO
) -> dict:
    try:
        result = await OrderController.create_order(request)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.post(
    "/orders/{order_id}/items", tags=["Order Items"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def add_order_items(
    request: CreateOrderItemDTO,
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderController.add_order_items(request, order_id)
    except DomainError:
        raise OrderItemError.modification_blocked()
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/orders/{order_id}/items",  tags=["Order Items"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def change_order_item_quantity(
    order_id: uuid.UUID,
    request: UpdateOrderItemDTO
) -> dict:
    try:
        result = await OrderController.change_order_item_quantity(order_id, request)
    except DomainError:
        raise OrderItemError.modification_blocked()
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/orders/{order_id}/checkout", tags=["Orders"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def confirm_order(
    order_id: uuid.UUID
) -> dict:
    try:
        order = await OrderController.get_order_by_id(order_id)

        url = "https://api.mercadopago.com/instore/orders/qr/seller/collectors/1467637782/pos/LOJA001POS001/qrs"
        headers = {
            "Authorization": "Bearer APP_USR-2598238696055751-090212-6c7c340484abe79170a7037e08467d22-1467637782"
        }

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

        params = {
          "external_reference": str(order_id),
          "total_amount": float(order["result"]["orderTotal"]),
          "items": items,
          "title": str(order_id),
          "description": f"Pedido {order_id}",
          "notification_url": "https://lasting-partly-trout.ngrok-free.app/webhook"
        }
        r = httpx.post(url, headers=headers, json=params)
        json_response = json.loads(r.content)

        result = await OrderController.confirm_order(order_id, json_response["qr_data"])
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/orders/{order_id}/in-progress", tags=["Orders"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def order_in_progress(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderController.change_order_status_in_progress(order_id)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/orders/{order_id}/ready", tags=["Orders"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def order_ready(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderController.change_order_status_ready(order_id)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/orders/{order_id}/finalized", tags=["Orders"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def order_finalized(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderController.change_order_status_ready(order_id)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.delete(
    "/orders/{order_id}", tags=["Orders"],
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_order(
    order_id: uuid.UUID
) -> dict:
    try:
        await OrderController.remove_order(order_id)
    except DomainError:
        raise OrderItemError.modification_blocked()
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": "Order removed successfully"}


@router.delete(
    "/orders/{order_id}/items", tags=["Order Items"],
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_order_item(
    order_id: uuid.UUID,
    request: RemoveOrderItemDTO
) -> dict:
    try:
        await OrderController.remove_order_item(order_id, request)
    except DomainError:
        raise OrderItemError.modification_blocked()
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": "Order item removed successfully"}
