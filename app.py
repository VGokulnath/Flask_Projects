import os
import markdown
import openai
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'

# OpenAI API key - set this as an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

class MarkdownQA:
    def __init__(self, markdown_file_path):
        self.markdown_content = ""
        self.parsed_content = ""
        self.load_markdown(markdown_file_path)
    
    def load_markdown(self, file_path):
        """Load and parse the Markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.markdown_content = file.read()
                # Convert markdown to plain text for better processing
                self.parsed_content = markdown.markdown(self.markdown_content)
                # Remove HTML tags for cleaner text
                import re
                self.parsed_content = re.sub('<[^<]+?>', '', self.parsed_content)
                print(f"Loaded markdown file: {file_path}")
        except FileNotFoundError:
            print(f"Warning: Markdown file '{file_path}' not found. Creating a sample data.md file.")
            self.create_sample_markdown(file_path)
            self.load_markdown(file_path)
        except Exception as e:
            print(f"Error loading markdown file: {e}")
            self.markdown_content = "Error loading document."
            self.parsed_content = "Error loading document."
    
    def create_sample_markdown(self, file_path):
        """Create a sample markdown file if none exists"""
        sample_content = """# Sample Document

## Introduction
This is a sample document for the DocChatWeb application. You can replace this with your own Markdown content.

## Features
- Chat with your documents using AI
- Supports Markdown formatting
- Easy to use web interface
- Powered by OpenAI GPT models

## Usage
1. Replace this data.md file with your own content
2. Ask questions about the document
3. Get AI-powered answers based only on the document content

## Technical Details
This application uses Flask for the web framework and OpenAI's GPT models for natural language processing.

### Supported Formats
- Standard Markdown syntax
- Headers, lists, and formatting
- Code blocks and inline code

## Conclusion
Start chatting with your documents today!
"""
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(sample_content)
        print(f"Created sample markdown file: {file_path}")
    
    def get_answer(self, question):
        """Get an answer to a question based on the markdown content"""
        if not openai.api_key:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
        
        try:
            # Create a prompt that instructs the model to only use the provided content
            prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided document content. 

Document content:
{self.parsed_content}

Question: {question}

Instructions:
1. Answer the question using ONLY the information provided in the document above
2. If the answer is not found in the document, respond with "Sorry, I don't see that in the document."
3. Do not use any external knowledge or information not contained in the document
4. Be concise and accurate

Answer:"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based strictly on provided document content. If information is not in the document, you must say so."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error getting AI response: {str(e)}"

# Initialize the QA system with the markdown file
qa_system = MarkdownQA('data.md')

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle question submission and return AI response"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'error': 'Please provide a question'
            }), 400
        
        # Get answer from the QA system
        answer = qa_system.get_answer(question)
        
        return jsonify({
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/reload', methods=['POST'])
def reload_document():
    """Reload the markdown document"""
    try:
        qa_system.load_markdown('data.md')
        return jsonify({
            'message': 'Document reloaded successfully'
        })
    except Exception as e:
        return jsonify({
            'error': f'Error reloading document: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("Starting DocChatWeb...")
    print("Make sure to set your OPENAI_API_KEY environment variable")
    print("Place your Markdown content in 'data.md' file")
    app.run(debug=True, host='0.0.0.0', port=5000)