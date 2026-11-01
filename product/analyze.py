import pandas as pd
from engine import batch
h=pd.read_csv('data/history.csv').fillna('');r=batch(h)
x=h.merge(r,on='request_id',suffixes=('','_engine'))
print('History',len(h),'auto',sum(h.decided_by=='auto'),'human',sum(h.decided_by!='auto'))
print('Replay approves',sum(r.action=='approve'),'review',sum(r.action=='review'))
print('Auto approvals historical',sum((r.action=='approve')&(h.decision=='approved')))
print('Historical non-approvals in auto group',sum((r.action=='approve')&(h.decision!='approved')))
print('Chargebacks',sum(h.outcome_note.astype(str).str.contains('chargeback',case=False)))
print('Appeal reversals',sum(h.outcome_note.astype(str).str.contains('overturned|refunded on appeal',case=False,regex=True)))
print('Review minutes',pd.to_numeric(h.review_minutes,errors='coerce').sum())
print('Policy rules\n',r.rule.value_counts().to_string())
