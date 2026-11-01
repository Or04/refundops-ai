from api import app, simulation, validate_policy, Policy
from engine import DEFAULT_POLICY
from fastapi.testclient import TestClient

def test_overview_has_real_pending():
    c=TestClient(app);r=c.get('/api/overview');assert r.status_code==200
    d=r.json();assert len(d['items'])==len(__import__('pandas').read_csv('data/pending.csv'))

def test_simulation_identity_has_no_changes():
    impact=simulation(DEFAULT_POLICY)
    assert impact['pending_changes']==[] and impact['new_auto_exposure_usd']==0

def test_invalid_policy_rejected():
    from fastapi import HTTPException
    p=Policy(**{**DEFAULT_POLICY,'auto_max_usd':9999})
    try:validate_policy(p)
    except HTTPException as e:assert e.status_code==400
    else:assert False

def test_review_requires_note():
    c=TestClient(app);r=c.post('/api/review/RF-1067',json={'decision':'approve','note':'  '});assert r.status_code==400

def test_time_machine_historical_replay():
    impact=simulation({**DEFAULT_POLICY,'auto_max_usd':75})
    assert impact['historical_changed_count']==len(impact['history_changes'])
    assert impact['historical_new_auto_exposure_usd']>=0
    assert isinstance(impact['historical_new_auto_cases'],list)

def test_versions_endpoint():
    c=TestClient(app)
    r=c.get('/api/policy/versions')
    assert r.status_code==200 and 'active' in r.json()

def test_rollback_unknown_version_rejected():
    c=TestClient(app)
    version=c.get('/api/overview').json()['version']
    r=c.post('/api/policy/rollback',json={'target_version':-1,'expected_version':version,'rationale':'test'})
    assert r.status_code==404
