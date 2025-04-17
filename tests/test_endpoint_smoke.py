
import os
import boto3
import pandas as pd
import pytest
import json

@pytest.fixture(scope="session")
def endpoint_name():
    name = os.getenv("ENDPOINT_NAME")
    if not name:
        pytest.skip("No ENDPOINT_NAME env var set, skipping smoke test")
    return name

def test_endpoint_smoke(endpoint_name):
    # load a tiny slice of your prepared test data
    df = pd.read_csv("data/processed/test.csv", nrows=3)
    df = df.drop(columns=["Delay"]) #remove the Delay column
    payload = {"instances": df.to_dict(orient='records')}

    runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")
    resp = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload)
    )

    # basic assertions
    body = resp["Body"].read().decode("utf-8").strip()
    results = json.loads(body)["predictions"]
    assert len(results) == 3, f"Expected 3 preds, got {results!r}"
    for r in results:
        assert isinstance(r, (int, float)), f"Expected a number, got {type(r)}"