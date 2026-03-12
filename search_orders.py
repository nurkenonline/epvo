import json
import codecs

def main():
    try:
        with codecs.open('instructions/chat_epvo.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with codecs.open('search_orders.txt', 'w', encoding='utf-8') as out:
            for m in data.get('messages', []):
                text = m.get('text', '')
                if isinstance(text, list):
                    text = "".join([t if isinstance(t, str) else t.get('text', '') for t in text])
                
                if not isinstance(text, str):
                    continue
                    
                text_lower = text.lower()
                if 'отчисл' in text_lower and 'приказ' in text_lower:
                    date = m.get('date', '')
                    sender = m.get('from', '')
                    out.write(f"[{date}] {sender}: {text}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
