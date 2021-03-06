""" Dependencies for poll endpoints """

from decimal import Decimal
from typing import List, Optional

from fastapi import HTTPException
from jose import jwt
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app import crud, models
from app.api.dependencies import numerai
from app.core.config import settings


def validate_active_52_weeks(user_models_snapshots: List) -> None:
    """Validate user active for 52 weeks"""
    is_valid = False
    for model_snapshot in user_models_snapshots:
        if model_snapshot.return_52_weeks is not None:
            is_valid = True
            break
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="You are not eligible for this poll: "
            "need to have at least one active model for more than 52 weeks",
        )


def validate_active_13_weeks(user_models_snapshots: List) -> None:
    """Validate user active for 13 weeks"""
    is_valid = False
    for model_snapshot in user_models_snapshots:
        if model_snapshot.return_13_weeks is not None:
            is_valid = True
            break
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="You are not eligible for this poll: "
            "need to have at least one active model for more than 13 weeks",
        )


def generate_voter_id(poll: models.Poll, user: models.User) -> str:
    """Generate voter ID"""
    if poll.is_anonymous:
        # todo other wallet support
        to_encode = {"poll_id": poll.id, "voter_address": user.numerai_wallet_address}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt
    return user.numerai_wallet_address  # type: ignore


def get_voter_weight(
    db: Session, poll: models.Poll, user: models.User, override: bool = False
) -> Optional[Decimal]:
    """Get voter weight"""
    min_stake = poll.min_stake if poll.min_stake is not None else 0

    # Numerai API, check regardless weight mode
    numerai.check_user_numerai_api(user)

    weight = None

    if poll.weight_mode == "equal":
        weight = Decimal("1")
    else:
        if poll.weight_mode in ["log_numerai_balance", "log_balance"]:
            raise HTTPException(status_code=400, detail="Weight mode not yet supported")

        stake_basis_round = (
            poll.stake_basis_round
            if poll.stake_basis_round is not None
            else crud.globals.get_singleton(db=db).active_round  # type: ignore
        )

        user_models_snapshots = (
            db.query(models.StakeSnapshot)
            .join(models.Model, models.Model.id == models.StakeSnapshot.model_id)
            .filter(
                and_(
                    models.Model.owner_id == user.id,
                    models.StakeSnapshot.round_tournament == stake_basis_round,
                )
            )
            .all()
        )
        user_nmr_staked = sum(
            [
                model_snapshot.nmr_staked
                for model_snapshot in user_models_snapshots
                if model_snapshot.nmr_staked is not None
            ]
        )

        # min stake requirement
        if user_nmr_staked <= min_stake:
            raise HTTPException(
                status_code=400,
                detail=f"You are not eligible for this poll: "
                f"need to stake more than {min_stake} NMR",
            )

        # min rounds requirement
        if poll.min_rounds == 13:
            validate_active_13_weeks(user_models_snapshots)

        if poll.min_rounds == 52:
            validate_active_52_weeks(user_models_snapshots)

        if poll.is_stake_predetermined or override:
            # clip stake
            if poll.clip_low and min_stake < user_nmr_staked < poll.clip_low:
                user_nmr_staked = poll.clip_low

            if poll.clip_high and user_nmr_staked > poll.clip_high:
                user_nmr_staked = poll.clip_high

            # calculate weight
            if poll.weight_mode == "equal_staked":
                weight = Decimal("1")
            elif poll.weight_mode == "log_numerai_stake":
                weight = (Decimal(user_nmr_staked) + Decimal("1")).ln()
        else:
            return None
    return weight


def get_user_from_voter_id(
    db: Session, voter_id: str, is_anonymous: bool
) -> Optional[models.User]:
    """Get user from voter ID"""
    if is_anonymous:
        voter_id_decoded = jwt.decode(
            voter_id, settings.SECRET_KEY, algorithms=["HS256"]
        )
        voter_address = voter_id_decoded["voter_address"]
        return (
            db.query(models.User)
            .filter(models.User.numerai_wallet_address == voter_address)
            .first()
        )
    return (
        db.query(models.User)
        .filter(models.User.numerai_wallet_address == voter_id)
        .first()
    )


def take_stake_weight_snapshots(db: Session, poll: models.Poll) -> None:
    """Take stake weight snapshots"""
    for each_vote in poll.votes:  # type: ignore
        voter = get_user_from_voter_id(db, each_vote.voter_id, poll.is_anonymous)
        try:
            weight = get_voter_weight(db, poll, voter, override=True)  # type: ignore
            each_vote.weight_basis = weight
        except Exception:  # pylint: disable=broad-except
            print(
                f"Error taking weight snapshot for {each_vote.voter_id} for poll {poll.id}"
            )
    db.commit()
    db.refresh(poll)
