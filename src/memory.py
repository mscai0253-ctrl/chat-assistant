import pandas as pd
import os

FILE = "data/chat_logs.csv"

def save_chat(user, message, response):
    os.makedirs("data", exist_ok=True)

    df = pd.DataFrame([[user, message, response]],
                      columns=["User", "Message", "Response"])

    if os.path.exists(FILE):
        df.to_csv(FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(FILE, index=False)

def load_chat():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=["User", "Message", "Response"])