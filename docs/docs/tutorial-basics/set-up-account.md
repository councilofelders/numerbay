---
sidebar_position: 1
---

# Set up Account

In order to buy or sell on NumerBay, a NumerBay account with Numerai API key needs to be set up.

## Sign up

Head to **[numerbay.ai](https://numerbay.ai)**, click the account icon on the top right of the page, and:

### Login via MetaMask
<img alt="Sign up MetaMask" src="/img/tutorial/signUpMetaMask.png" width="400"/>
<img alt="Sign up MetaMask Sign" src="/img/tutorial/signUpMetaMaskSign.png" width="300"/>

### Username sign up
If you don't want to use MetaMask, sign up manually by clicking the **Username Login** tab, and click **Register today** to switch to the sign up form.
<img alt="Sign up Username" src="/img/tutorial/signUpUsername.png" width="400"/>


## Set up Numerai API Key

After signing up and logging in, head to the [NumerBay account](https://numerbay.ai/my-account) page for the **[Numerai API form](https://numerbay.ai/my-account/numerai-api)** under the Account sidebar section.

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

:::info

If you encounter error while updating with a valid Numerai API key, it may be likely that you are not logged in with the correct NumerBay account, you may have another old account bound to the same Numerai account. 
Please check if you are logged in with the correct MetaMask wallet or if you have an old account or account created with username.

:::

## Update profile
You can change your username, password and email in the [profile update form](https://numerbay.ai/my-account/my-profile). By default, your Numerai email address is used to receive email notifications.

:::caution

If you disconnect MetaMask wallet in the profile update form and your account was created with MetaMask login. You need to set a password before logging out, or you might lose access to the account.

NumerBay does not yet allow password recovery, please contact site admin for assistance by posting in the [#numerbay](https://community.numer.ai/channel/numerbay) channel on RocketChat.

:::

![Profile](/img/tutorial/profile.png)
