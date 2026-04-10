# Dark Pattern Detection Project

An AI-powered system to detect manipulative "dark patterns" in web interfaces and content. This project helps identify unethical design practices that trick users into actions they might not want to take.

## 🏗️ Project Structure

```
dark-pattern-detector/
├── backend/                    # Python FastAPI server
│   ├── main.py                # API endpoints
│   ├── detector.py            # Pattern detection logic
│   ├── image_cv.py            # OpenCV image analysis
│   ├── image_temp.py          # Image handling utilities
│   ├── test.py                # API testing script
│   └── requirements.txt       # Python dependencies
├── chrome-extension/          # Browser extension
│   ├── manifest.json          # Extension configuration
│   ├── content.js             # Page content analysis
│   ├── popup.html             # Extension popup UI
│   ├── popup.js               # Popup functionality
│   ├── background.js          # Service worker
│   ├── styles.css             # Highlighting styles
│   └── README.md              # Extension documentation
├── webapp/                    # Web-based testing interface
│   └── index.html             # Test interface
└── dataset/                   # Training/validation data (future)
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API will be available at `http://localhost:8000`

### 2. Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `chrome-extension` folder
4. The extension icon will appear in your toolbar

### 3. Test the System

- **Web Interface**: Open `webapp/index.html` in your browser
- **API Testing**: Run `python backend/test.py`
- **Extension**: Visit any website and click the extension icon

## 🎯 Features

### Backend API
- **Text Analysis**: Detects 9+ categories of dark patterns
- **HTML Analysis**: Scans forms for pre-checked boxes
- **Image Analysis**: Uses OpenCV to detect attention-manipulating UI elements
- **Confidence Scoring**: Provides confidence levels for each detection

### Chrome Extension
- **Real-time Analysis**: Automatically analyzes pages as you browse
- **Visual Highlighting**: Highlights detected patterns with colored underlines
- **Interactive Popup**: View detailed results and control the extension
- **Manual Analysis**: Trigger analysis on demand

### Pattern Categories Detected

1. **False Urgency** - Pressure to act immediately
2. **False Scarcity** - Misleading low-stock claims
3. **Confirmshaming** - Guilt-tripping opt-out options
4. **Trick Wording** - Ambiguous or misleading labels
5. **Hidden Costs** - Surprise fees and charges
6. **Forced Action** - Blocking progress without compliance
7. **Subscription Traps** - Auto-renewal and cancellation pressure
8. **Pre-selected Checkboxes** - Opt-out defaults
9. **UI Attention Manipulation** - Bright elements drawing focus

## 🔧 Development

### Adding New Patterns

1. Add pattern rules to `backend/detector.py` in the `_RULES` tuple
2. Include phrases, weight, and description
3. Test with the webapp interface

### Extension Customization

- Modify `chrome-extension/styles.css` for different highlighting styles
- Update `chrome-extension/content.js` for additional analysis features
- Add new popup controls in `chrome-extension/popup.html`

### API Endpoints

- `POST /analyze` - Analyze text/HTML/image for patterns
- `GET /health` - Server health check
- `GET /docs` - Interactive API documentation (FastAPI)

## 📊 Testing

### Backend Tests
```bash
cd backend
python test.py
```

### Manual Testing
- Use the webapp interface for text analysis
- Test extension on various websites
- Check browser console for errors

## 🔒 Privacy & Security

- **Local Processing**: All analysis happens on your machine
- **No Data Collection**: No user data is sent to external servers
- **Open Source**: Transparent detection algorithms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by research on dark patterns in UX design
- Built with FastAPI, OpenCV, and Chrome Extension APIs
- Pattern definitions based on established UX research

## 🔍 Future Enhancements

- [ ] Machine learning model for better pattern detection
- [ ] Browser extension for Firefox/Safari
- [ ] Dataset collection for training
- [ ] Real-time analysis of dynamic content
- [ ] Integration with accessibility tools
- [ ] Pattern reporting and aggregation