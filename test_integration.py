from dotenv import load_dotenv
import os
import openai

def test_environment():
    # Load environment variables
    load_dotenv()
    
    # Test OpenAI key
    openai_key = os.getenv('OPENAI_API_KEY')
    print(f"OpenAI key loaded: {'sk-' in openai_key}")
    
    # Test Database path
    db_path = os.getenv('DATABASE_EXCEL_PATH')
    print(f"Database path exists: {os.path.exists(db_path)}")
    
    # Test actual OpenAI API
    try:
        openai.api_key = openai_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Say hello!"}],
            max_tokens=10
        )
        print("OpenAI API Test Response:", response.choices[0].message['content'])
        print("OpenAI API connection successful!")
    except Exception as e:
        print(f"OpenAI API Error: {e}")

if __name__ == "__main__":
    test_environment()