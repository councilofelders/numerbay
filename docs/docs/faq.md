---
sidebar_position: 2
---

# FAQ

Here are some frequently asked questions and troubleshooting guides.

## Authentication and Account Setup

### I can't login

If you had entered correct credentials, but the browser did not respond (e.g. no MetaMask pop up). This may be an issue with browser cache which tends to happen when the browser just recovered from a previous session. Please try to refresh the page and login again.

If you registered an account with username before and did not connect a MetaMask wallet, you would need to use the [legacy username login](https://numerbay.ai/login).

If you had a connected MetaMask wallet, make sure you are using the correct wallet for login.

If you forgot your account username or wallet, please post in the #numerbay channel in [Numerai Discord Server](https://discord.gg/numerai) for assistance.

### I'm getting "Numerai API Error: Insufficient Permission"

This may indicate your Numerai API key has expired or does not have required permissions, please check [here](./tutorial-basics/set-up-account.md#set-up-numerai-api-key) for the table of required permissions for different tasks, and go to the [Numerai Settings page](https://numerbay.ai/numerai-settings) to change your Numerai API key.

## Buying

### I bought a good model, and then it went to hell

Sorry to hear that. Unfortunately the market can be quite unpredictable, past performance is no indication of future returns. NumerBay is not an investment platform and financial gains are not guaranteed. You should be aware of the financial risks when making decisions. Good luck!

### Seller didn't upload files for my order

If the round has not ended yet, then be patient. Some sellers might upload closer to the deadline. If you are unsure, feel free to reach out to the seller privately or post in the #numerbay channel in [Numerai Discord Server](https://discord.gg/numerai) for assistance.

You can use the `Send Reminder` button on the Download popup to reminder the seller. Alternatively you can also request a refund on the purchases page which also allows attaching a message to the seller. 

NumerBay doesn't yet provide fully automated dispute resolution. If you did not receive anything after the round deadline, you can request a refund with a message to try to contact the seller in private or post in the #numerbay channel in [Numerai Discord Server](https://discord.gg/numerai) for assistance. Depending on the specific situation, you might be able to get a refund or order extension.

### I changed model name, but my order's submission slot is still the old name

Don't worry, the submission will go to the correct slot. To show the new model name in the future, go to the [Numerai Settings page](https://numerbay.ai/numerai-settings) and click the `sync` button on the top right to sync your model slots with Numerai. 

When you changed your model names or created new model slots, it's recommended to refresh the API using the `refresh` button on the top right of the Numerai API Key form on the [Numerai Settings page](https://numerbay.ai/numerai-settings).


## Selling

### I'm getting "Upload cancelled, no active order to upload for"

This happens when your product uses buyer-side encryption (which is by default), and you don't have any active sale order for the product. Upload is only possible when a sale order is available. 

If you want to automate things, you can solve this in two ways in the [listing settings](https://numerbay.ai/listings). Edit your listing, check the `Show advanced settings` box and then:
1. Set a webhook URL for NumerBay to trigger on each confirmed sale to automate each submission, OR
2. Disable client-side encryption to upload only once regardless of any sale order (Make sure you only turn off encryption when you don't have any active sale, including past sales that are still active. Otherwise, the buyers won't be able to receive files)

### Do I have to upload again on each new order?

Yes if your product uses buyer-side encryption (which is by default), you can check whether this is enabled [listing settings](https://numerbay.ai/listings). Edit your listing, check the `Show advanced settings` box to see the option.

If you don't want to do this, check the answer for the previous question for solutions.

### I missed upload for a buyer

NumerBay doesn't yet provide automated dispute resolution, please post in the #numerbay channel in [Numerai Discord Server](https://discord.gg/numerai) for assistance. You can offer a refund, or an order extension.
