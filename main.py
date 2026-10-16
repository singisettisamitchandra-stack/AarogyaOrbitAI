
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from model import generate_response
from tools import calculate_grocery_budget, compare_budget


# --------------------------------------------------
# APP SETUP
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
SKILL_FILE = BASE_DIR / "SKILL.md"

app = FastAPI(
    title="AarogyaOrbit AI",
    description="AI health education and grocery budget assistant",
    version="1.0.0",
)

STATIC_DIR = BASE_DIR / "static"

if STATIC_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=STATIC_DIR),
        name="static",
    )


# --------------------------------------------------
# LOAD AI INSTRUCTIONS
# --------------------------------------------------

try:
    SKILL_INSTRUCTIONS = SKILL_FILE.read_text(encoding="utf-8")
except OSError:
    SKILL_INSTRUCTIONS = """
You are AarogyaOrbit AI, a helpful health education assistant.
Reply in the user's language.
Give general health information, not a medical diagnosis.
Do not prescribe medicines.
Clearly explain when someone should seek professional medical care.
Treat grocery prices and nutrition values as estimates.
"""


SYSTEM_PROMPT = f"""
{SKILL_INSTRUCTIONS}

You are AarogyaOrbit AI.
Be friendly, clear, and practical.
For health questions, provide general educational information.
Never claim to diagnose a disease or prescribe medication.
For emergencies, advise the user to seek urgent medical help.
"""


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)


class GroceryPlanRequest(BaseModel):
    budget: float = Field(..., gt=0)
    people: int = Field(default=1, ge=1, le=20)
    days: int = Field(default=7, ge=1, le=31)
    preferences: str = Field(default="", max_length=1000)


class GroceryCalculateRequest(BaseModel):
    items: list[dict] = Field(..., min_length=1, max_length=100)
    budget: float = Field(..., gt=0)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AarogyaOrbit AI</title>
    <link rel="stylesheet" href="/static/style.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 850px;
            margin: 35px auto;
            padding: 20px;
            background: #f3f8f5;
            color: #20352c;
        }
        .container {
            background: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 5px 20px #00000010;
        }
        h1 { color: #16794b; }
        textarea {
            width: 100%;
            min-height: 110px;
            padding: 12px;
            box-sizing: border-box;
            border: 1px solid #ccd8d0;
            border-radius: 8px;
            font-size: 16px;
        }
        button, .link-button {
            display: inline-block;
            background: #16794b;
            color: white;
            border: none;
            padding: 12px 18px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            margin-top: 10px;
        }
        button:hover, .link-button:hover { background: #105e38; }
        #answer {
            white-space: pre-wrap;
            line-height: 1.6;
            margin-top: 20px;
        }
        .hint { color: #627269; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌿 AarogyaOrbit AI</h1>
        <p>Your AI assistant for general health education and everyday wellness.</p>

        <label for="message"><strong>Ask your question</strong></label>
        <textarea id="message" placeholder="Ask a health or wellness question..."></textarea>

        <button id="sendButton" onclick="sendMessage()">Ask AarogyaOrbit AI</button>
        <a class="link-button" href="/grocery">Open Grocery Planner</a>

        <div id="answer" aria-live="polite"></div>
        <p class="hint">General educational information only; not a substitute for professional medical advice.</p>
    </div>

    <script>
        async function sendMessage() {
            const messageBox = document.getElementById("message");
            const answer = document.getElementById("answer");
            const button = document.getElementById("sendButton");
            const message = messageBox.value.trim();

            if (!message) {
                answer.textContent = "Please enter a question first.";
                return;
            }

            button.disabled = true;
            answer.textContent = "Thinking...";

            try {
                const response = await fetch("/api/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: message})
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || "Request failed.");
                }

                answer.textContent = data.reply;
            } catch (error) {
                answer.textContent = "Error: " + error.message;
            } finally {
                button.disabled = false;
            }
        }
    </script>
</body>
</html>
"""


# --------------------------------------------------
# CHAT API
# --------------------------------------------------

@app.post("/api/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    prompt = f"{SYSTEM_PROMPT}\n\nUser question:\n{message}"

    try:
        reply = generate_response(prompt)

        if not reply:
            raise HTTPException(
                status_code=502,
                detail="The AI model returned an empty response.",
            )

        return {"reply": str(reply)}

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "Could not get a response from the local AI model. "
                "Check that Ollama is running and the model is available. "
                f"Details: {exc}"
            ),
        ) from exc


# --------------------------------------------------
# GROCERY PLANNER PAGE
# --------------------------------------------------

@app.get("/grocery", response_class=HTMLResponse)
def grocery_page():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AarogyaOrbit AI - Grocery Planner</title>
    <link rel="stylesheet" href="/static/style.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 850px;
            margin: 35px auto;
            padding: 20px;
            background: #f3f8f5;
            color: #20352c;
        }
        .container {
            background: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 5px 20px #00000010;
        }
        h1 { color: #16794b; }
        label { display: block; margin-top: 14px; }
        input {
            width: 100%;
            box-sizing: border-box;
            padding: 11px;
            margin-top: 6px;
            border: 1px solid #ccd8d0;
            border-radius: 8px;
        }
        button, a {
            display: inline-block;
            background: #16794b;
            color: white;
            border: none;
            padding: 12px 18px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            margin-top: 15px;
        }
        #result {
            white-space: pre-wrap;
            line-height: 1.6;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 Grocery Budget Planner</h1>
        <p>Plan grocery spending based on your budget, household size, and number of days.</p>

        <label for="budget">Budget (₹)</label>
        <input id="budget" type="number" min="1" step="0.01" value="2000">

        <label for="people">Number of people</label>
        <input id="people" type="number" min="1" max="20" value="2">

        <label for="days">Number of days</label>
        <input id="days" type="number" min="1" max="31" value="7">

        <label for="preferences">Food preferences (optional)</label>
        <input id="preferences" type="text" placeholder="e.g. vegetarian, rice, dal">

        <button id="planButton" onclick="makePlan()">Create Grocery Plan</button>
        <a href="/">Back to Home</a>

        <div id="result" aria-live="polite"></div>
    </div>

    <script>
        async function makePlan() {
            const budget = Number(document.getElementById("budget").value);
            const people = Number(document.getElementById("people").value);
            const days = Number(document.getElementById("days").value);
            const preferences = document.getElementById("preferences").value.trim();
            const result = document.getElementById("result");
            const button = document.getElementById("planButton");

            if (budget <= 0 || people < 1 || days < 1) {
                result.textContent = "Enter a valid budget, number of people, and number of days.";
                return;
            }

            button.disabled = true;
            result.textContent = "Creating your grocery plan...";

            try {
                const response = await fetch("/api/grocery-plan", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        budget: budget,
                        people: people,
                        days: days,
                        preferences: preferences
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || "Could not create the plan.");
                }

                result.textContent = data.plan;
            } catch (error) {
                result.textContent = "Error: " + error.message;
            } finally {
                button.disabled = false;
            }
        }
    </script>
</body>
</html>
"""


# --------------------------------------------------
# GROCERY PLAN API
# --------------------------------------------------

@app.post("/api/grocery-plan")
def grocery_plan(request: GroceryPlanRequest):
    prompt = f"""
Create a practical grocery plan for a household.

Budget: ₹{request.budget:.2f}
People: {request.people}
Duration: {request.days} days
Food preferences: {request.preferences or "No preferences specified"}

Give:
1. A grocery list with approximate quantities.
2. Estimated costs in Indian rupees.
3. A total estimated cost.
4. Simple tips to stay within budget.

Do not claim that prices are live or verified.
If the budget is too small, explain that politely.
Keep the answer clear and easy to follow.
"""

    try:
        plan = generate_response(f"{SYSTEM_PROMPT}\n\n{prompt}")

        if not plan:
            raise HTTPException(
                status_code=502,
                detail="The AI model returned an empty plan.",
            )

        return {"plan": str(plan)}

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not generate the grocery plan: {exc}",
        ) from exc


# --------------------------------------------------
# GROCERY BUDGET CALCULATOR API
# --------------------------------------------------

@app.post("/api/grocery-calculate")
def grocery_calculate(request: GroceryCalculateRequest):
    try:
        result = calculate_grocery_budget(request.items)

        try:
            comparison = compare_budget(result, request.budget)
        except (TypeError, ValueError):
            comparison = None

        return {
            "calculation": result,
            "budget_comparison": comparison,
            "budget": request.budget,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not calculate the grocery budget. "
                "Check the item format expected by tools.py. "
                f"Details: {exc}"
            ),
        ) from exc


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": "AarogyaOrbit AI",
    }
