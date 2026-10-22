"""Direct-run entrypoints for scheduled jobs."""

import argparse
from functools import partial
from typing import Callable, Dict, Iterable, Optional

from app.core.async_tasks import (
    TASK_BATCH_UPDATE_PAYMENTS,
    TASK_BATCH_UPDATE_POLLS,
    TASK_BATCH_UPDATE_PRODUCT_SALES_STATS,
    TASK_BATCH_UPDATE_STAKE_SNAPSHOTS,
    TASK_BATCH_PRUNE_STORAGE,
    TASK_SEND_ORDER_ARTIFACT_UPLOAD_REMINDER_EMAILS,
    TASK_UPDATE_GLOBALS_STATS,
    run_async_task,
)

JobRunner = Callable[[], None]


JOB_RUNNERS: Dict[str, JobRunner] = {
    "artifact-reminders": partial(
        run_async_task, TASK_SEND_ORDER_ARTIFACT_UPLOAD_REMINDER_EMAILS
    ),
    "globals-stats": partial(run_async_task, TASK_UPDATE_GLOBALS_STATS),
    "polls": partial(run_async_task, TASK_BATCH_UPDATE_POLLS),
    "product-sales-stats": partial(
        run_async_task, TASK_BATCH_UPDATE_PRODUCT_SALES_STATS
    ),
    "prune-storage": partial(run_async_task, TASK_BATCH_PRUNE_STORAGE),
    "reconcile-payments": partial(run_async_task, TASK_BATCH_UPDATE_PAYMENTS),
    "stake-snapshots": partial(run_async_task, TASK_BATCH_UPDATE_STAKE_SNAPSHOTS),
}


def list_jobs() -> Iterable[str]:
    """Return the supported direct-run job names."""

    return sorted(JOB_RUNNERS.keys())


def run_job(job_name: str) -> None:
    """Execute the requested direct-run job."""

    try:
        runner = JOB_RUNNERS[job_name]
    except KeyError as exc:
        available = ", ".join(list_jobs())
        raise ValueError(
            f"unknown job '{job_name}'. available jobs: {available}"
        ) from exc

    runner()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser for scheduled job operations."""

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="run a scheduled job once")
    run_parser.add_argument("job_name", choices=list_jobs())

    subparsers.add_parser("list", help="list supported scheduled jobs")
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    """CLI entrypoint for direct-run jobs."""

    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command == "list":
        for job_name in list_jobs():
            print(job_name)
        return 0

    if args.command == "run":
        run_job(args.job_name)
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
