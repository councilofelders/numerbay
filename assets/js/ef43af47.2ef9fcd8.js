"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[329],{3905:function(e,t,a){a.d(t,{Zo:function(){return p},kt:function(){return y}});var n=a(7294);function r(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function o(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function i(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?o(Object(a),!0).forEach((function(t){r(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):o(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function l(e,t){if(null==e)return{};var a,n,r=function(e,t){if(null==e)return{};var a,n,r={},o=Object.keys(e);for(n=0;n<o.length;n++)a=o[n],t.indexOf(a)>=0||(r[a]=e[a]);return r}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)a=o[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(r[a]=e[a])}return r}var s=n.createContext({}),u=function(e){var t=n.useContext(s),a=t;return e&&(a="function"==typeof e?e(t):i(i({},t),e)),a},p=function(e){var t=u(e.components);return n.createElement(s.Provider,{value:t},e.children)},d="mdxType",c={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},m=n.forwardRef((function(e,t){var a=e.components,r=e.mdxType,o=e.originalType,s=e.parentName,p=l(e,["components","mdxType","originalType","parentName"]),d=u(a),m=r,y=d["".concat(s,".").concat(m)]||d[m]||c[m]||o;return a?n.createElement(y,i(i({ref:t},p),{},{components:a})):n.createElement(y,i({ref:t},p))}));function y(e,t){var a=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var o=a.length,i=new Array(o);i[0]=m;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[d]="string"==typeof e?e:r,i[1]=l;for(var u=2;u<o;u++)i[u]=a[u];return n.createElement.apply(null,i)}return n.createElement.apply(null,a)}m.displayName="MDXCreateElement"},3538:function(e,t,a){a.r(t),a.d(t,{assets:function(){return s},contentTitle:function(){return i},default:function(){return c},frontMatter:function(){return o},metadata:function(){return l},toc:function(){return u}});var n=a(3117),r=(a(7294),a(3905));const o={sidebar_position:2},i="Buy a Product",l={unversionedId:"tutorial-basics/buy-a-product",id:"tutorial-basics/buy-a-product",title:"Buy a Product",description:"This tutorial walks you through the process of buying a product on NumerBay.",source:"@site/docs/tutorial-basics/buy-a-product.md",sourceDirName:"tutorial-basics",slug:"/tutorial-basics/buy-a-product",permalink:"/docs/tutorial-basics/buy-a-product",draft:!1,editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/docs/tutorial-basics/buy-a-product.md",tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"tutorialSidebar",previous:{title:"Set up Account",permalink:"/docs/tutorial-basics/set-up-account"},next:{title:"Sell a Product",permalink:"/docs/tutorial-basics/sell-a-product"}},s={},u=[{value:"Browse products",id:"browse-products",level:2},{value:"Key product properties",id:"key-product-properties",level:3},{value:"Checkout and payment",id:"checkout-and-payment",level:2},{value:"Place an order",id:"place-an-order",level:3},{value:"Payment",id:"payment",level:3},{value:"Download artifacts",id:"download-artifacts",level:2},{value:"Decryption",id:"decryption",level:3},{value:"Submission",id:"submission",level:2},{value:"Change auto-submit model slot",id:"change-auto-submit-model-slot",level:3},{value:"Manage coupons",id:"manage-coupons",level:2}],p={toc:u},d="wrapper";function c(e){let{components:t,...o}=e;return(0,r.kt)(d,(0,n.Z)({},p,o,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"buy-a-product"},"Buy a Product"),(0,r.kt)("p",null,"This tutorial walks you through the process of buying a product on NumerBay."),(0,r.kt)("admonition",{type:"note"},(0,r.kt)("p",{parentName:"admonition"},"You need to have a ",(0,r.kt)("a",{parentName:"p",href:"./set-up-account"},"NumerBay account")," with Numerai API Key in order to make purchases on NumerBay."),(0,r.kt)("p",{parentName:"admonition"},"It is also recommended to ",(0,r.kt)("a",{parentName:"p",href:"/docs/tutorial-basics/set-up-account#generate-key-pair"},"Generate a key pair")," as\nsome products use client-side encryption.")),(0,r.kt)("admonition",{type:"tip"},(0,r.kt)("p",{parentName:"admonition"},"Some products use client-side encryption and are delivered on a per-order basis. It is therefore recommended to buy before\nthe tournaments start."),(0,r.kt)("p",{parentName:"admonition"},"Learn more about ",(0,r.kt)("a",{parentName:"p",href:"/updates/encryption"},"client-side encryption"),".")),(0,r.kt)("h2",{id:"browse-products"},"Browse products"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("a",{parentName:"li",href:"https://numerbay.ai/explore/numerai-predictions"},"Numerai Tournament Predictions")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("a",{parentName:"li",href:"https://numerbay.ai/explore/numerai-models"},"Numerai Tournament Models")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("a",{parentName:"li",href:"https://numerbay.ai/explore/signals-predictions"},"Signals Tournament Predictions")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("a",{parentName:"li",href:"https://numerbay.ai/explore/signals-data"},"Signals Tournament Data")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("a",{parentName:"li",href:"https://numerbay.ai/explore/onlyfams"},"NFTs and Others"))),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Product Catalog",src:a(8221).Z,width:"1755",height:"1630"})),(0,r.kt)("h3",{id:"key-product-properties"},"Key product properties"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"Category",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"numerai-predictions"),": ",(0,r.kt)("a",{parentName:"li",href:"https://numer.ai/tournament"},'Numerai "Classic" tournament')," submission files, per-round category"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"numerai-model"),": Model binary file, training scripts or Jupyter notebooks for the associated model"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"signals-predictions"),": ",(0,r.kt)("a",{parentName:"li",href:"https://signals.numer.ai/tournament"},"Signals tournament")," submission files, per-round category"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"signals-data"),": Data files used to train the associated Signals model or other files useful for Signals modeling, per-round category"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"onlyfams-*"),": Anything other than the above such as meme NFTs, clothing, etc."))),(0,r.kt)("li",{parentName:"ul"},"Platform",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"On-Platform"),": Product is sold on NumerBay with full features"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"Off-Platform"),": Product only links to an external listing page"))),(0,r.kt)("li",{parentName:"ul"},"Listing Mode:",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"File Mode"),": You can download artifact files and optionally designate a model slot for submission"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"Stake Only Mode"),": Submit for you automatically without distributing artifact files, without stake limit. ",'[only available for "numerai-predictions" and "signals-predictions" categories]'),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"Stake Only Mode with Limit"),": Submit for you automatically without distributing artifact files, with a stake limit (in NMR). ",'[only available for "numerai-predictions" and "signals-predictions" categories]'))),(0,r.kt)("li",{parentName:"ul"},"Ready: If a ",(0,r.kt)("inlineCode",{parentName:"li"},"Ready")," badge is shown for a product, this means the product artifact files are ready for download immediately after purchasing (for unencrypted listings), or the seller has delivered for at least one buyer (for encrypted listings). If the ready badge is not shown or if the product uses encryption, you will need to wait for seller to upload after your purchase.\nThis badge is reset every round for per-round categories ",(0,r.kt)("inlineCode",{parentName:"li"},"numerai-predictions"),", ",(0,r.kt)("inlineCode",{parentName:"li"},"signals-predictions")," and ",(0,r.kt)("inlineCode",{parentName:"li"},"signals-data"),"."),(0,r.kt)("li",{parentName:"ul"},"Daily: If a ",(0,r.kt)("inlineCode",{parentName:"li"},"Daily")," badge is shown for a product, this product uploads for every round, otherwise the product might only upload on weekends.")),(0,r.kt)("h2",{id:"checkout-and-payment"},"Checkout and payment"),(0,r.kt)("h3",{id:"place-an-order"},"Place an order"),(0,r.kt)("p",null,"Navigate to a product you are interested in, and click ",(0,r.kt)("strong",{parentName:"p"},"Buy"),". Then, select your preferred ",(0,r.kt)("strong",{parentName:"p"},"product option")," and the ",(0,r.kt)("strong",{parentName:"p"},"quantity (number of rounds)")," of that product option you would like to buy, read the disclaimer, and click ",(0,r.kt)("strong",{parentName:"p"},"Place an Order"),"."),(0,r.kt)("p",null,"If the product you are buying is a tournament submission, you can select a model slot to ",(0,r.kt)("strong",{parentName:"p"},"auto-submit"),' to. This is mandatory if the product is sold in "Stake Only" mode. '),(0,r.kt)("p",null,"If you have a valid discount ",(0,r.kt)("strong",{parentName:"p"},"coupon")," for the product, you can also apply it before placing an order."),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Product Quantity",src:a(9900).Z,width:"1717",height:"1500"})),(0,r.kt)("admonition",{type:"info"},(0,r.kt)("p",{parentName:"admonition"},"The ",(0,r.kt)("strong",{parentName:"p"},"quantity")," selected here is the number of tournament rounds based on the pricing option selected."),(0,r.kt)("p",{parentName:"admonition"},"Each week consists of 5 daily rounds, therefore enter 5 if you want to buy for a week. Alternatively you can use the advanced calendar date picker to select specific days to buy.")),(0,r.kt)("h3",{id:"payment"},"Payment"),(0,r.kt)("p",null,"After placing an order, you will see the payment instructions. Copy the address and amount to make a payment via your ",(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("a",{parentName:"strong",href:"https://numer.ai/wallet"},"Numerai wallet")),". You can leave this page if you want to."),(0,r.kt)("p",null,"Your orders are viewable in the ",(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("a",{parentName:"strong",href:"https://numerbay.ai/purchases"},"Purchases"))," page. Orders are typically confirmed within 30 seconds after payments are confirmed on-chain."),(0,r.kt)("admonition",{type:"caution"},(0,r.kt)("p",{parentName:"admonition"},"Payment needs to be made ",(0,r.kt)("strong",{parentName:"p"},"in full")," and ",(0,r.kt)("strong",{parentName:"p"},"in one single transaction")," from your ",(0,r.kt)("strong",{parentName:"p"},"Numerai wallet")," within ",(0,r.kt)("strong",{parentName:"p"},"45 minutes")," after order creation. If no matching payment transaction is found within the time limit, the order will expire."),(0,r.kt)("p",{parentName:"admonition"},"NumerBay currently does not fully support payment from arbitrary NMR wallet, ",(0,r.kt)("strong",{parentName:"p"},"DO NOT")," send NMR from your own wallet or exchange wallets."),(0,r.kt)("p",{parentName:"admonition"},"If you need help, please contact support by posting in the #numerbay channel in ",(0,r.kt)("a",{parentName:"p",href:"https://discord.gg/numerai"},"Numerai Discord Server"),".")),(0,r.kt)("img",{alt:"Product Payment",src:"/img/tutorial/productPayment.png",width:"450"}),(0,r.kt)("h2",{id:"download-artifacts"},"Download artifacts"),(0,r.kt)("p",null,"Head to the ",(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("a",{parentName:"strong",href:"https://numerbay.ai/purchases"},"Purchases"))," page. Click the ",(0,r.kt)("strong",{parentName:"p"},"download")," button next to your order to view the list of downloadable artifact files. Then, click on the file name to download the file."),(0,r.kt)("p",null,"If you purchased before Numerai tournament round starts, artifacts may not be available for immediate download.\nSellers will be notified of your order and will upload artifacts once the tournament round starts. You cannot download artifacts for past rounds."),(0,r.kt)("p",null,"It is recommended to place orders early so sellers would have enough time to fulfill the upload."),(0,r.kt)("admonition",{title:"Advanced tip",type:"tip"},(0,r.kt)("p",{parentName:"admonition"},"You can also download via the NumerBay Python / Cli Client, head over to the ",(0,r.kt)("a",{parentName:"p",href:"/docs/tutorial-extras/download-automation"},"API Tutorial")," for examples.")),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Order List",src:a(4625).Z,width:"1762",height:"1321"})),(0,r.kt)("h3",{id:"decryption"},"Decryption"),(0,r.kt)("p",null,"If the product you bought uses client-side encryption, you may be prompted by MetaMask to decrypt your NumerBay key in order to decrypt the file."),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Decrypt",src:a(227).Z,width:"1518",height:"970"})),(0,r.kt)("h2",{id:"submission"},"Submission"),(0,r.kt)("p",null,"If you made your order with auto-submission set up during checkout, submissions will be automatically done for you after tournament round open and after the seller submits their files."),(0,r.kt)("h3",{id:"change-auto-submit-model-slot"},"Change auto-submit model slot"),(0,r.kt)("p",null,"You can change the auto-submit destination model in the order details panel which can be opened by clicking on the ",(0,r.kt)("strong",{parentName:"p"},"View details")," button in the ",(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("a",{parentName:"strong",href:"https://numerbay.ai/purchases"},"Purchases"))," page."),(0,r.kt)("img",{alt:"Change Auto-submit",src:"/img/tutorial/changeAutosubmit.png",width:"700"}),(0,r.kt)("h2",{id:"manage-coupons"},"Manage coupons"),(0,r.kt)("p",null,"Some sellers may reward you with coupons for your orders. Your coupons are viewable in the ",(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("a",{parentName:"strong",href:"https://numerbay.ai/coupons"},"My Coupons"))," page. "),(0,r.kt)("img",{alt:"My Coupons",src:"/img/tutorial/myCoupons.png",width:"800"}))}c.isMDXComponent=!0},227:function(e,t,a){t.Z=a.p+"assets/images/decrypt-87509fa401f811b43a4198ba175dfdb4.png"},4625:function(e,t,a){t.Z=a.p+"assets/images/orderList-932ec9f5771f519ddf18c6f17b68f154.png"},8221:function(e,t,a){t.Z=a.p+"assets/images/productCatalog-2e04faaa5c4ffcb47029e93d13853764.png"},9900:function(e,t,a){t.Z=a.p+"assets/images/productQuantity-f3d16f3987efe2de2a376e0bfefa3e4e.png"}}]);