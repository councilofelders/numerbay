"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[165],{3905:function(e,t,n){n.d(t,{Zo:function(){return c},kt:function(){return k}});var a=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function u(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},i=Object.keys(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var p=a.createContext({}),l=function(e){var t=a.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):o(o({},t),e)),n},c=function(e){var t=l(e.components);return a.createElement(p.Provider,{value:t},e.children)},s="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},d=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,i=e.originalType,p=e.parentName,c=u(e,["components","mdxType","originalType","parentName"]),s=l(n),d=r,k=s["".concat(p,".").concat(d)]||s[d]||m[d]||i;return n?a.createElement(k,o(o({ref:t},c),{},{components:n})):a.createElement(k,o({ref:t},c))}));function k(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=n.length,o=new Array(i);o[0]=d;var u={};for(var p in t)hasOwnProperty.call(t,p)&&(u[p]=t[p]);u.originalType=e,u[s]="string"==typeof e?e:r,o[1]=u;for(var l=2;l<i;l++)o[l]=n[l];return a.createElement.apply(null,o)}return a.createElement.apply(null,n)}d.displayName="MDXCreateElement"},4281:function(e,t,n){n.r(t),n.d(t,{assets:function(){return p},contentTitle:function(){return o},default:function(){return m},frontMatter:function(){return i},metadata:function(){return u},toc:function(){return l}});var a=n(3117),r=(n(7294),n(3905));const i={sidebar_position:1},o="Set up Account",u={unversionedId:"tutorial-basics/set-up-account",id:"tutorial-basics/set-up-account",title:"Set up Account",description:"In order to buy or sell on NumerBay, a NumerBay account with Numerai API key needs to be set up.",source:"@site/docs/tutorial-basics/set-up-account.md",sourceDirName:"tutorial-basics",slug:"/tutorial-basics/set-up-account",permalink:"/docs/tutorial-basics/set-up-account",draft:!1,editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/docs/tutorial-basics/set-up-account.md",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",previous:{title:"FAQ",permalink:"/docs/faq"},next:{title:"Buy a Product",permalink:"/docs/tutorial-basics/buy-a-product"}},p={},l=[{value:"Sign up",id:"sign-up",level:2},{value:"Generate Key Pair",id:"generate-key-pair",level:2},{value:"Set up Numerai API Key",id:"set-up-numerai-api-key",level:2},{value:"Update profile",id:"update-profile",level:2}],c={toc:l},s="wrapper";function m(e){let{components:t,...i}=e;return(0,r.kt)(s,(0,a.Z)({},c,i,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"set-up-account"},"Set up Account"),(0,r.kt)("p",null,"In order to buy or sell on NumerBay, a NumerBay account with Numerai API key needs to be set up."),(0,r.kt)("h2",{id:"sign-up"},"Sign up"),(0,r.kt)("p",null,"Head to ",(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("a",{parentName:"strong",href:"https://numerbay.ai"},"numerbay.ai")),", click the ",(0,r.kt)("strong",{parentName:"p"},"Connect Wallet")," button on the top right of the page, and login by connecting your MetaMask wallet."),(0,r.kt)("admonition",{type:"caution"},(0,r.kt)("p",{parentName:"admonition"},"Sign-up by username has been deprecated. Users who had not connected a MetaMask wallet to their accounts can login via the legacy username login tab.")),(0,r.kt)("img",{alt:"Sign up MetaMask",src:"/img/tutorial/signUpMetaMask.png",width:"450"}),(0,r.kt)("img",{alt:"Sign up MetaMask Sign",src:"/img/tutorial/signUpMetaMaskSign.png",width:"250"}),(0,r.kt)("h2",{id:"generate-key-pair"},"Generate Key Pair"),(0,r.kt)("p",null,"In the ",(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("a",{parentName:"strong",href:"https://numerbay.ai/account"},"Edit profile page")),", click the ",(0,r.kt)("strong",{parentName:"p"},"Generate Key Pair")," button to generate a public-private key pair that will be used to encrypt your purchased artifact files.\nAfter doing so, click ",(0,r.kt)("strong",{parentName:"p"},"Export key file")," to safe-keep the generated key. The exported key file can be used in the ",(0,r.kt)("a",{parentName:"p",href:"/docs/tutorial-extras/api-automation"},"Python client")," to download encrypted files."),(0,r.kt)("p",null,(0,r.kt)("img",{alt:"Profile",src:n(9031).Z,width:"1756",height:"1030"})),(0,r.kt)("h2",{id:"set-up-numerai-api-key"},"Set up Numerai API Key"),(0,r.kt)("p",null,"After logging in, head to the NumerBay account settings for the ",(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("a",{parentName:"strong",href:"https://numerbay.ai/numerai-settings"},"Numerai Settings page"))," in the sidebar."),(0,r.kt)("p",null,"If you don't have a Numerai API key yet, you can create one in the ",(0,r.kt)("a",{parentName:"p",href:"https://numer.ai/account"},"Numerai Account Settings")," page. Make sure it has at least ",(0,r.kt)("strong",{parentName:"p"},"View user info")," permission. NumerBay only uses user info for model ownership verification and email notifications."),(0,r.kt)("p",null,"Additional API permissions may be needed depending on what you want to do on NumerBay, you can always change API keys later:"),(0,r.kt)("table",null,(0,r.kt)("thead",{parentName:"table"},(0,r.kt)("tr",{parentName:"thead"},(0,r.kt)("th",{parentName:"tr",align:null},"Task\\Permission"),(0,r.kt)("th",{parentName:"tr",align:"center"},"View user info"),(0,r.kt)("th",{parentName:"tr",align:"center"},"View submission info"),(0,r.kt)("th",{parentName:"tr",align:"center"},"Upload submissions"),(0,r.kt)("th",{parentName:"tr",align:"center"},"Stake*"))),(0,r.kt)("tbody",{parentName:"table"},(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"Buy (File Mode)"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"}),(0,r.kt)("td",{parentName:"tr",align:"center"}),(0,r.kt)("td",{parentName:"tr",align:"center"})),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"Buy (with Auto-submit)"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"})),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"Buy (Stake Only Mode)"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"})),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"Buy (with Stake Limit)"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f")),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"Sell"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"}),(0,r.kt)("td",{parentName:"tr",align:"center"}),(0,r.kt)("td",{parentName:"tr",align:"center"})),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"Vote"),(0,r.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,r.kt)("td",{parentName:"tr",align:"center"}),(0,r.kt)("td",{parentName:"tr",align:"center"}),(0,r.kt)("td",{parentName:"tr",align:"center"})))),(0,r.kt)("p",null,"[*]",": ",(0,r.kt)("strong",{parentName:"p"},"Stake")," permission is only used to down-adjust stake below the product's stake limit if exceeded"),(0,r.kt)("p",null,"After creating an API key with the permissions required, plug them into the form as shown below, wait for a few seconds for validation, and the updated API Key permission info will be reflected:\n",(0,r.kt)("img",{alt:"Numerai API Key",src:n(9358).Z,width:"1276",height:"775"})),(0,r.kt)("admonition",{type:"info"},(0,r.kt)("p",{parentName:"admonition"},"If you encounter errors while updating with a valid Numerai API key, it may be likely that you are not logged in with the correct NumerBay account, you might have another old account bound to the same Numerai account.\nPlease check if you are logged in with the correct MetaMask wallet or if you have an old account or account created with username.")),(0,r.kt)("h2",{id:"update-profile"},"Update profile"),(0,r.kt)("p",null,"You can change your username, password and email in the ",(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("a",{parentName:"strong",href:"https://numerbay.ai/account"},"Edit profile page")),". By default, your Numerai email address is used to receive email notifications."),(0,r.kt)("admonition",{type:"caution"},(0,r.kt)("p",{parentName:"admonition"},"NumerBay does not yet allow password recovery, please contact support by posting in the ",(0,r.kt)("a",{parentName:"p",href:"https://community.numer.ai/channel/numerbay"},"#numerbay")," channel on RocketChat.")))}m.isMDXComponent=!0},9358:function(e,t,n){t.Z=n.p+"assets/images/numeraiApiKey-d3f476683d58198f932e45f01a54893a.png"},9031:function(e,t,n){t.Z=n.p+"assets/images/profile-641bb11af2a3017cddc7f920db507703.png"}}]);