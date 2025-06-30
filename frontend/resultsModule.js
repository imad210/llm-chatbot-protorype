// resultsModule.js
// This module is responsible for displaying the data analysis results
// received from the backend in the designated results section.

import Utils from './utils.js'; // Import utility functions for formatting and DOM manipulation.

const ResultsModule = {
    container: null, // Reference to the DOM element where results will be displayed.

    /**
     * Initializes the ResultsModule by getting the reference to the results content container.
     */
    init() {
        this.container = document.getElementById('resultsContent'); // Get the results content container.
    },

    /**
     * Displays the parsed data analysis results in the results section.
     * @param {Object} data - The data object containing 'plan' and 'answer' from the backend.
     * @param {Object} data.plan - An object describing the filters applied (e.g., gender, state).
     * @param {Object} data.answer - An object containing the total count and grouped data.
     * @param {number} [data.answer.total] - The total count of people matching the criteria.
     * @param {Array<Object>} [data.answer.groups] - An array of grouped data, if applicable.
     */
    displayResults(data) {
        if (!this.container || !data) return; // Exit if container or data is missing.

        const { plan, answer } = data; // Destructure the plan and answer from the data.
        let html = ''; // Initialize an empty string to build the HTML content.
        
        // Display the total count if it exists in the answer.
        if (answer.total !== undefined) {
            html += `
                <div class="total-count">
                    📊 Jumlah Keseluruhan: ${Utils.formatNumber(answer.total)} orang
                </div>
            `;
        }

        // Generate and append the HTML for the search parameters (plan).
        html += this.generatePlanCard(plan);

        // Display grouped results if they exist and are not empty.
        if (answer.groups && answer.groups.length > 0) {
            html += this.generateGroupsCard(answer.groups);
        }

        // Set the generated HTML to the results container, replacing previous content.
        this.container.innerHTML = html;
    },

    /**
     * Generates the HTML for the "Parameter Carian" (Search Parameters) card.
     * It filters out 'Any' values and formats the keys and values.
     * @param {Object} plan - The plan object containing search criteria.
     * @returns {string} The HTML string for the plan card.
     */
    generatePlanCard(plan) {
        // Convert plan object to an array of [key, value] pairs, filter out 'Any' values,
        // and map them to HTML data items.
        const filteredPlan = Object.entries(plan)
            .filter(([key, value]) => value !== 'Any') // Only include parameters that were specified.
            .map(([key, value]) => `
                <div class="data-item">
                    <span>${Utils.formatKey(key)}:</span> <!-- Format the key for display -->
                    <span class="data-value">${Utils.escapeHtml(value)}</span> <!-- Escape value for safety -->
                </div>
            `).join(''); // Join all data items into a single string.

        return `
            <div class="result-card">
                <div class="result-title">🎯 Parameter Carian</div>
                ${filteredPlan}
            </div>
        `;
    },

    /**
     * Generates the HTML for the "Pecahan Data" (Data Breakdown) card,
     * displaying grouped data.
     * @param {Array<Object>} groups - An array of grouped data objects.
     * @returns {string} The HTML string for the groups card.
     */
    generateGroupsCard(groups) {
        // Map through each group to generate its HTML structure.
        const groupsHtml = groups.map(group => `
            <div class="group-data">
                <div class="group-title">${Utils.escapeHtml(group.label)}</div> <!-- Group label -->
                ${group.data.map(item => {
                    const key = Object.keys(item)[0]; // Get the dynamic key for the data item (e.g., 'state', 'age_group').
                    const count = item.COUNT;         // Get the count associated with the data item.
                    return `
                        <div class="data-item">
                            <span>${Utils.escapeHtml(item[key])}</span> <!-- Display the data item value -->
                            <span class="data-value">${Utils.formatNumber(count)}</span> <!-- Display the formatted count -->
                        </div>
                    `;
                }).join('')}
            </div>
        `).join(''); // Join all group HTML structures.

        return `
            <div class="result-card">
                <div class="result-title">📈 Pecahan Data</div>
                ${groupsHtml}
            </div>
        `;
    }
};

export default ResultsModule; // Export the ResultsModule object.
