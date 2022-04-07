---
slug: encryption
title: Client-side Encryption Release
authors: [restrading]
tags: [update]
---

NumerBay now supports **client-side encryption** for delivery of artifact files. 

Each file will be uploaded for each active order separately and all files are encrypted in browser / Python client 
with buyer's public key before transmission. This is a small first step towards decentralization for NumerBay.

New listings will default to using encryption, but the legacy option continues to be available.


## What's different
The following table outlines the key differences for listings with and without client-side encryption:

| Item                         | With Client-side Encryption | Without Client-side Encryption |
| ---------------------------- | :-------------------------: | :----------------------------: |
| 1. One-off Upload            |                             | :heavy_check_mark:             |
| 2. Auto Numerai Submission   | :heavy_check_mark:*****     | :heavy_check_mark:             |
| 3. External URL Artifact     |                             | :heavy_check_mark:             |
| 4. Requires MetaMask         | :heavy_check_mark:          |                                |


1. For encrypted listings, upload is only possible when you have active sale orders.
   Upload is repeated for every active sale order at the time of upload, and
   the process needs to be repeated for any subsequent sale order. Both the web UI and Python client automates this
   by repeating the encryption and upload during upload. In the future, polling listener for Python client 
   or browser notification might be added to make automation easier.
2. [*] Numerai submission for encrypted artifact is done during seller upload for each order as a separate 
   special artifact, instead of being automated by the NumerBay backend. Therefore, for buyers this has reliability
   implication. Soon NumerBay will add reminder emails to sellers for outstanding file delivery and submissions.
3. Encrypted listings do not support adding external URLs as artifacts, only file upload is allowed.
4. MetaMask connection is required due to the need for generating encryption keys and performing decryption.


## Q&A
### I'm an existing seller, do I have to change my workflow due to this release?
No, you don't have to change anything. Encryption is optional at this point.

You can continue to use the existing mechanism for artifact delivery.
There is no plan to disable the existing artifact APIs, 
therefore your existing automation pipelines will be compatible with this change.

### I'm a seller, how do I start using encryption?
In the [listing edit panel](https://numerbay.ai/listings) for your product, select the 
**Use Client-side Encryption** option. That's it! Files will be encrypted for new sale orders, 
existing active sales will not be affected. 
You can use the [Python client](/docs/tutorial-extras/api-automation) to automate encryption and file upload.
A tutorial for selling is available [here](/docs/tutorial-basics/sell-a-product#for-products-using-client-side-encryption).

### I'm a buyer, what do I need to do?
An encryption key pair is required for encryption on the seller side and for decryption after you download the files, 
please head to the [profile page](https://numerbay.ai/account) to generate a key pair. Export the key file for 
safe-keeping and for use with the [Python client](/docs/tutorial-extras/download-automation). 
A tutorial for buying is available [here](/docs/tutorial-basics/buy-a-product#decryption).

### How does the encryption work?
A 32-byte key pair is generated in your browser. Its private key is immediately encrypted with your MetaMask account.
The encrypted private key together with the public key are stored in your user profile on the NumerBay server. NumerBay
does not have access to your unencrypted private key.

When you make an order for an encrypted product, your public key is shared with the seller which they will use to 
encrypt any artifact file that will be delivered to you. 

When downloading a file in browser, file is first downloaded into browser cache. You will then be prompted by MetaMask
to decrypt your NumerBay private key, and the file is then decrypted with the NumerBay private key and save as a file.
