# USSD Service for Tanzania (Sandbox)

This is a simple USSD backend application built with Python and Flask, designed to simulate a USSD menu for a Tanzanian service.

## Setup

1.  **Dependencies**: Install the required packages:
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`
2.  **Run Locally**:
    \`\`\`bash
    python ussd_app.py
    \`\`\`

## Deployment

This application is configured for deployment on platforms like Heroku, Render, or Railway using the provided \`Procfile\` and \`requirements.txt\`.

## Files

*   \`ussd_app.py\`: The main Flask application logic.
*   \`requirements.txt\`: Python dependencies (Flask, gunicorn).
*   \`Procfile\`: Gunicorn command for web deployment.
