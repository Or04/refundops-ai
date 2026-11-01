from fastapi.testclient import TestClient
from api import app


def test_fraud_review_approval_blocked():
    client=TestClient(app)
    r=client.post('/api/review/RF-1070',json={'decision':'approve','note':'Looks fine to me'})
    assert r.status_code==409


def test_review_queue_excludes_completed_cases_in_view(monkeypatch):
    import api
    monkeypatch.setattr(api,'load_state',lambda:{'policy':dict(api.DEFAULT_POLICY),'reviews':{'RF-1067':{'decision':'reject','note':'test'}},'audit':[],'version':1})
    item=next(x for x in api.view() if x['request_id']=='RF-1067')
    assert item['status']=='resolved'


def test_review_requires_valid_decision():
    client=TestClient(app)
    assert client.post('/api/review/RF-1067',json={'decision':'refund_now','note':'unsafe'}).status_code==400


def test_activation_requires_same_policy_preview(tmp_path,monkeypatch):
    import api
    from engine import DEFAULT_POLICY
    monkeypatch.setattr(api,'STATE',tmp_path/'state.json')
    client=TestClient(app)
    policy={**DEFAULT_POLICY,'auto_max_usd':75}
    payload={**policy,'expected_version':1,'rationale':'Controlled test'}
    assert client.post('/api/policy/activate',json=payload).status_code==409
    assert client.post('/api/policy/simulate',json=policy).status_code==200
    assert client.post('/api/policy/activate',json={**payload,'auto_max_usd':76}).status_code==409
    assert client.post('/api/policy/activate',json=payload).status_code==200
    assert client.get('/api/overview').json()['version']==2
