from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.tick": "main-queue",
    "app.worker.update_model_subtask": "beat-queue",
    # "app.worker.commit_models_subtask": "beat-queue",
    "app.worker.batch_update_models_task": "beat-queue",
}
