// statusManager.js
// This module manages the display of the backend connection status.

import ApiService from './apiService.js'; // Import the API service for health checks.
import Config from './config.js';         // Import configuration for intervals.

const StatusManager = {
    indicator: null, // Reference to the DOM element that displays the status.

    /**
     * Initializes the StatusManager by getting the status indicator element
     * and setting up periodic health checks.
     */
    init() {
        this.indicator = document.getElementById('statusIndicator'); // Get the status indicator element.
        this.checkHealth(); // Perform an initial health check on startup.
        // Set up an interval to periodically check the backend health.
        setInterval(() => this.checkHealth(), Config.HEALTH_CHECK_INTERVAL);
    },

    /**
     * Asynchronously checks the backend health using ApiService and updates the UI.
     */
    async checkHealth() {
        try {
            this.updateStatus('checking'); // Set status to 'checking' while the check is in progress.
            await ApiService.checkHealth(); // Await the health check from ApiService.
            this.updateStatus('online');   // If successful, set status to 'online'.
        } catch (error) {
            console.warn('Backend health check failed:', error.message); // Log any health check failures.
            this.updateStatus('offline'); // If failed, set status to 'offline'.
        }
    },

    /**
     * Updates the status indicator's text and CSS class based on the given status.
     * @param {'online'|'offline'|'checking'} status - The status to display.
     */
    updateStatus(status) {
        if (!this.indicator) return; // Exit if the indicator element is not found.

        // Define configuration for different status states.
        const statusConfig = {
            online: { text: '🟢 Backend Online', class: 'status-online' },
            offline: { text: '🔴 Backend Offline', class: 'status-offline' },
            checking: { text: '🟡 Checking...', class: 'status-checking' }
        };

        const config = statusConfig[status]; // Get the specific configuration for the current status.
        if (config) {
            this.indicator.textContent = config.text;     // Update the text content.
            this.indicator.className = `status-indicator ${config.class}`; // Update the CSS class.
        }
    }
};

export default StatusManager; // Export the StatusManager object.
