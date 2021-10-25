import os

import pymsteams
from flask import request, jsonify, Flask
from waitress import serve

TOKEN = os.environ.get("TOKEN")

app = Flask(__name__)


@app.route('/webhook/<token>', methods=['POST'])
def alert_processor(token):
    if token == '' or token != TOKEN:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    if not data:
        return jsonify({'error': 'Bad Request. No data received'}), 400
    process_payload(request.json)
    return jsonify({'message': 'Processed successfully'}), 200


@app.errorhandler(500)
def internal_error(e):
    print("Server Internal Error occurred: " + str(e))
    return jsonify(error=str(e)), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


def process_payload(payload):
    status = payload['status'].upper()
    if status == 'FIRING':
        color = "#ff0000"  # red
    elif status == "RESOLVED":
        color = "#196F3D"  # green
    else:
        color = "#F8C471"  # yellow
    ms_teams_webhook_url = os.environ.get('MS_TEAMS_WEBHOOK_URL', '')
    ms_teams_message = pymsteams.connectorcard(ms_teams_webhook_url)
    ms_teams_message.title(f"{status}: {payload['commonAnnotations']['summary']}")
    ms_teams_message.text(payload['commonAnnotations']['description'])
    ms_teams_message.color(color)
    details_section = pymsteams.cardsection()
    details_section.title("<b>Labels</b>")
    details_section.addFact("alertname", payload['commonLabels']['alertname'])
    details_section.addFact("application", payload['commonLabels']['application'])
    details_section.addFact("region", payload['commonLabels']['region'])
    details_section.addFact("organization", payload['commonLabels']['organization'])
    details_section.addFact("space", payload['commonLabels']['space'])
    details_section.addFact("severity", payload['commonLabels']['severity'])
    ms_teams_message.addSection(details_section)
    ms_teams_message.send()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    serve(app, host='0.0.0.0', port=port, url_scheme='https')
