from fastapi import FastAPI, HTTPException
import mathgenerator as mg  # Import the mathgenerator package
import os
import  uvicorn
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Math Problem Generator API!"}

def get_callable_topics():
    """
    Returns a sorted list of topic names (keys) from the mathgenerator module
    that are callable and do not start with '__'.
    """
    topics = [key for key in mg.__dict__.keys() if not key.startswith("__") and callable(mg.__dict__[key])]
    return sorted(topics)

@app.get("/topics")
def list_topics():
    """
    Lists all available topics with a corresponding topic ID.
    """
    topics = get_callable_topics()
    return {idx: topic for idx, topic in enumerate(topics)}

@app.get("/generate/{topic_id}")
def generate_math_problem(topic_id: int):
    """
    Generates a math problem for the given topic_id.
    The function associated with the topic should return either a tuple (problem, solution)
    or a single value (which will be converted to a string).
    """
    topics = get_callable_topics()
    if topic_id < 0 or topic_id >= len(topics):
        raise HTTPException(status_code=400, detail="Invalid topic ID. Please check /topics for available IDs.")
    
    topic_name = topics[topic_id]
    func = mg.__dict__.get(topic_name)
    
    if not callable(func):
        raise HTTPException(status_code=500, detail=f"Topic '{topic_name}' is not callable.")
    
    try:
        result = func()
        # Expecting a tuple with two elements (problem, solution)
        if isinstance(result, tuple) and len(result) == 2:
            problem, solution = result
        else:
            # If not a tuple, return the result as a string and leave solution empty
            problem, solution = str(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating math problem: {e}")
    
    return {"topic": topic_name, "problem": problem, "solution":solution}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0",  port =port,reload=True)
