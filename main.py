import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from groq import Groq

# Initialize FastAPI
app = FastAPI()

# Mount the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Directly pass the API key for testing (use this only for testing, remove for production)
client = Groq(api_key='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')  # Replace with your actual API key


# Serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html") as f:
        return f.read()


# Endpoint to generate code using Groq
@app.post("/generate_code/")
async def generate_code(request: Request):
    data = await request.json()
    user_input = data.get("description", "")

    if not user_input:
        raise HTTPException(status_code=400, detail="Description is required.")

    try:
        # Use the Groq API to generate code based on the user input
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generate Python code for: {user_input}",
                }
            ],
            model="llama3-8b-8192",  # Specify the model you want to use
        )

        generated_code = chat_completion.choices[0].message.content
        return JSONResponse(content={"code": generated_code})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
