// apiService.js
// This module handles all communication with the backend API,
// including health checks and sending user queries.

import Config from './config.js'; // Import configuration constants.

const ApiService = {
    /**
     * Performs a health check on the backend API with retry logic and a timeout.
     * @param {number} [retries=Config.RETRY_ATTEMPTS] - The number of remaining retries.
     * @returns {Promise<Object>} A promise that resolves with the health status, or rejects on failure.
     */
    checkHealth: async (retries = Config.RETRY_ATTEMPTS) => {
        try {
            // Create an AbortController to implement a request timeout.
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000); // Set timeout for 5 seconds.

            // Fetch the health endpoint.
            const response = await fetch(`${Config.API_BASE_URL}/health`, {
                method: 'GET',
                signal: controller.signal // Associate the abort signal with the fetch request.
            });
            
            clearTimeout(timeoutId); // Clear the timeout if the fetch completes before the timeout.

            // Check if the response was successful (HTTP status 2xx).
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`); // Throw an error for non-OK responses.
            }
            
            return await response.json(); // Parse and return the JSON response.
        } catch (error) {
            // Handle specific AbortError for timeouts.
            if (error.name === 'AbortError') {
                console.warn('Backend health check timed out.');
            } else {
                console.error('Backend health check failed:', error);
            }

            // Retry if retries are remaining.
            if (retries > 0) {
                // Wait for a specified delay before retrying.
                await new Promise(resolve => setTimeout(resolve, Config.RETRY_DELAY));
                return ApiService.checkHealth(retries - 1); // Recursively call checkHealth with reduced retries.
            }
            throw error; // Re-throw the error if no retries left.
        }
    },

    /**
     * Sends a user query to the backend API for data analysis.
     * @param {string} query - The user's input query.
     * @returns {Promise<Object>} A promise that resolves with the analysis results, or rejects on error.
     */
    sendQuery: async (query) => {
        const response = await fetch(`${Config.API_BASE_URL}/ask`, {
            method: 'POST', // Use POST method for sending data.
            headers: {
                'Content-Type': 'application/json', // Specify content type as JSON.
            },
            body: JSON.stringify({ // Convert the query object to a JSON string.
                user_query: query
            })
        });

        // Check for HTTP errors.
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json(); // Parse the JSON response.
        
        // Check if the backend returned an application-level error.
        if (data.error) {
            throw new Error(data.error);
        }

        return data; // Return the processed data.
    }
};

export default ApiService; // Export the ApiService object.
