## Project Structure
```bash
.
├── connectors       # Handles browser automation (Selenium setup)
├── controllers      # Coordinates scraping flow
├── exporters        # Exports parsed data (e.g. CSV)
├── models           # Data models (e.g. Match)
├── pages            # Page-level interactions (e.g. loading the ESPN page)
├── parsers          # Extracts structured data from HTML
├── main.py          # Entry point to run the scraper
└── requirements.txt # Python dependencies
```

## Architecture Flow
![architecture](https://www.mermaidchart.com/raw/bce7bac1-9ad3-4b04-852f-ce4b56ee48f2?theme=light&version=v0.1&format=svg)

## Setup Instructions

### Windows

1. Install Firefox from [mozilla.org](https://www.mozilla.org)
2. Install Geckodriver:
   - Download from [geckodriver releases](https://github.com/mozilla/geckodriver/releases)
   - Extract and add the path to your System Environment Variables > PATH
3. Install Python packages:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Run the scraper
```bash
python main.py
```
### Linux

1. Install firefox:
```bash
sudo apt install firefox -y
```
2. Install GeckoDriver:
```bash
sudo apt install firefox-geckodriver -y
```
3. Install Python packages:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
4. Run the scraper:
```bash
python main.py
```
> **_NOTE:_**
> If you're using Firefox installed via Snap, set this in the controller:
> ```python
> BaseDriver(binary_path="/snap/firefox/current/usr/lib/firefox/firefox")
> ```
