"""Auditable refund decision engine. Never executes a payment."""
import re
from dataclasses import dataclass,asdict
import pandas as pd

DEFAULT_POLICY = {'auto_max_usd':50.0,'min_tenure_months':6,'max_prior_refunds':1,'manual_above_usd':300.0,'damage_photo_above_usd':50.0,'auto_wrong_item':False,'auto_stolen_card_confirmed':False}
ALIASES={'changed mind':'changed_mind','arrived damaged':'arrived_damaged','damaged':'arrived_damaged','wrong item':'wrong_item','late':'late_delivery'}
@dataclass
class Result:
    request_id:str
    action:str
    reason:str
    rule:str
    amount_usd:float|None
    risk:str
    evidence:str

def money(value):
    try:
        s=re.sub(r'[^0-9.\-]','',str(value))
        n=float(s)
        return n if 0<n<=100000 else None
    except (ValueError,TypeError):return None

def clean(row):
    d=dict(row)
    d['amount_usd']=money(d.get('amount_usd'))
    d['stated_reason']=ALIASES.get(str(d.get('stated_reason','')).strip().lower(),str(d.get('stated_reason','')).strip().lower())
    return d

def numeric(v):
    try:
        n=float(v)
        return n if pd.notna(n) else None
    except (TypeError,ValueError):return None

def decide(raw,policy=None):
    p={**DEFAULT_POLICY,**(policy or {})};r=clean(raw);a=r['amount_usd'];rid=str(r.get('request_id','UNKNOWN'))
    def out(action,reason,rule,risk='medium',evidence='Structured fields'):
        return Result(rid,action,reason,rule,a,risk,evidence)
    if a is None:return out('review','Missing or invalid refund amount','DATA_INVALID','high')
    if str(r.get('fraud_flag','')).strip().lower() not in ('yes','no'):return out('review','Unknown fraud status','DATA_INVALID','high')
    reason=r['stated_reason'];note=' '.join(str(r.get(k,'') or '') for k in ('support_note','customer_note')).lower()
    if str(r.get('fraud_flag','')).strip().lower()=='yes':
        if p['auto_stolen_card_confirmed'] and 'fraud team confirmed' in note:
            return out('approve','Fraud team confirmation present; refund cardholder','FRAUD_CONFIRMED','high','Explicit fraud team confirmation in note (demo only)')
        return out('review','Fraud team verification required','FRAUD_HOLD','high')
    if a>float(p['manual_above_usd']):return out('review','Above manager review threshold','HIGH_AMOUNT','high')
    days=numeric(r.get('days_since_delivery'))
    if reason=='changed_mind':
        if days is None:return out('review','Delivery age unknown','MISSING_DELIVERY_AGE')
        if days>14:return out('review','Outside strict 14-day change-of-mind window; reviewer should reject unless data corrected','OUTSIDE_WINDOW','high')
    if reason=='arrived_damaged' and a>float(p['damage_photo_above_usd']):
        if not any(x in note for x in ('photo attached','photo received','image attached','picture attached')):
            return out('review','Photo evidence not verified','PHOTO_REQUIRED','medium','Support note keyword check, not image verification')
    if reason=='never_arrived':return out('review','Carrier delivery proof/investigation must be checked','CARRIER_CHECK','high')
    if reason=='late_delivery':return out('review','Partial refund amount requires reviewer judgment','PARTIAL_DISCRETION')
    if reason=='wrong_item':
        if p['auto_wrong_item'] and 'warehouse confirmed' in note:return out('approve','Warehouse confirmed picking error','WRONG_ITEM_CONFIRMED','medium','Support note keyword check, not independent warehouse verification')
        return out('review','Verify merchant picking error; policy requires full refund once confirmed','WRONG_ITEM_VERIFY')
    if reason not in ('wrong_size','changed_mind','arrived_damaged'):return out('review','Unknown reason','UNKNOWN_REASON','high')
    tenure=numeric(r.get('tenure_months'));prior=numeric(r.get('prior_refunds_12m'))
    if tenure is None or prior is None or prior<0:return out('review','Missing or invalid customer history','MISSING_HISTORY')
    if a>float(p['auto_max_usd']):return out('review','Above automatic approval cap','AUTO_CAP')
    if tenure<float(p['min_tenure_months']) or prior>float(p['max_prior_refunds']):return out('review','Customer history outside low-risk cohort','CUSTOMER_RISK')
    return out('approve','Low-value, eligible request with no known exception','LOW_RISK','low')

def batch(df,policy=None):
    return pd.DataFrame([asdict(decide(r,policy)) for r in df.to_dict('records')])
