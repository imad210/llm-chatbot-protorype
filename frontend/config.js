// config.js
// This module defines global configuration constants for the chatbot application.

const Config = {
    API_BASE_URL: 'http://localhost:8000', // Base URL for the backend API.
    HEALTH_CHECK_INTERVAL: 30000, // Interval (in milliseconds) for checking backend health.
    ANIMATION_DURATION: 300,     // Duration (in milliseconds) for UI animations.
    RETRY_ATTEMPTS: 3,           // Number of retry attempts for API calls.
    RETRY_DELAY: 1000            // Delay (in milliseconds) between retry attempts.
};

export default Config; // Export the Config object for use in other modules.
