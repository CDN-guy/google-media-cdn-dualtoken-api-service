# Google MediaCDN Dual-token Authentication TokenGen API Service

## What it is?
This is an example of hosting the MediaCDN dual-token authentication token generator on [Cloud Run](https://cloud.google.com/run) as an API without the need of integrating the token generator into your code base.

Media CDN supports multiple signed request options to help protect your content from unauthorized distribution.
With [dual-token authentication](https://cloud.google.com/media-cdn/docs/use-dual-token-authentication), Media CDN uses a **short-duration token** for playback initiation, and a **long-duration token** for the remainder of the playback session. 
MediaCDN has extensive documentations on [how to generate tokens](https://cloud.google.com/media-cdn/docs/generate-tokens), the code samples are written in [Python](https://cloud.google.com/media-cdn/docs/generate-tokens#mediacdn_dualtoken_sign_token-python), [Java](https://cloud.google.com/media-cdn/docs/generate-tokens#mediacdn_dualtoken_sign_token-java), and [Ruby](https://github.com/GoogleCloudPlatform/ruby-docs-samples/tree/main/media_cdn).

Looking for enabling dual-token authentication? Follow this [step-by-step guide](https://cloud.google.com/media-cdn/docs/use-dual-token-authentication) from Google. 

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

1. Go to `main.py`, edit Line 12 & 14 to your own **Token Key** and **Signature Algorithm**, then save.
   ```
   token_base64_key = b"DJUcnLguVFKmVCFnWGubG1MZg7fWAnxacMjKDhVZMGI="

   signature_algorithm = "Ed25519"
   ```

1. Run the following command. Note: you can change `dual-token-gen-api` to a preferred service name.
    ```
    gcloud run deploy dual-token-gen-api --source .
    ```

1. When prompt "Please specify a region: ", **select a region that closest to you**

1. When prompt "Allow unauthenticated invocations (y/N)? ", **enter Y**

1. Wait a few mins for the service to deploy. Once deployment is completed, you should receive the service url like this:
    ```
    https://dual-token-gen-api-<random_string>-uc.a.run.app
    ```

## How to use?
Construct a **POST** request with the required and/or optional fields in JSON format to the service endpoint: `https://dual-token-gen-api-<random_string>-uc.a.run.app/token`

Example POST body in JSON:
```
{
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

## Licensing

* See [LICENSE](LICENSE)