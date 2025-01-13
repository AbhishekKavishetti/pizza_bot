from flask import Flask, request, jsonify, render_template
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext, ActivityHandler
from botbuilder.schema import Activity
import asyncio

app = Flask(__name__)

# Initialize the Bot Framework Adapter with empty settings
adapter_settings = BotFrameworkAdapterSettings(app_id=None, app_password=None)
adapter = BotFrameworkAdapter(adapter_settings)

# Chat history to store messages (this will reset when the server restarts)
chat_history = []

# Create a bot class by inheriting ActivityHandler
class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text  # Get the user's input
        response = handle_user_input(user_input)  # Process user query

        # Add the user input and bot response to chat history
        chat_history.append({"user": user_input, "bot": response})

        # Send the bot's response
        await turn_context.send_activity(f"Bot: {response}")

        # Format the conversation history
        formatted_history = "\n".join(
            f"User: {entry['user']}\nBot: {entry['bot']}" for entry in chat_history
        )
        await turn_context.send_activity(f"Conversation History:\n{formatted_history}")

# Instantiate the bot
bot = MyBot()

# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Flask will look for `index.html` in the `templates` folder

@app.route('/api/messages', methods=['POST'])
def messages():
    try:
        body = request.json
        user_message = body.get("text", "")
        bot_response = handle_user_input(user_message)
        chat_history.append({"user": user_message, "bot": bot_response})
        return jsonify({"response": bot_response, "history": chat_history})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

def handle_user_input(user_input):
    """
    Processes user input and generates a bot response.
    """
    if "types of pizza" in user_input.lower():
        return "We offer Small, Medium, and Large pizzas with toppings like Pepperoni, Mushrooms, and Onions."
    elif "cost" in user_input.lower():
        return "Small ($10), Medium ($15), Large ($20). Toppings: $2 each."
    elif "hi" in user_input.lower():
        return "Hi there! Ask me about pizzas!"
    else:
        return "Sorry, I didn't understand. Try asking about pizza types or costs."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
