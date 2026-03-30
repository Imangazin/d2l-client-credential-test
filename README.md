# d2l client credentials grant type authentication test
Simple for dev purposes
## Steps
* Create private.key and public.pem within the same folder.
  
  ```openssl genpkey -algorithm RSA -out private.key -pkeyopt rsa_keygen_bits:2048```
  
  ```openssl rsa -in private.key -pubout -out public.pem```
  
* Convert public key to JWKS
  
  run jwsk-generator.py to generate jwsk.json file
* Host jwsk (https required)
* OAuth2 app on d2l
  
  Set up d2l OAuth2 app with the necessary scope and server user with permissions needed for the task
* run auth2.py to test
  
  Plug in

          BRIGHTSPACE_BASE_URL = 
          CLIENT_ID = 
          KID =   # must match the "kid" in your JWKS
          SCOPES = 
  from the OAuth2 app and jwks.json then run.
