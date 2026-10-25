#!/usr/bin/env python3
"""Synthetic sealed-checkpoint metric adjudication, includes malicious self-consistent re-sealing."""
from pathlib import Path
import tempfile,sys,math,json
import primary_case as m
import numpy as np

def run():
 u=np.arange(1,32,dtype=float);v=u.copy();v[0]=3.5
 metrics=m.stability(u,v,[[i] for i in range(31)])
 scientific={'gate':'R7-D35-PF4-PRIMARY-P1','status':'PRIMARY_CASE_ORDINAL_COMMITTED','task':'TON2','family':'LIN_SGD_LOGISTIC','seed':11,'ordinal':0,'x_test_index':287,'clean_class':0,'source_count':31,'encoded_count':153,'original_full_xai_ordinal_not_deduplicated':True,'primary_PF4_authorized_by_user':True,'PF5_executed':False,'n_applicable':1,'n_NA':2,'profile':{'ordinal':0,'x_test_index':287,'clean_predicted_class':0,'clean_single_predicted_class':0,'clean_batch_predicted_class':0,'source_magnitude_shap':list(map(float,u)),'source_signed_shap':list(map(float,u)),'source_features':['s'+str(i) for i in range(31)]},'stability':[dict(ordinal=0,draw=0,status='APPLICABLE',perturbed_source_magnitude_shap=list(map(float,v)),perturbed_source_signed_shap=list(map(float,v)),prediction_stable=True,perturbed_predicted_class=0,**metrics),dict(ordinal=0,draw=0,status='NOT_APPLICABLE',jaccard_10=None,prediction_stable=None),dict(ordinal=0,draw=0,status='NOT_APPLICABLE',jaccard_10=None,prediction_stable=None)],'ablation':[dict(score_drop=-.10,clean_historical_native_score=.70,ablated_historical_native_score=.80),dict(score_drop=.20,clean_historical_native_score=.70,ablated_historical_native_score=.50)],'additivity':[{'absolute_residual':1e-6},{'absolute_residual':2e-6}]}
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'ordinal_000000';m.commit(p,scientific);m.verify_checkpoint(p,'TON2','LIN_SGD_LOGISTIC',11,0)
  sc=p/'scientific.json';record=m.read(sc);record['stability'][0]['jaccard_10']=.12345;sc.write_bytes(m.encode(record));seal=m.read(p/'COMMITTED.json');seal['files']['scientific.json']={'sha256':m.sha(sc),'bytes':sc.stat().st_size};(p/'COMMITTED.json').write_bytes(m.encode(seal))
  try:m.verify_checkpoint(p,'TON2','LIN_SGD_LOGISTIC',11,0)
  except m.PrimaryFailure as e:assert 'METRIC_RECONCILIATION' in str(e),str(e)
  else:raise AssertionError('SEMANTIC_TAMPER_NOT_REJECTED')
  print('PF4_PRIMARY_METRIC_NEGATIVE_TEST=PASS::SIGNED_NEGATIVE_DROP_PRESERVED::REAL_SEAL_ADJUDICATION::RESEALED_METRIC_TAMPER_REJECTED')
if __name__=='__main__':run()
