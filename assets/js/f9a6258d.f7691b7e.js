"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[829],{3905:function(e,t,n){n.d(t,{Zo:function(){return d},kt:function(){return y}});var a=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},o=Object.keys(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var s=a.createContext({}),u=function(e){var t=a.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},d=function(e){var t=u(e.components);return a.createElement(s.Provider,{value:t},e.children)},p="mdxType",c={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},m=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,o=e.originalType,s=e.parentName,d=l(e,["components","mdxType","originalType","parentName"]),p=u(n),m=r,y=p["".concat(s,".").concat(m)]||p[m]||c[m]||o;return n?a.createElement(y,i(i({ref:t},d),{},{components:n})):a.createElement(y,i({ref:t},d))}));function y(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var o=n.length,i=new Array(o);i[0]=m;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[p]="string"==typeof e?e:r,i[1]=l;for(var u=2;u<o;u++)i[u]=n[u];return a.createElement.apply(null,i)}return a.createElement.apply(null,n)}m.displayName="MDXCreateElement"},335:function(e,t,n){n.r(t),n.d(t,{assets:function(){return s},contentTitle:function(){return i},default:function(){return c},frontMatter:function(){return o},metadata:function(){return l},toc:function(){return u}});var a=n(3117),r=(n(7294),n(3905));const o={slug:"daily-sales",title:"Daily Sales",authors:["restrading"],tags:["update"]},i=void 0,l={permalink:"/updates/daily-sales",editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/updates/2022-12-16-daily-sales.md",source:"@site/updates/2022-12-16-daily-sales.md",title:"Daily Sales",description:"Numerai moved towards daily tournament rounds since late Oct 2022 and will soon enable payout for the weekday rounds.",date:"2022-12-16T00:00:00.000Z",formattedDate:"December 16, 2022",tags:[{label:"update",permalink:"/updates/tags/update"}],readingTime:1.97,hasTruncateMarker:!1,authors:[{name:"ResTrading",title:"Maintainer of NumerBay",url:"https://github.com/restrading",imageURL:"https://github.com/restrading.png",key:"restrading"}],frontMatter:{slug:"daily-sales",title:"Daily Sales",authors:["restrading"],tags:["update"]},nextItem:{title:"Encryption Update",permalink:"/updates/encryption-v2"}},s={authorsImageUrls:[void 0]},u=[{value:"What&#39;s the impact",id:"whats-the-impact",level:2},{value:"Q&amp;A",id:"qa",level:2},{value:"I&#39;m an existing seller, will my automation pipeline fail during weekdays if I do not enable daily sales?",id:"im-an-existing-seller-will-my-automation-pipeline-fail-during-weekdays-if-i-do-not-enable-daily-sales",level:3},{value:"I&#39;m a buyer, how do I know if a product supports weekday rounds?",id:"im-a-buyer-how-do-i-know-if-a-product-supports-weekday-rounds",level:3},{value:"What happened to the round rollover embargo?",id:"what-happened-to-the-round-rollover-embargo",level:3}],d={toc:u},p="wrapper";function c(e){let{components:t,...o}=e;return(0,r.kt)(p,(0,a.Z)({},d,o,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("p",null,"Numerai moved towards ",(0,r.kt)("a",{parentName:"p",href:"https://forum.numer.ai/t/daily-tournaments/5766"},"daily tournament rounds")," since late Oct 2022 and will soon enable payout for the weekday rounds. "),(0,r.kt)("p",null,"NumerBay sales remained weekly up until now and the platform is finally making the transition towards daily as well."),(0,r.kt)("h2",{id:"whats-the-impact"},"What's the impact"),(0,r.kt)("p",null,"Buyers will now place orders using a calendar date picker to select the rounds to purchase.\nSelect ",(0,r.kt)("strong",{parentName:"p"},"Saturdays")," to buy the weekend rounds and ",(0,r.kt)("strong",{parentName:"p"},"Tue-Fri")," to buy the weekday rounds.\nOrder rounds are no longer required to be consecutive.\nThe same product can also be bought multiple times during the same week so long as the rounds don't overlap.\nOnly one pending order is allowed at a time."),(0,r.kt)("img",{alt:"Daily Order",src:"/img/update/dailyOrder.png",width:"450"}),(0,r.kt)("p",null,"Sellers with existing products will remain weekend-sales-only and can choose to enable weekday (daily) sales in the Edit Listing page.\nNew products created will enable weekday sales by default and can be switched off during listing creation."),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Daily Option",src:n(6069).Z,width:"1156",height:"435"})),(0,r.kt)("p",null,"There was no change to the NumerBay submission endpoints and users' existing pipelines are expected to work normally."),(0,r.kt)("h2",{id:"qa"},"Q&A"),(0,r.kt)("h3",{id:"im-an-existing-seller-will-my-automation-pipeline-fail-during-weekdays-if-i-do-not-enable-daily-sales"},"I'm an existing seller, will my automation pipeline fail during weekdays if I do not enable daily sales?"),(0,r.kt)("p",null,"No, it should work normally. No order can be placed for your product for weekday rounds if you do not enable daily sales, therefore your webhook shouldn't be triggered in the first place.\nIf you use the same automation for Numerai and NumerBay, any such attempt to upload will just result in no-op since there's no order for the weekday rounds, the effect is equivalent to trying to upload for weekend rounds when you do not have any active order. "),(0,r.kt)("h3",{id:"im-a-buyer-how-do-i-know-if-a-product-supports-weekday-rounds"},"I'm a buyer, how do I know if a product supports weekday rounds?"),(0,r.kt)("p",null,'Products with weekday sales enabled will show a blue "daily" badge in the products catalog page.\nIn addition, if you try to place an order for a product not supporting weekday rounds, you will get an error saying ',(0,r.kt)("em",{parentName:"p"},"This product is not available for weekday sale"),"."),(0,r.kt)("img",{alt:"Daily Badge",src:"/img/update/dailyBadge.png",width:"450"}),(0,r.kt)("h3",{id:"what-happened-to-the-round-rollover-embargo"},"What happened to the round rollover embargo?"),(0,r.kt)("p",null,"There used to be a 30-minute freeze at the end of the weekend submission window.\nAfter this change, there would no long be any freeze of activity near the deadline. However, it is recommended not to submit last minute as some NumerBay processes may take time to complete."))}c.isMDXComponent=!0},6069:function(e,t,n){t.Z=n.p+"assets/images/dailyOption-3e273020615a29b4a383cac488c5ffb0.png"}}]);