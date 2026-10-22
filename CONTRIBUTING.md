# How to contribute
This project uses [FastAPI](https://fastapi.tiangolo.com/) for backend, and [Vue Storefront](https://docs.vuestorefront.io/v2/) (API middleware and composables) + [Bootstrap 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/) (theme) for frontend.

Questions about contributing? Please post in the #numerbay channel in [Numerai Discord Server](https://discord.gg/numerai).

## Did you find a bug?

If you discover bugs, other issues or ideas for enhancements, do not hesitate to make a Github issue. Describe the background on the issue. Add screenshots or any error message you see if this is relevant for solving the issue. Also, please add appropriate labels for the Github issue.

* Ensure the bug was not already reported by searching on GitHub under Issues.
* If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.
* Be sure to add the complete error messages.

#### Did you write a patch that fixes a bug?

* Open a new GitHub pull request with the patch.
* Ensure that your PR includes a test that fails without your patch, and pass with it.
* Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

## PR submission guidelines

* Keep each PR focused. While it's more convenient, do not combine several unrelated fixes together. Create as many branches as needing to keep each PR focused.
* Do not mix style changes/fixes with "functional" changes. It's very difficult to review such PRs and it most likely get rejected.
* Do not add/remove vertical whitespace. Preserve the original style of the file you edit as much as you can.
* Do not turn an already submitted PR into your development playground. If after you submitted PR, you discovered that more work is needed - close the PR, do the required work and then submit a new PR. Otherwise each of your commits requires attention from maintainers of the project.
* If, however, you submitted a PR and received a request for changes, you should proceed with commits inside that PR, so that the maintainer can see the incremental fixes and won't need to review the whole PR again. In the exception case where you realize it'll take many many commits to complete the requests, then it's probably best to close the PR, do the work and then submit it again. Use common sense where you'd choose one way over another.


# Development Guide
## Backend Requirements

* [uv](https://docs.astral.sh/uv/), which installs Python 3.11 and the locked dependencies.
* PostgreSQL 17.

## Backend local development

* Run a project-local PostgreSQL cluster in `.dev/` (ignored by git), from the repository root:

```bash
PGBIN=/usr/lib/postgresql/17/bin  # Debian/Ubuntu path
$PGBIN/initdb -D .dev/pgdata -U postgres --auth=trust
cat >> .dev/pgdata/postgresql.conf <<'EOF'
port = 54320
listen_addresses = '127.0.0.1'
unix_socket_directories = ''
timezone = 'UTC'
EOF
$PGBIN/pg_ctl -D .dev/pgdata -l .dev/postgres.log start
psql -h 127.0.0.1 -p 54320 -U postgres -c "create database app"
psql -h 127.0.0.1 -p 54320 -U postgres -c "create database app_test"
```

Stop it with `$PGBIN/pg_ctl -D .dev/pgdata stop`, and start it again with the `pg_ctl` start line above.

* Configure the backend, bootstrap the database and start the API with live reload:

```bash
cp .env.example .env
echo "PGPORT=54320" >> .env
cd backend/app
uv sync
uv run --env-file ../../.env bash bootstrap-db.sh
uv run --env-file ../../.env uvicorn app.main:app --reload --port 8000
```

`bootstrap-db.sh` applies the migrations and seeds the superuser and categories.

* Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI: http://localhost:8000/backend-api/v1/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8000/docs

Some features still depend on GCP or live services and don't work locally: endpoints that enqueue background tasks (they are dispatched to Cloud Tasks), artifact upload and download URLs (signed with GCP credentials), and anything driven by the Numerai round schedule, which comes from the live Numerai API.

### Backend tests

Bootstrap the `app_test` database once, then run the tests against it, from `backend/app`:

```bash
POSTGRES_DB=app_test uv run --env-file ../../.env bash bootstrap-db.sh
POSTGRES_DB=app_test uv run --env-file ../../.env bash tests-start.sh
```

`tests-start.sh` runs `scripts/lint.sh`, then `pytest`; extra arguments are passed to `pytest`. Tests that call Google Cloud Storage need `GOOGLE_APPLICATION_CREDENTIALS` with access to the `storage.test.numerbay.ai` bucket. Without it they fail, and so do some tests that run after them.

### Migrations

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

Run these commands from `backend/app`.

* If you created a new model in `./backend/app/app/models/`, make sure to import it in `./backend/app/app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic.

* After changing a model (for example, adding a column), create a revision, e.g.:

```console
$ uv run --env-file ../../.env alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ uv run --env-file ../../.env alembic upgrade head
```

If you don't want to start with the default models and want to remove them / modify them, from the beginning, without having any previous revision, you can remove the revision files (`.py` Python files) under `./backend/app/alembic/versions/`. And then create a first migration as described above.

## Continuous Integration / Continuous Delivery

This repository currently has the following GitHub Actions set up:

* `Run tests` automatically runs tests for every push to the `master` branch
* `Deploy Staging` builds and deploys the `master` branch to the staging environment (stag.numerbay.ai), requires manual trigger. (Not recommended, as the deployment server may have limited capacity.)
* `Deploy Production` automatically builds and deploys the `production` branch to the live environment (numerbay.ai) for every push to the `production` branch


## URLs

These are the URLs that will be used and generated by the project.

### Production URLs

Production URLs, from the branch `production`.

Frontend: https://numerbay.ai

Backend: https://numerbay.ai/api/

Automatic Interactive Docs (Swagger UI): https://numerbay.ai/docs

Automatic Alternative Docs (ReDoc): https://numerbay.ai/redoc

Flower: https://flower.numerbay.ai

### Staging URLs

Staging URLs, from the branch `master`.

Frontend: https://stag.numerbay.ai

Backend: https://stag.numerbay.ai/api/

Automatic Interactive Docs (Swagger UI): https://stag.numerbay.ai/docs

Automatic Alternative Docs (ReDoc): https://stag.numerbay.ai/redoc

Flower: https://flower.stag.numerbay.ai
