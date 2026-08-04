<template>
  <div class="auth-page">
    <!-- Background layers -->
    <div class="bg-subtle"></div>
    <div class="bg-dots"></div>

    <!-- Auth container -->
    <div class="auth-container">
      <div class="auth-card">
        <!-- Left brand panel (desktop) -->
        <div class="brand-panel">
          <!-- Floating geometric shapes -->
          <div class="brand-shapes">
            <svg viewBox="0 0 400 600" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="80" cy="120" r="60" stroke="white" stroke-width="0.5" stroke-dasharray="4 4" opacity="0.4" />
              <circle cx="320" cy="400" r="80" stroke="white" stroke-width="0.5" stroke-dasharray="6 6" opacity="0.3" />
              <circle cx="200" cy="280" r="40" fill="white" opacity="0.06" />
              <rect x="120" y="80" width="30" height="30" rx="6" stroke="white" stroke-width="0.6" opacity="0.25" transform="rotate(15 135 95)" />
              <rect x="250" y="480" width="25" height="25" rx="5" stroke="white" stroke-width="0.6" opacity="0.2" transform="rotate(-10 262 492)" />
            </svg>
          </div>

          <div class="brand-top">
            <div class="brand-logo">
              <div class="logo-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
                  <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                </svg>
              </div>
              <span class="brand-name">A2UI</span>
            </div>
            <h1 class="brand-title">{{ $t('login.brandTitle') }}</h1>
            <p class="brand-desc">{{ $t('login.brandDesc') }}</p>
            <div class="brand-tags">
              <span class="brand-tag">{{ $t('login.brandTags.0') }}</span>
              <span class="brand-tag">{{ $t('login.brandTags.1') }}</span>
              <span class="brand-tag">{{ $t('login.brandTags.2') }}</span>
            </div>
          </div>

          <div class="brand-bottom">
            <span>{{ $t('login.brandVersion') }}</span>
          </div>
        </div>

        <!-- Right form panel -->
        <div class="form-panel">
          <!-- Mobile logo -->
          <div class="mobile-logo">
            <div class="logo-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
                <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
              </svg>
            </div>
            <span class="brand-name-mobile">A2UI</span>
          </div>

          <!-- Language switcher (mobile) -->
          <div class="mobile-lang">
            <LanguageSwitcher />
          </div>

          <h2 class="form-title">{{ $t('login.welcomeBack') }}</h2>
          <p class="form-subtitle">{{ $t('login.subtitle') }}</p>

          <!-- Global error banner -->
          <div v-if="errorMsg" class="error-banner">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>{{ errorMsg }}</span>
          </div>

          <!-- Login form -->
          <form @submit.prevent="onSubmit" novalidate class="auth-form">
            <!-- Username -->
            <div class="field">
              <label class="field-label" for="loginUser">{{ $t('login.usernameLabel') }}</label>
              <div class="field-input-wrap">
                <svg class="field-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                <input
                  id="loginUser"
                  v-model="formData.username"
                  :class="['field-input', { 'field-input-error': errors.username }]"
                  :placeholder="$t('login.usernamePlaceholder')"
                  autocomplete="username"
                  @input="clearError('username')"
                  @blur="validateField('username')"
                />
              </div>
              <div v-if="errors.username" class="field-error">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {{ errors.username }}
              </div>
            </div>

            <!-- Password -->
            <div class="field">
              <label class="field-label" for="loginPwd">{{ $t('login.passwordLabel') }}</label>
              <div class="field-input-wrap">
                <svg class="field-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
                <input
                  id="loginPwd"
                  v-model="formData.password"
                  :type="showPwd ? 'text' : 'password'"
                  :class="['field-input', 'field-input-has-toggle', { 'field-input-error': errors.password }]"
                  :placeholder="$t('login.passwordPlaceholder')"
                  autocomplete="current-password"
                  @input="clearError('password')"
                  @blur="validateField('password')"
                  @keyup.enter="onSubmit"
                />
                <button type="button" class="pwd-toggle" @click="showPwd = !showPwd" :aria-label="showPwd ? $t('login.hidePassword') : $t('login.showPassword')">
                  <svg v-if="!showPwd" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
              </div>
              <div v-if="errors.password" class="field-error">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {{ errors.password }}
              </div>
            </div>

            <!-- Remember me & Forgot -->
            <div class="form-options">
              <label class="remember-label">
                <input type="checkbox" v-model="formData.remember" class="custom-checkbox" />
                <span>{{ $t('login.rememberMe') }}</span>
              </label>
              <a href="#" class="forgot-link">{{ $t('login.forgotPassword') }}</a>
            </div>

            <!-- Submit -->
            <button type="submit" :disabled="loading" class="submit-btn">
              <template v-if="!loading">{{ $t('login.submit') }}</template>
              <template v-else>
                <span class="spinner"></span>
                {{ $t('login.submitting') }}
              </template>
            </button>
          </form>

          <!-- Divider -->
          <div class="divider-row">
            <div class="divider-line"></div>
            <span class="divider-text">{{ $t('login.noAccount') }}</span>
            <div class="divider-line"></div>
          </div>

          <!-- Register link -->
          <button class="register-btn" @click="$router.push('/register')">
            {{ $t('login.createAccount') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useI18n } from "vue-i18n";
import { useAuth } from "@/composables/useAuth";
import LanguageSwitcher from "@/components/common/LanguageSwitcher.vue";

const { t } = useI18n();
const { handleLogin } = useAuth();

const formData = reactive({
  username: "",
  password: "",
  remember: false,
});

const errors = reactive<Record<string, string>>({
  username: "",
  password: "",
});

const errorMsg = ref("");
const loading = ref(false);
const showPwd = ref(false);

/** Clear a specific field error on input. */
function clearError(field: string) {
  errors[field] = "";
  errorMsg.value = "";
}

/** Validate a single field on blur. */
function validateField(field: string) {
  if (field === "username") {
    if (!formData.username.trim()) {
      errors.username = t("validation.usernameRequired");
    } else if (formData.username.trim().length < 2) {
      errors.username = t("validation.usernameMinLength");
    } else {
      errors.username = "";
    }
  }
  if (field === "password") {
    if (!formData.password) {
      errors.password = t("validation.passwordRequired");
    } else if (formData.password.length < 6) {
      errors.password = t("validation.passwordMinLength");
    } else {
      errors.password = "";
    }
  }
}

/** Validate all fields before submit. */
function validateAll(): boolean {
  validateField("username");
  validateField("password");
  return !errors.username && !errors.password;
}

/** Handle form submission. */
async function onSubmit() {
  if (!validateAll()) return;

  loading.value = true;
  errorMsg.value = "";

  try {
    const err = await handleLogin(formData.username, formData.password);
    if (err) {
      errorMsg.value = err;
      errors.username = " ";
      errors.password = " ";
    }
  } catch (e: unknown) {
    errorMsg.value = t("register.retryFailed");
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* ─── Design tokens (inherited from Clean Studio) ─── */
.auth-page {
  --bg-page: #f8fafb;
  --bg-card: #ffffff;
  --border-subtle: #e2e8f0;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  --accent-primary: #2563eb;
  --accent-danger: #ef4444;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.03);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.04);
  --shadow-lg: 0 12px 40px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.03);
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --font-display: 'Outfit', system-ui, sans-serif;
  --font-body: 'Plus Jakarta Sans', system-ui, sans-serif;

  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-page);
  font-family: var(--font-body);
  color: var(--text-primary);
  line-height: 1.65;
}

/* ─── Background layers ─── */
.bg-subtle {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 60% 50% at 15% 20%, rgba(37,99,235,0.06) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 85% 75%, rgba(13,148,136,0.05) 0%, transparent 60%),
    var(--bg-page);
}
.bg-dots {
  position: fixed; inset: 0; z-index: 0; opacity: 0.25; pointer-events: none;
  background-image: radial-gradient(#cbd5e1 0.5px, transparent 0.5px);
  background-size: 22px 22px;
}

/* ─── Container ─── */
.auth-container {
  position: relative; z-index: 10;
  width: 100%; max-width: 56rem;
  margin: 2rem 1rem;
}

.auth-card {
  display: flex;
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  min-height: 520px;
}

/* ─── Left Brand Panel ─── */
.brand-panel {
  width: 41.666%;
  background: linear-gradient(160deg, #1e3a5f 0%, #1a365d 30%, #1e40af 70%, #1d4ed8 100%);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.brand-shapes {
  position: absolute; inset: 0; opacity: 0.2;
}
.brand-shapes svg {
  width: 100%; height: 100%;
}

.brand-top {
  position: relative; z-index: 10;
  padding: 2.5rem 2rem 0;
}
.brand-logo {
  display: flex; align-items: center; gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.logo-icon {
  width: 2.5rem; height: 2.5rem;
  border-radius: 0.75rem;
  display: flex; align-items: center; justify-content: center;
  background: rgba(255,255,255,0.15);
}
.brand-name {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1.5rem;
  color: white;
  letter-spacing: -0.02em;
}

.brand-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  line-height: 1.25;
  margin-bottom: 0.75rem;
  white-space: pre-line;
}
.brand-desc {
  font-size: 0.8125rem;
  line-height: 1.6;
  color: rgba(255,255,255,0.7);
}

.brand-tags {
  display: flex; flex-wrap: wrap; gap: 0.5rem;
  margin-top: 1.5rem;
}
.brand-tag {
  font-size: 0.6875rem;
  font-weight: 500;
  padding: 0.375rem 0.75rem;
  border-radius: 999px;
  color: rgba(255,255,255,0.85);
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.12);
}

.brand-bottom {
  position: relative; z-index: 10;
  padding: 0 2rem 2.5rem;
  font-size: 0.6875rem;
  color: rgba(255,255,255,0.35);
}

/* ─── Right Form Panel ─── */
.form-panel {
  flex: 1;
  display: flex; flex-direction: column; justify-content: center;
  padding: 2.5rem 3rem;
  max-width: 480px;
}

.mobile-logo {
  display: none;
}

.mobile-lang {
  display: none;
}

.form-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}
.form-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

/* ─── Error Banner ─── */
.error-banner {
  display: flex; align-items: flex-start; gap: 0.5rem;
  padding: 0.625rem 0.875rem;
  font-size: 0.8125rem;
  color: #991b1b;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: var(--radius-sm);
  margin-bottom: 1rem;
  animation: fadeSlideUp 0.3s ease-out;
}
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ─── Form ─── */
.auth-form {
  display: flex; flex-direction: column; gap: 1rem;
  width: 100%;
}

.field-label {
  display: block;
  font-family: var(--font-display);
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 0.375rem;
}

.field {
  width: 100%;
}

.field-input-wrap {
  position: relative;
  width: 100%;
}

.field-icon {
  position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
  z-index: 1;
}

.field-input {
  width: 100%;
  box-sizing: border-box;
  min-height: 48px;
  padding: 0.75rem 0.875rem;
  background: #f8fafc;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: 0.9375rem;
  color: var(--text-primary);
  transition: all 0.2s ease;
  outline: none;
}
.field-input::placeholder { color: var(--text-muted); }
.field-input:focus {
  border-color: var(--accent-primary);
  background: var(--bg-card);
  box-shadow: 0 0 0 3px rgba(37,99,235,0.08);
}
.field-input-error,
.field-input-error:focus {
  border-color: var(--accent-danger);
  box-shadow: 0 0 0 3px rgba(239,68,68,0.06);
  background: #fff;
}

/* Icon padding — all inputs inside a wrap get left room for the SVG icon */
.field-input-wrap .field-input {
  padding-left: 2.5rem;
}
/* Password — extra right room for the visibility toggle button */
.field-input-has-toggle {
  padding-right: 2.5rem;
}

.field-error {
  display: flex; align-items: center; gap: 0.25rem;
  font-size: 0.75rem;
  color: var(--accent-danger);
  margin-top: 0.25rem;
}

.pwd-toggle {
  position: absolute; right: 0.75rem; top: 50%; transform: translateY(-50%);
  background: none; border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.25rem;
  min-width: 36px; min-height: 36px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 0.25rem;
}
.pwd-toggle:hover { color: var(--text-secondary); }

/* ─── Options row ─── */
.form-options {
  display: flex; align-items: center; justify-content: space-between;
  font-size: 0.8125rem;
}
.remember-label {
  display: flex; align-items: center; gap: 0.5rem;
  color: var(--text-secondary);
  cursor: pointer;
}
.custom-checkbox {
  appearance: none;
  width: 18px; height: 18px;
  border: 1.5px solid var(--border-subtle);
  border-radius: 4px;
  background: var(--bg-card);
  cursor: pointer;
  flex-shrink: 0;
  position: relative;
  transition: all 0.15s;
}
.custom-checkbox:checked {
  background: var(--accent-primary);
  border-color: var(--accent-primary);
}
.custom-checkbox:checked::after {
  content: '';
  position: absolute; top: 1px; left: 4px;
  width: 5px; height: 9px;
  border: solid #fff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
.forgot-link {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--accent-primary);
  text-decoration: none;
}
.forgot-link:hover { text-decoration: underline; }

/* ─── Submit button ─── */
.submit-btn {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--accent-primary);
  color: #fff;
  cursor: pointer;
  width: 100%;
  box-sizing: border-box;
  min-height: 48px;
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  box-shadow: 0 2px 8px rgba(37,99,235,0.2);
  transition: all 0.15s ease;
  margin-top: 0.25rem;
}
.submit-btn:hover:not(:disabled) {
  background: #1d4ed8;
  box-shadow: 0 6px 20px rgba(37,99,235,0.25);
  transform: translateY(-1px);
}
.submit-btn:active:not(:disabled) { transform: scale(0.98); }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ─── Divider ─── */
.divider-row {
  display: flex; align-items: center; gap: 0.75rem;
  margin: 1.25rem 0 1rem;
}
.divider-line {
  flex: 1; height: 1px; background: var(--border-subtle);
}
.divider-text {
  font-size: 0.75rem; color: var(--text-muted);
  white-space: nowrap;
}

/* ─── Register button ─── */
.register-btn {
  font-family: var(--font-display);
  font-weight: 500;
  font-size: 0.875rem;
  padding: 0.625rem 1rem;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: #f8fafc;
  color: var(--text-secondary);
  cursor: pointer;
  width: 100%;
  min-height: 44px;
  transition: all 0.15s;
}
.register-btn:hover {
  border-color: var(--accent-primary);
  background: #eff6ff;
  color: var(--accent-primary);
}

/* ─── Responsive ─── */
@media (max-width: 768px) {
  .auth-page { align-items: flex-start; padding: 0; }
  .auth-container { margin: 0; max-width: 100%; }
  .auth-card { border-radius: 0; min-height: 100svh; box-shadow: none; }

  .brand-panel { display: none; }

  .form-panel {
    max-width: 100%;
    padding: 2.5rem 1.5rem;
    justify-content: flex-start;
  }

  .mobile-logo {
    display: flex; align-items: center; gap: 0.625rem;
    margin-bottom: 1.5rem;
  }
  .mobile-logo .logo-icon {
    width: 2.25rem; height: 2.25rem;
    background: var(--accent-primary);
  }
  .brand-name-mobile {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--text-primary);
  }

  .mobile-lang {
    display: block;
    margin-bottom: 1rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
