from flask import Flask
import datetime

off_task = False

app = Flask(__name__)

@app.route('/off-task', methods=['GET', 'POST'])
def off_task_webhook():
    timestamp = datetime.datetime.now()
    print(f"Webhook received at {timestamp} /off-task")
    off_task = True

    with open("shared.info.txt", "w") as file:
        file.write(str(off_task))

    return f"Received at {timestamp}"

@app.route('/locked-in', methods=['GET', 'POST'])
def locked_in_webhook():
    timestamp = datetime.datetime.now()
    print(f"Webhook received at {timestamp} /locked-in")
    off_task = False

    with open("shared.info.txt", "w") as file:
        file.write(str(off_task))

    return f"Received at {timestamp}"

if __name__ == '__main__':
    with open("shared.info.txt", "w") as file:
        file.write("False")
    app.run(host='0.0.0.0', port=8000, debug=True)
