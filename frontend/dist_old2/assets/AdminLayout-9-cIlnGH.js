import{d as _,P as c,Q as He,R as Qe,S as Re,U as Ie,V as re,W as X,X as s,Y as w,Z as Pe,_ as ve,$ as G,a0 as Te,a1 as me,I as C,l as M,K as q,a2 as d,a3 as I,a4 as ke,q as j,a5 as oe,a6 as W,a7 as Je,a8 as U,a9 as he,aa as ce,F as eo,ab as ne,ac as oo,ad as to,ae as ze,af as ro,ag as no,o as fe,c as pe,a as V,u as io,e as D,H as ie,C as J,ah as lo,p as ao,ai as co}from"./index-C0M1mhNe.js";import{T as so}from"./TopNavbar-Cf-nixDW.js";import{d as uo,t as vo,C as mo,f as le,N as ho,a as fo,V as po,u as go,c as ae,b as we}from"./Dropdown-BaSOTI8d.js";import{u as de,c as E}from"./resolve-slot-BNUvGlIa.js";import"./LanguageSwitcher-Bl2SqUu6.js";import"./_plugin-vue_export-helper-DlAUqK2U.js";const Co=_({name:"ChevronDownFilled",render(){return c("svg",{viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg"},c("path",{d:"M3.20041 5.73966C3.48226 5.43613 3.95681 5.41856 4.26034 5.70041L8 9.22652L11.7397 5.70041C12.0432 5.41856 12.5177 5.43613 12.7996 5.73966C13.0815 6.0432 13.0639 6.51775 12.7603 6.7996L8.51034 10.7996C8.22258 11.0668 7.77743 11.0668 7.48967 10.7996L3.23966 6.7996C2.93613 6.51775 2.91856 6.0432 3.20041 5.73966Z",fill:"currentColor"}))}});function bo(e){const{baseColor:r,textColor2:o,bodyColor:n,cardColor:a,dividerColor:l,actionColor:v,scrollbarColor:g,scrollbarColorHover:m,invertedColor:h}=e;return{textColor:o,textColorInverted:"#FFF",color:n,colorEmbedded:v,headerColor:a,headerColorInverted:h,footerColor:v,footerColorInverted:h,headerBorderColor:l,headerBorderColorInverted:h,footerBorderColor:l,footerBorderColorInverted:h,siderBorderColor:l,siderBorderColorInverted:h,siderColor:a,siderColorInverted:h,siderToggleButtonBorder:`1px solid ${l}`,siderToggleButtonColor:r,siderToggleButtonIconColor:o,siderToggleButtonIconColorInverted:o,siderToggleBarColor:Ie(n,g),siderToggleBarColorHover:Ie(n,m),__invertScrollbar:"true"}}const Ne=He({name:"Layout",common:Re,peers:{Scrollbar:Qe},self:bo});function xo(e,r,o,n){return{itemColorHoverInverted:"#0000",itemColorActiveInverted:r,itemColorActiveHoverInverted:r,itemColorActiveCollapsedInverted:r,itemTextColorInverted:e,itemTextColorHoverInverted:o,itemTextColorChildActiveInverted:o,itemTextColorChildActiveHoverInverted:o,itemTextColorActiveInverted:o,itemTextColorActiveHoverInverted:o,itemTextColorHorizontalInverted:e,itemTextColorHoverHorizontalInverted:o,itemTextColorChildActiveHorizontalInverted:o,itemTextColorChildActiveHoverHorizontalInverted:o,itemTextColorActiveHorizontalInverted:o,itemTextColorActiveHoverHorizontalInverted:o,itemIconColorInverted:e,itemIconColorHoverInverted:o,itemIconColorActiveInverted:o,itemIconColorActiveHoverInverted:o,itemIconColorChildActiveInverted:o,itemIconColorChildActiveHoverInverted:o,itemIconColorCollapsedInverted:e,itemIconColorHorizontalInverted:e,itemIconColorHoverHorizontalInverted:o,itemIconColorActiveHorizontalInverted:o,itemIconColorActiveHoverHorizontalInverted:o,itemIconColorChildActiveHorizontalInverted:o,itemIconColorChildActiveHoverHorizontalInverted:o,arrowColorInverted:e,arrowColorHoverInverted:o,arrowColorActiveInverted:o,arrowColorActiveHoverInverted:o,arrowColorChildActiveInverted:o,arrowColorChildActiveHoverInverted:o,groupTextColorInverted:n}}function yo(e){const{borderRadius:r,textColor3:o,primaryColor:n,textColor2:a,textColor1:l,fontSize:v,dividerColor:g,hoverColor:m,primaryColorHover:h}=e;return Object.assign({borderRadius:r,color:"#0000",groupTextColor:o,itemColorHover:m,itemColorActive:re(n,{alpha:.1}),itemColorActiveHover:re(n,{alpha:.1}),itemColorActiveCollapsed:re(n,{alpha:.1}),itemTextColor:a,itemTextColorHover:a,itemTextColorActive:n,itemTextColorActiveHover:n,itemTextColorChildActive:n,itemTextColorChildActiveHover:n,itemTextColorHorizontal:a,itemTextColorHoverHorizontal:h,itemTextColorActiveHorizontal:n,itemTextColorActiveHoverHorizontal:n,itemTextColorChildActiveHorizontal:n,itemTextColorChildActiveHoverHorizontal:n,itemIconColor:l,itemIconColorHover:l,itemIconColorActive:n,itemIconColorActiveHover:n,itemIconColorChildActive:n,itemIconColorChildActiveHover:n,itemIconColorCollapsed:l,itemIconColorHorizontal:l,itemIconColorHoverHorizontal:h,itemIconColorActiveHorizontal:n,itemIconColorActiveHoverHorizontal:n,itemIconColorChildActiveHorizontal:n,itemIconColorChildActiveHoverHorizontal:n,itemHeight:"42px",arrowColor:a,arrowColorHover:a,arrowColorActive:n,arrowColorActiveHover:n,arrowColorChildActive:n,arrowColorChildActiveHover:n,colorInverted:"#0000",borderColorHorizontal:"#0000",fontSize:v,dividerColor:g},xo("#BBB",n,"#FFF","#AAA"))}const Io=He({name:"Menu",common:Re,peers:{Tooltip:vo,Dropdown:uo},self:yo}),_e=X("n-layout-sider"),Oe={type:String,default:"static"},zo=s("layout",`
 color: var(--n-text-color);
 background-color: var(--n-color);
 box-sizing: border-box;
 position: relative;
 z-index: auto;
 flex: auto;
 overflow: hidden;
 transition:
 box-shadow .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
`,[s("layout-scroll-container",`
 overflow-x: hidden;
 box-sizing: border-box;
 height: 100%;
 `),w("absolute-positioned",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 `)]),wo={embedded:Boolean,position:Oe,nativeScrollbar:{type:Boolean,default:!0},scrollbarProps:Object,onScroll:Function,contentClass:String,contentStyle:{type:[String,Object],default:""},hasSider:Boolean,siderPlacement:{type:String,default:"left"}},Be=X("n-layout");function Ee(e){return _({name:e?"LayoutContent":"Layout",props:Object.assign(Object.assign({},G.props),wo),setup(r){const o=M(null),n=M(null),{mergedClsPrefixRef:a,inlineThemeDisabled:l}=ve(r),v=G("Layout","-layout",zo,Ne,r,a);function g(z,S){if(r.nativeScrollbar){const{value:P}=o;P&&(S===void 0?P.scrollTo(z):P.scrollTo(z,S))}else{const{value:P}=n;P&&P.scrollTo(z,S)}}q(Be,r);let m=0,h=0;const N=z=>{var S;const P=z.target;m=P.scrollLeft,h=P.scrollTop,(S=r.onScroll)===null||S===void 0||S.call(r,z)};Te(()=>{if(r.nativeScrollbar){const z=o.value;z&&(z.scrollTop=h,z.scrollLeft=m)}});const k={display:"flex",flexWrap:"nowrap",width:"100%",flexDirection:"row"},f={scrollTo:g},T=C(()=>{const{common:{cubicBezierEaseInOut:z},self:S}=v.value;return{"--n-bezier":z,"--n-color":r.embedded?S.colorEmbedded:S.color,"--n-text-color":S.textColor}}),R=l?me("layout",C(()=>r.embedded?"e":""),T,r):void 0;return Object.assign({mergedClsPrefix:a,scrollableElRef:o,scrollbarInstRef:n,hasSiderStyle:k,mergedTheme:v,handleNativeElScroll:N,cssVars:l?void 0:T,themeClass:R==null?void 0:R.themeClass,onRender:R==null?void 0:R.onRender},f)},render(){var r;const{mergedClsPrefix:o,hasSider:n}=this;(r=this.onRender)===null||r===void 0||r.call(this);const a=n?this.hasSiderStyle:void 0,l=[this.themeClass,e&&`${o}-layout-content`,`${o}-layout`,`${o}-layout--${this.position}-positioned`];return c("div",{class:l,style:this.cssVars},this.nativeScrollbar?c("div",{ref:"scrollableElRef",class:[`${o}-layout-scroll-container`,this.contentClass],style:[this.contentStyle,a],onScroll:this.handleNativeElScroll},this.$slots):c(Pe,Object.assign({},this.scrollbarProps,{onScroll:this.onScroll,ref:"scrollbarInstRef",theme:this.mergedTheme.peers.Scrollbar,themeOverrides:this.mergedTheme.peerOverrides.Scrollbar,contentClass:this.contentClass,contentStyle:[this.contentStyle,a]}),this.$slots))}})}const So=Ee(!1),Ao=Ee(!0),Ho=s("layout-sider",`
 flex-shrink: 0;
 box-sizing: border-box;
 position: relative;
 z-index: 1;
 color: var(--n-text-color);
 transition:
 color .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 min-width .3s var(--n-bezier),
 max-width .3s var(--n-bezier),
 transform .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 background-color: var(--n-color);
 display: flex;
 justify-content: flex-end;
`,[w("bordered",[d("border",`
 content: "";
 position: absolute;
 top: 0;
 bottom: 0;
 width: 1px;
 background-color: var(--n-border-color);
 transition: background-color .3s var(--n-bezier);
 `)]),d("left-placement",[w("bordered",[d("border",`
 right: 0;
 `)])]),w("right-placement",`
 justify-content: flex-start;
 `,[w("bordered",[d("border",`
 left: 0;
 `)]),w("collapsed",[s("layout-toggle-button",[s("base-icon",`
 transform: rotate(180deg);
 `)]),s("layout-toggle-bar",[I("&:hover",[d("top",{transform:"rotate(-12deg) scale(1.15) translateY(-2px)"}),d("bottom",{transform:"rotate(12deg) scale(1.15) translateY(2px)"})])])]),s("layout-toggle-button",`
 left: 0;
 transform: translateX(-50%) translateY(-50%);
 `,[s("base-icon",`
 transform: rotate(0);
 `)]),s("layout-toggle-bar",`
 left: -28px;
 transform: rotate(180deg);
 `,[I("&:hover",[d("top",{transform:"rotate(12deg) scale(1.15) translateY(-2px)"}),d("bottom",{transform:"rotate(-12deg) scale(1.15) translateY(2px)"})])])]),w("collapsed",[s("layout-toggle-bar",[I("&:hover",[d("top",{transform:"rotate(-12deg) scale(1.15) translateY(-2px)"}),d("bottom",{transform:"rotate(12deg) scale(1.15) translateY(2px)"})])]),s("layout-toggle-button",[s("base-icon",`
 transform: rotate(0);
 `)])]),s("layout-toggle-button",`
 transition:
 color .3s var(--n-bezier),
 right .3s var(--n-bezier),
 left .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 cursor: pointer;
 width: 24px;
 height: 24px;
 position: absolute;
 top: 50%;
 right: 0;
 border-radius: 50%;
 display: flex;
 align-items: center;
 justify-content: center;
 font-size: 18px;
 color: var(--n-toggle-button-icon-color);
 border: var(--n-toggle-button-border);
 background-color: var(--n-toggle-button-color);
 box-shadow: 0 2px 4px 0px rgba(0, 0, 0, .06);
 transform: translateX(50%) translateY(-50%);
 z-index: 1;
 `,[s("base-icon",`
 transition: transform .3s var(--n-bezier);
 transform: rotate(180deg);
 `)]),s("layout-toggle-bar",`
 cursor: pointer;
 height: 72px;
 width: 32px;
 position: absolute;
 top: calc(50% - 36px);
 right: -28px;
 `,[d("top, bottom",`
 position: absolute;
 width: 4px;
 border-radius: 2px;
 height: 38px;
 left: 14px;
 transition: 
 background-color .3s var(--n-bezier),
 transform .3s var(--n-bezier);
 `),d("bottom",`
 position: absolute;
 top: 34px;
 `),I("&:hover",[d("top",{transform:"rotate(12deg) scale(1.15) translateY(-2px)"}),d("bottom",{transform:"rotate(-12deg) scale(1.15) translateY(2px)"})]),d("top, bottom",{backgroundColor:"var(--n-toggle-bar-color)"}),I("&:hover",[d("top, bottom",{backgroundColor:"var(--n-toggle-bar-color-hover)"})])]),d("border",`
 position: absolute;
 top: 0;
 right: 0;
 bottom: 0;
 width: 1px;
 transition: background-color .3s var(--n-bezier);
 `),s("layout-sider-scroll-container",`
 flex-grow: 1;
 flex-shrink: 0;
 box-sizing: border-box;
 height: 100%;
 opacity: 0;
 transition: opacity .3s var(--n-bezier);
 max-width: 100%;
 `),w("show-content",[s("layout-sider-scroll-container",{opacity:1})]),w("absolute-positioned",`
 position: absolute;
 left: 0;
 top: 0;
 bottom: 0;
 `)]),Ro=_({props:{clsPrefix:{type:String,required:!0},onClick:Function},render(){const{clsPrefix:e}=this;return c("div",{onClick:this.onClick,class:`${e}-layout-toggle-bar`},c("div",{class:`${e}-layout-toggle-bar__top`}),c("div",{class:`${e}-layout-toggle-bar__bottom`}))}}),Po=_({name:"LayoutToggleButton",props:{clsPrefix:{type:String,required:!0},onClick:Function},render(){const{clsPrefix:e}=this;return c("div",{class:`${e}-layout-toggle-button`,onClick:this.onClick},c(ke,{clsPrefix:e},{default:()=>c(mo,null)}))}}),To={position:Oe,bordered:Boolean,collapsedWidth:{type:Number,default:48},width:{type:[Number,String],default:272},contentClass:String,contentStyle:{type:[String,Object],default:""},collapseMode:{type:String,default:"transform"},collapsed:{type:Boolean,default:void 0},defaultCollapsed:Boolean,showCollapsedContent:{type:Boolean,default:!0},showTrigger:{type:[Boolean,String],default:!1},nativeScrollbar:{type:Boolean,default:!0},inverted:Boolean,scrollbarProps:Object,triggerClass:String,triggerStyle:[String,Object],collapsedTriggerClass:String,collapsedTriggerStyle:[String,Object],"onUpdate:collapsed":[Function,Array],onUpdateCollapsed:[Function,Array],onAfterEnter:Function,onAfterLeave:Function,onExpand:[Function,Array],onCollapse:[Function,Array],onScroll:Function},ko=_({name:"LayoutSider",props:Object.assign(Object.assign({},G.props),To),setup(e){const r=j(Be),o=M(null),n=M(null),a=M(e.defaultCollapsed),l=de(oe(e,"collapsed"),a),v=C(()=>le(l.value?e.collapsedWidth:e.width)),g=C(()=>e.collapseMode!=="transform"?{}:{minWidth:le(e.width)}),m=C(()=>r?r.siderPlacement:"left");function h(H,x){if(e.nativeScrollbar){const{value:y}=o;y&&(x===void 0?y.scrollTo(H):y.scrollTo(H,x))}else{const{value:y}=n;y&&y.scrollTo(H,x)}}function N(){const{"onUpdate:collapsed":H,onUpdateCollapsed:x,onExpand:y,onCollapse:L}=e,{value:$}=l;x&&E(x,!$),H&&E(H,!$),a.value=!$,$?y&&E(y):L&&E(L)}let k=0,f=0;const T=H=>{var x;const y=H.target;k=y.scrollLeft,f=y.scrollTop,(x=e.onScroll)===null||x===void 0||x.call(e,H)};Te(()=>{if(e.nativeScrollbar){const H=o.value;H&&(H.scrollTop=f,H.scrollLeft=k)}}),q(_e,{collapsedRef:l,collapseModeRef:oe(e,"collapseMode")});const{mergedClsPrefixRef:R,inlineThemeDisabled:z}=ve(e),S=G("Layout","-layout-sider",Ho,Ne,e,R);function P(H){var x,y;H.propertyName==="max-width"&&(l.value?(x=e.onAfterLeave)===null||x===void 0||x.call(e):(y=e.onAfterEnter)===null||y===void 0||y.call(e))}const Y={scrollTo:h},F=C(()=>{const{common:{cubicBezierEaseInOut:H},self:x}=S.value,{siderToggleButtonColor:y,siderToggleButtonBorder:L,siderToggleBarColor:$,siderToggleBarColorHover:te}=x,O={"--n-bezier":H,"--n-toggle-button-color":y,"--n-toggle-button-border":L,"--n-toggle-bar-color":$,"--n-toggle-bar-color-hover":te};return e.inverted?(O["--n-color"]=x.siderColorInverted,O["--n-text-color"]=x.textColorInverted,O["--n-border-color"]=x.siderBorderColorInverted,O["--n-toggle-button-icon-color"]=x.siderToggleButtonIconColorInverted,O.__invertScrollbar=x.__invertScrollbar):(O["--n-color"]=x.siderColor,O["--n-text-color"]=x.textColor,O["--n-border-color"]=x.siderBorderColor,O["--n-toggle-button-icon-color"]=x.siderToggleButtonIconColor),O}),B=z?me("layout-sider",C(()=>e.inverted?"a":"b"),F,e):void 0;return Object.assign({scrollableElRef:o,scrollbarInstRef:n,mergedClsPrefix:R,mergedTheme:S,styleMaxWidth:v,mergedCollapsed:l,scrollContainerStyle:g,siderPlacement:m,handleNativeElScroll:T,handleTransitionend:P,handleTriggerClick:N,inlineThemeDisabled:z,cssVars:F,themeClass:B==null?void 0:B.themeClass,onRender:B==null?void 0:B.onRender},Y)},render(){var e;const{mergedClsPrefix:r,mergedCollapsed:o,showTrigger:n}=this;return(e=this.onRender)===null||e===void 0||e.call(this),c("aside",{class:[`${r}-layout-sider`,this.themeClass,`${r}-layout-sider--${this.position}-positioned`,`${r}-layout-sider--${this.siderPlacement}-placement`,this.bordered&&`${r}-layout-sider--bordered`,o&&`${r}-layout-sider--collapsed`,(!o||this.showCollapsedContent)&&`${r}-layout-sider--show-content`],onTransitionend:this.handleTransitionend,style:[this.inlineThemeDisabled?void 0:this.cssVars,{maxWidth:this.styleMaxWidth,width:le(this.width)}]},this.nativeScrollbar?c("div",{class:[`${r}-layout-sider-scroll-container`,this.contentClass],onScroll:this.handleNativeElScroll,style:[this.scrollContainerStyle,{overflow:"auto"},this.contentStyle],ref:"scrollableElRef"},this.$slots):c(Pe,Object.assign({},this.scrollbarProps,{onScroll:this.onScroll,ref:"scrollbarInstRef",style:this.scrollContainerStyle,contentStyle:this.contentStyle,contentClass:this.contentClass,theme:this.mergedTheme.peers.Scrollbar,themeOverrides:this.mergedTheme.peerOverrides.Scrollbar,builtinThemeOverrides:this.inverted&&this.cssVars.__invertScrollbar==="true"?{colorHover:"rgba(255, 255, 255, .4)",color:"rgba(255, 255, 255, .3)"}:void 0}),this.$slots),n?n==="bar"?c(Ro,{clsPrefix:r,class:o?this.collapsedTriggerClass:this.triggerClass,style:o?this.collapsedTriggerStyle:this.triggerStyle,onClick:this.handleTriggerClick}):c(Po,{clsPrefix:r,class:o?this.collapsedTriggerClass:this.triggerClass,style:o?this.collapsedTriggerStyle:this.triggerStyle,onClick:this.handleTriggerClick}):null,this.bordered?c("div",{class:`${r}-layout-sider__border`}):null)}}),Z=X("n-menu"),Me=X("n-submenu"),ge=X("n-menu-item-group"),Se=[I("&::before","background-color: var(--n-item-color-hover);"),d("arrow",`
 color: var(--n-arrow-color-hover);
 `),d("icon",`
 color: var(--n-item-icon-color-hover);
 `),s("menu-item-content-header",`
 color: var(--n-item-text-color-hover);
 `,[I("a",`
 color: var(--n-item-text-color-hover);
 `),d("extra",`
 color: var(--n-item-text-color-hover);
 `)])],Ae=[d("icon",`
 color: var(--n-item-icon-color-hover-horizontal);
 `),s("menu-item-content-header",`
 color: var(--n-item-text-color-hover-horizontal);
 `,[I("a",`
 color: var(--n-item-text-color-hover-horizontal);
 `),d("extra",`
 color: var(--n-item-text-color-hover-horizontal);
 `)])],No=I([s("menu",`
 background-color: var(--n-color);
 color: var(--n-item-text-color);
 overflow: hidden;
 transition: background-color .3s var(--n-bezier);
 box-sizing: border-box;
 font-size: var(--n-font-size);
 padding-bottom: 6px;
 `,[w("horizontal",`
 max-width: 100%;
 width: 100%;
 display: flex;
 overflow: hidden;
 padding-bottom: 0;
 `,[s("submenu","margin: 0;"),s("menu-item","margin: 0;"),s("menu-item-content",`
 padding: 0 20px;
 border-bottom: 2px solid #0000;
 `,[I("&::before","display: none;"),w("selected","border-bottom: 2px solid var(--n-border-color-horizontal)")]),s("menu-item-content",[w("selected",[d("icon","color: var(--n-item-icon-color-active-horizontal);"),s("menu-item-content-header",`
 color: var(--n-item-text-color-active-horizontal);
 `,[I("a","color: var(--n-item-text-color-active-horizontal);"),d("extra","color: var(--n-item-text-color-active-horizontal);")])]),w("child-active",`
 border-bottom: 2px solid var(--n-border-color-horizontal);
 `,[s("menu-item-content-header",`
 color: var(--n-item-text-color-child-active-horizontal);
 `,[I("a",`
 color: var(--n-item-text-color-child-active-horizontal);
 `),d("extra",`
 color: var(--n-item-text-color-child-active-horizontal);
 `)]),d("icon",`
 color: var(--n-item-icon-color-child-active-horizontal);
 `)]),W("disabled",[W("selected, child-active",[I("&:focus-within",Ae)]),w("selected",[K(null,[d("icon","color: var(--n-item-icon-color-active-hover-horizontal);"),s("menu-item-content-header",`
 color: var(--n-item-text-color-active-hover-horizontal);
 `,[I("a","color: var(--n-item-text-color-active-hover-horizontal);"),d("extra","color: var(--n-item-text-color-active-hover-horizontal);")])])]),w("child-active",[K(null,[d("icon","color: var(--n-item-icon-color-child-active-hover-horizontal);"),s("menu-item-content-header",`
 color: var(--n-item-text-color-child-active-hover-horizontal);
 `,[I("a","color: var(--n-item-text-color-child-active-hover-horizontal);"),d("extra","color: var(--n-item-text-color-child-active-hover-horizontal);")])])]),K("border-bottom: 2px solid var(--n-border-color-horizontal);",Ae)]),s("menu-item-content-header",[I("a","color: var(--n-item-text-color-horizontal);")])])]),W("responsive",[s("menu-item-content-header",`
 overflow: hidden;
 text-overflow: ellipsis;
 `)]),w("collapsed",[s("menu-item-content",[w("selected",[I("&::before",`
 background-color: var(--n-item-color-active-collapsed) !important;
 `)]),s("menu-item-content-header","opacity: 0;"),d("arrow","opacity: 0;"),d("icon","color: var(--n-item-icon-color-collapsed);")])]),s("menu-item",`
 height: var(--n-item-height);
 margin-top: 6px;
 position: relative;
 `),s("menu-item-content",`
 box-sizing: border-box;
 line-height: 1.75;
 height: 100%;
 display: grid;
 grid-template-areas: "icon content arrow";
 grid-template-columns: auto 1fr auto;
 align-items: center;
 cursor: pointer;
 position: relative;
 padding-right: 18px;
 transition:
 background-color .3s var(--n-bezier),
 padding-left .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[I("> *","z-index: 1;"),I("&::before",`
 z-index: auto;
 content: "";
 background-color: #0000;
 position: absolute;
 left: 8px;
 right: 8px;
 top: 0;
 bottom: 0;
 pointer-events: none;
 border-radius: var(--n-border-radius);
 transition: background-color .3s var(--n-bezier);
 `),w("disabled",`
 opacity: .45;
 cursor: not-allowed;
 `),w("collapsed",[d("arrow","transform: rotate(0);")]),w("selected",[I("&::before","background-color: var(--n-item-color-active);"),d("arrow","color: var(--n-arrow-color-active);"),d("icon","color: var(--n-item-icon-color-active);"),s("menu-item-content-header",`
 color: var(--n-item-text-color-active);
 `,[I("a","color: var(--n-item-text-color-active);"),d("extra","color: var(--n-item-text-color-active);")])]),w("child-active",[s("menu-item-content-header",`
 color: var(--n-item-text-color-child-active);
 `,[I("a",`
 color: var(--n-item-text-color-child-active);
 `),d("extra",`
 color: var(--n-item-text-color-child-active);
 `)]),d("arrow",`
 color: var(--n-arrow-color-child-active);
 `),d("icon",`
 color: var(--n-item-icon-color-child-active);
 `)]),W("disabled",[W("selected, child-active",[I("&:focus-within",Se)]),w("selected",[K(null,[d("arrow","color: var(--n-arrow-color-active-hover);"),d("icon","color: var(--n-item-icon-color-active-hover);"),s("menu-item-content-header",`
 color: var(--n-item-text-color-active-hover);
 `,[I("a","color: var(--n-item-text-color-active-hover);"),d("extra","color: var(--n-item-text-color-active-hover);")])])]),w("child-active",[K(null,[d("arrow","color: var(--n-arrow-color-child-active-hover);"),d("icon","color: var(--n-item-icon-color-child-active-hover);"),s("menu-item-content-header",`
 color: var(--n-item-text-color-child-active-hover);
 `,[I("a","color: var(--n-item-text-color-child-active-hover);"),d("extra","color: var(--n-item-text-color-child-active-hover);")])])]),w("selected",[K(null,[I("&::before","background-color: var(--n-item-color-active-hover);")])]),K(null,Se)]),d("icon",`
 grid-area: icon;
 color: var(--n-item-icon-color);
 transition:
 color .3s var(--n-bezier),
 font-size .3s var(--n-bezier),
 margin-right .3s var(--n-bezier);
 box-sizing: content-box;
 display: inline-flex;
 align-items: center;
 justify-content: center;
 `),d("arrow",`
 grid-area: arrow;
 font-size: 16px;
 color: var(--n-arrow-color);
 transform: rotate(180deg);
 opacity: 1;
 transition:
 color .3s var(--n-bezier),
 transform 0.2s var(--n-bezier),
 opacity 0.2s var(--n-bezier);
 `),s("menu-item-content-header",`
 grid-area: content;
 transition:
 color .3s var(--n-bezier),
 opacity .3s var(--n-bezier);
 opacity: 1;
 white-space: nowrap;
 color: var(--n-item-text-color);
 `,[I("a",`
 outline: none;
 text-decoration: none;
 transition: color .3s var(--n-bezier);
 color: var(--n-item-text-color);
 `,[I("&::before",`
 content: "";
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 `)]),d("extra",`
 font-size: .93em;
 color: var(--n-group-text-color);
 transition: color .3s var(--n-bezier);
 `)])]),s("submenu",`
 cursor: pointer;
 position: relative;
 margin-top: 6px;
 `,[s("menu-item-content",`
 height: var(--n-item-height);
 `),s("submenu-children",`
 overflow: hidden;
 padding: 0;
 `,[Je({duration:".2s"})])]),s("menu-item-group",[s("menu-item-group-title",`
 margin-top: 6px;
 color: var(--n-group-text-color);
 cursor: default;
 font-size: .93em;
 height: 36px;
 display: flex;
 align-items: center;
 transition:
 padding-left .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `)])]),s("menu-tooltip",[I("a",`
 color: inherit;
 text-decoration: none;
 `)]),s("menu-divider",`
 transition: background-color .3s var(--n-bezier);
 background-color: var(--n-divider-color);
 height: 1px;
 margin: 6px 18px;
 `)]);function K(e,r){return[w("hover",e,r),I("&:hover",e,r)]}const $e=_({name:"MenuOptionContent",props:{collapsed:Boolean,disabled:Boolean,title:[String,Function],icon:Function,extra:[String,Function],showArrow:Boolean,childActive:Boolean,hover:Boolean,paddingLeft:Number,selected:Boolean,maxIconSize:{type:Number,required:!0},activeIconSize:{type:Number,required:!0},iconMarginRight:{type:Number,required:!0},clsPrefix:{type:String,required:!0},onClick:Function,tmNode:{type:Object,required:!0},isEllipsisPlaceholder:Boolean},setup(e){const{props:r}=j(Z);return{menuProps:r,style:C(()=>{const{paddingLeft:o}=e;return{paddingLeft:o&&`${o}px`}}),iconStyle:C(()=>{const{maxIconSize:o,activeIconSize:n,iconMarginRight:a}=e;return{width:`${o}px`,height:`${o}px`,fontSize:`${n}px`,marginRight:`${a}px`}})}},render(){const{clsPrefix:e,tmNode:r,menuProps:{renderIcon:o,renderLabel:n,renderExtra:a,expandIcon:l}}=this,v=o?o(r.rawNode):U(this.icon);return c("div",{onClick:g=>{var m;(m=this.onClick)===null||m===void 0||m.call(this,g)},role:"none",class:[`${e}-menu-item-content`,{[`${e}-menu-item-content--selected`]:this.selected,[`${e}-menu-item-content--collapsed`]:this.collapsed,[`${e}-menu-item-content--child-active`]:this.childActive,[`${e}-menu-item-content--disabled`]:this.disabled,[`${e}-menu-item-content--hover`]:this.hover}],style:this.style},v&&c("div",{class:`${e}-menu-item-content__icon`,style:this.iconStyle,role:"none"},[v]),c("div",{class:`${e}-menu-item-content-header`,role:"none"},this.isEllipsisPlaceholder?this.title:n?n(r.rawNode):U(this.title),this.extra||a?c("span",{class:`${e}-menu-item-content-header__extra`}," ",a?a(r.rawNode):U(this.extra)):null),this.showArrow?c(ke,{ariaHidden:!0,class:`${e}-menu-item-content__arrow`,clsPrefix:e},{default:()=>l?l(r.rawNode):c(Co,null)}):null)}}),ee=8;function Ce(e){const r=j(Z),{props:o,mergedCollapsedRef:n}=r,a=j(Me,null),l=j(ge,null),v=C(()=>o.mode==="horizontal"),g=C(()=>v.value?o.dropdownPlacement:"tmNodes"in e?"right-start":"right"),m=C(()=>{var f;return Math.max((f=o.collapsedIconSize)!==null&&f!==void 0?f:o.iconSize,o.iconSize)}),h=C(()=>{var f;return!v.value&&e.root&&n.value&&(f=o.collapsedIconSize)!==null&&f!==void 0?f:o.iconSize}),N=C(()=>{if(v.value)return;const{collapsedWidth:f,indent:T,rootIndent:R}=o,{root:z,isGroup:S}=e,P=R===void 0?T:R;return z?n.value?f/2-m.value/2:P:l&&typeof l.paddingLeftRef.value=="number"?T/2+l.paddingLeftRef.value:a&&typeof a.paddingLeftRef.value=="number"?(S?T/2:T)+a.paddingLeftRef.value:0}),k=C(()=>{const{collapsedWidth:f,indent:T,rootIndent:R}=o,{value:z}=m,{root:S}=e;return v.value||!S||!n.value?ee:(R===void 0?T:R)+z+ee-(f+z)/2});return{dropdownPlacement:g,activeIconSize:h,maxIconSize:m,paddingLeft:N,iconMarginRight:k,NMenu:r,NSubmenu:a,NMenuOptionGroup:l}}const be={internalKey:{type:[String,Number],required:!0},root:Boolean,isGroup:Boolean,level:{type:Number,required:!0},title:[String,Function],extra:[String,Function]},_o=_({name:"MenuDivider",setup(){const e=j(Z),{mergedClsPrefixRef:r,isHorizontalRef:o}=e;return()=>o.value?null:c("div",{class:`${r.value}-menu-divider`})}}),Fe=Object.assign(Object.assign({},be),{tmNode:{type:Object,required:!0},disabled:Boolean,icon:Function,onClick:Function}),Oo=he(Fe),Bo=_({name:"MenuOption",props:Fe,setup(e){const r=Ce(e),{NSubmenu:o,NMenu:n,NMenuOptionGroup:a}=r,{props:l,mergedClsPrefixRef:v,mergedCollapsedRef:g}=n,m=o?o.mergedDisabledRef:a?a.mergedDisabledRef:{value:!1},h=C(()=>m.value||e.disabled);function N(f){const{onClick:T}=e;T&&T(f)}function k(f){h.value||(n.doSelect(e.internalKey,e.tmNode.rawNode),N(f))}return{mergedClsPrefix:v,dropdownPlacement:r.dropdownPlacement,paddingLeft:r.paddingLeft,iconMarginRight:r.iconMarginRight,maxIconSize:r.maxIconSize,activeIconSize:r.activeIconSize,mergedTheme:n.mergedThemeRef,menuProps:l,dropdownEnabled:ce(()=>e.root&&g.value&&l.mode!=="horizontal"&&!h.value),selected:ce(()=>n.mergedValueRef.value===e.internalKey),mergedDisabled:h,handleClick:k}},render(){const{mergedClsPrefix:e,mergedTheme:r,tmNode:o,menuProps:{renderLabel:n,nodeProps:a}}=this,l=a==null?void 0:a(o.rawNode);return c("div",Object.assign({},l,{role:"menuitem",class:[`${e}-menu-item`,l==null?void 0:l.class]}),c(ho,{theme:r.peers.Tooltip,themeOverrides:r.peerOverrides.Tooltip,trigger:"hover",placement:this.dropdownPlacement,disabled:!this.dropdownEnabled||this.title===void 0,internalExtraClass:["menu-tooltip"]},{default:()=>n?n(o.rawNode):U(this.title),trigger:()=>c($e,{tmNode:o,clsPrefix:e,paddingLeft:this.paddingLeft,iconMarginRight:this.iconMarginRight,maxIconSize:this.maxIconSize,activeIconSize:this.activeIconSize,selected:this.selected,title:this.title,extra:this.extra,disabled:this.mergedDisabled,icon:this.icon,onClick:this.handleClick})}))}}),Le=Object.assign(Object.assign({},be),{tmNode:{type:Object,required:!0},tmNodes:{type:Array,required:!0}}),Eo=he(Le),Mo=_({name:"MenuOptionGroup",props:Le,setup(e){const r=Ce(e),{NSubmenu:o}=r,n=C(()=>o!=null&&o.mergedDisabledRef.value?!0:e.tmNode.disabled);q(ge,{paddingLeftRef:r.paddingLeft,mergedDisabledRef:n});const{mergedClsPrefixRef:a,props:l}=j(Z);return function(){const{value:v}=a,g=r.paddingLeft.value,{nodeProps:m}=l,h=m==null?void 0:m(e.tmNode.rawNode);return c("div",{class:`${v}-menu-item-group`,role:"group"},c("div",Object.assign({},h,{class:[`${v}-menu-item-group-title`,h==null?void 0:h.class],style:[(h==null?void 0:h.style)||"",g!==void 0?`padding-left: ${g}px;`:""]}),U(e.title),e.extra?c(eo,null," ",U(e.extra)):null),c("div",null,e.tmNodes.map(N=>xe(N,l))))}}});function se(e){return e.type==="divider"||e.type==="render"}function $o(e){return e.type==="divider"}function xe(e,r){const{rawNode:o}=e,{show:n}=o;if(n===!1)return null;if(se(o))return $o(o)?c(_o,Object.assign({key:e.key},o.props)):null;const{labelField:a}=r,{key:l,level:v,isGroup:g}=e,m=Object.assign(Object.assign({},o),{title:o.title||o[a],extra:o.titleExtra||o.extra,key:l,internalKey:l,level:v,root:v===0,isGroup:g});return e.children?e.isGroup?c(Mo,ne(m,Eo,{tmNode:e,tmNodes:e.children,key:l})):c(ue,ne(m,Fo,{key:l,rawNodes:o[r.childrenField],tmNodes:e.children,tmNode:e})):c(Bo,ne(m,Oo,{key:l,tmNode:e}))}const je=Object.assign(Object.assign({},be),{rawNodes:{type:Array,default:()=>[]},tmNodes:{type:Array,default:()=>[]},tmNode:{type:Object,required:!0},disabled:Boolean,icon:Function,onClick:Function,domId:String,virtualChildActive:{type:Boolean,default:void 0},isEllipsisPlaceholder:Boolean}),Fo=he(je),ue=_({name:"Submenu",props:je,setup(e){const r=Ce(e),{NMenu:o,NSubmenu:n}=r,{props:a,mergedCollapsedRef:l,mergedThemeRef:v}=o,g=C(()=>{const{disabled:f}=e;return n!=null&&n.mergedDisabledRef.value||a.disabled?!0:f}),m=M(!1);q(Me,{paddingLeftRef:r.paddingLeft,mergedDisabledRef:g}),q(ge,null);function h(){const{onClick:f}=e;f&&f()}function N(){g.value||(l.value||o.toggleExpand(e.internalKey),h())}function k(f){m.value=f}return{menuProps:a,mergedTheme:v,doSelect:o.doSelect,inverted:o.invertedRef,isHorizontal:o.isHorizontalRef,mergedClsPrefix:o.mergedClsPrefixRef,maxIconSize:r.maxIconSize,activeIconSize:r.activeIconSize,iconMarginRight:r.iconMarginRight,dropdownPlacement:r.dropdownPlacement,dropdownShow:m,paddingLeft:r.paddingLeft,mergedDisabled:g,mergedValue:o.mergedValueRef,childActive:ce(()=>{var f;return(f=e.virtualChildActive)!==null&&f!==void 0?f:o.activePathRef.value.includes(e.internalKey)}),collapsed:C(()=>a.mode==="horizontal"?!1:l.value?!0:!o.mergedExpandedKeysRef.value.includes(e.internalKey)),dropdownEnabled:C(()=>!g.value&&(a.mode==="horizontal"||l.value)),handlePopoverShowChange:k,handleClick:N}},render(){var e;const{mergedClsPrefix:r,menuProps:{renderIcon:o,renderLabel:n}}=this,a=()=>{const{isHorizontal:v,paddingLeft:g,collapsed:m,mergedDisabled:h,maxIconSize:N,activeIconSize:k,title:f,childActive:T,icon:R,handleClick:z,menuProps:{nodeProps:S},dropdownShow:P,iconMarginRight:Y,tmNode:F,mergedClsPrefix:B,isEllipsisPlaceholder:H,extra:x}=this,y=S==null?void 0:S(F.rawNode);return c("div",Object.assign({},y,{class:[`${B}-menu-item`,y==null?void 0:y.class],role:"menuitem"}),c($e,{tmNode:F,paddingLeft:g,collapsed:m,disabled:h,iconMarginRight:Y,maxIconSize:N,activeIconSize:k,title:f,extra:x,showArrow:!v,childActive:T,clsPrefix:B,icon:R,hover:P,onClick:z,isEllipsisPlaceholder:H}))},l=()=>c(oo,null,{default:()=>{const{tmNodes:v,collapsed:g}=this;return g?null:c("div",{class:`${r}-submenu-children`,role:"menu"},v.map(m=>xe(m,this.menuProps)))}});return this.root?c(fo,Object.assign({size:"large",trigger:"hover"},(e=this.menuProps)===null||e===void 0?void 0:e.dropdownProps,{themeOverrides:this.mergedTheme.peerOverrides.Dropdown,theme:this.mergedTheme.peers.Dropdown,builtinThemeOverrides:{fontSizeLarge:"14px",optionIconSizeLarge:"18px"},value:this.mergedValue,disabled:!this.dropdownEnabled,placement:this.dropdownPlacement,keyField:this.menuProps.keyField,labelField:this.menuProps.labelField,childrenField:this.menuProps.childrenField,onUpdateShow:this.handlePopoverShowChange,options:this.rawNodes,onSelect:this.doSelect,inverted:this.inverted,renderIcon:o,renderLabel:n}),{default:()=>c("div",{class:`${r}-submenu`,role:"menu","aria-expanded":!this.collapsed,id:this.domId},a(),this.isHorizontal?null:l())}):c("div",{class:`${r}-submenu`,role:"menu","aria-expanded":!this.collapsed,id:this.domId},a(),l())}}),Lo=Object.assign(Object.assign({},G.props),{options:{type:Array,default:()=>[]},collapsed:{type:Boolean,default:void 0},collapsedWidth:{type:Number,default:48},iconSize:{type:Number,default:20},collapsedIconSize:{type:Number,default:24},rootIndent:Number,indent:{type:Number,default:32},labelField:{type:String,default:"label"},keyField:{type:String,default:"key"},childrenField:{type:String,default:"children"},disabledField:{type:String,default:"disabled"},defaultExpandAll:Boolean,defaultExpandedKeys:Array,expandedKeys:Array,value:[String,Number],defaultValue:{type:[String,Number],default:null},mode:{type:String,default:"vertical"},watchProps:{type:Array,default:void 0},disabled:Boolean,show:{type:Boolean,default:!0},inverted:Boolean,"onUpdate:expandedKeys":[Function,Array],onUpdateExpandedKeys:[Function,Array],onUpdateValue:[Function,Array],"onUpdate:value":[Function,Array],expandIcon:Function,renderIcon:Function,renderLabel:Function,renderExtra:Function,dropdownProps:Object,accordion:Boolean,nodeProps:Function,dropdownPlacement:{type:String,default:"bottom"},responsive:Boolean,items:Array,onOpenNamesChange:[Function,Array],onSelect:[Function,Array],onExpandedNamesChange:[Function,Array],expandedNames:Array,defaultExpandedNames:Array}),jo=_({name:"Menu",inheritAttrs:!1,props:Lo,setup(e){const{mergedClsPrefixRef:r,inlineThemeDisabled:o}=ve(e),n=G("Menu","-menu",No,Io,e,r),a=j(_e,null),l=C(()=>{var u;const{collapsed:b}=e;if(b!==void 0)return b;if(a){const{collapseModeRef:t,collapsedRef:p}=a;if(t.value==="width")return(u=p.value)!==null&&u!==void 0?u:!1}return!1}),v=C(()=>{const{keyField:u,childrenField:b,disabledField:t}=e;return ae(e.items||e.options,{getIgnored(p){return se(p)},getChildren(p){return p[b]},getDisabled(p){return p[t]},getKey(p){var A;return(A=p[u])!==null&&A!==void 0?A:p.name}})}),g=C(()=>new Set(v.value.treeNodes.map(u=>u.key))),{watchProps:m}=e,h=M(null);m!=null&&m.includes("defaultValue")?ze(()=>{h.value=e.defaultValue}):h.value=e.defaultValue;const N=oe(e,"value"),k=de(N,h),f=M([]),T=()=>{f.value=e.defaultExpandAll?v.value.getNonLeafKeys():e.defaultExpandedNames||e.defaultExpandedKeys||v.value.getPath(k.value,{includeSelf:!1}).keyPath};m!=null&&m.includes("defaultExpandedKeys")?ze(T):T();const R=go(e,["expandedNames","expandedKeys"]),z=de(R,f),S=C(()=>v.value.treeNodes),P=C(()=>v.value.getPath(k.value).keyPath);q(Z,{props:e,mergedCollapsedRef:l,mergedThemeRef:n,mergedValueRef:k,mergedExpandedKeysRef:z,activePathRef:P,mergedClsPrefixRef:r,isHorizontalRef:C(()=>e.mode==="horizontal"),invertedRef:oe(e,"inverted"),doSelect:Y,toggleExpand:B});function Y(u,b){const{"onUpdate:value":t,onUpdateValue:p,onSelect:A}=e;p&&E(p,u,b),t&&E(t,u,b),A&&E(A,u,b),h.value=u}function F(u){const{"onUpdate:expandedKeys":b,onUpdateExpandedKeys:t,onExpandedNamesChange:p,onOpenNamesChange:A}=e;b&&E(b,u),t&&E(t,u),p&&E(p,u),A&&E(A,u),f.value=u}function B(u){const b=Array.from(z.value),t=b.findIndex(p=>p===u);if(~t)b.splice(t,1);else{if(e.accordion&&g.value.has(u)){const p=b.findIndex(A=>g.value.has(A));p>-1&&b.splice(p,1)}b.push(u)}F(b)}const H=u=>{const b=v.value.getPath(u??k.value,{includeSelf:!1}).keyPath;if(!b.length)return;const t=Array.from(z.value),p=new Set([...t,...b]);e.accordion&&g.value.forEach(A=>{p.has(A)&&!b.includes(A)&&p.delete(A)}),F(Array.from(p))},x=C(()=>{const{inverted:u}=e,{common:{cubicBezierEaseInOut:b},self:t}=n.value,{borderRadius:p,borderColorHorizontal:A,fontSize:We,itemHeight:Xe,dividerColor:Ze}=t,i={"--n-divider-color":Ze,"--n-bezier":b,"--n-font-size":We,"--n-border-color-horizontal":A,"--n-border-radius":p,"--n-item-height":Xe};return u?(i["--n-group-text-color"]=t.groupTextColorInverted,i["--n-color"]=t.colorInverted,i["--n-item-text-color"]=t.itemTextColorInverted,i["--n-item-text-color-hover"]=t.itemTextColorHoverInverted,i["--n-item-text-color-active"]=t.itemTextColorActiveInverted,i["--n-item-text-color-child-active"]=t.itemTextColorChildActiveInverted,i["--n-item-text-color-child-active-hover"]=t.itemTextColorChildActiveInverted,i["--n-item-text-color-active-hover"]=t.itemTextColorActiveHoverInverted,i["--n-item-icon-color"]=t.itemIconColorInverted,i["--n-item-icon-color-hover"]=t.itemIconColorHoverInverted,i["--n-item-icon-color-active"]=t.itemIconColorActiveInverted,i["--n-item-icon-color-active-hover"]=t.itemIconColorActiveHoverInverted,i["--n-item-icon-color-child-active"]=t.itemIconColorChildActiveInverted,i["--n-item-icon-color-child-active-hover"]=t.itemIconColorChildActiveHoverInverted,i["--n-item-icon-color-collapsed"]=t.itemIconColorCollapsedInverted,i["--n-item-text-color-horizontal"]=t.itemTextColorHorizontalInverted,i["--n-item-text-color-hover-horizontal"]=t.itemTextColorHoverHorizontalInverted,i["--n-item-text-color-active-horizontal"]=t.itemTextColorActiveHorizontalInverted,i["--n-item-text-color-child-active-horizontal"]=t.itemTextColorChildActiveHorizontalInverted,i["--n-item-text-color-child-active-hover-horizontal"]=t.itemTextColorChildActiveHoverHorizontalInverted,i["--n-item-text-color-active-hover-horizontal"]=t.itemTextColorActiveHoverHorizontalInverted,i["--n-item-icon-color-horizontal"]=t.itemIconColorHorizontalInverted,i["--n-item-icon-color-hover-horizontal"]=t.itemIconColorHoverHorizontalInverted,i["--n-item-icon-color-active-horizontal"]=t.itemIconColorActiveHorizontalInverted,i["--n-item-icon-color-active-hover-horizontal"]=t.itemIconColorActiveHoverHorizontalInverted,i["--n-item-icon-color-child-active-horizontal"]=t.itemIconColorChildActiveHorizontalInverted,i["--n-item-icon-color-child-active-hover-horizontal"]=t.itemIconColorChildActiveHoverHorizontalInverted,i["--n-arrow-color"]=t.arrowColorInverted,i["--n-arrow-color-hover"]=t.arrowColorHoverInverted,i["--n-arrow-color-active"]=t.arrowColorActiveInverted,i["--n-arrow-color-active-hover"]=t.arrowColorActiveHoverInverted,i["--n-arrow-color-child-active"]=t.arrowColorChildActiveInverted,i["--n-arrow-color-child-active-hover"]=t.arrowColorChildActiveHoverInverted,i["--n-item-color-hover"]=t.itemColorHoverInverted,i["--n-item-color-active"]=t.itemColorActiveInverted,i["--n-item-color-active-hover"]=t.itemColorActiveHoverInverted,i["--n-item-color-active-collapsed"]=t.itemColorActiveCollapsedInverted):(i["--n-group-text-color"]=t.groupTextColor,i["--n-color"]=t.color,i["--n-item-text-color"]=t.itemTextColor,i["--n-item-text-color-hover"]=t.itemTextColorHover,i["--n-item-text-color-active"]=t.itemTextColorActive,i["--n-item-text-color-child-active"]=t.itemTextColorChildActive,i["--n-item-text-color-child-active-hover"]=t.itemTextColorChildActiveHover,i["--n-item-text-color-active-hover"]=t.itemTextColorActiveHover,i["--n-item-icon-color"]=t.itemIconColor,i["--n-item-icon-color-hover"]=t.itemIconColorHover,i["--n-item-icon-color-active"]=t.itemIconColorActive,i["--n-item-icon-color-active-hover"]=t.itemIconColorActiveHover,i["--n-item-icon-color-child-active"]=t.itemIconColorChildActive,i["--n-item-icon-color-child-active-hover"]=t.itemIconColorChildActiveHover,i["--n-item-icon-color-collapsed"]=t.itemIconColorCollapsed,i["--n-item-text-color-horizontal"]=t.itemTextColorHorizontal,i["--n-item-text-color-hover-horizontal"]=t.itemTextColorHoverHorizontal,i["--n-item-text-color-active-horizontal"]=t.itemTextColorActiveHorizontal,i["--n-item-text-color-child-active-horizontal"]=t.itemTextColorChildActiveHorizontal,i["--n-item-text-color-child-active-hover-horizontal"]=t.itemTextColorChildActiveHoverHorizontal,i["--n-item-text-color-active-hover-horizontal"]=t.itemTextColorActiveHoverHorizontal,i["--n-item-icon-color-horizontal"]=t.itemIconColorHorizontal,i["--n-item-icon-color-hover-horizontal"]=t.itemIconColorHoverHorizontal,i["--n-item-icon-color-active-horizontal"]=t.itemIconColorActiveHorizontal,i["--n-item-icon-color-active-hover-horizontal"]=t.itemIconColorActiveHoverHorizontal,i["--n-item-icon-color-child-active-horizontal"]=t.itemIconColorChildActiveHorizontal,i["--n-item-icon-color-child-active-hover-horizontal"]=t.itemIconColorChildActiveHoverHorizontal,i["--n-arrow-color"]=t.arrowColor,i["--n-arrow-color-hover"]=t.arrowColorHover,i["--n-arrow-color-active"]=t.arrowColorActive,i["--n-arrow-color-active-hover"]=t.arrowColorActiveHover,i["--n-arrow-color-child-active"]=t.arrowColorChildActive,i["--n-arrow-color-child-active-hover"]=t.arrowColorChildActiveHover,i["--n-item-color-hover"]=t.itemColorHover,i["--n-item-color-active"]=t.itemColorActive,i["--n-item-color-active-hover"]=t.itemColorActiveHover,i["--n-item-color-active-collapsed"]=t.itemColorActiveCollapsed),i}),y=o?me("menu",C(()=>e.inverted?"a":"b"),x,e):void 0,L=ro(),$=M(null),te=M(null);let O=!0;const ye=()=>{var u;O?O=!1:(u=$.value)===null||u===void 0||u.sync({showAllItemsBeforeCalculate:!0})};function Ke(){return document.getElementById(L)}const Q=M(-1);function Ve(u){Q.value=e.options.length-u}function De(u){u||(Q.value=-1)}const Ue=C(()=>{const u=Q.value;return{children:u===-1?[]:e.options.slice(u)}}),Ge=C(()=>{const{childrenField:u,disabledField:b,keyField:t}=e;return ae([Ue.value],{getIgnored(p){return se(p)},getChildren(p){return p[u]},getDisabled(p){return p[b]},getKey(p){var A;return(A=p[t])!==null&&A!==void 0?A:p.name}})}),qe=C(()=>ae([{}]).treeNodes[0]);function Ye(){var u;if(Q.value===-1)return c(ue,{root:!0,level:0,key:"__ellpisisGroupPlaceholder__",internalKey:"__ellpisisGroupPlaceholder__",title:"···",tmNode:qe.value,domId:L,isEllipsisPlaceholder:!0});const b=Ge.value.treeNodes[0],t=P.value,p=!!(!((u=b.children)===null||u===void 0)&&u.some(A=>t.includes(A.key)));return c(ue,{level:0,root:!0,key:"__ellpisisGroup__",internalKey:"__ellpisisGroup__",title:"···",virtualChildActive:p,tmNode:b,domId:L,rawNodes:b.rawNode.children||[],tmNodes:b.children||[],isEllipsisPlaceholder:!0})}return{mergedClsPrefix:r,controlledExpandedKeys:R,uncontrolledExpanededKeys:f,mergedExpandedKeys:z,uncontrolledValue:h,mergedValue:k,activePath:P,tmNodes:S,mergedTheme:n,mergedCollapsed:l,cssVars:o?void 0:x,themeClass:y==null?void 0:y.themeClass,overflowRef:$,counterRef:te,updateCounter:()=>{},onResize:ye,onUpdateOverflow:De,onUpdateCount:Ve,renderCounter:Ye,getCounter:Ke,onRender:y==null?void 0:y.onRender,showOption:H,deriveResponsiveState:ye}},render(){const{mergedClsPrefix:e,mode:r,themeClass:o,onRender:n}=this;n==null||n();const a=()=>this.tmNodes.map(m=>xe(m,this.$props)),v=r==="horizontal"&&this.responsive,g=()=>c("div",no(this.$attrs,{role:r==="horizontal"?"menubar":"menu",class:[`${e}-menu`,o,`${e}-menu--${r}`,v&&`${e}-menu--responsive`,this.mergedCollapsed&&`${e}-menu--collapsed`],style:this.cssVars}),v?c(po,{ref:"overflowRef",onUpdateOverflow:this.onUpdateOverflow,getCounter:this.getCounter,onUpdateCount:this.onUpdateCount,updateCounter:this.updateCounter,style:{width:"100%",display:"flex",overflow:"hidden"}},{default:a,counter:this.renderCounter}):a());return v?c(to,{onResize:this.onResize},{default:g}):g()}}),Ko={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Vo=V("path",{d:"M402 168c-2.93 40.67-33.1 72-66 72s-63.12-31.32-66-72c-3-42.31 26.37-72 66-72s69 30.46 66 72z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),Do=V("path",{d:"M336 304c-65.17 0-127.84 32.37-143.54 95.41c-2.08 8.34 3.15 16.59 11.72 16.59h263.65c8.57 0 13.77-8.25 11.72-16.59C463.85 335.36 401.18 304 336 304z",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"},null,-1),Uo=V("path",{d:"M200 185.94c-2.34 32.48-26.72 58.06-53 58.06s-50.7-25.57-53-58.06C91.61 152.15 115.34 128 147 128s55.39 24.77 53 57.94z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),Go=V("path",{d:"M206 306c-18.05-8.27-37.93-11.45-59-11.45c-52 0-102.1 25.85-114.65 76.2c-1.65 6.66 2.53 13.25 9.37 13.25H154",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-miterlimit":"10","stroke-width":"32"},null,-1),qo=[Vo,Do,Uo,Go],Yo=_({name:"PeopleOutline",render:function(r,o){return fe(),pe("svg",Ko,qo)}}),Wo={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Xo=V("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M336 176L225.2 304L176 255.8"},null,-1),Zo=V("path",{d:"M463.1 112.37C373.68 96.33 336.71 84.45 256 48c-80.71 36.45-117.68 48.33-207.1 64.37C32.7 369.13 240.58 457.79 256 464c15.42-6.21 223.3-94.87 207.1-351.63z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),Qo=[Xo,Zo],Jo=_({name:"ShieldCheckmarkOutline",render:function(r,o){return fe(),pe("svg",Wo,Qo)}}),et={class:"h-screen flex flex-col"},ot={class:"flex-1 overflow-hidden"},ct=_({__name:"AdminLayout",setup(e){const r=ao(),o=co(),{t:n}=io(),a=C(()=>o.path),l=C(()=>[{label:n("admin.userManagement"),key:"/admin/users",icon:()=>c(we,null,{default:()=>c(Yo)})},{label:n("admin.roleManagement"),key:"/admin/roles",icon:()=>c(we,null,{default:()=>c(Jo)})}]);function v(g){r.push(g)}return(g,m)=>{const h=lo("router-view");return fe(),pe("div",et,[D(so),V("div",ot,[D(J(So),{"has-sider":"",class:"h-full"},{default:ie(()=>[D(J(ko),{bordered:"",width:"200"},{default:ie(()=>[D(J(jo),{value:a.value,options:l.value,"onUpdate:value":v},null,8,["value","options"])]),_:1}),D(J(Ao),{class:"p-6 overflow-y-auto"},{default:ie(()=>[D(h)]),_:1})]),_:1})])])}}});export{ct as default};
