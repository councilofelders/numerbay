---
sidebar_position: 3
---

# Vote

This tutorial walks you through the process of creating a sybil-resistant poll on NumerBay.

:::note

You need to have a [NumerBay account](./set-up-account) with Numerai API Key in order to create polls or vote on NumerBay.

:::

## Create a poll
To create a poll, head to **[My polls](https://numerbay.ai/polls)** page. Click the **New Poll** button and complete the new poll form as shown below.

### Basic settings
<img alt="Poll Creation Basic" src="/img/tutorial/pollCreationBasic.png" width="800"/>

* Topic: Main topic of the poll
* End Date: Poll automatically ends on this date at 00:00 UTC
* Description: Description of the poll
* Short url: Used for generating short URL, cannot be changed later
* Multiple choice: Whether a voter can choose multiple (and how many) options
* Weighting Mode:
  - `Equal Weights for All`: Anyone can vote. All votes are equal weighted
  - `Equal Weights for Staked`: Only staked Numerai participants can vote. All votes are equal weighted
  - `Log Staked NMR`: Votes are weighted by the formula `LN(1+[Tournament Stake])`

### Advanced settings
Click **Show advanced settings** for additional configurations.
<img alt="Poll Creation Advanced" src="/img/tutorial/pollCreationAdvanced.png" width="800"/>

* Blind results: Whether to keep the results hidden until the poll ends
* Anonymous votes: Whether voter ID (Numerai Wallet Address) is encrypted when stored in the backend. This has no visible effect for the voters. This only needs to be set if a subsequent vote audit is required
* Min participation threshold:
    - `All Active Participants`: No minimum staked rounds requirement
    - `Min 3 Month Participation`: Requires staked participation for the past 13 weeks
    - `Min 1 Year Participation`: Requires staked participation for the past 52 weeks
* Stake Determination (only for blind polls):
    - `Pre-determine Stake`: Use the stake snapshot taken for the tournament round before poll creation
    - `Post-determine Stake`: Only applicable for blind polls. Use the stake snapshot taken for the tournament round when poll closes
* Stake basis round: use stake snapshot as of a certain tournament round for vote weight calculation
* Min stake: Minimum staked NMR required to vote
* Clipping for low stake: Clip lower NMR values to this amount
* Clipping for high stake: Clip higher NMR values to this amount

## Vote on a poll
<img alt="Poll Vote" src="/img/tutorial/pollVote.png" width="600"/>
