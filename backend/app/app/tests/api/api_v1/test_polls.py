import copy
import datetime

import numpy as np
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.tests.utils.poll import create_random_poll
from app.tests.utils.user import authentication_token_from_username, create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_poll(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    poll_id = random_lower_string()
    data = {
        "id": poll_id,
        "topic": "Description",
        "description": "Description",
        "date_finish": "2032-12-31",
        "is_multiple": True,
        "max_options": 2,
        "is_anonymous": True,
        "is_blind": True,
        "weight_mode": "equal",
        "options": [
            {"value": 0, "text": "Python"},
            {"value": 1, "text": "R"},
            {"value": 2, "text": "Java"},
        ],
    }

    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == data["id"]
    assert content["topic"] == data["topic"]
    assert content["options"][0]["text"] == data["options"][0]["text"]  # type: ignore

    crud.poll.remove(db, id=content["id"])


def test_create_poll_invalid_inputs(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    poll_id = random_lower_string()
    base_data = {
        "id": poll_id,
        "topic": "Description",
        "description": "Description",
        "date_finish": "2022-12-31",
        "is_multiple": True,
        "max_options": 2,
        "is_anonymous": True,
        "is_blind": True,
        "weight_mode": "equal",
        "options": [
            {"value": 0, "text": "Python"},
            {"value": 1, "text": "R"},
            {"value": 2, "text": "Java"},
        ],
    }

    # invalid id
    data = copy.deepcopy(base_data)
    data["id"] = "~#123,."
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Invalid id (should only contain alphabetic characters, numbers, dashes or underscores)"
    )

    # duplicate poll id
    existing_poll = create_random_poll(db, owner_id=current_user["id"])
    data = copy.deepcopy(base_data)
    data["id"] = existing_poll.id
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Poll with this id already exists"
    crud.poll.remove(db, id=existing_poll.id)  # type: ignore

    # blind post determination
    data = copy.deepcopy(base_data)
    data["is_blind"] = False
    data["is_stake_predetermined"] = False  # type: ignore

    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Post stake determination is only available for blind polls"
    )

    # negative max_option
    data = copy.deepcopy(base_data)
    data["max_options"] = -10
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Max options setting must be at least 1"

    # no max_options for single selection poll
    data = copy.deepcopy(base_data)
    data["is_multiple"] = False
    data["max_options"] = 2
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Max options setting is not available for single selection polls"
    )

    # valid weight mode
    data = copy.deepcopy(base_data)
    data["weight_mode"] = "invalid_mode"
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid weight mode"

    # valid stake basis round
    data = copy.deepcopy(base_data)
    data["stake_basis_round"] = 128
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "stake_basis_round must be between 293 and current active round"
    )

    # valid min stake
    data = copy.deepcopy(base_data)
    data["min_stake"] = -0.1
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Min stake threshold must be positive"

    # valid min rounds
    data = copy.deepcopy(base_data)
    data["min_rounds"] = 12
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "Min rounds threshold must be one of 0, 13 or 52"
    )

    # no clipping for non-stake weighted polls
    data = copy.deepcopy(base_data)
    data["clip_low"] = 1
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "Clipping is only applicable to NMR weighted modes"
    )

    # valid clipping range
    data = copy.deepcopy(base_data)
    data["weight_mode"] = "log_numerai_stake"
    data["clip_low"] = -1
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Low-side clipping threshold must be positive"

    data = copy.deepcopy(base_data)
    data["weight_mode"] = "log_numerai_stake"
    data["clip_high"] = -1
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "High-side clipping threshold must be positive"

    data = copy.deepcopy(base_data)
    data["weight_mode"] = "log_numerai_stake"
    data["clip_low"] = 1
    data["min_stake"] = 2
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Low-side clipping threshold must be greater than min stake threshold"
    )

    data = copy.deepcopy(base_data)
    data["weight_mode"] = "log_numerai_stake"
    data["clip_low"] = 2
    data["clip_high"] = 1
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "High-side clipping threshold must be greater than low-side clipping threshold"
    )

    # valid number of options
    data = copy.deepcopy(base_data)
    data["options"] = []
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid number of options"

    data = copy.deepcopy(base_data)
    data["max_options"] = 6
    response = client.post(
        f"{settings.API_V1_STR}/polls/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid number of options"


def test_search_polls(client: TestClient, db: Session) -> None:
    poll = create_random_poll(db)
    response = client.post(f"{settings.API_V1_STR}/polls/search", json={"id": poll.id},)
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]

    crud.poll.remove(db, id=poll.id)  # type: ignore
    crud.user.remove(db, id=poll.owner_id)  # type: ignore


def test_search_polls_authenticated(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    poll = create_random_poll(db)
    response = client.post(
        f"{settings.API_V1_STR}/polls/search-authenticated", json={"id": poll.id},
    )
    assert response.status_code == 401

    response = client.post(
        f"{settings.API_V1_STR}/polls/search-authenticated",
        json={"id": poll.id},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]

    crud.poll.remove(db, id=poll.id)  # type: ignore
    crud.user.remove(db, id=poll.owner_id)  # type: ignore


def test_update_poll(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    poll = create_random_poll(db, owner_id=current_user["id"])
    data = dict()  # type: ignore

    # update blind
    data["options"] = [
        {"value": 0, "text": "Python"},
        {"value": 1, "text": "R"},
    ]
    response = client.put(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    assert len(content["options"]) == 2
    assert content["is_blind"]

    data = {"is_blind": False}  # type: ignore
    response = client.put(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    assert len(content["options"]) == 2
    assert content["is_blind"] is False

    # invalid attempt to change owner id
    data["owner_id"] = current_user["id"] + 1
    response = client.put(
        f"{settings.API_V1_STR}/polls/{content['id']}",
        headers=superuser_token_headers,
        json=data,
    )
    content = response.json()
    assert content["owner"]["id"] == current_user["id"]

    # invalid attempt to change id
    data["id"] = random_lower_string()  # type: ignore
    response = client.put(
        f"{settings.API_V1_STR}/polls/{content['id']}",
        headers=superuser_token_headers,
        json=data,
    )
    content = response.json()
    assert content["id"] == poll.id

    # invalid attempt to change poll topic
    data["topic"] = random_lower_string()  # type: ignore
    response = client.put(
        f"{settings.API_V1_STR}/polls/{content['id']}",
        headers=superuser_token_headers,
        json=data,
    )
    content = response.json()
    assert content["topic"] == poll.topic

    response = client.delete(
        f"{settings.API_V1_STR}/polls/{content['id']}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    poll = crud.poll.get(db, id=content["id"])  # type: ignore
    assert poll is None


def test_voting(client: TestClient, superuser_token_headers: dict, db: Session) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    poll = create_random_poll(db, owner_id=current_user["id"])

    data = [{"value": 0}]

    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]
    assert content["data"][0]["has_voted"]
    assert "votes" not in content["data"][0]["options"][0]

    # invalid duplicate vote
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "You already voted"

    crud.poll.remove(db, id=poll.id)  # type: ignore


def test_voting_observable(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    poll = create_random_poll(db, owner_id=current_user["id"])
    poll.is_blind = False
    db.commit()
    db.refresh(poll)

    data = [{"value": 0}]

    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]
    assert content["data"][0]["has_voted"]
    assert "votes" in content["data"][0]["options"][0]

    # invalid duplicate vote
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "You already voted"

    crud.poll.remove(db, id=poll.id)  # type: ignore


def test_voting_numerai_stake(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    poll = create_random_poll(
        db, owner_id=current_user["id"], weight_mode="log_numerai_stake"
    )
    poll = crud.poll.update(
        db, db_obj=poll, obj_in={"min_stake": 0.5, "clip_low": 2, "is_blind": False}
    )
    model_name = random_lower_string()
    model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=model_name, name=model_name, tournament=8, owner_id=current_user["id"],
        ),
    )
    crud.stake_snapshot.create(
        db,
        obj_in=schemas.StakeSnapshotCreate(
            date_creation=datetime.datetime.now(),
            name=model.name,
            tournament=model.tournament,
            nmr_staked=1,
            model_id=model.id,
        ),
    )

    # first vote
    data = [{"value": 0}]

    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]
    assert content["data"][0]["has_voted"]
    assert "votes" in content["data"][0]["options"][0]

    # second vote
    another_voter = create_random_user(db)
    another_voter = crud.user.update(
        db, db_obj=another_voter, obj_in={"is_superuser": True}
    )
    another_token_headers = authentication_token_from_username(
        client=client, username=another_voter.username, db=db
    )
    another_model_name = random_lower_string()
    another_model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=another_model_name,
            name=another_model_name,
            tournament=8,
            owner_id=another_voter.id,
        ),
    )
    crud.stake_snapshot.create(
        db,
        obj_in=schemas.StakeSnapshotCreate(
            date_creation=datetime.datetime.now(),
            name=another_model.name,
            tournament=another_model.tournament,
            nmr_staked=2,
            model_id=another_model.id,
        ),
    )

    data = [{"value": 1}]

    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=another_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]
    assert content["data"][0]["has_voted"]
    assert "votes" in content["data"][0]["options"][1]
    assert content["data"][0]["options"][1]["votes"] == np.log(2 + 1)
    assert (
        content["data"][0]["options"][1]["votes"]
        == content["data"][0]["options"][0]["votes"]
    )

    # invalid duplicate vote
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "You already voted"

    crud.poll.remove(db, id=poll.id)  # type: ignore
    crud.model.remove(db, id=model.id)  # type: ignore
    crud.model.remove(db, id=another_model.id)  # type: ignore
    crud.user.remove(db, id=another_voter.id)


def test_voting_numerai_stake_post_determined(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    poll = create_random_poll(
        db, owner_id=current_user["id"], weight_mode="log_numerai_stake"
    )
    poll = crud.poll.update(
        db,
        db_obj=poll,
        obj_in={"min_stake": 0.5, "clip_low": 2, "is_stake_predetermined": False},
    )
    model_name = random_lower_string()
    model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=model_name, name=model_name, tournament=8, owner_id=current_user["id"],
        ),
    )
    crud.stake_snapshot.create(
        db,
        obj_in=schemas.StakeSnapshotCreate(
            date_creation=datetime.datetime.now(),
            name=model.name,
            tournament=model.tournament,
            nmr_staked=1,
            model_id=model.id,
        ),
    )

    # first vote
    data = [{"value": 0}]

    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]
    assert content["data"][0]["has_voted"]
    assert "votes" not in content["data"][0]["options"][0]

    # second vote
    another_voter = create_random_user(db)
    another_voter = crud.user.update(
        db,
        db_obj=another_voter,
        obj_in={"is_superuser": True, "numerai_wallet_address": another_voter.username},
    )
    another_token_headers = authentication_token_from_username(
        client=client, username=another_voter.username, db=db
    )
    another_model_name = random_lower_string()
    another_model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=another_model_name,
            name=another_model_name,
            tournament=8,
            owner_id=another_voter.id,
        ),
    )
    crud.stake_snapshot.create(
        db,
        obj_in=schemas.StakeSnapshotCreate(
            date_creation=datetime.datetime.now(),
            name=another_model.name,
            tournament=another_model.tournament,
            nmr_staked=2,
            model_id=another_model.id,
        ),
    )

    data = [{"value": 1}]

    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=another_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]
    assert content["data"][0]["has_voted"]
    assert "votes" not in content["data"][0]["options"][1]

    # close poll
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}/close", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["options"][1]["votes"] == np.log(2 + 1)
    assert content["options"][1]["votes"] == content["options"][0]["votes"]

    # invalid vote after close
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Poll already closed"

    crud.poll.remove(db, id=poll.id)  # type: ignore
    crud.model.remove(db, id=model.id)  # type: ignore
    crud.model.remove(db, id=another_model.id)  # type: ignore
    crud.user.remove(db, id=another_voter.id)


def test_voting_equal_staked(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    poll = create_random_poll(
        db, owner_id=current_user["id"], weight_mode="equal_staked"
    )
    poll = crud.poll.update(
        db,
        db_obj=poll,
        obj_in={
            "min_stake": 0.5,
            "clip_low": 2,
            "is_blind": False,
            "stake_basis_round": 293,
        },
    )
    model_name = random_lower_string()
    model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=model_name, name=model_name, tournament=8, owner_id=current_user["id"],
        ),
    )
    crud.stake_snapshot.create(
        db,
        obj_in=schemas.StakeSnapshotCreate(
            date_creation=datetime.datetime.now(),
            round_tournament=293,
            name=model.name,
            tournament=model.tournament,
            nmr_staked=1,
            model_id=model.id,
        ),
    )

    # first vote
    data = [{"value": 0}]

    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]
    assert content["data"][0]["has_voted"]
    assert "votes" in content["data"][0]["options"][0]

    # second vote
    another_voter = create_random_user(db)
    another_voter = crud.user.update(
        db, db_obj=another_voter, obj_in={"is_superuser": True}
    )
    another_token_headers = authentication_token_from_username(
        client=client, username=another_voter.username, db=db
    )
    another_model_name = random_lower_string()
    another_model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=another_model_name,
            name=another_model_name,
            tournament=8,
            owner_id=another_voter.id,
        ),
    )
    crud.stake_snapshot.create(
        db,
        obj_in=schemas.StakeSnapshotCreate(
            date_creation=datetime.datetime.now(),
            round_tournament=293,
            name=another_model.name,
            tournament=another_model.tournament,
            nmr_staked=2,
            model_id=another_model.id,
        ),
    )

    data = [{"value": 1}]

    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=another_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert poll.id == content["data"][0]["id"]
    assert content["data"][0]["has_voted"]
    assert "votes" in content["data"][0]["options"][1]
    assert content["data"][0]["options"][1]["votes"] == 1
    assert (
        content["data"][0]["options"][1]["votes"]
        == content["data"][0]["options"][0]["votes"]
    )

    # invalid duplicate vote
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "You already voted"

    crud.poll.remove(db, id=poll.id)  # type: ignore
    crud.model.remove(db, id=model.id)  # type: ignore
    crud.model.remove(db, id=another_model.id)  # type: ignore
    crud.user.remove(db, id=another_voter.id)


def test_voting_invalid_inputs(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    poll = create_random_poll(db, owner_id=current_user["id"])

    # no option selected
    data = []  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid number of options"

    # more options than allowed
    data = [{"value": 0}, {"value": 1}, {"value": 3}]
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid number of options"

    # multiple options for single poll
    poll = crud.poll.update(db, db_obj=poll, obj_in={"is_multiple": False})
    data = [{"value": 0}, {"value": 1}]
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid number of options"
    poll = crud.poll.update(db, db_obj=poll, obj_in={"is_multiple": True})

    # no stake snapshot
    poll = crud.poll.update(
        db, db_obj=poll, obj_in={"weight_mode": "log_numerai_stake"}
    )
    data = [{"value": 0}, {"value": 1}]
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "You are not eligible for this poll: need to stake more than 0 NMR"
    )

    # not enough stake
    poll = crud.poll.update(db, db_obj=poll, obj_in={"min_stake": 1})
    model_name = random_lower_string()
    model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=model_name, name=model_name, tournament=8, owner_id=current_user["id"],
        ),
    )
    stake_snapshot = crud.stake_snapshot.create(
        db,
        obj_in=schemas.StakeSnapshotCreate(
            date_creation=datetime.datetime.now(),
            name=model.name,
            tournament=model.tournament,
            nmr_staked=1,
            model_id=model.id,
        ),
    )
    data = [{"value": 0}, {"value": 1}]
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "You are not eligible for this poll: need to stake more than 1 NMR"
    )

    # not enough active rounds
    poll = crud.poll.update(db, db_obj=poll, obj_in={"min_rounds": 52})
    # todo why is crud not working?
    stake_snapshot.nmr_staked = 2
    stake_snapshot.return_13_weeks = 0.5
    db.commit()
    db.refresh(stake_snapshot)
    response = client.post(
        f"{settings.API_V1_STR}/polls/{poll.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "You are not eligible for this poll: need to have at least one active model for more than 52 weeks"
    )

    crud.poll.update(db, db_obj=poll, obj_in={"weight_mode": "equal"})
    crud.model.remove(db, id=model.id)  # type: ignore
