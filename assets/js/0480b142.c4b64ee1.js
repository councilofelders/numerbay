"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[836],{3905:function(e,t,n){n.d(t,{Zo:function(){return d},kt:function(){return h}});var o=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,o)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,o,r=function(e,t){if(null==e)return{};var n,o,r={},a=Object.keys(e);for(o=0;o<a.length;o++)n=a[o],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(o=0;o<a.length;o++)n=a[o],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var s=o.createContext({}),u=function(e){var t=o.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},d=function(e){var t=u(e.components);return o.createElement(s.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return o.createElement(o.Fragment,{},t)}},p=o.forwardRef((function(e,t){var n=e.components,r=e.mdxType,a=e.originalType,s=e.parentName,d=l(e,["components","mdxType","originalType","parentName"]),p=u(n),h=r,m=p["".concat(s,".").concat(h)]||p[h]||c[h]||a;return n?o.createElement(m,i(i({ref:t},d),{},{components:n})):o.createElement(m,i({ref:t},d))}));function h(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var a=n.length,i=new Array(a);i[0]=p;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l.mdxType="string"==typeof e?e:r,i[1]=l;for(var u=2;u<a;u++)i[u]=n[u];return o.createElement.apply(null,i)}return o.createElement.apply(null,n)}p.displayName="MDXCreateElement"},3584:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return l},contentTitle:function(){return s},metadata:function(){return u},toc:function(){return d},default:function(){return p}});var o=n(7462),r=n(3366),a=(n(7294),n(3905)),i=["components"],l={sidebar_position:2},s="FAQ",u={unversionedId:"faq",id:"faq",title:"FAQ",description:"Here are some frequently asked questions and troubleshooting guides.",source:"@site/docs/faq.md",sourceDirName:".",slug:"/faq",permalink:"/docs/faq",editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/docs/faq.md",tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"tutorialSidebar",previous:{title:"Intro",permalink:"/docs/intro"},next:{title:"Set up Account",permalink:"/docs/tutorial-basics/set-up-account"}},d=[{value:"Authentication and Account Setup",id:"authentication-and-account-setup",children:[{value:"I can&#39;t login",id:"i-cant-login",children:[],level:3},{value:"I&#39;m getting &quot;Numerai API Error: Insufficient Permission&quot;",id:"im-getting-numerai-api-error-insufficient-permission",children:[],level:3}],level:2},{value:"Buying",id:"buying",children:[{value:"I bought a good model, and then it went to hell",id:"i-bought-a-good-model-and-then-it-went-to-hell",children:[],level:3},{value:"Seller didn&#39;t upload files for my order",id:"seller-didnt-upload-files-for-my-order",children:[],level:3},{value:"I changed model name, but my order&#39;s submission slot is still the old name",id:"i-changed-model-name-but-my-orders-submission-slot-is-still-the-old-name",children:[],level:3}],level:2},{value:"Selling",id:"selling",children:[{value:"I&#39;m getting &quot;Upload cancelled, no active order to upload for&quot;",id:"im-getting-upload-cancelled-no-active-order-to-upload-for",children:[],level:3},{value:"Do I have to upload again on each new order?",id:"do-i-have-to-upload-again-on-each-new-order",children:[],level:3},{value:"I missed upload for a buyer",id:"i-missed-upload-for-a-buyer",children:[],level:3}],level:2}],c={toc:d};function p(e){var t=e.components,n=(0,r.Z)(e,i);return(0,a.kt)("wrapper",(0,o.Z)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h1",{id:"faq"},"FAQ"),(0,a.kt)("p",null,"Here are some frequently asked questions and troubleshooting guides."),(0,a.kt)("h2",{id:"authentication-and-account-setup"},"Authentication and Account Setup"),(0,a.kt)("h3",{id:"i-cant-login"},"I can't login"),(0,a.kt)("p",null,"If you had entered correct credentials, but the browser did not respond (e.g. no MetaMask pop up). This may be an issue with browser cache which tends to happen when the browser just recovered from a previous session. Please try to refresh the page and login again."),(0,a.kt)("p",null,"If you registered an account with username before and did not connect a MetaMask wallet, you would need to use the ",(0,a.kt)("a",{parentName:"p",href:"https://numerbay.ai/login"},"legacy username login"),"."),(0,a.kt)("p",null,"If you had a connected MetaMask wallet, make sure you are using the correct wallet for login."),(0,a.kt)("p",null,"If you forgot your account username or wallet, please post in ",(0,a.kt)("a",{parentName:"p",href:"https://rocketchat.numer.ai/channel/numerbay"},"#numerbay")," for assistance."),(0,a.kt)("h3",{id:"im-getting-numerai-api-error-insufficient-permission"},'I\'m getting "Numerai API Error: Insufficient Permission"'),(0,a.kt)("p",null,"This may indicate your Numerai API key has expired or does not have required permissions, please check ",(0,a.kt)("a",{parentName:"p",href:"/docs/tutorial-basics/set-up-account#set-up-numerai-api-key"},"here")," for the table of required permissions for different tasks, and go to the ",(0,a.kt)("a",{parentName:"p",href:"https://numerbay.ai/numerai-settings"},"Numerai Settings page")," to change your Numerai API key."),(0,a.kt)("h2",{id:"buying"},"Buying"),(0,a.kt)("h3",{id:"i-bought-a-good-model-and-then-it-went-to-hell"},"I bought a good model, and then it went to hell"),(0,a.kt)("p",null,"Sorry to hear that. Unfortunately the market can be quite unpredictable, past performance is no indication of future returns. NumerBay is not an investment platform and financial gains are not guaranteed. You should be aware of the financial risks when making decisions. Good luck!"),(0,a.kt)("h3",{id:"seller-didnt-upload-files-for-my-order"},"Seller didn't upload files for my order"),(0,a.kt)("p",null,"If the round has not ended yet, then be patient. Some sellers might upload closer to the deadline. If you are unsure, feel free to reach out to the seller privately or post in ",(0,a.kt)("a",{parentName:"p",href:"https://rocketchat.numer.ai/channel/numerbay"},"#numerbay")," for assistance."),(0,a.kt)("p",null,"NumerBay doesn't yet provide automated dispute resolution. If you did not receive anything after the round deadline, you can try to contact the seller in private or post in ",(0,a.kt)("a",{parentName:"p",href:"https://rocketchat.numer.ai/channel/numerbay"},"#numerbay")," for assistance. Depending on the specific situation, you might be able to get a refund or order extension."),(0,a.kt)("h3",{id:"i-changed-model-name-but-my-orders-submission-slot-is-still-the-old-name"},"I changed model name, but my order's submission slot is still the old name"),(0,a.kt)("p",null,"Don't worry, the submission will go to the correct slot. To show the new model name in the future, go to the ",(0,a.kt)("a",{parentName:"p",href:"https://numerbay.ai/numerai-settings"},"Numerai Settings page")," and click the ",(0,a.kt)("inlineCode",{parentName:"p"},"sync")," button on the top right to sync your model slots with Numerai. "),(0,a.kt)("h2",{id:"selling"},"Selling"),(0,a.kt)("h3",{id:"im-getting-upload-cancelled-no-active-order-to-upload-for"},'I\'m getting "Upload cancelled, no active order to upload for"'),(0,a.kt)("p",null,"This happens when your product uses buyer-side encryption (which is by default), and you don't have any active sale order for the product. Upload is only possible when a sale order is available. "),(0,a.kt)("p",null,"If you want to automate things, you can solve this in two ways in the ",(0,a.kt)("a",{parentName:"p",href:"https://numerbay.ai/listings"},"listing settings"),". Edit your listing, check the ",(0,a.kt)("inlineCode",{parentName:"p"},"Show advanced settings")," box and then:"),(0,a.kt)("ol",null,(0,a.kt)("li",{parentName:"ol"},"Set a webhook URL for NumerBay to trigger on each confirmed sale to automate each submission, OR"),(0,a.kt)("li",{parentName:"ol"},"Disable client-side encryption to upload only once regardless of any sale order (Make sure you only turn off encryption when you don't have any active sale, including past sales that are still active. Otherwise, the buyers won't be able to receive files)")),(0,a.kt)("h3",{id:"do-i-have-to-upload-again-on-each-new-order"},"Do I have to upload again on each new order?"),(0,a.kt)("p",null,"Yes if your product uses buyer-side encryption (which is by default), you can check whether this is enabled ",(0,a.kt)("a",{parentName:"p",href:"https://numerbay.ai/listings"},"listing settings"),". Edit your listing, check the ",(0,a.kt)("inlineCode",{parentName:"p"},"Show advanced settings")," box to see the option."),(0,a.kt)("p",null,"If you don't want to do this, check the answer for the previous question for solutions."),(0,a.kt)("h3",{id:"i-missed-upload-for-a-buyer"},"I missed upload for a buyer"),(0,a.kt)("p",null,"NumerBay doesn't yet provide automated dispute resolution, please post in ",(0,a.kt)("a",{parentName:"p",href:"https://rocketchat.numer.ai/channel/numerbay"},"#numerbay")," for assistance. You can offer a refund, or an order extension."))}p.isMDXComponent=!0}}]);