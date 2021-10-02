from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.tick": "main-queue",
    "app.worker.send_email_task": "main-queue",
    "app.worker.update_model_subtask": "beat-queue",
    # "app.worker.commit_models_subtask": "beat-queue",
    "app.worker.batch_update_models_task": "beat-queue",
    "app.worker.update_globals_task": "beat-queue",  # todo deprecate old global update to new rollover
    "app.worker.update_active_round": "beat-queue",
    "app.worker.update_round_rollover": "beat-queue",
    "app.worker.update_payment_subtask": "beat-queue",
    "app.worker.batch_update_payments_task": "beat-queue",
    "app.worker.upload_numerai_artifact_task": "beat-queue",
    "app.worker.submit_numerai_model_subtask": "beat-queue",
    "app.worker.batch_submit_numerai_models_task": "beat-queue",
}
