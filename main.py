import os
import datetime
import base64
import dualtoken
import snippets


from flask import Flask, request, make_response
from flask import jsonify

app = Flask(__name__)

## definite global parameters
# set token key
# token_base64_key = b"DJUcnLguVFKmVCFnWGubG1MZg7fWAnxacMjKDhVZMGI="
# set signature_algorithm
# signature_algorithm = "Ed25519"

def is_valid_base64(bytes):
    """
    Checks if a string is a valid Base64 encoded string, optionally with a specific length.

    Args:
        string: The string to check.
        expected_length: (Optional) The expected length of the decoded string.

    Returns:
        True if the string is valid Base64 and matches the expected length (if provided), False otherwise.
    """

    try:
        decoded = base64.urlsafe_b64encode(bytes)
        # if expected_length is not None and len(decoded) != expected_length:
        #     return False
        return True
    except (base64.binascii.Error, ValueError):  # Catch decoding errors
        return False

# Flask default behavior: DENY all traffic except /dual-token
@app.route('/', defaults={'path': ''},methods=['POST','HEAD','GET'])
@app.route('/<path:path>',methods=['POST','HEAD','GET'])
def catch_all(path):
    response = make_response("Token Gen Service only listens on paths: /dual-token, /sign-url, /sign-url-prefix, /sign-cookie, /sign-path-component for POST requests")
    response.status_code = 403
    return response

# Flask /dual-token
@app.route("/dual-token", methods=['POST'])
def token_gen():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req_body = request.json
        try:
            ## Enforce Input Validation Check & set default token parameters
            if 'base64_key' not in req_body:
                raise Exception("base64_key cannot be empty")
            elif not is_valid_base64(req_body['base64_key'].encode('utf-8')):
                raise Exception("base64_key invalid")
            if 'signature_algorithm' not in req_body:
                raise Exception("signature_algorithm cannot be empty")
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
                base64_key = req_body['base64_key'].encode('utf-8'),
                signature_algorithm = req_body['signature_algorithm'],
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
            return jsonify(token=output_token, expiration_time=req_body['expiration_time'], signature_algorithm=req_body['signature_algorithm'])
        
        except Exception as e:
            response = make_response(f"TokenGenError: {e}")
            response.status_code = 403
            return response
    else:
        response = make_response("TokenGenError: Content-Type not supported")
        response.status_code = 403
        return response

# Flask /sign-url 
@app.route("/sign-url", methods=['POST'])
def sign_url_gen():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req_body = request.json
        try:
            ## Enforce Input Validation Check & set default token parameters
            if 'base64_key' not in req_body:
                raise Exception("base64_key cannot be empty")
            elif not is_valid_base64(req_body['base64_key'].encode('utf-8')):
                raise Exception("base64_key invalid")
            if 'expiration_time' not in req_body:
                expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                req_body['expiration_time'] = expiration_time
            else:
                e_time = req_body['expiration_time']
                datetime.datetime.fromisoformat(e_time.replace('Z', '+00:00'))
                req_body['expiration_time'] = datetime.datetime.strptime(req_body['expiration_time'],"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
            if 'url' not in req_body:
                raise Exception("url cannot be empty")
            if 'key_name' not in req_body:
                raise Exception("key_name cannot be empty")
                        
            # generate sign_url
            output_token = snippets.sign_url(
                base64_key = req_body['base64_key'].encode('utf-8'),
                expiration_time = req_body['expiration_time'],
                key_name = req_body['key_name'],
                url = req_body['url']
            )
            return jsonify(sign_url=output_token, expiration_time=req_body['expiration_time'])
        
        except Exception as e:
            response = make_response(f"TokenGenError: {e}")
            response.status_code = 403
            return response
    else:
        response = make_response("TokenGenError: Content-Type not supported")
        response.status_code = 403
        return response

# Flask /sign-url-prefix
@app.route("/sign-url-prefix", methods=['POST'])
def sign_url_prefix_gen():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req_body = request.json
        try:
            ## Enforce Input Validation Check & set default token parameters
            if 'base64_key' not in req_body:
                raise Exception("base64_key cannot be empty")
            elif not is_valid_base64(req_body['base64_key'].encode('utf-8')):
                raise Exception("base64_key invalid")
            if 'expiration_time' not in req_body:
                expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                req_body['expiration_time'] = expiration_time
            else:
                e_time = req_body['expiration_time']
                datetime.datetime.fromisoformat(e_time.replace('Z', '+00:00'))
                req_body['expiration_time'] = datetime.datetime.strptime(req_body['expiration_time'],"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
            if 'url' not in req_body:
                raise Exception("url cannot be empty")
            if 'url_prefix' not in req_body:
                raise Exception("url_prefix cannot be empty")
            if 'key_name' not in req_body:
                raise Exception("key_name cannot be empty")
                        
            # generate sign_url_prefix
            output_token = snippets.sign_url_prefix(
                base64_key = req_body['base64_key'].encode('utf-8'),
                expiration_time = req_body['expiration_time'],
                key_name = req_body['key_name'],
                url = req_body['url'],
                url_prefix= req_body['url_prefix']
            )
            return jsonify(sign_url_prefix=output_token, expiration_time=req_body['expiration_time'])
        
        except Exception as e:
            response = make_response(f"TokenGenError: {e}")
            response.status_code = 403
            return response
    else:
        response = make_response("TokenGenError: Content-Type not supported")
        response.status_code = 403
        return response

# Flask /sign-cookie
@app.route("/sign-cookie", methods=['POST'])
def sign_cookie_gen():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req_body = request.json
        try:
            ## Enforce Input Validation Check & set default token parameters
            if 'base64_key' not in req_body:
                raise Exception("base64_key cannot be empty")
            elif not is_valid_base64(req_body['base64_key'].encode('utf-8')):
                raise Exception("base64_key invalid")
            if 'expiration_time' not in req_body:
                expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                req_body['expiration_time'] = expiration_time
            else:
                e_time = req_body['expiration_time']
                datetime.datetime.fromisoformat(e_time.replace('Z', '+00:00'))
                req_body['expiration_time'] = datetime.datetime.strptime(req_body['expiration_time'],"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
            if 'url_prefix' not in req_body:
                raise Exception("url_prefix cannot be empty")
            if 'key_name' not in req_body:
                raise Exception("key_name cannot be empty")
                        
            # generate sign_cookie
            output_token = snippets.sign_cookie(
                base64_key = req_body['base64_key'].encode('utf-8'),
                expiration_time = req_body['expiration_time'],
                key_name = req_body['key_name'],
                url_prefix= req_body['url_prefix']
            )
            return jsonify(sign_cookie=output_token, expiration_time=req_body['expiration_time'])
        
        except Exception as e:
            response = make_response(f"TokenGenError: {e}")
            response.status_code = 403
            return response
    else:
        response = make_response("TokenGenError: Content-Type not supported")
        response.status_code = 403
        return response

# Flask /sign-path-component
@app.route("/sign-path-component", methods=['POST'])
def sign_path_component_gen():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req_body = request.json
        try:
            ## Enforce Input Validation Check & set default token parameters
            if 'base64_key' not in req_body:
                raise Exception("base64_key cannot be empty")
            elif not is_valid_base64(req_body['base64_key'].encode('utf-8')):
                raise Exception("base64_key invalid")
            if 'expiration_time' not in req_body:
                expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                req_body['expiration_time'] = expiration_time
            else:
                e_time = req_body['expiration_time']
                datetime.datetime.fromisoformat(e_time.replace('Z', '+00:00'))
                req_body['expiration_time'] = datetime.datetime.strptime(req_body['expiration_time'],"%Y-%m-%dT%H:%M:%S%z")
            if 'url_prefix' not in req_body:
                raise Exception("url_prefix cannot be empty")
            if 'key_name' not in req_body:
                raise Exception("key_name cannot be empty")
            if 'filename' not in req_body:
                raise Exception("filename cannot be empty")
                        
            # generate token
            output_token = dualtoken.sign_path_component(
                base64_key = req_body['base64_key'].encode('utf-8'),
                expiration_time = req_body['expiration_time'],
                url_prefix = req_body['url_prefix'],
                key_name = req_body['key_name'],
                filename = req_body['filename']
            )
            return jsonify(token=output_token, expiration_time=req_body['expiration_time'])
        
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
