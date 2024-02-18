"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[152],{3905:function(e,t,r){r.d(t,{Zo:function(){return d},kt:function(){return m}});var n=r(7294);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function l(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function i(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var u=n.createContext({}),c=function(e){var t=n.useContext(u),r=t;return e&&(r="function"==typeof e?e(t):l(l({},t),e)),r},d=function(e){var t=c(e.components);return n.createElement(u.Provider,{value:t},e.children)},p="mdxType",s={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},f=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,u=e.parentName,d=i(e,["components","mdxType","originalType","parentName"]),p=c(r),f=a,m=p["".concat(u,".").concat(f)]||p[f]||s[f]||o;return r?n.createElement(m,l(l({ref:t},d),{},{components:r})):n.createElement(m,l({ref:t},d))}));function m(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,l=new Array(o);l[0]=f;var i={};for(var u in t)hasOwnProperty.call(t,u)&&(i[u]=t[u]);i.originalType=e,i[p]="string"==typeof e?e:a,l[1]=i;for(var c=2;c<o;c++)l[c]=r[c];return n.createElement.apply(null,l)}return n.createElement.apply(null,r)}f.displayName="MDXCreateElement"},7042:function(e,t,r){r.r(t),r.d(t,{assets:function(){return u},contentTitle:function(){return l},default:function(){return s},frontMatter:function(){return o},metadata:function(){return i},toc:function(){return c}});var n=r(3117),a=(r(7294),r(3905));const o={},l="Changelog",i={unversionedId:"reference/CHANGELOG",id:"reference/CHANGELOG",title:"Changelog",description:"Notable changes to this project.",source:"@site/docs/reference/CHANGELOG.md",sourceDirName:"reference",slug:"/reference/CHANGELOG",permalink:"/docs/reference/CHANGELOG",draft:!1,editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/docs/reference/CHANGELOG.md",tags:[],version:"current",frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"NumerBlox Integration",permalink:"/docs/tutorial-extras/numerblox"},next:{title:"cli",permalink:"/docs/reference/cli"}},u={},c=[{value:"0.2.3 - 2022-09-20",id:"023---2022-09-20",level:2},{value:"0.2.2 - 2022-05-13",id:"022---2022-05-13",level:2},{value:"0.2.1 - 2022-02-19",id:"021---2022-02-19",level:2},{value:"0.2.0 - 2022-02-02",id:"020---2022-02-02",level:2},{value:"0.1.4 - 2022-01-16",id:"014---2022-01-16",level:2},{value:"0.1.3 - 2022-01-09",id:"013---2022-01-09",level:2}],d={toc:c},p="wrapper";function s(e){let{components:t,...r}=e;return(0,a.kt)(p,(0,n.Z)({},d,r,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h1",{id:"changelog"},"Changelog"),(0,a.kt)("p",null,"Notable changes to this project."),(0,a.kt)("h2",{id:"023---2022-09-20"},"[0.2.3]"," - 2022-09-20"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"added exponential backoff retry for requests")),(0,a.kt)("h2",{id:"022---2022-05-13"},"[0.2.2]"," - 2022-05-13"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"added warning for encrypted upload when no sale available")),(0,a.kt)("h2",{id:"021---2022-02-19"},"[0.2.1]"," - 2022-02-19"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"added install dependency for nacl")),(0,a.kt)("h2",{id:"020---2022-02-02"},"[0.2.0]"," - 2022-02-02"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"added support for per-order artifact upload and encryption"),(0,a.kt)("li",{parentName:"ul"},"added support for per-order artifact download and decryption"),(0,a.kt)("li",{parentName:"ul"},"added support for per-order direct Numerai submission")),(0,a.kt)("h2",{id:"014---2022-01-16"},"[0.1.4]"," - 2022-01-16"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"added ",(0,a.kt)("inlineCode",{parentName:"li"},"get_my_sales")),(0,a.kt)("li",{parentName:"ul"},"added error message for resolving artifact_id in ",(0,a.kt)("inlineCode",{parentName:"li"},"download_artifact")," when no active artifact exists"),(0,a.kt)("li",{parentName:"ul"},"set pypi GitHub workflow to run only on tagged commits"),(0,a.kt)("li",{parentName:"ul"},"trimmed docs to API reference only")),(0,a.kt)("h2",{id:"013---2022-01-09"},"[0.1.3]"," - 2022-01-09"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"initial code release")))}s.isMDXComponent=!0}}]);