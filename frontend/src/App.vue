<template>
  <div id="app">
    <!-- Login View -->
    <LoginView
      v-if="currentView === 'login'"
      @login="handleLogin"
    />

    <!-- Dashboard View -->
    <DashboardView
      v-else-if="currentView === 'dashboard'"
      @logout="handleLogout"
      @go-to-admin="goToAdmin"
    />

    <!-- Admin Panel -->
    <AdminPanel
      v-else-if="currentView === 'admin'"
      @logout="handleLogout"
      @go-to-dashboard="goToDashboard"
    />

    <!-- Shared Song View -->
    <SharedSongView
      v-else-if="currentView === 'shared'"
      :songId="sharedSongId"
    />
  </div>
</template>

<script>
import LoginView from './components/LoginView.vue';
import DashboardView from './components/DashboardView.vue';
import AdminPanel from './components/AdminPanel.vue';
import SharedSongView from './components/SharedSongView.vue';
import api from './api-service.js';

export default {
  name: 'App',
  components: { LoginView, DashboardView, AdminPanel, SharedSongView },
  data() {
    return {
      currentView: 'login',
      sharedSongId: null
    };
  },
  mounted() {
    this.handleGoogleCallback();
    this.handleRouting();
    window.addEventListener('hashchange', () => this.handleRouting());
  },
  methods: {
    handleLogin() {
      this.currentView = 'dashboard';
    },
    handleLogout() {
      this.currentView = 'login';
    },
    goToAdmin() {
      this.currentView = 'admin';
    },
    goToDashboard() {
      this.currentView = 'dashboard';
    },
    handleRouting() {
      const hash = window.location.hash.slice(1);
      if (hash.startsWith('/shared/')) {
        this.sharedSongId = hash.split('/')[2];
        this.currentView = 'shared';
      } else if (api.isAuthenticated() && this.currentView === 'login') {
        this.currentView = 'dashboard';
      }
    },
    async handleGoogleCallback() {
      const urlParams = new URLSearchParams(window.location.search);
      const authToken = urlParams.get('auth_token');
      const userId = urlParams.get('user');

      if (authToken && userId) {
        window.history.replaceState({}, document.title, '/');
        try {
          api.token = authToken;
          localStorage.setItem('authToken', authToken);
          const user = await api.getUser(userId);
          localStorage.setItem('currentUser', JSON.stringify(user));
          this.currentView = 'dashboard';
        } catch (error) {
          console.error('Failed to process OAuth callback:', error);
          this.currentView = 'login';
        }
      }
    }
  }
};
</script>

