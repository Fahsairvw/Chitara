<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-[600px] mx-auto px-6 h-[60px] flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 bg-gray-900 text-white rounded-md flex items-center justify-center text-sm"><i class="fas fa-music"></i></div>
          <span class="font-bold text-[17px]">Chitara</span>
        </div>
        <span class="text-xs font-semibold uppercase tracking-wider text-gray-400 border border-gray-200 rounded-full px-2.5 py-0.5">Shared Song</span>
      </div>
    </header>

    <main class="flex-1 flex items-center justify-center p-8 px-6">
      <!-- Loading -->
      <div v-if="loading" class="text-center text-gray-500">
        <i class="fas fa-circle-notch spin text-3xl mb-3 text-gray-400 block"></i>
        <p>Loading song…</p>
      </div>

      <!-- Error -->
      <div v-else-if="!song" class="text-center text-gray-500">
        <div class="w-16 h-16 bg-gray-50 border border-gray-200 rounded-full flex items-center justify-center text-2xl text-gray-400 mx-auto mb-5"><i class="fas fa-music-slash"></i></div>
        <h2 class="text-xl font-semibold text-gray-900 mb-2">Song not found</h2>
        <p>This link may have expired or the song was deleted.</p>
      </div>

      <!-- Song Card -->
      <div v-else class="bg-white border border-gray-200 rounded-2xl p-8 w-full max-w-[440px] shadow-sm flex flex-col gap-6">
        <!-- Art -->
        <div class="w-[140px] h-[140px] bg-gradient-to-br from-[#1c1c1c] to-[#3a3a3a] rounded-2xl flex items-center justify-center text-white/50 text-[40px] mx-auto">
          <i v-if="song.status === 'GENERATING' || song.status === 'Generating'" class="fas fa-circle-notch spin"></i>
          <i v-else-if="song.status === 'FAILED' || song.status === 'Failed'" class="fas fa-exclamation text-red-500"></i>
          <i v-else class="fas fa-music"></i>
        </div>

        <!-- Info -->
        <div class="text-center">
          <h1 class="text-xl font-bold mb-1.5 text-gray-900">{{ song.title }}</h1>
          <p class="text-sm text-gray-400 m-0">{{ [song.genre, song.occasion].filter(Boolean).join(' · ') }}</p>
          <p class="text-sm text-gray-400 mt-1 mb-0" v-if="song.mood">{{ song.mood }}</p>
          <p class="text-sm text-gray-500 mt-3 leading-relaxed mb-0" v-if="song.description">{{ song.description }}</p>
        </div>

        <!-- Player (FR-17, FR-18) -->
        <div class="flex flex-col gap-4" v-if="song.link && (song.status === 'Succeeded' || song.status === 'SUCCEEDED')">
          <audio
            ref="audio"
            :src="song.link"
            @timeupdate="onTimeUpdate"
            @loadedmetadata="onMetadata"
            @ended="onEnded"
            preload="metadata"
          ></audio>

          <!-- Progress -->
          <div class="flex items-center gap-2">
            <span class="text-xs text-gray-400 min-w-[36px] text-center">{{ fmtTime(currentTime) }}</span>
            <input
              type="range"
              class="flex-1 h-1 bg-gray-200 rounded cursor-pointer appearance-none outline-none [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3.5 [&::-webkit-slider-thumb]:h-3.5 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-gray-900 [&::-webkit-slider-thumb]:cursor-pointer"
              :value="currentTime"
              :max="duration || 100"
              step="0.1"
              @input="seek"
            />
            <span class="text-xs text-gray-400 min-w-[36px] text-center">{{ fmtTime(duration) }}</span>
          </div>

          <!-- Controls (FR-18) -->
          <div class="flex items-center justify-center gap-5">
            <button class="flex flex-col items-center justify-center w-11 h-11 rounded-full bg-gray-50 border border-gray-200 text-gray-500 text-base cursor-pointer transition-colors hover:bg-gray-200 hover:text-gray-900 relative" @click="skipBack" title="Back 10s">
              <i class="fas fa-rotate-left"></i>
              <span class="text-[8px] font-bold absolute bottom-1">10</span>
            </button>
            <button class="flex flex-col items-center justify-center !w-14 !h-14 rounded-full !bg-gray-900 border !border-gray-900 !text-white text-xl cursor-pointer transition-colors hover:!bg-gray-800 relative" @click="togglePlay">
              <i :class="playing ? 'fas fa-pause' : 'fas fa-play'"></i>
            </button>
            <button class="flex flex-col items-center justify-center w-11 h-11 rounded-full bg-gray-50 border border-gray-200 text-gray-500 text-base cursor-pointer transition-colors hover:bg-gray-200 hover:text-gray-900 relative" @click="skipForward" title="Forward 10s">
              <i class="fas fa-rotate-right"></i>
              <span class="text-[8px] font-bold absolute bottom-1">10</span>
            </button>
          </div>

          <!-- Volume -->
          <div class="flex items-center gap-2.5">
            <button class="text-gray-400 text-sm cursor-pointer w-5 shrink-0 bg-transparent border-none p-0 hover:text-gray-600" @click="toggleMute">
              <i :class="muted ? 'fas fa-volume-xmark' : 'fas fa-volume-high'"></i>
            </button>
            <input
              type="range"
              class="flex-1 h-[3px] bg-gray-200 rounded cursor-pointer appearance-none outline-none [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-gray-900 [&::-webkit-slider-thumb]:cursor-pointer"
              min="0"
              max="1"
              step="0.05"
              :value="muted ? 0 : volume"
              @input="setVolume"
            />
          </div>

          <!-- Actions (FR-19, FR-20) -->
          <div class="grid grid-cols-2 gap-2">
            <button class="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium border transition-colors cursor-pointer bg-gray-900 text-white border-gray-900 hover:bg-gray-800" @click="download">
              <i class="fas fa-download"></i> Download MP3
            </button>
            <button class="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium border transition-colors cursor-pointer bg-transparent text-gray-500 border-gray-200 hover:bg-gray-50 hover:text-gray-900" @click="copyLink">
              <i class="fas fa-link"></i>
              {{ copied ? 'Copied!' : 'Copy Link' }}
            </button>
          </div>
        </div>

        <!-- Generating -->
        <div v-else-if="song.status === 'GENERATING' || song.status === 'Generating'" class="text-center p-4 rounded-lg text-sm flex flex-col items-center gap-2 bg-yellow-50 text-yellow-800">
          <i class="fas fa-hourglass-half text-2xl"></i>
          <p class="m-0 text-yellow-800">This song is still being generated. Check back later.</p>
        </div>

        <!-- Failed -->
        <div v-else-if="song.status === 'FAILED' || song.status === 'Failed'" class="text-center p-4 rounded-lg text-sm flex flex-col items-center gap-2 bg-red-50 text-red-600">
          <i class="fas fa-exclamation-circle text-2xl"></i>
          <p class="m-0 text-red-600">Generation of this song failed.</p>
        </div>
      </div>
    </main>

    <footer class="bg-white border-t border-gray-200 p-5 text-center text-[13px] text-gray-400">
      Created with <strong class="text-gray-600">Chitara</strong> — AI Music Generation
    </footer>
  </div>
</template>

<script>
import api from '../api-service.js';

export default {
  name: 'SharedSongView',
  props: { songId: { type: String, required: true } },
  data() {
    return {
      song: null,
      loading: true,
      playing: false,
      currentTime: 0,
      duration: 0,
      volume: 0.85,
      muted: false,
      copied: false
    };
  },
  async mounted() {
    try {
      this.song = await api.getSong(this.songId);
    } catch (e) {
      console.error('Failed to load shared song:', e);
    } finally {
      this.loading = false;
    }
  },
  beforeUnmount() {
    if (this.$refs.audio) this.$refs.audio.pause();
  },
  methods: {
    togglePlay() {
      const a = this.$refs.audio;
      if (!a) return;
      if (this.playing) a.pause(); else a.play();
      this.playing = !this.playing;
    },
    onTimeUpdate() {
      const a = this.$refs.audio;
      if (a) this.currentTime = a.currentTime;
    },
    onMetadata() {
      const a = this.$refs.audio;
      if (a) this.duration = a.duration;
    },
    onEnded() { this.playing = false; },
    seek(e) {
      const a = this.$refs.audio;
      if (a) a.currentTime = parseFloat(e.target.value);
    },
    skipBack() { const a = this.$refs.audio; if (a) a.currentTime = Math.max(0, a.currentTime - 10); },
    skipForward() { const a = this.$refs.audio; if (a) a.currentTime = Math.min(this.duration, a.currentTime + 10); },
    toggleMute() { this.muted = !this.muted; if (this.$refs.audio) this.$refs.audio.muted = this.muted; },
    setVolume(e) {
      this.volume = parseFloat(e.target.value);
      if (this.$refs.audio) this.$refs.audio.volume = this.volume;
    },
    fmtTime(s) {
      if (!s || isNaN(s)) return '0:00';
      return `${Math.floor(s / 60)}:${Math.floor(s % 60).toString().padStart(2, '0')}`;
    },
    download() {
      if (!this.song.link) return;
      const a = document.createElement('a');
      a.href = this.song.link;
      a.download = `${this.song.title}.mp3`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
    copyLink() {
      navigator.clipboard.writeText(window.location.href).then(() => {
        this.copied = true;
        setTimeout(() => { this.copied = false; }, 2500);
      });
    }
  }
};
</script>
