 
import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

discord_token = os.getenv("SECRET_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name='gemini-2.5-flash')

with open("chat.txt" , "r") as f:
    chat = f.read()

# chat = ""

def query_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini error:", str(e))
        return "❌ Gemini API error."

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'✅ Logged in as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        global chat
        chat += f"{message.author}: {message.content}\n"
        if self.user != message.author and self.user in message.mentions:
            prompt = f"{chat}\nCdacGPT: "
            reply = query_gemini(prompt)
            await message.channel.send(reply)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_token)