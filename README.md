# 📊 Chartastrophe

> **Absurd and hilarious correlation generator**

An interactive web application that generates improbable statistical correlations between real datasets, with deliriously pseudo-scientific explanations.

## 🎯 What is Chartastrophe?

Chartastrophe discovers statistical "connections" between completely disconnected phenomena:
- 🌊 "Sea Level Rise Measurements affects Programming Language Trends"
- 🏠 "Income Distribution affects Green Hydrogen Potential" 
- 🚀 "Space Station Position affects Waste Recycling Rates"

Each correlation comes with a hilarious pseudo-scientific explanation and interactive charts.

## ✨ Features

### 🎲 **Random Generation**
- Instant correlations between real datasets
- Interactive charts with Plotly
- AI-generated pseudo-scientific explanations

### 📊 **Real Data Sources**
- **Government**: France, USA, UK, Canada, Germany, Japan, Singapore, Australia
- **Scientific**: NASA, NOAA, USGS, CERN, ESA, WHO
- **Economic**: World Bank, OECD, IMF, IEA, IRENA
- **Social**: Google Trends, Wikipedia, Reddit, GitHub
- **Transport**: SNCF, RATP, FlightRadar24, mobility data

### 🎨 **Modern Interface**
- Responsive and elegant design
- Centered and optimized charts
- User feedback system
- Easy correlation sharing

## 🚀 Installation and Launch

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Clone the project
git clone <repository-url>
cd chartastrophe

# Create virtual environment
python -m venv venv_new
source venv_new/bin/activate  # Linux/Mac
# or
venv_new\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Launch
```bash
python wsgi.py
```

The application will be accessible at `http://127.0.0.1:5000`

## 🏗️ Architecture

```
src/
├── web/                    # Flask web interface
│   ├── app.py             # Flask application
│   ├── routes.py          # API and web routes
│   └── templates/         # HTML templates
├── collectors/            # Data collectors
│   ├── real_data_collector.py    # Main collector
│   ├── open_data_sources.py      # Open sources
│   └── data_sources_registry.py  # Source registry
├── correlation/           # Correlation engine
│   ├── correlation_engine.py     # Statistical calculations
│   └── correlation_analyzer.py   # Data analysis
├── generator/             # Explanation generator
│   └── explanation_generator.py  # AI for explanations
└── feedback/              # Feedback system
    └── user_feedback.py   # User feedback management
```

## 🎮 Usage

1. **Access the application** at `http://127.0.0.1:5000`
2. **Click "Generate new correlation"**
3. **Admire** the generated absurd correlation
4. **Read the delirious** pseudo-scientific explanation
5. **Share** with friends to make them laugh!

## 🔧 Configuration

### Environment variables
Create a `.env` file:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Logging
Configuration in `logging.conf` for optimal debugging.

## 🤝 Contribution

Contributions are welcome! You can:
- Add new data sources
- Improve generated explanations
- Optimize user interface
- Fix bugs

## ⚠️ Important Warning

**This project is purely humorous and educational.**

- Generated correlations are **intentionally absurd**
- They demonstrate that **"correlation is not causation"**
- **Never** take these results seriously
- Use this tool to **laugh** and **raise awareness** about statistical biases

## 📜 License

This project is under MIT license. See the `LICENSE` file for more details.

---

*"In a world where everything seems correlated, Chartastrophe reveals the most improbable connections!"* 🎭 