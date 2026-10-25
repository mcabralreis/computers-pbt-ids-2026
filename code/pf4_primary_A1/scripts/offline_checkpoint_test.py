#!/usr/bin/env python3
"""No model loading: exercise real production execute/commit/resume/tamper pathways with explicit synthetic records."""
from __future__ import annotations
import tempfile,json
from pathlib import Path
import primary_case as m

def run():
 rows,d24,d32=m.manifest()
 original_load=m.load_context;original_one=m.one_profile
 try:
  def fake_load(root,task,family,seed,row,d24):return {'raw':[{}]*1000}
  def fake_one(ctx,task,family,seed,j):
   return {'original_full_xai_ordinal_not_deduplicated':True,'source_count':31,'encoded_count':153,'clean_class':0,'profile':{'ordinal':j,'x_test_index':j,'clean_predicted_class':0,'clean_single_predicted_class':0,'clean_batch_predicted_class':0,'source_magnitude_shap':list(range(1,32)),'source_signed_shap':list(range(1,32)),'source_features':['feature_'+str(i) for i in range(31)]},'gate':'R7-D35-PF4-PRIMARY-P1','task':task,'family':family,'seed':seed,'ordinal':j,'x_test_index':j,'primary_PF4_authorized_by_user':True,'PF5_executed':False,'n_applicable':0,'n_NA':3,'stability':[{'ordinal':j,'status':'NOT_APPLICABLE','draw':0,'jaccard_10':None,'prediction_stable':None}]*3,'ablation':[{'ordinal':j,'score_drop':0.0,'clean_historical_native_score':.75,'ablated_historical_native_score':.75}]*2,'additivity':[{'ordinal':j,'absolute_residual':0.0}]}
  m.load_context=fake_load;m.one_profile=fake_one
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);store=root/'primary_store';store.mkdir();case=store/'TON2'/'LIN_SGD_LOGISTIC'/'seed_11';ck=case/'checkpoints'
   m.execute(root,store,'TON2','LIN_SGD_LOGISTIC',11,3)
   assert sorted(p.name for p in ck.iterdir())==['ordinal_000000','ordinal_000001','ordinal_000002']
   m.execute(root,store,'TON2','LIN_SGD_LOGISTIC',11,5)
   assert len(list(ck.iterdir()))==8
   p=ck/'ordinal_000000';s=p/'scientific.json';original=s.read_bytes();s.write_bytes(original+b'\n')
   try:m.execute(root,store,'TON2','LIN_SGD_LOGISTIC',11,1)
   except m.PrimaryFailure as e:assert 'CHECKPOINT_BYTES' in str(e)
   else:raise AssertionError('TAMPER_NOT_DETECTED')
   s.write_bytes(original);(ck/'ordinal_000008.staging').mkdir()
   try:m.execute(root,store,'TON2','LIN_SGD_LOGISTIC',11,1)
   except m.PrimaryFailure as e:assert 'CHECKPOINT_UNRECOGNIZED' in str(e)
   else:raise AssertionError('STAGING_NOT_DETECTED')
   print('PF4_PRIMARY_ATOMIC_RESUME_TEST=PASS::3_PLUS_5_SEALED::NO_RECOMPUTE::TAMPER_REJECTED::STAGING_REJECTED')
 finally:m.load_context=original_load;m.one_profile=original_one
if __name__=='__main__':run()
