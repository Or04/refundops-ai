from fastapi.testclient import TestClient
from api import app
client=TestClient(app)
def test_experience_loads():
    r=client.get('/experience')
    assert r.status_code==200 and 'INVESTIGATION AGENT' in r.text
def test_agent_grounded_case():
    r=client.get('/api/agent/investigate/RF-1067')
    assert r.status_code==200
    data=r.json()
    assert data['request_id']=='RF-1067'
    assert len(data['tool_trace'])==5
    assert data['recommendation']=='HUMAN REVIEW'
def test_agent_missing_case():
    assert client.get('/api/agent/investigate/UNKNOWN').status_code==404
