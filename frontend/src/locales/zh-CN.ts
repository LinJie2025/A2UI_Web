/** Simplified Chinese (简体中文) — baseline */
export default {
  // ── Brand ──
  brand: {
    subtitle: "智能 ERP 对话助手",
    desc: "用自然语言管理库存、订单、客户 — AI 为你生成可交互的操作界面。",
    tag1: "💬 自然语言交互",
    tag2: "📋 动态表格表单",
    tag3: "🔗 Odoo 无缝对接",
    version: "v1.0.0 · 生产环境就绪",
  },

  // ── Navigation ──
  nav: {
    chat: "聊天",
    admin: "管理",
    adminBadge: "管理员",
    logout: "退出登录",
    defaultUser: "用户",
  },

  // ── Sidebar ──
  sidebar: {
    newChat: "新对话",
    empty: "暂无会话记录",
    deleteTitle: "删除会话",
    newSession: "新会话",
    expand: "展开侧栏",
    collapse: "折叠侧栏",
  },

  // ── Login ──
  login: {
    title: "欢迎回来",
    subtitle: "登录你的账号以继续使用",
    usernameLabel: "用户名",
    usernamePlaceholder: "请输入用户名",
    passwordLabel: "密码",
    passwordPlaceholder: "请输入密码",
    rememberMe: "记住我",
    forgotPassword: "忘记密码？",
    submit: "登录",
    submitting: "登录中...",
    showPassword: "显示密码",
    hidePassword: "隐藏密码",
    noAccount: "还没有账号？",
    createAccount: "创建一个新账号",
    welcomeBack: "欢迎回来",
    brandTitle: "智能 ERP\n对话助手",
    brandDesc: "用自然语言管理库存、订单、客户 — AI 为你生成可交互的操作界面。",
    brandTags: ["💬 自然语言交互", "📋 动态表格表单", "🔗 Odoo 无缝对接"],
    brandVersion: "v1.0.0 · 生产环境就绪",
  },

  // ── Register ──
  register: {
    title: "创建账号",
    subtitle: "填写以下信息完成注册",
    brandTitle: "创建账号",
    brandDesc: "注册一个账号，开始使用 AI 驱动的智能 ERP 对话助手，让工作更高效。",
    brandTags: ["🔒 安全加密", "⚡ 即时开通", "🎯 角色权限"],
    usernameLabel: "用户名",
    usernamePlaceholder: "设置用户名",
    passwordLabel: "密码",
    passwordPlaceholder: "至少 6 位字符",
    confirmPasswordLabel: "确认密码",
    confirmPasswordPlaceholder: "再次输入密码",
    submit: "创建账号",
    submitting: "注册中...",
    hasAccount: "已有账号？",
    backToLogin: "返回登录",
    showPassword: "显示密码",
    hidePassword: "隐藏密码",
    success: "注册成功，请登录",
    failed: "注册失败",
    retryFailed: "注册失败，请稍后重试",
  },

  // ── Chat ──
  chat: {
    welcome: "你好，我是 A2UI 助手",
    welcomeDesc: "问我任何关于库存、订单、客户、采购的问题 — 我会直接返回可操作的界面。",
    inputPlaceholder: "输入消息... (Enter 发送，Shift+Enter 换行)",
    sendAria: "发送消息",
    assistantName: "A2UI 助手",
    me: "我",
    generatingUI: "A2UI 正在生成界面...",
    closeOverlay: "关闭",
    expandFullscreen: "展开全屏",
  },

  // ── Overlay ──
  overlay: {
    prevStep: "上一步",
    nextStep: "下一步",
    statusDone: "已完成",
    statusActive: "进行中",
  },

  // ── Tool Call ──
  toolCall: {
    prefix: "Tool:",
    running: "执行中...",
    success: "完成",
    error: "失败",
    arguments: "参数",
    result: "结果",
  },

  // ── Validation ──
  validation: {
    usernameRequired: "请输入用户名",
    usernameMinLength: "用户名至少 2 个字符",
    passwordRequired: "请输入密码",
    passwordMinLength: "密码至少 6 个字符",
    confirmPasswordRequired: "请再次输入密码",
    passwordMismatch: "两次输入的密码不一致",
    roleNameRequired: "请输入角色名称",
  },

  // ── Admin ──
  admin: {
    userManagement: "用户管理",
    roleManagement: "角色管理",
    createUser: "新建用户",
    createRole: "新建角色",
    editUser: "编辑用户",
    editRole: "编辑角色",
    statusUpdated: "状态已更新",
    userUpdated: "用户已更新",
    userCreated: "用户已创建",
    roleDeleted: "角色已删除",
    roleUpdated: "角色已更新",
    roleCreated: "角色已创建",
    noTools: "暂无可用工具（请检查 MCP 连接）",
  },

  // ── User Table ──
  userTable: {
    id: "ID",
    username: "用户名",
    role: "角色",
    admin: "管理员",
    status: "状态",
    createdAt: "创建时间",
    actions: "操作",
    yes: "是",
    no: "否",
  },

  // ── Role Table ──
  roleTable: {
    id: "ID",
    name: "名称",
    description: "描述",
    whitelistTools: "白名单工具",
    noTools: "无工具",
    createdAt: "创建时间",
    actions: "操作",
  },

  // ── User Form ──
  userForm: {
    username: "用户名",
    password: "密码",
    passwordPlaceholder: "留空不修改",
    passwordCreatePlaceholder: "请输入密码",
    role: "角色",
    rolePlaceholder: "选择角色",
    odooApiKey: "Odoo API Key",
    odooApiKeyPlaceholder: "加密存储",
    admin: "管理员",
    active: "启用",
    cancel: "取消",
    save: "保存",
  },

  // ── Role Form ──
  roleForm: {
    name: "名称",
    namePlaceholder: "角色名称",
    description: "描述",
    descriptionPlaceholder: "角色描述",
    toolWhitelist: "工具白名单",
    cancel: "取消",
    save: "保存",
  },

  // ── Language ──
  language: {
    label: "语言",
    switchTo: "切换语言",
  },

};
