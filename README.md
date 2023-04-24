```
.
├── cdk_code
│   └── my_cdk_stack.py
├── src
│   └── lambdas
│       └── transformation
│           └── lambda_handler.py
└── tests
    └── unit
        └── lambdas
            └── transformation
                ├── test_lambda_handler.py
                ├── sample_data.csv
                └── test_event.json
```
---

```
.
├── cdk_code
│   ├── __init__.py
│   └── my_cdk_stack.py
├── src
│   ├── __init__.py
│   └── lambdas
│       ├── __init__.py
│       └── transformation
│           ├── __init__.py
│           └── lambda_handler.py
└── tests
    ├── __init__.py
    └── unit
        ├── __init__.py
        └── lambdas
            ├── __init__.py
            └── transformation
                ├── __init__.py
                ├── test_lambda_handler.py
                ├── sample_data.csv
                └── test_event.json
```


---

```
cdk init app --language python
.\.venv\Scripts\activate.ps1
pip install aws-cdk.aws-lambda aws-cdk.aws-s3 aws-cdk.aws-apigateway pandas boto3 pytest moto
```

---


```
mkdir -p cdk_code
mkdir -p src/lambdas/transformation
mkdir -p tests/unit/lambdas/transformation

New-Item -ItemType File cdk_code/my_cdk_stack.py
New-Item -ItemType File src/lambdas/transformation/lambda_handler.py
New-Item -ItemType File tests/unit/lambdas/transformation/test_lambda_handler.py
New-Item -ItemType File tests/unit/lambdas/transformation/sample_data.csv
New-Item -ItemType File tests/unit/lambdas/transformation/test_event.json
```

