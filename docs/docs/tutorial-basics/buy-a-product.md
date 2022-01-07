---
sidebar_position: 2
---

# Buy a Product

This tutorial walks you through the process of buying a product on NumerBay.

:::note

You need to have a [NumerBay account](./set-up-account) with Numerai API Key in order to make purchases on NumerBay.

:::

## Browse products

- [Classic Numerai Tournament Products](https://numerbay.ai/c/numerai)
- [Signals Tournament Products](https://numerbay.ai/c/signals)
- [NFTs and Others](https://numerbay.ai/c/onlyfams)

![Product Catalog](/img/tutorial/productCatalog.png)

### Key product properties
* Category
    - numerai-predictions: [Numerai "Classic" tournament](https://numer.ai/tournament) submission files
    - numerai-model: Model binary file, training scripts or Jupyter notebooks for the associated model
    - signals-predictions: [Signals tournament](https://signals.numer.ai/tournament) submission files
    - signals-data: Data files used to train the associated Signals model or other files useful for Signals modeling
    - onlyfams-*: Anything other than the above such as meme NFTs, clothing, etc.
* Platform
    - On-Platform: Product is sold on NumerBay with full features
    - Off-Platform: Product only links to an external listing page
* Listing Mode:
    - File Mode: You can download artifact files and optionally designate a model slot for submission
    - Stake Only Mode: Submit for you automatically without distributing artifact files, without stake limit. [only available for "numerai-predictions" and "signals-predictions" categories]
    - Stake Only Mode with Limit: Submit for you automatically without distributing artifact files, with a stake limit (in NMR). [only available for "numerai-predictions" and "signals-predictions" categories]
* Reward: If a Reward badge is shown on the category page for a product option, you will be rewarded with a coupon if your order meets some conditions.


## Checkout and payment

### Select product option and quantity
Select your preferred **product option** and the **quantity** of that product option you would like to buy, then click the **buy** button.

![Product Quantity](/img/tutorial/productQuantity.png)

:::info

The **quantity** selected here is the amount of the product option selected (which may bundle more than 1 tournament round) rather than the number of tournament rounds.

E.g. buying 3 of `2 x files for 4 NMR` option will result in an order of `3 x 2 = 6` tournament rounds totaling `3 x 4 = 12` NMRs.

:::

### Checkout
In the checkout page, confirm your order details and click **Pay**.

![Product Checkout](/img/tutorial/productCheckout.png)


### Apply coupon
If you have a valid discount coupon for the product, you can apply it on the right sidebar.

![Product Coupon](/img/tutorial/productCoupon.png)


### Auto-submission
If the product you are buying is a tournament submission, you can select a model slot to auto-submit to. This is mandatory if the product is sold in "Stake Only" mode. 


### Payment
You will be directed to the payment confirmation page. You can leave this page if you want to. Head over to your [Numerai wallet](https://numer.ai/wallet) to make payment.

![Product Payment](/img/tutorial/productPayment.png)

:::caution

Payment needs to be made **in full** and **in one single transaction** from your **Numerai wallet** within **45 minutes** after order creation. If no matching payment transaction is found within the time limit, the order will expire.

If you need help, please contact site admin for assistance by posting in the [#numerbay](https://community.numer.ai/channel/numerbay) channel on RocketChat.
:::

## Download artifacts

Your past orders are viewable in the **[Order History](https://numerbay.ai/my-account/order-history)** page. 
In order to download product artifacts such as tournament submission files, click **View details** on your order to view the list of downloadable artifact files.

![Order List](/img/tutorial/orderList.png)

## Submission
If you made your order with auto-submission set up during checkout, submissions will be automatically done for you after tournament round open and after the seller submits their files.

If you did not designate auto-submission lot or auto-submission failed, you can trigger a submission from the artifact list.

