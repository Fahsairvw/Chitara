import axios from 'axios';

// API Service - Handles all communication with Django backend
class ChitaraAPI {
    constructor(baseURL = 'http://localhost:8000/api') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('authToken');
    }

    // Headers with authentication
    getHeaders() {
        const headers = { 'Content-Type': 'application/json' };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    // User endpoints
    async registerUser(userData) {
        try {
            const response = await axios.post(`${this.baseURL}/users/`, userData);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async loginUser(email) {
        try {
            const response = await axios.get(`${this.baseURL}/users/`);
            const user = response.data.find(u => u.email === email);
            if (user) {
                this.token = `user_${user.id}`;
                localStorage.setItem('authToken', this.token);
                localStorage.setItem('currentUser', JSON.stringify(user));
                return user;
            }
            throw new Error('User not found');
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    // Google OAuth Login
    async loginWithGoogle(idToken) {
        try {
            const response = await axios.post(`${this.baseURL}/auth/google/`, {
                id_token: idToken
            });
            
            const { token, user } = response.data;
            this.token = token;
            localStorage.setItem('authToken', token);
            localStorage.setItem('currentUser', JSON.stringify(user));
            
            return user;
        } catch (error) {
            console.error('API: Google login error:', error);
            throw error.response?.data || { error: 'Google login failed', details: error.message };
        }
    }

    async getUser(userId) {
        try {
            const response = await axios.get(`${this.baseURL}/users/`);
            const users = response.data;
            const user = users.find(u => u.id === parseInt(userId));
            if (user) {
                return user;
            }
            throw new Error('User not found');
        } catch (error) {
            console.error('Error fetching user:', error);
            throw error.response?.data || error.message;
        }
    }

    async getAllUsers() {
        try {
            const response = await axios.get(`${this.baseURL}/users/`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    // Library endpoints
    async getUserLibrary(userId, page = 1) {
        try {
            console.log('Fetching all songs from API...');
            // Get all songs and filter by user
            const response = await axios.get(`${this.baseURL}/songs/`);
            console.log('Response from API:', response.data);
            
            const allSongs = response.data;
            console.log('Total songs from API:', allSongs.length);
            
            const userSongs = allSongs.filter(song => {
                console.log('Checking song:', song.id, 'user:', song.user, 'userId:', userId);
                return song.user === userId;
            });
            console.log('User songs filtered:', userSongs.length);
            
            // Sort newest first BEFORE pagination
            userSongs.sort((a, b) => new Date(b.createAt) - new Date(a.createAt));
            
            // Pagination
            const pageSize = 10;
            const start = (page - 1) * pageSize;
            const songs = userSongs.slice(start, start + pageSize);
            
            return {
                library: { id: 1, name: 'My Library', user: userId },
                songs: songs,
                total: userSongs.length
            };
        } catch (error) {
            console.error('Error fetching library:', error);
            throw error.response?.data || error.message;
        }
    }

    async getLibrary(libraryId, page = 1) {
        try {
            const response = await axios.get(
                `${this.baseURL}/libraries/${libraryId}/?page=${page}`
            );
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    // Choices endpoint
    async getChoices() {
        try {
            const response = await axios.get(`${this.baseURL}/choices/`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    // Song endpoints
    async getAllSongs() {
        try {
            const response = await axios.get(`${this.baseURL}/songs/`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async getSong(songId) {
        try {
            const response = await axios.get(`${this.baseURL}/songs/${songId}/`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async generateSong(songData) {
        try {
            const response = await axios.post(`${this.baseURL}/songs/generate/`, songData);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async checkSongStatus(taskId) {
        try {
            const response = await axios.get(`${this.baseURL}/songs/status/${taskId}/`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async updateSong(songId, data) {
        try {
            const response = await axios.patch(`${this.baseURL}/songs/${songId}/`, data);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async deleteSong(songId) {
        try {
            const response = await axios.delete(`${this.baseURL}/songs/${songId}/`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async downloadSong(songId, userId) {
        try {
            const response = await axios.get(
                `${this.baseURL}/songs/${songId}/download/`,
                { headers: this.getHeaders() }
            );
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    // Check if authenticated
    isAuthenticated() {
        return !!this.token;
    }

    // Get current user
    getCurrentUser() {
        const user = localStorage.getItem('currentUser');
        return user ? JSON.parse(user) : null;
    }

    // Logout
    logout() {
        this.token = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('currentUser');
    }
}

export default new ChitaraAPI();
