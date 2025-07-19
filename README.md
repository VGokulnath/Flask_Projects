# DocChatWeb

DocChatWeb is a Flask-powered web application that allows you to chat with your Markdown documents using AI. Ask questions about your document content and get intelligent answers powered by OpenAI's GPT models.

## Features

- 🤖 **AI-Powered Q&A**: Uses GPT models to answer questions based strictly on your document content
- 📝 **Markdown Support**: Load and parse any Markdown file
- 💬 **Clean Chat Interface**: Modern, responsive chat UI with real-time messaging
- 🔒 **Document-Only Responses**: AI only uses information from your loaded document
- 🔄 **Live Document Reload**: Update your document and reload it without restarting the app
- 📱 **Mobile Friendly**: Responsive design that works on all devices

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

### 1. Clone or Download the Project

If you're starting fresh, create a new directory for your project:

```bash
mkdir docchatweb
cd docchatweb
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up OpenAI API Key

You need an OpenAI API key to use the AI features. Get one from [OpenAI's website](https://platform.openai.com/api-keys).

Set your API key as an environment variable:

**On Linux/Mac:**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**On Windows:**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Or create a .env file** (recommended):
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 4. Prepare Your Document

Replace the sample `data.md` file with your own Markdown content, or keep the sample to test the application.

## Usage

### Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Start chatting with your document!

### Using the Chat Interface

- Type your questions in the input field at the bottom
- Press Enter or click the send button (➤) to submit
- The AI will respond based only on your document content
- If the answer isn't in the document, you'll get: "Sorry, I don't see that in the document."
- Use the "Reload Doc" button to refresh the document if you make changes

### Example Questions

Based on the sample Python guide document, you can ask:

- "What is Python?"
- "Who created Python?"
- "What are some popular Python libraries for data science?"
- "How do you create a function in Python?"
- "What are Python's key features?"

## File Structure

```
docchatweb/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── data.md               # Your Markdown document (replace with your content)
├── README.md             # This file
└── templates/
    └── index.html        # Chat interface template
```

## Customization

### Changing the Document

Simply replace `data.md` with your own Markdown file. The application will automatically load it when started.

### Modifying the AI Model

In `app.py`, you can change the GPT model by modifying this line:

```python
model="gpt-3.5-turbo",  # Change to "gpt-4" for better responses
```

### Styling the Interface

The CSS is embedded in `templates/index.html`. You can modify the styles to match your preferences.

## API Endpoints

- `GET /` - Main chat interface
- `POST /ask` - Submit a question and get an AI response
- `POST /reload` - Reload the Markdown document

## Troubleshooting

### Common Issues

1. **"Error: OpenAI API key not configured"**
   - Make sure you've set the `OPENAI_API_KEY` environment variable
   - Verify your API key is valid and has credits

2. **"Module not found" errors**
   - Run `pip install -r requirements.txt` to install dependencies
   - Make sure you're in the correct directory

3. **"File not found" for data.md**
   - The app will create a sample `data.md` if none exists
   - Make sure your custom markdown file is named `data.md`

4. **Port already in use**
   - Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify your OpenAI API key is set and valid
3. Ensure your `data.md` file exists and contains valid Markdown
4. Check the console output for detailed error messages

## Dependencies

- **Flask 2.3.3**: Web framework
- **openai 0.28.1**: OpenAI API client
- **markdown 3.5.1**: Markdown parsing
- Additional Flask dependencies (Werkzeug, Jinja2, etc.)

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve DocChatWeb!

---

**Happy chatting with your documents! 🚀**