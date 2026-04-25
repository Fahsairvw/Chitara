<template>
  <!-- Dimmed backdrop -->
  <div class="fixed inset-0 bg-black/45 flex items-center justify-center z-[1000] p-6" @click="handleOverlayClick">
    <div class="bg-white rounded-2xl w-full max-w-[520px] shadow-2xl flex flex-col max-h-[95vh] overflow-hidden" @click.stop>

      <!-- Step 1: Form (FR-04, FR-05, FR-06) -->
      <template v-if="step === 1">
        <div class="px-6 py-5 border-b border-gray-200 flex items-center justify-between shrink-0">
          <h2 class="text-[17px] font-semibold">New Song</h2>
          <button class="w-8 h-8 rounded-md flex items-center justify-center text-gray-400 text-sm transition-colors hover:bg-gray-50 hover:text-gray-900 cursor-pointer" @click="close"><i class="fas fa-times"></i></button>
        </div>

        <form class="p-6 overflow-y-auto flex-1" @submit.prevent="goToConfirm" novalidate>
          <div class="mb-4">
            <div class="mb-4">
              <label for="title" class="block text-[13px] font-medium mb-1.5 text-gray-500">Song Title <span class="text-red-500">*</span></label>
              <input
                id="title"
                v-model="form.title"
                type="text"
                placeholder="e.g. Midnight Serenade"
                class="w-full px-3 py-2.5 border border-gray-200 rounded-lg text-[15px] text-gray-900 bg-white transition-all outline-none focus:border-gray-400 focus:shadow-[0_0_0_3px_rgba(17,17,17,0.06)]"
                :class="{ '!border-red-500': errors.title }"
                autocomplete="off"
              />
              <span class="block text-xs text-red-500 mt-1" v-if="errors.title">{{ errors.title }}</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3 mb-4">
            <div>
              <label for="genre" class="block text-[13px] font-medium mb-1.5 text-gray-500">Genre <span class="text-red-500">*</span></label>
              <select id="genre" v-model="form.genre" class="w-full px-3 py-2.5 border border-gray-200 rounded-lg text-[15px] text-gray-900 bg-white transition-all outline-none focus:border-gray-400 focus:shadow-[0_0_0_3px_rgba(17,17,17,0.06)]" :class="{ '!border-red-500': errors.genre }">
                <option value="">Select genre</option>
                <option
                  v-for="g in genres"
                  :key="g.value"
                  :value="g.value"
                >{{ g.label }}</option>
              </select>
              <span class="block text-xs text-red-500 mt-1" v-if="errors.genre">{{ errors.genre }}</span>
            </div>

            <div>
              <label for="occasion" class="block text-[13px] font-medium mb-1.5 text-gray-500">Occasion <span class="text-red-500">*</span></label>
              <select id="occasion" v-model="form.occasion" class="w-full px-3 py-2.5 border border-gray-200 rounded-lg text-[15px] text-gray-900 bg-white transition-all outline-none focus:border-gray-400 focus:shadow-[0_0_0_3px_rgba(17,17,17,0.06)]" :class="{ '!border-red-500': errors.occasion }">
                <option value="">Select occasion</option>
                <option
                  v-for="o in occasions"
                  :key="o.value"
                  :value="o.value"
                >{{ o.label }}</option>
              </select>
              <span class="block text-xs text-red-500 mt-1" v-if="errors.occasion">{{ errors.occasion }}</span>
            </div>
          </div>

          <div class="mb-4">
            <label for="mood" class="block text-[13px] font-medium mb-1.5 text-gray-500">Mood / Feeling</label>
            <input
              id="mood"
              v-model="form.mood"
              type="text"
              placeholder="Happy, Melancholic, อบอุ่น, 평화로운…"
              class="w-full px-3 py-2.5 border border-gray-200 rounded-lg text-[15px] text-gray-900 bg-white transition-all outline-none focus:border-gray-400 focus:shadow-[0_0_0_3px_rgba(17,17,17,0.06)]"
            />
            <span class="block text-xs text-gray-400 mt-1">You can type in any language (FR-06)</span>
          </div>

          <div class="mb-4">
            <label for="description" class="block text-[13px] font-medium mb-1.5 text-gray-500">Song Description / Prompt</label>
            <textarea
              id="description"
              v-model="form.description"
              rows="3"
              placeholder="Describe what you want… ใช้ภาษาไทยได้เลย, can use any language"
              class="w-full px-3 py-2.5 border border-gray-200 rounded-lg text-[15px] text-gray-900 bg-white transition-all outline-none focus:border-gray-400 focus:shadow-[0_0_0_3px_rgba(17,17,17,0.06)] resize-none"
            ></textarea>
          </div>

          <div class="px-6 py-4 border-t border-gray-200 flex gap-2 justify-end shrink-0 -mx-6 -mb-6 mt-6">
            <button type="button" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all bg-transparent text-gray-500 border border-gray-200 hover:bg-gray-50 hover:text-gray-900 cursor-pointer whitespace-nowrap" @click="close">Cancel</button>
            <button type="submit" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all bg-gray-900 text-white border border-gray-900 hover:bg-gray-800 cursor-pointer whitespace-nowrap">
              Review & Confirm <i class="fas fa-arrow-right"></i>
            </button>
          </div>
        </form>
      </template>

      <!-- Step 2: Confirmation (FR-08) -->
      <template v-else-if="step === 2">
        <div class="px-6 py-5 border-b border-gray-200 flex items-center justify-between shrink-0">
          <h2 class="text-[17px] font-semibold">Confirm Your Song</h2>
          <button class="w-8 h-8 rounded-md flex items-center justify-center text-gray-400 text-sm transition-colors hover:bg-gray-50 hover:text-gray-900 cursor-pointer" @click="close"><i class="fas fa-times"></i></button>
        </div>

        <div class="p-6 overflow-y-auto flex-1">
          <p class="text-sm text-gray-500 mb-4">Please review your song details before generating.</p>

          <div class="border border-gray-200 rounded-lg overflow-hidden">
            <div class="flex gap-4 py-3 px-4 border-b border-gray-200 text-[15px] last:border-b-0">
              <span class="font-medium text-gray-500 min-w-[90px] shrink-0">Title</span>
              <span class="text-gray-900 whitespace-nowrap overflow-hidden text-ellipsis">{{ form.title }}</span>
            </div>
            <div class="flex gap-4 py-3 px-4 border-b border-gray-200 text-[15px] last:border-b-0">
              <span class="font-medium text-gray-500 min-w-[90px] shrink-0">Genre</span>
              <span class="text-gray-900 whitespace-nowrap overflow-hidden text-ellipsis">{{ form.genre }}</span>
            </div>
            <div class="flex gap-4 py-3 px-4 border-b border-gray-200 text-[15px] last:border-b-0">
              <span class="font-medium text-gray-500 min-w-[90px] shrink-0">Occasion</span>
              <span class="text-gray-900 whitespace-nowrap overflow-hidden text-ellipsis">{{ form.occasion }}</span>
            </div>
            <div class="flex gap-4 py-3 px-4 border-b border-gray-200 text-[15px] last:border-b-0" v-if="form.mood">
              <span class="font-medium text-gray-500 min-w-[90px] shrink-0">Mood</span>
              <span class="text-gray-900 whitespace-nowrap overflow-hidden text-ellipsis">{{ form.mood }}</span>
            </div>
            <div class="flex gap-4 py-3 px-4 border-b border-gray-200 text-[15px] last:border-b-0" v-if="form.description">
              <span class="font-medium text-gray-500 min-w-[90px] shrink-0">Description</span>
              <span class="text-gray-900 whitespace-normal break-words">{{ form.description }}</span>
            </div>
          </div>
        </div>

        <!-- Generating state (FR-10) -->
        <div v-if="isGenerating" class="flex items-center justify-center gap-2.5 p-5 text-gray-500 text-[15px] border-t border-gray-200">
          <i class="fas fa-circle-notch spin"></i>
          <span>Starting generation…</span>
        </div>

        <!-- Error with retry/discard (FR-12, FR-13) -->
        <div v-if="submitError" class="mx-6 mb-0 px-4 py-3.5 bg-red-50 border border-red-300 rounded-lg flex items-start gap-3 text-red-500 text-[15px]">
          <i class="fas fa-exclamation-circle mt-1"></i>
          <div>
            <strong>Generation failed</strong>
            <p class="mt-1 text-red-900">{{ submitError }}</p>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-gray-200 flex gap-2 justify-end shrink-0" v-if="!isGenerating">
          <button class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all bg-transparent text-gray-500 border border-gray-200 hover:bg-gray-50 hover:text-gray-900 cursor-pointer whitespace-nowrap" @click="step = 1">
            <i class="fas fa-arrow-left"></i> Back
          </button>
          <button v-if="submitError" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all bg-transparent text-gray-500 border border-gray-200 hover:bg-gray-50 hover:text-gray-900 cursor-pointer whitespace-nowrap" @click="close">
            Discard
          </button>
          <button class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all bg-gray-900 text-white border border-gray-900 hover:bg-gray-800 cursor-pointer whitespace-nowrap disabled:opacity-45 disabled:cursor-default disabled:pointer-events-none" @click="generate" :disabled="isGenerating">
            <i class="fas fa-wand-magic-sparkles"></i>
            {{ submitError ? 'Retry' : 'Generate Song' }}
          </button>
        </div>
      </template>

    </div>
  </div>
</template>

<script>
import api from '../api-service.js';

export default {
  name: 'SongGenerator',
  props: {
    userId: { type: Number, required: true },
    libraryId: { type: Number, required: true }
  },
  emits: ['close', 'song-generating'],
  data() {
    return {
      step: 1,
      form: {
        title: '',
        genre: '',
        occasion: '',
        mood: '',
        description: ''
      },
      errors: {},
      isGenerating: false,
      submitError: '',
      genres: [],
      occasions: []
    };
  },
  async mounted() {
    try {
      const choices = await api.getChoices();
      this.genres = choices.genres;
      this.occasions = choices.occasions;
    } catch (e) {
      console.error('Failed to load choices from backend:', e);
    }
  },
  methods: {
    validateForm() {
      this.errors = {};
      if (!this.form.title.trim()) this.errors.title = 'Title is required';
      if (!this.form.genre) this.errors.genre = 'Please select a genre';
      if (!this.form.occasion) this.errors.occasion = 'Please select an occasion';
      return Object.keys(this.errors).length === 0;
    },
    goToConfirm() {
      if (this.validateForm()) this.step = 2;
    },
    async generate() {
      this.submitError = '';
      this.isGenerating = true;
      try {
        const allSongs = await api.getAllSongs();
        const userSongs = allSongs.filter(s => s.user === this.userId);
        const isDuplicate = userSongs.some(s => s.title.toLowerCase() === this.form.title.trim().toLowerCase());
        
        this.$emit('song-generating', { isDuplicate });
        
        const songData = {
          ...this.form,
          user: this.userId,
          library: this.libraryId
        };
        await api.generateSong(songData);
        // Close immediately — song will be tracked via polling (FR-11)
        this.close();
      } catch (e) {
        this.submitError = e?.error || e?.message || 'Generation request failed. Please try again.';
        this.isGenerating = false;
      }
    },
    handleOverlayClick() {
      if (!this.isGenerating) this.close();
    },
    close() {
      this.$emit('close');
    }
  }
};
</script>
