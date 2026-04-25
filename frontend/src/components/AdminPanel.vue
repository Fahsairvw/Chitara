<template>
  <div class="flex-1 flex flex-col min-h-screen bg-gray-50">
    <header class="bg-white border-b border-gray-200 py-6 shadow-sm">
      <div class="max-w-7xl mx-auto px-8 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <i class="fas fa-music text-2xl text-gray-900"></i>
          <h1 class="text-2xl font-bold m-0">Chitara Admin</h1>
        </div>
        <div class="flex items-center gap-4">
          <span class="font-medium text-gray-700">{{ currentUser.firstName }} {{ currentUser.lastName }}</span>
          <button class="inline-flex items-center gap-2 px-4 py-2.5 bg-gray-200 text-gray-700 font-medium rounded-lg hover:bg-gray-300 transition-colors cursor-pointer" @click="logout">
            <i class="fas fa-sign-out-alt"></i> Logout
          </button>
          <button class="inline-flex items-center gap-2 px-4 py-2.5 bg-gray-200 text-gray-700 font-medium rounded-lg hover:bg-gray-300 transition-colors cursor-pointer" @click="goToDashboard">
            <i class="fas fa-arrow-left"></i> Back to Dashboard
          </button>
        </div>
      </div>
    </header>

    <main class="flex-1 py-8 bg-gray-50">
      <div class="max-w-7xl mx-auto px-8">
        <h2 class="text-2xl font-semibold mb-8">Admin Dashboard</h2>

        <!-- Statistics -->
        <div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-8 mb-12">
          <div class="bg-white p-8 rounded-2xl shadow-sm flex items-center gap-6 border border-gray-200">
            <div class="text-3xl text-gray-900 w-[60px] h-[60px] bg-gray-100 rounded-lg flex items-center justify-center shrink-0">
              <i class="fas fa-users"></i>
            </div>
            <div>
              <h3 class="text-[15px] text-gray-500 font-medium m-0 mb-2">Total Users</h3>
              <p class="text-3xl font-bold text-gray-900 m-0">{{ totalUsers }}</p>
            </div>
          </div>

          <div class="bg-white p-8 rounded-2xl shadow-sm flex items-center gap-6 border border-gray-200">
            <div class="text-3xl text-gray-900 w-[60px] h-[60px] bg-gray-100 rounded-lg flex items-center justify-center shrink-0">
              <i class="fas fa-music"></i>
            </div>
            <div>
              <h3 class="text-[15px] text-gray-500 font-medium m-0 mb-2">Total Songs</h3>
              <p class="text-3xl font-bold text-gray-900 m-0">{{ totalSongs }}</p>
            </div>
          </div>

          <div class="bg-white p-8 rounded-2xl shadow-sm flex items-center gap-6 border border-gray-200">
            <div class="text-3xl text-gray-900 w-[60px] h-[60px] bg-gray-100 rounded-lg flex items-center justify-center shrink-0">
              <i class="fas fa-wand-magic-sparkles"></i>
            </div>
            <div>
              <h3 class="text-[15px] text-gray-500 font-medium m-0 mb-2">Songs Generated</h3>
              <p class="text-3xl font-bold text-gray-900 m-0">{{ generatedSongs }}</p>
            </div>
          </div>
        </div>

        <!-- Users Section -->
        <section class="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
          <h3 class="text-xl font-semibold mt-0 mb-6">Users</h3>
          <div v-if="loading" class="text-center p-8 text-gray-500">Loading...</div>
          <div v-else-if="users.length === 0" class="text-center p-8 text-gray-500">
            No users found.
          </div>
          <table v-else class="w-full border-collapse">
            <thead class="bg-gray-50 border-b-2 border-gray-200">
              <tr>
                <th class="p-4 text-left font-semibold text-gray-700 text-sm uppercase">ID</th>
                <th class="p-4 text-left font-semibold text-gray-700 text-sm uppercase">Email</th>
                <th class="p-4 text-left font-semibold text-gray-700 text-sm uppercase">Name</th>
                <th class="p-4 text-left font-semibold text-gray-700 text-sm uppercase">Role</th>
                <th class="p-4 text-left font-semibold text-gray-700 text-sm uppercase">Joined</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50 transition-colors">
                <td class="p-4 border-b border-gray-200 text-gray-500">{{ user.id }}</td>
                <td class="p-4 border-b border-gray-200 text-gray-500">{{ user.email }}</td>
                <td class="p-4 border-b border-gray-200 text-gray-500">{{ user.firstName }} {{ user.lastName }}</td>
                <td class="p-4 border-b border-gray-200 text-gray-500">{{ user.role }}</td>
                <td class="p-4 border-b border-gray-200 text-gray-500">{{ formatDate(user.createAt) }}</td>
              </tr>
            </tbody>
          </table>
        </section>
      </div>
    </main>
  </div>
</template>

<script>
import api from '../api-service.js';

export default {
  name: 'AdminPanel',
  data() {
    return {
      currentUser: null,
      users: [],
      totalUsers: 0,
      totalSongs: 0,
      generatedSongs: 0,
      loading: true
    };
  },
  async mounted() {
    this.currentUser = api.getCurrentUser();
    if (!this.currentUser || this.currentUser.role !== 'PlatformOwner') {
      this.$emit('go-to-dashboard');
      return;
    }

    await this.loadData();
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        const allUsers = await api.getAllUsers();
        const allSongs = await api.getAllSongs();
        
        this.users = allUsers;
        this.totalUsers = allUsers.length;
        this.totalSongs = allSongs.length;
        this.generatedSongs = allSongs.filter(s => s.status === 'Succeeded').length;
      } catch (error) {
        console.error('Failed to load admin data:', error);
      } finally {
        this.loading = false;
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    logout() {
      api.logout();
      this.$emit('logout');
    },
    goToDashboard() {
      this.$emit('go-to-dashboard');
    }
  }
};
</script>
