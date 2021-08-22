from typing import Any, List, Dict
from numerapi import NumerAPI

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List)
def get_numerai_models(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve products.
    """
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
                  apiTokens {
                    name
                    public_id
                    scopes
                  }
                }
              }
            """
    if current_user.numerai_api_key_secret is None or len(current_user.numerai_api_key_secret)==0:
        raise HTTPException(
            status_code=403,
            detail="Numerai API Key is required to perform this action",
        )
    api = NumerAPI(public_id=current_user.numerai_api_key_public_id, secret_key=current_user.numerai_api_key_secret)
    account = api.raw_query(query, authorization=True)['data']['account']
    all_models = account['models']
    return all_models


def normalize_data(data, tournament: int = 8):
    normalized_data = {'rounds': data['rounds']}
    normalized_data['modelPerformance'] = {}
    if tournament == 8:
        normalized_data['modelPerformance'] = data['v3UserProfile']
        normalized_data['nmrStaked'] = data['v3UserProfile']['nmrStaked']
        normalized_data['startDate'] = data['v3UserProfile']['startDate']
    else:
        normalized_data['nmrStaked'] = data['signalsUserProfile']['totalStake']
        normalized_data['startDate'] = data['signalsUserProfile']['startDate']
        normalized_data['modelPerformance'] = {}
        if data['signalsUserProfile']['latestRanks']:
            normalized_data['modelPerformance']['latestRanks'] = {
                'corr': data['signalsUserProfile']['latestRanks']['rank'],
                'mmc': data['signalsUserProfile']['latestRanks']['mmcRank']
            }
            normalized_data['modelPerformance']['latestReps'] = {
                'corr': data['signalsUserProfile']['latestRoundPerformances'][0]['corrRep'],
                'mmc': data['signalsUserProfile']['latestRoundPerformances'][0]['mmcRep']
            }
            normalized_data['modelPerformance']['latestReturns'] = data['signalsUserProfile']['latestReturns']
        else:
            normalized_data['modelPerformance']['latestRanks'] = {}
            normalized_data['modelPerformance']['latestReps'] = {}
            normalized_data['modelPerformance']['latestReturns'] = {}
        normalized_data['modelPerformance']['roundModelPerformances'] = []
        for round_performance in data['signalsUserProfile']['latestRoundPerformances']:
            if round_performance['correlation'] is not None:
                normalized_data['modelPerformance']['roundModelPerformances'].append(
                    {"corr": round_performance['correlation'], "mmc": round_performance['mmc'], "roundNumber": round_performance['roundNumber']}
                )
    return normalized_data


@router.get("/{tournament}/{model_name}", response_model=Dict)
def get_numerai_model_performance(
    tournament: int,
    model_name: str
) -> Any:
    """
    Retrieve products.
    """
    numerai_query = """
            query($username: String!) {
              rounds(tournament: 8, number: 0) {
                number
              },
              v3UserProfile(modelName: $username) {
                startDate
                nmrStaked
                roundModelPerformances {
                  roundNumber
                  corr
                  mmc
                }
                latestReps {
                  corr
                  mmc
                }
                latestRanks {
                  corr
                  mmc
                } 
                latestReturns {
                  oneDay
                  threeMonths
                  oneYear
                }
              }
            }
    """

    signals_query = """
            query($username: String!) {
              rounds(tournament: 8, number: 0) {
                number
              },
              signalsUserProfile(username: $username) {
                startDate
                totalStake
                latestRanks {
                  rank
                  mmcRank
                }
                latestReturns {
                  oneDay
                  threeMonths
                  oneYear
                }
                latestRoundPerformances {
                  roundNumber
                  corrRep
                  mmcRep
                  correlation
                  mmc
                }
              }
            }
    """

    if tournament == 8:
        query = numerai_query
    elif tournament == 11:
        query = signals_query
    else:
        raise HTTPException(status_code=404, detail="Tournament not found")

    arguments = {'username': model_name}
    api = NumerAPI()
    data = api.raw_query(query, arguments)['data']
    data = normalize_data(data, tournament=tournament)

    return data
