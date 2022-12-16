---
slug: daily-sales
title: Daily Sales
authors: [restrading]
tags: [update]
---

Numerai moved towards [daily tournament rounds](https://forum.numer.ai/t/daily-tournaments/5766) since late Oct 2022 and will soon enable payout for the weekday rounds. 

NumerBay sales remained weekly up until now and the platform is finally making the transition towards daily as well.

## What's the impact

Buyers will now place orders using a calendar date picker to select the rounds to purchase. 
Select **Saturdays** to buy the weekend rounds and **Tue-Fri** to buy the weekday rounds. 
Order rounds are no longer required to be consecutive. 
The same product can also be bought multiple times during the same week so long as the rounds don't overlap. 
Only one pending order is allowed at a time.

<img alt="Daily Order" src="/img/update/dailyOrder.png" width="450"/>

Sellers with existing products will remain weekend-sales-only and can choose to enable weekday (daily) sales in the Edit Listing page. 
New products created will enable weekday sales by default and can be switched off during listing creation.

![Daily Option](/img/update/dailyOption.png)

There was no change to the NumerBay submission endpoints and users' existing pipelines are expected to work normally.


## Q&A
### I'm an existing seller, will my automation pipeline fail during weekdays if I do not enable daily sales?
No, it should work normally. No order can be placed for your product for weekday rounds if you do not enable daily sales, therefore your webhook shouldn't be triggered in the first place. 
If you use the same automation for Numerai and NumerBay, any such attempt to upload will just result in no-op since there's no order for the weekday rounds, the effect is equivalent to trying to upload for weekend rounds when you do not have any active order. 

### I'm a buyer, how do I know if a product supports weekday rounds?
Products with weekday sales enabled will show a blue "daily" badge in the products catalog page. 
In addition, if you try to place an order for a product not supporting weekday rounds, you will get an error saying *This product is not available for weekday sale*.

<img alt="Daily Badge" src="/img/update/dailyBadge.png" width="450"/>

### What happened to the round rollover embargo?
There used to be a 30-minute freeze at the end of the weekend submission window. 
After this change, there would no long be any freeze of activity near the deadline. However, it is recommended not to submit last minute as some NumerBay processes may take time to complete.