---
sidebar_position: 1
---

# Set up Account

In order to buy or sell on NumerBay, a NumerBay account with Numerai API key needs to be set up.

## Sign up

Head to [numerbay.ai](https://numerbay.ai), click the account icon on the top right of the page, and:

### Login via MetaMask
Login via Metamask if you prefer easier authentication
<img alt="Sign up MetaMask" src="/img/tutorial/signUpMetaMask.png" width="400"/>
<img alt="Sign up MetaMask Sign" src="/img/tutorial/signUpMetaMaskSign.png" width="300"/>

### Username sign up
Sign up manually by clicking the **Username Login** tab, and click **Register today** to switch to the sign up form
<img alt="Sign up Username" src="/img/tutorial/signUpUsername.png" width="400"/>


## Set up Numerai API Key

After signing up and logging in, head to the [NumerBay account](https://numerbay.ai/my-account) page for the [Numerai API tab](https://numerbay.ai/my-account/numerai-api) under the Account sidebar section.

If you don't have a Numerai API key yet, you can create API Keys in the [Numerai Account Settings](https://numer.ai/account) page. Make sure it has at least **View user info** permission. NumerBay only uses user info for model ownership verification and email notifications.

Additional API permissions are needed depending on what you want to do on NumerBay, you can always change API keys later:

| Task\Permission         |    View user info    | View submission info |  Upload submissions  |        Stake*        |
| ----------------------- | :------------------: | :------------------: | :------------------: | :------------------: |
| Buy (File Mode)         | :heavy_check_mark:   |                      |                      |                      |
| Buy (with Auto-submit)  | :heavy_check_mark:   | :heavy_check_mark:   | :heavy_check_mark:   |                      |
| Buy (Stake Only Mode)   | :heavy_check_mark:   | :heavy_check_mark:   | :heavy_check_mark:   |                      |
| Buy (with Stake Limit)  | :heavy_check_mark:   | :heavy_check_mark:   | :heavy_check_mark:   |  :heavy_check_mark:  |
| Sell                    | :heavy_check_mark:   |                      |                      |                      |
| Vote                    | :heavy_check_mark:   |                      |                      |                      |

![Numerai API Key](/img/tutorial/numeraiApiKey.png)

[*]: **Stake** permission is only used to down-adjust stake below the product's stake limit if exceeded

## Update profile (WIP)
![Profile](/img/tutorial/profile.png)
