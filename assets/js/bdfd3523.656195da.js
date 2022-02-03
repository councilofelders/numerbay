"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[165],{3905:function(e,t,a){a.d(t,{Zo:function(){return c},kt:function(){return d}});var n=a(7294);function r(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function i(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function o(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?i(Object(a),!0).forEach((function(t){r(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):i(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function u(e,t){if(null==e)return{};var a,n,r=function(e,t){if(null==e)return{};var a,n,r={},i=Object.keys(e);for(n=0;n<i.length;n++)a=i[n],t.indexOf(a)>=0||(r[a]=e[a]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)a=i[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(r[a]=e[a])}return r}var l=n.createContext({}),p=function(e){var t=n.useContext(l),a=t;return e&&(a="function"==typeof e?e(t):o(o({},t),e)),a},c=function(e){var t=p(e.components);return n.createElement(l.Provider,{value:t},e.children)},s={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},m=n.forwardRef((function(e,t){var a=e.components,r=e.mdxType,i=e.originalType,l=e.parentName,c=u(e,["components","mdxType","originalType","parentName"]),m=p(a),d=r,g=m["".concat(l,".").concat(d)]||m[d]||s[d]||i;return a?n.createElement(g,o(o({ref:t},c),{},{components:a})):n.createElement(g,o({ref:t},c))}));function d(e,t){var a=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=a.length,o=new Array(i);o[0]=m;var u={};for(var l in t)hasOwnProperty.call(t,l)&&(u[l]=t[l]);u.originalType=e,u.mdxType="string"==typeof e?e:r,o[1]=u;for(var p=2;p<i;p++)o[p]=a[p];return n.createElement.apply(null,o)}return n.createElement.apply(null,a)}m.displayName="MDXCreateElement"},4281:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return u},contentTitle:function(){return l},metadata:function(){return p},toc:function(){return c},default:function(){return m}});var n=a(7462),r=a(3366),i=(a(7294),a(3905)),o=["components"],u={sidebar_position:1},l="Set up Account",p={unversionedId:"tutorial-basics/set-up-account",id:"tutorial-basics/set-up-account",title:"Set up Account",description:"In order to buy or sell on NumerBay, a NumerBay account with Numerai API key needs to be set up.",source:"@site/docs/tutorial-basics/set-up-account.md",sourceDirName:"tutorial-basics",slug:"/tutorial-basics/set-up-account",permalink:"/docs/tutorial-basics/set-up-account",editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/docs/tutorial-basics/set-up-account.md",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",previous:{title:"Intro",permalink:"/docs/intro"},next:{title:"Buy a Product",permalink:"/docs/tutorial-basics/buy-a-product"}},c=[{value:"Sign up",id:"sign-up",children:[{value:"Login via MetaMask (Recommended)",id:"login-via-metamask-recommended",children:[],level:3},{value:"Username sign up",id:"username-sign-up",children:[],level:3}],level:2},{value:"Generate Key Pair",id:"generate-key-pair",children:[],level:2},{value:"Set up Numerai API Key",id:"set-up-numerai-api-key",children:[],level:2},{value:"Update profile",id:"update-profile",children:[],level:2}],s={toc:c};function m(e){var t=e.components,u=(0,r.Z)(e,o);return(0,i.kt)("wrapper",(0,n.Z)({},s,u,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("h1",{id:"set-up-account"},"Set up Account"),(0,i.kt)("p",null,"In order to buy or sell on NumerBay, a NumerBay account with Numerai API key needs to be set up."),(0,i.kt)("h2",{id:"sign-up"},"Sign up"),(0,i.kt)("p",null,"Head to ",(0,i.kt)("strong",{parentName:"p"},(0,i.kt)("a",{parentName:"strong",href:"https://numerbay.ai"},"numerbay.ai")),", click the account icon on the top right of the page, and sign up/login via either MetaMask or username:"),(0,i.kt)("h3",{id:"login-via-metamask-recommended"},"Login via MetaMask (Recommended)"),(0,i.kt)("img",{alt:"Sign up MetaMask",src:"/img/tutorial/signUpMetaMask.png",width:"400"}),(0,i.kt)("img",{alt:"Sign up MetaMask Sign",src:"/img/tutorial/signUpMetaMaskSign.png",width:"300"}),(0,i.kt)("h3",{id:"username-sign-up"},"Username sign up"),(0,i.kt)("p",null,"If you don't want to use MetaMask, sign up manually by clicking the ",(0,i.kt)("strong",{parentName:"p"},"Username Login")," tab, and click ",(0,i.kt)("strong",{parentName:"p"},"Register today")," to switch to the sign up form."),(0,i.kt)("img",{alt:"Sign up Username",src:"/img/tutorial/signUpUsername.png",width:"400"}),(0,i.kt)("h2",{id:"generate-key-pair"},"Generate Key Pair"),(0,i.kt)("p",null,"In the ",(0,i.kt)("strong",{parentName:"p"},(0,i.kt)("a",{parentName:"strong",href:"https://numerbay.ai/my-account/my-profile"},"profile update form")),", click the ",(0,i.kt)("strong",{parentName:"p"},"Generate Key Pair")," button to generate a public-private key pair that will be used to encrypt your purchased artifact files.\nAfter doing so, click ",(0,i.kt)("strong",{parentName:"p"},"Export key file")," to safe-keep the generated key. The exported key file can be used in the ",(0,i.kt)("a",{parentName:"p",href:"/docs/tutorial-extras/api-automation"},"Python client")," to download encrypted files."),(0,i.kt)("p",null,(0,i.kt)("img",{alt:"Profile",src:a(8621).Z})),(0,i.kt)("h2",{id:"set-up-numerai-api-key"},"Set up Numerai API Key"),(0,i.kt)("p",null,"After signing up and logging in, head to the NumerBay account page for the ",(0,i.kt)("strong",{parentName:"p"},(0,i.kt)("a",{parentName:"strong",href:"https://numerbay.ai/my-account/numerai-api"},"Numerai API form"))," under the Account sidebar section."),(0,i.kt)("p",null,"If you don't have a Numerai API key yet, you can create one in the ",(0,i.kt)("a",{parentName:"p",href:"https://numer.ai/account"},"Numerai Account Settings")," page. Make sure it has at least ",(0,i.kt)("strong",{parentName:"p"},"View user info")," permission. NumerBay only uses user info for model ownership verification and email notifications."),(0,i.kt)("p",null,"Additional API permissions may be needed depending on what you want to do on NumerBay, you can always change API keys later:"),(0,i.kt)("table",null,(0,i.kt)("thead",{parentName:"table"},(0,i.kt)("tr",{parentName:"thead"},(0,i.kt)("th",{parentName:"tr",align:null},"Task\\Permission"),(0,i.kt)("th",{parentName:"tr",align:"center"},"View user info"),(0,i.kt)("th",{parentName:"tr",align:"center"},"View submission info"),(0,i.kt)("th",{parentName:"tr",align:"center"},"Upload submissions"),(0,i.kt)("th",{parentName:"tr",align:"center"},"Stake*"))),(0,i.kt)("tbody",{parentName:"table"},(0,i.kt)("tr",{parentName:"tbody"},(0,i.kt)("td",{parentName:"tr",align:null},"Buy (File Mode)"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"}),(0,i.kt)("td",{parentName:"tr",align:"center"}),(0,i.kt)("td",{parentName:"tr",align:"center"})),(0,i.kt)("tr",{parentName:"tbody"},(0,i.kt)("td",{parentName:"tr",align:null},"Buy (with Auto-submit)"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"})),(0,i.kt)("tr",{parentName:"tbody"},(0,i.kt)("td",{parentName:"tr",align:null},"Buy (Stake Only Mode)"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"})),(0,i.kt)("tr",{parentName:"tbody"},(0,i.kt)("td",{parentName:"tr",align:null},"Buy (with Stake Limit)"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f")),(0,i.kt)("tr",{parentName:"tbody"},(0,i.kt)("td",{parentName:"tr",align:null},"Sell"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"}),(0,i.kt)("td",{parentName:"tr",align:"center"}),(0,i.kt)("td",{parentName:"tr",align:"center"})),(0,i.kt)("tr",{parentName:"tbody"},(0,i.kt)("td",{parentName:"tr",align:null},"Vote"),(0,i.kt)("td",{parentName:"tr",align:"center"},"\u2714\ufe0f"),(0,i.kt)("td",{parentName:"tr",align:"center"}),(0,i.kt)("td",{parentName:"tr",align:"center"}),(0,i.kt)("td",{parentName:"tr",align:"center"})))),(0,i.kt)("p",null,"[*]",": ",(0,i.kt)("strong",{parentName:"p"},"Stake")," permission is only used to down-adjust stake below the product's stake limit if exceeded"),(0,i.kt)("p",null,"After creating an API key with the permissions required, plug them into the form as shown below, wait for a few seconds for validation, and the updated API Key permission info will be reflected:\n",(0,i.kt)("img",{alt:"Numerai API Key",src:a(7570).Z})),(0,i.kt)("div",{className:"admonition admonition-info alert alert--info"},(0,i.kt)("div",{parentName:"div",className:"admonition-heading"},(0,i.kt)("h5",{parentName:"div"},(0,i.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,i.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,i.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"}))),"info")),(0,i.kt)("div",{parentName:"div",className:"admonition-content"},(0,i.kt)("p",{parentName:"div"},"If you encounter errors while updating with a valid Numerai API key, it may be likely that you are not logged in with the correct NumerBay account, you might have another old account bound to the same Numerai account.\nPlease check if you are logged in with the correct MetaMask wallet or if you have an old account or account created with username."))),(0,i.kt)("h2",{id:"update-profile"},"Update profile"),(0,i.kt)("p",null,"You can change your username, password and email in the ",(0,i.kt)("a",{parentName:"p",href:"https://numerbay.ai/my-account/my-profile"},"profile update form"),". By default, your Numerai email address is used to receive email notifications."),(0,i.kt)("div",{className:"admonition admonition-caution alert alert--warning"},(0,i.kt)("div",{parentName:"div",className:"admonition-heading"},(0,i.kt)("h5",{parentName:"div"},(0,i.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,i.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",viewBox:"0 0 16 16"},(0,i.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M8.893 1.5c-.183-.31-.52-.5-.887-.5s-.703.19-.886.5L.138 13.499a.98.98 0 0 0 0 1.001c.193.31.53.501.886.501h13.964c.367 0 .704-.19.877-.5a1.03 1.03 0 0 0 .01-1.002L8.893 1.5zm.133 11.497H6.987v-2.003h2.039v2.003zm0-3.004H6.987V5.987h2.039v4.006z"}))),"caution")),(0,i.kt)("div",{parentName:"div",className:"admonition-content"},(0,i.kt)("p",{parentName:"div"},"If you disconnect MetaMask wallet in the profile page, and your account was created with MetaMask login (without a password). You need to set a password before logging out, or you might lose access to the account."),(0,i.kt)("p",{parentName:"div"},"NumerBay does not yet allow password recovery, please contact support by posting in the ",(0,i.kt)("a",{parentName:"p",href:"https://community.numer.ai/channel/numerbay"},"#numerbay")," channel on RocketChat."))))}m.isMDXComponent=!0},7570:function(e,t,a){t.Z=a.p+"assets/images/numeraiApiKey-a14d57d874085f8f8c8faf1d127e84df.png"},8621:function(e,t,a){t.Z=a.p+"assets/images/profile-b175f1ae0efa510900f23aef731c0275.png"}}]);