
import requests
import time

# --- CONFIGURATION ---
WALLET = "7hQrTMwrUbZVfpiMSjRpMkeWKgszuAoMVDKGbjFCh13y"
BOT_TOKEN = "7621052158:AAEsxkndRtysQu-tPGXe0-C8XxQEfFO22Nc"
CHAT_ID = "5015545212"
CHECK_INTERVAL = 15  # in seconds
SEEN_TXS = set()

# --- HELPER FUNCTIONS ---

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def get_latest_txs(wallet):
    url = "https://api.mainnet-beta.solana.com"
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [wallet, {"limit": 10}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json().get("result", [])
        return result
    except Exception as e:
        print(f"RPC error: {e}")
        return []

# --- MAIN MONITOR LOOP ---

def monitor():
    print(f"Monitoring wallet: {WALLET}")
    while True:
        txs = get_latest_txs(WALLET)
        for tx in txs:
            sig = tx["signature"]
            if sig not in SEEN_TXS:
                message = (
                    "*New transaction detected:*

"
                    f"`{sig}`
"
                    f"[View on Solana Explorer](https://solscan.io/tx/{sig})"
                )
                print(f"New TX: {sig}")
                send_telegram_alert(message)
                SEEN_TXS.add(sig)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()
