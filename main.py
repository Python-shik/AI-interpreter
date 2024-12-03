import datetime
import os

from src.AI import prompts
from src import actions
from src.AI.BASE import Gen


if "gemini_api_key" not in os.listdir("src/AI/"):
    with open("src/AI/gemini_api_key", "w", encoding="utf-8") as f:
        f.write(input("[Gemini API Key] "))

ai = Gen()
ai.system_instructions = [
    {"text": prompts.Instructions.first_instruction},
    {"text": prompts.Instructions.action_instruction},
    {"text": prompts.Instructions.examples}]
ai.import_history_anyway("conversations/history")


msg = None

while True:
    if not msg:
        msg = f"{str(datetime.datetime.now())}\nfrom_user||"+input("[user] ")
    ai.history_add("user", msg)
    result = ai.generate()
    ai.history_add("assistant", result)
    try:
        target = result.split("||")[0]
        if target.lower() == "user":
            print("[assistant] " + result.split("||")[1])
            ai.export_history("conversations/history")
            msg = None

        elif target.lower() == "system":
            func4exec = result.split("||")[1]

            result = eval("actions."+func4exec)
            msg = f"{str(datetime.datetime.now())}\n{result.split('||')[1]}"
    except Exception as e:
        print(e)
        msg = 'error||' + str(e)