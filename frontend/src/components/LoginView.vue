<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 p-6">
    <div class="bg-white border border-gray-200 rounded-2xl shadow-xl p-10 w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-7">
        <div class="w-14 h-14 bg-gray-900 text-white rounded-xl inline-flex items-center justify-center text-xl mb-3.5">
          <i class="fas fa-music"></i>
        </div>
        <h1 class="text-2xl font-bold tracking-tight mb-1">Chitara</h1>
        <p class="text-gray-400 text-sm">AI Music Generation</p>
      </div>

      <!-- Divider -->
      <div class="h-px bg-gray-200 mb-7"></div>

      <!-- Sign In -->
      <div class="mb-6">
        <p class="text-sm text-gray-600 mb-4 text-center">Sign in to continue</p>

        <button
          id="google-signin-btn"
          class="w-full flex items-center justify-center gap-2.5 p-3 bg-white border-[1.5px] border-gray-200 rounded-lg text-gray-900 text-[15px] font-medium transition-all hover:not(:disabled):border-gray-400 hover:not(:disabled):shadow-sm hover:not(:disabled):bg-gray-50 disabled:opacity-60 cursor-pointer disabled:cursor-default"
          @click="handleGoogleLogin"
          :disabled="loading"
        >
          <!-- Google Logo SVG -->
          <svg class="w-5 h-5 shrink-0" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
          <span v-if="!loading">Continue with Google</span>
          <span v-else><i class="fas fa-circle-notch spin"></i> Connecting…</span>
        </button>

        <!-- Error -->
        <div v-if="error" class="mt-4 py-3 px-4 bg-red-50 border border-red-300 rounded-md text-red-500 text-sm flex items-center gap-2" role="alert">
          <i class="fas fa-exclamation-circle"></i>
          {{ error }}
        </div>
      </div>

      <p class="text-xs text-gray-400 text-center">
        By continuing, you agree to our terms of service.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      loading: false,
      error: ''
    };
  },
  methods: {
    async handleGoogleLogin() {
      this.error = '';
      this.loading = true;
      try {
        const response = await fetch('http://localhost:8000/api/auth/google/');
        const data = await response.json();
        window.location.href = data.auth_url;
      } catch {
        this.error = 'Failed to connect to Google. Please try again.';
        this.loading = false;
      }
    }
  }
};
</script>
