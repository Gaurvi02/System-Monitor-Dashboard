# 🚀 Advanced System Monitor Dashboard

A powerful, real-time system monitoring dashboard built with Python Flask that provides comprehensive insights into your system's performance, hardware metrics, and database usage analytics.


## ✨ Features

### System Metrics
- **CPU Analytics**: Real-time CPU usage, per-core metrics, and temperature monitoring
- **Memory Insights**: Detailed RAM utilization and allocation statistics
- **Storage Analysis**: Disk space usage, read/write speeds, and partition information
- **Network Monitoring**: Bandwidth usage, interface statistics, and network performance
- **GPU Metrics**: Temperature, memory usage, and performance statistics (optional)

### Database Integration
- **MySQL Integration**: Real-time analysis of database table space usage
- **Recipe Analytics**: Track user-specific recipe storage metrics and usage patterns
- **Performance Monitoring**: Database connection and query performance metrics

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **System Monitoring**: psutil, GPUtil
- **Database**: MySQL Connector
- **Frontend**: HTML5, CSS3, JavaScript
- **Real-time Updates**: Server-Sent Events (SSE)

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/system-monitor.git
cd system-monitor
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database settings**
```python
# Update app.py with your MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}
```

5. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser to access the dashboard.

## 📸 Screenshots

[Add screenshots of your dashboard here]


## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments

- [psutil](https://github.com/giampaolo/psutil) - System monitoring library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [GPUtil](https://github.com/anderskm/gputil) - GPU monitoring
- [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/) - Database connectivity

## 📬 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/system-monitor](https://github.com/yourusername/system-monitor)
