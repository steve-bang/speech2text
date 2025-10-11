# VardyTests - Speech to Text API

A Flask-based REST API service that provides speech-to-text transcription, translation, keyword extraction, and video-to-audio conversion capabilities.

## Features

- 🎤 **Speech to Text Transcription** - Convert audio files to text using Google Speech Recognition
- 🌍 **Translation** - Translate text to multiple languages
- 🔑 **Keyword Extraction** - Extract main keywords from text using NLP
- 🎬 **Video to Audio Conversion** - Extract audio from video files
- 📁 **Multiple Audio Formats** - Support for MP3, WAV, and other audio formats

## Prerequisites

- Python 3.8 or higher
- FFmpeg
- Docker (optional, for containerized deployment)

## Quick Start with Docker

The easiest way to get started is using our pre-built Docker image:

```bash
docker pull dev1byte/speech2text
docker run -p 8801:8801 -v $(pwd)/upload-files:/app/upload-files dev1byte/speech2text
```

The API will be available at `http://localhost:8801`

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install system dependencies (FFmpeg):
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create the upload directory:
```bash
mkdir upload-files
```

5. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8801`

### Docker Setup

#### Option 1: Use Pre-built Image (Recommended)

```bash
# Pull the image
docker pull dev1byte/speech2text

# Run the container
docker run -d \
  -p 8801:8801 \
  -v $(pwd)/upload-files:/app/upload-files \
  --name speech2text-api \
  dev1byte/speech2text
```

#### Option 2: Build from Source

1. Build the Docker image:
```bash
docker build -t speech2text-api .
```

2. Run the container:
```bash
docker run -d \
  -p 8801:8801 \
  -v $(pwd)/upload-files:/app/upload-files \
  --name speech2text-api \
  speech2text-api
```

#### Docker Compose (Optional)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  speech2text:
    image: dev1byte/speech2text
    ports:
      - "8801:8801"
    volumes:
      - ./upload-files:/app/upload-files
    restart: unless-stopped
```

Then run:
```bash
docker-compose up -d
```

## API Endpoints

### 1. Speech to Text (Primary)

**Endpoint:** `POST /api/speech-to-text`

Transcribe audio files to text.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (audio file)

**Example:**
```bash
curl -X POST http://localhost:8801/api/speech-to-text \
  -F "file=@audio.mp3"
```

**Response:**
```json
{
  "transcription": "Your transcribed text here"
}
```

### 2. Speech to Text (Alternative)

**Endpoint:** `POST /api/v1/speech-to-text`

Alternative endpoint for audio transcription.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `audio` (audio file)

**Example:**
```bash
curl -X POST http://localhost:8801/api/v1/speech-to-text \
  -F "audio=@audio.wav"
```

**Response:**
```json
{
  "text": "Your transcribed text here"
}
```

### 3. Keyword Extraction

**Endpoint:** `POST /api/keywords`

Extract main keywords from text using natural language processing.

**Request:**
- Method: `POST`
- Content-Type: `application/x-www-form-urlencoded`
- Body: `text` (string)

**Example:**
```bash
curl -X POST http://localhost:8801/api/keywords \
  -d "text=Artificial intelligence is transforming the technology industry"
```

**Response:**
```json
{
  "keywords": ["artificial intelligence", "technology industry"]
}
```

### 4. Translation

**Endpoint:** `POST /api/translation`

Translate text to different languages using Google Translate.

**Request:**
- Method: `POST`
- Content-Type: `application/x-www-form-urlencoded`
- Body: 
  - `content` (string) - Text to translate
  - `languageCode` (string) - Target language code (e.g., 'es', 'fr', 'de')

**Example:**
```bash
curl -X POST http://localhost:8801/api/translation \
  -d "content=Hello World" \
  -d "languageCode=es"
```

**Response:**
```json
{
  "text": "Hola Mundo"
}
```

### 5. Video to Audio Conversion

**Endpoint:** `POST /api/convert-video-to-audio`

Extract audio from video files and convert to MP3 format.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `videoFile` (video file)

**Example:**
```bash
curl -X POST http://localhost:8801/api/convert-video-to-audio \
  -F "videoFile=@video.mp4"
```

**Response:**
```json
{
  "audio_url": "http://localhost:8801/files/uploads/video.mp3"
}
```

### 6. Download Files

**Endpoint:** `GET /files/uploads/<filename>`

Download uploaded/converted files.

**Example:**
```bash
curl http://localhost:8801/files/uploads/audio.mp3 -o downloaded_audio.mp3
```

## Supported Formats

### Audio Formats
- WAV
- MP3
- FLAC
- OGG
- M4A
- Other formats supported by pydub/FFmpeg

### Video Formats
- MP4
- AVI
- MOV
- MKV
- WMV
- FLV
- Other formats supported by MoviePy/FFmpeg

### Language Codes (Translation)

Common language codes for translation:

| Language | Code |
|----------|------|
| English | `en` |
| Spanish | `es` |
| French | `fr` |
| German | `de` |
| Italian | `it` |
| Portuguese | `pt` |
| Russian | `ru` |
| Japanese | `ja` |
| Korean | `ko` |
| Chinese (Simplified) | `zh-cn` |
| Chinese (Traditional) | `zh-tw` |
| Arabic | `ar` |
| Hindi | `hi` |
| Vietnamese | `vi` |
| Thai | `th` |

[View full list of language codes](https://cloud.google.com/translate/docs/languages)

## Configuration

You can modify the following configuration in `main.py`:

```python
app.config['UPLOAD_FILE_FOLDER'] = 'upload-files'  # Upload directory
app.config['PORT'] = 8801                           # Server port
```

For Docker deployment, you can override these with environment variables:

```bash
docker run -d \
  -p 8801:8801 \
  -e PORT=8801 \
  -v $(pwd)/upload-files:/app/upload-files \
  dev1byte/speech2text
```

## Error Handling

All endpoints return appropriate error messages:

**Error Response Format:**
```json
{
  "error": "Error description"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (missing file or parameters)
- `500` - Internal Server Error

**Common Error Messages:**
- "No file part in the request" - File not included in request
- "No selected file" - Empty filename
- "Cannot recognize audio file" - Audio quality too poor or unsupported language
- "The language code is not supported" - Invalid language code provided

## Usage Examples

### Python Example

```python
import requests

# Speech to text
with open('audio.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:8801/api/speech-to-text',
        files={'file': f}
    )
    print(response.json())

# Translation
response = requests.post(
    'http://localhost:8801/api/translation',
    data={
        'content': 'Hello World',
        'languageCode': 'es'
    }
)
print(response.json())

# Keyword extraction
response = requests.post(
    'http://localhost:8801/api/keywords',
    data={'text': 'Your text here'}
)
print(response.json())
```

### JavaScript Example

```javascript
// Speech to text
const formData = new FormData();
formData.append('file', audioFile);

fetch('http://localhost:8801/api/speech-to-text', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data.transcription));

// Translation
fetch('http://localhost:8801/api/translation', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
        'content': 'Hello World',
        'languageCode': 'es'
    })
})
.then(response => response.json())
.then(data => console.log(data.text));
```

## Dependencies

- **Flask** - Web framework
- **SpeechRecognition** - Speech-to-text conversion using Google Speech Recognition API
- **googletrans** (4.0.0-rc1) - Translation service
- **TextBlob** - Natural language processing for keyword extraction
- **pydub** - Audio file manipulation
- **moviepy** - Video processing and audio extraction
- **FFmpeg** - Audio/video encoding and conversion (system dependency)

## Limitations

- Audio files are automatically converted to 16kHz sample rate for optimal recognition
- Large files may take longer to process depending on server resources
- Internet connection required for Google Speech Recognition and Translation services
- Recognition accuracy depends on audio quality and clarity
- Translation API has rate limits (part of Google Translate free tier)

## Development

To run in development mode with debug enabled:

```bash
python main.py
```

The server will automatically reload when code changes are detected.

### Running Tests

```bash
# Add your test commands here
python -m pytest tests/
```

## Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8801 main:app
```

2. **Update Dockerfile CMD** for production:
```dockerfile
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8801", "main:app"]
```

3. **Set up nginx as a reverse proxy**
4. **Implement rate limiting** to prevent abuse
5. **Add authentication/authorization** for API endpoints
6. **Set up proper logging** and monitoring
7. **Use environment variables** for sensitive configuration
8. **Disable debug mode** (`debug=False`)
9. **Set up SSL/TLS** for HTTPS
10. **Configure CORS** if needed for web applications

## Docker Management

### View Logs
```bash
docker logs speech2text-api
```

### Stop Container
```bash
docker stop speech2text-api
```

### Start Container
```bash
docker start speech2text-api
```

### Remove Container
```bash
docker rm speech2text-api
```

### Update to Latest Version
```bash
docker pull dev1byte/speech2text
docker stop speech2text-api
docker rm speech2text-api
docker run -d -p 8801:8801 -v $(pwd)/upload-files:/app/upload-files --name speech2text-api dev1byte/speech2text
```

## Troubleshooting

### FFmpeg not found
**Issue:** `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solution:** Ensure FFmpeg is installed:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Recognition errors
**Issue:** Audio not being recognized or returning errors

**Solutions:**
- Check audio quality and ensure speech is clear
- Verify audio is in a supported language (default: English)
- Ensure stable internet connection for Google Speech Recognition
- Try converting audio to WAV format first
- Reduce background noise in audio

### Import errors
**Issue:** `ModuleNotFoundError`

**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port already in use
**Issue:** `Address already in use`

**Solution:** Change the port or stop the process using port 8801:
```bash
# Find process using port 8801
lsof -i :8801

# Kill the process
kill -9 <PID>

# Or use a different port
docker run -p 8802:8801 dev1byte/speech2text
```

### Permission denied (Docker volumes)
**Issue:** Cannot write to upload-files directory

**Solution:** Ensure proper permissions:
```bash
mkdir -p upload-files
chmod 755 upload-files
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 style guidelines and includes appropriate tests.

## License

[Specify your license here - e.g., MIT, Apache 2.0, GPL]

## Support

If you encounter any issues or have questions:

- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

## Acknowledgments

- Google Speech Recognition API
- Google Translate API
- FFmpeg project
- Flask framework
- All contributors

## Changelog

### Version 1.0.0
- Initial release
- Speech to text transcription
- Multi-language translation
- Keyword extraction
- Video to audio conversion
- Docker support

---

**Docker Hub:** [dev1byte/speech2text](https://hub.docker.com/r/dev1byte/speech2text)

**Made with ❤️ by [VardyTests]**
