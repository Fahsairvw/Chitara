<template>
  <div class="min-h-screen flex flex-col bg-gray-50">

    <!-- Header -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-5xl mx-auto px-6 h-[60px] flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 bg-gray-900 text-white rounded-md flex items-center justify-center text-sm">
            <i class="fas fa-music"></i>
          </div>
          <span class="font-bold text-[17px] tracking-tight">Chitara</span>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-sm text-gray-500" v-if="currentUser">
            {{ currentUser.firstName }} {{ currentUser.lastName }}
          </span>
          <button v-if="currentUser && currentUser.role === 'PlatformOwner'" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-[15px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" @click="$emit('go-to-admin')">
            <i class="fas fa-chart-bar"></i> Admin
          </button>
          <button class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-[15px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" @click="logout">
            <i class="fas fa-sign-out-alt"></i> Sign out
          </button>
        </div>
      </div>
    </header>

    <!-- Generating Banner (FR-11: app still usable) -->
    <div class="bg-yellow-50 border-b border-yellow-200 py-2.5 px-6 flex items-center justify-center gap-2.5 text-sm text-yellow-800" v-if="generatingActive">
      <i class="fas fa-circle-notch spin"></i>
      <span>Your song is being generated — you can keep browsing your library.</span>
    </div>

    <main class="max-w-5xl mx-auto px-6 py-8 w-full flex-1">

      <!-- Create Section (FR-03) -->
      <section class="mb-10">
        <div class="bg-white border border-gray-200 rounded-2xl p-6 px-8 flex items-center justify-between gap-4">
          <div>
            <h2 class="text-lg font-semibold mb-1">Create a new song</h2>
            <p class="text-sm text-gray-400">Generate a unique AI song based on your preferences</p>
          </div>
          <button
            id="create-song-btn"
            class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-[15px] font-medium transition-all bg-gray-900 text-white border border-gray-900 hover:bg-gray-800 hover:border-gray-800 disabled:opacity-45 whitespace-nowrap"
            @click="openGenerator"
            :disabled="generatingActive"
            :title="generatingActive ? 'One song is already generating. Please wait.' : ''"
          >
            <i class="fas fa-plus"></i>
            Generate Song
          </button>
        </div>
        <p v-if="generatingActive" class="mt-2.5 text-[13px] text-gray-400 flex items-center gap-1.5">
          <i class="fas fa-lock"></i>
          One song at a time — generation in progress
        </p>
      </section>

      <!-- Library Section -->
      <section>
        <div class="flex items-center justify-between mb-5">
          <h2 class="text-lg font-semibold">Your Library</h2>
          <div class="flex items-center gap-3.5">
            <span class="text-sm text-gray-400" v-if="!loading">{{ totalSongs }} song{{ totalSongs !== 1 ? 's' : '' }}</span>
            <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" @click="loadLibrary(currentPage)" :disabled="loading">
              <i :class="loading ? 'fas fa-circle-notch spin' : 'fas fa-arrows-rotate'"></i>
              Refresh
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!loading && songs.length === 0" class="text-center py-16 px-8 text-gray-500">
          <div class="w-16 h-16 bg-gray-50 border border-gray-200 rounded-full flex items-center justify-center text-2xl text-gray-400 mx-auto mb-5"><i class="fas fa-music"></i></div>
          <h3 class="text-lg font-semibold mb-1.5">No songs yet</h3>
          <p class="text-sm text-gray-400">Generate your first song to get started</p>
        </div>

        <!-- Song Grid -->
        <div v-else class="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-4">
          <div
            v-for="song in songs"
            :key="song.id"
            class="bg-white border border-gray-200 rounded-2xl overflow-hidden transition-all duration-150 hover:shadow-md hover:-translate-y-0.5"
            :class="{ 'border-red-300': song.status && song.status.toUpperCase() === 'FAILED' }"
          >
            <!-- Card Art -->
            <div class="h-[120px] flex items-center justify-center" :class="artClass(song)">
              <i v-if="song.status && ['GENERATING', 'PENDING'].includes(song.status.toUpperCase())" class="fas fa-circle-notch spin text-3xl text-white/60"></i>
              <i v-else-if="song.status && song.status.toUpperCase() === 'FAILED'" class="fas fa-exclamation text-3xl text-white/60"></i>
              <i v-else class="fas fa-music text-3xl text-white/60"></i>
            </div>

            <!-- Card Body -->
            <div class="p-4 pb-2">
              <div class="flex items-center justify-between mb-2">
                <span class="text-[11px] font-semibold tracking-wider px-2 py-0.5 rounded-full uppercase" :class="badgeClass(song.status)">
                  {{ displayStatus(song.status) }}
                </span>
                <span class="text-xs text-gray-400">{{ formatDate(song.createAt) }}</span>
              </div>
              <div v-if="editingSongId === song.id" class="flex items-center gap-2 mb-1">
                <input 
                  type="text" 
                  v-model="editingTitle" 
                  @keyup.enter="saveTitle(song)"
                  @keyup.esc="cancelEditTitle"
                  class="flex-1 min-w-0 px-2 py-1 border border-gray-400 rounded-md text-[15px] outline-none focus:border-gray-900"
                  ref="titleInput"
                  :disabled="isSavingTitle"
                />
                <div class="flex items-center gap-1">
                  <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" @click="saveTitle(song)" :disabled="isSavingTitle" title="Save">
                    <i class="fas fa-check text-green-700"></i>
                  </button>
                  <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" @click="cancelEditTitle" :disabled="isSavingTitle" title="Cancel">
                    <i class="fas fa-xmark"></i>
                  </button>
                </div>
              </div>
              <h3 v-else class="text-base font-semibold mb-1 truncate">{{ song.title }}</h3>
              <p class="text-[13px] text-gray-400" v-if="song.genre">{{ song.genre }}<span v-if="song.occasion"> · {{ song.occasion }}</span></p>
            </div>

            <!-- Card Actions -->
            <div class="px-4 py-3 flex items-center gap-2 border-t border-gray-200">
              <!-- Succeeded actions -->
              <template v-if="song.status && song.status.toUpperCase() === 'SUCCEEDED'">
                <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all bg-gray-900 text-white border border-gray-900 hover:bg-gray-800 hover:border-gray-800 disabled:opacity-45 whitespace-nowrap" @click="playSong(song)" title="Play">
                  <i class="fas fa-play"></i> Play
                </button>
                <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" @click="startEditTitle(song)" title="Rename">
                  <i class="fas fa-pen"></i>
                </button>
                <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" @click="downloadSong(song)" title="Download MP3">
                  <i class="fas fa-download"></i>
                </button>
                <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" @click="shareSong(song)" title="Copy share link">
                  <i class="fas fa-link"></i>
                </button>
              </template>

              <!-- Failed actions (FR-13) -->
              <template v-else-if="song.status && song.status.toUpperCase() === 'FAILED'">
                <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all bg-transparent text-red-500 border border-red-300 hover:bg-red-50 disabled:opacity-45 whitespace-nowrap" @click="retrySong(song)" title="Retry generation">
                  <i class="fas fa-rotate-right"></i> Retry
                </button>
                <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" @click="discardSong(song)" title="Discard">
                  <i class="fas fa-trash"></i>
                </button>
              </template>

              <!-- Generating: no action buttons -->
              <template v-else>
                <span class="text-[13px] text-gray-400 flex items-center gap-1.5"><i class="fas fa-hourglass-half"></i> Generating…</span>
              </template>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-center gap-4 mt-8" v-if="totalPages > 1">
          <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" :disabled="currentPage <= 1" @click="currentPage--">
            <i class="fas fa-chevron-left"></i> Prev
          </button>
          <span class="text-sm text-gray-500">Page {{ currentPage }} / {{ totalPages }}</span>
          <button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all border border-gray-200 bg-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900 disabled:opacity-45 whitespace-nowrap" :disabled="currentPage >= totalPages" @click="currentPage++">
            Next <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </section>
    </main>

    <!-- Share toast -->
    <div class="fixed bottom-6 left-1/2 -translate-x-1/2 px-5 py-3 rounded-xl text-sm flex items-center gap-2 shadow-xl z-50" v-if="toastMessage" :class="toastType === 'danger' ? 'bg-red-500 text-white' : toastType === 'warning' ? 'bg-yellow-500 text-white' : 'bg-gray-900 text-white'">
      <i v-if="toastType === 'success'" class="fas fa-check-circle"></i>
      <i v-else-if="toastType === 'warning'" class="fas fa-exclamation-triangle"></i>
      <i v-else class="fas fa-exclamation-circle"></i>
      {{ toastMessage }}
    </div>

    <!-- Song Generator Modal (FR-04 through FR-13) -->
    <SongGenerator
      v-if="showGenerator"
      :userId="currentUser.id"
      :libraryId="library?.id || 1"
      @close="handleGeneratorClose"
      @song-generating="onSongGenerating"
    />

    <!-- Song Player Modal (FR-17, FR-18) -->
    <SongPlayer
      v-if="playingSong"
      :song="playingSong"
      @close="playingSong = null"
    />
  </div>
</template>

<script>
import api from '../api-service.js';
import SongGenerator from './SongGenerator.vue';
import SongPlayer from './SongPlayer.vue';

export default {
  name: 'DashboardView',
  components: { SongGenerator, SongPlayer },
  emits: ['logout', 'go-to-admin'],
  data() {
    return {
      currentUser: null,
      library: null,
      songs: [],
      loading: true,
      showGenerator: false,
      playingSong: null,
      generatingActive: false,
      currentPage: 1,
      totalPages: 1,
      totalSongs: 0,
      pageSize: 10,
      refreshInterval: null,
      toastMessage: '',
      toastType: 'success',
      toastTimer: null,
      editingSongId: null,
      editingTitle: '',
      isSavingTitle: false
    };
  },
  async mounted() {
    this.currentUser = api.getCurrentUser();
    if (!this.currentUser) { this.$emit('logout'); return; }
    await this.loadLibrary();
    this.refreshInterval = setInterval(() => {
      this.loadLibrary(this.currentPage);
      this.updateGeneratingStatus();
    }, 4000);
  },
  beforeUnmount() {
    if (this.refreshInterval) clearInterval(this.refreshInterval);
  },
  methods: {
    async loadLibrary(page = 1) {
      this.loading = true;
      try {
        const data = await api.getUserLibrary(this.currentUser.id, page);
        this.library = data.library;
        // Sort newest first (FR-16)
        const sorted = [...(data.songs || [])].sort(
          (a, b) => new Date(b.createAt) - new Date(a.createAt)
        );
        this.songs = sorted;
        this.currentPage = page;
        this.totalPages = Math.max(1, Math.ceil(data.total / this.pageSize));
        this.totalSongs = data.total;
        this.updateGeneratingStatus();
      } catch (e) {
        console.error('Failed to load library:', e);
      } finally {
        this.loading = false;
      }
    },
    updateGeneratingStatus() {
      this.generatingActive = this.songs.some(
        s => s.status && ['GENERATING', 'PENDING'].includes(s.status.toUpperCase())
      );
    },
    openGenerator() { this.showGenerator = true; },
    onSongGenerating(payload) {
      this.generatingActive = true;
      if (payload && payload.isDuplicate) {
        this.showToast('Warning: A song with this name already exists.', 'warning');
      }
    },
    handleGeneratorClose() {
      this.showGenerator = false;
      this.loadLibrary(this.currentPage);
    },
    playSong(song) { this.playingSong = song; },
    async retrySong(song) {
      // Retry: show generator with pre-filled data is ideal, but for now re-submit same data
      try {
        const songData = {
          title: song.title,
          genre: song.genre,
          occasion: song.occasion,
          mood: song.mood,
          description: song.description,
          user: this.currentUser.id,
          library: this.library?.id || 1
        };
        await api.generateSong(songData);
        this.showToast('Retrying song generation…', 'success');
        this.generatingActive = true;
        setTimeout(() => this.loadLibrary(this.currentPage), 1500);
      } catch (e) {
        this.showToast('Retry failed. Please try again.', 'danger');
      }
    },
    async discardSong(song) {
      try {
        await api.deleteSong(song.id);
        this.songs = this.songs.filter(s => s.id !== song.id);
        this.totalSongs = Math.max(0, this.totalSongs - 1);
      } catch(e) {
        this.showToast('Failed to delete song.', 'danger');
      }
    },
    downloadSong(song) {
      const link = document.createElement('a');
      link.href = song.link;
      link.download = `${song.title}.mp3`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    shareSong(song) {
      const shareUrl = `${window.location.origin}/#/shared/${song.id}`;
      navigator.clipboard.writeText(shareUrl).then(() => {
        this.showToast('Share link copied to clipboard!', 'success');
      });
    },
    startEditTitle(song) {
      this.editingSongId = song.id;
      this.editingTitle = song.title;
      this.$nextTick(() => {
        if (this.$refs.titleInput && this.$refs.titleInput[0]) {
          this.$refs.titleInput[0].focus();
        } else if (this.$refs.titleInput) {
          this.$refs.titleInput.focus();
        }
      });
    },
    cancelEditTitle() {
      this.editingSongId = null;
      this.editingTitle = '';
    },
    async saveTitle(song) {
      if (!this.editingTitle.trim()) {
        this.showToast('Song name cannot be empty', 'danger');
        return;
      }
      
      if (this.editingTitle.trim() === song.title) {
        this.cancelEditTitle();
        return;
      }
      
      this.isSavingTitle = true;
      try {
        const newTitle = this.editingTitle.trim();
        const allSongs = await api.getAllSongs();
        const userSongs = allSongs.filter(s => s.user === this.currentUser.id && s.id !== song.id);
        const isDuplicate = userSongs.some(s => s.title.toLowerCase() === newTitle.toLowerCase());
        
        if (isDuplicate) {
          this.showToast('Warning: A song with this name already exists.', 'warning');
        }
        
        await api.updateSong(song.id, { title: newTitle });
        
        song.title = newTitle;
        if (!isDuplicate) {
          this.showToast('Song renamed successfully!', 'success');
        }
        this.cancelEditTitle();
      } catch (e) {
        this.showToast('Failed to rename song.', 'danger');
      } finally {
        this.isSavingTitle = false;
      }
    },
    logout() {
      api.logout();
      this.$emit('logout');
    },
    formatDate(date) {
      if (!date) return '';
      return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },
    displayStatus(status) {
      if (!status) return '';
      const map = { SUCCEEDED: 'Ready', GENERATING: 'Generating', PENDING: 'Pending', FAILED: 'Failed' };
      return map[status.toUpperCase()] || status;
    },
    badgeClass(status) {
      if (!status) return '';
      const s = status.toUpperCase();
      if (s === 'SUCCEEDED') return 'bg-green-50 text-green-800';
      if (s === 'FAILED') return 'bg-red-50 text-red-800';
      return 'bg-yellow-50 text-yellow-800';
    },
    artClass(song) {
      if (!song.status) return 'bg-gradient-to-br from-[#1c1c1c] to-[#3a3a3a]';
      const s = song.status.toUpperCase();
      if (s === 'FAILED') return 'bg-gradient-to-br from-[#4a1d1d] to-[#7f1d1d]';
      if (s === 'GENERATING' || s === 'PENDING') return 'bg-gradient-to-br from-[#1e3a5f] to-[#2d5a8e]';
      return 'bg-gradient-to-br from-[#1c1c1c] to-[#3a3a3a]';
    },
    showToast(msg, type = 'success') {
      this.toastMessage = msg;
      this.toastType = type;
      if (this.toastTimer) clearTimeout(this.toastTimer);
      this.toastTimer = setTimeout(() => { this.toastMessage = ''; }, 3000);
    }
  },
  watch: {
    currentPage(newPage) { this.loadLibrary(newPage); }
  }
};
</script>
