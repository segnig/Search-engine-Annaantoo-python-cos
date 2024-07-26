import os
import shutil
import logging
import asyncio
from telebot import TeleBot, types
from telebot.async_telebot import AsyncTeleBot
from similarity_measure import * 
from remove_stopping_words import *
from weighter import * 
from weight_to_file import *
from query_proccesor import *
from datetime import datetime


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# directories
TARGET_DIRECTORY = "corpus"
STEMMED_WORDS_DIRECTORY = "Stemmed-words"
INDEXED_FILE_LIST = "indexed_file/Uploaded_file.txt"
SEARCH_HISTORY_FILE = "search_history.txt"

# Ensure directories exist
for directory in [TARGET_DIRECTORY, STEMMED_WORDS_DIRECTORY, os.path.dirname(INDEXED_FILE_LIST)]:
    if not os.path.exists(directory):
        os.makedirs(directory)

TOKEN = '7084855614:AAE0Im0QxjGN_moEuuEjFIhdF5j-U0_1USY'

bot = AsyncTeleBot(TOKEN)

def log_search(query):
    with open(SEARCH_HISTORY_FILE, 'a') as f:
        f.write(f"{datetime.now()}: {query}\n")

async def handle_search(message: types.Message, query: str):
    log_search(query)
    await bot.send_message(message.chat.id, f"Searching for {query}...")
    try:
        results = QueryProcessor(query).process_results()
        if results:
            keyboard = types.InlineKeyboardMarkup()
            for i, result in enumerate(results):
                preview = f"{result['content'][:200]}..."
                button = types.InlineKeyboardButton(text=f"{result['title']}", callback_data=f"result_{query}_{i}")
                keyboard.add(button)
            await bot.send_message(message.chat.id, "Here are the results:", reply_markup=keyboard)
        else:
            await bot.send_message(message.chat.id, "No results found.")
    except Exception as e:
        await bot.send_message(message.chat.id, f"Error occurred: {str(e)}")

@bot.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Welcome to the AnnaanToo Search Engine Bot! Use /search <query> to perform a search.')

@bot.message_handler(commands=['search'])
async def search(message: types.Message):
    query = ' '.join(message.text.split()[1:])
    if query:
        await handle_search(message, query)
    else:
        await bot.send_message(message.chat.id, "Please provide a search query after /search command.")

@bot.message_handler(content_types=['document'])
async def upload(message: types.Message):
    if message.document:
        file_info = await bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        file_name = message.document.file_name
        downloaded_file = await bot.download_file(file_path)

        file_local_path = os.path.join(TARGET_DIRECTORY, file_name)
        if file_local_path.endswith(".txt"):
            with open(file_local_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            process_file(file_local_path)
            await bot.send_message(message.chat.id, f"File '{file_name}' processed successfully.")
        else:
            await bot.send_message(message.chat.id, "Invalid file format. Please upload a text file.")
    else:
        await bot.send_message(message.chat.id, "Please send a file to upload.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('result_'))
async def handle_result_click(callback_query: types.CallbackQuery):

    _, query, result_index_str = callback_query.data.split('_')
    result_index = int(result_index_str)
    
    try:

        results = QueryProcessor(query).process_results()
        if 0 <= result_index < len(results):
            result = results[result_index]
            details = f"Title: {result['title']}\nContent: {result['content'][:1000]}..."

            
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, details)

            print(result['file'])
            file = result['file']
            file = file[23:]
            file = file.split(r"__stemmed__.txt")[0]
            file = r"corpus\\" + file + ".txt"
            result['file'] = file
            if os.path.exists(result['file']):
                with open(result['file'], 'rb') as file:
                    await bot.send_document(callback_query.from_user.id, file, caption=result['title'])
            else:
                await bot.send_message(callback_query.from_user.id, "No file associated with this result.")
        else:
            await bot.send_message(callback_query.from_user.id, "Invalid result index.")
    except Exception as e:
        await bot.send_message(callback_query.from_user.id, f"Error occurred: {str(e)}")

@bot.message_handler(commands=['delete_file'])
async def delete_file(message: types.Message):
    file_name = ' '.join(message.text.split()[1:])
    if file_name:
        file_path = os.path.join(TARGET_DIRECTORY, file_name)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                await bot.send_message(message.chat.id, f"File '{file_name}' deleted successfully.")
            except Exception as e:
                await bot.send_message(message.chat.id, f"Error occurred while deleting file '{file_name}': {str(e)}")
        else:
            await bot.send_message(message.chat.id, f"File '{file_name}' not found.")
    else:
        await bot.send_message(message.chat.id, "Please provide a file name to delete.")

@bot.message_handler(commands=['list_files'])
async def list_files(message: types.Message):
    files = os.listdir(TARGET_DIRECTORY)
    if files:
        file_list = "\n".join(files)
        await bot.send_message(message.chat.id, f"Indexed files:\n{file_list}")
    else:
        await bot.send_message(message.chat.id, "No files found.")

@bot.message_handler(commands=['search_history'])
async def search_history(message: types.Message):
    if os.path.exists(SEARCH_HISTORY_FILE):
        with open(SEARCH_HISTORY_FILE, 'r') as f:
            history = f.readlines()
        if len(history) > 5:history = history[-5:]
        history = [line.strip() for line in history]
        history = "\n".join(history)
        if history:
            await bot.send_message(message.chat.id, f"Search history:\n{history}")
        else:
            await bot.send_message(message.chat.id, "No search history found.")
    else:
        await bot.send_message(message.chat.id, "No search history file found.")

@bot.message_handler(commands=['index_status'])
async def index_status(message: types.Message):
    await bot.send_message(message.chat.id, "Indexing status information is not yet implemented.")

@bot.message_handler(commands=['reindex'])
async def reindex(message: types.Message):
    await bot.send_message(message.chat.id, "Reindexing of files is not yet implemented.")

def process_file(file_path):
    base_name = os.path.basename(file_path)
    target_path = os.path.join(TARGET_DIRECTORY, base_name)

    uploaded_files = set()
    if os.path.exists(INDEXED_FILE_LIST):
        with open(INDEXED_FILE_LIST) as f:
            uploaded_files = {line.strip() for line in f}

    if base_name not in uploaded_files:
        try:
            shutil.copy(file_path, target_path)
        except Exception as e:
            logger.error(f"Error occurred while saving file '{base_name}': {str(e)}")

        if base_name not in uploaded_files:
            try:
                if not StopWords(target_path):
                    stemmed_file_path = os.path.join(STEMMED_WORDS_DIRECTORY, f"{base_name[:-4]}__stemmed__.txt")
                    Weights_TF_Matrix(stemmed_file_path)
                    logger.info(f"File '{base_name}' processed and weights updated.")
                else:
                    logger.warning(f"StopWords processing failed for file '{base_name}'.")
            except Exception as e:
                logger.error(f"Error occurred while processing file '{base_name}': {str(e)}")

async def main():
    await bot.polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise