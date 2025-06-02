# ASL (American Sign Language) Recognition Project

A comprehensive solution for real-time American Sign Language recognition using computer vision and deep learning.

## Project Structure

```
├── Scripts/                 # Core ML/AI implementation
│   ├── Keypoints/          # Keypoint-based recognition
│   ├── YOLO/               # YOLO-based object detection
│   └── train/              # Training scripts and utilities
├── UI_expo/                # Mobile application (Expo/React Native)
├── docs/                   # Project documentation
├── models/                 # Trained model weights
├── server/                 # Backend server implementation
└── requirements.txt        # Python dependencies
```

## Features

- Real-time ASL recognition using computer vision
- Multiple recognition approaches:
  - CNN-based classification
  - Keypoint-based detection
  - YOLO object detection
- Cross-platform mobile application
- RESTful API server

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up the mobile application:
```bash
cd UI_expo
npm install
```

3. Start the development server:
```bash
python app.py
```

4. Launch the mobile app:
```bash
cd UI_expo
npm start
```

## Models

- `asl_cnn.pth`: CNN-based ASL recognition model
- `asl_gnn.pth`: Graph Neural Network for hand pose estimation

## Documentation

Detailed documentation is available in the `docs/` directory.

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request