"""Direct-run entrypoints for scheduled jobs."""

import argparse
from typing import Callable, Dict, Iterable, Optional

from app.worker import (
    batch_prune_storage,
    batch_update_payments_task,
    batch_update_polls,
    batch_update_product_sales_stats,
    batch_update_stake_snapshots,
    update_globals_stats_task,
)

JobRunner = Callable[[], None]


JOB_RUNNERS: Dict[str, JobRunner] = {
    "globals-stats": update_globals_stats_task,
    "polls": batch_update_polls,
    "product-sales-stats": batch_update_product_sales_stats,
    "prune-storage": batch_prune_storage,
    "reconcile-payments": batch_update_payments_task,
    "stake-snapshots": batch_update_stake_snapshots,
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
