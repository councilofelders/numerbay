"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[174],{4395:function(e){e.exports=JSON.parse('{"blogPosts":[{"id":"daily-sales","metadata":{"permalink":"/updates/daily-sales","editUrl":"https://github.com/councilofelders/numerbay/tree/master/docs/updates/2022-12-16-daily-sales.md","source":"@site/updates/2022-12-16-daily-sales.md","title":"Daily Sales","description":"Numerai moved towards daily tournament rounds since late Oct 2022 and will soon enable payout for the weekday rounds.","date":"2022-12-16T00:00:00.000Z","formattedDate":"December 16, 2022","tags":[{"label":"update","permalink":"/updates/tags/update"}],"readingTime":1.97,"hasTruncateMarker":false,"authors":[{"name":"ResTrading","title":"Maintainer of NumerBay","url":"https://github.com/restrading","imageURL":"https://github.com/restrading.png","key":"restrading"}],"frontMatter":{"slug":"daily-sales","title":"Daily Sales","authors":["restrading"],"tags":["update"]},"nextItem":{"title":"Encryption Update","permalink":"/updates/encryption-v2"}},"content":"Numerai moved towards [daily tournament rounds](https://forum.numer.ai/t/daily-tournaments/5766) since late Oct 2022 and will soon enable payout for the weekday rounds. \\n\\nNumerBay sales remained weekly up until now and the platform is finally making the transition towards daily as well.\\n\\n## What\'s the impact\\n\\nBuyers will now place orders using a calendar date picker to select the rounds to purchase. \\nSelect **Saturdays** to buy the weekend rounds and **Tue-Fri** to buy the weekday rounds. \\nOrder rounds are no longer required to be consecutive. \\nThe same product can also be bought multiple times during the same week so long as the rounds don\'t overlap. \\nOnly one pending order is allowed at a time.\\n\\n<img alt=\\"Daily Order\\" src=\\"/img/update/dailyOrder.png\\" width=\\"450\\"/>\\n\\nSellers with existing products will remain weekend-sales-only and can choose to enable weekday (daily) sales in the Edit Listing page. \\nNew products created will enable weekday sales by default and can be switched off during listing creation.\\n\\n![Daily Option](/img/update/dailyOption.png)\\n\\nThere was no change to the NumerBay submission endpoints and users\' existing pipelines are expected to work normally.\\n\\n\\n## Q&A\\n### I\'m an existing seller, will my automation pipeline fail during weekdays if I do not enable daily sales?\\nNo, it should work normally. No order can be placed for your product for weekday rounds if you do not enable daily sales, therefore your webhook shouldn\'t be triggered in the first place. \\nIf you use the same automation for Numerai and NumerBay, any such attempt to upload will just result in no-op since there\'s no order for the weekday rounds, the effect is equivalent to trying to upload for weekend rounds when you do not have any active order. \\n\\n### I\'m a buyer, how do I know if a product supports weekday rounds?\\nProducts with weekday sales enabled will show a blue \\"daily\\" badge in the products catalog page. \\nIn addition, if you try to place an order for a product not supporting weekday rounds, you will get an error saying *This product is not available for weekday sale*.\\n\\n<img alt=\\"Daily Badge\\" src=\\"/img/update/dailyBadge.png\\" width=\\"450\\"/>\\n\\n### What happened to the round rollover embargo?\\nThere used to be a 30-minute freeze at the end of the weekend submission window. \\nAfter this change, there would no long be any freeze of activity near the deadline. However, it is recommended not to submit last minute as some NumerBay processes may take time to complete."},{"id":"encryption-v2","metadata":{"permalink":"/updates/encryption-v2","editUrl":"https://github.com/councilofelders/numerbay/tree/master/docs/updates/2022-09-24-encryption-v2.md","source":"@site/updates/2022-09-24-encryption-v2.md","title":"Encryption Update","description":"There\'s an update to NumerBay\'s encryption mechanism due to MetaMask deprecating some methods.","date":"2022-09-24T00:00:00.000Z","formattedDate":"September 24, 2022","tags":[{"label":"update","permalink":"/updates/tags/update"}],"readingTime":1.75,"hasTruncateMarker":false,"authors":[{"name":"ResTrading","title":"Maintainer of NumerBay","url":"https://github.com/restrading","imageURL":"https://github.com/restrading.png","key":"restrading"}],"frontMatter":{"slug":"encryption-v2","title":"Encryption Update","authors":["restrading"],"tags":["update"]},"prevItem":{"title":"Daily Sales","permalink":"/updates/daily-sales"},"nextItem":{"title":"Client-side Encryption Release","permalink":"/updates/encryption"}},"content":"There\'s an update to NumerBay\'s encryption mechanism due to MetaMask deprecating some methods.\\n\\n## What\'s the impact\\n\\nUsers are encouraged to generate a new key pair by clicking the **Replace key pair** in the **[Edit profile page](https://numerbay.ai/account)**.\\n\\nThis action is not compulsory at this point.\\n\\nApart from above, there is no change to user workflow.\\n\\n:::caution\\n\\nAfter generating a new key pair, you will lose access to all existing files encrypted with the old key. It is recommended to replace key pair only when you don\'t have active orders.\\n\\nIf your workflow uses the exported key file, you need to export it again after replacing the keys.\\n\\n:::\\n\\n\\n## Q&A\\n### I\'m an existing user, do I have to change my workflow due to this release?\\nNo, you don\'t have to change anything. Change of encryption key is optional at this point.\\n\\n### When will this change become compulsory?\\nWhen MetaMask announces the timeline for the removal of the deprecated methods, another update will be posted.\\n\\n### I use the NumerBay python client, do I need to change my code?\\nNo, you don\'t need to change your code. This update is related to the change of storage encryption mechanism for the encryption key only and does not change how files are encrypted or decrypted.\\n\\nHowever, if your code uses the exported key file for file decryption, you need to **export it again** after regenerating the key pair and replace the old key file in your repository.\\n\\n### What\'s the change?\\nThe existing encryption mechanism (legacy mechanism) on NumerBay encrypts the generated encryption key with user\'s MetaMask wallet and stores the encrypted key on the server, and when need it is then decrypted using the MetaMask wallet. \\nThis process involes MetaMask\'s `eth_getEncryptionPublicKey` and `eth_decrypt` methods which have [recently been deprecated](https://github.com/MetaMask/metamask-extension/issues/15379).\\n\\nThe new mechanism (encryption v2) instead encrypts the encryption key with a storage key derived from signature by having the user sign a random salt. This gets around the above two deprecated methods and may also enable support for some hardware wallets which don\'t allow direct access to their public keys."},{"id":"encryption","metadata":{"permalink":"/updates/encryption","editUrl":"https://github.com/councilofelders/numerbay/tree/master/docs/updates/2022-02-02-encryption.md","source":"@site/updates/2022-02-02-encryption.md","title":"Client-side Encryption Release","description":"NumerBay now supports client-side encryption for delivery of artifact files.","date":"2022-02-02T00:00:00.000Z","formattedDate":"February 2, 2022","tags":[{"label":"update","permalink":"/updates/tags/update"}],"readingTime":2.99,"hasTruncateMarker":false,"authors":[{"name":"ResTrading","title":"Maintainer of NumerBay","url":"https://github.com/restrading","imageURL":"https://github.com/restrading.png","key":"restrading"}],"frontMatter":{"slug":"encryption","title":"Client-side Encryption Release","authors":["restrading"],"tags":["update"]},"prevItem":{"title":"Encryption Update","permalink":"/updates/encryption-v2"}},"content":"NumerBay now supports **client-side encryption** for delivery of artifact files. \\n\\nEach file will be uploaded for each active order separately and all files are encrypted in browser / Python client \\nwith buyer\'s public key before transmission. This is a small first step towards decentralization for NumerBay.\\n\\nNew listings will default to using encryption, but the legacy option continues to be available.\\n\\n\\n## What\'s different\\nThe following table outlines the key differences for listings with and without client-side encryption:\\n\\n| Item                         | With Client-side Encryption | Without Client-side Encryption |\\n| ---------------------------- | :-------------------------: | :----------------------------: |\\n| 1. One-off Upload            |                             | :heavy_check_mark:             |\\n| 2. Auto Numerai Submission   | :heavy_check_mark:*****     | :heavy_check_mark:             |\\n| 3. External URL Artifact     |                             | :heavy_check_mark:             |\\n| 4. Requires MetaMask         | :heavy_check_mark:          |                                |\\n\\n\\n1. For encrypted listings, upload is only possible when you have active sale orders.\\n   Upload is repeated for every active sale order at the time of upload, and\\n   the process needs to be repeated for any subsequent sale order. Both the web UI and Python client automates this\\n   by repeating the encryption and upload during upload. In the future, polling listener for Python client \\n   or browser notification might be added to make automation easier.\\n2. [*] Numerai submission for encrypted artifact is done during seller upload for each order as a separate \\n   special artifact, instead of being automated by the NumerBay backend. Therefore, for buyers this has reliability\\n   implication. Soon NumerBay will add reminder emails to sellers for outstanding file delivery and submissions.\\n3. Encrypted listings do not support adding external URLs as artifacts, only file upload is allowed.\\n4. MetaMask connection is required due to the need for generating encryption keys and performing decryption.\\n\\n\\n## Q&A\\n### I\'m an existing seller, do I have to change my workflow due to this release?\\nNo, you don\'t have to change anything. Encryption is optional at this point.\\n\\nYou can continue to use the existing mechanism for artifact delivery.\\nThere is no plan to disable the existing artifact APIs, \\ntherefore your existing automation pipelines will be compatible with this change.\\n\\n### I\'m a seller, how do I start using encryption?\\nIn the [listing edit panel](https://numerbay.ai/listings) for your product, select the \\n**Use Client-side Encryption** option. That\'s it! Files will be encrypted for new sale orders, \\nexisting active sales will not be affected. \\nYou can use the [Python client](/docs/tutorial-extras/api-automation) to automate encryption and file upload.\\nA tutorial for selling is available [here](/docs/tutorial-basics/sell-a-product#for-products-using-client-side-encryption).\\n\\n### I\'m a buyer, what do I need to do?\\nAn encryption key pair is required for encryption on the seller side and for decryption after you download the files, \\nplease head to the [profile page](https://numerbay.ai/account) to generate a key pair. Export the key file for \\nsafe-keeping and for use with the [Python client](/docs/tutorial-extras/download-automation). \\nA tutorial for buying is available [here](/docs/tutorial-basics/buy-a-product#decryption).\\n\\n### How does the encryption work?\\nA 32-byte key pair is generated in your browser. Its private key is immediately encrypted with your MetaMask account.\\nThe encrypted private key together with the public key are stored in your user profile on the NumerBay server. NumerBay\\ndoes not have access to your unencrypted private key.\\n\\nWhen you make an order for an encrypted product, your public key is shared with the seller which they will use to \\nencrypt any artifact file that will be delivered to you. \\n\\nWhen downloading a file in browser, file is first downloaded into browser cache. You will then be prompted by MetaMask\\nto decrypt your NumerBay private key, and the file is then decrypted with the NumerBay private key and save as a file."}]}')}}]);