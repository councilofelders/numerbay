"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[49],{3905:function(e,t,r){r.d(t,{Zo:function(){return s},kt:function(){return f}});var n=r(7294);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function l(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?l(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):l(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function o(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var c=n.createContext({}),p=function(e){var t=n.useContext(c),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},s=function(e){var t=p(e.components);return n.createElement(c.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,l=e.originalType,c=e.parentName,s=o(e,["components","mdxType","originalType","parentName"]),d=p(r),f=a,m=d["".concat(c,".").concat(f)]||d[f]||u[f]||l;return r?n.createElement(m,i(i({ref:t},s),{},{components:r})):n.createElement(m,i({ref:t},s))}));function f(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var l=r.length,i=new Array(l);i[0]=d;var o={};for(var c in t)hasOwnProperty.call(t,c)&&(o[c]=t[c]);o.originalType=e,o.mdxType="string"==typeof e?e:a,i[1]=o;for(var p=2;p<l;p++)i[p]=r[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}d.displayName="MDXCreateElement"},9352:function(e,t,r){r.r(t),r.d(t,{frontMatter:function(){return o},contentTitle:function(){return c},metadata:function(){return p},toc:function(){return s},default:function(){return d}});var n=r(7462),a=r(3366),l=(r(7294),r(3905)),i=["components"],o={sidebar_label:"utils",title:"utils"},c=void 0,p={unversionedId:"reference/utils",id:"reference/utils",title:"utils",description:"collection of utility functions (adapted from numerapi//github.com/uuazed/numerapi)",source:"@site/docs/reference/utils.md",sourceDirName:"reference",slug:"/reference/utils",permalink:"/docs/reference/utils",editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/docs/reference/utils.md",tags:[],version:"current",frontMatter:{sidebar_label:"utils",title:"utils"},sidebar:"API Documentation",previous:{title:"numerbay",permalink:"/docs/reference/numerbay"}},s=[{value:"parse_datetime_string",id:"parse_datetime_string",children:[],level:4},{value:"parse_float_string",id:"parse_float_string",children:[],level:4},{value:"replace",id:"replace",children:[],level:4},{value:"download_file",id:"download_file",children:[],level:4},{value:"get_with_err_handling",id:"get_with_err_handling",children:[],level:4},{value:"post_with_err_handling",id:"post_with_err_handling",children:[],level:4},{value:"encrypt_file_object",id:"encrypt_file_object",children:[],level:4},{value:"decrypt_file",id:"decrypt_file",children:[],level:4}],u={toc:s};function d(e){var t=e.components,r=(0,a.Z)(e,i);return(0,l.kt)("wrapper",(0,n.Z)({},u,r,{components:t,mdxType:"MDXLayout"}),(0,l.kt)("p",null,"collection of utility functions (adapted from numerapi: ",(0,l.kt)("a",{parentName:"p",href:"https://github.com/uuazed/numerapi"},"https://github.com/uuazed/numerapi"),")"),(0,l.kt)("h4",{id:"parse_datetime_string"},"parse","_","datetime","_","string"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"def parse_datetime_string(string: str) -> Optional[datetime.datetime]\n")),(0,l.kt)("p",null,"try to parse string to datetime object"),(0,l.kt)("h4",{id:"parse_float_string"},"parse","_","float","_","string"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"def parse_float_string(string: str) -> Optional[float]\n")),(0,l.kt)("p",null,"try to parse string to decimal.Decimal object"),(0,l.kt)("h4",{id:"replace"},"replace"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"def replace(dictionary: Dict, key: str, function)\n")),(0,l.kt)("p",null,"apply a function to dict item"),(0,l.kt)("h4",{id:"download_file"},"download","_","file"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"def download_file(url: str, dest_path: str, show_progress_bars: bool = True)\n")),(0,l.kt)("p",null,"downloads a file and shows a progress bar. allow resuming a download"),(0,l.kt)("h4",{id:"get_with_err_handling"},"get","_","with","_","err","_","handling"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"def get_with_err_handling(url: str, params: Dict = None, headers: Dict = None, timeout: Optional[int] = None) -> Dict\n")),(0,l.kt)("p",null,"send ",(0,l.kt)("inlineCode",{parentName:"p"},"get")," request and handle (some) errors that might occur"),(0,l.kt)("h4",{id:"post_with_err_handling"},"post","_","with","_","err","_","handling"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"def post_with_err_handling(url: str, body: str = None, json: str = None, headers: Dict = None, timeout: Optional[int] = None) -> Dict\n")),(0,l.kt)("p",null,"send ",(0,l.kt)("inlineCode",{parentName:"p"},"post")," request and handle (some) errors that might occur"),(0,l.kt)("h4",{id:"encrypt_file_object"},"encrypt","_","file","_","object"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"def encrypt_file_object(file: Union[BinaryIO, BytesIO], key: str)\n")),(0,l.kt)("p",null,"encrypt a file stream"),(0,l.kt)("h4",{id:"decrypt_file"},"decrypt","_","file"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"def decrypt_file(dest_path: str, key_path: str = None, key_base64: str = None)\n")),(0,l.kt)("p",null,"decrypt and overwrite a file"))}d.isMDXComponent=!0}}]);