---
sidebar_position: 3
---

# Vote

This tutorial walks you through the process of creating a sybil-resistant poll on NumerBay.

:::note

You need to have a [NumerBay account](./set-up-account) with Numerai API Key in order to create polls or vote on NumerBay.

:::

## Create a poll
To create a poll, head to **[My polls](https://numerbay.ai/my-account/my-polls)** page. Click the **New Poll** button and complete the new poll form as shown below.

![Poll Creation](/img/tutorial/pollCreation.png)
* Custom Poll ID: Used for generating short URL, cannot be changed later
* End Date: Poll automatically ends on this date at 00:00 UTC
* Anonymous / Named Votes: Whether voter ID (Numerai Wallet Address) is stored in the backend encrypted. This has no visible effect for the voters
* Result Visibility:
    - Observable: Point-in-time poll results are visible to voters after they vote
    - Blind: Results are only visible after poll ends
* Weighting Mode:
    - Equal Weights for Staked Participants: Only staked Numerai participants can vote. All votes are equal weighted
    - Equal Weights for All: Anyone can vote. All votes are equal weighted
    - Log Staked NMR: Votes are weighted by the formula `LN(1+[Tournament Stake])`
* Stake Determination:
    - Pre-determine Stake: Use the stake snapshot taken for the tournament round before poll creation
    - Post-determine Stake: Only applicable for blind polls. Use the stake snapshot taken for the tournament round when poll closes
* Participation Threshold:
    - All Active Participants: No minimum staked rounds requirement
    - Min 3 Month Participation: Requires staked participation for the past 13 weeks
    - Min 1 Year Participation: Requires staked participation for the past 52 weeks

## Vote on a poll
![Poll Vote](/img/tutorial/pollVote.png)
