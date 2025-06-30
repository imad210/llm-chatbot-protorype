// app.js
// This is the main application entry point. It initializes all other modules
// and orchestrates their interactions.

// Import all necessary modules.
import StatusManager from './statusManager.js';
import ChatModule from './chatModule.js';
import ResultsModule from './resultsModule.js';

/**
 * ChatbotApp class orchestrates the initialization of all application modules.
 */
class ChatbotApp {
    constructor() {
        // List of modules to be initialized.
        this.modules = [StatusManager, ChatModule, ResultsModule];
    }

    /**
     * Initializes the application. It waits for the DOM to be fully loaded
     * before initializing individual modules.
     */
    init() {
        // Check if the DOM is already fully loaded.
        if (document.readyState === 'loading') {
            // If not, wait for the 'DOMContentLoaded' event before initializing modules.
            document.addEventListener('DOMContentLoaded', () => this.initializeModules());
        } else {
            // If already loaded, initialize modules immediately.
            this.initializeModules();
        }
    }

    /**
     * Iterates through the registered modules and calls their `init` method.
     * Includes basic error handling for module initialization.
     */
    initializeModules() {
        try {
            this.modules.forEach(module => {
                // Check if the module has an 'init' method before calling it.
                if (typeof module.init === 'function') {
                    module.init();
                }
            });
            console.log('Chatbot application initialized successfully');
        } catch (error) {
            console.error('Failed to initialize application:', error);
        }
    }
}

// Create an instance of the ChatbotApp and initialize it.
const app = new ChatbotApp();
app.init();

// Expose ChatModule methods globally. This is necessary because `onclick`
// attributes in HTML directly look for functions in the global scope.
// For modern JavaScript, it's generally preferred to attach event listeners
// programmatically within the modules themselves (e.g., `button.addEventListener('click', ...)`)
// but keeping this for compatibility with the original HTML structure.
window.ChatModule = ChatModule;

