def test_jwt():
    import jwt

    with open("key.pem", "rb") as f:
        public_key = f.read()

    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJOb21icmUiOiJhIiwiUm9sIjoiVXN1YXJpbyIsIkFwZWxsaWRvIjoiYSIsIkVtYWlsIjoiYUBob3RtYWlsLmNvbSIsIkN1aWwiOiIxIiwiRXN0YWRvIjoiVHJ1ZSIsIkVzdGFkb0NyZWRpdGljaW8iOiJUcnVlIiwibmJmIjoxNzA5MDU3MjQzLCJleHAiOjE3MDkxNDM2NDMsImlzcyI6IlNSVlAiLCJhdWQiOiJ0b21vcnJvdyJ9.pqSnblHfw5TBTs6776JINSGxvycslb0KerfYUaRV5KgiIwFzJLrIx_SYP873UjePvJO2u0ozdgogQsN08cg8f-fQAp_a35Er1CMpT0Nom5OM5f_vwRfiL7vL3Ogt964y5cddQVajxbRhD3D07GXJzFwDMDrADn0pXGVS9ERT0WvyycOjxcN3C43dRXQmXh0J5imIUJSERrrIjYJRr-UOjW__KDvjyyXVFOPsxXZ7In80VyU0OTP5iEsBH1WXs90TrsAcZr7yUsyqkUHuMlXK9pLIKakTnaEkyIliHIf9x4H4tUfszJ_bWHJ1jLMXBFjZkyBReyG7MWJhBJVonQX3jg"
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        options={
            "verify_exp": False,  # Skipping expiration date check
            "verify_aud": False,
        },
        # if jose.exceptions.JWTError: The specified alg value is not allowed, install cryptography
    )
    return payload
