"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[375],{3905:function(e,t,n){n.d(t,{Zo:function(){return u},kt:function(){return c}});var a=n(7294);function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){i(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function o(e,t){if(null==e)return{};var n,a,i=function(e,t){if(null==e)return{};var n,a,i={},r=Object.keys(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}var p=a.createContext({}),m=function(e){var t=a.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},u=function(e){var t=m(e.components);return a.createElement(p.Provider,{value:t},e.children)},d={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},s=a.forwardRef((function(e,t){var n=e.components,i=e.mdxType,r=e.originalType,p=e.parentName,u=o(e,["components","mdxType","originalType","parentName"]),s=m(n),c=i,k=s["".concat(p,".").concat(c)]||s[c]||d[c]||r;return n?a.createElement(k,l(l({ref:t},u),{},{components:n})):a.createElement(k,l({ref:t},u))}));function c(e,t){var n=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var r=n.length,l=new Array(r);l[0]=s;var o={};for(var p in t)hasOwnProperty.call(t,p)&&(o[p]=t[p]);o.originalType=e,o.mdxType="string"==typeof e?e:i,l[1]=o;for(var m=2;m<r;m++)l[m]=n[m];return a.createElement.apply(null,l)}return a.createElement.apply(null,n)}s.displayName="MDXCreateElement"},4811:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return o},contentTitle:function(){return p},metadata:function(){return m},toc:function(){return u},default:function(){return s}});var a=n(7462),i=n(3366),r=(n(7294),n(3905)),l=["components"],o={sidebar_label:"numerbay",title:"numerbay"},p=void 0,m={unversionedId:"reference/numerbay",id:"reference/numerbay",title:"numerbay",description:"Parts of the API that is shared between Signals and Classic",source:"@site/docs/reference/numerbay.md",sourceDirName:"reference",slug:"/reference/numerbay",permalink:"/docs/reference/numerbay",editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/docs/reference/numerbay.md",tags:[],version:"current",frontMatter:{sidebar_label:"numerbay",title:"numerbay"},sidebar:"API Documentation",previous:{title:"cli",permalink:"/docs/reference/cli"},next:{title:"utils",permalink:"/docs/reference/utils"}},u=[{value:"NumerBay Objects",id:"numerbay-objects",children:[{value:"__init__",id:"__init__",children:[],level:3},{value:"get_account",id:"get_account",children:[],level:3},{value:"get_my_orders",id:"get_my_orders",children:[],level:3},{value:"get_my_listings",id:"get_my_listings",children:[],level:3},{value:"upload_artifact",id:"upload_artifact",children:[],level:3},{value:"download_artifact",id:"download_artifact",children:[],level:3}],level:2}],d={toc:u};function s(e){var t=e.components,n=(0,i.Z)(e,l);return(0,r.kt)("wrapper",(0,a.Z)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("p",null,"Parts of the API that is shared between Signals and Classic"),(0,r.kt)("h2",{id:"numerbay-objects"},"NumerBay Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class NumerBay()\n")),(0,r.kt)("p",null,"Wrapper around the NumerBay API"),(0,r.kt)("h3",{id:"__init__"},"_","_","init","_","_"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'def __init__(username=None, password=None, verbosity="INFO", show_progress_bars=True)\n')),(0,r.kt)("p",null,"initialize NumerBay API wrapper for Python"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"username")," ",(0,r.kt)("em",{parentName:"li"},"str")," - your NumerBay username"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"password")," ",(0,r.kt)("em",{parentName:"li"},"str")," - your NumerBay password"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"verbosity")," ",(0,r.kt)("em",{parentName:"li"},"str"),' - indicates what level of messages should be\ndisplayed. valid values are "debug", "info", "warning",\n"error" and "critical"'),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"show_progress_bars")," ",(0,r.kt)("em",{parentName:"li"},"bool")," - flag to turn of progress bars")),(0,r.kt)("h3",{id:"get_account"},"get","_","account"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def get_account() -> Dict\n")),(0,r.kt)("p",null,"Get all information about your account!"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("p",{parentName:"li"},(0,r.kt)("inlineCode",{parentName:"p"},"dict")," - user information including the following fields:"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"email (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"id (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"is_active (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"is_superuser (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"public_address (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"username (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"numerai_api_key_public_id (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"numerai_api_key_can_read_user_info (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"numerai_api_key_can_read_submission_info (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"numerai_api_key_can_upload_submission (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"numerai_api_key_can_stake (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"numerai_wallet_address (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"models (",(0,r.kt)("inlineCode",{parentName:"li"},"list"),") each with the following fields:"),(0,r.kt)("li",{parentName:"ul"},"id (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"name (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"tournament (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"start_date (",(0,r.kt)("inlineCode",{parentName:"li"},"datetime"),")"),(0,r.kt)("li",{parentName:"ul"},"coupons (",(0,r.kt)("inlineCode",{parentName:"li"},"list"),")")))),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Example"),":"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'api = NumerBay(username="..", password="..")\napi.get_account()\n')),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},'{\n"email":"me@example.com",\n"is_active":True,\n"is_superuser":False,\n"username":"myusername",\n"public_address":"0xmymetamaskaddressdde80ca30248e7a8890cacb",\n"id":2,\n"numerai_api_key_public_id":"MYNUMERAIAPIKEYRCXBVB66ACTSLDR53",\n"numerai_api_key_can_upload_submission":True,\n"numerai_api_key_can_stake":True,\n"numerai_api_key_can_read_submission_info":True,\n"numerai_api_key_can_read_user_info":True,\n"numerai_wallet_address":"0x000000000000000000000000mynumeraiaddress",\n"models":[{\n"id":"xxxxxxxx-xxxx-xxxx-xxxx-411487a4d64a",\n"name":"mymodel",\n"tournament":8,\n"start_date":"2021-03-22T17:44:50"\n}, ..],\n"coupons":[..]\n}\n')),(0,r.kt)("h3",{id:"get_my_orders"},"get","_","my","_","orders"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def get_my_orders() -> List\n")),(0,r.kt)("p",null,"Get all your orders."),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("p",{parentName:"li"},(0,r.kt)("inlineCode",{parentName:"p"},"list")," - List of dicts with the following structure:"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"date_order (",(0,r.kt)("inlineCode",{parentName:"li"},"datetime"),")"),(0,r.kt)("li",{parentName:"ul"},"round_order (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"quantity (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"price (",(0,r.kt)("inlineCode",{parentName:"li"},"decimal.Decimal"),")"),(0,r.kt)("li",{parentName:"ul"},"currency (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"mode (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"stake_limit (",(0,r.kt)("inlineCode",{parentName:"li"},"decimal.Decimal"),")"),(0,r.kt)("li",{parentName:"ul"},"submit_model_id (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"submit_model_name (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"submit_state (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"chain (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"from_address (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"to_address (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"transaction_hash (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"state (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"applied_coupon_id (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"coupon (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"coupon_specs (",(0,r.kt)("inlineCode",{parentName:"li"},"dict"),")"),(0,r.kt)("li",{parentName:"ul"},"id (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"product (",(0,r.kt)("inlineCode",{parentName:"li"},"dict"),")"),(0,r.kt)("li",{parentName:"ul"},"buyer (",(0,r.kt)("inlineCode",{parentName:"li"},"dict"),")")))),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Example"),":"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'api = NumerBay(username="..", password="..")\napi.get_my_orders()\n')),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},'[{\n"date_order":"2021-12-25T06:34:58.047278",\n"round_order":296,\n"quantity":1,\n"price":9,\n"currency":"NMR",\n"mode":"file",\n"stake_limit":None,\n"submit_model_id":None,\n"submit_model_name":None,\n"submit_state":None,\n"chain":"ethereum",\n"from_address":"0x00000000000000000000000000000fromaddress",\n"to_address":"0x0000000000000000000000000000000toaddress",\n"transaction_hash":"0x09bd2a0f814a745...7a20e5abcdef",\n"state":"confirmed",\n"applied_coupon_id":1,\n"coupon":None,\n"coupon_specs":None,\n"id":126,\n"product":{..},\n"buyer":{\n"id":2,\n"username":"myusername"\n}\n}, ...]\n')),(0,r.kt)("h3",{id:"get_my_listings"},"get","_","my","_","listings"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def get_my_listings()\n")),(0,r.kt)("p",null,"Get all your listings."),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("p",{parentName:"li"},(0,r.kt)("inlineCode",{parentName:"p"},"list")," - List of dicts with the following structure:"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"avatar (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"description (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"is_active (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"is_ready (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"expiration_round (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"total_num_sales (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"last_sale_price (",(0,r.kt)("inlineCode",{parentName:"li"},"decimal.Decimal"),")"),(0,r.kt)("li",{parentName:"ul"},"last_sale_price_delta (",(0,r.kt)("inlineCode",{parentName:"li"},"decimal.Decimal"),")"),(0,r.kt)("li",{parentName:"ul"},"featured_products (",(0,r.kt)("inlineCode",{parentName:"li"},"list"),")"),(0,r.kt)("li",{parentName:"ul"},"id (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"name (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"sku (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"category (",(0,r.kt)("inlineCode",{parentName:"li"},"dict"),") with the following fields:"),(0,r.kt)("li",{parentName:"ul"},"name (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"slug (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"tournament (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"is_per_round (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"is_submission (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"id (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"items (",(0,r.kt)("inlineCode",{parentName:"li"},"list"),")"),(0,r.kt)("li",{parentName:"ul"},"parent (",(0,r.kt)("inlineCode",{parentName:"li"},"dict"),")"),(0,r.kt)("li",{parentName:"ul"},"owner (",(0,r.kt)("inlineCode",{parentName:"li"},"dict"),")"),(0,r.kt)("li",{parentName:"ul"},"model (",(0,r.kt)("inlineCode",{parentName:"li"},"dict"),")"),(0,r.kt)("li",{parentName:"ul"},"reviews (",(0,r.kt)("inlineCode",{parentName:"li"},"list"),")"),(0,r.kt)("li",{parentName:"ul"},"options (",(0,r.kt)("inlineCode",{parentName:"li"},"list"),") each with the following fields:"),(0,r.kt)("li",{parentName:"ul"},"id (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"is_on_platform (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"third_party_url (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"description (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"quantity (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")"),(0,r.kt)("li",{parentName:"ul"},"price (",(0,r.kt)("inlineCode",{parentName:"li"},"decimal.Decimal"),")"),(0,r.kt)("li",{parentName:"ul"},"currency (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"wallet (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"chain (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"stake_limit (",(0,r.kt)("inlineCode",{parentName:"li"},"decimal.Decimal"),")"),(0,r.kt)("li",{parentName:"ul"},"mode (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"is_active (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"coupon (",(0,r.kt)("inlineCode",{parentName:"li"},"bool"),")"),(0,r.kt)("li",{parentName:"ul"},"coupon_specs (",(0,r.kt)("inlineCode",{parentName:"li"},"dict"),")"),(0,r.kt)("li",{parentName:"ul"},"special_price (",(0,r.kt)("inlineCode",{parentName:"li"},"decimal.Decimal"),")"),(0,r.kt)("li",{parentName:"ul"},"applied_coupon (",(0,r.kt)("inlineCode",{parentName:"li"},"str"),")"),(0,r.kt)("li",{parentName:"ul"},"product_id (",(0,r.kt)("inlineCode",{parentName:"li"},"int"),")")))),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Example"),":"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'api = NumerBay(username="..", password="..")\napi.get_my_listings()\n')),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},'[{\n"avatar":"https://example.com/example.jpg",\n"description":"Product description",\n"is_active":True,\n"is_ready":False,\n"expiration_round":None,\n"total_num_sales":0,\n"last_sale_price":None,\n"last_sale_price_delta":None,\n"featured_products":None,\n"id":108,\n"name":"mymodel",\n"sku":"numerai-predictions-mymodel",\n"category":{\n"name":"Predictions",\n"slug":"numerai-predictions",\n"tournament":8,\n"is_per_round":True,\n"is_submission":True,\n"id":3,\n- `"items"` - [..],\n- `"parent"` - {..}\n},\n"owner":{\n"id":2,\n"username":"myusername"\n},\n"model":{\n"name":"mymodel",\n"tournament":8,\n"nmr_staked":100,\n"latest_ranks":{\n"corr":100,\n"fnc":200,\n"mmc":300\n},\n"latest_reps":{\n"corr":0.01,\n"fnc":0.01,\n"mmc":0.01\n},\n"latest_returns":{\n"oneDay":-5.120798695681796,\n"oneYear":None,\n"threeMonths":-5.915974438808858\n},\n"start_date":"2020-10-25T11:08:30"\n},\n"reviews":[...],\n"options":[{\n"id":6,\n"is_on_platform":True,\n"third_party_url":None,\n"description":None,\n"quantity":1,\n"price":1,\n"currency":"NMR",\n"wallet":None,\n"chain":None,\n"stake_limit":None,\n"mode":"file",\n"is_active":True,\n"coupon":None,\n"coupon_specs":None,\n"special_price":None,\n"applied_coupon":None,\n"product_id":108\n}]\n}, ...]\n')),(0,r.kt)("h3",{id:"upload_artifact"},"upload","_","artifact"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'def upload_artifact(file_path: str = "predictions.csv", product_id: int = None, product_full_name: str = None, df: pd.DataFrame = None) -> Dict\n')),(0,r.kt)("p",null,"Upload artifact from file."),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"file_path")," ",(0,r.kt)("em",{parentName:"li"},"str")," - file that will get uploaded"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"product_id")," ",(0,r.kt)("em",{parentName:"li"},"int")," - NumerBay product ID"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"product_full_name")," ",(0,r.kt)("em",{parentName:"li"},"str")," - NumerBay product full name (e.g. numerai-predictions-numerbay),\nused for resolving product_id if product_id is not provided"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"df")," ",(0,r.kt)("em",{parentName:"li"},"pandas.DataFrame")," - pandas DataFrame to upload, if function is\ngiven df and file_path, df will be uploaded.")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"str")," - submission_id")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Example"),":"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'api = NumerBay(username="..", password="..")\nproduct_full_name = "numerai-predictions-numerbay"\napi.upload_predictions("predictions.csv", product_full_name=product_full_name)\n# upload from pandas DataFrame directly:\napi.upload_predictions(df=predictions_df, product_full_name=product_full_name)\n')),(0,r.kt)("h3",{id:"download_artifact"},"download","_","artifact"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def download_artifact(filename: str = None, dest_path: str = None, product_id: int = None, product_full_name: str = None, artifact_id: int = None) -> None\n")),(0,r.kt)("p",null,"Download artifact file."),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"filename")," ",(0,r.kt)("em",{parentName:"li"},"str")," - filename to store as"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"dest_path")," ",(0,r.kt)("em",{parentName:"li"},"str, optional")," - complate path where the file should be\nstored, defaults to the same name as the source file"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"product_id")," ",(0,r.kt)("em",{parentName:"li"},"int")," - NumerBay product ID"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"product_full_name")," ",(0,r.kt)("em",{parentName:"li"},"str")," - NumerBay product full name (e.g. numerai-predictions-numerbay),\nused for resolving product_id if product_id is not provided"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"artifact_id")," ",(0,r.kt)("em",{parentName:"li"},"str")," - Artifact ID for the file to download,\ndefaults to the first artifact for your active order for the product")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Example"),":"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'api = NumerBay(username="..", password="..")\napi.download_artifact("predictions.csv", product_id=2, artifact_id=744)\n')))}s.isMDXComponent=!0}}]);