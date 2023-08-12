import os
import dualtoken
import datetime

from flask import Flask, request, make_response
from flask import jsonify

app = Flask(__name__)

## definite global parameters
# set token key
token_base64_key = b"DJUcnLguVFKmVCFnWGubG1MZg7fWAnxacMjKDhVZMGI="
# set signature_algorithm
signature_algorithm = "Ed25519"

# Flask default behavior: DENY all traffic except /token
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    response = make_response("Token Gen Service only listens on path /token for POST requests")
    response.status_code = 403
    return response

# Flask /token behavior: only accept POST method on /token
@app.route("/token", methods=['POST'])
def token_gen():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req_body = request.json
        try:
            ## Enforce Input Validation Check & set default token parameters
            if 'start_time' not in req_body:
                req_body['start_time'] = None
            else:
                datetime.datetime.fromisoformat(req_body['start_time'].replace('Z', '+00:00'))
                req_body['start_time'] = datetime.datetime.strptime(req_body['start_time'],"%Y-%m-%dT%H:%M:%S%z")
            if 'expiration_time' not in req_body:
                expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                req_body['expiration_time'] = expiration_time
            else:
                e_time = req_body['expiration_time']
                datetime.datetime.fromisoformat(e_time.replace('Z', '+00:00'))
                req_body['expiration_time'] = datetime.datetime.strptime(req_body['expiration_time'],"%Y-%m-%dT%H:%M:%S%z")
            if 'url_prefix' not in req_body:
                req_body['url_prefix']= None
            if 'full_path' not in req_body:
                req_body['full_path']= None
            if 'path_globs' not in req_body:
                req_body['path_globs']= None
            if 'session_id' not in req_body:
                req_body['session_id']= None
            if 'data' not in req_body:
                req_body['data']= None
            if 'headers' not in req_body:
                req_body['headers']= None
            if 'ip_ranges' not in req_body:
                req_body['ip_ranges']= None
                        
            # generate token
            output_token = dualtoken.sign_token(
                base64_key = token_base64_key,
                signature_algorithm = signature_algorithm,
                start_time = req_body['start_time'],
                expiration_time = req_body['expiration_time'],
                url_prefix = req_body['url_prefix'],
                full_path = req_body['full_path'],
                path_globs = req_body['path_globs'],
                session_id = req_body['session_id'],
                data = req_body['data'],
                headers = req_body['headers'],
                ip_ranges = req_body['ip_ranges']
            )
            return jsonify(token=output_token, expiration_time=req_body['expiration_time'], signature_algorithm=signature_algorithm)
        
        except Exception as e:
            response = make_response(f"TokenGenError: {e}")
            response.status_code = 403
            return response
    else:
        response = make_response("TokenGenError: Content-Type not supported")
        response.status_code = 403
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
