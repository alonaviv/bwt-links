from flask import Flask, redirect

app = Flask(__name__)

WHATSAPP_GROUP = 'https://chat.whatsapp.com/La9NtdsfoXC0xKnCVjTdIw'


@app.route('/whatsapp-from-lineapp')
def redirect_whatsapp_on_lineapp():
    return redirect(WHATSAPP_GROUP, code=302)


if __name__ == "__main__":
    app.run(debug=True)
