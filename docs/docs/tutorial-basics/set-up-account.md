---
sidebar_position: 1
---

# Set up Account

In order to buy or sell on NumerBay, a NumerBay account with Numerai API key needs to be set up.

## Sign up

Head to **[numerbay.ai](https://numerbay.ai)**, click the **Connect Wallet** button on the top right of the page, and login by connecting your MetaMask wallet.

:::caution

Sign-up by username has been deprecated. Users who had not connected a MetaMask wallet to their accounts can login via the legacy username login tab.

:::

<img alt="Sign up MetaMask" src="/img/tutorial/signUpMetaMask.png" width="450"/>
<img alt="Sign up MetaMask Sign" src="/img/tutorial/signUpMetaMaskSign.png" width="250"/>

## Generate Key Pair
In the **[Edit profile page](https://numerbay.ai/account)**, click the **Generate Key Pair** button to generate a public-private key pair that will be used to encrypt your purchased artifact files.
After doing so, click **Export key file** to safe-keep the generated key. The exported key file can be used in the [Python client](/docs/tutorial-extras/api-automation) to download encrypted files.

![Profile](/img/tutorial/profile.png)


## Set up Numerai API Key

After logging in, head to the NumerBay account settings for the **[Numerai Settings page](https://numerbay.ai/numerai-settings)** in the sidebar.

If you don't have a Numerai API key yet, you can create one in the [Numerai Account Settings](https://numer.ai/account) page. Make sure it has at least **View user info** permission. NumerBay only uses user info for model ownership verification and email notifications.

Additional API permissions may be needed depending on what you want to do on NumerBay, you can always change API keys later:

| Task\Permission         |    View user info    | View submission info |  Upload submissions  |        Stake*        |
| ----------------------- | :------------------: | :------------------: | :------------------: | :------------------: |
| Buy (File Mode)         | :heavy_check_mark:   |                      |                      |                      |
| Buy (with Auto-submit)  | :heavy_check_mark:   | :heavy_check_mark:   | :heavy_check_mark:   |                      |
| Buy (Stake Only Mode)   | :heavy_check_mark:   | :heavy_check_mark:   | :heavy_check_mark:   |                      |
| Buy (with Stake Limit)  | :heavy_check_mark:   | :heavy_check_mark:   | :heavy_check_mark:   |  :heavy_check_mark:  |
| Sell                    | :heavy_check_mark:   |                      |                      |                      |
| Vote                    | :heavy_check_mark:   |                      |                      |                      |

[*]: **Stake** permission is only used to down-adjust stake below the product's stake limit if exceeded

After creating an API key with the permissions required, plug them into the form as shown below, wait for a few seconds for validation, and the updated API Key permission info will be reflected:
![Numerai API Key](/img/tutorial/numeraiApiKey.png)

When you changed your model names or created new model slots, it's recommended to refresh the API using the `refresh` button on the top right.

:::info

If you encounter errors while updating with a valid Numerai API key, it may be likely that you are not logged in with the correct NumerBay account, you might have another old account bound to the same Numerai account. 
Please check if you are logged in with the correct MetaMask wallet or if you have an old account or account created with username.

:::


## Update profile
You can change your username, password and email in the **[Edit profile page](https://numerbay.ai/account)**. By default, your Numerai email address is used to receive email notifications.

:::caution

NumerBay does not yet allow password recovery, please contact support by posting in the #numerbay channel in [Numerai Discord Server](https://discord.gg/numerai).

:::
