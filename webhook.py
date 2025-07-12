from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test_webhook():
    timestamp = datetime.datetime.now()
    print(f"Webhook received at {timestamp}")
    return f"Received at {timestamp}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

