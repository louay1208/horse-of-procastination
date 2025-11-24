# AI Procrastination Detector 🐴

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An intelligent desktop application that detects cell phone usage via your laptop camera and triggers humorous "Horse of Wisdom" alerts to help you stay focused and productive.

![Demo](docs/demo.gif) <!-- Add a demo GIF if you have one -->

## ✨ Features

- 🐴 just a horse making sure u have shit done xD

## 📋 System Requirements

- **OS**: Windows (tested), Linux, macOS
- **Python**: 3.8 or higher
- **Hardware**: 
  - Webcam (built-in or external)
  - CUDA-capable GPU (optional, for 5-10x faster detection)
  - ~2GB disk space for dependencies

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/hourse-of-wisdom.git
cd hourse-of-wisdom
```

2. **Install dependencies**

Using `uv` (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. **Set up configuration**
```bash
# Copy example config
cp config.yaml.example config.yaml

# Generate default config (alternative)
python config.py
```

4. **Prepare assets**
   - Place your horse-of-wisdom meme images (PNG or GIF) in the `horse of wisdom/` folder
   - (Optional) Add `alert_sound.mp3` to the project root for custom audio
   - The YOLO model (`yolo11n.pt`) will download automatically on first run

5. **Run the application**
```bash
uv run app.py
# or
python app.py
```

## ⚙️ Configuration

Edit `config.yaml` to customize behavior:

```yaml
detection:
  threshold: 30          # Frames before triggering alert
  confidence: 0.5        # Detection confidence (0.0-1.0)

alert:
  images_folder: "horse of wisdom"  # Path to meme images
  switch_interval: 2000   # Milliseconds between carousel images
  transition_duration: 800  # Milliseconds for transitions

ui:
  button_continue_text: "I'm working!"
  button_quit_text: "Quit App"
  display_fps: 60

log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

See [`config.yaml.example`](config.yaml.example) for all available options.

## 📖 Usage

### Basic Usage

1. **Start the application**: Run `python app.py`
2. **Detection begins**: A window shows your webcam feed with detection boxes
3. **Counter appears**: When a phone is detected, you'll see: `Detection: X/30`
4. **Alert triggers**: After 30 consecutive detections, the Horse of Wisdom appears!
5. **Make your choice**: 
   - Click **"I'm working!"** to dismiss and continue detection
   - Click **"Quit App"** to exit the application

### Keyboard Shortcuts

- **`q`**: Quit the application
- **`ESC`**: Close alert window (continues detection)
- **`X`**: Close main window (exits application)

## 🔧 Troubleshooting

<details>
<summary><b>Camera Not Found</b></summary>

```
Error: Could not open webcam
```

**Solutions**:
- Check camera permissions in system settings
- Ensure no other application is using the camera
- Try unplugging and reconnecting external webcams
- Restart the application
</details>

<details>
<summary><b>No Images Found</b></summary>

```
No horse images found. Cannot display alert.
```

**Solutions**:
1. Verify `images_folder` path in `config.yaml`
2. Ensure folder contains PNG or GIF files
3. Check file permissions
4. Place at least one image in the `horse of wisdom/` folder
</details>

<details>
<summary><b>YOLO Model Missing</b></summary>

```
YOLO model not found at yolo11n.pt
```

**Solutions**:
- The model downloads automatically on first run
- Check your internet connection
- Manually download from [Ultralytics](https://github.com/ultralytics/ultralytics)
- Verify disk space (~6MB required)
</details>

<details>
<summary><b>Low FPS / Slow Detection</b></summary>

**Solutions**:
1. Enable CUDA if you have an NVIDIA GPU
2. Lower `display_fps` in config (try 30)
3. Reduce `confidence` threshold slightly
4. Close other resource-intensive applications
5. Use a smaller YOLO model variant
</details>

## 📁 Project Structure

```
hourse-of-wisdom/
├── app.py                  # Main application entry point
├── alert_system.py         # Alert popup system with carousel
├── config.py               # Configuration management
├── constants.py            # Constants and defaults
├── config.yaml             # User configuration (gitignored)
├── config.yaml.example     # Example configuration
├── pyproject.toml          # Project dependencies (uv)
├── requirements.txt        # Dependencies (pip)
├── LICENSE                 # MIT License
├── README.md               # This file
├── CONTRIBUTING.md         # Contribution guidelines
├── .gitignore              # Git ignore rules
└── horse of wisdom/        # Meme images directory
    └── *.png, *.gif        # Your horse memes
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/hourse-of-wisdom.git
cd hourse-of-wisdom

# Install dependencies
uv sync

# Create config
python config.py

# Run the app
uv run app.py
```

## 📊 Performance Tips

1. **GPU Acceleration**: Install CUDA toolkit for 5-10x faster detection
2. **Image Optimization**: Use images around 500px width for best performance
3. **FPS Limiting**: Default 60 FPS is usually sufficient
4. **Detection Threshold**: Higher values = fewer false alerts but slower response

## 🐛 Known Limitations

- Windows-specific audio fallback (uses `winsound`)
- GIF animation requires `imageio` library (optional)
- CUDA support requires NVIDIA GPU with compatible drivers
- Currently detects only cell phones (YOLO class 67)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **YOLO**: [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- **Inspiration**: The need to stay focused in a world full of distractions
- **Horse of Wisdom**: Internet meme culture

## 📧 Support

For issues, questions, or feature requests:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review logs (set `log_level: "DEBUG"` in config.yaml)
3. Search [existing issues](https://github.com/YOUR_USERNAME/hourse-of-wisdom/issues)
4. Open a [new issue](https://github.com/YOUR_USERNAME/hourse-of-wisdom/issues/new)

## ⭐ Star History

If you find this project helpful, please consider giving it a star!

---

**Stay focused! The Horse of Wisdom is watching! 🐴👀**

Made with ❤️ and a sense of humor
