 
import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

discord_token = os.getenv("SECRET_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
model_name=os.getenv("MODEL_NAME")
max_discord_message_length=int(os.getenv("MAX_DISCORD_MESSAGE_LENGTH"))


genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name=model_name)

# with open("chat.txt" , "r") as f:
#     chat = f.read()

# chat = ""

def query_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        print(response.text)
        return response.text
    except Exception as e:
        print("Gemini error:", str(e))
        return "❌ Gemini API error."
    


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'✅ Logged in as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        # global chat
        # chat += f"{message.author}: {message.content}\n"
        if self.user != message.author and self.user in message.mentions:
            # prompt = f"{chat}\nCdacGPT: "
            prompt = message.content

            reply = query_gemini(prompt)

            for i in range(0, len(reply), max_discord_message_length):
                await message.channel.send(reply[i:i+max_discord_message_length])



intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_token)