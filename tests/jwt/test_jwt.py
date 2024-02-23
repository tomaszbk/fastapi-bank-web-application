def test_jwt():
    import jwt

    with open("key.pem", "rb") as f:
        public_key = f.read()

    token = "eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNyc2Etc2hhMjU2IiwidHlwIjoiSldUIn0.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiYSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IlVzdWFyaW8iLCJBcGVsbGlkbyI6ImEiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9lbWFpbGFkZHJlc3MiOiJhQGhvdG1haWwuY29tIiwiQ3VpbCI6IjEiLCJFc3RhZG8iOiJUcnVlIiwiRXN0YWRvQ3JlZGl0aWNpbyI6IlRydWUiLCJuYmYiOjE3MDg1Njg0NzQsImV4cCI6MTcwODY1NDg3NCwiaXNzIjoiU1JWUCIsImF1ZCI6InRvbW9ycm93In0.HUxRqOjg7LU9_S600CXzRDDo2tNFRY_coniphiX5rtIlduEYvEzZ9aIR3HZEjEgFtxMvIyWNaQTcxaUxU8JYOUq-09UjQ_LvJirij9TC7R24qK_UQSkpBw8GfMdKljSJEV4wsXLY9NlzLQu0toDapDaIWE628FECJ474-UV3pNc7CEjSScjz0Fnp2zWfofFqfoRZnkGfilYB-GOAe3WYefCOQ1N2pOOI2yaX3NWGa5pHiYUtcof41orXOyxA4RPnWse1aLxerYydzRA1IJoDW5bTcQ8QkRAjiaD1VmEtjt6XbcMfXphV3Lfy7KU-IcAPD5JqWJvEJmLpbRxG1LP7Rw"
    # jwt.encode({"A": 1}, public_key, algorithm="RS256")
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


payload = test_jwt()
