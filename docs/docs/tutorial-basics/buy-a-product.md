---
sidebar_position: 2
---

# Buy a Product

This tutorial walks you through the process of buying a product on NumerBay.

:::note

You need to have a [NumerBay account](./set-up-account) with Numerai API Key in order to make purchases on NumerBay.

It is also recommended to [Generate a key pair](/docs/tutorial-basics/set-up-account#generate-key-pair) as 
some products use client-side encryption.

:::

:::tip

Some products use client-side encryption and are delivered on a per-order basis. It is therefore recommended to buy before
the tournaments start.

Learn more about [client-side encryption](/updates/encryption).

:::

## Browse products

- [Numerai Tournament Predictions](https://numerbay.ai/explore/numerai-predictions)
- [Numerai Tournament Models](https://numerbay.ai/explore/numerai-models)
- [Signals Tournament Predictions](https://numerbay.ai/explore/signals-predictions)
- [Signals Tournament Data](https://numerbay.ai/explore/signals-data)
- [NFTs and Others](https://numerbay.ai/explore/onlyfams)

![Product Catalog](/img/tutorial/productCatalog.png)

### Key product properties
* Category
    - `numerai-predictions`: [Numerai "Classic" tournament](https://numer.ai/tournament) submission files, per-round category
    - `numerai-model`: Model binary file, training scripts or Jupyter notebooks for the associated model
    - `signals-predictions`: [Signals tournament](https://signals.numer.ai/tournament) submission files, per-round category
    - `signals-data`: Data files used to train the associated Signals model or other files useful for Signals modeling, per-round category
    - `onlyfams-*`: Anything other than the above such as meme NFTs, clothing, etc.
* Platform
    - `On-Platform`: Product is sold on NumerBay with full features
    - `Off-Platform`: Product only links to an external listing page
* Listing Mode:
    - `File Mode`: You can download artifact files and optionally designate a model slot for submission
    - `Stake Only Mode`: Submit for you automatically without distributing artifact files, without stake limit. [only available for "numerai-predictions" and "signals-predictions" categories]
    - `Stake Only Mode with Limit`: Submit for you automatically without distributing artifact files, with a stake limit (in NMR). [only available for "numerai-predictions" and "signals-predictions" categories]
* Ready: If a `Ready` badge is shown for a product, this means the product artifact files are ready for download immediately after purchasing (for unencrypted listings), or the seller has delivered for at least one buyer (for encrypted listings). If the ready badge is not shown or if the product uses encryption, you will need to wait for seller to upload after your purchase. 
  This badge is reset every round for per-round categories `numerai-predictions`, `signals-predictions` and `signals-data`.
* Daily: If a `Daily` badge is shown for a product, this product uploads for every round, otherwise the product might only upload on weekends.

## Checkout and payment

### Place an order
Navigate to a product you are interested in, and click **Buy**. Then, select your preferred **product option** and the **quantity (number of rounds)** of that product option you would like to buy, read the disclaimer, and click **Place an Order**.

If the product you are buying is a tournament submission, you can select a model slot to **auto-submit** to. This is mandatory if the product is sold in "Stake Only" mode. 

If you have a valid discount **coupon** for the product, you can also apply it before placing an order.

![Product Quantity](/img/tutorial/productQuantity.png)

:::info

The **quantity** selected here is the number of tournament rounds based on the pricing option selected.

Each week consists of 5 daily rounds, therefore enter 5 if you want to buy for a week. Alternatively you can use the advanced calendar date picker to select specific days to buy.

:::

### Payment
After placing an order, you will see the payment instructions. Copy the address and amount to make a payment via your **[Numerai wallet](https://numer.ai/wallet)**. You can leave this page if you want to.

Your orders are viewable in the **[Purchases](https://numerbay.ai/purchases)** page. Orders are typically confirmed within 30 seconds after payments are confirmed on-chain.

:::caution

Payment needs to be made **in full** and **in one single transaction** from your **Numerai wallet** within **45 minutes** after order creation. If no matching payment transaction is found within the time limit, the order will expire.

NumerBay currently does not fully support payment from arbitrary NMR wallet, **DO NOT** send NMR from your own wallet or exchange wallets.

If you need help, please contact support by posting in the #numerbay channel in [Numerai Discord Server](https://discord.gg/numerai).

:::

<img alt="Product Payment" src="/img/tutorial/productPayment.png" width="450"/>

## Download artifacts

Head to the **[Purchases](https://numerbay.ai/purchases)** page. Click the **download** button next to your order to view the list of downloadable artifact files. Then, click on the file name to download the file.

If you purchased before Numerai tournament round starts, artifacts may not be available for immediate download. 
Sellers will be notified of your order and will upload artifacts once the tournament round starts. You cannot download artifacts for past rounds.

It is recommended to place orders early so sellers would have enough time to fulfill the upload.

:::tip Advanced tip

You can also download via the NumerBay Python / Cli Client, head over to the [API Tutorial](/docs/tutorial-extras/download-automation) for examples.

:::

![Order List](/img/tutorial/orderList.png)

### Decryption
If the product you bought uses client-side encryption, you may be prompted by MetaMask to decrypt your NumerBay key in order to decrypt the file.

![Decrypt](/img/tutorial/decrypt.png)

## Submission
If you made your order with auto-submission set up during checkout, submissions will be automatically done for you after tournament round open and after the seller submits their files.

### Change auto-submit model slot
You can change the auto-submit destination model in the order details panel which can be opened by clicking on the **View details** button in the **[Purchases](https://numerbay.ai/purchases)** page.

<img alt="Change Auto-submit" src="/img/tutorial/changeAutosubmit.png" width="700"/>

## Manage coupons
Some sellers may reward you with coupons for your orders. Your coupons are viewable in the **[My Coupons](https://numerbay.ai/coupons)** page. 

<img alt="My Coupons" src="/img/tutorial/myCoupons.png" width="800"/>
