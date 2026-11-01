"""Local demo API. No payments, no authentication, no external LLM calls."""
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import json
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import DEFAULT_POLICY, decide, batch
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'
STATE=ROOT/'.demo_state.json'
app=FastAPI(title='RefundOps | Home Assignment')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_methods=['*'],allow_headers=['*'])

def records(file):return pd.read_csv(DATA/file,keep_default_na=False).to_dict('records')
def load_state():
    if STATE.exists():
        try:return json.loads(STATE.read_text())
        except (ValueError,OSError):pass
    return {'policy':dict(DEFAULT_POLICY),'reviews':{},'audit':[],'version':1,'policy_history':[]}
def save(state):STATE.write_text(json.dumps(state,indent=2,default=str))
def now():return datetime.now(timezone.utc).isoformat()
def view():
    s=load_state(); items=[]
    for r in records('pending.csv'):
        result=decide(r,s['policy']); item={**r,**result.__dict__}; manual=s['reviews'].get(str(r['request_id']))
        item['review_decision']=manual;item['status']='resolved' if manual and manual.get('decision') in ('approve','reject') else ('escalated' if manual and manual.get('decision')=='escalate' else ('auto_eligible' if result.action=='approve' else 'needs_review'))
        items.append(item)
    return items

class Review(BaseModel):
    decision:str
    note:str
class Policy(BaseModel):
    auto_max_usd:float
    min_tenure_months:float
    max_prior_refunds:float
    manual_above_usd:float
    damage_photo_above_usd:float
    auto_wrong_item:bool=False
    auto_stolen_card_confirmed:bool=False
    rationale:str=''
    expected_version:Optional[int]=None

@app.get('/api/overview')
def overview():
    items=view();return {'items':items,'policy':load_state()['policy'],'version':load_state()['version'],'history_count':len(records('history.csv')),'pending_count':len(items)}
@app.get('/api/history')
def history():return records('history.csv')
@app.get('/api/audit')
def audit():return load_state()['audit'][::-1]
@app.post('/api/review/{request_id}')
def review(request_id:str, payload:Review):
    if payload.decision not in ('approve','reject','escalate'):raise HTTPException(400,'Invalid decision')
    if not payload.note.strip():raise HTTPException(400,'Review note is required')
    if request_id not in {str(x['request_id']) for x in records('pending.csv')}:raise HTTPException(404,'Request not found')
    case=next(x for x in view() if str(x['request_id'])==request_id)
    if case['status']=='auto_eligible':raise HTTPException(409,'Auto-eligible requests are not in the human review queue')
    if case['status'] in ('resolved','escalated'):raise HTTPException(409,'Case already has a reviewer decision')
    if payload.decision=='approve' and str(case.get('fraud_flag','')).strip().lower()=='yes':raise HTTPException(409,'Fraud-flagged case cannot be approved without verified fraud-team evidence')
    s=load_state();s['reviews'][request_id]={'decision':payload.decision,'note':payload.note.strip(),'at':now(),'actor':'Demo reviewer'}
    s['audit'].append({'type':'REVIEW_DECISION','request_id':request_id,'decision':payload.decision,'note':payload.note.strip(),'at':now()});save(s)
    return {'ok':True,'review':s['reviews'][request_id]}

def validate_policy(p):
    if p.auto_max_usd<=0 or p.manual_above_usd<=0 or p.damage_photo_above_usd<=0 or p.min_tenure_months<0 or p.max_prior_refunds<0:raise HTTPException(400,'Invalid policy thresholds')
    if p.auto_max_usd>p.manual_above_usd:raise HTTPException(400,'Auto approval cap must not exceed mandatory review threshold')

def simulation(proposed):
    s=load_state();pending=records('pending.csv');history=records('history.csv');old=s['policy'];new=proposed
    def diff(rows):
        changes=[]
        for row in rows:
            before=decide(row,old);after=decide(row,new)
            if before.action!=after.action or before.rule!=after.rule:
                changes.append({'request_id':row['request_id'],'amount_usd':after.amount_usd,'before':before.action,'after':after.action,'before_rule':before.rule,'after_rule':after.rule})
        return changes
    pending_changes=diff(pending);historical_changes=diff(history)
    newly_approved=[x for x in pending_changes if x['before']!='approve' and x['after']=='approve']
    warnings=[]
    if proposed.get('auto_stolen_card_confirmed'):warnings.append('HIGH RISK: fraud confirmation is inferred from free-text notes, not verified against a fraud-team system. Demo only.')
    if proposed.get('auto_wrong_item'):warnings.append('Wrong-item warehouse confirmation uses unverified text matching. Demo only.')
    if float(proposed['auto_max_usd'])>float(old['auto_max_usd']):warnings.append('Approval exposure increased: review new approvals before activation.')
    return {'pending_changes':pending_changes,'history_changes':historical_changes,'historical_changed_count':len(historical_changes),'historical_changed_amount_usd':round(sum(x['amount_usd'] or 0 for x in historical_changes),2),'historical_new_auto_count':sum(x['before']!='approve' and x['after']=='approve' for x in historical_changes),'historical_new_auto_exposure_usd':round(sum(x['amount_usd'] or 0 for x in historical_changes if x['before']!='approve' and x['after']=='approve'),2),'historical_new_auto_cases':[{'request_id':x['request_id'],'amount_usd':x['amount_usd'],'outcome_note':next((str(r.get('outcome_note','')) for r in history if str(r['request_id'])==str(x['request_id'])),''),'historical_decision':next((str(r.get('decision','')) for r in history if str(r['request_id'])==str(x['request_id'])),''),'warning':'Historical decisions are noisy and not ground truth'} for x in historical_changes if x['before']!='approve' and x['after']=='approve'][:30],'new_auto_count':len(newly_approved),'new_auto_exposure_usd':round(sum(x['amount_usd'] or 0 for x in newly_approved),2),'warnings':warnings,'before_auto_count':sum(decide(r,old).action=='approve' for r in pending),'after_auto_count':sum(decide(r,new).action=='approve' for r in pending)}
@app.post('/api/policy/simulate')
def simulate(p:Policy):
    validate_policy(p)
    proposed=p.model_dump(exclude={'rationale','expected_version'})
    impact=simulation(proposed)
    state=load_state()
    state['last_preview']={'version':state['version'],'policy':proposed,'at':now()}
    save(state)
    return impact
@app.post('/api/policy/activate')
def activate(p:Policy):
    validate_policy(p)
    if p.expected_version is not None and p.expected_version!=load_state()['version']:raise HTTPException(409,'Policy version changed. Re-run the simulation before activation')
    if not p.rationale.strip():raise HTTPException(400,'Change rationale required')
    s=load_state();new=p.model_dump(exclude={'rationale','expected_version'})
    preview=s.get('last_preview')
    if not preview or preview.get('version')!=s['version'] or preview.get('policy')!=new:
        raise HTTPException(409,'Simulate this exact policy against the current version before activation')
    impact=simulation(new)
    if impact['warnings'] and (new['auto_stolen_card_confirmed'] or new['auto_wrong_item']):raise HTTPException(400,'Unverified text evidence cannot be used to activate high-risk auto-approval rules')
    s.pop('last_preview',None)
    old=s['policy'];s.setdefault('policy_history',[]).append({'version':s['version'],'policy':old,'at':now()});s['policy']=new;s['version']+=1
    s['audit'].append({'type':'POLICY_ACTIVATED','version':s['version'],'at':now(),'rationale':p.rationale,'before':old,'after':new,'impact':impact});save(s)
    return {'ok':True,'version':s['version'],'impact':impact}
@app.post('/api/reset')
def reset():
    if STATE.exists():STATE.unlink()
    return {'ok':True}

@app.get('/api/policy/versions')
def versions():
    s=load_state()
    return {'active':{'version':s['version'],'policy':s['policy']},'previous':s.get('policy_history',[])[::-1]}

class Rollback(BaseModel):
    target_version:int
    expected_version:int
    rationale:str

@app.post('/api/policy/rollback')
def rollback(payload:Rollback):
    s=load_state()
    if payload.expected_version!=s['version']:raise HTTPException(409,'Policy version changed; refresh before rollback')
    if not payload.rationale.strip():raise HTTPException(400,'Rollback rationale required')
    target=next((x for x in s.get('policy_history',[]) if x['version']==payload.target_version),None)
    if not target:raise HTTPException(404,'Policy version not found')
    impact=simulation(target['policy'])
    if impact['warnings'] and (target['policy'].get('auto_stolen_card_confirmed') or target['policy'].get('auto_wrong_item')):raise HTTPException(400,'Unsafe rollback blocked')
    previous=s['policy'];s['policy']=target['policy'];s.setdefault('policy_history',[]).append({'version':s['version'],'policy':previous,'at':now()});s['version']+=1
    s['audit'].append({'type':'POLICY_ROLLBACK','version':s['version'],'target_version':payload.target_version,'at':now(),'rationale':payload.rationale,'impact':impact});save(s)
    return {'ok':True,'version':s['version'],'impact':impact}

# Agentic investigation: bounded, evidence-based tool workflow. No LLM or payment execution.
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

@app.get('/api/agent/investigate/{request_id}')
def agent_investigate(request_id:str):
    cases=view()
    case=next((r for r in cases if str(r['request_id'])==request_id),None)
    if case is None:raise HTTPException(404,'Case not found')
    history_rows=records('history.csv')
    same_customer=[r for r in history_rows if str(r.get('customer_id'))==str(case.get('customer_id'))]
    same_reason=[r for r in history_rows if str(r.get('stated_reason','')).strip().lower()==str(case.get('stated_reason','')).strip().lower()]
    evidence=[{'field':'amount_usd','value':case.get('amount_usd')},{'field':'fraud_flag','value':case.get('fraud_flag')},{'field':'stated_reason','value':case.get('stated_reason')},{'field':'support_note','value':case.get('support_note')},{'field':'days_since_delivery','value':case.get('days_since_delivery')}]
    trace=[{'tool':'load_request','status':'complete','detail':f"Loaded {request_id} from pending.csv"},{'tool':'check_policy','status':'complete','detail':f"Matched {case['rule']} against active policy v{load_state()['version']}"},{'tool':'lookup_history','status':'complete','detail':f"Found {len(same_customer)} historical requests for this customer"},{'tool':'compare_cohort','status':'complete','detail':f"Found {len(same_reason)} requests with the same reason"},{'tool':'evaluate_guardrails','status':'complete','detail':'Payment actions unavailable; reviewer approval required for exceptions'}]
    checks=[]
    if str(case.get('fraud_flag')).lower()=='yes':checks.append('Fraud-team verification required; no independent fraud system is connected')
    if case['rule']=='PHOTO_REQUIRED':checks.append('Image evidence not independently verified')
    if case['rule']=='CARRIER_CHECK':checks.append('Carrier proof unavailable in the supplied data')
    if case['rule']=='DATA_INVALID':checks.append('Source data invalid or incomplete')
    if not checks:checks.append('Verify source evidence and policy applicability before a manual decision')
    return {'request_id':request_id,'recommendation':'AUTO-ELIGIBLE' if case['action']=='approve' else 'HUMAN REVIEW','risk':case['risk'],'policy_rule':case['rule'],'summary':case['reason'],'evidence':evidence,'tool_trace':trace,'historical_customer_cases':len(same_customer),'historical_reason_cases':len(same_reason),'open_questions':checks,'limitations':'Deterministic agent workflow. No external LLM, no external tools, no payments. Historical outcomes are not ground truth.'}

@app.get('/experience')
def experience():return FileResponse(ROOT/'experience'/'index.html')
