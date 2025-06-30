// chatModule.js
// This module manages the chat interface, including sending messages,
// displaying user and bot messages, and handling loading states.

import ApiService from './apiService.js'; // Import the API service for sending queries.
import Utils from './utils.js';           // Import utility functions for DOM manipulation.
import StatusManager from './statusManager.js'; // Import StatusManager to update backend status on errors.
import ResultsModule from './resultsModule.js'; // Import ResultsModule to display analysis results.

const ChatModule = {
    container: null,    // Reference to the chat messages container.
    input: null,        // Reference to the message input field.
    sendButton: null,   // Reference to the send message button.
    isLoading: false,   // Boolean to track if a message is currently being processed.

    /**
     * Initializes the ChatModule by getting references to necessary DOM elements
     * and setting initial focus.
     */
    init() {
        this.container = document.getElementById('chatContainer');
        this.input = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        
        // Ensure the input field is focused when the app loads for immediate user interaction.
        this.input?.focus(); 
    },

    /**
     * Handles key press events on the input field, specifically listening for 'Enter' key
     * to send a message.
     * @param {KeyboardEvent} event - The keyboard event object.
     */
    handleKeyPress(event) {
        // If the 'Enter' key is pressed and the system is not already loading, send the message.
        if (event.key === 'Enter' && !this.isLoading) {
            this.sendMessage();
        }
    },

    /**
     * Asynchronously sends the user's message to the backend, displays responses,
     * and handles loading states and errors.
     */
    async sendMessage() {
        if (this.isLoading) return; // Prevent sending multiple messages while one is in progress.

        const message = this.input.value.trim(); // Get and trim the message from the input field.
        if (!message) return; // Do nothing if the message is empty.

        // Add the user's message to the chat display.
        this.addMessage(message, 'user');
        this.input.value = ''; // Clear the input field after sending.
        
        // Set the loading state to disable input and show a loading indicator.
        this.setLoading(true);
        
        try {
            // Send the user query to the backend API.
            const data = await ApiService.sendQuery(message);
            
            // Display the analysis results in the results section.
            ResultsModule.displayResults(data);
            
            // Add a confirmation message from the bot to the chat.
            const botMessage = 'Saya telah menganalisis data berdasarkan pertanyaan anda. Lihat keputusan di sebelah kanan.';
            this.addMessage(botMessage, 'bot');

        } catch (error) {
            console.error('Error sending message or processing response:', error);
            // Display an error message from the bot if something goes wrong.
            const errorMessage = `Maaf, terdapat ralat: ${error.message}`;
            this.addMessage(errorMessage, 'bot');
            // Update the backend status to 'offline' if there's an API error.
            StatusManager.updateStatus('offline');
        } finally {
            // Always reset the loading state, regardless of success or failure.
            this.setLoading(false);
        }
    },

    /**
     * Adds a new message to the chat container.
     * @param {string} content - The text content of the message.
     * @param {'user'|'bot'} sender - The sender of the message ('user' or 'bot').
     */
    addMessage(content, sender) {
        if (!this.container) return; // Ensure the chat container exists.

        // Create a new message div using the utility function.
        const messageDiv = Utils.createElement('div', `message ${sender}-message`);
        messageDiv.textContent = content; // Set the message text.
        
        this.container.appendChild(messageDiv); // Append the new message to the container.
        // Scroll to the bottom of the chat container to show the latest message.
        this.container.scrollTop = this.container.scrollHeight;
    },

    /**
     * Sets the loading state of the chat interface, enabling/disabling input
     * and showing/hiding a loading spinner on the send button.
     * @param {boolean} loading - True to set loading state, false to unset.
     */
    setLoading(loading) {
        this.isLoading = loading; // Update the internal loading flag.
        
        if (this.sendButton && this.input) {
            if (loading) {
                // Show a loading spinner inside the button.
                this.sendButton.innerHTML = '<div class="loading"></div>'; 
                this.sendButton.disabled = true; // Disable the button.
                this.input.disabled = true;      // Disable the input field.
            } else {
                this.sendButton.innerHTML = 'Hantar'; // Restore button text.
                this.sendButton.disabled = false;     // Enable the button.
                this.input.disabled = false;          // Enable the input field.
                this.input.focus();                   // Re-focus the input field.
            }
        }
    }
};

export default ChatModule; // Export the ChatModule object.
