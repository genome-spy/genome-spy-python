// Vendored from GenomeSpy 0.88.1.
var S=`
    :host {
        position: absolute;
        top: 8px;
        right: 8px;
        z-index: 1;
        max-width: calc(100% - 16px);
        color: var(--gs-controls-color, #333);
        font: 12px system-ui, sans-serif;
        pointer-events: none;
    }
    :host([data-placement="top"]) {
        top: auto;
        bottom: 100%;
    }
    :host([data-placement="bottom"]) {
        top: 100%;
    }
    :host([data-placement="top"]) .buttons {
        padding-bottom: 4px;
    }
    :host([data-placement="bottom"]) .buttons {
        padding-top: 4px;
    }
    .buttons {
        display: flex;
        justify-content: flex-end;
        gap: 3px;
        opacity: 0;
        transition: opacity 250ms ease;
    }
    :host([data-container-active]) .buttons {
        opacity: var(--gs-controls-hover-opacity, 0.3);
        pointer-events: auto;
    }
    :host(:hover) .buttons,
    :host(:focus-within) .buttons,
    :host([data-visibility="always"]) .buttons {
        opacity: 1;
        pointer-events: auto;
    }
    @media (hover: none) {
        :host([data-visibility]) .buttons {
            opacity: 1;
            pointer-events: auto;
        }
    }
    @media (prefers-reduced-motion: reduce) {
        .buttons {
            transition: none;
        }
    }
    button, a {
        display: inline-flex;
        box-sizing: border-box;
        align-items: center;
        justify-content: center;
        gap: 4px;
        min-width: 32px;
        min-height: 32px;
        padding: 5px 7px;
        border: 0;
        border-radius: 4px;
        background: var(--gs-controls-background, #fff);
        color: inherit;
        font: inherit;
        text-decoration: none;
        cursor: pointer;
    }
    button:hover, a:hover {
        outline: 1px solid #999;
    }
    button:focus-visible, a:focus-visible {
        outline: 2px solid currentColor;
        outline-offset: 2px;
    }
    button:disabled {
        opacity: 0.6;
        cursor: wait;
    }
    .icon {
        display: inline-flex;
        flex-shrink: 0;
    }
    .icon, .icon > *, svg, img {
        width: 16px;
        height: 16px;
    }
    p {
        position: absolute;
        top: 100%;
        right: 0;
        pointer-events: auto;
        width: max-content;
        max-width: min(320px, calc(100vw - 16px));
        box-sizing: border-box;
        padding: 8px;
        margin: 4px 0 0;
        border: 1px solid #bbb;
        border-radius: 4px;
        background: var(--gs-controls-background, #fff);
        white-space: pre-line;
        overflow-wrap: anywhere;
    }
    :host([data-placement="bottom"]) p {
        top: auto;
        bottom: 100%;
        margin: 0 0 4px;
    }
`;function v(e,n){let r=Object.keys(n).map(t=>({name:t,value:e.style.getPropertyValue(t),priority:e.style.getPropertyPriority(t)}));for(let[t,o]of Object.entries(n))e.style.setProperty(t,o,"important");return()=>{for(let{name:t,value:o,priority:i}of r)e.style.setProperty(t,o,i)}}function A(e){if(!e.label.trim())throw new Error("A button requires a non-empty accessible label.");return{mount(n){let r=n.container.ownerDocument,t=r.createElement("button");if(t.type="button",e.icon){let i=r.createElement("span");i.className="icon",i.setAttribute("aria-hidden","true"),i.inert=!0,i.append(r.importNode(e.icon,!0)),t.append(i)}else t.textContent=e.label;t.title=e.title??e.label,t.setAttribute("aria-label",e.label);async function o(){t.disabled=!0,n.showStatus("");try{await e.onClick(n)}catch(i){n.reportError(i)}finally{t.disabled=!1}}return t.addEventListener("click",o,{signal:n.signal}),{element:t,dispose(){t.removeEventListener("click",o)}}}}}function P(e={}){return C("PNG",e.filename??"genomespy",n=>n.imageExport.raster(e.exportOptions))}function z(e={}){return C("SVG",e.filename??"genomespy",n=>n.imageExport.svg(e.exportOptions))}var k=new WeakMap;function C(e,n,r){return{mount(t){k.has(t)||k.set(t,new Set);let o=k.get(t),i=A({label:e,title:"Download "+e,async onClick(){o.forEach(s=>s.disabled=!0),t.showStatus("Preparing "+e+"\u2026");try{let s=await r(t.api);t.signal.aborted||(U(t.container.ownerDocument,s.blob,`${n}.${e.toLowerCase()}`),t.showStatus(s.warnings?.join(`
`)??""))}finally{o.forEach(s=>s.disabled=!1)}}}).mount(t);return o.add(i.element),{element:i.element,dispose(){o.delete(i.element),i.dispose()}}}}}function U(e,n,r){let t=URL.createObjectURL(n),o=e.createElement("a");o.href=t,o.download=r,e.body.append(o);try{o.click()}finally{o.remove(),setTimeout(()=>URL.revokeObjectURL(t),1e3)}}function M(){return{mount:R}}function R(e){let{container:n,reportError:r}=e,t=n.ownerDocument;if(n==t.body||n==t.documentElement)throw new Error("Full-window controls require a dedicated visualization container.");let o=t.createElement("button");o.type="button";let i=t.createElementNS("http://www.w3.org/2000/svg","svg");i.setAttribute("viewBox","0 0 20 20"),i.setAttribute("aria-hidden","true"),i.setAttribute("fill","none"),i.setAttribute("stroke","currentColor"),i.setAttribute("stroke-width","1.5");let s=t.createElementNS(i.namespaceURI,"path");i.append(s),o.append(i);let l=t.createElement("dialog");l.setAttribute("aria-label","Full-window visualization"),l.style.cssText="position:fixed;inset:0;width:100%;height:100%;max-width:none;max-height:none;margin:0;padding:0;border:0;box-sizing:border-box;overflow:auto;background:white;color:inherit;";let g=t.createComment("GenomeSpy full-window container"),c;function m(){let u=!!c;o.title=u?"Restore visualization size":"Expand to full window",o.setAttribute("aria-label",o.title),o.setAttribute("aria-pressed",String(u)),s.setAttribute("d",u?"M2 7h5V2m6 0v5h5M2 13h5v5m6 0v-5h5":"M7 2H2v5m11-5h5v5M2 13v5h5m6 0h5v-5")}function p(){c&&(l.close(),g.replaceWith(n),c(),c=void 0,l.remove(),m(),o.focus({preventScroll:!0}))}function f(){let u=[];for(let d=n.parentElement;d;d=d.parentElement)u.push({element:d,left:d.scrollLeft,top:d.scrollTop});let x=v(n,{position:"relative",top:"auto",right:"auto",bottom:"auto",left:"auto",width:"100%",height:"100%","min-width":"0","min-height":"0","max-width":"none","max-height":"none","margin-top":"0","margin-right":"0","margin-bottom":"0","margin-left":"0","box-sizing":"border-box"}),E=v(t.documentElement,{"overflow-x":"hidden","overflow-y":"hidden"}),w=e.overridePlacement("inside");c=()=>{w(),x(),E();for(let{element:d,left:y,top:a}of u)d.scrollLeft=y,d.scrollTop=a},n.before(g),l.append(n),t.body.append(l);try{l.showModal()}catch(d){throw p(),d}m(),o.focus({preventScroll:!0})}let h=new AbortController;return o.addEventListener("click",()=>{try{c?p():f()}catch(u){r(u)}},{signal:h.signal}),l.addEventListener("cancel",u=>{u.preventDefault(),p()},{signal:h.signal}),l.addEventListener("close",()=>{l.open||p()},{signal:h.signal}),m(),{element:o,dispose(){p(),h.abort()}}}function j(){return{mount({container:e}){let n=e.ownerDocument,r=n.createElement("a");r.href="https://genomespy.app/",r.target="_blank",r.rel="noopener noreferrer",r.style.padding="5px",r.title="About GenomeSpy",r.setAttribute("aria-label",r.title);let t=n.createElement("img");return t.src=new URL("../img/genomespy-favicon.svg",import.meta.url).href,t.alt="",t.style.width=t.style.height="20px",r.append(t),{element:r,dispose(){r.remove()}}}}}function G(e,n,r){if(!e.isConnected)throw new Error("The controls container must be connected to the document.");if(!Array.isArray(r?.controls))throw new Error("An explicit controls array is required.");let t=e.ownerDocument,o=r.placement??"inside";L(o);let i=r.visibility??(o=="inside"?"hover":"always");if(i!="hover"&&i!="always")throw new Error("Unknown controls visibility: "+i);let s=t.createElement("div");s.dataset.visibility=i,s.dataset.placement=o;let l=s.attachShadow({mode:"open"}),g=t.createElement("style");g.textContent=S;let c=t.createElement("div");c.className="buttons",c.setAttribute("role","group"),c.setAttribute("aria-label","Visualization controls");let m=t.createElement("p");m.setAttribute("role","status"),m.hidden=!0,l.append(g,c,m);let p=new AbortController,{signal:f}=p;function h(){f.aborted||s.toggleAttribute("data-container-active",e.matches(":hover, :focus-within"))}for(let a of["pointerenter","pointerleave","focusin","focusout"])e.addEventListener(a,()=>t.defaultView.requestAnimationFrame(h),{signal:p.signal});c.addEventListener("click",a=>{a.detail>0&&queueMicrotask(()=>{let b=l.activeElement;b instanceof HTMLElement&&b.blur()})},{signal:p.signal});function u(a){f.aborted||(m.textContent=a,m.hidden=!a)}function x(a){f.aborted||(u("Unable to complete action: "+(a instanceof Error?a.message:String(a))),r.onError?.(a))}let E=v(e,t.defaultView.getComputedStyle(e).position=="static"?{position:"relative"}:{}),w=[],d={container:e,api:n,signal:f,showStatus:u,reportError:x,overridePlacement(a){L(a);let b=s.dataset.placement;return s.dataset.placement=a,()=>{s.dataset.placement=b}}};function y(){if(f.aborted)return;p.abort();let a=[];for(let b of w.toReversed())try{b.dispose()}catch(B){a.push(B)}if(s.remove(),E(),a.length)throw new AggregateError(a,"Unable to dispose controls.")}try{for(let a of r.controls){let b=a.mount(d);w.push(b),c.append(b.element)}e.append(s),h()}catch(a){throw y(),a}return{element:s,dispose:y}}function L(e){if(e!="inside"&&e!="top"&&e!="bottom")throw new Error("Unknown controls placement: "+e)}export{G as attachControls,A as button,M as fullWindowButton,j as genomeSpyButton,P as pngButton,z as svgButton};
