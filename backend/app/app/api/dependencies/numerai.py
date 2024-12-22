""" Dependencies for numerai endpoints """

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, Optional

import pandas as pd
from fastapi import HTTPException
from numerapi import NumerAPI
from sqlalchemy.orm import Session

from app import crud, models


def get_numerai_api_user_info(public_id: str, secret_key: str) -> Any:
    """
    Retrieve Numerai user info.
    """
    query = """
              query {
                account {
                  username
                  email
                  id
                  status
                  insertedAt
                  walletAddress
                  apiTokens {
                    name
                    publicId
                    scopes
                  }
                }
              }
            """

    api = NumerAPI(public_id=public_id, secret_key=secret_key)
    account = api.raw_query(query, authorization=True)["data"]["account"]
    return account


def get_numerai_model_profile(tournament: int, model_name: str) -> Any:
    """Get Numerai model performance"""
    numerai_query = """
            query($username: String!, $tournament: Int!) {
              v3UserProfile(modelName: $username, tournament: $tournament) {
                id
                username
                startDate
                stakeValue
                stakeInfo {
                  corrMultiplier
                  mmcMultiplier
                  takeProfit
                  tcMultiplier
                }
                latestUserScores {
                  displayName
                  rank
                  reputation
                }
                latestReturns {
                  oneDay
                  threeMonths
                  oneYear
                  allTime
                }
              }
            }
    """

    signals_query = """
            query($username: String!) {
              v2SignalsProfile(modelName: $username) {
                id
                username
                startDate
                stakeValue
                stakeInfo {
                  corrMultiplier
                  mmcMultiplier
                  takeProfit
                  tcMultiplier
                }
                latestUserScores {
                  displayName
                  rank
                  reputation
                }
                latestReturns {
                  oneDay
                  threeMonths
                  oneYear
                  allTime
                }
              }
            }
    """

    query = numerai_query
    if tournament == 11:
        query = signals_query

    arguments = {"username": model_name}
    if tournament != 11:
        arguments["tournament"] = tournament

    api = NumerAPI()
    data = api.raw_query(query, arguments)["data"]

    return (
        data.get("v3UserProfile", {})
        if tournament in [8, 12]
        else data.get("v2SignalsProfile", {})
    )


def get_numerai_round_model_performance_v2(
    tournament: int, model_id: str, n_rounds: int = 10
) -> Any:
    """Get Numerai model performance"""
    query = """
            query($model_id: String!, $lastNRounds: Integer!, $tournament: Integer!) {
              v2RoundModelPerformances(
                distinctOnRound: true,
                modelId: $model_id,
                lastNRounds: $lastNRounds,
                tournament: $tournament
              ) {
                atRisk
                corrMultiplier
                tcMultiplier
                roundId
                roundNumber
                roundOpenTime
                roundPayoutFactor
                roundResolveTime
                roundResolved
                roundScoreTime
                submissionScores {
                  date
                  day
                  displayName
                  payoutPending
                  payoutSettled
                  percentile
                  value
                }
              }
            }
    """

    arguments = {
        "model_id": model_id,
        "lastNRounds": n_rounds,
        "tournament": tournament,
    }
    api = NumerAPI()
    data = api.raw_query(query, arguments)["data"]
    return data


def get_numerai_models(public_id: str, secret_key: str) -> Any:
    """Get Numerai models"""
    query = """
              query {
                account {
                  username
                  email
                  id
                  status
                  insertedAt
                  models {
                    id
                    name
                    tournament
                    profileUrl
                  }
                }
              }
            """

    api = NumerAPI(public_id=public_id, secret_key=secret_key)
    account = api.raw_query(query, authorization=True)["data"]["account"]
    all_models = account["models"]
    return all_models


def get_numerai_wallet_transactions(public_id: str, secret_key: str) -> Any:
    """
    Retrieve Numerai wallet transactions.
    """
    query = """
              query {
                account {
                  username
                  walletAddress
                  walletTxns {
                    amount
                    from
                    status
                    time
                    to
                    tournament
                    txHash
                    type
                  }
                }
              }
            """

    api = NumerAPI(public_id=public_id, secret_key=secret_key)
    account = api.raw_query(query, authorization=True)["data"]["account"]
    wallet_transactions = account["walletTxns"]
    return wallet_transactions


def normalize_data(data: Dict, tournament: int = 8) -> Dict:
    """Normalize Numerai data"""
    normalized_data = {"rounds": data["rounds"], "modelPerformance": {}}
    if tournament in [8, 12]:
        normalized_data["modelPerformance"] = data["v3UserProfile"]
        normalized_data["nmrStaked"] = data["v3UserProfile"]["nmrStaked"]
        normalized_data["startDate"] = data["v3UserProfile"]["startDate"]
    else:
        normalized_data["nmrStaked"] = data["v2SignalsProfile"]["nmrStaked"]
        normalized_data["startDate"] = data["v2SignalsProfile"]["startDate"]
        normalized_data["modelPerformance"] = {}
        if data["v2SignalsProfile"]["latestRanks"]:
            normalized_data["modelPerformance"]["latestRanks"] = {
                "corr": data["v2SignalsProfile"]["latestRanks"]["corr20d"],
                "corr60": data["v2SignalsProfile"]["latestRanks"]["corr60"],
                "mmc": data["v2SignalsProfile"]["latestRanks"]["mmc20d"],
                "tc": data["v2SignalsProfile"]["latestRanks"]["tc"],
                "ic": data["v2SignalsProfile"]["latestRanks"]["ic"],
            }
            normalized_data["modelPerformance"]["latestReps"] = {
                "corr": data["v2SignalsProfile"]["latestReps"]["corr20d"],
                "corr60": data["v2SignalsProfile"]["latestReps"]["corr60"],
                "mmc": data["v2SignalsProfile"]["latestReps"]["mmc20d"],
                "tc": data["v2SignalsProfile"]["latestReps"]["tc"],
                "ic": data["v2SignalsProfile"]["latestReps"]["ic"],
            }
            normalized_data["modelPerformance"]["latestReturns"] = data[
                "v2SignalsProfile"
            ]["latestReturns"]
        else:
            normalized_data["modelPerformance"]["latestRanks"] = {}
            normalized_data["modelPerformance"]["latestReps"] = {}
            normalized_data["modelPerformance"]["latestReturns"] = {}
        normalized_data["modelPerformance"]["stakeInfo"] = data["v2SignalsProfile"][
            "stakeInfo"
        ]
        normalized_data["modelPerformance"]["roundModelPerformances"] = []
        for round_performance in data["v2SignalsProfile"]["roundModelPerformances"]:
            if round_performance["corr20d"] is not None:
                round_performance_normalized = {
                    "roundNumber": round_performance["roundNumber"],
                    "corr": round_performance["corr20d"],
                    "corr60": round_performance["corr60"],
                    "mmc": round_performance["mmc20d"],
                    "tc": round_performance["tc"],
                    "ic": round_performance["ic"],
                    "corrPercentile": round_performance["corr20dPercentile"],
                    "corr60Percentile": round_performance["corr60Percentile"],
                    "mmcPercentile": round_performance["mmc20dPercentile"],
                    "tcPercentile": round_performance["tcPercentile"],
                    "icPercentile": round_performance["icPercentile"],
                    "corrMultiplier": round_performance["corrMultiplier"],
                    "mmcMultiplier": round_performance["mmcMultiplier"],
                    "tcMultiplier": round_performance["tcMultiplier"],
                    "payout": round_performance["payout"],
                    "selectedStakeValue": round_performance["selectedStakeValue"],
                }
                normalized_data["modelPerformance"]["roundModelPerformances"].append(
                    round_performance_normalized
                )
    return normalized_data


def get_leaderboard(tournament: int) -> Any:
    """Get Numerai Leaderboard"""
    numerai_query = """
            query {
              v2Leaderboard {
                username
                nmrStaked
                return13Weeks
                return52Weeks
              }
            }
    """

    signals_query = """
            query {
              signalsLeaderboard {
                username
                nmrStaked
                return13Weeks
                return52Weeks
              }
            }
    """

    crypto_query = """
                query {
                  cryptosignalsLeaderboard {
                    username
                    nmrStaked
                    return13Weeks
                    return52Weeks
                  }
                }
        """

    api = NumerAPI()

    data = None
    if tournament == 8:
        query = numerai_query
        data = api.raw_query(query)["data"]["v2Leaderboard"]
    elif tournament == 11:
        query = signals_query
        data = api.raw_query(query)["data"]["signalsLeaderboard"]
    elif tournament == 12:
        query = crypto_query
        data = api.raw_query(query)["data"]["cryptosignalsLeaderboard"]

    return data


def get_numerai_pipeline_status(tournament: int) -> Any:
    """Get Numerai pipeline status"""
    query = """
            query($date: String!, $tournament: String!) {
              pipelineStatus(date: $date, tournament: $tournament) {
                dataReadyAt
                isScoringDay
                resolvedAt
                scoredAt
                startedAt
                tournament
              }
            }
    """
    arguments = {
        "date": str(datetime.utcnow().date()),
        "tournament": "classic" if tournament == 8 else "signals",
    }
    api = NumerAPI()
    data = api.raw_query(query, arguments)["data"]

    return data["pipelineStatus"]


def get_target_stake(
    public_id: str, secret_key: str, tournament: int, model_name: str
) -> Decimal:
    """Get target stake for Numerai model"""
    query = """
              query {
                  account {
                    models {
                      id
                      name
                      tournament
                      v2Stake {
                        latestValue
                        latestValueSettled
                        status
                        tournamentNumber
                        txHash
                        pendingV2ChangeStakeRequest {
                          dueDate
                          requestedAmount
                          status
                          type
                        }
                      }
                    }
                  }
                }
            """

    arguments = {"username": model_name}
    api = NumerAPI(public_id=public_id, secret_key=secret_key)
    numerai_models = api.raw_query(query, arguments, authorization=True)["data"][
        "account"
    ]["models"]
    for model in numerai_models:
        if model["name"] == model_name and model["tournament"] == tournament:
            stake_dict = model["v2Stake"]
            stake_amount = Decimal(stake_dict["latestValueSettled"])
            pending_stake_change = stake_dict.get("pendingV2ChangeStakeRequest", None)
            if pending_stake_change and pending_stake_change["status"] == "pending":
                delta_amount = Decimal(pending_stake_change["requestedAmount"])
                if pending_stake_change["type"] == "increase":
                    stake_amount += delta_amount
                else:
                    stake_amount -= delta_amount
            return stake_amount
    raise ValueError("No Matching Model.")


def set_target_stake(  # pylint: disable=too-many-locals
    public_id: str,
    secret_key: str,
    tournament: int,
    model_name: str,
    target_stake_amount: Decimal,
) -> Dict:
    """Set target stake for Numerai model"""
    query = """
              query {
                  account {
                    models {
                      id
                      name
                      tournament
                      v2Stake {
                        latestValue
                        latestValueSettled
                        status
                        tournamentNumber
                        txHash
                        pendingV2ChangeStakeRequest {
                          dueDate
                          requestedAmount
                          status
                          type
                        }
                      }
                    }
                  }
                }
            """

    api = NumerAPI(public_id=public_id, secret_key=secret_key)
    numerai_models = api.raw_query(query, {"username": model_name}, authorization=True)[
        "data"
    ]["account"]["models"]
    stake_amount = None
    pending_delta_amount = None
    matched_model = None

    for model in numerai_models:
        if model["name"] == model_name and model["tournament"] == tournament:
            matched_model = model
            stake_dict = model["v2Stake"]
            stake_amount = Decimal(stake_dict["latestValueSettled"])
            pending_stake_change = stake_dict.get("pendingV2ChangeStakeRequest", None)
            if pending_stake_change and pending_stake_change["status"] == "pending":
                pending_delta_amount = Decimal(pending_stake_change["requestedAmount"])
                if pending_stake_change["type"] == "decrease":
                    pending_delta_amount = (
                        -pending_delta_amount  # pylint: disable=invalid-unary-operand-type
                    )
    if matched_model is None or stake_amount is None:
        raise ValueError("No Matching Model.")

    pending_delta_amount = (
        pending_delta_amount if pending_delta_amount else Decimal("0")
    )
    remaining_delta_amount = Decimal(target_stake_amount) - (
        stake_amount + pending_delta_amount
    )
    net_delta_amount = pending_delta_amount + remaining_delta_amount
    print(f"apply delta {net_delta_amount}")

    result_stake = api.stake_change(
        str(abs(net_delta_amount)),
        action="increase" if net_delta_amount > 0 else "decrease",
        model_id=matched_model["id"]
    )
    return result_stake


def get_numerai_active_round() -> Dict:
    """
    Retrieve Numerai active round.
    """
    query = """
              query {
                rounds(tournament: 8
                       number: 0) {
                  number
                  openTime
                  closeTime
                  closeStakingTime
                }
              }
            """

    api = NumerAPI()
    active_round = api.raw_query(query)["data"]["rounds"][0]
    return active_round


async def fetch_single_user_models(user: models.User) -> Dict:
    """Fetch single user models"""
    from app.api.api_v1.endpoints.numerai import (  # pylint: disable=import-outside-toplevel
        get_numerai_models_endpoint,
        # get_numerai_model_profile_endpoint,
    )

    numerai_models = get_numerai_models_endpoint(current_user=user)  # type: ignore
    return {"id": user.id, "models": numerai_models}


def check_user_numerai_api(user: models.User) -> None:
    """Check user Numerai API key"""
    if not user.is_superuser:
        try:
            if not user.numerai_api_key_public_id or not user.numerai_api_key_secret:
                raise ValueError
            get_numerai_api_user_info(
                public_id=user.numerai_api_key_public_id,
                secret_key=user.numerai_api_key_secret,
            )
        except Exception:
            raise HTTPException(
                status_code=400, detail="Numerai API Error: Insufficient Permission."
            )


def sync_user_numerai_api(db: Session, user_json: dict) -> None:
    numerai_api_updated = crud.user.update_numerai_api(db, user_json)
    if not numerai_api_updated["success"]:
        raise HTTPException(status_code=400, detail=numerai_api_updated["message"])
    result = crud.model.update_model(db, user_json=user_json)
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Numerai API Error: Insufficient Permission.",
        )


def generate_numerai_submission_url(
    object_name: str,
    model_id: str,
    tournament: int = 8,
    numerai_api_key_public_id: str = None,
    numerai_api_key_secret: str = None,
) -> Dict:
    """
    Generate Numerai submission URL.
    """
    api = NumerAPI(
        public_id=numerai_api_key_public_id, secret_key=numerai_api_key_secret
    )

    if tournament in [8, 12]:
        auth_query = """
                            query($filename: String!
                                  $tournament: Int!
                                  $modelId: String) {
                                submission_upload_auth(filename: $filename
                                                       tournament: $tournament
                                                       modelId: $modelId) {
                                    filename
                                    url
                                }
                            }
                            """

        arguments = {
            "filename": object_name,
            "tournament": tournament,
            "modelId": model_id,
        }

        submission_auth = api.raw_query(auth_query, arguments, authorization=True)[
            "data"
        ]["submission_upload_auth"]

    else:
        auth_query = """
                    query($filename: String!
                          $modelId: String) {
                      submissionUploadSignalsAuth(filename: $filename
                                                modelId: $modelId) {
                            filename
                            url
                        }
                    }
                    """

        arguments = {"filename": object_name, "modelId": model_id}

        submission_auth = api.raw_query(auth_query, arguments, authorization=True)[
            "data"
        ]["submissionUploadSignalsAuth"]
    return submission_auth


def validate_numerai_submission(
    object_name: str,
    model_id: str,
    tournament: int = 8,
    numerai_api_key_public_id: str = None,
    numerai_api_key_secret: str = None,
) -> Optional[str]:
    """Validate Numerai submission"""
    api = NumerAPI(
        public_id=numerai_api_key_public_id, secret_key=numerai_api_key_secret
    )

    if tournament in [8, 12]:
        # Create submission
        create_query = """
                                    mutation($filename: String!
                                             $tournament: Int!
                                             $version: Int!
                                             $modelId: String
                                             $triggerId: String) {
                                        create_submission(filename: $filename
                                                          tournament: $tournament
                                                          version: $version
                                                          modelId: $modelId
                                                          triggerId: $triggerId
                                                          source: "numerapi") {
                                            id
                                        }
                                    }
                                    """

        arguments = {
            "filename": object_name,
            "tournament": tournament,
            "version": 1,
            "modelId": model_id,
            "triggerId": None,
        }  # os.getenv('TRIGGER_ID', None)}
    else:
        # Create submission
        create_query = """
                    mutation($filename: String!
                             $modelId: String
                             $triggerId: String) {
                        createSignalsSubmission(filename: $filename
                                                modelId: $modelId
                                                triggerId: $triggerId
                                                source: "numerapi") {
                            id
                            firstEffectiveDate
                        }
                    }
                    """

        arguments = {
            "filename": object_name,
            "modelId": model_id,
            "triggerId": None,
        }

    try:
        create = api.raw_query(create_query, arguments, authorization=True)
    except ValueError:  # try again with new data version
        print("Retrying upload with version 2")
        arguments["version"] = 2
        try:
            create = api.raw_query(create_query, arguments, authorization=True)
        except Exception:  # other errors  # pylint: disable=broad-except
            print("Retry failed, marking submission as failed")
            # mark failed submission
            return None
    except Exception:  # other errors  # pylint: disable=broad-except
        print("Submission failed")
        # mark failed submission
        return None
    if create:
        submission_id = (
            create["data"]["create_submission"]["id"]
            if tournament in [8, 12]
            else create["data"]["createSignalsSubmission"]["id"]
        )
        print(f"submission_id: {submission_id}")
        return submission_id
    print("Submission failed")
    return None


def validate_round_open() -> None:
    active_round = get_numerai_active_round()
    utc_time = datetime.now(timezone.utc)
    close_staking_time = pd.to_datetime(
        active_round["closeStakingTime"]
    ).to_pydatetime()
    if (  # pylint: disable=no-else-return
        utc_time > close_staking_time
    ):  # previous round closed for staking, next round not yet opened
        raise HTTPException(status_code=400, detail="Tournament round is not open")
    return None


def fill_missing_round_performances(data: Dict) -> Dict:
    model_performance = data.get("modelPerformance", None)
    if model_performance is None:
        return data
    round_model_performances = model_performance.get("roundModelPerformances", None)
    if round_model_performances is None:
        return data
    round_performance_mapping = {
        scores["roundNumber"]: scores for scores in round_model_performances
    }
    min_round = round_model_performances[-1]["roundNumber"]
    max_round = round_model_performances[0]["roundNumber"]
    for round_tournament in range(min_round, max_round + 1):
        if round_tournament not in round_performance_mapping:
            round_performance_mapping[round_tournament] = {
                "roundNumber": round_tournament,
                "corr": None,
                "mmc": None,
                "tc": None,
                "ic": None,
                "corrPercentile": None,
                "mmcPercentile": None,
                "tcPercentile": None,
                "icPercentile": None,
                "selectedStakeValue": None,
            }
    data["modelPerformance"]["roundModelPerformances"] = [
        round_performance_mapping[round_tournament]
        for round_tournament in reversed(range(min_round, max_round + 1))
    ]
    return data
