import{S as Se,V as Ce,X as oe,a2 as r,am as ie,a3 as I,Y as k,a6 as le,d as O,P as f,_ as Be,$ as re,l as _,a1 as Re,an as Fe,ao as ze,I as P,ap as z,aq as E,ar as x,a5 as Ue,u as Z,E as ne,C as c,o as ee,D as Ve,H as p,e as h,a as G,h as J,t as A,r as Te,A as Ne,c as Me}from"./index-C0M1mhNe.js";import{N as se,P as Pe,a as Ae,b as We,c as Oe,d as T,e as je,f as De,g as He,h as Ke,A as Le,t as Ie,u as Ee,i as qe}from"./admin-BPRU1Z3Y.js";import{i as q,r as U,u as Xe,c as X}from"./resolve-slot-BNUvGlIa.js";import{u as Ye,B as W,N as Y}from"./Button-DoTPXuJ9.js";import{b as de}from"./Dropdown-BaSOTI8d.js";import{u as Ge}from"./use-message-DCWNO6bJ.js";const Je={buttonHeightSmall:"14px",buttonHeightMedium:"18px",buttonHeightLarge:"22px",buttonWidthSmall:"14px",buttonWidthMedium:"18px",buttonWidthLarge:"22px",buttonWidthPressedSmall:"20px",buttonWidthPressedMedium:"24px",buttonWidthPressedLarge:"28px",railHeightSmall:"18px",railHeightMedium:"22px",railHeightLarge:"26px",railWidthSmall:"32px",railWidthMedium:"40px",railWidthLarge:"48px"};function Qe(e){const{primaryColor:m,opacityDisabled:n,borderRadius:d,textColor3:g}=e;return Object.assign(Object.assign({},Je),{iconColor:g,textColor:"white",loadingColor:m,opacityDisabled:n,railColor:"rgba(0, 0, 0, .14)",railColorActive:m,buttonBoxShadow:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",buttonColor:"#FFF",railBorderRadiusSmall:d,railBorderRadiusMedium:d,railBorderRadiusLarge:d,buttonBorderRadiusSmall:d,buttonBorderRadiusMedium:d,buttonBorderRadiusLarge:d,boxShadowFocus:`0 0 0 2px ${Ce(m,{alpha:.2})}`})}const Ze={common:Se,self:Qe},ea=oe("switch",`
 height: var(--n-height);
 min-width: var(--n-width);
 vertical-align: middle;
 user-select: none;
 -webkit-user-select: none;
 display: inline-flex;
 outline: none;
 justify-content: center;
 align-items: center;
`,[r("children-placeholder",`
 height: var(--n-rail-height);
 display: flex;
 flex-direction: column;
 overflow: hidden;
 pointer-events: none;
 visibility: hidden;
 `),r("rail-placeholder",`
 display: flex;
 flex-wrap: none;
 `),r("button-placeholder",`
 width: calc(1.75 * var(--n-rail-height));
 height: var(--n-rail-height);
 `),oe("base-loading",`
 position: absolute;
 top: 50%;
 left: 50%;
 transform: translateX(-50%) translateY(-50%);
 font-size: calc(var(--n-button-width) - 4px);
 color: var(--n-loading-color);
 transition: color .3s var(--n-bezier);
 `,[ie({left:"50%",top:"50%",originalTransform:"translateX(-50%) translateY(-50%)"})]),r("checked, unchecked",`
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 box-sizing: border-box;
 position: absolute;
 white-space: nowrap;
 top: 0;
 bottom: 0;
 display: flex;
 align-items: center;
 line-height: 1;
 `),r("checked",`
 right: 0;
 padding-right: calc(1.25 * var(--n-rail-height) - var(--n-offset));
 `),r("unchecked",`
 left: 0;
 justify-content: flex-end;
 padding-left: calc(1.25 * var(--n-rail-height) - var(--n-offset));
 `),I("&:focus",[r("rail",`
 box-shadow: var(--n-box-shadow-focus);
 `)]),k("round",[r("rail","border-radius: calc(var(--n-rail-height) / 2);",[r("button","border-radius: calc(var(--n-button-height) / 2);")])]),le("disabled",[le("icon",[k("rubber-band",[k("pressed",[r("rail",[r("button","max-width: var(--n-button-width-pressed);")])]),r("rail",[I("&:active",[r("button","max-width: var(--n-button-width-pressed);")])]),k("active",[k("pressed",[r("rail",[r("button","left: calc(100% - var(--n-offset) - var(--n-button-width-pressed));")])]),r("rail",[I("&:active",[r("button","left: calc(100% - var(--n-offset) - var(--n-button-width-pressed));")])])])])])]),k("active",[r("rail",[r("button","left: calc(100% - var(--n-button-width) - var(--n-offset))")])]),r("rail",`
 overflow: hidden;
 height: var(--n-rail-height);
 min-width: var(--n-rail-width);
 border-radius: var(--n-rail-border-radius);
 cursor: pointer;
 position: relative;
 transition:
 opacity .3s var(--n-bezier),
 background .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 background-color: var(--n-rail-color);
 `,[r("button-icon",`
 color: var(--n-icon-color);
 transition: color .3s var(--n-bezier);
 font-size: calc(var(--n-button-height) - 4px);
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 display: flex;
 justify-content: center;
 align-items: center;
 line-height: 1;
 `,[ie()]),r("button",`
 align-items: center; 
 top: var(--n-offset);
 left: var(--n-offset);
 height: var(--n-button-height);
 width: var(--n-button-width-pressed);
 max-width: var(--n-button-width);
 border-radius: var(--n-button-border-radius);
 background-color: var(--n-button-color);
 box-shadow: var(--n-button-box-shadow);
 box-sizing: border-box;
 cursor: inherit;
 content: "";
 position: absolute;
 transition:
 background-color .3s var(--n-bezier),
 left .3s var(--n-bezier),
 opacity .3s var(--n-bezier),
 max-width .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 `)]),k("active",[r("rail","background-color: var(--n-rail-color-active);")]),k("loading",[r("rail",`
 cursor: wait;
 `)]),k("disabled",[r("rail",`
 cursor: not-allowed;
 opacity: .5;
 `)])]),aa=Object.assign(Object.assign({},re.props),{size:String,value:{type:[String,Number,Boolean],default:void 0},loading:Boolean,defaultValue:{type:[String,Number,Boolean],default:!1},disabled:{type:Boolean,default:void 0},round:{type:Boolean,default:!0},"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],checkedValue:{type:[String,Number,Boolean],default:!0},uncheckedValue:{type:[String,Number,Boolean],default:!1},railStyle:Function,rubberBand:{type:Boolean,default:!0},spinProps:Object,onChange:[Function,Array]});let M;const Q=O({name:"Switch",props:aa,slots:Object,setup(e){M===void 0&&(typeof CSS<"u"?typeof CSS.supports<"u"?M=CSS.supports("width","max(1px)"):M=!1:M=!0);const{mergedClsPrefixRef:m,inlineThemeDisabled:n,mergedComponentPropsRef:d}=Be(e),g=re("Switch","-switch",ea,Ze,e,m),l=Ye(e,{mergedSize(s){var S,C;if(e.size!==void 0)return e.size;if(s)return s.mergedSize.value;const F=(C=(S=d==null?void 0:d.value)===null||S===void 0?void 0:S.Switch)===null||C===void 0?void 0:C.size;return F||"medium"}}),{mergedSizeRef:v,mergedDisabledRef:b}=l,a=_(e.defaultValue),$=Ue(e,"value"),w=Xe($,a),o=P(()=>w.value===e.checkedValue),t=_(!1),i=_(!1),u=P(()=>{const{railStyle:s}=e;if(s)return s({focused:i.value,checked:o.value})});function y(s){const{"onUpdate:value":S,onChange:C,onUpdateValue:F}=e,{nTriggerFormInput:j,nTriggerFormChange:D}=l;S&&X(S,s),F&&X(F,s),C&&X(C,s),a.value=s,j(),D()}function ae(){const{nTriggerFormFocus:s}=l;s()}function ue(){const{nTriggerFormBlur:s}=l;s()}function ce(){e.loading||b.value||(w.value!==e.checkedValue?y(e.checkedValue):y(e.uncheckedValue))}function he(){i.value=!0,ae()}function fe(){i.value=!1,ue(),t.value=!1}function ve(s){e.loading||b.value||s.key===" "&&(w.value!==e.checkedValue?y(e.checkedValue):y(e.uncheckedValue),t.value=!1)}function me(s){e.loading||b.value||s.key===" "&&(s.preventDefault(),t.value=!0)}const te=P(()=>{const{value:s}=v,{self:{opacityDisabled:S,railColor:C,railColorActive:F,buttonBoxShadow:j,buttonColor:D,boxShadowFocus:be,loadingColor:pe,textColor:ge,iconColor:we,[z("buttonHeight",s)]:B,[z("buttonWidth",s)]:ye,[z("buttonWidthPressed",s)]:_e,[z("railHeight",s)]:R,[z("railWidth",s)]:N,[z("railBorderRadius",s)]:ke,[z("buttonBorderRadius",s)]:xe},common:{cubicBezierEaseInOut:$e}}=g.value;let H,K,L;return M?(H=`calc((${R} - ${B}) / 2)`,K=`max(${R}, ${B})`,L=`max(${N}, calc(${N} + ${B} - ${R}))`):(H=E((x(R)-x(B))/2),K=E(Math.max(x(R),x(B))),L=x(R)>x(B)?N:E(x(N)+x(B)-x(R))),{"--n-bezier":$e,"--n-button-border-radius":xe,"--n-button-box-shadow":j,"--n-button-color":D,"--n-button-width":ye,"--n-button-width-pressed":_e,"--n-button-height":B,"--n-height":K,"--n-offset":H,"--n-opacity-disabled":S,"--n-rail-border-radius":ke,"--n-rail-color":C,"--n-rail-color-active":F,"--n-rail-height":R,"--n-rail-width":N,"--n-width":L,"--n-box-shadow-focus":be,"--n-loading-color":pe,"--n-text-color":ge,"--n-icon-color":we}}),V=n?Re("switch",P(()=>v.value[0]),te,e):void 0;return{handleClick:ce,handleBlur:fe,handleFocus:he,handleKeyup:ve,handleKeydown:me,mergedRailStyle:u,pressed:t,mergedClsPrefix:m,mergedValue:w,checked:o,mergedDisabled:b,cssVars:n?void 0:te,themeClass:V==null?void 0:V.themeClass,onRender:V==null?void 0:V.onRender}},render(){const{mergedClsPrefix:e,mergedDisabled:m,checked:n,mergedRailStyle:d,onRender:g,$slots:l}=this;g==null||g();const{checked:v,unchecked:b,icon:a,"checked-icon":$,"unchecked-icon":w}=l,o=!(q(a)&&q($)&&q(w));return f("div",{role:"switch","aria-checked":n,class:[`${e}-switch`,this.themeClass,o&&`${e}-switch--icon`,n&&`${e}-switch--active`,m&&`${e}-switch--disabled`,this.round&&`${e}-switch--round`,this.loading&&`${e}-switch--loading`,this.pressed&&`${e}-switch--pressed`,this.rubberBand&&`${e}-switch--rubber-band`],tabindex:this.mergedDisabled?void 0:0,style:this.cssVars,onClick:this.handleClick,onFocus:this.handleFocus,onBlur:this.handleBlur,onKeyup:this.handleKeyup,onKeydown:this.handleKeydown},f("div",{class:`${e}-switch__rail`,"aria-hidden":"true",style:d},U(v,t=>U(b,i=>t||i?f("div",{"aria-hidden":!0,class:`${e}-switch__children-placeholder`},f("div",{class:`${e}-switch__rail-placeholder`},f("div",{class:`${e}-switch__button-placeholder`}),t),f("div",{class:`${e}-switch__rail-placeholder`},f("div",{class:`${e}-switch__button-placeholder`}),i)):null)),f("div",{class:`${e}-switch__button`},U(a,t=>U($,i=>U(w,u=>f(Fe,null,{default:()=>this.loading?f(ze,Object.assign({key:"loading",clsPrefix:e,strokeWidth:20},this.spinProps)):this.checked&&(i||t)?f("div",{class:`${e}-switch__button-icon`,key:i?"checked-icon":"icon"},i||t):!this.checked&&(u||t)?f("div",{class:`${e}-switch__button-icon`,key:u?"unchecked-icon":"icon"},u||t):null})))),U(v,t=>t&&f("div",{key:"checked",class:`${e}-switch__checked`},t)),U(b,t=>t&&f("div",{key:"unchecked",class:`${e}-switch__unchecked`},t)))))}}),ta=O({__name:"UserTable",props:{users:{},loading:{type:Boolean}},emits:["edit","toggle-active","refresh"],setup(e,{emit:m}){const{t:n}=Z(),d=m,g=[{title:n("userTable.id"),key:"id",width:60},{title:n("userTable.username"),key:"username"},{title:n("userTable.role"),key:"role_name",render(l){return l.role_name?f(se,{type:"info",size:"small"},{default:()=>l.role_name}):"-"}},{title:n("userTable.admin"),key:"is_admin",width:80,render(l){return f(se,{type:l.is_admin?"success":"default",size:"small"},{default:()=>l.is_admin?n("userTable.yes"):n("userTable.no")})}},{title:n("userTable.status"),key:"is_active",width:80,render(l){return f(Q,{value:l.is_active,onUpdateValue:()=>d("toggle-active",l.id)})}},{title:n("userTable.createdAt"),key:"created_at",width:160,render(l){var v;return((v=l.created_at)==null?void 0:v.slice(0,19))||"-"}},{title:n("userTable.actions"),key:"actions",width:80,render(l){return f(W,{text:!0,type:"primary",onClick:()=>d("edit",l)},{icon:()=>f(de,null,{default:()=>f(Pe)})})}}];return(l,v)=>(ee(),ne(c(Ae),{columns:g,data:e.users,loading:e.loading,pagination:!1,striped:""},null,8,["data","loading"]))}}),oa={class:"flex justify-end gap-2"},ia=O({__name:"UserFormModal",props:{visible:{type:Boolean},user:{},roles:{}},emits:["close","save"],setup(e,{emit:m}){const{t:n}=Z(),d=e,g=m,l=_(null),v=_(!1),b=P(()=>d.roles.map(o=>({label:o.name,value:o.id}))),a=Te({username:"",password:"",role_id:null,odoo_api_key:"",is_admin:!1,is_active:!0}),$={username:[{required:!0,message:n("validation.usernameRequired")}]};Ve(()=>d.user,o=>{o?(a.username=o.username,a.password="",a.role_id=o.role_id,a.odoo_api_key=null,a.is_admin=o.is_admin,a.is_active=o.is_active):(a.username="",a.password="",a.role_id=null,a.odoo_api_key=null,a.is_admin=!1,a.is_active=!0)},{immediate:!0});async function w(){var i;if(!await((i=l.value)==null?void 0:i.validate().catch(()=>!1)))return;v.value=!0;const t={username:a.username,role_id:a.role_id,is_admin:a.is_admin,is_active:a.is_active};d.user?(a.password&&(t.password=a.password),a.odoo_api_key!==null&&(t.odoo_api_key=a.odoo_api_key)):(t.password=a.password,a.odoo_api_key&&(t.odoo_api_key=a.odoo_api_key)),g("save",t),v.value=!1}return(o,t)=>(ee(),ne(c(We),{show:e.visible,"mask-closable":!1,"onUpdate:show":t[8]||(t[8]=i=>!i&&o.$emit("close"))},{default:p(()=>[h(c(De),{style:{width:"600px"},title:e.user?o.$t("admin.editUser"):o.$t("admin.createUser"),bordered:!1,size:"huge",role:"dialog",closable:"",onClose:t[7]||(t[7]=i=>o.$emit("close"))},{footer:p(()=>[G("div",oa,[h(c(W),{onClick:t[6]||(t[6]=i=>o.$emit("close"))},{default:p(()=>[J(A(o.$t("userForm.cancel")),1)]),_:1}),h(c(W),{type:"primary",loading:v.value,onClick:w},{default:p(()=>[J(A(o.$t("userForm.save")),1)]),_:1},8,["loading"])])]),default:p(()=>[h(c(Oe),{ref_key:"formRef",ref:l,model:a,rules:$,"label-placement":"left","label-width":"100"},{default:p(()=>[h(c(T),{label:o.$t("userForm.username"),path:"username"},{default:p(()=>[h(c(Y),{value:a.username,"onUpdate:value":t[0]||(t[0]=i=>a.username=i),placeholder:o.$t("userForm.username")},null,8,["value","placeholder"])]),_:1},8,["label"]),h(c(T),{label:o.$t("userForm.password"),path:"password"},{default:p(()=>[h(c(Y),{value:a.password,"onUpdate:value":t[1]||(t[1]=i=>a.password=i),type:"password",placeholder:e.user?o.$t("userForm.passwordPlaceholder"):o.$t("userForm.passwordCreatePlaceholder")},null,8,["value","placeholder"])]),_:1},8,["label"]),h(c(T),{label:o.$t("userForm.role"),path:"role_id"},{default:p(()=>[h(c(je),{value:a.role_id,"onUpdate:value":t[2]||(t[2]=i=>a.role_id=i),options:b.value,placeholder:o.$t("userForm.rolePlaceholder"),clearable:""},null,8,["value","options","placeholder"])]),_:1},8,["label"]),h(c(T),{label:o.$t("userForm.odooApiKey"),path:"odoo_api_key"},{default:p(()=>[h(c(Y),{value:a.odoo_api_key,"onUpdate:value":t[3]||(t[3]=i=>a.odoo_api_key=i),type:"password",placeholder:o.$t("userForm.odooApiKeyPlaceholder")},null,8,["value","placeholder"])]),_:1},8,["label"]),h(c(T),{label:o.$t("userForm.admin"),path:"is_admin"},{default:p(()=>[h(c(Q),{value:a.is_admin,"onUpdate:value":t[4]||(t[4]=i=>a.is_admin=i)},null,8,["value"])]),_:1},8,["label"]),h(c(T),{label:o.$t("userForm.active"),path:"is_active"},{default:p(()=>[h(c(Q),{value:a.is_active,"onUpdate:value":t[5]||(t[5]=i=>a.is_active=i)},null,8,["value"])]),_:1},8,["label"])]),_:1},8,["model"])]),_:1},8,["title"])]),_:1},8,["show"]))}}),la={class:"flex justify-between items-center mb-4"},sa={class:"text-xl font-bold m-0"},fa=O({__name:"UserManagement",setup(e){const{t:m}=Z(),n=Ge(),d=_([]),g=_([]),l=_(!1),v=_(!1),b=_(null);Ne(()=>{a(),$()});async function a(){l.value=!0;try{const u=await He();u.code===0&&(d.value=u.data)}finally{l.value=!1}}async function $(){const u=await Ke();u.code===0&&(g.value=u.data)}function w(u){b.value=u,v.value=!0}async function o(u){(await Ie(u)).code===0&&(n.success(m("admin.statusUpdated")),a())}function t(){v.value=!1,b.value=null}async function i(u){b.value?(await Ee(b.value.id,u)).code===0&&(n.success(m("admin.userUpdated")),t(),a()):(await qe(u)).code===0&&(n.success(m("admin.userCreated")),t(),a())}return(u,y)=>(ee(),Me("div",null,[G("div",la,[G("h2",sa,A(u.$t("admin.userManagement")),1),h(c(W),{type:"primary",onClick:y[0]||(y[0]=ae=>v.value=!0)},{icon:p(()=>[h(c(de),null,{default:p(()=>[h(c(Le))]),_:1})]),default:p(()=>[J(" "+A(u.$t("admin.createUser")),1)]),_:1})]),h(ta,{users:d.value,loading:l.value,onEdit:w,onToggleActive:o,onRefresh:a},null,8,["users","loading"]),h(ia,{visible:v.value,user:b.value,roles:g.value,onClose:t,onSave:i},null,8,["visible","user","roles"])]))}});export{fa as default};
