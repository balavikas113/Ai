import os
from openai import OpenAI
import gradio as gr

# Step 1: Setup function with OpenAI configuration
def setup_openai_client():
    # Hardcoded API key for DeepSeek
    api_key = "sk-c10f285bc9564b3e8f954ffcee4caebe"  # Replace with your actual DeepSeek API key
    
    # Create client with DeepSeek configuration
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")  # Using DeepSeek's API endpoint
  
    return client

# Step 2: Text generation function with optimized prompt
def generate_text(prompt):
    try:
        client = setup_openai_client()
        
        response = client.chat.completions.create(
            model="deepseek-chat",  # Using DeepSeek's model
            messages=[  
                {  
                    "role": "system",  
                    "content": (  
                        "You are a **Code Guru**, an expert at analyzing code snippets and providing concise, "
                        "actionable feedback. Your role is to evaluate code for quality, efficiency, and "
                        "readability while suggesting improvements. Structure your response as follows:\n\n"
                        
                        "### **1. OVERVIEW**\n"
                        "- Briefly summarize the code's purpose and structure.\n\n"
                        
                        "### **2. POTENTIAL ISSUES**\n"
                        "- Identify bugs, edge cases, or security vulnerabilities.\n"
                        "- Example: *'Missing input validation for negative numbers.'*\n\n"
                        
                        "### **3. EFFICIENCY IMPROVEMENTS**\n"
                        "- Suggest optimizations (e.g., time/space complexity).\n"
                        "- Example: *'Use memoization to avoid redundant calculations.'*\n\n"
                        
                        "### **4. READABILITY IMPROVEMENTS**\n"
                        "- Recommend better variable names, comments, or formatting.\n"
                        "- Example: *'Rename `x` to `user_input` for clarity.'*\n\n"
                        
                        "### **5. BEST PRACTICES**\n"
                        "- Highlight deviations from language conventions (PEP 8 for Python).\n"
                        "- Example: *'Use `snake_case` for function names.'*\n\n"
                        
                        "### **6. ALTERNATIVE APPROACHES**\n"
                        "- Propose simpler or more elegant solutions if applicable.\n"
                        "- Example: *'This logic could be simplified with list comprehension.'*\n\n"
                        
                        "**Tone:** Professional, direct, and supportive. Reference specific lines when possible."
                    )  
                },  
                {  
                    "role": "user",  
                    "content": f"CODE TO ANALYZE:\n\n{prompt}"  
                }  
            ],
            max_tokens=1024,  # Increased for detailed analysis
            temperature=0.3,  # Balanced creativity
            top_p=0.9,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# Step 3: Gradio interface
def create_interface():
    return gr.Interface(
        fn=generate_text,
        inputs=gr.Textbox(label="Code Snippet", lines=10, placeholder="Paste your code here..."),   
        outputs=gr.Textbox(label="Code Analysis", lines=20),
        title="🔍 Code Guru AI",
        description="Get detailed code analysis with actionable improvement suggestions.",
        examples=[
            ["def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)"],
            ["def calculate_average(numbers):\n    return sum(numbers)/len(numbers)"],
            ["for i in range(10):\n    print(i**2)"],
        ],
        allow_flagging="never"
    )

# Step 4: Run the application
if __name__ == "__main__":
    interface = create_interface()
    interface.launch()
    