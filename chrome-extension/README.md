# Dark Pattern Detector Chrome Extension

A Chrome extension that detects manipulative dark patterns on websites in real-time using AI-powered analysis.

## Features

- **Real-time Detection**: Automatically analyzes webpage content for dark patterns
- **Visual Highlighting**: Highlights detected patterns directly on the page
- **Pattern Categories**: Detects various types of dark patterns including:
  - False urgency (limited time offers)
  - False scarcity (low stock claims)
  - Confirmshaming (guilt-tripping opt-outs)
  - Trick wording (misleading labels)
  - Hidden costs (surprise fees)
  - Forced actions (blocking progress)
  - Subscription traps (auto-renewal pressure)
  - Pre-selected checkboxes (opt-out defaults)
  - UI attention manipulation (bright elements)

- **Interactive Popup**: View detailed analysis results and control the extension
- **Confidence Scores**: Each detection includes a confidence level

## Installation

1. **Start the Backend Server**:
   ```bash
   cd backend
   python main.py
   ```
   The server will run on http://localhost:8000

2. **Load the Extension in Chrome**:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `chrome-extension` folder from this project

3. **Add Extension Icons** (Optional):
   - Create 16x16, 48x48, and 128x128 PNG icons
   - Place them in the `icons/` folder as `icon16.png`, `icon48.png`, `icon128.png`

## Usage

1. **Automatic Analysis**: The extension automatically analyzes pages when they load
2. **Manual Analysis**: Click the extension icon and use "Analyze Current Page"
3. **View Results**: Detected patterns are highlighted on the page with tooltips
4. **Control Extension**: Use the popup to enable/disable or clear highlights

## How It Works

1. **Content Extraction**: The extension extracts visible text and relevant HTML elements from web pages
2. **API Analysis**: Content is sent to the local Python backend for pattern detection
3. **Visual Feedback**: Detected patterns are highlighted with colored underlines and tooltips
4. **Real-time Updates**: Re-analyzes content when the page changes dynamically

## Development

### Backend API

The extension communicates with a FastAPI server that provides:

- `POST /analyze`: Analyze text/HTML for dark patterns
- `GET /health`: Health check endpoint
- `GET /docs`: Interactive API documentation

### Extension Architecture

- **content.js**: Extracts page content and handles highlighting
- **popup.html/popup.js**: User interface for controls and results
- **background.js**: Service worker for extension lifecycle
- **styles.css**: Highlighting and notification styles

## Privacy

- All analysis happens locally on your machine
- No data is sent to external servers
- Only analyzes content from websites you visit

## Troubleshooting

**Extension not working?**
- Ensure the backend server is running on localhost:8000
- Check browser console for errors
- Try refreshing the page

**No patterns detected?**
- Some pages may not contain detectable patterns
- Try pages with forms, popups, or sales content

**Highlights not showing?**
- Check if the extension is enabled
- Try clearing highlights and re-analyzing