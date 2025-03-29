# Flight Finder

A Python application that helps users find flights to cool destinations based on weather forecasts. The application uses various APIs to:
- Get the user's current location
- Find nearby cities with comfortable weather
- Search for available flights to these destinations

## Features

- IP-based location detection
- Weather forecast integration
- Flight search using AviationStack API
- Chrome extension interface
- Flask backend API

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd flight
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Create a `.env` file with your API keys:
```
AVIATIONSTACK_API_KEY=your_api_key
```

4. Run the Flask server:
```bash
python app.py
```

5. Load the Chrome extension:
- Open Chrome and go to `chrome://extensions/`
- Enable "Developer mode"
- Click "Load unpacked" and select the `extension` directory

## Project Structure

```
flight/
├── app.py              # Flask backend server
├── flight_checker.py   # Flight search functionality
├── weather.py          # Weather forecast functionality
├── ip_location.py      # IP-based location detection
├── extension/         # Chrome extension files
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
└── requirements.txt    # Python dependencies
```

## API Keys Required

- AviationStack API key for flight data
- (Add any other API keys required)

## Usage

1. Click the extension icon in Chrome
2. The extension will:
   - Detect your current location
   - Find nearby cities with comfortable weather
   - Search for available flights
   - Display the top 3 flights for each destination

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 