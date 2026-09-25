// Vendored from GenomeSpy 0.89.0.
var Xn=Object.defineProperty;var Kn=(t,e)=>()=>(t&&(e=t(t=0)),e);var Zn=(t,e)=>{for(var n in e)Xn(t,n,{get:e[n],enumerable:!0})};var Ft={};Zn(Ft,{GsInspectorPanel:()=>De});function Me(t,e){if(!Rt(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return xe===void 0?e:xe.createHTML(e)}function G(t,e,n=t,a){if(e===q)return e;let i=a===void 0?n._$Cl:n._$Co?.[a],r=at(e)?void 0:e._$litDirective$;return i?.constructor!==r&&(i?._$AO?.(!1),r===void 0?i=void 0:(i=new r(t),i._$AT(t,n,a)),a===void 0?n._$Cl=i:(n._$Co??=[])[a]=i),i!==void 0&&(e=G(t,i._$AS(t,e.values),i,a)),e}function Pt(t){let e=Object.entries(t);return e.length?e.map(([n,a])=>n+": "+a).join(", "):"-"}function wa(t){return t.disposed?"disposed":t.initialized?t.completed?"done":"active":"new"}function L(t){return t===void 0?"-":typeof t=="string"?t:JSON.stringify(t)}function ze(t){return c`
        <table>
            <thead>
                <tr>
                    <th>name</th>
                    <th>kind</th>
                    <th>writable</th>
                    <th>value</th>
                    <th>config</th>
                </tr>
            </thead>
            <tbody>
                ${t.map(e=>c`
                        <tr>
                            <td>${e.name}</td>
                            <td>${e.kind}</td>
                            <td>${String(e.writable)}</td>
                            <td>${L(e.value)}</td>
                            <td>
                                ${e.config?L(e.config):"-"}
                            </td>
                        </tr>
                    `)}
            </tbody>
        </table>
    `}var ft,Nt,Ot,be,Pe,Qn,ta,ea,ve,na,aa,ia,ra,sa,oa,ht,ye,la,da,et,_t,_e,$e,B,Mt,we,ut,xe,Ce,C,Ne,ca,T,nt,at,Rt,fa,Et,tt,ke,Ae,z,Se,Ie,Oe,c,q,g,Ee,D,ua,Ct,ha,jt,mt,ma,pa,ga,ba,va,ya,zt,F,$a,Dt,xa,ka,De,Lt=Kn(()=>{ft=globalThis,Nt=ft.ShadowRoot&&(ft.ShadyCSS===void 0||ft.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,Ot=Symbol(),be=new WeakMap,Pe=class{constructor(t,e,n){if(this._$cssResult$=!0,n!==Ot)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o,e=this.t;if(Nt&&t===void 0){let n=e!==void 0&&e.length===1;n&&(t=be.get(e)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),n&&be.set(e,t))}return t}toString(){return this.cssText}},Qn=t=>new Pe(typeof t=="string"?t:t+"",void 0,Ot),ta=(t,...e)=>new Pe(t.length===1?t[0]:e.reduce((n,a,i)=>n+(r=>{if(r._$cssResult$===!0)return r.cssText;if(typeof r=="number")return r;throw Error("Value passed to 'css' function must be a 'css' function result: "+r+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(a)+t[i+1],t[0]),t,Ot),ea=(t,e)=>{if(Nt)t.adoptedStyleSheets=e.map(n=>n instanceof CSSStyleSheet?n:n.styleSheet);else for(let n of e){let a=document.createElement("style"),i=ft.litNonce;i!==void 0&&a.setAttribute("nonce",i),a.textContent=n.cssText,t.appendChild(a)}},ve=Nt?t=>t:t=>t instanceof CSSStyleSheet?(e=>{let n="";for(let a of e.cssRules)n+=a.cssText;return Qn(n)})(t):t,{is:na,defineProperty:aa,getOwnPropertyDescriptor:ia,getOwnPropertyNames:ra,getOwnPropertySymbols:sa,getPrototypeOf:oa}=Object,ht=globalThis,ye=ht.trustedTypes,la=ye?ye.emptyScript:"",da=ht.reactiveElementPolyfillSupport,et=(t,e)=>t,_t={toAttribute(t,e){switch(e){case Boolean:t=t?la:null;break;case Object:case Array:t=t==null?t:JSON.stringify(t)}return t},fromAttribute(t,e){let n=t;switch(e){case Boolean:n=t!==null;break;case Number:n=t===null?null:Number(t);break;case Object:case Array:try{n=JSON.parse(t)}catch{n=null}}return n}},_e=(t,e)=>!na(t,e),$e={attribute:!0,type:String,converter:_t,reflect:!1,useDefault:!1,hasChanged:_e};Symbol.metadata??=Symbol("metadata"),ht.litPropertyMetadata??=new WeakMap;B=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=$e){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){let n=Symbol(),a=this.getPropertyDescriptor(t,n,e);a!==void 0&&aa(this.prototype,t,a)}}static getPropertyDescriptor(t,e,n){let{get:a,set:i}=ia(this.prototype,t)??{get(){return this[e]},set(r){this[e]=r}};return{get:a,set(r){let s=a?.call(this);i?.call(this,r),this.requestUpdate(t,s,n)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??$e}static _$Ei(){if(this.hasOwnProperty(et("elementProperties")))return;let t=oa(this);t.finalize(),t.l!==void 0&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(et("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(et("properties"))){let e=this.properties,n=[...ra(e),...sa(e)];for(let a of n)this.createProperty(a,e[a])}let t=this[Symbol.metadata];if(t!==null){let e=litPropertyMetadata.get(t);if(e!==void 0)for(let[n,a]of e)this.elementProperties.set(n,a)}this._$Eh=new Map;for(let[e,n]of this.elementProperties){let a=this._$Eu(e,n);a!==void 0&&this._$Eh.set(a,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){let e=[];if(Array.isArray(t)){let n=new Set(t.flat(1/0).reverse());for(let a of n)e.unshift(ve(a))}else t!==void 0&&e.push(ve(t));return e}static _$Eu(t,e){let n=e.attribute;return n===!1?void 0:typeof n=="string"?n:typeof t=="string"?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),this.renderRoot!==void 0&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){let t=new Map,e=this.constructor.elementProperties;for(let n of e.keys())this.hasOwnProperty(n)&&(t.set(n,this[n]),delete this[n]);t.size>0&&(this._$Ep=t)}createRenderRoot(){let t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return ea(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,n){this._$AK(t,n)}_$ET(t,e){let n=this.constructor.elementProperties.get(t),a=this.constructor._$Eu(t,n);if(a!==void 0&&n.reflect===!0){let i=(n.converter?.toAttribute===void 0?_t:n.converter).toAttribute(e,n.type);this._$Em=t,i==null?this.removeAttribute(a):this.setAttribute(a,i),this._$Em=null}}_$AK(t,e){let n=this.constructor,a=n._$Eh.get(t);if(a!==void 0&&this._$Em!==a){let i=n.getPropertyOptions(a),r=typeof i.converter=="function"?{fromAttribute:i.converter}:i.converter?.fromAttribute===void 0?_t:i.converter;this._$Em=a;let s=r.fromAttribute(e,i.type);this[a]=s??this._$Ej?.get(a)??s,this._$Em=null}}requestUpdate(t,e,n,a=!1,i){if(t!==void 0){let r=this.constructor;if(a===!1&&(i=this[t]),n??=r.getPropertyOptions(t),!((n.hasChanged??_e)(i,e)||n.useDefault&&n.reflect&&i===this._$Ej?.get(t)&&!this.hasAttribute(r._$Eu(t,n))))return;this.C(t,e,n)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(t,e,{useDefault:n,reflect:a,wrapped:i},r){n&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,r??e??this[t]),i!==!0||r!==void 0)||(this._$AL.has(t)||(this.hasUpdated||n||(e=void 0),this._$AL.set(t,e)),a===!0&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}let t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(let[a,i]of this._$Ep)this[a]=i;this._$Ep=void 0}let n=this.constructor.elementProperties;if(n.size>0)for(let[a,i]of n){let{wrapped:r}=i,s=this[a];r!==!0||this._$AL.has(a)||s===void 0||this.C(a,void 0,i,s)}}let t=!1,e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(n=>n.hostUpdate?.()),this.update(e)):this._$EM()}catch(n){throw t=!1,this._$EM(),n}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(e=>e.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(e=>this._$ET(e,this[e])),this._$EM()}updated(t){}firstUpdated(t){}};B.elementStyles=[],B.shadowRootOptions={mode:"open"},B[et("elementProperties")]=new Map,B[et("finalized")]=new Map,da?.({ReactiveElement:B}),(ht.reactiveElementVersions??=[]).push("2.1.2");Mt=globalThis,we=t=>t,ut=Mt.trustedTypes,xe=ut?ut.createPolicy("lit-html",{createHTML:t=>t}):void 0,Ce="$lit$",C=`lit$${Math.random().toFixed(9).slice(2)}$`,Ne="?"+C,ca=`<${Ne}>`,T=document,nt=()=>T.createComment(""),at=t=>t===null||typeof t!="object"&&typeof t!="function",Rt=Array.isArray,fa=t=>Rt(t)||typeof t?.[Symbol.iterator]=="function",Et=`[ 	
\f\r]`,tt=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,ke=/-->/g,Ae=/>/g,z=RegExp(`>|${Et}(?:([^\\s"'>=/]+)(${Et}*=${Et}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),Se=/'/g,Ie=/"/g,Oe=/^(?:script|style|textarea|title)$/i,c=(t=>(e,...n)=>({_$litType$:t,strings:e,values:n}))(1),q=Symbol.for("lit-noChange"),g=Symbol.for("lit-nothing"),Ee=new WeakMap,D=T.createTreeWalker(T,129);ua=(t,e)=>{let n=t.length-1,a=[],i,r=e===2?"<svg>":e===3?"<math>":"",s=tt;for(let o=0;o<n;o++){let d=t[o],f,h,m=-1,p=0;for(;p<d.length&&(s.lastIndex=p,h=s.exec(d),h!==null);)p=s.lastIndex,s===tt?h[1]==="!--"?s=ke:h[1]===void 0?h[2]===void 0?h[3]!==void 0&&(s=z):(Oe.test(h[2])&&(i=RegExp("</"+h[2],"g")),s=z):s=Ae:s===z?h[0]===">"?(s=i??tt,m=-1):h[1]===void 0?m=-2:(m=s.lastIndex-h[2].length,f=h[1],s=h[3]===void 0?z:h[3]==='"'?Ie:Se):s===Ie||s===Se?s=z:s===ke||s===Ae?s=tt:(s=z,i=void 0);let v=s===z&&t[o+1].startsWith("/>")?" ":"";r+=s===tt?d+ca:m>=0?(a.push(f),d.slice(0,m)+Ce+d.slice(m)+C+v):d+C+(m===-2?o:v)}return[Me(t,r+(t[n]||"<?>")+(e===2?"</svg>":e===3?"</math>":"")),a]},Ct=class Re{constructor({strings:e,_$litType$:n},a){let i;this.parts=[];let r=0,s=0,o=e.length-1,d=this.parts,[f,h]=ua(e,n);if(this.el=Re.createElement(f,a),D.currentNode=this.el.content,n===2||n===3){let m=this.el.content.firstChild;m.replaceWith(...m.childNodes)}for(;(i=D.nextNode())!==null&&d.length<o;){if(i.nodeType===1){if(i.hasAttributes())for(let m of i.getAttributeNames())if(m.endsWith(Ce)){let p=h[s++],v=i.getAttribute(m).split(C),k=/([.?@])?(.*)/.exec(p);d.push({type:1,index:r,name:k[2],strings:v,ctor:k[1]==="."?ma:k[1]==="?"?pa:k[1]==="@"?ga:mt}),i.removeAttribute(m)}else m.startsWith(C)&&(d.push({type:6,index:r}),i.removeAttribute(m));if(Oe.test(i.tagName)){let m=i.textContent.split(C),p=m.length-1;if(p>0){i.textContent=ut?ut.emptyScript:"";for(let v=0;v<p;v++)i.append(m[v],nt()),D.nextNode(),d.push({type:2,index:++r});i.append(m[p],nt())}}}else if(i.nodeType===8)if(i.data===Ne)d.push({type:2,index:r});else{let m=-1;for(;(m=i.data.indexOf(C,m+1))!==-1;)d.push({type:7,index:r}),m+=C.length-1}r++}}static createElement(e,n){let a=T.createElement("template");return a.innerHTML=e,a}};ha=class{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){let{el:{content:e},parts:n}=this._$AD,a=(t?.creationScope??T).importNode(e,!0);D.currentNode=a;let i=D.nextNode(),r=0,s=0,o=n[0];for(;o!==void 0;){if(r===o.index){let d;o.type===2?d=new jt(i,i.nextSibling,this,t):o.type===1?d=new o.ctor(i,o.name,o.strings,this,t):o.type===6&&(d=new ba(i,this,t)),this._$AV.push(d),o=n[++s]}r!==o?.index&&(i=D.nextNode(),r++)}return D.currentNode=T,a}p(t){let e=0;for(let n of this._$AV)n!==void 0&&(n.strings===void 0?n._$AI(t[e]):(n._$AI(t,n,e),e+=n.strings.length-2)),e++}},jt=class je{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(e,n,a,i){this.type=2,this._$AH=g,this._$AN=void 0,this._$AA=e,this._$AB=n,this._$AM=a,this.options=i,this._$Cv=i?.isConnected??!0}get parentNode(){let e=this._$AA.parentNode,n=this._$AM;return n!==void 0&&e?.nodeType===11&&(e=n.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,n=this){e=G(this,e,n),at(e)?e===g||e==null||e===""?(this._$AH!==g&&this._$AR(),this._$AH=g):e!==this._$AH&&e!==q&&this._(e):e._$litType$===void 0?e.nodeType===void 0?fa(e)?this.k(e):this._(e):this.T(e):this.$(e)}O(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}T(e){this._$AH!==e&&(this._$AR(),this._$AH=this.O(e))}_(e){this._$AH!==g&&at(this._$AH)?this._$AA.nextSibling.data=e:this.T(T.createTextNode(e)),this._$AH=e}$(e){let{values:n,_$litType$:a}=e,i=typeof a=="number"?this._$AC(e):(a.el===void 0&&(a.el=Ct.createElement(Me(a.h,a.h[0]),this.options)),a);if(this._$AH?._$AD===i)this._$AH.p(n);else{let r=new ha(i,this),s=r.u(this.options);r.p(n),this.T(s),this._$AH=r}}_$AC(e){let n=Ee.get(e.strings);return n===void 0&&Ee.set(e.strings,n=new Ct(e)),n}k(e){Rt(this._$AH)||(this._$AH=[],this._$AR());let n=this._$AH,a,i=0;for(let r of e)i===n.length?n.push(a=new je(this.O(nt()),this.O(nt()),this,this.options)):a=n[i],a._$AI(r),i++;i<n.length&&(this._$AR(a&&a._$AB.nextSibling,i),n.length=i)}_$AR(e=this._$AA.nextSibling,n){for(this._$AP?.(!1,!0,n);e!==this._$AB;){let a=we(e).nextSibling;we(e).remove(),e=a}}setConnected(e){this._$AM===void 0&&(this._$Cv=e,this._$AP?.(e))}},mt=class{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,n,a,i){this.type=1,this._$AH=g,this._$AN=void 0,this.element=t,this.name=e,this._$AM=a,this.options=i,n.length>2||n[0]!==""||n[1]!==""?(this._$AH=Array(n.length-1).fill(new String),this.strings=n):this._$AH=g}_$AI(t,e=this,n,a){let i=this.strings,r=!1;if(i===void 0)t=G(this,t,e,0),r=!at(t)||t!==this._$AH&&t!==q,r&&(this._$AH=t);else{let s=t,o,d;for(t=i[0],o=0;o<i.length-1;o++)d=G(this,s[n+o],e,o),d===q&&(d=this._$AH[o]),r||=!at(d)||d!==this._$AH[o],d===g?t=g:t!==g&&(t+=(d??"")+i[o+1]),this._$AH[o]=d}r&&!a&&this.j(t)}j(t){t===g?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}},ma=class extends mt{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===g?void 0:t}},pa=class extends mt{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==g)}},ga=class extends mt{constructor(t,e,n,a,i){super(t,e,n,a,i),this.type=5}_$AI(t,e=this){if((t=G(this,t,e,0)??g)===q)return;let n=this._$AH,a=t===g&&n!==g||t.capture!==n.capture||t.once!==n.once||t.passive!==n.passive,i=t!==g&&(n===g||a);a&&this.element.removeEventListener(this.name,this,n),i&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){typeof this._$AH=="function"?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}},ba=class{constructor(t,e,n){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=n}get _$AU(){return this._$AM._$AU}_$AI(t){G(this,t)}},va=Mt.litHtmlPolyfillSupport;va?.(Ct,jt),(Mt.litHtmlVersions??=[]).push("3.3.3");ya=(t,e,n)=>{let a=n?.renderBefore??e,i=a._$litPart$;if(i===void 0){let r=n?.renderBefore??null;a._$litPart$=i=new jt(e.insertBefore(nt(),r),r,void 0,n??{})}return i._$AI(t),i},zt=globalThis,F=class extends B{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){let t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){let e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=ya(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return q}};F._$litElement$=!0,F.finalized=!0,zt.litElementHydrateSupport?.({LitElement:F});$a=zt.litElementPolyfillSupport;$a?.({LitElement:F}),(zt.litElementVersions??=[]).push("4.2.2");Dt=ta`
    :host {
        display: block;
        height: 100%;
        min-height: 0;
        color: #d8dee9;
        background: #20242b;
        font:
            12px/1.45 ui-monospace,
            SFMono-Regular,
            Menlo,
            Consolas,
            "Liberation Mono",
            monospace;
    }

    .shell {
        display: grid;
        grid-template-rows: auto 1fr;
        height: 100%;
        min-height: 0;
    }

    .toolbar {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0.65rem;
        border-bottom: 1px solid #3a404a;
        background: #292e36;
    }

    .toolbar-title {
        white-space: nowrap;
    }

    .panel-tabs {
        display: flex;
        gap: 0.2rem;
    }

    button,
    label {
        font: inherit;
    }

    button {
        color: #d8dee9;
        background: #353b45;
        border: 1px solid #4a5260;
        border-radius: 4px;
        padding: 0.2rem 0.45rem;
        cursor: pointer;
    }

    button:hover {
        background: #414856;
    }

    .panel-tab {
        color: #b8c0cc;
        background: transparent;
        border-color: transparent;
    }

    .panel-tab.selected {
        color: #f4f7fb;
        background: #174f78;
        border-color: #2d6e9e;
    }

    .close-button {
        margin-left: auto;
    }

    .main {
        display: grid;
        grid-template-columns: minmax(15rem, 38%) minmax(0, 1fr);
        height: 100%;
        min-height: 0;
    }

    .single-panel {
        display: block;
        box-sizing: border-box;
        height: 100%;
        min-height: 0;
        overflow: auto;
        padding: 0.75rem;
    }

    .tree,
    .details {
        min-height: 0;
        overflow: auto;
    }

    .tree {
        border-right: 1px solid #3a404a;
        padding: 0.4rem 0;
    }

    .tree-controls {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.2rem 0.65rem 0.45rem;
        border-bottom: 1px solid #303743;
        margin-bottom: 0.3rem;
        color: #b8c0cc;
    }

    .details {
        padding: 0.75rem;
    }

    .empty {
        color: #9aa6b2;
        padding: 0.75rem;
    }

    .section-note {
        margin: -0.35rem 0 0.6rem;
        color: #9aa6b2;
    }

    .debug-errors {
        margin: 0 0 0.75rem;
        padding: 0.5rem 0.65rem;
        border: 1px solid #8f6a2f;
        border-radius: 4px;
        background: #34291c;
        color: #ffcf8a;
    }

    .debug-errors ul {
        margin: 0.35rem 0 0;
        padding-left: 1rem;
    }

    .node {
        display: grid;
        grid-template-columns: 1fr auto;
        align-items: center;
        gap: 0.45rem;
        width: 100%;
        min-width: 0;
        padding: 0.12rem 0.65rem;
        border: 0;
        border-radius: 0;
        background: transparent;
        color: inherit;
        text-align: left;
    }

    .node:hover {
        background: #303743;
    }

    .node.selected {
        background: #174f78;
    }

    .node.warning {
        color: #ffcf8a;
    }

    .node-main {
        min-width: 0;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

    .node-meta {
        color: #9aa6b2;
        white-space: nowrap;
    }

    .badge {
        display: inline-block;
        margin-left: 0.35rem;
        padding: 0 0.25rem;
        border: 1px solid #596273;
        border-radius: 3px;
        color: #b8c0cc;
    }

    h2 {
        margin: 0 0 0.6rem;
        font-size: 0.9rem;
        line-height: 1.2;
    }

    h3 {
        margin: 0 0 0.6rem;
        font-size: 1rem;
        line-height: 1.2;
    }

    h3 {
        margin-top: 1rem;
        font-size: 0.8rem;
        color: #9aa6b2;
        text-transform: uppercase;
    }

    dl {
        display: grid;
        grid-template-columns: max-content minmax(0, 1fr);
        gap: 0.25rem 0.75rem;
        margin: 0;
    }

    dt {
        color: #9aa6b2;
    }

    dd {
        margin: 0;
        min-width: 0;
        overflow-wrap: anywhere;
    }

    pre {
        margin: 0;
        padding: 0.6rem;
        overflow: auto;
        border: 1px solid #3a404a;
        border-radius: 4px;
        background: #171a20;
        color: #d8dee9;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 0.75rem;
    }

    th,
    td {
        padding: 0.25rem 0.35rem;
        border-bottom: 1px solid #303743;
        text-align: left;
        vertical-align: top;
    }

    th {
        color: #9aa6b2;
        font-weight: 600;
    }

    .linked {
        color: #8cc7ff;
        cursor: pointer;
    }

    .member-list {
        margin: 0;
        padding-left: 1rem;
    }

    .member-list li {
        margin: 0 0 0.15rem;
    }

    .link-button,
    .inline-action {
        padding: 0;
        border: 0;
        background: transparent;
        color: #8cc7ff;
    }

    .link-button {
        text-align: left;
    }

    .current-member {
        color: #d8dee9;
    }

    .current-member::after {
        color: #9aa6b2;
        content: " current";
    }

    .inline-action {
        margin-top: 0.25rem;
    }

    .link-button:hover,
    .inline-action:hover {
        background: transparent;
        text-decoration: underline;
    }

    .muted {
        color: #9aa6b2;
    }

    .flow-first {
        max-height: 22rem;
    }
`,xa=class extends F{static properties={snapshot:{attribute:!1},selectedFlowNodeId:{attribute:!1}};static styles=Dt;constructor(){super(),this.snapshot={dataflow:{sourceIds:[],nodes:[],collectorCount:0}},this.selectedFlowNodeId=void 0}render(){if(this.snapshot.dataflow.sourceIds.length===0)return c`
                <div class="single-panel">
                    <p class="empty">No dataflow has been built yet.</p>
                </div>
            `;let t=this.selectedFlowNodeId?this.#n(this.selectedFlowNodeId):this.#n(this.snapshot.dataflow.sourceIds[0]);return c`
            <div class="main">
                <div class="tree">
                    <p class="empty">
                        ${this.snapshot.dataflow.sourceIds.length} sources,
                        ${this.snapshot.dataflow.collectorCount} collectors
                    </p>
                    ${this.snapshot.dataflow.sourceIds.map(e=>this.#t(this.#n(e),0))}
                </div>
                <div class="details">
                    ${this.#e(t)}
                </div>
            </div>
        `}#t(t,e){let n=t.id===this.selectedFlowNodeId,a=t.disposed||!t.initialized;return c`
            <button
                class=${["node",n?"selected":"",a?"warning":""].join(" ")}
                style=${`padding-left: ${.65+e*1.1}rem`}
                @click=${()=>this.#a(t.id)}
                @mouseenter=${()=>this.#i(t.viewId)}
                @mouseleave=${()=>this.#i(void 0)}
            >
                <span class="node-main">
                    ${t.childIds.length>0?"v":"-"} ${t.label}
                    ${t.completed?c`<span class="badge">done</span>`:g}
                    ${t.disposed?c`<span class="badge">disposed</span>`:g}
                    ${t.initialized?g:c`<span class="badge">new</span>`}
                </span>
                <span class="node-meta">out ${t.count}</span>
            </button>
            ${t.childIds.map(i=>this.#t(this.#n(i),e+1))}
        `}#e(t){return c`
            <h2>${t.label}</h2>
            <dl>
                <dt>id</dt>
                <dd>${t.id}</dd>
                <dt>out count</dt>
                <dd>${t.count}</dd>
                <dt>children</dt>
                <dd>${t.childIds.length}</dd>
                <dt>completed</dt>
                <dd>${String(t.completed)}</dd>
                <dt>initialized</dt>
                <dd>${String(t.initialized)}</dd>
                <dt>disposed</dt>
                <dd>${String(t.disposed)}</dd>
                <dt>view</dt>
                <dd>
                    ${t.viewId?c`<span
                              class="linked"
                              @click=${()=>this.#s(t.viewId)}
                              >${t.viewPath}</span
                          >`:"-"}
                </dd>
                <dt>domain-sensitive scales</dt>
                <dd>
                    ${t.domainSensitiveScaleChannels.length?t.domainSensitiveScaleChannels.join(", "):"-"}
                </dd>
            </dl>

            <h3>Params</h3>
            ${t.params?c`<pre>${L(t.params)}</pre>`:c`<p class="empty">No flow node parameters.</p>`}

            <h3>First Datum</h3>
            ${t.first?c`<pre class="flow-first">${L(t.first)}</pre>`:c`<p class="empty">
                      ${t.count>0?"No datum preview is available.":"No data was propagated."}
                  </p>`}
        `}#n(t){let e=this.snapshot.dataflow.nodes.find(n=>n.id===t);if(!e)throw Error("Unknown inspector flow node: "+t);return e}#a(t){this.selectedFlowNodeId=t,this.dispatchEvent(new CustomEvent("select-flow-node",{detail:{flowNodeId:t},bubbles:!0,composed:!0}))}#s(t){this.dispatchEvent(new CustomEvent("select-view",{detail:{viewId:t},bubbles:!0,composed:!0}))}#i(t){this.dispatchEvent(new CustomEvent("highlight-view",{detail:{viewId:t},bubbles:!0,composed:!0}))}};customElements.define("gs-inspector-dataflow-panel",xa);ka=class extends F{static properties={snapshot:{attribute:!1}};static styles=Dt;constructor(){super(),this.snapshot={params:{scopes:[]}}}render(){let t=this.snapshot.params.scopes.filter(e=>e.params.length>0);return t.length===0?c`
                <div class="single-panel">
                    <p class="empty">No params.</p>
                </div>
            `:c`
            <div class="single-panel">
                <h2>Params</h2>
                ${t.map(e=>c`
                        <h3>
                            <span
                                class="linked"
                                @click=${()=>this.#t(e.viewId)}
                                >${e.viewPath}</span
                            >
                            <span class="muted">${e.scopeId}</span>
                        </h3>
                        ${ze(e.params)}
                    `)}
            </div>
        `}#t(t){this.dispatchEvent(new CustomEvent("select-view",{detail:{viewId:t},bubbles:!0,composed:!0}))}};customElements.define("gs-inspector-params-panel",ka);De=class extends F{static properties={session:{attribute:!1},snapshot:{state:!0},selectedViewId:{state:!0},selectedFlowNodeId:{state:!0},activePanel:{state:!0},expandedResolutionMemberIds:{state:!0}};static styles=Dt;constructor(){super(),this.session=void 0,this.snapshot={rootId:void 0,nodes:[],resolutions:{scales:[],axes:[],legends:[]},dataflow:{sourceIds:[],nodes:[],collectorCount:0},params:{scopes:[]},marks:{marks:[]}},this.selectedViewId=void 0,this.selectedFlowNodeId=void 0,this.activePanel="elements",this.expandedResolutionMemberIds=new Set}connectedCallback(){super.connectedCallback(),this.#s()}disconnectedCallback(){this.#i(),super.disconnectedCallback()}updated(t){t.has("session")&&(this.#i(),this.#s()),(t.has("selectedViewId")||t.has("activePanel"))&&this.#d()}#t=void 0;#e=t=>{this.selectedViewId=t.detail.viewId,this.activePanel="elements"};#n=t=>{this.selectedFlowNodeId=t.detail.flowNodeId};#a=t=>{this.session?.highlightView(t.detail.viewId)};#s(){if(!this.session||this.#t)return;let t=()=>{this.snapshot=this.session.snapshot,this.selectedViewId&&!this.snapshot.nodes.some(e=>e.id===this.selectedViewId)?this.selectedViewId=this.snapshot.rootId:this.selectedViewId??=this.snapshot.rootId,this.selectedFlowNodeId&&!this.snapshot.dataflow.nodes.some(e=>e.id===this.selectedFlowNodeId)?this.selectedFlowNodeId=this.snapshot.dataflow.sourceIds[0]:this.selectedFlowNodeId??=this.snapshot.dataflow.sourceIds[0]};this.session.addEventListener("snapshot",t),this.#t=()=>{this.session?.removeEventListener("snapshot",t),this.#t=void 0},t()}#i(){this.#t?.()}#d(){this.activePanel!=="elements"&&this.activePanel!=="resolutions"||this.renderRoot.querySelector(`.node.selected[data-view-id="${this.selectedViewId}"]`)?.scrollIntoView({block:"nearest",inline:"nearest"})}render(){let t=this.#g(),e=this.#N();return c`
            <div class="shell">
                <div class="toolbar">
                    <strong class="toolbar-title">Inspector</strong>
                    <span class="panel-tabs">
                        ${this.#r("elements","Views")}
                        ${this.#r("resolutions","Resolutions")}
                        ${this.#r("dataflow","Dataflow")}
                        ${this.#r("params","Params")}
                    </span>
                    <button @click=${()=>this.#C()}>Refresh</button>
                    <button
                        class="close-button"
                        title="Close inspector"
                        aria-label="Close inspector"
                        @click=${()=>this.#f()}
                    >
                        x
                    </button>
                </div>
                ${this.#c(t,e)}
            </div>
        `}#f(){this.dispatchEvent(new CustomEvent("close",{bubbles:!0,composed:!0}))}#r(t,e){return c`
            <button
                class=${this.activePanel===t?"panel-tab selected":"panel-tab"}
                @click=${()=>{this.activePanel=t}}
            >
                ${e}
            </button>
        `}#c(t,e){return this.activePanel==="dataflow"?c`
                <gs-inspector-dataflow-panel
                    .snapshot=${this.snapshot}
                    .selectedFlowNodeId=${this.selectedFlowNodeId}
                    @select-flow-node=${this.#n}
                    @select-view=${this.#e}
                    @highlight-view=${this.#a}
                ></gs-inspector-dataflow-panel>
            `:this.activePanel==="params"?c`
                <gs-inspector-params-panel
                    .snapshot=${this.snapshot}
                    @select-view=${this.#e}
                ></gs-inspector-params-panel>
            `:this.activePanel==="resolutions"?c`
                <div class="main">
                    ${this.#u(t)}
                    <div class="details">${this.#I()}</div>
                </div>
            `:c`
            <div class="main">
                ${this.#u(t)}
                <div class="details">
                    ${e?this.#l(e):c`<div class="empty">No view selected.</div>`}
                </div>
            </div>
        `}#u(t){return c`
            <div class="tree">
                <div class="tree-controls">
                    <label>
                        <input
                            type="checkbox"
                            .checked=${this.session?.includeChrome??!1}
                            @change=${e=>{let n=e.target;this.session?.setIncludeChrome(n.checked)}}
                        />
                        Show view chrome
                    </label>
                </div>
                ${t?this.#h(t,0):c`<div class="empty">
                              Launch the app to inspect the hierarchy.
                          </div>`}
            </div>
        `}#h(t,e){return c`
            <button
                class=${t.id===this.selectedViewId?"node selected":"node"}
                data-view-id=${t.id}
                style=${`padding-left: ${.65+e*1.1}rem`}
                @click=${()=>{this.selectedViewId=t.id}}
                @mouseenter=${()=>this.session?.highlightView(t.id)}
                @mouseleave=${()=>this.session?.highlightView(void 0)}
            >
                <span class="node-main">
                    ${t.childIds.length>0?"v":"-"} ${t.name}
                    ${t.chrome?c`<span class="badge">chrome</span>`:g}
                    ${t.visible?g:c`<span class="badge">hidden</span>`}
                </span>
                <span class="node-meta"> ${t.markType??t.type} </span>
            </button>
            ${t.childIds.map(n=>this.#h(this.#O(n),e+1))}
        `}#l(t){return c`
            <h2>${t.path}</h2>
            ${this.#o(t)}
            <dl>
                <dt>id</dt>
                <dd>${t.id}</dd>
                <dt>class</dt>
                <dd>${t.className}</dd>
                <dt>type</dt>
                <dd>${t.type}</dd>
                <dt>mark</dt>
                <dd>${t.markType??"-"}</dd>
                <dt>selector</dt>
                <dd>${t.selector?JSON.stringify(t.selector):"-"}</dd>
                <dt>visible</dt>
                <dd>${String(t.visible)}</dd>
                <dt>configured visible</dt>
                <dd>${String(t.configuredVisible)}</dd>
                <dt>data init</dt>
                <dd>${t.dataInitializationState}</dd>
                <dt>bounds</dt>
                <dd>${t.bounds?JSON.stringify(t.bounds):"-"}</dd>
            </dl>

            <h3>Encodings</h3>
            <p class="section-note">
                Channels defined on this view and the resolution ids they use.
            </p>
            ${this.#S(t)}

            <h3>Resolutions</h3>
            <p class="section-note">
                Direct scale, axis, and legend resolution ids registered on this
                view.
            </p>
            <dl>
                <dt>scale</dt>
                <dd>${Pt(t.scaleResolutionIds)}</dd>
                <dt>axis</dt>
                <dd>${Pt(t.axisResolutionIds)}</dd>
                <dt>legend</dt>
                <dd>${Pt(t.legendResolutionIds)}</dd>
            </dl>

            <h3>Dataflow</h3>
            <p class="section-note">
                Flow nodes owned by this view. Use the Dataflow button to jump
                to the full flow tree.
            </p>
            ${this.#A(t)}

            <h3>Params</h3>
            <p class="section-note">Params declared in this view scope.</p>
            ${this.#P(t)}

            <h3>Mark</h3>
            <p class="section-note">
                Runtime mark state for unit views, including data and vertex
                counts.
            </p>
            ${this.#_(t)}

            <h3>Related Resolutions</h3>
            <p class="section-note">
                Resolutions that this view uses directly or participates in as a
                member. The Resolutions tab shows the global list.
            </p>
            ${this.#E(t)}

            <h3>Spec</h3>
            <p class="section-note">
                Authored or generated view spec snapshot for this runtime view.
            </p>
            <pre>${JSON.stringify(t.spec,null,2)}</pre>
        `}#o(t){return!t.debugErrors||t.debugErrors.length===0?g:c`
            <div class="debug-errors">
                <strong>Incomplete debug snapshot</strong>
                <ul>
                    ${t.debugErrors.map(e=>c`
                            <li>${e.field}: ${e.message}</li>
                        `)}
                </ul>
            </div>
        `}#A(t){let e=this.#M(t.id);return e.length===0?c`<p class="empty">No linked dataflow nodes.</p>`:c`
            <table>
                <thead>
                    <tr>
                        <th>node</th>
                        <th>out</th>
                        <th>state</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    ${e.map(n=>c`
                            <tr>
                                <td>${n.label}</td>
                                <td>${n.count}</td>
                                <td>${wa(n)}</td>
                                <td>
                                    <button
                                        @click=${()=>this.#R(n.id)}
                                    >
                                        Dataflow
                                    </button>
                                </td>
                            </tr>
                        `)}
                </tbody>
            </table>
        `}#S(t){let e=Object.values(t.encodings);return e.length===0?c`<p class="empty">No encodings.</p>`:c`
            <table>
                <thead>
                    <tr>
                        <th>channel</th>
                        <th>field / expr / value</th>
                        <th>type</th>
                        <th>scale</th>
                        <th>axis</th>
                        <th>legend</th>
                    </tr>
                </thead>
                <tbody>
                    ${e.map(n=>c`
                            <tr>
                                <td>${n.channel}</td>
                                <td>
                                    ${n.field??n.expr??L(n.value)}
                                </td>
                                <td>${n.type??"-"}</td>
                                <td>${n.scaleResolutionId??"-"}</td>
                                <td>${n.axisResolutionId??"-"}</td>
                                <td>${n.legendResolutionId??"-"}</td>
                            </tr>
                        `)}
                </tbody>
            </table>
        `}#I(){let{scales:t,axes:e,legends:n}=this.snapshot.resolutions;return c`
            <h3>Scales</h3>
            ${this.#b(t)}
            <h3>Axes</h3>
            ${this.#v(e)}
            <h3>Legends</h3>
            ${this.#y(n)}
        `}#E(t){let{scales:e,axes:n,legends:a}=this.snapshot.resolutions,i=new Set(Object.values(t.scaleResolutionIds)),r=new Set(Object.values(t.axisResolutionIds)),s=new Set(Object.values(t.legendResolutionIds)),o=e.filter(h=>i.has(h.id)||h.members.some(m=>m.viewId===t.id)),d=n.filter(h=>r.has(h.id)||h.members.some(m=>m.viewId===t.id)),f=a.filter(h=>s.has(h.id)||h.members.some(m=>m.viewId===t.id));return o.length===0&&d.length===0&&f.length===0?c`<p class="empty">No related resolutions.</p>`:c`
            <h4>Scales</h4>
            ${this.#b(o)}
            <h4>Axes</h4>
            ${this.#v(d)}
            <h4>Legends</h4>
            ${this.#y(f)}
        `}#b(t){return t.length===0?c`<p class="empty">No scale resolutions.</p>`:c`
            <table>
                <thead>
                    <tr>
                        <th>id</th>
                        <th>channel</th>
                        <th>name</th>
                        <th>type</th>
                        <th>domain</th>
                        <th>owner</th>
                        <th>members</th>
                    </tr>
                </thead>
                <tbody>
                    ${t.map(e=>c`
                            <tr>
                                <td>${e.id}</td>
                                <td>${e.channel}</td>
                                <td>${e.name??"-"}</td>
                                <td>
                                    ${e.resolvedScaleType??e.type}
                                </td>
                                <td>
                                    ${L(e.complexDomain??e.domain)}
                                </td>
                                <td>
                                    ${this.#p(e.hostViewId,e.hostViewPath,"Jump to owner view")}
                                </td>
                                <td>
                                    ${this.#m(e.id,e.members)}
                                </td>
                            </tr>
                        `)}
                </tbody>
            </table>
        `}#v(t){return t.length===0?c`<p class="empty">No axis resolutions.</p>`:c`
            <table>
                <thead>
                    <tr>
                        <th>id</th>
                        <th>channel</th>
                        <th>title</th>
                        <th>scale</th>
                        <th>owner</th>
                        <th>members</th>
                    </tr>
                </thead>
                <tbody>
                    ${t.map(e=>c`
                            <tr>
                                <td>${e.id}</td>
                                <td>${e.channel}</td>
                                <td>${e.title??"-"}</td>
                                <td>${e.scaleResolutionId??"-"}</td>
                                <td>
                                    ${this.#p(e.hostViewId,e.hostViewPath,"Jump to owner view")}
                                </td>
                                <td>
                                    ${this.#m(e.id,e.members)}
                                </td>
                            </tr>
                        `)}
                </tbody>
            </table>
        `}#y(t){return t.length===0?c`<p class="empty">No legend resolutions.</p>`:c`
            <table>
                <thead>
                    <tr>
                        <th>id</th>
                        <th>channel</th>
                        <th>definitions</th>
                        <th>owner</th>
                        <th>members</th>
                    </tr>
                </thead>
                <tbody>
                    ${t.map(e=>c`
                            <tr>
                                <td>${e.id}</td>
                                <td>${e.channel}</td>
                                <td>${e.definitionCount}</td>
                                <td>
                                    ${this.#p(e.hostViewId,e.hostViewPath,"Jump to owner view")}
                                </td>
                                <td>
                                    ${this.#m(e.id,e.members)}
                                </td>
                            </tr>
                        `)}
                </tbody>
            </table>
        `}#m(t,e){if(e.length===0)return c`<span class="muted">none</span>`;let n=e.slice().sort((r,s)=>+!!r.chrome-+!!s.chrome),a=this.expandedResolutionMemberIds.has(t),i=a?n:n.slice(0,5);return c`
            <ul class="member-list">
                ${i.map(r=>r.viewId===this.selectedViewId?c`
                              <li>
                                  <span class="current-member">
                                      ${r.viewPath}:${r.channel}
                                  </span>
                                  ${r.chrome?c`<span class="badge"
                                                >chrome</span
                                            >`:g}
                              </li>
                          `:c`
                              <li>
                                  <button
                                      class="link-button"
                                      title="Jump to member view"
                                      @click=${()=>{this.#$(r)}}
                                      @mouseenter=${()=>this.session?.highlightView(r.viewId)}
                                      @mouseleave=${()=>this.session?.highlightView(void 0)}
                                  >
                                      ${r.viewPath}:${r.channel}
                                  </button>
                                  ${r.chrome?c`<span class="badge"
                                                >chrome</span
                                            >`:g}
                              </li>
                          `)}
            </ul>
            ${e.length>i.length?c`
                          <button
                              class="inline-action"
                              @click=${()=>this.#w(t,!0)}
                          >
                              Show all ${e.length}
                          </button>
                      `:g}
            ${a&&e.length>5?c`
                          <button
                              class="inline-action"
                              @click=${()=>this.#w(t,!1)}
                          >
                              Show fewer
                          </button>
                      `:g}
        `}#p(t,e,n){return!t||!e?c`<span class="muted">-</span>`:t===this.selectedViewId?c`<span class="current-member">${e}</span>`:c`
            <button
                class="link-button"
                title=${n}
                @click=${()=>{this.#$({viewId:t})}}
                @mouseenter=${()=>this.session?.highlightView(t)}
                @mouseleave=${()=>this.session?.highlightView(void 0)}
            >
                ${e}
            </button>
        `}async#$(t){!this.#k(t.viewId)&&this.session&&(await this.session.setIncludeChrome(!0),this.snapshot=this.session.snapshot),this.#k(t.viewId)&&(this.selectedViewId=t.viewId),this.activePanel="elements",this.session?.highlightView(void 0),await this.updateComplete,this.#d()}#w(t,e){let n=new Set(this.expandedResolutionMemberIds);e?n.add(t):n.delete(t),this.expandedResolutionMemberIds=n}#P(t){let e=this.#j(t.id);return!e||e.params.length===0?c`<p class="empty">No local params.</p>`:ze(e.params)}#_(t){let e=this.#z(t.id);return e?c`
            <dl>
                <dt>type</dt>
                <dd>${e.type}</dd>
                <dt>ready</dt>
                <dd>${String(e.ready)}</dd>
                <dt>picking</dt>
                <dd>${String(e.pickingParticipant)}</dd>
                <dt>data count</dt>
                <dd>${e.dataCount??"-"}</dd>
                <dt>vertices</dt>
                <dd>${e.vertexCount??"-"}</dd>
                <dt>allocated vertices</dt>
                <dd>${e.allocatedVertices??"-"}</dd>
                <dt>ranges</dt>
                <dd>${e.rangeCount}</dd>
                <dt>encoding channels</dt>
                <dd>${e.encodingChannels.join(", ")||"-"}</dd>
                <dt>encoder channels</dt>
                <dd>${e.encoderChannels.join(", ")||"-"}</dd>
                <dt>search fields</dt>
                <dd>${e.searchFields.join(", ")||"-"}</dd>
                <dt>uniforms dirty</dt>
                <dd>${String(e.markUniformsAltered)}</dd>
            </dl>

            <h3>Mark Props</h3>
            <pre>${L(e.properties)}</pre>
        `:c`<p class="empty">No mark for this view.</p>`}async#C(){this.session&&await this.session.refresh()}#g(){return this.snapshot.rootId?this.#x(this.snapshot.rootId):void 0}#N(){return this.selectedViewId?this.#x(this.selectedViewId)??this.#g():this.#g()}#O(t){let e=this.snapshot.nodes.find(n=>n.id===t);if(!e)throw Error("Unknown inspector node: "+t);return e}#x(t){return this.snapshot.nodes.find(e=>e.id===t)}#k(t){return this.snapshot.nodes.some(e=>e.id===t)}#M(t){return this.snapshot.dataflow.nodes.filter(e=>e.viewId===t)}#R(t){this.selectedFlowNodeId=t,this.activePanel="dataflow"}#j(t){return this.snapshot.params.scopes.find(e=>e.viewId===t)}#z(t){return this.snapshot.marks.marks.find(e=>e.viewId===t)}};customElements.define("gs-inspector-panel",De)});var Fe=Object.defineProperty,Aa=(t,e)=>{let n={};for(var a in t)Fe(n,a,{get:t[a],enumerable:!0});return e||Fe(n,Symbol.toStringTag,{value:"Module"}),n},hn={prefix:"fas",iconName:"bug",icon:[512,512,[],"f188","M256 0c53 0 96 43 96 96l0 3.6c0 15.7-12.7 28.4-28.4 28.4l-135.1 0c-15.7 0-28.4-12.7-28.4-28.4l0-3.6c0-53 43-96 96-96zM41.4 105.4c12.5-12.5 32.8-12.5 45.3 0l64 64c.7 .7 1.3 1.4 1.9 2.1c14.2-7.3 30.4-11.4 47.5-11.4l112 0c17.1 0 33.2 4.1 47.5 11.4c.6-.7 1.2-1.4 1.9-2.1l64-64c12.5-12.5 32.8-12.5 45.3 0s12.5 32.8 0 45.3l-64 64c-.7 .7-1.4 1.3-2.1 1.9c6.2 12 10.1 25.3 11.1 39.5l64.3 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c0 24.6-5.5 47.8-15.4 68.6c2.2 1.3 4.2 2.9 6 4.8l64 64c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0l-63.1-63.1c-24.5 21.8-55.8 36.2-90.3 39.6L272 240c0-8.8-7.2-16-16-16s-16 7.2-16 16l0 239.2c-34.5-3.4-65.8-17.8-90.3-39.6L86.6 502.6c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l64-64c1.9-1.9 3.9-3.4 6-4.8C101.5 367.8 96 344.6 96 320l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32l64.3 0c1.1-14.1 5-27.5 11.1-39.5c-.7-.6-1.4-1.2-2.1-1.9l-64-64c-12.5-12.5-12.5-32.8 0-45.3z"]},Sa=Aa({default:()=>mn}),mn=class extends EventTarget{#t;#e=!1;#n=new WeakMap;#a=new Map;#s={};#i=new WeakSet;#d;#f;#r=[];#c=!1;snapshot={rootId:void 0,nodes:[],resolutions:{scales:[],axes:[],legends:[]},dataflow:{sourceIds:[],nodes:[],collectorCount:0},params:{scopes:[]},marks:{marks:[]}};constructor(t){super(),this.#t=t}get includeChrome(){return this.#e}async setIncludeChrome(t){this.#e!==t&&(this.#e=t,await this.refresh())}async refresh(){if(this.#c)return;let t=this.#l(),e=await this.#u();if(this.#c)return;this.#f=e,this.#a=new Map,this.#i=Ia(t);let n=e.createViewDebugSnapshot(t,{includeChrome:this.#e,getDebugId:a=>this.#o(a)});this.snapshot={...n,resolutions:e.createResolutionDebugSnapshot(t,{getDebugId:a=>this.#o(a)}),dataflow:e.createDataflowDebugSnapshot(t?.context.dataFlow,{getDebugId:a=>this.#o(a),rootView:t}),params:e.createParamDebugSnapshot(t,{getDebugId:a=>this.#o(a)}),marks:e.createMarkDebugSnapshot(t,{getDebugId:a=>this.#o(a)})},this.#h(),this.dispatchEvent(new Event("snapshot"))}highlightView(t){let e=t?this.#a.get(t):null,n=this.#l();n&&n.context.highlightView(e??null)}dispose(){this.#c=!0;for(let t of this.#r.splice(0))t();this.highlightView(void 0)}#u(){return this.#d??=this.#t.getModules(),this.#d}#h(){if(this.#r.length>0)return;let t=this.#l();if(!t)return;let e=()=>{this.refresh()};for(let n of["layoutComputed","subtreeDataReady","dataFlowBuilt"])t.context.addBroadcastListener(n,e),this.#r.push(()=>t.context.removeBroadcastListener(n,e))}#l(){return this.#t.getViewRoot()}#o(t){if(this.#i.has(t)){let r=this.#l(),s=this.#f;if(!s)throw Error("Inspector debug modules have not been loaded.");let o=s.getViewIdentityRegistry(r).getId(t);return this.#a.set(o,t),o}let e=this.#n.get(t);if(e)return this.#a.set(e,t),e;let n=Ea(t),a=(this.#s[n]??0)+1;this.#s[n]=a;let i=n+String(a);return this.#n.set(t,i),this.#a.set(i,t),i}};function Ia(t){let e=new WeakSet;return t?.visit?.(n=>{e.add(n)}),e}function Ea(t){return"channel"in t?"r":"o"}function Pa(t={}){return{name:"@genome-spy/inspector",async install(e){if(!e.ui?.registerToolbarMenuItem)throw Error("inspector requires an App UI host.");let n,a,i,r=async()=>{if(a)return a;if(!e.ui.registerSidePanel)throw Error("inspector requires side panel support.");let[{GsInspectorPanel:d}]=await Promise.all([Promise.resolve().then(()=>(Lt(),Ft))]);return n=new mn(e.debug),i=new d,i.session=n,i.addEventListener("close",()=>{a?.hide()}),a=e.ui.registerSidePanel({id:"genome-spy-inspector",element:i,preferredWidth:t.preferredWidth??"min(46vw, 760px)"}),a},s=async(d={})=>{let f=await r();d.panel&&i&&(i.activePanel=d.panel),f.show(),await n.refresh()},o=e.ui.registerToolbarMenuItem({label:"Inspector",icon:hn,callback:()=>{s().catch(()=>{})}});return()=>{o(),n?.dispose(),n=void 0,a?.dispose(),a=void 0,i?.remove(),i=void 0}}}}var Dr=Pa;async function _a(t,e={}){e.signal?.throwIfAborted();let[{default:n},{GsInspectorPanel:a}]=await Promise.all([Promise.resolve().then(()=>Sa),Promise.resolve().then(()=>(Lt(),Ft))]);e.signal?.throwIfAborted();let i=new n(t),r=new a;r.session=i,e.activePanel&&(r.activePanel=e.activePanel);let s=()=>{e.signal?.removeEventListener("abort",s),i.dispose(),r.remove()};e.signal?.addEventListener("abort",s,{once:!0});try{await i.refresh(),e.signal?.throwIfAborted()}catch(o){throw s(),o}return{panel:r,session:i,dispose:s}}async function Ca(t,e={}){let n=e.container??document.body;e.signal?.throwIfAborted();let a=n.ownerDocument.createElement("section");a.setAttribute("role","dialog"),a.setAttribute("aria-label","GenomeSpy Inspector"),a.tabIndex=-1,a.className="gs-inspector-overlay",Object.assign(a.style,{position:"fixed",top:"0",right:"0",bottom:"0",zIndex:"2147483647",width:e.width??"min(46vw, 760px)",minWidth:"320px",maxWidth:"100vw",boxShadow:"0 0 18px rgba(0, 0, 0, 0.35)",resize:"horizontal",overflow:"hidden"});let i=await _a(t,{activePanel:e.activePanel,signal:e.signal});Object.assign(i.panel.style,{display:"block",height:"100%",minHeight:"0"});let r=!1,s=()=>{r||(r=!0,e.signal?.removeEventListener("abort",s),i.panel.removeEventListener("close",s),i.dispose(),a.remove())};try{e.signal?.throwIfAborted(),e.signal?.addEventListener("abort",s,{once:!0}),i.panel.addEventListener("close",s,{once:!0}),a.append(i.panel),n.append(a)}catch(o){throw s(),o}return{element:a,panel:i.panel,session:i.session,dispose:s}}function Na(t){if(!t.label.trim())throw Error("A button requires a non-empty accessible label.");return{mount(e){let n=e.container.ownerDocument,a=n.createElement("button");if(a.type="button",t.icon){let r=n.createElement("span");r.className="icon",r.setAttribute("aria-hidden","true"),r.inert=!0,r.append(n.importNode(t.icon,!0)),a.append(r)}else a.textContent=t.label;a.title=t.title??t.label,a.setAttribute("aria-label",t.label);async function i(){a.disabled=!0,e.showStatus("");try{await t.onClick(e)}catch(r){e.reportError(r)}finally{a.disabled=!1}}return a.addEventListener("click",i,{signal:e.signal}),{element:a,dispose(){a.removeEventListener("click",i)}}}}}function Oa(t,e,n){return(e=Ra(e))in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}function Le(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(t);e&&(a=a.filter(function(i){return Object.getOwnPropertyDescriptor(t,i).enumerable})),n.push.apply(n,a)}return n}function l(t){for(var e=1;e<arguments.length;e++){var n=arguments[e]==null?{}:arguments[e];e%2?Le(Object(n),!0).forEach(function(a){Oa(t,a,n[a])}):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):Le(Object(n)).forEach(function(a){Object.defineProperty(t,a,Object.getOwnPropertyDescriptor(n,a))})}return t}function Ma(t,e){if(typeof t!="object"||!t)return t;var n=t[Symbol.toPrimitive];if(n!==void 0){var a=n.call(t,e||"default");if(typeof a!="object")return a;throw TypeError("@@toPrimitive must return a primitive value.")}return(e==="string"?String:Number)(t)}function Ra(t){var e=Ma(t,"string");return typeof e=="symbol"?e:e+""}var Te=()=>{},se={},pn={},gn=null,bn={mark:Te,measure:Te};try{typeof window<"u"&&(se=window),typeof document<"u"&&(pn=document),typeof MutationObserver<"u"&&(gn=MutationObserver),typeof performance<"u"&&(bn=performance)}catch{}var{userAgent:Ue=""}=se.navigator||{},O=se,b=pn,Ve=gn,pt=bn;O.document;var P=!!b.documentElement&&!!b.head&&typeof b.addEventListener=="function"&&typeof b.createElement=="function",vn=~Ue.indexOf("MSIE")||~Ue.indexOf("Trident/"),ja=/fa(s|r|l|t|d|dr|dl|dt|b|k|kd|ss|sr|sl|st|sds|sdr|sdl|sdt)?[\-\ ]/,za=/Font ?Awesome ?([56 ]*)(Solid|Regular|Light|Thin|Duotone|Brands|Free|Pro|Sharp Duotone|Sharp|Kit)?.*/i,yn={classic:{fa:"solid",fas:"solid","fa-solid":"solid",far:"regular","fa-regular":"regular",fal:"light","fa-light":"light",fat:"thin","fa-thin":"thin",fab:"brands","fa-brands":"brands"},duotone:{fa:"solid",fad:"solid","fa-solid":"solid","fa-duotone":"solid",fadr:"regular","fa-regular":"regular",fadl:"light","fa-light":"light",fadt:"thin","fa-thin":"thin"},sharp:{fa:"solid",fass:"solid","fa-solid":"solid",fasr:"regular","fa-regular":"regular",fasl:"light","fa-light":"light",fast:"thin","fa-thin":"thin"},"sharp-duotone":{fa:"solid",fasds:"solid","fa-solid":"solid",fasdr:"regular","fa-regular":"regular",fasdl:"light","fa-light":"light",fasdt:"thin","fa-thin":"thin"}},Da={GROUP:"duotone-group",SWAP_OPACITY:"swap-opacity",PRIMARY:"primary",SECONDARY:"secondary"},$n=["fa-classic","fa-duotone","fa-sharp","fa-sharp-duotone"],$="classic",wt="duotone",wn=[$,wt,"sharp","sharp-duotone"],Fa={classic:{900:"fas",400:"far",normal:"far",300:"fal",100:"fat"},duotone:{900:"fad",400:"fadr",300:"fadl",100:"fadt"},sharp:{900:"fass",400:"fasr",300:"fasl",100:"fast"},"sharp-duotone":{900:"fasds",400:"fasdr",300:"fasdl",100:"fasdt"}},La={"Font Awesome 6 Free":{900:"fas",400:"far"},"Font Awesome 6 Pro":{900:"fas",400:"far",normal:"far",300:"fal",100:"fat"},"Font Awesome 6 Brands":{400:"fab",normal:"fab"},"Font Awesome 6 Duotone":{900:"fad",400:"fadr",normal:"fadr",300:"fadl",100:"fadt"},"Font Awesome 6 Sharp":{900:"fass",400:"fasr",normal:"fasr",300:"fasl",100:"fast"},"Font Awesome 6 Sharp Duotone":{900:"fasds",400:"fasdr",normal:"fasdr",300:"fasdl",100:"fasdt"}},Ta=new Map([["classic",{defaultShortPrefixId:"fas",defaultStyleId:"solid",styleIds:["solid","regular","light","thin","brands"],futureStyleIds:[],defaultFontWeight:900}],["sharp",{defaultShortPrefixId:"fass",defaultStyleId:"solid",styleIds:["solid","regular","light","thin"],futureStyleIds:[],defaultFontWeight:900}],["duotone",{defaultShortPrefixId:"fad",defaultStyleId:"solid",styleIds:["solid","regular","light","thin"],futureStyleIds:[],defaultFontWeight:900}],["sharp-duotone",{defaultShortPrefixId:"fasds",defaultStyleId:"solid",styleIds:["solid","regular","light","thin"],futureStyleIds:[],defaultFontWeight:900}]]),Ua={classic:{solid:"fas",regular:"far",light:"fal",thin:"fat",brands:"fab"},duotone:{solid:"fad",regular:"fadr",light:"fadl",thin:"fadt"},sharp:{solid:"fass",regular:"fasr",light:"fasl",thin:"fast"},"sharp-duotone":{solid:"fasds",regular:"fasdr",light:"fasdl",thin:"fasdt"}},Va=["fak","fa-kit","fakd","fa-kit-duotone"],He={kit:{fak:"kit","fa-kit":"kit"},"kit-duotone":{fakd:"kit-duotone","fa-kit-duotone":"kit-duotone"}},Ha=["kit"],Wa={kit:{"fa-kit":"fak"},"kit-duotone":{"fa-kit-duotone":"fakd"}},Ya=["fak","fakd"],Ba={kit:{fak:"fa-kit"},"kit-duotone":{fakd:"fa-kit-duotone"}},We={kit:{kit:"fak"},"kit-duotone":{"kit-duotone":"fakd"}},gt={GROUP:"duotone-group",SWAP_OPACITY:"swap-opacity",PRIMARY:"primary",SECONDARY:"secondary"},qa=["fa-classic","fa-duotone","fa-sharp","fa-sharp-duotone"],Ga=["fak","fa-kit","fakd","fa-kit-duotone"],Ja={"Font Awesome Kit":{400:"fak",normal:"fak"},"Font Awesome Kit Duotone":{400:"fakd",normal:"fakd"}},Xa={classic:{"fa-brands":"fab","fa-duotone":"fad","fa-light":"fal","fa-regular":"far","fa-solid":"fas","fa-thin":"fat"},duotone:{"fa-regular":"fadr","fa-light":"fadl","fa-thin":"fadt"},sharp:{"fa-solid":"fass","fa-regular":"fasr","fa-light":"fasl","fa-thin":"fast"},"sharp-duotone":{"fa-solid":"fasds","fa-regular":"fasdr","fa-light":"fasdl","fa-thin":"fasdt"}},Ka={classic:["fas","far","fal","fat","fad"],duotone:["fadr","fadl","fadt"],sharp:["fass","fasr","fasl","fast"],"sharp-duotone":["fasds","fasdr","fasdl","fasdt"]},Bt={classic:{fab:"fa-brands",fad:"fa-duotone",fal:"fa-light",far:"fa-regular",fas:"fa-solid",fat:"fa-thin"},duotone:{fadr:"fa-regular",fadl:"fa-light",fadt:"fa-thin"},sharp:{fass:"fa-solid",fasr:"fa-regular",fasl:"fa-light",fast:"fa-thin"},"sharp-duotone":{fasds:"fa-solid",fasdr:"fa-regular",fasdl:"fa-light",fasdt:"fa-thin"}},Za=["fa-solid","fa-regular","fa-light","fa-thin","fa-duotone","fa-brands"],qt=["fa","fas","far","fal","fat","fad","fadr","fadl","fadt","fab","fass","fasr","fasl","fast","fasds","fasdr","fasdl","fasdt",...qa,...Za],Qa=["solid","regular","light","thin","duotone","brands"],xn=[1,2,3,4,5,6,7,8,9,10],ti=xn.concat([11,12,13,14,15,16,17,18,19,20]),ei=[...Object.keys(Ka),...Qa,"2xs","xs","sm","lg","xl","2xl","beat","border","fade","beat-fade","bounce","flip-both","flip-horizontal","flip-vertical","flip","fw","inverse","layers-counter","layers-text","layers","li","pull-left","pull-right","pulse","rotate-180","rotate-270","rotate-90","rotate-by","shake","spin-pulse","spin-reverse","spin","stack-1x","stack-2x","stack","ul",gt.GROUP,gt.SWAP_OPACITY,gt.PRIMARY,gt.SECONDARY].concat(xn.map(t=>`${t}x`),ti.map(t=>`w-${t}`)),ni={"Font Awesome 5 Free":{900:"fas",400:"far"},"Font Awesome 5 Pro":{900:"fas",400:"far",normal:"far",300:"fal"},"Font Awesome 5 Brands":{400:"fab",normal:"fab"},"Font Awesome 5 Duotone":{900:"fad"}},I="___FONT_AWESOME___",Gt=16,kn="fa",An="svg-inline--fa",H="data-fa-i2svg",Jt="data-fa-pseudo-element",ai="data-fa-pseudo-element-pending",oe="data-prefix",le="data-icon",Ye="fontawesome-i2svg",ii="async",ri=["HTML","HEAD","STYLE","SCRIPT"],Sn=(()=>{try{return!0}catch{return!1}})();function dt(t){return new Proxy(t,{get(e,n){return n in e?e[n]:e[$]}})}var In=l({},yn);In[$]=l(l(l(l({},{"fa-duotone":"duotone"}),yn[$]),He.kit),He["kit-duotone"]);var si=dt(In),Xt=l({},Ua);Xt[$]=l(l(l(l({},{duotone:"fad"}),Xt[$]),We.kit),We["kit-duotone"]);var Be=dt(Xt),Kt=l({},Bt);Kt[$]=l(l({},Kt[$]),Ba.kit);var de=dt(Kt),Tt=l({},Xa);Tt[$]=l(l({},Tt[$]),Wa.kit),dt(Tt);var oi=ja,En="fa-layers-text",li=za;dt(l({},Fa));var di=["class","data-prefix","data-icon","data-fa-transform","data-fa-mask"],Ut=Da,ci=[...Ha,...ei],rt=O.FontAwesomeConfig||{};function fi(t){var e=b.querySelector("script["+t+"]");if(e)return e.getAttribute(t)}function ui(t){return t===""?!0:t==="false"?!1:t==="true"||t}b&&typeof b.querySelector=="function"&&[["data-family-prefix","familyPrefix"],["data-css-prefix","cssPrefix"],["data-family-default","familyDefault"],["data-style-default","styleDefault"],["data-replacement-class","replacementClass"],["data-auto-replace-svg","autoReplaceSvg"],["data-auto-add-css","autoAddCss"],["data-auto-a11y","autoA11y"],["data-search-pseudo-elements","searchPseudoElements"],["data-observe-mutations","observeMutations"],["data-mutate-approach","mutateApproach"],["data-keep-original-source","keepOriginalSource"],["data-measure-performance","measurePerformance"],["data-show-missing-icons","showMissingIcons"]].forEach(t=>{let[e,n]=t,a=ui(fi(e));a!=null&&(rt[n]=a)});var Pn={styleDefault:"solid",familyDefault:$,cssPrefix:kn,replacementClass:An,autoReplaceSvg:!0,autoAddCss:!0,autoA11y:!0,searchPseudoElements:!1,observeMutations:!0,mutateApproach:"async",keepOriginalSource:!0,measurePerformance:!1,showMissingIcons:!0};rt.familyPrefix&&(rt.cssPrefix=rt.familyPrefix);var J=l(l({},Pn),rt);J.autoReplaceSvg||(J.observeMutations=!1);var u={};Object.keys(Pn).forEach(t=>{Object.defineProperty(u,t,{enumerable:!0,set:function(e){J[t]=e,st.forEach(n=>n(u))},get:function(){return J[t]}})}),Object.defineProperty(u,"familyPrefix",{enumerable:!0,set:function(t){J.cssPrefix=t,st.forEach(e=>e(u))},get:function(){return J.cssPrefix}}),O.FontAwesomeConfig=u;var st=[];function hi(t){return st.push(t),()=>{st.splice(st.indexOf(t),1)}}var N=Gt,A={size:16,x:0,y:0,rotate:0,flipX:!1,flipY:!1};function mi(t){if(!t||!P)return;let e=b.createElement("style");e.setAttribute("type","text/css"),e.innerHTML=t;let n=b.head.childNodes,a=null;for(let i=n.length-1;i>-1;i--){let r=n[i],s=(r.tagName||"").toUpperCase();["STYLE","LINK"].indexOf(s)>-1&&(a=r)}return b.head.insertBefore(e,a),t}var pi="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";function ot(){let t=12,e="";for(;t-- >0;)e+=pi[Math.random()*62|0];return e}function Z(t){let e=[];for(let n=(t||[]).length>>>0;n--;)e[n]=t[n];return e}function ce(t){return t.classList?Z(t.classList):(t.getAttribute("class")||"").split(" ").filter(e=>e)}function _n(t){return`${t}`.replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/'/g,"&#39;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}function gi(t){return Object.keys(t||{}).reduce((e,n)=>e+`${n}="${_n(t[n])}" `,"").trim()}function xt(t){return Object.keys(t||{}).reduce((e,n)=>e+`${n}: ${t[n].trim()};`,"")}function fe(t){return t.size!==A.size||t.x!==A.x||t.y!==A.y||t.rotate!==A.rotate||t.flipX||t.flipY}function bi(t){let{transform:e,containerWidth:n,iconWidth:a}=t;return{outer:{transform:`translate(${n/2} 256)`},inner:{transform:`${`translate(${e.x*32}, ${e.y*32}) `} ${`scale(${e.size/16*(e.flipX?-1:1)}, ${e.size/16*(e.flipY?-1:1)}) `} ${`rotate(${e.rotate} 0 0)`}`},path:{transform:`translate(${a/2*-1} -256)`}}}function vi(t){let{transform:e,width:n=Gt,height:a=Gt,startCentered:i=!1}=t,r="";return i&&vn?r+=`translate(${e.x/N-n/2}em, ${e.y/N-a/2}em) `:i?r+=`translate(calc(-50% + ${e.x/N}em), calc(-50% + ${e.y/N}em)) `:r+=`translate(${e.x/N}em, ${e.y/N}em) `,r+=`scale(${e.size/N*(e.flipX?-1:1)}, ${e.size/N*(e.flipY?-1:1)}) `,r+=`rotate(${e.rotate}deg) `,r}var yi=`:root, :host {
  --fa-font-solid: normal 900 1em/1 "Font Awesome 6 Free";
  --fa-font-regular: normal 400 1em/1 "Font Awesome 6 Free";
  --fa-font-light: normal 300 1em/1 "Font Awesome 6 Pro";
  --fa-font-thin: normal 100 1em/1 "Font Awesome 6 Pro";
  --fa-font-duotone: normal 900 1em/1 "Font Awesome 6 Duotone";
  --fa-font-duotone-regular: normal 400 1em/1 "Font Awesome 6 Duotone";
  --fa-font-duotone-light: normal 300 1em/1 "Font Awesome 6 Duotone";
  --fa-font-duotone-thin: normal 100 1em/1 "Font Awesome 6 Duotone";
  --fa-font-brands: normal 400 1em/1 "Font Awesome 6 Brands";
  --fa-font-sharp-solid: normal 900 1em/1 "Font Awesome 6 Sharp";
  --fa-font-sharp-regular: normal 400 1em/1 "Font Awesome 6 Sharp";
  --fa-font-sharp-light: normal 300 1em/1 "Font Awesome 6 Sharp";
  --fa-font-sharp-thin: normal 100 1em/1 "Font Awesome 6 Sharp";
  --fa-font-sharp-duotone-solid: normal 900 1em/1 "Font Awesome 6 Sharp Duotone";
  --fa-font-sharp-duotone-regular: normal 400 1em/1 "Font Awesome 6 Sharp Duotone";
  --fa-font-sharp-duotone-light: normal 300 1em/1 "Font Awesome 6 Sharp Duotone";
  --fa-font-sharp-duotone-thin: normal 100 1em/1 "Font Awesome 6 Sharp Duotone";
}

svg:not(:root).svg-inline--fa, svg:not(:host).svg-inline--fa {
  overflow: visible;
  box-sizing: content-box;
}

.svg-inline--fa {
  display: var(--fa-display, inline-block);
  height: 1em;
  overflow: visible;
  vertical-align: -0.125em;
}
.svg-inline--fa.fa-2xs {
  vertical-align: 0.1em;
}
.svg-inline--fa.fa-xs {
  vertical-align: 0em;
}
.svg-inline--fa.fa-sm {
  vertical-align: -0.0714285705em;
}
.svg-inline--fa.fa-lg {
  vertical-align: -0.2em;
}
.svg-inline--fa.fa-xl {
  vertical-align: -0.25em;
}
.svg-inline--fa.fa-2xl {
  vertical-align: -0.3125em;
}
.svg-inline--fa.fa-pull-left {
  margin-right: var(--fa-pull-margin, 0.3em);
  width: auto;
}
.svg-inline--fa.fa-pull-right {
  margin-left: var(--fa-pull-margin, 0.3em);
  width: auto;
}
.svg-inline--fa.fa-li {
  width: var(--fa-li-width, 2em);
  top: 0.25em;
}
.svg-inline--fa.fa-fw {
  width: var(--fa-fw-width, 1.25em);
}

.fa-layers svg.svg-inline--fa {
  bottom: 0;
  left: 0;
  margin: auto;
  position: absolute;
  right: 0;
  top: 0;
}

.fa-layers-counter, .fa-layers-text {
  display: inline-block;
  position: absolute;
  text-align: center;
}

.fa-layers {
  display: inline-block;
  height: 1em;
  position: relative;
  text-align: center;
  vertical-align: -0.125em;
  width: 1em;
}
.fa-layers svg.svg-inline--fa {
  transform-origin: center center;
}

.fa-layers-text {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  transform-origin: center center;
}

.fa-layers-counter {
  background-color: var(--fa-counter-background-color, #ff253a);
  border-radius: var(--fa-counter-border-radius, 1em);
  box-sizing: border-box;
  color: var(--fa-inverse, #fff);
  line-height: var(--fa-counter-line-height, 1);
  max-width: var(--fa-counter-max-width, 5em);
  min-width: var(--fa-counter-min-width, 1.5em);
  overflow: hidden;
  padding: var(--fa-counter-padding, 0.25em 0.5em);
  right: var(--fa-right, 0);
  text-overflow: ellipsis;
  top: var(--fa-top, 0);
  transform: scale(var(--fa-counter-scale, 0.25));
  transform-origin: top right;
}

.fa-layers-bottom-right {
  bottom: var(--fa-bottom, 0);
  right: var(--fa-right, 0);
  top: auto;
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: bottom right;
}

.fa-layers-bottom-left {
  bottom: var(--fa-bottom, 0);
  left: var(--fa-left, 0);
  right: auto;
  top: auto;
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: bottom left;
}

.fa-layers-top-right {
  top: var(--fa-top, 0);
  right: var(--fa-right, 0);
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: top right;
}

.fa-layers-top-left {
  left: var(--fa-left, 0);
  right: auto;
  top: var(--fa-top, 0);
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: top left;
}

.fa-1x {
  font-size: 1em;
}

.fa-2x {
  font-size: 2em;
}

.fa-3x {
  font-size: 3em;
}

.fa-4x {
  font-size: 4em;
}

.fa-5x {
  font-size: 5em;
}

.fa-6x {
  font-size: 6em;
}

.fa-7x {
  font-size: 7em;
}

.fa-8x {
  font-size: 8em;
}

.fa-9x {
  font-size: 9em;
}

.fa-10x {
  font-size: 10em;
}

.fa-2xs {
  font-size: 0.625em;
  line-height: 0.1em;
  vertical-align: 0.225em;
}

.fa-xs {
  font-size: 0.75em;
  line-height: 0.0833333337em;
  vertical-align: 0.125em;
}

.fa-sm {
  font-size: 0.875em;
  line-height: 0.0714285718em;
  vertical-align: 0.0535714295em;
}

.fa-lg {
  font-size: 1.25em;
  line-height: 0.05em;
  vertical-align: -0.075em;
}

.fa-xl {
  font-size: 1.5em;
  line-height: 0.0416666682em;
  vertical-align: -0.125em;
}

.fa-2xl {
  font-size: 2em;
  line-height: 0.03125em;
  vertical-align: -0.1875em;
}

.fa-fw {
  text-align: center;
  width: 1.25em;
}

.fa-ul {
  list-style-type: none;
  margin-left: var(--fa-li-margin, 2.5em);
  padding-left: 0;
}
.fa-ul > li {
  position: relative;
}

.fa-li {
  left: calc(-1 * var(--fa-li-width, 2em));
  position: absolute;
  text-align: center;
  width: var(--fa-li-width, 2em);
  line-height: inherit;
}

.fa-border {
  border-color: var(--fa-border-color, #eee);
  border-radius: var(--fa-border-radius, 0.1em);
  border-style: var(--fa-border-style, solid);
  border-width: var(--fa-border-width, 0.08em);
  padding: var(--fa-border-padding, 0.2em 0.25em 0.15em);
}

.fa-pull-left {
  float: left;
  margin-right: var(--fa-pull-margin, 0.3em);
}

.fa-pull-right {
  float: right;
  margin-left: var(--fa-pull-margin, 0.3em);
}

.fa-beat {
  animation-name: fa-beat;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-bounce {
  animation-name: fa-bounce;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.28, 0.84, 0.42, 1));
}

.fa-fade {
  animation-name: fa-fade;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-beat-fade {
  animation-name: fa-beat-fade;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-flip {
  animation-name: fa-flip;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-shake {
  animation-name: fa-shake;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin {
  animation-name: fa-spin;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 2s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin-reverse {
  --fa-animation-direction: reverse;
}

.fa-pulse,
.fa-spin-pulse {
  animation-name: fa-spin;
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, steps(8));
}

@media (prefers-reduced-motion: reduce) {
  .fa-beat,
.fa-bounce,
.fa-fade,
.fa-beat-fade,
.fa-flip,
.fa-pulse,
.fa-shake,
.fa-spin,
.fa-spin-pulse {
    animation-delay: -1ms;
    animation-duration: 1ms;
    animation-iteration-count: 1;
    transition-delay: 0s;
    transition-duration: 0s;
  }
}
@keyframes fa-beat {
  0%, 90% {
    transform: scale(1);
  }
  45% {
    transform: scale(var(--fa-beat-scale, 1.25));
  }
}
@keyframes fa-bounce {
  0% {
    transform: scale(1, 1) translateY(0);
  }
  10% {
    transform: scale(var(--fa-bounce-start-scale-x, 1.1), var(--fa-bounce-start-scale-y, 0.9)) translateY(0);
  }
  30% {
    transform: scale(var(--fa-bounce-jump-scale-x, 0.9), var(--fa-bounce-jump-scale-y, 1.1)) translateY(var(--fa-bounce-height, -0.5em));
  }
  50% {
    transform: scale(var(--fa-bounce-land-scale-x, 1.05), var(--fa-bounce-land-scale-y, 0.95)) translateY(0);
  }
  57% {
    transform: scale(1, 1) translateY(var(--fa-bounce-rebound, -0.125em));
  }
  64% {
    transform: scale(1, 1) translateY(0);
  }
  100% {
    transform: scale(1, 1) translateY(0);
  }
}
@keyframes fa-fade {
  50% {
    opacity: var(--fa-fade-opacity, 0.4);
  }
}
@keyframes fa-beat-fade {
  0%, 100% {
    opacity: var(--fa-beat-fade-opacity, 0.4);
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(var(--fa-beat-fade-scale, 1.125));
  }
}
@keyframes fa-flip {
  50% {
    transform: rotate3d(var(--fa-flip-x, 0), var(--fa-flip-y, 1), var(--fa-flip-z, 0), var(--fa-flip-angle, -180deg));
  }
}
@keyframes fa-shake {
  0% {
    transform: rotate(-15deg);
  }
  4% {
    transform: rotate(15deg);
  }
  8%, 24% {
    transform: rotate(-18deg);
  }
  12%, 28% {
    transform: rotate(18deg);
  }
  16% {
    transform: rotate(-22deg);
  }
  20% {
    transform: rotate(22deg);
  }
  32% {
    transform: rotate(-12deg);
  }
  36% {
    transform: rotate(12deg);
  }
  40%, 100% {
    transform: rotate(0deg);
  }
}
@keyframes fa-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.fa-rotate-90 {
  transform: rotate(90deg);
}

.fa-rotate-180 {
  transform: rotate(180deg);
}

.fa-rotate-270 {
  transform: rotate(270deg);
}

.fa-flip-horizontal {
  transform: scale(-1, 1);
}

.fa-flip-vertical {
  transform: scale(1, -1);
}

.fa-flip-both,
.fa-flip-horizontal.fa-flip-vertical {
  transform: scale(-1, -1);
}

.fa-rotate-by {
  transform: rotate(var(--fa-rotate-angle, 0));
}

.fa-stack {
  display: inline-block;
  vertical-align: middle;
  height: 2em;
  position: relative;
  width: 2.5em;
}

.fa-stack-1x,
.fa-stack-2x {
  bottom: 0;
  left: 0;
  margin: auto;
  position: absolute;
  right: 0;
  top: 0;
  z-index: var(--fa-stack-z-index, auto);
}

.svg-inline--fa.fa-stack-1x {
  height: 1em;
  width: 1.25em;
}
.svg-inline--fa.fa-stack-2x {
  height: 2em;
  width: 2.5em;
}

.fa-inverse {
  color: var(--fa-inverse, #fff);
}

.sr-only,
.fa-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.sr-only-focusable:not(:focus),
.fa-sr-only-focusable:not(:focus) {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.svg-inline--fa .fa-primary {
  fill: var(--fa-primary-color, currentColor);
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa .fa-secondary {
  fill: var(--fa-secondary-color, currentColor);
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-primary {
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-secondary {
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa mask .fa-primary,
.svg-inline--fa mask .fa-secondary {
  fill: black;
}`;function Cn(){let t=kn,e=An,n=u.cssPrefix,a=u.replacementClass,i=yi;if(n!==t||a!==e){let r=RegExp(`\\.${t}\\-`,"g"),s=RegExp(`\\--${t}\\-`,"g"),o=RegExp(`\\.${e}`,"g");i=i.replace(r,`.${n}-`).replace(s,`--${n}-`).replace(o,`.${a}`)}return i}var qe=!1;function Vt(){u.autoAddCss&&!qe&&(mi(Cn()),qe=!0)}var $i={mixout(){return{dom:{css:Cn,insertCss:Vt}}},hooks(){return{beforeDOMElementCreation(){Vt()},beforeI2svg(){Vt()}}}},E=O||{};E[I]||(E[I]={}),E[I].styles||(E[I].styles={}),E[I].hooks||(E[I].hooks={}),E[I].shims||(E[I].shims=[]);var S=E[I],Nn=[],On=function(){b.removeEventListener("DOMContentLoaded",On),yt=1,Nn.map(t=>t())},yt=!1;P&&(yt=(b.documentElement.doScroll?/^loaded|^c/:/^loaded|^i|^c/).test(b.readyState),yt||b.addEventListener("DOMContentLoaded",On));function wi(t){P&&(yt?setTimeout(t,0):Nn.push(t))}function ct(t){let{tag:e,attributes:n={},children:a=[]}=t;return typeof t=="string"?_n(t):`<${e} ${gi(n)}>${a.map(ct).join("")}</${e}>`}function Ge(t,e,n){if(t&&t[e]&&t[e][n])return{prefix:e,iconName:n,icon:t[e][n]}}var xi=function(t,e){return function(n,a,i,r){return t.call(e,n,a,i,r)}},Ht=function(t,e,n,a){var i=Object.keys(t),r=i.length,s=a===void 0?e:xi(e,a),o,d,f;for(n===void 0?(o=1,f=t[i[0]]):(o=0,f=n);o<r;o++)d=i[o],f=s(f,t[d],d,t);return f};function ki(t){let e=[],n=0,a=t.length;for(;n<a;){let i=t.charCodeAt(n++);if(i>=55296&&i<=56319&&n<a){let r=t.charCodeAt(n++);(r&64512)==56320?e.push(((i&1023)<<10)+(r&1023)+65536):(e.push(i),n--)}else e.push(i)}return e}function Mn(t){let e=ki(t);return e.length===1?e[0].toString(16):null}function Ai(t,e){let n=t.length,a=t.charCodeAt(e),i;return a>=55296&&a<=56319&&n>e+1&&(i=t.charCodeAt(e+1),i>=56320&&i<=57343)?(a-55296)*1024+i-56320+65536:a}function Je(t){return Object.keys(t).reduce((e,n)=>{let a=t[n];return a.icon?e[a.iconName]=a.icon:e[n]=a,e},{})}function Zt(t,e){let{skipHooks:n=!1}=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{},a=Je(e);typeof S.hooks.addPack=="function"&&!n?S.hooks.addPack(t,Je(e)):S.styles[t]=l(l({},S.styles[t]||{}),a),t==="fas"&&Zt("fa",e)}var{styles:lt,shims:Si}=S,Rn=Object.keys(de),Ii=Rn.reduce((t,e)=>(t[e]=Object.keys(de[e]),t),{}),ue=null,jn={},zn={},Dn={},Fn={},Ln={};function Ei(t){return~ci.indexOf(t)}function Pi(t,e){let n=e.split("-"),a=n[0],i=n.slice(1).join("-");return a===t&&i!==""&&!Ei(i)?i:null}var Tn=()=>{let t=a=>Ht(lt,(i,r,s)=>(i[s]=Ht(r,a,{}),i),{});jn=t((a,i,r)=>(i[3]&&(a[i[3]]=r),i[2]&&i[2].filter(s=>typeof s=="number").forEach(s=>{a[s.toString(16)]=r}),a)),zn=t((a,i,r)=>(a[r]=r,i[2]&&i[2].filter(s=>typeof s=="string").forEach(s=>{a[s]=r}),a)),Ln=t((a,i,r)=>{let s=i[2];return a[r]=r,s.forEach(o=>{a[o]=r}),a});let e="far"in lt||u.autoFetchSvg,n=Ht(Si,(a,i)=>{let r=i[0],s=i[1],o=i[2];return s==="far"&&!e&&(s="fas"),typeof r=="string"&&(a.names[r]={prefix:s,iconName:o}),typeof r=="number"&&(a.unicodes[r.toString(16)]={prefix:s,iconName:o}),a},{names:{},unicodes:{}});Dn=n.names,Fn=n.unicodes,ue=kt(u.styleDefault,{family:u.familyDefault})};hi(t=>{ue=kt(t.styleDefault,{family:u.familyDefault})}),Tn();function he(t,e){return(jn[t]||{})[e]}function _i(t,e){return(zn[t]||{})[e]}function U(t,e){return(Ln[t]||{})[e]}function Un(t){return Dn[t]||{prefix:null,iconName:null}}function Ci(t){let e=Fn[t],n=he("fas",t);return e||(n?{prefix:"fas",iconName:n}:null)||{prefix:null,iconName:null}}function M(){return ue}var Vn=()=>({prefix:null,iconName:null,rest:[]});function Ni(t){let e=$,n=Rn.reduce((a,i)=>(a[i]=`${u.cssPrefix}-${i}`,a),{});return wn.forEach(a=>{(t.includes(n[a])||t.some(i=>Ii[a].includes(i)))&&(e=a)}),e}function kt(t){let{family:e=$}=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=si[e][t];if(e===wt&&!t)return"fad";let a=Be[e][t]||Be[e][n],i=t in S.styles?t:null;return a||i||null}function Oi(t){let e=[],n=null;return t.forEach(a=>{let i=Pi(u.cssPrefix,a);i?n=i:a&&e.push(a)}),{iconName:n,rest:e}}function Xe(t){return t.sort().filter((e,n,a)=>a.indexOf(e)===n)}function At(t){let{skipLookups:e=!1}=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=null,a=qt.concat(Ga),i=Xe(t.filter(f=>a.includes(f))),r=Xe(t.filter(f=>!qt.includes(f))),[s=null]=i.filter(f=>(n=f,!$n.includes(f))),o=Ni(i),d=l(l({},Oi(r)),{},{prefix:kt(s,{family:o})});return l(l(l({},d),zi({values:t,family:o,styles:lt,config:u,canonical:d,givenPrefix:n})),Mi(e,n,d))}function Mi(t,e,n){let{prefix:a,iconName:i}=n;if(t||!a||!i)return{prefix:a,iconName:i};let r=e==="fa"?Un(i):{},s=U(a,i);return i=r.iconName||s||i,a=r.prefix||a,a==="far"&&!lt.far&&lt.fas&&!u.autoFetchSvg&&(a="fas"),{prefix:a,iconName:i}}var Ri=wn.filter(t=>t!==$||t!==wt),ji=Object.keys(Bt).filter(t=>t!==$).map(t=>Object.keys(Bt[t])).flat();function zi(t){let{values:e,family:n,canonical:a,givenPrefix:i="",styles:r={},config:s={}}=t,o=n===wt,d=e.includes("fa-duotone")||e.includes("fad"),f=s.familyDefault==="duotone",h=a.prefix==="fad"||a.prefix==="fa-duotone";return!o&&(d||f||h)&&(a.prefix="fad"),(e.includes("fa-brands")||e.includes("fab"))&&(a.prefix="fab"),!a.prefix&&Ri.includes(n)&&(Object.keys(r).find(m=>ji.includes(m))||s.autoFetchSvg)&&(a.prefix=Ta.get(n).defaultShortPrefixId,a.iconName=U(a.prefix,a.iconName)||a.iconName),(a.prefix==="fa"||i==="fa")&&(a.prefix=M()||"fas"),a}var Di=class{constructor(){this.definitions={}}add(){let t=[...arguments].reduce(this._pullDefinitions,{});Object.keys(t).forEach(e=>{this.definitions[e]=l(l({},this.definitions[e]||{}),t[e]),Zt(e,t[e]);let n=de[$][e];n&&Zt(n,t[e]),Tn()})}reset(){this.definitions={}}_pullDefinitions(t,e){let n=e.prefix&&e.iconName&&e.icon?{0:e}:e;return Object.keys(n).map(a=>{let{prefix:i,iconName:r,icon:s}=n[a],o=s[2];t[i]||(t[i]={}),o.length>0&&o.forEach(d=>{typeof d=="string"&&(t[i][d]=s)}),t[i][r]=s}),t}},Ke=[],X={},K={},Fi=Object.keys(K);function Li(t,e){let{mixoutsTo:n}=e;return Ke=t,X={},Object.keys(K).forEach(a=>{Fi.indexOf(a)===-1&&delete K[a]}),Ke.forEach(a=>{let i=a.mixout?a.mixout():{};if(Object.keys(i).forEach(r=>{typeof i[r]=="function"&&(n[r]=i[r]),typeof i[r]=="object"&&Object.keys(i[r]).forEach(s=>{n[r]||(n[r]={}),n[r][s]=i[r][s]})}),a.hooks){let r=a.hooks();Object.keys(r).forEach(s=>{X[s]||(X[s]=[]),X[s].push(r[s])})}a.provides&&a.provides(K)}),n}function Qt(t,e){var n=[...arguments].slice(2);return(X[t]||[]).forEach(a=>{e=a.apply(null,[e,...n])}),e}function V(t){var e=[...arguments].slice(1);(X[t]||[]).forEach(n=>{n.apply(null,e)})}function R(){let t=arguments[0],e=Array.prototype.slice.call(arguments,1);return K[t]?K[t].apply(null,e):void 0}function te(t){t.prefix==="fa"&&(t.prefix="fas");let{iconName:e}=t,n=t.prefix||M();if(e)return e=U(n,e)||e,Ge(Hn.definitions,n,e)||Ge(S.styles,n,e)}var Hn=new Di,x={noAuto:()=>{u.autoReplaceSvg=!1,u.observeMutations=!1,V("noAuto")},config:u,dom:{i2svg:function(){let t=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};return P?(V("beforeI2svg",t),R("pseudoElements2svg",t),R("i2svg",t)):Promise.reject(Error("Operation requires a DOM of some kind."))},watch:function(){let t=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},{autoReplaceSvgRoot:e}=t;u.autoReplaceSvg===!1&&(u.autoReplaceSvg=!0),u.observeMutations=!0,wi(()=>{Ti({autoReplaceSvgRoot:e}),V("watch",t)})}},parse:{icon:t=>{if(t===null)return null;if(typeof t=="object"&&t.prefix&&t.iconName)return{prefix:t.prefix,iconName:U(t.prefix,t.iconName)||t.iconName};if(Array.isArray(t)&&t.length===2){let e=t[1].indexOf("fa-")===0?t[1].slice(3):t[1],n=kt(t[0]);return{prefix:n,iconName:U(n,e)||e}}if(typeof t=="string"&&(t.indexOf(`${u.cssPrefix}-`)>-1||t.match(oi))){let e=At(t.split(" "),{skipLookups:!0});return{prefix:e.prefix||M(),iconName:U(e.prefix,e.iconName)||e.iconName}}if(typeof t=="string"){let e=M();return{prefix:e,iconName:U(e,t)||t}}}},library:Hn,findIconDefinition:te,toHtml:ct},Ti=function(){let{autoReplaceSvgRoot:t=b}=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};(Object.keys(S.styles).length>0||u.autoFetchSvg)&&P&&u.autoReplaceSvg&&x.dom.i2svg({node:t})};function St(t,e){return Object.defineProperty(t,"abstract",{get:e}),Object.defineProperty(t,"html",{get:function(){return t.abstract.map(n=>ct(n))}}),Object.defineProperty(t,"node",{get:function(){if(!P)return;let n=b.createElement("div");return n.innerHTML=t.html,n.children}}),t}function Ui(t){let{children:e,main:n,mask:a,attributes:i,styles:r,transform:s}=t;if(fe(s)&&n.found&&!a.found){let{width:o,height:d}=n,f={x:o/d/2,y:.5};i.style=xt(l(l({},r),{},{"transform-origin":`${f.x+s.x/16}em ${f.y+s.y/16}em`}))}return[{tag:"svg",attributes:i,children:e}]}function Vi(t){let{prefix:e,iconName:n,children:a,attributes:i,symbol:r}=t,s=r===!0?`${e}-${u.cssPrefix}-${n}`:r;return[{tag:"svg",attributes:{style:"display: none;"},children:[{tag:"symbol",attributes:l(l({},i),{},{id:s}),children:a}]}]}function me(t){let{icons:{main:e,mask:n},prefix:a,iconName:i,transform:r,symbol:s,title:o,maskId:d,titleId:f,extra:h,watchable:m=!1}=t,{width:p,height:v}=n.found?n:e,k=Ya.includes(a),j=[u.replacementClass,i?`${u.cssPrefix}-${i}`:""].filter(Y=>h.classes.indexOf(Y)===-1).filter(Y=>Y!==""||!!Y).concat(h.classes).join(" "),w={children:[],attributes:l(l({},h.attributes),{},{"data-prefix":a,"data-icon":i,class:j,role:h.attributes.role||"img",xmlns:"http://www.w3.org/2000/svg",viewBox:`0 0 ${p} ${v}`})},_=k&&!~h.classes.indexOf("fa-fw")?{width:`${p/v*16*.0625}em`}:{};m&&(w.attributes[H]=""),o&&(w.children.push({tag:"title",attributes:{id:w.attributes["aria-labelledby"]||`title-${f||ot()}`},children:[o]}),delete w.attributes.title);let y=l(l({},w),{},{prefix:a,iconName:i,main:e,mask:n,maskId:d,transform:r,symbol:s,styles:l(l({},_),h.styles)}),{children:W,attributes:Q}=n.found&&e.found?R("generateAbstractMask",y)||{children:[],attributes:{}}:R("generateAbstractIcon",y)||{children:[],attributes:{}};return y.children=W,y.attributes=Q,s?Vi(y):Ui(y)}function Ze(t){let{content:e,width:n,height:a,transform:i,title:r,extra:s,watchable:o=!1}=t,d=l(l(l({},s.attributes),r?{title:r}:{}),{},{class:s.classes.join(" ")});o&&(d[H]="");let f=l({},s.styles);fe(i)&&(f.transform=vi({transform:i,startCentered:!0,width:n,height:a}),f["-webkit-transform"]=f.transform);let h=xt(f);h.length>0&&(d.style=h);let m=[];return m.push({tag:"span",attributes:d,children:[e]}),r&&m.push({tag:"span",attributes:{class:"sr-only"},children:[r]}),m}function Hi(t){let{content:e,title:n,extra:a}=t,i=l(l(l({},a.attributes),n?{title:n}:{}),{},{class:a.classes.join(" ")}),r=xt(a.styles);r.length>0&&(i.style=r);let s=[];return s.push({tag:"span",attributes:i,children:[e]}),n&&s.push({tag:"span",attributes:{class:"sr-only"},children:[n]}),s}var{styles:Wt}=S;function ee(t){let e=t[0],n=t[1],[a]=t.slice(4),i=null;return i=Array.isArray(a)?{tag:"g",attributes:{class:`${u.cssPrefix}-${Ut.GROUP}`},children:[{tag:"path",attributes:{class:`${u.cssPrefix}-${Ut.SECONDARY}`,fill:"currentColor",d:a[0]}},{tag:"path",attributes:{class:`${u.cssPrefix}-${Ut.PRIMARY}`,fill:"currentColor",d:a[1]}}]}:{tag:"path",attributes:{fill:"currentColor",d:a}},{found:!0,width:e,height:n,icon:i}}var Wi={found:!1,width:512,height:512};function Yi(t,e){!Sn&&!u.showMissingIcons&&t&&console.error(`Icon with name "${t}" and prefix "${e}" is missing.`)}function ne(t,e){let n=e;return e==="fa"&&u.styleDefault!==null&&(e=M()),new Promise((a,i)=>{if(n==="fa"){let r=Un(t)||{};t=r.iconName||t,e=r.prefix||e}if(t&&e&&Wt[e]&&Wt[e][t]){let r=Wt[e][t];return a(ee(r))}Yi(t,e),a(l(l({},Wi),{},{icon:u.showMissingIcons&&t&&R("missingIconAbstract")||{}}))})}var Qe=()=>{},ae=u.measurePerformance&&pt&&pt.mark&&pt.measure?pt:{mark:Qe,measure:Qe},it='FA "6.7.2"',Bi=t=>(ae.mark(`${it} ${t} begins`),()=>Wn(t)),Wn=t=>{ae.mark(`${it} ${t} ends`),ae.measure(`${it} ${t}`,`${it} ${t} begins`,`${it} ${t} ends`)},pe={begin:Bi,end:Wn},bt=()=>{};function tn(t){return typeof(t.getAttribute?t.getAttribute(H):null)=="string"}function qi(t){let e=t.getAttribute?t.getAttribute(oe):null,n=t.getAttribute?t.getAttribute(le):null;return e&&n}function Gi(t){return t&&t.classList&&t.classList.contains&&t.classList.contains(u.replacementClass)}function Ji(){return u.autoReplaceSvg===!0?vt.replace:vt[u.autoReplaceSvg]||vt.replace}function Xi(t){return b.createElementNS("http://www.w3.org/2000/svg",t)}function Ki(t){return b.createElement(t)}function Yn(t){let{ceFn:e=t.tag==="svg"?Xi:Ki}=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};if(typeof t=="string")return b.createTextNode(t);let n=e(t.tag);return Object.keys(t.attributes||[]).forEach(function(a){n.setAttribute(a,t.attributes[a])}),(t.children||[]).forEach(function(a){n.appendChild(Yn(a,{ceFn:e}))}),n}function Zi(t){let e=` ${t.outerHTML} `;return e=`${e}Font Awesome fontawesome.com `,e}var vt={replace:function(t){let e=t[0];if(e.parentNode)if(t[1].forEach(n=>{e.parentNode.insertBefore(Yn(n),e)}),e.getAttribute(H)===null&&u.keepOriginalSource){let n=b.createComment(Zi(e));e.parentNode.replaceChild(n,e)}else e.remove()},nest:function(t){let e=t[0],n=t[1];if(~ce(e).indexOf(u.replacementClass))return vt.replace(t);let a=RegExp(`${u.cssPrefix}-.*`);if(delete n[0].attributes.id,n[0].attributes.class){let r=n[0].attributes.class.split(" ").reduce((s,o)=>(o===u.replacementClass||o.match(a)?s.toSvg.push(o):s.toNode.push(o),s),{toNode:[],toSvg:[]});n[0].attributes.class=r.toSvg.join(" "),r.toNode.length===0?e.removeAttribute("class"):e.setAttribute("class",r.toNode.join(" "))}let i=n.map(r=>ct(r)).join(`
`);e.setAttribute(H,""),e.innerHTML=i}};function en(t){t()}function Bn(t,e){let n=typeof e=="function"?e:bt;if(t.length===0)n();else{let a=en;u.mutateApproach===ii&&(a=O.requestAnimationFrame||en),a(()=>{let i=Ji(),r=pe.begin("mutate");t.map(i),r(),n()})}}var ge=!1;function qn(){ge=!0}function ie(){ge=!1}var $t=null;function nn(t){if(!Ve||!u.observeMutations)return;let{treeCallback:e=bt,nodeCallback:n=bt,pseudoElementsCallback:a=bt,observeMutationsRoot:i=b}=t;$t=new Ve(r=>{if(ge)return;let s=M();Z(r).forEach(o=>{if(o.type==="childList"&&o.addedNodes.length>0&&!tn(o.addedNodes[0])&&(u.searchPseudoElements&&a(o.target),e(o.target)),o.type==="attributes"&&o.target.parentNode&&u.searchPseudoElements&&a(o.target.parentNode),o.type==="attributes"&&tn(o.target)&&~di.indexOf(o.attributeName))if(o.attributeName==="class"&&qi(o.target)){let{prefix:d,iconName:f}=At(ce(o.target));o.target.setAttribute(oe,d||s),f&&o.target.setAttribute(le,f)}else Gi(o.target)&&n(o.target)})}),P&&$t.observe(i,{childList:!0,attributes:!0,characterData:!0,subtree:!0})}function Qi(){$t&&$t.disconnect()}function tr(t){let e=t.getAttribute("style"),n=[];return e&&(n=e.split(";").reduce((a,i)=>{let r=i.split(":"),s=r[0],o=r.slice(1);return s&&o.length>0&&(a[s]=o.join(":").trim()),a},{})),n}function er(t){let e=t.getAttribute("data-prefix"),n=t.getAttribute("data-icon"),a=t.innerText===void 0?"":t.innerText.trim(),i=At(ce(t));return i.prefix||=M(),e&&n&&(i.prefix=e,i.iconName=n),i.iconName&&i.prefix||(i.prefix&&a.length>0&&(i.iconName=_i(i.prefix,t.innerText)||he(i.prefix,Mn(t.innerText))),!i.iconName&&u.autoFetchSvg&&t.firstChild&&t.firstChild.nodeType===Node.TEXT_NODE&&(i.iconName=t.firstChild.data)),i}function nr(t){let e=Z(t.attributes).reduce((i,r)=>(i.name!=="class"&&i.name!=="style"&&(i[r.name]=r.value),i),{}),n=t.getAttribute("title"),a=t.getAttribute("data-fa-title-id");return u.autoA11y&&(n?e["aria-labelledby"]=`${u.replacementClass}-title-${a||ot()}`:(e["aria-hidden"]="true",e.focusable="false")),e}function ar(){return{iconName:null,title:null,titleId:null,prefix:null,transform:A,symbol:!1,mask:{iconName:null,prefix:null,rest:[]},maskId:null,extra:{classes:[],styles:{},attributes:{}}}}function an(t){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{styleParser:!0},{iconName:n,prefix:a,rest:i}=er(t),r=nr(t),s=Qt("parseNodeAttributes",{},t),o=e.styleParser?tr(t):[];return l({iconName:n,title:t.getAttribute("title"),titleId:t.getAttribute("data-fa-title-id"),prefix:a,transform:A,mask:{iconName:null,prefix:null,rest:[]},maskId:null,symbol:!1,extra:{classes:i,styles:o,attributes:r}},s)}var{styles:ir}=S;function Gn(t){let e=u.autoReplaceSvg==="nest"?an(t,{styleParser:!1}):an(t);return~e.extra.classes.indexOf(En)?R("generateLayersText",t,e):R("generateSvgReplacementMutation",t,e)}function rr(){return[...Va,...qt]}function rn(t){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;if(!P)return Promise.resolve();let n=b.documentElement.classList,a=h=>n.add(`${Ye}-${h}`),i=h=>n.remove(`${Ye}-${h}`),r=u.autoFetchSvg?rr():$n.concat(Object.keys(ir));r.includes("fa")||r.push("fa");let s=[`.${En}:not([${H}])`].concat(r.map(h=>`.${h}:not([${H}])`)).join(", ");if(s.length===0)return Promise.resolve();let o=[];try{o=Z(t.querySelectorAll(s))}catch{}if(o.length>0)a("pending"),i("complete");else return Promise.resolve();let d=pe.begin("onTree"),f=o.reduce((h,m)=>{try{let p=Gn(m);p&&h.push(p)}catch(p){Sn||p.name==="MissingIcon"&&console.error(p)}return h},[]);return new Promise((h,m)=>{Promise.all(f).then(p=>{Bn(p,()=>{a("active"),a("complete"),i("pending"),typeof e=="function"&&e(),d(),h()})}).catch(p=>{d(),m(p)})})}function sr(t){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;Gn(t).then(n=>{n&&Bn([n],e)})}function or(t){return function(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},a=(e||{}).icon?e:te(e||{}),{mask:i}=n;return i&&=(i||{}).icon?i:te(i||{}),t(a,l(l({},n),{},{mask:i}))}}var lr=function(t){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},{transform:n=A,symbol:a=!1,mask:i=null,maskId:r=null,title:s=null,titleId:o=null,classes:d=[],attributes:f={},styles:h={}}=e;if(!t)return;let{prefix:m,iconName:p,icon:v}=t;return St(l({type:"icon"},t),()=>(V("beforeDOMElementCreation",{iconDefinition:t,params:e}),u.autoA11y&&(s?f["aria-labelledby"]=`${u.replacementClass}-title-${o||ot()}`:(f["aria-hidden"]="true",f.focusable="false")),me({icons:{main:ee(v),mask:i?ee(i.icon):{found:!1,width:null,height:null,icon:{}}},prefix:m,iconName:p,transform:l(l({},A),n),symbol:a,title:s,maskId:r,titleId:o,extra:{attributes:f,styles:h,classes:d}})))},dr={mixout(){return{icon:or(lr)}},hooks(){return{mutationObserverCallbacks(t){return t.treeCallback=rn,t.nodeCallback=sr,t}}},provides(t){t.i2svg=function(e){let{node:n=b,callback:a=()=>{}}=e;return rn(n,a)},t.generateSvgReplacementMutation=function(e,n){let{iconName:a,title:i,titleId:r,prefix:s,transform:o,symbol:d,mask:f,maskId:h,extra:m}=n;return new Promise((p,v)=>{Promise.all([ne(a,s),f.iconName?ne(f.iconName,f.prefix):Promise.resolve({found:!1,width:512,height:512,icon:{}})]).then(k=>{let[j,w]=k;p([e,me({icons:{main:j,mask:w},prefix:s,iconName:a,transform:o,symbol:d,maskId:h,title:i,titleId:r,extra:m,watchable:!0})])}).catch(v)})},t.generateAbstractIcon=function(e){let{children:n,attributes:a,main:i,transform:r,styles:s}=e,o=xt(s);o.length>0&&(a.style=o);let d;return fe(r)&&(d=R("generateAbstractTransformGrouping",{main:i,transform:r,containerWidth:i.width,iconWidth:i.width})),n.push(d||i.icon),{children:n,attributes:a}}}},cr={mixout(){return{layer(t){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},{classes:n=[]}=e;return St({type:"layer"},()=>{V("beforeDOMElementCreation",{assembler:t,params:e});let a=[];return t(i=>{Array.isArray(i)?i.map(r=>{a=a.concat(r.abstract)}):a=a.concat(i.abstract)}),[{tag:"span",attributes:{class:[`${u.cssPrefix}-layers`,...n].join(" ")},children:a}]})}}}},fr={mixout(){return{counter(t){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},{title:n=null,classes:a=[],attributes:i={},styles:r={}}=e;return St({type:"counter",content:t},()=>(V("beforeDOMElementCreation",{content:t,params:e}),Hi({content:t.toString(),title:n,extra:{attributes:i,styles:r,classes:[`${u.cssPrefix}-layers-counter`,...a]}})))}}}},ur={mixout(){return{text(t){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},{transform:n=A,title:a=null,classes:i=[],attributes:r={},styles:s={}}=e;return St({type:"text",content:t},()=>(V("beforeDOMElementCreation",{content:t,params:e}),Ze({content:t,transform:l(l({},A),n),title:a,extra:{attributes:r,styles:s,classes:[`${u.cssPrefix}-layers-text`,...i]}})))}}},provides(t){t.generateLayersText=function(e,n){let{title:a,transform:i,extra:r}=n,s=null,o=null;if(vn){let d=parseInt(getComputedStyle(e).fontSize,10),f=e.getBoundingClientRect();s=f.width/d,o=f.height/d}return u.autoA11y&&!a&&(r.attributes["aria-hidden"]="true"),Promise.resolve([e,Ze({content:e.innerHTML,width:s,height:o,transform:i,title:a,extra:r,watchable:!0})])}}},hr=RegExp('"',"ug"),sn=[1105920,1112319],on=l(l(l(l({},{FontAwesome:{normal:"fas",400:"fas"}}),La),ni),Ja),re=Object.keys(on).reduce((t,e)=>(t[e.toLowerCase()]=on[e],t),{}),mr=Object.keys(re).reduce((t,e)=>{let n=re[e];return t[e]=n[900]||[...Object.entries(n)][0][1],t},{});function pr(t){let e=t.replace(hr,""),n=Ai(e,0),a=n>=sn[0]&&n<=sn[1],i=e.length===2&&e[0]===e[1];return{value:Mn(i?e[0]:e),isSecondary:a||i}}function gr(t,e){let n=t.replace(/^['"]|['"]$/g,"").toLowerCase(),a=parseInt(e),i=isNaN(a)?"normal":a;return(re[n]||{})[i]||mr[n]}function ln(t,e){let n=`${ai}${e.replace(":","-")}`;return new Promise((a,i)=>{if(t.getAttribute(n)!==null)return a();let r=Z(t.children).filter(m=>m.getAttribute(Jt)===e)[0],s=O.getComputedStyle(t,e),o=s.getPropertyValue("font-family"),d=o.match(li),f=s.getPropertyValue("font-weight"),h=s.getPropertyValue("content");if(r&&!d)return t.removeChild(r),a();if(d&&h!=="none"&&h!==""){let m=s.getPropertyValue("content"),p=gr(o,f),{value:v,isSecondary:k}=pr(m),j=d[0].startsWith("FontAwesome"),w=he(p,v),_=w;if(j){let y=Ci(v);y.iconName&&y.prefix&&(w=y.iconName,p=y.prefix)}if(w&&!k&&(!r||r.getAttribute(oe)!==p||r.getAttribute(le)!==_)){t.setAttribute(n,_),r&&t.removeChild(r);let y=ar(),{extra:W}=y;W.attributes[Jt]=e,ne(w,p).then(Q=>{let Y=me(l(l({},y),{},{icons:{main:Q,mask:Vn()},prefix:p,iconName:_,extra:W,watchable:!0})),It=b.createElementNS("http://www.w3.org/2000/svg","svg");e==="::before"?t.insertBefore(It,t.firstChild):t.appendChild(It),It.outerHTML=Y.map(Jn=>ct(Jn)).join(`
`),t.removeAttribute(n),a()}).catch(i)}else a()}else a()})}function br(t){return Promise.all([ln(t,"::before"),ln(t,"::after")])}function vr(t){return t.parentNode!==document.head&&!~ri.indexOf(t.tagName.toUpperCase())&&!t.getAttribute(Jt)&&(!t.parentNode||t.parentNode.tagName!=="svg")}function dn(t){if(P)return new Promise((e,n)=>{let a=Z(t.querySelectorAll("*")).filter(vr).map(br),i=pe.begin("searchPseudoElements");qn(),Promise.all(a).then(()=>{i(),ie(),e()}).catch(()=>{i(),ie(),n()})})}var yr={hooks(){return{mutationObserverCallbacks(t){return t.pseudoElementsCallback=dn,t}}},provides(t){t.pseudoElements2svg=function(e){let{node:n=b}=e;u.searchPseudoElements&&dn(n)}}},cn=!1,$r={mixout(){return{dom:{unwatch(){qn(),cn=!0}}}},hooks(){return{bootstrap(){nn(Qt("mutationObserverCallbacks",{}))},noAuto(){Qi()},watch(t){let{observeMutationsRoot:e}=t;cn?ie():nn(Qt("mutationObserverCallbacks",{observeMutationsRoot:e}))}}}},fn=t=>t.toLowerCase().split(" ").reduce((e,n)=>{let a=n.toLowerCase().split("-"),i=a[0],r=a.slice(1).join("-");if(i&&r==="h")return e.flipX=!0,e;if(i&&r==="v")return e.flipY=!0,e;if(r=parseFloat(r),isNaN(r))return e;switch(i){case"grow":e.size+=r;break;case"shrink":e.size-=r;break;case"left":e.x-=r;break;case"right":e.x+=r;break;case"up":e.y-=r;break;case"down":e.y+=r;break;case"rotate":e.rotate+=r;break}return e},{size:16,x:0,y:0,flipX:!1,flipY:!1,rotate:0}),wr={mixout(){return{parse:{transform:t=>fn(t)}}},hooks(){return{parseNodeAttributes(t,e){let n=e.getAttribute("data-fa-transform");return n&&(t.transform=fn(n)),t}}},provides(t){t.generateAbstractTransformGrouping=function(e){let{main:n,transform:a,containerWidth:i,iconWidth:r}=e,s={outer:{transform:`translate(${i/2} 256)`},inner:{transform:`${`translate(${a.x*32}, ${a.y*32}) `} ${`scale(${a.size/16*(a.flipX?-1:1)}, ${a.size/16*(a.flipY?-1:1)}) `} ${`rotate(${a.rotate} 0 0)`}`},path:{transform:`translate(${r/2*-1} -256)`}};return{tag:"g",attributes:l({},s.outer),children:[{tag:"g",attributes:l({},s.inner),children:[{tag:n.icon.tag,children:n.icon.children,attributes:l(l({},n.icon.attributes),s.path)}]}]}}}},Yt={x:0,y:0,width:"100%",height:"100%"};function un(t){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0;return t.attributes&&(t.attributes.fill||e)&&(t.attributes.fill="black"),t}function xr(t){return t.tag==="g"?t.children:[t]}Li([$i,dr,cr,fr,ur,yr,$r,wr,{hooks(){return{parseNodeAttributes(t,e){let n=e.getAttribute("data-fa-mask"),a=n?At(n.split(" ").map(i=>i.trim())):Vn();return a.prefix||=M(),t.mask=a,t.maskId=e.getAttribute("data-fa-mask-id"),t}}},provides(t){t.generateAbstractMask=function(e){let{children:n,attributes:a,main:i,mask:r,maskId:s,transform:o}=e,{width:d,icon:f}=i,{width:h,icon:m}=r,p=bi({transform:o,containerWidth:h,iconWidth:d}),v={tag:"rect",attributes:l(l({},Yt),{},{fill:"white"})},k=f.children?{children:f.children.map(un)}:{},j={tag:"g",attributes:l({},p.inner),children:[un(l({tag:f.tag,attributes:l(l({},f.attributes),p.path)},k))]},w={tag:"g",attributes:l({},p.outer),children:[j]},_=`mask-${s||ot()}`,y=`clip-${s||ot()}`,W={tag:"mask",attributes:l(l({},Yt),{},{id:_,maskUnits:"userSpaceOnUse",maskContentUnits:"userSpaceOnUse"}),children:[v,w]},Q={tag:"defs",children:[{tag:"clipPath",attributes:{id:y},children:xr(m)},W]};return n.push(Q,{tag:"rect",attributes:l({fill:"currentColor","clip-path":`url(#${y})`,mask:`url(#${_})`},Yt)}),{children:n,attributes:a}}}},{provides(t){let e=!1;O.matchMedia&&(e=O.matchMedia("(prefers-reduced-motion: reduce)").matches),t.missingIconAbstract=function(){let n=[],a={fill:"currentColor"},i={attributeType:"XML",repeatCount:"indefinite",dur:"2s"};n.push({tag:"path",attributes:l(l({},a),{},{d:"M156.5,447.7l-12.6,29.5c-18.7-9.5-35.9-21.2-51.5-34.9l22.7-22.7C127.6,430.5,141.5,440,156.5,447.7z M40.6,272H8.5 c1.4,21.2,5.4,41.7,11.7,61.1L50,321.2C45.1,305.5,41.8,289,40.6,272z M40.6,240c1.4-18.8,5.2-37,11.1-54.1l-29.5-12.6 C14.7,194.3,10,216.7,8.5,240H40.6z M64.3,156.5c7.8-14.9,17.2-28.8,28.1-41.5L69.7,92.3c-13.7,15.6-25.5,32.8-34.9,51.5 L64.3,156.5z M397,419.6c-13.9,12-29.4,22.3-46.1,30.4l11.9,29.8c20.7-9.9,39.8-22.6,56.9-37.6L397,419.6z M115,92.4 c13.9-12,29.4-22.3,46.1-30.4l-11.9-29.8c-20.7,9.9-39.8,22.6-56.8,37.6L115,92.4z M447.7,355.5c-7.8,14.9-17.2,28.8-28.1,41.5 l22.7,22.7c13.7-15.6,25.5-32.9,34.9-51.5L447.7,355.5z M471.4,272c-1.4,18.8-5.2,37-11.1,54.1l29.5,12.6 c7.5-21.1,12.2-43.5,13.6-66.8H471.4z M321.2,462c-15.7,5-32.2,8.2-49.2,9.4v32.1c21.2-1.4,41.7-5.4,61.1-11.7L321.2,462z M240,471.4c-18.8-1.4-37-5.2-54.1-11.1l-12.6,29.5c21.1,7.5,43.5,12.2,66.8,13.6V471.4z M462,190.8c5,15.7,8.2,32.2,9.4,49.2h32.1 c-1.4-21.2-5.4-41.7-11.7-61.1L462,190.8z M92.4,397c-12-13.9-22.3-29.4-30.4-46.1l-29.8,11.9c9.9,20.7,22.6,39.8,37.6,56.9 L92.4,397z M272,40.6c18.8,1.4,36.9,5.2,54.1,11.1l12.6-29.5C317.7,14.7,295.3,10,272,8.5V40.6z M190.8,50 c15.7-5,32.2-8.2,49.2-9.4V8.5c-21.2,1.4-41.7,5.4-61.1,11.7L190.8,50z M442.3,92.3L419.6,115c12,13.9,22.3,29.4,30.5,46.1 l29.8-11.9C470,128.5,457.3,109.4,442.3,92.3z M397,92.4l22.7-22.7c-15.6-13.7-32.8-25.5-51.5-34.9l-12.6,29.5 C370.4,72.1,384.4,81.5,397,92.4z"})});let r=l(l({},i),{},{attributeName:"opacity"}),s={tag:"circle",attributes:l(l({},a),{},{cx:"256",cy:"364",r:"28"}),children:[]};return e||s.children.push({tag:"animate",attributes:l(l({},i),{},{attributeName:"r",values:"28;14;28;28;14;28;"})},{tag:"animate",attributes:l(l({},r),{},{values:"1;0;1;1;0;1;"})}),n.push(s),n.push({tag:"path",attributes:l(l({},a),{},{opacity:"1",d:"M263.7,312h-16c-6.6,0-12-5.4-12-12c0-71,77.4-63.9,77.4-107.8c0-20-17.8-40.2-57.4-40.2c-29.1,0-44.3,9.6-59.2,28.7 c-3.9,5-11.1,6-16.2,2.4l-13.1-9.2c-5.6-3.9-6.9-11.8-2.6-17.2c21.2-27.2,46.4-44.7,91.2-44.7c52.3,0,97.4,29.8,97.4,80.2 c0,67.6-77.4,63.5-77.4,107.8C275.7,306.6,270.3,312,263.7,312z"}),children:e?[]:[{tag:"animate",attributes:l(l({},r),{},{values:"1;0;0;0;0;1;"})}]}),e||n.push({tag:"path",attributes:l(l({},a),{},{opacity:"0",d:"M232.5,134.5l7,168c0.3,6.4,5.6,11.5,12,11.5h9c6.4,0,11.7-5.1,12-11.5l7-168c0.3-6.8-5.2-12.5-12-12.5h-23 C237.7,122,232.2,127.7,232.5,134.5z"}),children:[{tag:"animate",attributes:l(l({},r),{},{values:"0;0;1;1;0;0;"})}]}),{tag:"g",attributes:{class:"missing"},children:n}}}},{hooks(){return{parseNodeAttributes(t,e){let n=e.getAttribute("data-fa-symbol");return t.symbol=n===null?!1:n===""||n,t}}}}],{mixoutsTo:x}),x.noAuto,x.config,x.library,x.dom,x.parse,x.findIconDefinition,x.toHtml;var kr=x.icon;x.layer,x.text,x.counter;function Fr(t={}){return{mount(e){let n,a=Na({label:t.text??"Inspector",title:t.title??"Inspect visualization",icon:t.text===void 0?kr(hn).node[0]:void 0,async onClick(){if(n?.element.isConnected){n.element.focus({preventScroll:!0});return}if(e.showStatus("Loading Inspector\u2026"),n=await Ca(e.api.debug,{container:e.container,width:t.width,activePanel:t.activePanel,signal:e.signal}),e.signal.aborted){n.dispose(),n=void 0;return}n.panel.addEventListener("close",()=>{n=void 0,a.element.focus({preventScroll:!0})},{once:!0,signal:e.signal}),n.element.focus({preventScroll:!0}),e.showStatus("")}}).mount(e);return a.element.setAttribute("aria-haspopup","dialog"),{element:a.element,dispose(){a.dispose(),n?.dispose(),n=void 0}}}}}export{mn as InspectorSession,Pa as appInspector,Ca as attachInspectorOverlay,_a as createInspectorPanel,Dr as genomeSpyInspector,Fr as inspectorButton};
