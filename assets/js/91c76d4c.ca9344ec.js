"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[960],{3905:function(e,n,t){t.d(n,{Zo:function(){return d},kt:function(){return m}});var r=t(7294);function o(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function l(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function c(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?l(Object(t),!0).forEach((function(n){o(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):l(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function a(e,n){if(null==e)return{};var t,r,o=function(e,n){if(null==e)return{};var t,r,o={},l=Object.keys(e);for(r=0;r<l.length;r++)t=l[r],n.indexOf(t)>=0||(o[t]=e[t]);return o}(e,n);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(r=0;r<l.length;r++)t=l[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(o[t]=e[t])}return o}var i=r.createContext({}),u=function(e){var n=r.useContext(i),t=n;return e&&(t="function"==typeof e?e(n):c(c({},n),e)),t},d=function(e){var n=u(e.components);return r.createElement(i.Provider,{value:n},e.children)},p={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},s=r.forwardRef((function(e,n){var t=e.components,o=e.mdxType,l=e.originalType,i=e.parentName,d=a(e,["components","mdxType","originalType","parentName"]),s=u(t),m=o,f=s["".concat(i,".").concat(m)]||s[m]||p[m]||l;return t?r.createElement(f,c(c({ref:n},d),{},{components:t})):r.createElement(f,c({ref:n},d))}));function m(e,n){var t=arguments,o=n&&n.mdxType;if("string"==typeof e||o){var l=t.length,c=new Array(l);c[0]=s;var a={};for(var i in n)hasOwnProperty.call(n,i)&&(a[i]=n[i]);a.originalType=e,a.mdxType="string"==typeof e?e:o,c[1]=a;for(var u=2;u<l;u++)c[u]=t[u];return r.createElement.apply(null,c)}return r.createElement.apply(null,t)}s.displayName="MDXCreateElement"},2045:function(e,n,t){t.r(n),t.d(n,{frontMatter:function(){return a},contentTitle:function(){return i},metadata:function(){return u},toc:function(){return d},default:function(){return s}});var r=t(7462),o=t(3366),l=(t(7294),t(3905)),c=["components"],a={sidebar_label:"cli",title:"cli"},i=void 0,u={unversionedId:"reference/cli",id:"reference/cli",title:"cli",description:"Access the numerai API via command line",source:"@site/docs/reference/cli.md",sourceDirName:"reference",slug:"/reference/cli",permalink:"/docs/reference/cli",editUrl:"https://github.com/councilofelders/numerbay/tree/master/docs/docs/reference/cli.md",tags:[],version:"current",frontMatter:{sidebar_label:"cli",title:"cli"},sidebar:"API Documentation",next:{title:"numerbay",permalink:"/docs/reference/numerbay"}},d=[{value:"CommonJSONEncoder Objects",id:"commonjsonencoder-objects",children:[{value:"prettify",id:"prettify",children:[],level:4},{value:"cli",id:"cli",children:[],level:4},{value:"account",id:"account",children:[],level:4},{value:"orders",id:"orders",children:[],level:4},{value:"listings",id:"listings",children:[],level:4},{value:"submit",id:"submit",children:[],level:4},{value:"download",id:"download",children:[],level:4},{value:"version",id:"version",children:[],level:4}],level:2}],p={toc:d};function s(e){var n=e.components,t=(0,o.Z)(e,c);return(0,l.kt)("wrapper",(0,r.Z)({},p,t,{components:n,mdxType:"MDXLayout"}),(0,l.kt)("p",null,"Access the numerai API via command line"),(0,l.kt)("h2",{id:"commonjsonencoder-objects"},"CommonJSONEncoder Objects"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class CommonJSONEncoder(json.JSONEncoder)\n")),(0,l.kt)("p",null,"Common JSON Encoder\njson.dumps(jsonString, cls=CommonJSONEncoder)"),(0,l.kt)("h4",{id:"prettify"},"prettify"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"def prettify(stuff)\n")),(0,l.kt)("p",null,"prettify json"),(0,l.kt)("h4",{id:"cli"},"cli"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@click.group()\ndef cli()\n")),(0,l.kt)("p",null,"Wrapper around the NumerBay API"),(0,l.kt)("h4",{id:"account"},"account"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@cli.command()\ndef account()\n")),(0,l.kt)("p",null,"Get all information about your account!"),(0,l.kt)("h4",{id:"orders"},"orders"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@cli.command()\ndef orders()\n")),(0,l.kt)("p",null,"Get all your orders!"),(0,l.kt)("h4",{id:"listings"},"listings"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@cli.command()\ndef listings()\n")),(0,l.kt)("p",null,"Get all your listings!"),(0,l.kt)("h4",{id:"submit"},"submit"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},'@cli.command()\n@click.option("--product_id", type=int, default=None, help="NumerBay product ID")\n@click.option(\n    "--product_full_name",\n    type=str,\n    default=None,\n    help="NumerBay product full name (e.g. numerai-predictions-numerbay), \\\n    used for resolving product_id if product_id is not provided",\n)\n@click.argument("path", type=click.Path(exists=True))\ndef submit(path, product_id, product_full_name)\n')),(0,l.kt)("p",null,"Upload artifact from file."),(0,l.kt)("h4",{id:"download"},"download"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},'@cli.command()\n@click.option("--product_id", type=int, default=None, help="NumerBay product ID")\n@click.option(\n    "--product_full_name",\n    type=str,\n    default=None,\n    help="NumerBay product full name (e.g. numerai-predictions-numerbay), \\\n    used for resolving product_id if product_id is not provided",\n)\n@click.option(\n    "--artifact_id",\n    type=int,\n    default=None,\n    help="Artifact ID for the file to download, \\\n    defaults to the first artifact for your active order for the product",\n)\n@click.option("--filename", help="filename to store as")\n@click.option(\n    "--dest_path",\n    help="complate path where the file should be stored, \\\n    defaults to the same name as the source file",\n)\ndef download(filename, dest_path, product_id, product_full_name, artifact_id)\n')),(0,l.kt)("p",null,"Download artifact file."),(0,l.kt)("h4",{id:"version"},"version"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@cli.command()\ndef version()\n")),(0,l.kt)("p",null,"Installed numerbay version."))}s.isMDXComponent=!0}}]);