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
* Webhook url: webhook to trigger on new confirmed sale order. Useful for triggering auto uploading of files for encrypted listings.
  A `POST` request is made on each new sale with the following json body:
  ```json
  {
    "date": "2022-04-02T13:25:32.893448",
    "product_id": 4206,
    "product_category": "numerai-predictions",
    "product_name": "myproduct",
    "product_full_name": "numerai-predictions-myproduct",
    "model_id": "adabxxx-3acf-470e-8733-e4283261xxxx",
    "tournament": 8
  }
  ```
* Featured products: Select from your other listings to be featured in this product's page

### Pricing options
<img alt="Listing Option" src="/img/tutorial/listingOption.png" width="800"/>

* Platform
    - `On-Platform`: Product is sold on NumerBay with full features
    - `Off-Platform`: Product only links to an external listing page
* Listing mode:
    - `File Mode`: Buyers can download artifact files and optionally designate a model slot for submission. You can upload artifacts to NumerBay or add external file URLs
    - `Stake Only Mode`: Submit for buyers automatically without distributing artifact files, without stake limit. You must upload artifacts to NumerBay. [only available for "numerai-predictions" and "signals-predictions" categories]
    - `Stake Only Mode with Limit`: Submit for buyers automatically without distributing artifact files, with a stake limit (in NMR). You must upload artifacts to NumerBay. [only available for "numerai-predictions" and "signals-predictions" categories]
* Number of bundled rounds per unit sold: Number of tournament rounds bundled into this pricing option. 
* Total price: Total price for the option including all bundled quantities. 

:::info

Total number of rounds for an order will be `[order quantity] x [bundled number of rounds per unit]`

:::

### Reward coupons
If you want to reward coupons to buyers meeting certain conditions, tick the **Reward coupons to buyers** box and configure as shown below.

<img alt="Listing Coupon Specs" src="/img/tutorial/listingCouponSpecs.png" width="800"/>

* Min spend for reward
    - Minimum spend in NMR required for the currently edited product to reward the buyer with a coupon
    - This is not the min spend for the actual coupon rewarded
* Applicable products:
    - Your *other* listings that the rewarded coupon can be applied to
    - The currently edited product is always included in the applicable products list
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
For encrypted listings, upload is only possible when you have active sale orders. 

Each file upload is repeated for every active sale order at the time of upload, both the web UI and Python client automate this 
repetition. The process needs to be manually repeated for any subsequent sale order after the previous upload. 

For Stake Only sales and sales where the buyer designated an auto-submission slot, any Numerai submission is also done
during the upload in your browser instead of being automated by the NumerBay backend.

<img alt="Listing Order Artifacts" src="/img/tutorial/listingOrderArtifacts.png" width="800"/>

### For products without client-side encryption
If you opted not to use client-side encryption, upload can happen at any time. It is recommended to upload artifacts after tournament round opens and regardless if you have active buyers.

Once artifacts are uploaded, your product will be tagged with a `Instant` badge in the catalog page which might make it more likely to be purchased.

<img alt="Product Ready" src="/img/tutorial/productReady.png" width="600"/>

## Manage sales
Your sales are viewable in the **[Sales](https://numerbay.ai/sales)** page. You can click on the order IDs to view order details.

![Sales History](/img/tutorial/salesHistory.png)
