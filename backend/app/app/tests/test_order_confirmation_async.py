from types import SimpleNamespace

from app.api.dependencies import orders


def test_schedule_initial_payment_update_is_best_effort(monkeypatch) -> None:
    order_obj = SimpleNamespace(id=42, currency="NMR")
    fallback_calls = []

    monkeypatch.setattr(orders.settings, "ASYNC_OWNER_PAYMENTS", "gcp")

    def raise_enqueue(order_id):
        raise RuntimeError(f"boom-{order_id}")

    monkeypatch.setattr(orders, "enqueue_update_payment", raise_enqueue)
    monkeypatch.setattr(
        orders.celery_app,
        "send_task",
        lambda name, **kwargs: fallback_calls.append((name, kwargs)),
    )

    orders.schedule_initial_payment_update(order_obj)

    assert fallback_calls == [
        (
            "app.worker.update_payment_subtask",
            {
                "args": [42],
                "countdown": orders.settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS,
            },
        )
    ]


def test_on_order_confirmed_skips_repeat_mutations(monkeypatch) -> None:
    order_obj = SimpleNamespace(
        id=7,
        state="confirmed",
        transaction_hash="0xabc",
        product=SimpleNamespace(total_num_sales=1, last_sale_price=1),
    )
    calls = []
    db_calls = []

    monkeypatch.setattr(
        orders,
        "dispatch_order_confirmation_side_effects",
        lambda *args, **kwargs: calls.append("dispatch"),
    )

    class FakeDB:
        def add(self, obj):
            db_calls.append(("add", obj))

        def flush(self):
            db_calls.append(("flush", None))

        def commit(self):
            db_calls.append(("commit", None))

        def refresh(self, obj):
            db_calls.append(("refresh", obj))

    db = FakeDB()

    orders.on_order_confirmed(db, order_obj, "0xabc")

    assert calls == ["dispatch"]


def test_dispatch_order_confirmation_side_effects_skips_completed_markers(
    monkeypatch,
) -> None:
    order_obj = SimpleNamespace(
        id=17,
        props={
            orders.ORDER_CONFIRMATION_SIDE_EFFECTS_KEY: {
                orders.ORDER_CONFIRMATION_UPLOAD_ENQUEUED_KEY: True,
                orders.ORDER_CONFIRMATION_WEBHOOK_ENQUEUED_KEY: True,
                orders.ORDER_CONFIRMATION_EMAILS_SENT_KEY: True,
            }
        },
        submit_model_id=None,
        submit_state=None,
        product_id=5,
    )
    calls = []
    db_calls = []

    monkeypatch.setattr(
        orders,
        "get_order_confirmation_round_state",
        lambda *_args, **_kwargs: {"selling_round": 1, "active_round": 1},
    )
    monkeypatch.setattr(
        orders,
        "enqueue_upload_numerai_artifact",
        lambda *args, **kwargs: calls.append(("upload", args, kwargs)),
    )
    monkeypatch.setattr(
        orders,
        "enqueue_trigger_webhook_for_product",
        lambda *args, **kwargs: calls.append(("webhook", args, kwargs)),
    )
    monkeypatch.setattr(
        orders,
        "send_order_confirmation_emails",
        lambda *args, **kwargs: calls.append(("email", args, kwargs)),
    )

    class FakeDB:
        def commit(self):
            db_calls.append(("commit", None))

        def refresh(self, obj):
            db_calls.append(("refresh", obj))

    db = FakeDB()

    orders.dispatch_order_confirmation_side_effects(db, order_obj)

    assert calls == []
    assert ("commit", None) in db_calls
    assert ("refresh", order_obj) in db_calls


def test_clear_order_confirmation_side_effect_complete(monkeypatch) -> None:
    order_obj = SimpleNamespace(
        props={
            orders.ORDER_CONFIRMATION_SIDE_EFFECTS_KEY: {
                orders.ORDER_CONFIRMATION_UPLOAD_ENQUEUED_KEY: True,
                orders.ORDER_CONFIRMATION_WEBHOOK_ENQUEUED_KEY: True,
            }
        }
    )
    db_calls = []

    class FakeDB:
        def add(self, obj):
            db_calls.append(("add", obj))

        def flush(self):
            db_calls.append(("flush", None))

    db = FakeDB()

    orders.clear_order_confirmation_side_effect_complete(
        db,
        order_obj,
        orders.ORDER_CONFIRMATION_UPLOAD_ENQUEUED_KEY,
    )

    assert order_obj.props == {
        orders.ORDER_CONFIRMATION_SIDE_EFFECTS_KEY: {
            orders.ORDER_CONFIRMATION_WEBHOOK_ENQUEUED_KEY: True
        }
    }
    assert ("add", order_obj) in db_calls
    assert ("flush", None) in db_calls


def test_update_payment_retries_confirmed_orders(monkeypatch) -> None:
    order_obj = SimpleNamespace(
        id=11,
        state="confirmed",
        transaction_hash="0xconfirmed",
        currency="NMR",
    )
    calls = []

    class FakeQuery:
        def filter(self, *_args, **_kwargs):
            return self

        def with_for_update(self):
            return self

        def first(self):
            return order_obj

    class FakeDB:
        def query(self, *_args, **_kwargs):
            return FakeQuery()

    monkeypatch.setattr(
        orders,
        "on_order_confirmed",
        lambda db, order, transaction=None: calls.append(
            (db, order.id, transaction)
        ),
    )

    db = FakeDB()

    orders.update_payment(db, 11)

    assert calls == [(db, 11, "0xconfirmed")]
