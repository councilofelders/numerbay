---
slug: encryption-v2
title: Encryption Update
authors: [restrading]
tags: [update]
---

There's an update to NumerBay's encryption mechanism due to MetaMask deprecating some methods.

## What's the impact

Users are encouraged to generate a new key pair by clicking the **Replace key pair** in the **[Edit profile page](https://numerbay.ai/account)**.

This action is not compulsory at this point.

Apart from above, there is no change to user workflow.

:::caution

After generating a new key pair, you will lose access to all existing files encrypted with the old key. It is recommended to replace key pair only when you don't have active orders.

If your workflow uses the exported key file, you need to export it again after replacing the keys.

:::


## Q&A
### I'm an existing user, do I have to change my workflow due to this release?
No, you don't have to change anything. Change of encryption key is optional at this point.

### When will this change become compulsory?
When MetaMask announces the timeline for the removal of the deprecated methods, another update will be posted.

### I use the NumerBay python client, do I need to change my code?
No, you don't need to change your code. This update is related to the change of storage encryption mechanism for the encryption key only and does not change how files are encrypted or decrypted.

However, if your code uses the exported key file for file decryption, you need to **export it again** after regenerating the key pair and replace the old key file in your repository.

### What's the change?
The existing encryption mechanism (legacy mechanism) on NumerBay encrypts the generated encryption key with user's MetaMask wallet and stores the encrypted key on the server, and when need it is then decrypted using the MetaMask wallet. 
This process involes MetaMask's `eth_getEncryptionPublicKey` and `eth_decrypt` methods which have [recently been deprecated](https://github.com/MetaMask/metamask-extension/issues/15379).

The new mechanism (encryption v2) instead encrypts the encryption key with a storage key derived from signature by having the user sign a random salt. This gets around the above two deprecated methods and may also enable support for some hardware wallets which don't allow direct access to their public keys.
