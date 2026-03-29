from app.ops import jobs


def test_list_jobs_includes_phase_one_families() -> None:
    assert list(jobs.list_jobs()) == [
        "artifact-reminders",
        "globals-stats",
        "polls",
        "product-sales-stats",
        "prune-storage",
        "stake-snapshots",
    ]


def test_run_job_invokes_runner(monkeypatch) -> None:
    called = []

    monkeypatch.setitem(jobs.JOB_RUNNERS, "test-job", lambda: called.append(True))

    jobs.run_job("test-job")

    assert called == [True]
