---
sidebar_position: 3
---

# Sell a Product

This tutorial walks you through the process of listing a product on NumerBay.

:::note

You need to have a [NumerBay account](./set-up-account) with Numerai API Key in order to sell on NumerBay.

:::

## Create listing
To create a listing, head to **[My listings](https://numerbay.ai/listings)** page. Click **New Listing** and complete the new listing form as shown below.

### Basic product information
<img alt="Listing Basic" src="/img/tutorial/listingBasic.png" width="800"/>

* Category
    - `numerai-predictions`: [Numerai "Classic" tournament](https://numer.ai/tournament) submission files
    - `numerai-model`: Model binary file, training scripts or Jupyter notebooks for the associated model
    - `signals-predictions`: [Signals tournament](https://signals.numer.ai/tournament) submission files
    - `signals-data`: Data files used to train the associated Signals model or other files useful for Signals modeling
    - `onlyfams-*`: Anything other than the above such as meme NFTs, clothing, etc.
* Product name:
    - For tournament categories this is a dropdown of Numerai models, select one
    - For onlyfams categories, enter an alphanumeric product name
* Avatar image URL:
    - This defaults to your numerai model avatar after selecting the model
    - This must be an HTTPS URL
* Sell for weekday rounds:
    - Sell for all daily tournament rounds (default)

### Product description
An informative product description will help potential buyers make decisions. 
The product description field supports Markdown shortcuts and image upload to help you write rich text.

Some product categories (e.g. Signals data) comes with description templates which is populated automatically during listing creation when the category is selected.

To trigger the Markdown shortcuts, type in the editor instead of copy-and-pasting Markdown text. 
The following shortcuts are supported:

~~~markdown
# Headers

**Bold text**

*Italic*

***Bold italic***

~~Strikethrough~~

- Bullet points

1. Numbered lists

[] Checkboxes

[]() Links

> Blockquote

`Inline code block`

```
Fenced Code block
```

--- Horizontal Rule
~~~

<img alt="Listing Advanced" src="/img/tutorial/listingDescription.png" width="800"/>

To upload images, it is recommended to use the insert image button on the editor instead of copy-and-pasting images. 

### Advanced settings
Click **Show advanced settings** for additional configurations.
<img alt="Listing Advanced" src="/img/tutorial/listingAdvanced.png" width="800"/>

* Active for sale: Whether your product will be active for sale immediately affer creation (default: yes)
* Auto expiration: Whether your listing automatically delist for sale after a certain tournament round (default: no)
* Use client-side encryption: Whether to encrypt artifact files with buyer's public key (default: yes). [Learn more about encryption](/updates/encryption)
* Webhook url: Webhook to trigger auto uploads. [Learn more about webhook](/docs/tutorial-extras/api-automation#webhook-trigger)
* Featured products: Select from your other listings to be featured in this product's page

### Pricing options
<img alt="Listing Option" src="/img/tutorial/listingOption.png" width="800"/>

* Platform
    - `On-Platform`: Product is sold on NumerBay with full features (recommended)
    - `Off-Platform`: Product only links to an external listing page
* Total price: Total price for the option including all bundled quantities. 
* Number of bundled rounds: Number of tournament rounds bundled into this pricing option.
* Listing mode:
    - `File Mode`: Buyers can download artifact files and optionally designate a model slot for submission. You can upload artifacts to NumerBay or add external file URLs
    - `Stake Only Mode`: Submit for buyers automatically without distributing artifact files, without stake limit. You must upload artifacts to NumerBay. [only available for "numerai-predictions" and "signals-predictions" categories]
    - `Stake Only Mode with Limit`: Submit for buyers automatically without distributing artifact files, with a stake limit (in NMR). You must upload artifacts to NumerBay. [only available for "numerai-predictions" and "signals-predictions" categories]

### Reward coupons on sale
If you want to reward coupons to buyers meeting certain conditions, tick the **Reward coupons to buyers** box and configure as shown below.

You can also [create coupons manually](/docs/tutorial-basics/sell-a-product#create-coupons-manually) for specific users.

<img alt="Listing Coupon Specs" src="/img/tutorial/listingCouponSpecs.png" width="800"/>

* Min spend for reward
    - Minimum spend in NMR required for the currently edited product to reward the buyer with a coupon
    - This is not the min spend for the actual coupon rewarded
* Applicable products: Your listings that the rewarded coupons can be applied to
* Discount %: 0-100 integer, 100 being free
* Max discount: Maximum discount cap in NMR for the rewarded coupons
* Min spend for redemption: Minimum spend in NMR required for the applicable products in order for a buyer to use the rewarded coupons

:::info

Coupons generated using this reward mechanism are bound to the specific buyers and cannot be transferred or used by others.

:::

## Upload artifacts
:::tip Advanced tip

You can automate upload via NumerBay Python / Cli Client, head over to the [API Tutorial](/docs/tutorial-extras/api-automation) for examples.

:::

:::caution

After submitting to NumerBay, you still need to submit your files to Numerai. NumerBay does not forward submissions to Numerai for sellers.

:::

After tournament round opens, you need to upload artifact files to NumerBay to fulfill your active orders. 
Click the **upload** button next to your product in the **[My listings](https://numerbay.ai/listings)** page for the upload panel.

### For products using client-side encryption (default)
:::tip Advanced tip

You can automate the per-order uploads for encrypted listings using webhook. [Learn more about webhook](/docs/tutorial-extras/api-automation#webhook-trigger)

:::

For encrypted listings, upload is only possible when you have active sale orders. 

Each file upload is repeated for every active sale order at the time of upload, both the web UI and Python client automate this 
repetition. The process needs to be manually repeated for any subsequent sale order after the previous upload. 

For Stake Only sales and sales where the buyer designated an auto-submission slot, any Numerai submission is also done
during the upload in your browser instead of being automated by the NumerBay backend.

Once you upload for at least one buyer, your product will be tagged with a `Ready` badge in the catalog page. However, you still need to deliver for any subsequent order.

<img alt="Listing Order Artifacts" src="/img/tutorial/listingOrderArtifacts.png" width="800"/>

### For products without client-side encryption
If you opted not to use client-side encryption, upload can happen at any time. It is recommended to upload artifacts after tournament round opens and regardless if you have active buyers.

Once artifacts are uploaded, your product will be tagged with a `Ready` badge in the catalog page.

## Manage sales
Your sales are viewable in the **[Sales](https://numerbay.ai/sales)** page. You can click on the order IDs to view order details.

![Sales History](/img/tutorial/salesHistory.png)

## Create coupons manually

In the **[My Coupons](https://numerbay.ai/coupons)** page you can create coupons manually for specific buyers, this can be useful when you have other payment arrangements and simply want to use NumerBay as a delivery service.

<img alt="Coupon Creation" src="/img/tutorial/couponCreation.png" width="800"/>

* Username of recipient: Case-sensitive NumerBay username 
* Applicable products: Your listings that the coupons can be applied to
* Discount %: 0-100 integer, 100 being free
* Number of redemptions: Number of times the coupon code can be redeemed
* Max discount: Maximum discount cap in NMR for the rewarded coupons
* Min spend for redemption: Minimum spend in NMR required for the applicable products in order for a buyer to use the rewarded coupons
* Custom coupon code: optional custom coupon code, needs to have at least 6 characters
* Expiration date: optional expiration date of the coupons

You can also delete created coupons:

<img alt="Coupon Deletion" src="/img/tutorial/couponDeletion.png" width="800"/>
