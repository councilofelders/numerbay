"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[756],{3905:function(e,t,a){a.d(t,{Zo:function(){return c},kt:function(){return m}});var n=a(7294);function i(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function r(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function o(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?r(Object(a),!0).forEach((function(t){i(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):r(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function l(e,t){if(null==e)return{};var a,n,i=function(e,t){if(null==e)return{};var a,n,i={},r=Object.keys(e);for(n=0;n<r.length;n++)a=r[n],t.indexOf(a)>=0||(i[a]=e[a]);return i}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(n=0;n<r.length;n++)a=r[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(i[a]=e[a])}return i}var s=n.createContext({}),u=function(e){var t=n.useContext(s),a=t;return e&&(a="function"==typeof e?e(t):o(o({},t),e)),a},c=function(e){var t=u(e.components);return n.createElement(s.Provider,{value:t},e.children)},d={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},p=n.forwardRef((function(e,t){var a=e.components,i=e.mdxType,r=e.originalType,s=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),p=u(a),m=i,f=p["".concat(s,".").concat(m)]||p[m]||d[m]||r;return a?n.createElement(f,o(o({ref:t},c),{},{components:a})):n.createElement(f,o({ref:t},c))}));function m(e,t){var a=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var r=a.length,o=new Array(r);o[0]=p;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l.mdxType="string"==typeof e?e:i,o[1]=l;for(var u=2;u<r;u++)o[u]=a[u];return n.createElement.apply(null,o)}return n.createElement.apply(null,a)}p.displayName="MDXCreateElement"},3934:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return l},contentTitle:function(){return s},metadata:function(){return u},toc:function(){return c},default:function(){return p}});var n=a(7462),i=a(3366),r=(a(7294),a(3905)),o=["components"],l={sidebar_position:3},s="Sell a Product",u={unversionedId:"tutorial-basics/sell-a-product",id:"tutorial-basics/sell-a-product",title:"Sell a Product",description:"You need to have a NumerBay account with Numerai API Key in order to sell on NumerBay.",source:"@site/docs/tutorial-basics/sell-a-product.md",sourceDirName:"tutorial-basics",slug:"/tutorial-basics/sell-a-product",permalink:"/docs/tutorial-basics/sell-a-product",editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/docs/tutorial-basics/sell-a-product.md",tags:[],version:"current",sidebarPosition:3,frontMatter:{sidebar_position:3},sidebar:"tutorialSidebar",previous:{title:"Buy a Product",permalink:"/docs/tutorial-basics/buy-a-product"},next:{title:"Vote",permalink:"/docs/tutorial-basics/vote"}},c=[{value:"Create listing",id:"create-listing",children:[{value:"Basic product information",id:"basic-product-information",children:[],level:3},{value:"Featured products",id:"featured-products",children:[],level:3},{value:"Pricing options",id:"pricing-options",children:[],level:3},{value:"Reward coupons",id:"reward-coupons",children:[],level:3}],level:2},{value:"Upload artifacts (WIP)",id:"upload-artifacts-wip",children:[],level:2},{value:"Manage sales (WIP)",id:"manage-sales-wip",children:[],level:2}],d={toc:c};function p(e){var t=e.components,l=(0,i.Z)(e,o);return(0,r.kt)("wrapper",(0,n.Z)({},d,l,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"sell-a-product"},"Sell a Product"),(0,r.kt)("div",{className:"admonition admonition-note alert alert--secondary"},(0,r.kt)("div",{parentName:"div",className:"admonition-heading"},(0,r.kt)("h5",{parentName:"div"},(0,r.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,r.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,r.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,r.kt)("div",{parentName:"div",className:"admonition-content"},(0,r.kt)("p",{parentName:"div"},"You need to have a ",(0,r.kt)("a",{parentName:"p",href:"./set-up-account"},"NumerBay account")," with Numerai API Key in order to sell on NumerBay."))),(0,r.kt)("h2",{id:"create-listing"},"Create listing"),(0,r.kt)("h3",{id:"basic-product-information"},"Basic product information"),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Listing Basic",src:a(7249).Z})),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"Category",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"numerai-predictions: ",(0,r.kt)("a",{parentName:"li",href:"https://numer.ai/tournament"},'Numerai "Classic" tournament')," submission files"),(0,r.kt)("li",{parentName:"ul"},"numerai-model: Model binary file, training scripts or Jupyter notebooks for the associated model"),(0,r.kt)("li",{parentName:"ul"},"signals-predictions: ",(0,r.kt)("a",{parentName:"li",href:"https://signals.numer.ai/tournament"},"Signals tournament")," submission files"),(0,r.kt)("li",{parentName:"ul"},"signals-data: Data files used to train the associated Signals model or other files useful for Signals modeling"),(0,r.kt)("li",{parentName:"ul"},"onlyfams-*: anything other than the above such as meme NFTs, clothing, etc."))),(0,r.kt)("li",{parentName:"ul"},"Product name:",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"For tournament categories this is a dropdown of Numerai models, select one"),(0,r.kt)("li",{parentName:"ul"},"For onlyfams categories, enter an alphanumeric product name"))),(0,r.kt)("li",{parentName:"ul"},"Avatar image URL:",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"This defaults to your numerai model avatar after selecting the model"),(0,r.kt)("li",{parentName:"ul"},"This must be an HTTPS URL"))),(0,r.kt)("li",{parentName:"ul"},"Active / Inactive: Whether your product will be active for sale immediately affer creation"),(0,r.kt)("li",{parentName:"ul"},"Perpetual / Temporary Listing: Whether (and when) your listing becomes unavailable for sale")),(0,r.kt)("h3",{id:"featured-products"},"Featured products"),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Listing Featured",src:a(2197).Z}),"\nSelect from your other listings to be featured in this product's page"),(0,r.kt)("h3",{id:"pricing-options"},"Pricing options"),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Listing Option",src:a(8132).Z})),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"Platform",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"On-Platform: Sell on NumerBay with full features"),(0,r.kt)("li",{parentName:"ul"},"Off-Platform: Only link to an external listing page"))),(0,r.kt)("li",{parentName:"ul"},"Listing Mode:",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"File Mode: Buyers can download artifact files and optionally designate a model slot for submission. You can upload artifacts to NumerBay or add external file URLs"),(0,r.kt)("li",{parentName:"ul"},"Stake Only Mode: Submit for buyers automatically without distributing artifact files, without stake limit. You must upload artifacts to NumerBay"),(0,r.kt)("li",{parentName:"ul"},"Stake Only Mode with Limit: Submit for buyers automatically without distributing artifact files, with a stake limit (in NMR). You must upload artifacts to NumerBay"))),(0,r.kt)("li",{parentName:"ul"},"Number of Rounds per Unit: Number of tournament rounds bundled into this pricing option. ")),(0,r.kt)("div",{className:"admonition admonition-info alert alert--info"},(0,r.kt)("div",{parentName:"div",className:"admonition-heading"},(0,r.kt)("h5",{parentName:"div"},(0,r.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,r.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,r.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"}))),"info")),(0,r.kt)("div",{parentName:"div",className:"admonition-content"},(0,r.kt)("p",{parentName:"div"},"Total number of rounds for an order will be ",(0,r.kt)("inlineCode",{parentName:"p"},"[order quantity] x [bundled number of rounds per unit]")))),(0,r.kt)("h3",{id:"reward-coupons"},"Reward coupons"),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Listing Coupon Specs",src:a(1881).Z})),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"Min Spend for Rewarding Coupon",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"Minimum spend in NMR required for the currently edited product to reward the buyer with a coupon"),(0,r.kt)("li",{parentName:"ul"},"This is not the min spend for the actual coupon rewarded"))),(0,r.kt)("li",{parentName:"ul"},"Applicable Products:",(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"Your ",(0,r.kt)("em",{parentName:"li"},"other")," listings that the rewarded coupon can be applied to"),(0,r.kt)("li",{parentName:"ul"},"The currently edited product is always included in the applicable products list"))),(0,r.kt)("li",{parentName:"ul"},"Coupon Discount: 0-100 integer, 100 being free"),(0,r.kt)("li",{parentName:"ul"},"Coupon Max Discount: Maximum discount cap in NMR for the rewarded coupons"),(0,r.kt)("li",{parentName:"ul"},"Coupon Min Spend: Minimum spend in NMR required for the applicable products in order for a buyer to use the rewarded coupons")),(0,r.kt)("div",{className:"admonition admonition-info alert alert--info"},(0,r.kt)("div",{parentName:"div",className:"admonition-heading"},(0,r.kt)("h5",{parentName:"div"},(0,r.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,r.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,r.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"}))),"info")),(0,r.kt)("div",{parentName:"div",className:"admonition-content"},(0,r.kt)("p",{parentName:"div"},"Coupons generated using this reward mechanism are bound to the specific buyers and cannot be transferred or used by others."))),(0,r.kt)("h2",{id:"upload-artifacts-wip"},"Upload artifacts (WIP)"),(0,r.kt)("div",{className:"admonition admonition-tip alert alert--success"},(0,r.kt)("div",{parentName:"div",className:"admonition-heading"},(0,r.kt)("h5",{parentName:"div"},(0,r.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,r.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"12",height:"16",viewBox:"0 0 12 16"},(0,r.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.5 0C3.48 0 1 2.19 1 5c0 .92.55 2.25 1 3 1.34 2.25 1.78 2.78 2 4v1h5v-1c.22-1.22.66-1.75 2-4 .45-.75 1-2.08 1-3 0-2.81-2.48-5-5.5-5zm3.64 7.48c-.25.44-.47.8-.67 1.11-.86 1.41-1.25 2.06-1.45 3.23-.02.05-.02.11-.02.17H5c0-.06 0-.13-.02-.17-.2-1.17-.59-1.83-1.45-3.23-.2-.31-.42-.67-.67-1.11C2.44 6.78 2 5.65 2 5c0-2.2 2.02-4 4.5-4 1.22 0 2.36.42 3.22 1.19C10.55 2.94 11 3.94 11 5c0 .66-.44 1.78-.86 2.48zM4 14h5c-.23 1.14-1.3 2-2.5 2s-2.27-.86-2.5-2z"}))),"Advanced tip")),(0,r.kt)("div",{parentName:"div",className:"admonition-content"},(0,r.kt)("p",{parentName:"div"},"You can automate this via NumerBay API, head over to the advanced ",(0,r.kt)("a",{parentName:"p",href:"/docs/tutorial-extras/api-automation"},"API Tutorial")," for details"))),(0,r.kt)("p",null,"After tournament round opens, you need to upload artifact files to NumerBay to fulfill your active orders."),(0,r.kt)("h2",{id:"manage-sales-wip"},"Manage sales (WIP)"))}p.isMDXComponent=!0},7249:function(e,t,a){t.Z=a.p+"assets/images/listingBasic-088434590a88dd2b24240bb7a5555f4b.png"},1881:function(e,t,a){t.Z=a.p+"assets/images/listingCouponSpecs-8b1f91efe24827cd84efda7c90fbfa2c.png"},2197:function(e,t,a){t.Z=a.p+"assets/images/listingFeatured-2c673eb89683b969e1e2deb4029b1f3b.png"},8132:function(e,t,a){t.Z=a.p+"assets/images/listingOption-16ac9ec0aabf970326716d17b210fde7.png"}}]);