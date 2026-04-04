from datetime import datetime
from types import SimpleNamespace

from app.api.api_v1.endpoints import orders as orders_endpoint
from app.api.dependencies import orders


def test_on_order_confirmed_dispatches_legacy_side_effects(monkeypatch) -> None:
    order_obj = SimpleNamespace(
        id=7,
        transaction_hash=None,
        state="pending",
        price=5,
        submit_model_id="model-1",
        product_id=9,
        buyer=SimpleNamespace(
            numerai_api_key_public_id="public-id",
            numerai_api_key_secret="secret-key",
        ),
        product=SimpleNamespace(
            total_num_sales=1,
            last_sale_price=3,
            model=SimpleNamespace(tournament=8),
        ),
    )
    calls = []

    monkeypatch.setattr(
        orders.crud.order,
        "update",
        lambda *args, **kwargs: calls.append(("order.update", kwargs["obj_in"])),
    )
    monkeypatch.setattr(
        orders,
        "create_coupon_for_order",
        lambda *args, **kwargs: calls.append(("coupon.create", None)),
    )
    monkeypatch.setattr(
        orders.crud.product,
        "update",
        lambda *args, **kwargs: calls.append(("product.update", kwargs["obj_in"])),
    )
    monkeypatch.setattr(
        orders.crud.globals,
        "update_singleton",
        lambda *_args, **_kwargs: SimpleNamespace(active_round=10, selling_round=10),
    )
    monkeypatch.setattr(
        orders.crud.artifact,
        "get_multi_by_product_round",
        lambda *_args, **_kwargs: [SimpleNamespace(object_name="artifact.csv")],
    )

    class FakeBlob:
        def exists(self) -> bool:
            return True

    class FakeBucket:
        def blob(self, _name):
            return FakeBlob()

    monkeypatch.setattr(orders.deps, "get_gcs_bucket", lambda: FakeBucket())
    monkeypatch.setattr(
        orders,
        "enqueue_upload_numerai_artifact",
        lambda **kwargs: calls.append(("upload.enqueue", kwargs)),
    )
    monkeypatch.setattr(
        orders,
        "enqueue_trigger_webhook_for_product",
        lambda *args: calls.append(("webhook.enqueue", args)),
    )
    monkeypatch.setattr(
        orders,
        "send_order_confirmation_emails",
        lambda order: calls.append(("emails.send", order.id)),
    )

    orders.on_order_confirmed(
        db=SimpleNamespace(), order_obj=order_obj, transaction="0xabc"
    )

    assert (
        "order.update",
        {"transaction_hash": "0xabc", "state": "confirmed"},
    ) in calls
    assert ("coupon.create", None) in calls
    assert any(call[0] == "product.update" for call in calls)
    assert any(call[0] == "upload.enqueue" for call in calls)
    assert ("webhook.enqueue", (9, 7)) in calls
    assert ("emails.send", 7) in calls


def test_update_payment_confirms_manual_transaction(monkeypatch) -> None:
    order_obj = SimpleNamespace(
        id=11,
        state="pending",
        transaction_hash="0xconfirmed",
        currency="NMR",
        price=1,
        date_order=datetime.utcnow(),
    )
    calls = []

    monkeypatch.setattr(orders.crud.order, "get", lambda *_args, **_kwargs: order_obj)
    monkeypatch.setattr(
        orders, "match_transaction_for_order", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(
        orders,
        "on_order_confirmed",
        lambda db, order, transaction=None: calls.append((db, order.id, transaction)),
    )

    db = SimpleNamespace()

    orders.update_payment(db, 11)

    assert calls == [(db, 11, "0xconfirmed")]


def test_create_order_ignores_new_order_email_failures(monkeypatch) -> None:
    current_user = SimpleNamespace(
        id=1,
        email="buyer@example.com",
        username="buyer",
        is_superuser=False,
        public_key=None,
        public_key_v2=None,
        numerai_wallet_address="0xbuyer",
        numerai_api_key_can_upload_submission=True,
        numerai_api_key_can_stake=False,
        models=[],
    )
    product = SimpleNamespace(
        id=101,
        sku="PRODUCT-1",
        owner_id=2,
        owner=SimpleNamespace(
            default_receiving_wallet_address="0xseller",
            numerai_wallet_address="0xseller",
        ),
        category=SimpleNamespace(is_per_round=True),
        use_encryption=False,
        is_active=True,
        is_daily=True,
        round_lock=None,
        model=None,
    )
    product_option = SimpleNamespace(
        id=201,
        product_id=101,
        is_on_platform=True,
        currency="NMR",
        mode="file",
        stake_limit=None,
        chain="ethereum",
        wallet=None,
    )
    calculated_option = SimpleNamespace(
        price=2,
        special_price=2,
        applied_coupon=False,
        coupon=False,
        coupon_specs=None,
    )
    created_order = SimpleNamespace(
        id=301,
        round_order=340,
        date_order=datetime.utcnow(),
        from_address="0xbuyer",
        to_address="0xseller",
        price=2,
        currency="NMR",
    )

    monkeypatch.setattr(
        orders_endpoint, "validate_existing_product", lambda *_args, **_kwargs: product
    )
    monkeypatch.setattr(
        orders_endpoint,
        "validate_existing_product_option",
        lambda *_args, **_kwargs: product_option,
    )
    monkeypatch.setattr(
        orders_endpoint, "any_weekday_round", lambda *_args, **_kwargs: False
    )
    monkeypatch.setattr(
        orders_endpoint,
        "validate_not_during_rollover",
        lambda *_args, **_kwargs: SimpleNamespace(selling_round=340),
    )
    monkeypatch.setattr(orders_endpoint, "valid_rounds", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(
        orders_endpoint.crud.order,
        "search",
        lambda *_args, **_kwargs: {"data": []},
    )
    monkeypatch.setattr(
        orders_endpoint.numerai,
        "check_user_numerai_api",
        lambda *_args, **_kwargs: None,
    )
    monkeypatch.setattr(
        orders_endpoint.crud.coupon, "get_by_code", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(
        orders_endpoint.schemas.ProductOption,
        "from_orm",
        lambda _obj: calculated_option,
    )
    monkeypatch.setattr(
        orders_endpoint,
        "calculate_option_price",
        lambda *_args, **_kwargs: calculated_option,
    )
    monkeypatch.setattr(
        orders_endpoint.crud.order,
        "create_with_buyer",
        lambda *_args, **_kwargs: created_order,
    )
    monkeypatch.setattr(
        orders_endpoint,
        "send_new_order_email",
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
    )

    order = orders_endpoint.create_order(
        db=SimpleNamespace(),
        id=101,
        option_id=201,
        rounds=[340],
        submit_model_id=None,
        coupon=None,
        current_user=current_user,
    )

    assert order is created_order
