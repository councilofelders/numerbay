from typing import Any

from numerapi import NumerAPI


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
