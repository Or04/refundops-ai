import argparse
import pandas as pd
from engine import batch
p=argparse.ArgumentParser();p.add_argument('--input',default='data/pending.csv');p.add_argument('--output',default='decisions.csv');args=p.parse_args()
df=pd.read_csv(args.input).fillna('');required={'request_id','amount_usd','stated_reason','fraud_flag'}
if not required.issubset(df.columns):p.error('Missing required columns: '+str(required-set(df.columns)))
out=batch(df);out.to_csv(args.output,index=False)
print(f'{len(out)} evaluated; {(out.action=="approve").sum()} auto-approvable; {(out.action=="review").sum()} human review; saved {args.output}')
