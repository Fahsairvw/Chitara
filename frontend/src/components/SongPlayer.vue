<template>
  <div class="fixed inset-0 bg-black/55 flex items-center justify-center z-[1000] p-6" @click="close">
    <div class="bg-white rounded-2xl w-full max-w-[420px] shadow-2xl overflow-hidden relative" @click.stop>

      <!-- Header -->
      <div class="flex items-center justify-between px-5 py-4 border-b border-gray-200">
        <div class="flex items-center gap-2 text-[13px] font-medium text-gray-500 uppercase tracking-wider">
          <i class="fas fa-music animate-[spin_3s_linear_infinite]"></i>
          Now Playing
        </div>
        <button class="w-[30px] h-[30px] rounded-md flex items-center justify-center text-gray-400 text-sm cursor-pointer transition-colors hover:bg-gray-50 hover:text-gray-900 bg-transparent border-none p-0" @click="close"><i class="fas fa-times"></i></button>
      </div>

      <!-- Player Body -->
      <div class="p-6 flex flex-col gap-5">
        <!-- Album Art -->
        <div class="w-[140px] h-[140px] bg-gradient-to-br from-[#1c1c1c] to-[#3a3a3a] rounded-2xl flex items-center justify-center text-white/50 text-[40px] mx-auto shadow-sm">
          <i class="fas fa-music"></i>
        </div>

        <!-- Song Info -->
        <div class="text-center">
          <h2 class="text-lg mb-1 font-bold text-gray-900">{{ song.title }}</h2>
          <p class="text-sm text-gray-400 m-0">{{ [song.genre, song.occasion].filter(Boolean).join(' · ') }}</p>
          <p class="text-sm text-gray-400 m-0 mt-1" v-if="song.mood">{{ song.mood }}</p>
        </div>

        <!-- Audio Player (FR-17, FR-18) -->
        <div class="flex flex-col gap-4" v-if="song.link">
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

          <!-- Control Buttons (FR-18: play, pause, forward, backward) -->
          <div class="flex items-center justify-center gap-5">
            <button class="flex flex-col items-center justify-center gap-0.5 w-11 h-11 rounded-full bg-gray-50 border border-gray-200 text-gray-500 text-base transition-colors cursor-pointer hover:bg-gray-200 hover:text-gray-900 relative" title="Back 10s" @click="skipBack">
              <i class="fas fa-rotate-left"></i>
              <span class="text-[9px] font-semibold absolute bottom-1">10</span>
            </button>
            <button class="flex flex-col items-center justify-center gap-0.5 !w-14 !h-14 rounded-full !bg-gray-900 !text-white border !border-gray-900 text-xl transition-colors cursor-pointer hover:!bg-gray-800 relative" @click="togglePlay" :title="playing ? 'Pause' : 'Play'">
              <i :class="playing ? 'fas fa-pause' : 'fas fa-play'"></i>
            </button>
            <button class="flex flex-col items-center justify-center gap-0.5 w-11 h-11 rounded-full bg-gray-50 border border-gray-200 text-gray-500 text-base transition-colors cursor-pointer hover:bg-gray-200 hover:text-gray-900 relative" title="Forward 10s" @click="skipForward">
              <i class="fas fa-rotate-right"></i>
              <span class="text-[9px] font-semibold absolute bottom-1">10</span>
            </button>
          </div>

          <!-- Volume -->
          <div class="flex items-center gap-2.5">
            <button class="text-gray-400 text-sm w-6 shrink-0 cursor-pointer transition-colors hover:text-gray-600 bg-transparent border-none p-0" @click="toggleMute">
              <i :class="muted ? 'fas fa-volume-xmark' : volume > 0.5 ? 'fas fa-volume-high' : 'fas fa-volume-low'"></i>
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
        </div>

        <div v-else class="text-center p-6 text-gray-400 text-sm">
          <i class="fas fa-hourglass-half text-2xl mb-2 block"></i>
          <p class="m-0">Song is still generating…</p>
        </div>

        <!-- Action Buttons (FR-19, FR-20) -->
        <div class="grid grid-cols-2 gap-2" v-if="song.link">
          <button class="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium border transition-colors cursor-pointer whitespace-nowrap bg-gray-900 text-white border-gray-900 hover:bg-gray-800" @click="downloadSong">
            <i class="fas fa-download"></i> Download MP3
          </button>
          <button class="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium border transition-colors cursor-pointer whitespace-nowrap bg-transparent text-gray-500 border-gray-200 hover:bg-gray-50 hover:text-gray-900" @click="shareSong">
            <i class="fas fa-link"></i> Copy Link
          </button>
        </div>
      </div>

      <!-- Share toast -->
      <div class="absolute bottom-0 left-0 right-0 bg-green-600 text-white p-2.5 text-center text-sm flex items-center justify-center gap-1.5" v-if="copied">
        <i class="fas fa-check-circle"></i> Link copied!
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SongPlayer',
  props: {
    song: { type: Object, required: true }
  },
  emits: ['close'],
  data() {
    return {
      playing: false,
      currentTime: 0,
      duration: 0,
      volume: 0.85,
      muted: false,
      copied: false,
      copiedTimer: null
    };
  },
  mounted() {
    if (this.$refs.audio) {
      this.$refs.audio.volume = this.volume;
    }
  },
  beforeUnmount() {
    if (this.$refs.audio) this.$refs.audio.pause();
    if (this.copiedTimer) clearTimeout(this.copiedTimer);
  },
  methods: {
    togglePlay() {
      const a = this.$refs.audio;
      if (!a) return;
      if (this.playing) { a.pause(); } else { a.play(); }
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
    onEnded() {
      this.playing = false;
      this.currentTime = 0;
    },
    seek(e) {
      const a = this.$refs.audio;
      if (a) { a.currentTime = parseFloat(e.target.value); }
    },
    // FR-18: backward navigation
    skipBack() {
      const a = this.$refs.audio;
      if (a) a.currentTime = Math.max(0, a.currentTime - 10);
    },
    // FR-18: forward navigation
    skipForward() {
      const a = this.$refs.audio;
      if (a) a.currentTime = Math.min(this.duration, a.currentTime + 10);
    },
    toggleMute() {
      const a = this.$refs.audio;
      this.muted = !this.muted;
      if (a) a.muted = this.muted;
    },
    setVolume(e) {
      this.volume = parseFloat(e.target.value);
      const a = this.$refs.audio;
      if (a) {
        a.volume = this.volume;
        a.muted = this.volume === 0;
        this.muted = this.volume === 0;
      }
    },
    fmtTime(s) {
      if (!s || isNaN(s)) return '0:00';
      const m = Math.floor(s / 60);
      const sec = Math.floor(s % 60).toString().padStart(2, '0');
      return `${m}:${sec}`;
    },
    // FR-19
    downloadSong() {
      if (!this.song.link) return;
      const a = document.createElement('a');
      a.href = this.song.link;
      a.download = `${this.song.title}.mp3`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
    // FR-20
    shareSong() {
      const url = `${window.location.origin}/#/shared/${this.song.id}`;
      navigator.clipboard.writeText(url).then(() => {
        this.copied = true;
        if (this.copiedTimer) clearTimeout(this.copiedTimer);
        this.copiedTimer = setTimeout(() => { this.copied = false; }, 2500);
      });
    },
    close() {
      this.$emit('close');
    }
  }
};
</script>
