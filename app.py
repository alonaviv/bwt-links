from flask import Flask, redirect, request
import requests
import threading
import time
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
WHATSAPP_GROUP = 'https://chat.whatsapp.com/La9NtdsfoXC0xKnCVjTdIw'


# def send_ga_event(utm_params, user_agent):
#     data = {
#         'v': '1',
#         'tid': app.config['GA_TRACKING_ID'],
#         'cid': '555',  # Anonymous Client ID. Ideally, generate this uniquely for each user/session.
#         't': 'event',
#         'ec': 'outbound',
#         'ea': 'redirect',
#         'el': 'whatsapp',
#         'cs': utm_params.get('utm_source'),
#         'cm': utm_params.get('utm_medium'),
#         'cn': utm_params.get('utm_campaign'),
#         # add other UTM parameters if needed
#     }
#     headers = {
#         'User-Agent': user_agent
#     }
#     endpoint = 'https://www.google-analytics.com/collect'
#     response = requests.post(endpoint, data=data, headers=headers)


def send_fb_pixel_event(fbclid):
    data = {
        "data": [{
            "event_name": "JoinWhatsApp",
            "event_time": int(time.time()),
            "action_source": "website",
            "custom_data": {"fbclid": fbclid} if fbclid else {}
        }]

    }
    fb_endpoint = f"https://graph.facebook.com/v18.0/{app.config['PIXEL_ID']}/events?access_token={app.config['PIXEL_ACCESS_TOKEN']}"
    res = requests.post(fb_endpoint, json=data)
    print(res.text)


@app.route('/whatsapp-from-lineapp')
def redirect_whatsapp_on_lineapp():
    referer = request.headers.get("Referer", "")

    query_parameters = parse_qs(urlparse(referer).query)

    fbclid = query_parameters.get('fbclid', [None])[0]
    user_agent = request.headers.get('User-Agent')
    utm_params = {key: value for key, value in request.args.items() if key.startswith('utm_')}

    # threading.Thread(target=send_ga_event, args=(utm_params, user_agent)).start()
    threading.Thread(target=send_fb_pixel_event, args=(fbclid,)).start()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>This is a test page</h1>
        <p>referer: {referer}</p>
        <p>Got {fbclid}</p>
    </body>
    </html>
    """

    return redirect(WHATSAPP_GROUP, code=302)


if __name__ == "__main__":
    # TODO Figure out production settings
    app.run(debug=True)
