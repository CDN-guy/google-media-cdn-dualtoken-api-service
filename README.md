# Google Media CDN Signed Request and Dual-token Authentication TokenGen API Service

## What is it?
This example demonstrates how to host a Media CDN signed request and dual-token authentication token generator on [Google Cloud Run](https://cloud.google.com/run) as a standalone API service. This approach eliminates the need to integrate the token generation code directly into your application code base, simplifying your workflow and streamlining content protection.

Media CDN supports multiple signed request / token options to help protect your content from unauthorized distribution.
* [Signatures](https://cloud.google.com/media-cdn/docs/signed-requests): Media CDN uses a single signature to help protect content.
* [Tokens](https://cloud.google.com/media-cdn/docs/use-dual-token-authentication): Media CDN uses tokens to help protect content. You can choose to use either single-token or dual-token authentication.
  * with [dual-token authentication](https://cloud.google.com/media-cdn/docs/use-dual-token-authentication), Media CDN uses a **short-duration token** for playback initiation, and a **long-duration token** for the remainder of the playback session. 

> Looking for step-by-step instructions to enable Signed Request / Dual-token authentication? 
>
> These are the public docs from Google Cloud.
> * [Signed Reqeusts](https://cloud.google.com/media-cdn/docs/signed-requests)
> * [Dual-token Authenticaiton](https://cloud.google.com/media-cdn/docs/use-dual-token-authentication)


> Looking for Source codes?
> Google published the code samples written in [Python](https://cloud.google.com/media-cdn/docs/generate-tokens#mediacdn_dualtoken_sign_token-python), [Java](https://cloud.google.com/media-cdn/docs/generate-tokens#mediacdn_dualtoken_sign_token-java), and [Ruby](https://github.com/GoogleCloudPlatform/ruby-docs-samples/tree/main/media_cdn).

## Prerequisites
First, you need to have a Google Cloud account. Don't have one? Sign up for [Free Trial](https://console.cloud.google.com/getting-started)  

Second, Make sure you install the latest [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)

## How to deploy?

1. Clone this repo.
   ```
   git clone https://github.com/CDN-guy/google-media-cdn-dualtoken-api-service.git
   ```

1. Change directories to the source.
   ```
   cd google-media-cdn-dualtoken-api-service
   ```

2. Run the following command. Note: you can change `google-cdn-token-gen-api` to a preferred service name.
    ```
    gcloud run deploy google-cdn-token-gen-api --source .
    ```

3. When prompt "Please specify a region: ", **select a region that closest to you**

4. When prompt "Allow unauthenticated invocations (y/N)? ", **enter Y**

5. Wait a few mins for the service to deploy. Once deployment is completed, you should receive the service url like this:
    ```
    https://google-cdn-token-gen-api-<random_string>-uc.a.run.app
    ```


## How to use?
Construct a **POST** request with the required and/or optional fields in JSON format to the service endpoint: `https://google-cdn-token-gen-api-<random_string>-uc.a.run.app/<service-api>`

| services | service-apis |
|---|---|
| Signed Requests | /sign-url |
| Signed Requests | /sign_url-prefix |
| Signed Requests | /sign-cookie |
| Signed Requests | /sign-path-component |
| Dual-token Authentication | /sign-token |


Examples of POST body in JSON:
```
{
    
    "base64_key" = "DJUcnLguVFKmVCFnWGubG1MZg7fWAnxacMjKDhVZMGI=",
    "signature_algorithm" = "Ed25519",
    "start_time": "2022-09-13T00:00:00Z",
    "expiration_time": "2022-09-13T12:00:00Z",
    "path_globs": "/*",
    "data": "test-data",
    "headers":[{
        "name": "Foo",
        "value": "bar"
    },
    {
        "name": "BAZ",
        "value": "quux"
    }],
    "ip_ranges": "203.0.113.0/24,2001:db8:4a7f:a732/64"
}
```

For all token fields, check this out: 
[Required token fields](https://cloud.google.com/media-cdn/docs/generate-tokens#required-token-fields),
[Optional token fields](https://cloud.google.com/media-cdn/docs/generate-tokens#optional-token-fields)



You should expect to get the following response from the service endpoint, with **token** filed contains the generated token value,  **signature_algorithem** field indicates the token signature, and **expireation_time** field indicates the expiry time.  

```
{
    "expiration_time": "Sat, 12 Aug 2023 00:47:54 GMT",
    "signature_algorithm": "Ed25519",
    "token": "URLPrefix=Lyo~Expires=1691801274~Signature=3DePhQwntI5LaXS-lGCe7dXRdToKEBC3tF_A1hjzBK7VkB9ibdHqjKuccL41-R_KMxA3UyRUve_Dgg8XuDhXAA"
}
```

 OK, REAY TO GO! HAPPY STREAMING!

## How to get the base64-encoded token keys?

1. Ed25519 Private/Public Key Pair
   ```
   # generate an ed25519 key pair
   openssl genpkey -algorithm ed25519 -outform PEM -out ed25519.key

   # base64-encoded private key 
   openssl pkey -outform DER -in ed25519.key | tail -c +17 | python3 -c "import base64, sys; print(('%s' % base64.urlsafe_b64encode(sys.stdin.buffer.read()))[2:-1])"

   # base64-encoded public key
   openssl pkey -outform DER -pubout -in ed25519.key | tail -c +13 | python3 -c "import base64, sys; print(('%s' % base64.urlsafe_b64encode(sys.stdin.buffer.read()))[2:-1])"
   ```

1. HAMC-based Secret Key
   ```
   # generate HAMC secret key
   python3 -c "import secrets;open('token.secret','wb').write(secrets.token_bytes(32))"

   # base64-encoded secret key
   cat token.secret| python3 -c "import base64, sys; print(('%s' % base64.urlsafe_b64encode(sys.stdin.buffer.read()))[2:-1])"
   ```




## Licensing

* See [LICENSE](LICENSE)

