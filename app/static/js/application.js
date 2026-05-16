// Stimulus application setup
import { Application } from "https://cdn.jsdelivr.net/npm/stimulus@3/dist/stimulus.js"

const application = Application.start()

// Export for use in other scripts
window.Stimulus = application

// Optional: Log for debugging
console.log('Stimulus application started')
