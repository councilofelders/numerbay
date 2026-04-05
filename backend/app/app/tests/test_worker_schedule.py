from types import SimpleNamespace

from app import worker


class FakeSender:
    def __init__(self) -> None:
        self.conf = SimpleNamespace(beat_schedule={})
        self.periodic_calls = []

    def add_periodic_task(self, *args, **kwargs) -> None:
        self.periodic_calls.append((args, kwargs))


def test_setup_periodic_tasks_registers_celery_owned_jobs() -> None:
    sender = FakeSender()

    worker.setup_periodic_tasks(sender)

    assert "batch_update_model_scores" in sender.conf.beat_schedule
    assert "update_active_round" in sender.conf.beat_schedule
    assert "batch_prune_storage" in sender.conf.beat_schedule
    assert "batch_send_order_artifact_upload_reminder_emails_1" in sender.conf.beat_schedule
    assert "batch_send_order_artifact_upload_reminder_emails_2" in sender.conf.beat_schedule
    assert len(sender.periodic_calls) == 1


def test_setup_periodic_tasks_skips_gcp_owned_jobs(monkeypatch) -> None:
    sender = FakeSender()

    monkeypatch.setattr(worker.settings, "SCHEDULER_OWNER_GLOBALS_STATS", "gcp")
    monkeypatch.setattr(worker.settings, "SCHEDULER_OWNER_PRUNE_STORAGE", "gcp")
    monkeypatch.setattr(worker.settings, "SCHEDULER_OWNER_ARTIFACT_REMINDERS", "gcp")
    monkeypatch.setattr(worker.settings, "SCHEDULER_OWNER_MODEL_SCORES", "gcp")
    monkeypatch.setattr(worker.settings, "SCHEDULER_OWNER_ACTIVE_ROUND", "gcp")
    monkeypatch.setattr(worker.settings, "ASYNC_OWNER_PAYMENTS", "gcp")

    worker.setup_periodic_tasks(sender)

    assert "batch_update_model_scores" not in sender.conf.beat_schedule
    assert "update_active_round" not in sender.conf.beat_schedule
    assert "update_globals_stats_task" not in sender.conf.beat_schedule
    assert "batch_prune_storage" not in sender.conf.beat_schedule
    assert "batch_send_order_artifact_upload_reminder_emails_1" not in sender.conf.beat_schedule
    assert "batch_send_order_artifact_upload_reminder_emails_2" not in sender.conf.beat_schedule
    assert len(sender.periodic_calls) == 0


def test_update_active_round_forwards_schedule_slot(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(
        worker,
        "run_async_task",
        lambda task_name, args=None, kwargs=None: calls.append(
            (task_name, args, kwargs)
        ),
    )

    worker.update_active_round(schedule_slot="202604050901")

    assert calls == [
        (
            worker.TASK_UPDATE_ACTIVE_ROUND,
            None,
            {"schedule_slot": "202604050901"},
        )
    ]
