Config files are excluded from version control and must be collected manually.
We have converted the config files to single .env files for ease of use.
The .env file is also excluded from version control.
The .env file has KEY=VALUE pairs format and the values have no quotes.

    .env
        ## FASTAPI CONFIG
        FASTAPI_ENV=

        ## FIREBASE SERVICE ACCOUNT
        FIREBASE_TYPE=
        FIREBASE_PROJECT_ID=
        FIREBASE_PRIVATE_KEY_ID=
        FIREBASE_PRIVATE_KEY=
        FIREBASE_CLIENT_EMAIL=
        FIREBASE_CLIENT_ID=
        FIREBASE_AUTH_URI=
        FIREBASE_TOKEN_URI=
        FIREBASE_AUTH_PROVIDER_X509_CERT_URL=
        FIREBASE_CLIENT_X509_CERT_URL=

        ## FIREBASE CONFIG
        FIREBASE_API_KEY=
        FIREBASE_AUTH_DOMAIN=
        FIREBASE_DATABASE_URL=
        FIREBASE_STORAGE_BUCKET=
        FIREBASE_MESSAGING_SENDER_ID=
        FIREBASE_APP_ID=
        FIREBASE_MEASUREMENT_ID=

        ## MONGODB CONFIG
        MONGODB_DATABASE_URL=
        MONGODB_USERNAME=
        MONGODB_PASSWORD=

        ##  SENDGRID CONFIG
        SENDGRID_API_KEY=
        SENDGRID_FROM_EMAIL=
        SENDGRID_SERVER_EMAIL=
        SENDGRID_PORT=
        SENDGRID_USERNAME=
        SENDGRID_PASSWORD=
