// utils.js
// This module provides a collection of utility functions used across the application,
// such as DOM manipulation, data formatting, and common helpers.

const Utils = {
    /**
     * Creates a new HTML element with optional class name and text content.
     * @param {string} tag - The HTML tag name (e.g., 'div', 'p', 'span').
     * @param {string} [className] - Optional CSS class name(s) to add to the element.
     * @param {string} [content] - Optional text content for the element.
     * @returns {HTMLElement} The newly created HTML element.
     */
    createElement: (tag, className, content) => {
        const element = document.createElement(tag);
        if (className) element.className = className; // Apply class if provided.
        if (content) element.textContent = content;   // Set text content if provided.
        return element;
    },

    /**
     * Formats a number according to the Malay (Malaysia) locale.
     * This adds thousands separators.
     * @param {number} num - The number to format.
     * @returns {string} The formatted number string.
     */
    formatNumber: (num) => {
        // Using 'ms-MY' locale for number formatting (e.g., 10,000).
        return new Intl.NumberFormat('ms-MY').format(num);
    },

    /**
     * Debounces a function, ensuring it's only called after a specified delay
     * since the last time it was invoked. Useful for limiting the rate of
     * function calls (e.g., on resize or input events).
     * @param {Function} func - The function to debounce.
     * @param {number} wait - The delay (in milliseconds) to wait before calling the function.
     * @returns {Function} The debounced function.
     */
    debounce: (func, wait) => {
        let timeout; // Stores the timeout ID.
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout); // Clear any existing timeout.
                func(...args);         // Call the original function.
            };
            clearTimeout(timeout);     // Clear timeout if function is called again before delay.
            timeout = setTimeout(later, wait); // Set new timeout.
        };
    },

    /**
     * Formats a snake_case key string into a human-readable title case.
     * E.g., "user_name" becomes "User Name".
     * @param {string} key - The string key to format.
     * @returns {string} The formatted string.
     */
    formatKey: (key) => {
        return key.replace(/_/g, ' ') // Replace underscores with spaces.
                  .replace(/\b\w/g, l => l.toUpperCase()); // Capitalize the first letter of each word.
    },

    /**
     * Escapes HTML special characters in a string to prevent Cross-Site Scripting (XSS) attacks.
     * @param {string} text - The raw text string to escape.
     * @returns {string} The HTML-escaped string.
     */
    escapeHtml: (text) => {
        const div = document.createElement('div'); // Create a temporary div element.
        div.textContent = text;                      // Set the text content, which automatically escapes HTML.
        return div.innerHTML;                        // Retrieve the escaped HTML.
    }
};

export default Utils; // Export the Utils object.
