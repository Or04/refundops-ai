import json,os
from pathlib import Path
import pandas as pd
import streamlit as st
from engine import DEFAULT_POLICY,batch,decide
ROOT=Path(__file__).parent
st.set_page_config(page_title='Windward | Decision Intelligence',page_icon='◈',layout='wide')
st.markdown("""<style>
:root {color-scheme:dark}
.stApp{background:#071421;color:#e6f3fa}
[data-testid="stSidebar"]{background:#0a1d2e;border-right:1px solid #16364b}
.block-container{padding-top:1.6rem;max-width:1450px}
h1,h2,h3{letter-spacing:-.035em!important}
h1{font-size:2.1rem!important;font-weight:700!important}
.stMetric{background:linear-gradient(135deg,#0d2739,#0a1e2d);border:1px solid #244457;border-radius:14px;padding:18px}
[data-testid="stMetricValue"]{color:#e8faff}
[data-testid="stMetricLabel"]{color:#9bb4c4}
.stButton>button[kind="primary"]{background:#13c8d4;color:#04212c;border:0;font-weight:700}
.stButton>button{border-radius:9px}
[data-testid="stAlert"]{border-radius:10px}
div[data-testid="stDataFrame"]{border:1px solid #1d4356;border-radius:10px}
.brand{font-size:12px;font-weight:800;letter-spacing:.19em;color:#5bdde2;margin-bottom:8px}
.hero{background:radial-gradient(ellipse at 85% 20%,#174b61 0%,#0c2638 45%,#091b2b 100%);padding:26px 30px;border:1px solid #25546a;border-radius:16px;margin:10px 0 23px}
.hero h2{font-size:32px;margin:0;color:#f1fcff}.hero p{color:#aac6d5;margin:10px 0 0}
.eyebrow{color:#6fe2e4;letter-spacing:.16em;font-size:11px;font-weight:800}
.signal{border:1px solid #23495c;background:#0b2638;padding:17px;border-radius:12px}
</style>""",unsafe_allow_html=True)
@st.cache_data
def read_file(name):return pd.read_csv(ROOT/'data'/name).fillna('')
if 'policy' not in st.session_state:st.session_state.policy=DEFAULT_POLICY.copy()
if 'decisions' not in st.session_state:st.session_state.decisions={}
if 'audit' not in st.session_state:st.session_state.audit=[]
st.markdown('<div class="brand">◈ WINDWARD  /  DECISION INTELLIGENCE</div>',unsafe_allow_html=True)
st.markdown('<div class="hero"><span class="eyebrow">MISSION CONTROL / REFUND OPERATIONS</span><h2>Every decision. Accounted for.</h2><p>Signals into action · Explainable routing · Human oversight · Policy simulation</p></div>',unsafe_allow_html=True)
st.caption('Concept experience inspired by public Windward product language · Independent take-home prototype · No real payments')
page=st.sidebar.radio('Workspace',['Command center','Investigation queue','Policy simulator','Decision intelligence','Audit log'])
up=st.sidebar.file_uploader('Optional: upload pending-format CSV',type='csv')
try:pending=pd.read_csv(up).fillna('') if up else read_file('pending.csv')
except Exception as exc:st.error(f'Invalid CSV: {exc}');st.stop()
required=['request_id','amount_usd','stated_reason','fraud_flag']
if any(c not in pending for c in required):st.error('Missing required columns: '+', '.join(c for c in required if c not in pending));st.stop()
results=batch(pending,st.session_state.policy)
joined=pending.merge(results,on='request_id',suffixes=('','_engine'))
if page=='Command center':
    st.subheader('Operational picture')
    st.caption('Live routing snapshot across the uploaded decision set')
    a,b,c,d=st.columns(4)
    a.metric('Requests',len(results));b.metric('Auto-approvable',int((results.action=='approve').sum()));c.metric('Human review',int((results.action=='review').sum()));d.metric('Auto approval rate',f"{(results.action=='approve').mean():.0%}" if len(results) else '0%')
    st.markdown('#### Routing signals')
    x,y=st.columns([3,2])
    with x: st.bar_chart(results.rule.value_counts(),horizontal=True)
    with y:
        st.markdown('**Risk distribution**')
        st.bar_chart(results.risk.value_counts(),horizontal=True)
        st.markdown('**Control status**')
        st.success('No real payment integration')
        st.info('Uncertain evidence is routed to a human')
    st.info('Approvals are recommendations in this sandbox. No payments are issued. High-risk cases never get a free-form LLM approval.')
    st.dataframe(results[['request_id','action','amount_usd','reason','rule']],hide_index=True,use_container_width=True)
elif page=='Investigation queue':
    st.subheader('Investigation workbench')
    st.caption('Risk-prioritized cases with supporting signals and traceable human decisions')
    queue=joined[joined.action=='review'].copy()
    queue=queue[~queue.request_id.astype(str).isin(st.session_state.decisions)]
    st.caption(f'{len(queue)} open cases · prioritized by risk and requested amount')
    queue['risk_rank']=queue.risk.map({'high':0,'medium':1,'low':2}).fillna(3)
    queue=queue.sort_values(['risk_rank','amount_usd_engine'],ascending=[True,False])
    if queue.empty:st.success('Queue clear')
    else:
        st.dataframe(queue[['request_id','amount_usd_engine','stated_reason','risk','rule']],hide_index=True,use_container_width=True)
        rid=st.selectbox('Open case',queue.request_id.astype(str).tolist())
        r=queue[queue.request_id.astype(str)==rid].iloc[0];decision=decide(r.to_dict(),st.session_state.policy)
        l,k=st.columns([2,1])
        with l:
            st.markdown(f'### {rid} · ${decision.amount_usd:,.2f}')
            st.write('**Customer note:**',r.get('customer_note','') or 'Not provided')
            st.write('**Support evidence:**',r.get('support_note','') or 'Not provided')
            st.write('**Reason:**',r.get('stated_reason',''))
            st.write('**Customer tenure / prior refunds:**',r.get('tenure_months',''), '/',r.get('prior_refunds_12m',''))
        with k:
            st.warning(f'SIGNAL / {decision.rule}')
            st.write('**Decision rationale**',decision.reason)
            st.caption(f'RISK: {decision.risk.upper()}  |  EVIDENCE: {decision.evidence}')
        choice=st.radio('Reviewer action',['Approve','Reject','Partial','Escalate to fraud','Request evidence'],horizontal=True)
        amount=st.number_input('Partial amount (USD)',min_value=0.0,max_value=float(decision.amount_usd or 0),value=0.0) if choice=='Partial' else None
        explanation=st.text_area('Decision rationale (required)')
        if st.button('Record decision',type='primary',disabled=not explanation.strip() or (choice=='Partial' and (not amount or amount>=decision.amount_usd))):
            record={'request_id':rid,'action':choice,'partial_amount':amount,'rationale':explanation,'actor':'Demo reviewer','policy':st.session_state.policy.copy()}
            st.session_state.decisions[rid]=record;st.session_state.audit.append({'event':'reviewer_decision',**record});st.rerun()
elif page=='Policy simulator':
    st.subheader('Policy impact simulator')
    st.caption('Controlled change management · Compare the current and proposed decision boundaries')
    st.write('Change a control, replay every case, inspect the delta, and only then activate the policy.')
    p=st.session_state.policy.copy()
    l,r=st.columns(2)
    with l:
        cap=st.number_input('Auto approval cap ($)',min_value=1.0,max_value=300.0,value=float(p['auto_max_usd']))
        tenure=st.number_input('Minimum tenure (months)',min_value=0,max_value=120,value=int(p['min_tenure_months']))
        prior=st.number_input('Maximum prior refunds (12m)',min_value=0,max_value=20,value=int(p['max_prior_refunds']))
        threshold=st.number_input('Mandatory human review above ($)',min_value=1.0,max_value=10000.0,value=float(p['manual_above_usd']))
    with r:
        photo=st.number_input('Damaged-item photo threshold ($)',min_value=0.0,max_value=1000.0,value=float(p['damage_photo_above_usd']))
        wrong=st.checkbox('Auto approve warehouse-confirmed wrong item (demo note evidence)',value=p['auto_wrong_item'])
        stolen=st.checkbox('Auto approve fraud-team-confirmed stolen-card cases (demo note evidence)',value=p['auto_stolen_card_confirmed'])
        st.warning('Confirmation keywords in notes are NOT trusted evidence in production. These switches demonstrate manager-requested policy changes only.')
    draft={'auto_max_usd':cap,'min_tenure_months':tenure,'max_prior_refunds':prior,'manual_above_usd':threshold,'damage_photo_above_usd':photo,'auto_wrong_item':wrong,'auto_stolen_card_confirmed':stolen}
    new=batch(pending,draft);old=results
    c1,c2,c3=st.columns(3)
    c1.metric('Current approvals',int((old.action=='approve').sum()));c2.metric('Draft approvals',int((new.action=='approve').sum()),delta=int((new.action=='approve').sum()-(old.action=='approve').sum()));c3.metric('Changed routes',int((old.action!=new.action).sum()))
    delta=old[['request_id','action','rule']].merge(new[['request_id','action','rule']],on='request_id',suffixes=('_current','_draft'))
    st.dataframe(delta[(delta.action_current!=delta.action_draft)|(delta.rule_current!=delta.rule_draft)],hide_index=True,use_container_width=True)
    st.download_button('Export draft impact report',delta.to_csv(index=False),'policy_impact.csv')
    acknowledge=st.checkbox('I reviewed the impact and understand that this is a demo policy, not a payment authorization')
    if st.button('Publish draft policy',type='primary',disabled=not acknowledge):
        st.session_state.policy=draft;st.session_state.audit.append({'event':'policy_published','policy':draft.copy(),'changed_routes':int((old.action!=new.action).sum())});st.success('Policy published in this session');st.rerun()
elif page=='Decision intelligence':
    st.subheader('Decision intelligence explorer')
    st.dataframe(joined[['request_id','amount_usd_engine','stated_reason','action','reason','rule','risk','evidence']],hide_index=True,use_container_width=True)
    st.download_button('Export decisions CSV',results.to_csv(index=False),'decisions.csv')
else:
    st.subheader('Operational audit log')
    st.json(st.session_state.audit)
    st.caption('Session-only audit for demo. Production requires durable, tamper-evident logs and RBAC.')
