---
sidebar_position: 3
---

# Sell a Product

This tutorial walks you through the process of listing a product on NumerBay.

:::note

You need to have a [NumerBay account](./set-up-account) with Numerai API Key in order to sell on NumerBay.

:::

## Create listing
To create a listing, head to **[My listings](https://numerbay.ai/my-account/my-listings)** page. Click the **New Listing** button and complete the new listing form as shown below.

### Basic product information
![Listing Basic](/img/tutorial/listingBasic.png)
* Category
    - numerai-predictions: [Numerai "Classic" tournament](https://numer.ai/tournament) submission files
    - numerai-model: Model binary file, training scripts or Jupyter notebooks for the associated model
    - signals-predictions: [Signals tournament](https://signals.numer.ai/tournament) submission files
    - signals-data: Data files used to train the associated Signals model or other files useful for Signals modeling
    - onlyfams-*: anything other than the above such as meme NFTs, clothing, etc.
* Product name:
    - For tournament categories this is a dropdown of Numerai models, select one
    - For onlyfams categories, enter an alphanumeric product name
* Avatar image URL:
    - This defaults to your numerai model avatar after selecting the model
    - This must be an HTTPS URL
* Active / Inactive: Whether your product will be active for sale immediately affer creation
* Perpetual / Temporary Listing: Whether (and when) your listing becomes unavailable for sale

### Featured products
![Listing Featured](/img/tutorial/listingFeatured.png)
Select from your other listings to be featured in this product's page

### Pricing options
![Listing Option](/img/tutorial/listingOption.png)
* Platform
    - On-Platform: Sell on NumerBay with full features
    - Off-Platform: Only link to an external listing page
* Listing Mode:
    - File Mode: Buyers can download artifact files and optionally designate a model slot for submission. You can upload artifacts to NumerBay or add external file URLs
    - Stake Only Mode: Submit for buyers automatically without distributing artifact files, without stake limit. You must upload artifacts to NumerBay
    - Stake Only Mode with Limit: Submit for buyers automatically without distributing artifact files, with a stake limit (in NMR). You must upload artifacts to NumerBay
* Number of Rounds per Unit: Number of tournament rounds bundled into this pricing option. 

:::info

Total number of rounds for an order will be `[order quantity] x [bundled number of rounds per unit]`

:::

### Reward coupons
![Listing Coupon Specs](/img/tutorial/listingCouponSpecs.png)
* Min Spend for Rewarding Coupon
    - Minimum spend in NMR required for the currently edited product to reward the buyer with a coupon
    - This is not the min spend for the actual coupon rewarded
* Applicable Products:
    - Your *other* listings that the rewarded coupon can be applied to
    - The currently edited product is always included in the applicable products list
* Coupon Discount: 0-100 integer, 100 being free
* Coupon Max Discount: Maximum discount cap in NMR for the rewarded coupons
* Coupon Min Spend: Minimum spend in NMR required for the applicable products in order for a buyer to use the rewarded coupons

:::info

Coupons generated using this reward mechanism are bound to the specific buyers and cannot be transferred or used by others.

:::

## Upload artifacts (WIP)
:::tip Advanced tip

You can automate this via NumerBay API, head over to the advanced [API Tutorial](/docs/tutorial-extras/api-automation) for details

:::

After tournament round opens, you need to upload artifact files to NumerBay to fulfill your active orders.

## Manage sales (WIP)
