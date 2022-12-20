# Moto to test AWS DynamoDB

## Set Up Steps

1. Create a virtual environment ```python3 -m venv venv```
2. Activate the virtual environemnt ```source venv/bin/activate```
3. Run ```pip install -r requirements.txt``` for necessary packages

## Test Command

```pytest tests/```
```pytest tests/test_dynamodb.py```

### Debug Pro-Tip

Include "-s" inside test command to see print statements:
    ex: ```pytest -s tests/```

Include "-sv" for detailed list of pass/fail per test
