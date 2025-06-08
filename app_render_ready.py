from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

def send_email(data_dict):
    msg = EmailMessage()
    msg['Subject'] = 'نموذج سيرة ذاتية جديد'
    msg['From'] = 'aalghamdi4810@stu.kau.edu.sa'
    msg['To'] = 'aalghamdi4810@stu.kau.edu.sa'

    body = "\n".join([f"{k}: {v}" for k, v in data_dict.items()])
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('aalghamdi4810@stu.kau.edu.sa', 'udvg sduz fmcb nxuu')
        smtp.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = request.form.to_dict(flat=False)
        df = pd.DataFrame.from_dict(data, orient="index").T
        filename = f"cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)
        send_email({k: ', '.join(v) for k, v in data.items()})
        return "تم الإرسال بنجاح"
    return render_template("form.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))