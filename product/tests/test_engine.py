from engine import decide,money,DEFAULT_POLICY
BASE={'request_id':'RF-TEST','amount_usd':25,'stated_reason':'wrong_size','fraud_flag':'no','tenure_months':24,'prior_refunds_12m':0,'days_since_delivery':5,'support_note':''}
def check(**changes):return decide({**BASE,**changes})
def test_small_eligible():assert check().action=='approve'
def test_bad_money():assert check(amount_usd='garbage').rule=='DATA_INVALID'
def test_currency_parse():assert money('USD 120.00')==120
def test_fraud_hold():assert check(fraud_flag='yes').rule=='FRAUD_HOLD'
def test_outside_window():assert check(stated_reason='changed_mind',days_since_delivery=15).rule=='OUTSIDE_WINDOW'
def test_photo():assert check(stated_reason='arrived_damaged',amount_usd=55).rule=='PHOTO_REQUIRED'
def test_never_arrived():assert check(stated_reason='never_arrived').rule=='CARRIER_CHECK'
def test_large():assert check(amount_usd=301).rule=='HIGH_AMOUNT'
def test_missing_history():assert check(tenure_months='').rule=='MISSING_HISTORY'
def test_partial_judgment():assert check(stated_reason='late_delivery').action=='review'
def test_policy_preview():assert check(amount_usd=75).action=='review' and decide({**BASE,'amount_usd':75},{'auto_max_usd':100}).action=='approve'
def test_stolen_confirmed_opt_in_is_still_held():
 assert decide({**BASE,'fraud_flag':'yes','support_note':'fraud team confirmed'},{'auto_stolen_card_confirmed':True}).rule=='FRAUD_HOLD'

def test_warehouse_note_never_auto_approves():
 assert decide({**BASE,'stated_reason':'wrong_item','support_note':'warehouse confirmed'},{'auto_wrong_item':True}).rule=='WRONG_ITEM_VERIFY'
