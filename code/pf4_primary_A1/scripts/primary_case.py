#!/usr/bin/env python3
"""PF4 PRIMARY: frozen full canonical XAI, case-scoped resumable scientific worker.
One atomic JSON + seal per original ordinal, no exploratory C3 reselection or new thresholds.
Separate user authorization recorded in PACKAGE_MANIFEST, D32 historical provenance immutable.
"""
from __future__ import annotations
import argparse, collections, csv, hashlib, importlib.util, json, math, os, sys, traceback
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent.parent
REF=HERE/'reference'
D24_SHA='8a86a9b4b56ad4f45abe72843890823bc3e2b381727a3863251d6ed6ad5bb72a'
D24_REPORT_SHA='82c50577baf1a21f453c18c79fc53719aaf7061ae5064e59a2adc58e918d5a2d'
D32_SHA='27470b04c90c024d56351e3196affe14966dae867cba0fe3fd25fd39257f3b40'
D15='scripts/C5K_P2_R4_R6_P4_R7_D15_exact_clean_perturbed_input_pilot.py';D15_SHA='524fd22b067bb8ded3d4bde0001f890f990fc655d3c9ed0df12370cb7232dd06'
R5='scripts/C5K_P2_R4_R6_P4_R5_all_seeds_non_rf_worker.py';R5_SHA='10c8ffb8d751ca15ac4c8aae0968888770538984bd5a1d83283efa0b6a8363ea'
R3='scripts/C5K_P2_R4_R6_P4_R3_fidelity_semantics_worker.py';R3_SHA='21024bdb4db1ddde5660ca4ceba4967b29a563f6a4678fd0ce02f92bfce559d1'
C4F='scripts/C4F_R3_parent_cleanup_test_resume.py';C4F_SHA='003c732a0095230414dcde617df47fe4039e09bcef0c3bb90b17f67dff2388e1'
LEVELS=(0.01,0.05,0.10); FAMS=('LIN_SGD_LOGISTIC','HGB','MLP'); TASKS=('CIC34','TON10','TON2'); SEEDS=(11,23,37,53,71)
BASE_SOURCE_MANIFEST_SHA='5b0d93bf99879ab676722450006959592b591e12fb4f08bf7ff3b55bc5823d70'
A1_ID='PF4-A1';A1_POLICY='BOUNDARY_TIE_NA';A1_DIAGNOSTIC_SHA='f158b6e905e7e5a8274bba484afadd97788f074276f6ca053e5002264a700af3'

class PrimaryFailure(RuntimeError):pass
def require(ok,code):
 if not ok:raise PrimaryFailure('PF4_PRIMARY_FAIL_CLOSED::'+str(code))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4<<20),b''):h.update(b)
 return h.hexdigest()
def hashbytes(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def encode(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8')
def write_new(p,x):
 p=Path(p);require(not p.exists(),'OVERWRITE::'+str(p));p.write_bytes(encode(x))
def pin(p,h,tag):
 require(p.is_file(),'MISSING::'+tag);require(sha(p)==h,'HASH::'+tag);return p
def mod(p,n):
 spec=importlib.util.spec_from_file_location(n,p);require(spec and spec.loader,'MODULE::'+str(p));x=importlib.util.module_from_spec(spec);spec.loader.exec_module(x);return x

def manifest():
 pin(REF/'D24_45_case_manifest.csv',D24_SHA,'D24');pin(REF/'D24_report.json',D24_REPORT_SHA,'D24_REPORT');pin(REF/'contract_D32.json',D32_SHA,'D32')
 d24=read(REF/'D24_report.json');d32=read(REF/'contract_D32.json');approval=read(HERE/'PRIMARY_AUTHORIZATION.json')
 require(d24['gate']=='R7-D24' and d24['status'].startswith('PASS_STATIC_45_CASE'),'D24_GATE')
 require(d32['version']=='D32-1.0' and d32['primary_PF4_approved'] is False,'HISTORICAL_D32_CHANGED')
 require(approval['primary_PF4_authorized_by_user'] is True and approval['scope']=='45 D24 cases, CIC34/TON10/TON2 x LIN_SGD_LOGISTIC/HGB/MLP x seeds 11,23,37,53,71' and approval['PF5_authorized'] is False,'PRIMARY_USER_AUTHORIZATION')
 with (REF/'D24_45_case_manifest.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 require(len(rows)==45 and len(set((r['task'],r['family'],int(r['seed'])) for r in rows))==45,'MATRIX_45_KEYS')
 require(set((r['task'],r['family'],int(r['seed'])) for r in rows)=={(t,f,s) for t in TASKS for f in FAMS for s in SEEDS},'MATRIX_EXACT_CARTESIAN')
 for r in rows:
  c=d24['cohorts'][r['task']];require(int(r['xai_rows'])==c['xai_rows'] and int(r['score_dim'])==c['output_dim'] and r['intensities']=='0.01|0.05|0.10' and int(r['draw'])==0,'D24_ROW::'+str(r))
 pm=read(HERE/'PACKAGE_MANIFEST.json');a1=read(HERE/'PF4_A1_AMENDMENT.json');diag=HERE/'reference/PF4_A1_BOUNDARY_TIE_DIAGNOSTIC.json'
 require(pm.get('amendment_id')==A1_ID and pm.get('base_source_manifest_sha256')==BASE_SOURCE_MANIFEST_SHA and pm.get('boundary_tie_policy')==A1_POLICY,'A1_PACKAGE_METADATA')
 require(a1.get('amendment_id')==A1_ID and a1.get('policy')==A1_POLICY and a1.get('base_source_manifest_sha256')==BASE_SOURCE_MANIFEST_SHA and a1.get('diagnostic_sha256')==A1_DIAGNOSTIC_SHA and a1.get('PF5_authorized') is False and a1.get('RF_authorized') is False,'A1_AMENDMENT_SCOPE')
 require(diag.is_file() and sha(diag)==A1_DIAGNOSTIC_SHA,'A1_DIAGNOSTIC_PIN')
 return rows,d24,d32

def source_groups(root,d15,ds,dim,expected):
 m=d15.outs(root/'C3C_P3A_artifacts/C3C_P3A_manifest.json')
 schema=d15.checked_member(root,m,f'C3C_P3A_artifacts/{ds}/encoded_feature_schema.csv');pre=d15.checked_member(root,m,f'C3C_P3A_artifacts/{ds}/preprocessor.json')
 pr=read(pre);enc_names=pr['encoded_feature_names'];require(len(enc_names)==dim and len(set(enc_names))==dim,'ENCODED_SCHEMA_NAMES')
 rr=d15.rows(schema);require(len(rr)==dim,'SCHEMA_ROWS')
 cols={x.lower().strip():x for x in rr[0]}
 def col(names):return next((cols[x] for x in names if x in cols),None)
 sn=col(('source_feature','source_feature_name','original_feature','original_feature_name','raw_feature','raw_feature_name','source_column','source_name'))
 en=col(('encoded_feature','encoded_feature_name','encoded_name','feature_name','name'))
 ix=col(('encoded_index','encoded_feature_index','feature_index','index','position','column_index'))
 require(sn and (en or ix),'MAPPING_FIELDS');ordered=[None]*dim
 for j,r in enumerate(rr):
  i=int(r[ix]) if ix else j;require(0<=i<dim and ordered[i] is None,'MAPPING_INDEX')
  require(not en or r[en]==enc_names[i],'MAPPING_NAME');ordered[i]=r[sn].strip()
 require(all(ordered),'MAPPING_MISSING');g=collections.OrderedDict()
 for i,n in enumerate(ordered):g.setdefault(n,[]).append(i)
 require(len(g)==expected and sorted(i for v in g.values() for i in v)==list(range(dim)),'SOURCE_COVERAGE')
 return list(g),list(g.values()),{'schema_sha256':sha(schema),'preprocessor_sha256':sha(pre)}

def rankavg(a):
 import numpy as np
 a=np.asarray(a,dtype=np.float64);ii=np.argsort(a,kind='mergesort');r=np.empty(len(a),np.float64);i=0
 while i<len(a):
  j=i+1
  while j<len(a) and a[ii[j]]==a[ii[i]]:j+=1
  r[ii[i:j]]=(i+j-1)/2+1;i=j
 return r

def topk_info(m,k):
 import numpy as np
 v=np.asarray(m,dtype=np.float64);require(len(v)>k and np.isfinite(v).all() and (v>=0).all(),'TOPK_INPUT')
 z=np.argsort(-v,kind='mergesort');boundary=float(v[z[k-1]]);tie=bool(v[z[k-1]]==v[z[k]])
 tied=[int(i) for i in range(len(v)) if v[i]==boundary] if tie else []
 return {'status':'NA_BOUNDARY_TIE' if tie else 'DEFINED','selection':None if tie else list(map(int,z[:k])),'boundary_value':boundary,'boundary_tied_indices':tied}

def topk(m,k):return topk_info(m,k)['selection']

def stability(a,b,groups):
 import numpy as np
 u=np.array([np.sum(np.abs(a[g]),dtype=np.float64) for g in groups]);v=np.array([np.sum(np.abs(b[g]),dtype=np.float64) for g in groups]);ru,rv=rankavg(u),rankavg(v)
 den=float(np.sqrt(np.sum((ru-ru.mean())**2)*np.sum((rv-rv.mean())**2)));sp=None if den==0 else float(np.sum((ru-ru.mean())*(rv-rv.mean()))/den)
 su,sv=u.sum(),v.sum();l1=0.0 if su==sv==0 else 1.0 if (su==0)!=(sv==0) else float(np.sum(np.abs(u/su-v/sv)))
 d={'spearman':sp,'normalized_L1':l1}
 for k in (5,10):
  ai,bi=topk_info(u,k),topk_info(v,k);key='jaccard_'+str(k);skey=key+'_status'
  if ai['status']!='DEFINED' or bi['status']!='DEFINED':d[key]=None;d[skey]='NA_BOUNDARY_TIE'
  else:
   x,y=set(ai['selection']),set(bi['selection']);d[key]=len(x&y)/len(x|y);d[skey]='DEFINED'
 return d

def load_context(root,task,family,seed,row,d24):
 import numpy as np, shap, joblib
 ds=d24['cohorts'][task]['dataset'];c=d24['cohorts'][task];dim=c['encoded_features'];native_dim=2 if task=='TON2' and family=='MLP' else (1 if task=='TON2' else c['output_dim']);nrows=c['xai_rows'];source_count=39 if task=='CIC34' else 31
 pin(root/D15,D15_SHA,'D15');pin(root/R5,R5_SHA,'R5');pin(root/R3,R3_SHA,'R3')
 d15=mod(root/D15,'pf4_primary_d15');r5=mod(root/R5,'pf4_primary_r5');r3=mod(root/R3,'pf4_primary_r3')
 for rel,h in d15.SOURCE_HASHES.items():pin(root/rel,h,'SOURCE::'+rel)
 p2=d15.outs(root/'C3C_P2_artifacts/C3C_P2_manifest.json');p3e=d15.outs(root/'C3C_P3E_artifacts/C3C_P3E_manifest.json')
 def checked(rel,man):return d15.checked_member(root,man,rel)
 rawp=d15.gzrows(checked(f'data/cohorts/C3C_P2/{ds}/property.csv.gz',p2));raw=d15.gzrows(checked(f'data/cohorts/C3C_P2/{ds}/xai.csv.gz',p2))
 iip=np.load(checked(f'data/encoded/C3C_P3E/{ds}/property_test_indices.npy',p3e),allow_pickle=False);ix=np.load(checked(f'data/encoded/C3C_P3E/{ds}/xai_test_indices.npy',p3e),allow_pickle=False)
 xtpath=checked(f'data/encoded/C3C_P3E/{ds}/X_test.npy',p3e);pin(xtpath,c['x_test_sha256'],'D24_XTEST');xx=np.load(xtpath,mmap_mode='r',allow_pickle=False)
 require(sha(root/f'data/encoded/C3C_P3E/{ds}/xai_test_indices.npy')==c['xai_index_sha256'],'D24_XAI_HASH')
 bgpath=pin(root/f'data/xai/C5K_P2/{ds}/background_X.npy',c['background_sha256'],'D24_BACKGROUND');bg=np.load(bgpath,allow_pickle=False)
 require(len(raw)==nrows and ix.shape==(nrows,) and xx.shape==(c['test_rows'],dim) and bg.shape==(256,dim) and len(rawp)==len(iip),'FROZEN_SHAPES')
 require(len(set(map(int,ix)))==len(ix) and np.isfinite(bg).all() and np.isfinite(np.asarray(xx[ix])).all(),'XAI_OR_BG_INVALID')
 key='__selection_rank_hex';lookup={r[key]:int(iip[j]) for j,r in enumerate(rawp)}
 require(len(lookup)==len(rawp) and len(set(r[key] for r in raw))==len(raw) and all(lookup.get(r[key])==int(ix[j]) for j,r in enumerate(raw)),'ALL_XAI_RAW_INDEX_PARITY')
 p3b=mod(root/'scripts/C3C_P3B_transform_all_baseline_cohorts.py','pf4_primary_p3b');encmod=mod(root/'scripts/C5F_raw_to_encoded_model_interface_parity.py','pf4_primary_encoder');project=mod(root/'scripts/C5D_R3_R1_bound_guard_engine_reference.py','pf4_primary_project');rep=mod(root/'scripts/C5F_R2_representation_effective_engine.py','pf4_primary_rep')
 encoder=encmod.FrozenEncoder(root,ds,p3b);require(encoder.encoded_count==dim,'ENCODER_DIM')
 names,groups,mapping=source_groups(root,d15,ds,dim,source_count)
 spec=read(root/'contracts/C5B_R5_executable_property_specification.json')['PF1'];require(spec['cohort']=='property' and tuple(map(float,spec['intensities']))==LEVELS,'FROZEN_PF1')
 stats=d15.rows(root/f'C3C_P3A_artifacts/{ds}/numeric_fit_stats.csv');all_iqr={v['feature']:float(v['iqr']) for v in stats};constraints=d15.rows(root/'contracts/C5B_R5_PF1_feature_constraints.csv');eligible=list(spec['eligibility'][task]);intlike={v['source_feature']:v['integer_like']=='YES' for v in constraints if v['task']==task and v['PF1_eligible']=='YES'}
 require(set(eligible)==set(intlike) and set(eligible).issubset(all_iqr),'PF1_ELIGIBILITY');iqr={n:all_iqr[n] for n in eligible}
 modelpath=pin(root/row['model_path'],row['model_sha256'],'D24_MODEL');require(modelpath.stat().st_size==int(row['model_bytes']),'MODEL_BYTES')
 if family!='MLP':
  model=joblib.load(modelpath);require(type(model).__name__==('SGDClassifier' if family=='LIN_SGD_LOGISTIC' else 'HistGradientBoostingClassifier'),'MODEL_TYPE');require(list(map(int,model.classes_))==list(range(2 if task=='TON2' else native_dim)),'MODEL_CLASSES')
  def score(x):
   y=np.asarray(r3.decision(model,np.asarray(x,dtype=np.float32)),dtype=np.float64);require(y.shape==(len(x),native_dim) and np.isfinite(y).all(),'NATIVE_MARGIN');return y
  def pred(x):return np.asarray(model.predict(np.asarray(x,dtype=np.float32)),dtype=np.int64)
  def p1(x):
   y=np.asarray(model.predict_proba(np.asarray(x,dtype=np.float32)),dtype=np.float64);require(y.shape==(len(x),2) and np.isfinite(y).all() and ((y>=0)&(y<=1)).all(),'P1');return y[:,1]
  mask=shap.maskers.Independent(bg,max_samples=256);ex=shap.LinearExplainer(model,mask) if family=='LIN_SGD_LOGISTIC' else shap.TreeExplainer(model,data=mask,feature_perturbation='interventional');require(r5.masker_rows(ex)==256,'EXPLAINER_BG_ROWS');base=r3.basevec(ex,native_dim);require(base.shape==(native_dim,),'BASE_SHAPE')
 else:
  import torch
  pin(root/C4F,C4F_SHA,'FROZEN_MLP_BUILDER');helper=mod(root/C4F,'pf4_primary_mlp_builder');pkg=torch.load(modelpath,map_location='cpu',weights_only=False);model=helper.build_mlp(pkg);model=model[0] if isinstance(model,(list,tuple)) else model;model.eval();bgt=torch.as_tensor(bg,dtype=torch.float32)
  def logits(x):
   with torch.no_grad():
    y=model(torch.as_tensor(np.asarray(x,dtype=np.float32),dtype=torch.float32));y=y[0] if isinstance(y,(list,tuple)) else y
   require(tuple(y.shape)==(len(x),native_dim) and bool(torch.isfinite(y).all()),'MLP_LOGITS');return y
  def score(x):return np.asarray(logits(x).detach().cpu().numpy(),dtype=np.float64)
  def pred(x):return np.argmax(score(x),axis=1).astype(np.int64)
  def p1(x):return np.asarray(torch.softmax(logits(x),dim=1)[:,1].detach().cpu().numpy(),dtype=np.float64)
  ex=shap.GradientExplainer(model,bgt);base=None
 return locals()

def one_profile(ctx,task,family,seed,j):
 import numpy as np
 row=ctx['raw'][j];idx=int(ctx['ix'][j]);dim=ctx['dim'];encoder=ctx['encoder'];names=ctx['names'];groups=ctx['groups'];model=ctx['model'];score=ctx['score'];pred=ctx['pred'];r5=ctx['r5'];r3=ctx['r3'];ex=ctx['ex']
 clean=np.asarray(encoder.encode_p3e(row),dtype=np.float32);ref=np.asarray(ctx['xx'][idx],dtype=np.float32)
 drift=float(np.max(np.abs(clean.astype(np.float64)-ref.astype(np.float64))));require(clean.shape==(dim,) and np.isfinite(clean).all() and np.isfinite(ref).all() and drift<=3e-6,'ENCODE_PARITY::'+str(j))
 rawsha=hashbytes(np.ascontiguousarray(ref).tobytes());pairs=[];meta=[]
 for lev in LEVELS:
  cand=ctx['rep'].representation_effective_candidate(row,clean,encoder,ctx['project'],task,family,seed,ctx['eligible'],ctx['iqr'],ctx['intlike'],row['__selection_rank_hex'],lev,0)
  require(cand['status'] in ('APPLICABLE','NOT_APPLICABLE'),'PF1_STATUS');m={'ordinal':j,'x_test_index':idx,'intensity':lev,'draw':0,'status':cand['status'],'raw_valid_candidates_seen':int(cand.get('raw_valid_candidates_seen',0)),'encoded_noops_seen':int(cand.get('encoded_noops_seen',0))}
  if cand['status']=='APPLICABLE':
   v=np.asarray(cand['encoded'],dtype=np.float32);require(v.shape==(dim,) and np.isfinite(v).all() and not np.array_equal(v,clean) and float(cand['actual_abs_change'])<=float(cand['nominal_bound'])+1e-12,'PF1_PAIR');m.update(feature=cand['feature'],nominal_bound=float(cand['nominal_bound']),actual_abs_change=float(cand['actual_abs_change']),encoded_max_abs_change=float(cand['encoded_max_abs_change']),opposite_sign_used=bool(cand['opposite_sign_used']));pairs.append(v)
  meta.append(m)
 block=np.stack([clean]+pairs).astype(np.float32)
 if family=='HGB':values=ex.shap_values(block,check_additivity=False)
 elif family=='MLP':
  import torch
  values=ex.shap_values(torch.as_tensor(block,dtype=torch.float32))
 else:values=ex.shap_values(block)
 phi=r5.norm_shap(values,len(block),dim);require(phi.shape==(len(block),dim,ctx['native_dim']) and np.array_equal(phi,r3.norm_shap(values,len(block),dim)) and np.isfinite(phi).all(),'SHAP_NATIVE_DIM')
 native=score(block);pr=pred(block);require(pr.shape==(len(block),),'PRED_SHAPE')
 native_pred=(native[:,0]>0).astype(np.int64) if task=='TON2' and family!='MLP' else np.argmax(native,axis=1)
 require(np.array_equal(pr,native_pred),'NATIVE_PRED_PARITY');coord=int(pr[0]);native_coord=0 if task=='TON2' and family!='MLP' else coord;bound=phi[:,:,native_coord]
 add=[]
 if family!='MLP':
  recon=ctx['base'][native_coord]+np.sum(bound,axis=1,dtype=np.float64);levels=[None]+[m['intensity'] for m in meta if m['status']=='APPLICABLE']
  for i,lev in enumerate(levels):add.append({'ordinal':j,'level':lev,'clean_class_coordinate':coord,'native_explanation_coordinate':native_coord,'native_score':float(native[i,native_coord]),'reconstructed_score':float(recon[i]),'absolute_residual':float(abs(native[i,native_coord]-recon[i]))})
 mags=np.array([np.sum(np.abs(bound[0,g]),dtype=np.float64) for g in groups]);topinfo={k:topk_info(mags,k) for k in (5,10)};top={k:topinfo[k]['selection'] for k in (5,10)};stab=[]
 for m in meta:
  s={'ordinal':j,'x_test_index':idx,'intensity':m['intensity'],'draw':0,'status':m['status'],'perturbed_source_feature':m.get('feature'),'clean_predicted_class':coord}
  if m['status']=='APPLICABLE':
   i=1+sum(t['status']=='APPLICABLE' for t in meta if t['intensity']<m['intensity']);s.update(stability(bound[0],bound[i],groups));s.update(perturbed_predicted_class=int(pr[i]),prediction_stable=bool(pr[i]==coord),perturbed_source_magnitude_shap=[float(np.sum(np.abs(bound[i,g]),dtype=np.float64)) for g in groups],perturbed_source_signed_shap=[float(np.sum(bound[i,g],dtype=np.float64)) for g in groups])
  else:s.update(jaccard_5=None,jaccard_10=None,jaccard_5_status='NOT_APPLICABLE',jaccard_10_status='NOT_APPLICABLE',spearman=None,normalized_L1=None,perturbed_predicted_class=None,prediction_stable=None)
  stab.append(s)
 single=score(clean[None,:])[0];single_pred=int(pred(clean[None,:])[0]);checkpred=int(single[0]>0) if task=='TON2' and family!='MLP' else int(np.argmax(single));require(single_pred==checkpred==coord,'SINGLE_CLASS_DRIFT')
 if task=='TON2':
  cp=float(ctx['p1'](clean[None,:])[0]);clean_hist=float(cp if coord==1 else 1-cp);historical_sem='p1_if_clean_class1_else_1_minus_p1'
 else:clean_hist=float(single[coord]);historical_sem='native_historical_clean_class_score'
 require(np.isfinite(clean_hist),'CLEAN_HIST_FINITE');ab=[]
 for k in (5,10):
  selection=top[k]
  if selection is None:
   ab.append({'ordinal':j,'x_test_index':idx,'k':k,'status':'NA_BOUNDARY_TIE','reason':'CLEAN_TOPK_BOUNDARY_TIE','clean_class_coordinate':coord,'historical_score_semantics':historical_sem,'selected_topk_source_features':None,'effective_source_features':None,'effective_count':None,'encoded_noop':None,'clean_historical_native_score':clean_hist,'ablated_historical_native_score':None,'score_drop':None,'ablated_predicted_class':None,'prediction_changed':None});continue
  alter=dict(row)
  for g in selection:require(names[g] in alter,'ABLATION_SOURCE_MISSING');alter[names[g]]=''
  ax=np.asarray(encoder.encode_p3e(alter),dtype=np.float32);require(ax.shape==(dim,) and np.isfinite(ax).all(),'ABLATION_SHAPE')
  active={v for g in selection for v in groups[g]};outside=[v for v in range(dim) if v not in active];require(np.array_equal(ax[outside],clean[outside]),'ABLATION_OUTSIDE_CHANGED')
  effective=[names[g] for g in selection if not np.array_equal(ax[groups[g]],clean[groups[g]])];noop=bool(np.array_equal(ax,clean));require(noop==(not effective),'ABLATION_NOOP')
  if noop:abl_hist=clean_hist;abl_pred=coord
  else:
   ss=score(ax[None,:])[0];abl_pred=int(pred(ax[None,:])[0]);expected=int(ss[0]>0) if task=='TON2' and family!='MLP' else int(np.argmax(ss));require(expected==abl_pred,'ABLATION_CLASS_NATIVE')
   if task=='TON2':ap=float(ctx['p1'](ax[None,:])[0]);abl_hist=float(ap if coord==1 else 1-ap)
   else:abl_hist=float(ss[coord])
  ab.append({'ordinal':j,'x_test_index':idx,'k':k,'status':'DEFINED','clean_class_coordinate':coord,'historical_score_semantics':historical_sem,'selected_topk_source_features':[names[g] for g in selection],'effective_source_features':effective,'effective_count':len(effective),'encoded_noop':noop,'clean_historical_native_score':clean_hist,'ablated_historical_native_score':abl_hist,'score_drop':float(clean_hist-abl_hist),'ablated_predicted_class':abl_pred,'prediction_changed':abl_pred!=coord})
 profile={'ordinal':j,'x_test_index':idx,'selection_rank_hex':row['__selection_rank_hex'],'encoded_profile_sha256_raw_float32':rawsha,'reencode_vs_Xtest_max_abs':drift,'clean_predicted_class':coord,'clean_single_predicted_class':single_pred,'clean_batch_predicted_class':coord,'native_explanation_coordinate':native_coord,'clean_single_native_scores':[float(x) for x in single],'clean_batch_native_scores':[float(x) for x in native[0]],'single_vs_batch_coord_abs_delta':float(abs(single[native_coord]-native[0,native_coord])),'single_vs_batch_vector_max_abs_delta':float(np.max(np.abs(single-native[0]))),'clean_historical_score':clean_hist,'historical_score_semantics':historical_sem,'source_features':names,'source_signed_shap':[float(np.sum(bound[0,g],dtype=np.float64)) for g in groups],'source_magnitude_shap':[float(x) for x in mags],'top5':None if top[5] is None else [names[g] for g in top[5]],'top10':None if top[10] is None else [names[g] for g in top[10]],'top5_status':topinfo[5]['status'],'top10_status':topinfo[10]['status'],'top5_boundary_tied_source_features':[names[g] for g in topinfo[5]['boundary_tied_indices']],'top10_boundary_tied_source_features':[names[g] for g in topinfo[10]['boundary_tied_indices']]}
 return {'gate':'R7-D35-PF4-PRIMARY-P1','status':'PRIMARY_CASE_ORDINAL_COMMITTED','task':task,'family':family,'seed':seed,'ordinal':j,'x_test_index':idx,'clean_class':coord,'n_applicable':len(pairs),'n_NA':3-len(pairs),'PF1_metadata':meta,'profile':profile,'stability':stab,'ablation':ab,'additivity':add if family!='MLP' else 'N/A_FROZEN_NO_SUBSTITUTION','primary_PF4_authorized_by_user':True,'PF5_executed':False,'native_semantics':('two_raw_logits_fixed_clean_class' if family=='MLP' else 'native_binary_scalar_margin_coordinate_zero' if task=='TON2' else 'native_multiclass_decision_function_fixed_clean_class'),'source_count':len(names),'encoded_count':dim,'original_full_xai_ordinal_not_deduplicated':True,'protocol_amendment':{'id':A1_ID,'policy':A1_POLICY,'base_source_manifest_sha256':BASE_SOURCE_MANIFEST_SHA}}

def verify_checkpoint(p,task,family,seed,ordinal):
 require(p.is_dir(),'CHECKPOINT_NOT_DIR');require({v.name for v in p.iterdir()}=={'scientific.json','COMMITTED.json'},'CHECKPOINT_FILESET');sc=p/'scientific.json';com=read(p/'COMMITTED.json')
 require(com['gate']=='R7-D35-PF4-PRIMARY-P1' and (com['task'],com['family'],com['seed'],com['ordinal'])==(task,family,seed,ordinal) and com['status']=='SEALED_PRIMARY_ORDINAL','CHECKPOINT_SEAL_SCOPE');require(com['files']=={'scientific.json':{'sha256':sha(sc),'bytes':sc.stat().st_size}},'CHECKPOINT_BYTES')
 data=read(sc);require(data['primary_PF4_authorized_by_user'] is True and data['PF5_executed'] is False and (data['task'],data['family'],data['seed'],data['ordinal'])==(task,family,seed,ordinal) and len(data['stability'])==3 and len(data['ablation'])==2 and data['n_applicable']+data['n_NA']==3,'CHECKPOINT_SCIENTIFIC_SCOPE')
 require(data['additivity']=='N/A_FROZEN_NO_SUBSTITUTION' if family=='MLP' else len(data['additivity'])==1+data['n_applicable'],'CHECKPOINT_ADDITIVITY')
 require(data.get('original_full_xai_ordinal_not_deduplicated') is True,'CHECKPOINT_CANONICAL_SCOPE')
 prof=data['profile'];require(prof['ordinal']==ordinal and data['x_test_index']==prof['x_test_index'] and data['clean_class']==prof['clean_predicted_class']==prof['clean_single_predicted_class']==prof['clean_batch_predicted_class'],'CHECKPOINT_PROFILE_BINDING')
 u=prof['source_magnitude_shap'];require(len(u)==data['source_count'] and len(prof['source_signed_shap'])==len(u) and len(prof['source_features'])==len(u),'SOURCE_FEATURE_COUNTS')
 import numpy as np
 info={k:topk_info(np.asarray(u),k) for k in (5,10)};amended='protocol_amendment' in data or 'top5_status' in prof or 'top10_status' in prof
 if amended:
  require(data.get('protocol_amendment')=={'id':A1_ID,'policy':A1_POLICY,'base_source_manifest_sha256':BASE_SOURCE_MANIFEST_SHA},'A1_CHECKPOINT_AMENDMENT')
  for k in (5,10):
   status=info[k]['status'];require(prof.get('top'+str(k)+'_status')==status,'A1_PROFILE_TOPK_STATUS::'+str(k));expected=None if status!='DEFINED' else [prof['source_features'][g] for g in info[k]['selection']];require(prof.get('top'+str(k))==expected,'A1_PROFILE_TOPK_SELECTION::'+str(k));ties=[prof['source_features'][g] for g in info[k]['boundary_tied_indices']];require(prof.get('top'+str(k)+'_boundary_tied_source_features')==ties,'A1_PROFILE_TOPK_TIES::'+str(k))
 else:
  for k in (5,10):require(info[k]['status']=='DEFINED','LEGACY_CHECKPOINT_HAS_BOUNDARY_TIE::'+str(k));require(prof['top'+str(k)]==[prof['source_features'][g] for g in info[k]['selection']],'LEGACY_TOPK_RECONCILIATION::'+str(k))
 for a in data['ablation']:
  require(a['ordinal']==ordinal and a['k'] in (5,10),'CHECKPOINT_ABLATION_SCOPE');status=a.get('status','DEFINED')
  if status=='DEFINED':require(info[a['k']]['status']=='DEFINED','ABLATION_DEFINED_WITH_TIED_TOPK');require(math.isclose(a['score_drop'],a['clean_historical_native_score']-a['ablated_historical_native_score'],abs_tol=1e-14,rel_tol=0),'CHECKPOINT_SIGNED_ABLATION')
  else:
   require(status=='NA_BOUNDARY_TIE' and info[a['k']]['status']=='NA_BOUNDARY_TIE' and a.get('reason')=='CLEAN_TOPK_BOUNDARY_TIE','A1_ABLATION_NA_SCOPE')
   for key in ('selected_topk_source_features','effective_source_features','effective_count','encoded_noop','ablated_historical_native_score','score_drop','ablated_predicted_class','prediction_changed'):require(a.get(key) is None,'A1_ABLATION_NA_FIELD::'+key)
 for st in data['stability']:
  require(st['ordinal']==ordinal and st['draw']==0,'CHECKPOINT_STABILITY_SCOPE')
  if st['status']=='APPLICABLE':
   v=st['perturbed_source_magnitude_shap'];require(len(v)==len(u) and len(st['perturbed_source_signed_shap'])==len(u),'PERTURBED_MAGNITUDE_LENGTH');calc=stability(np.asarray(u),np.asarray(v),[[i] for i in range(len(u))])
   for key in ('spearman','normalized_L1','jaccard_5','jaccard_10'):
    val=calc[key]
    if val is None:require(st[key] is None,'NULL_RECONCILIATION::'+key)
    else:require(math.isclose(st[key],val,rel_tol=0,abs_tol=1e-12),'METRIC_RECONCILIATION::'+key)
   for k in (5,10):
    sk='jaccard_'+str(k)+'_status';expected=calc[sk]
    if sk in st:require(st[sk]==expected,'A1_JACCARD_STATUS::'+str(k))
    else:require(expected=='DEFINED','LEGACY_JACCARD_BOUNDARY_TIE::'+str(k))
   require(st['prediction_stable']==(st['perturbed_predicted_class']==data['clean_class']),'PRED_STABILITY_RECONCILIATION')
  else:
   require(st['status']=='NOT_APPLICABLE' and st['jaccard_5'] is None and st['jaccard_10'] is None and st['prediction_stable'] is None,'NA_RECONCILIATION')
   for k in (5,10):
    sk='jaccard_'+str(k)+'_status'
    if sk in st:require(st[sk]=='NOT_APPLICABLE','A1_NA_STATUS::'+str(k))
 return data

def commit(p,obj):
 require(not p.exists(),'PROFILE_EXISTS');tmp=p.with_name(p.name+'.staging');require(not tmp.exists(),'PARTIAL_STAGING_PRESERVE');tmp.mkdir(parents=True,exist_ok=False)
 sci=tmp/'scientific.json';write_new(sci,obj);write_new(tmp/'COMMITTED.json',{'gate':'R7-D35-PF4-PRIMARY-P1','status':'SEALED_PRIMARY_ORDINAL','task':obj['task'],'family':obj['family'],'seed':obj['seed'],'ordinal':obj['ordinal'],'files':{'scientific.json':{'sha256':sha(sci),'bytes':sci.stat().st_size}}});verify_checkpoint(tmp,obj['task'],obj['family'],obj['seed'],obj['ordinal']);os.replace(tmp,p)

def execute(root,store,task,family,seed,max_new):
 rows,d24,d32=manifest();matches=[r for r in rows if (r['task'],r['family'],int(r['seed']))==(task,family,seed)];require(len(matches)==1,'CASE_D24');row=matches[0];total=int(row['xai_rows'])
 require(max_new>=1 and max_new<=total,'MAX_NEW_RANGE');case=store/task/family/('seed_'+str(seed));require(store.is_dir(),'STORE_PARENT_NOT_FOUND');case.mkdir(parents=True,exist_ok=True)
 ctxfile=case/'CASE_CONTEXT.json';spec={'gate':'R7-D35-PF4-PRIMARY-P1','authorization':'USER_EXPLICIT_2026-10-02','task':task,'family':family,'seed':seed,'canonical_xai_rows':total,'d24_model_path':row['model_path'],'d24_model_sha256':row['model_sha256'],'d24_manifest_sha256':D24_SHA,'d32_historical_contract_sha256':D32_SHA,'PF5_executed':False,'primary_PF4_authorized_by_user':True,'source_package_sha256':BASE_SOURCE_MANIFEST_SHA}
 if ctxfile.exists():require(read(ctxfile)==spec,'CASE_CONTEXT_DRIFT')
 else:
  require({p.name for p in case.iterdir()}==set(),'UNRECOGNIZED_CASE_DIR');write_new(ctxfile,spec)
 for p in case.iterdir():require(p.name=='CASE_CONTEXT.json' or p.name=='checkpoints','CASE_EXTRA_FILE::'+p.name)
 checkpoints=case/'checkpoints';checkpoints.mkdir(exist_ok=True)
 existing={}
 for p in checkpoints.iterdir():
  require(p.is_dir() and p.name.startswith('ordinal_') and p.name[8:].isdigit() and len(p.name)==14,'CHECKPOINT_UNRECOGNIZED::'+p.name)
  n=int(p.name[8:]);require(n not in existing and 0<=n<total,'CHECKPOINT_ORDINAL');existing[n]=verify_checkpoint(p,task,family,seed,n)
 require(all(i==int(v['ordinal']) for i,v in existing.items()),'CHECKPOINT_ORDINAL_MISMATCH')
 missing=[j for j in range(total) if j not in existing];print('PF4_PRIMARY_CASE='+task+'/'+family+'/seed_'+str(seed)+'::SEALED_EXISTING='+str(len(existing))+'::REMAINING='+str(len(missing))+'::MAX_NEW='+str(max_new),flush=True)
 if not missing:print('PF4_PRIMARY_CASE=COMPLETE_ALREADY_SEALED',flush=True);return
 ctx=load_context(root,task,family,seed,row,d24);require(len(ctx['raw'])==total,'CANONICAL_COHORT_LENGTH')
 new=[]
 for j in missing[:max_new]:
  result=one_profile(ctx,task,family,seed,j);dest=checkpoints/('ordinal_'+str(j).zfill(6));commit(dest,result);new.append(j)
  print('PF4_PRIMARY_COMMITTED::'+task+'::'+family+'::seed='+str(seed)+'::ordinal='+str(j)+'::applicable='+str(result['n_applicable'])+'::NA='+str(result['n_NA']),flush=True)
 sealed=[verify_checkpoint(p,task,family,seed,int(p.name[8:])) for p in checkpoints.iterdir()]
 require(len(sealed)==len(existing)+len(new),'POST_COMMIT_COUNT');print('PF4_PRIMARY_TRANCHE=PASS::NEW='+str(len(new))+'::TOTAL_SEALED='+str(len(sealed))+'::TARGET='+str(total)+'::CASE_COMPLETE='+str(len(sealed)==total),flush=True)

def selftest():
 import numpy as np
 rows,d24,d32=manifest();require(len(rows)==45 and {int(r['seed']) for r in rows}==set(SEEDS),'MATRIX_TEST');g=[[j] for j in range(31)];a=np.arange(1,32,dtype=float);s=stability(a,a,g);require(s['jaccard_5']==s['jaccard_10']==s['spearman']==1 and s['normalized_L1']==0 and s['jaccard_5_status']==s['jaccard_10_status']=='DEFINED','IDENTITY_METRICS')
 require(np.array_equal(rankavg([2.,2.,4.,1.]),np.array([2.5,2.5,4.,1.])),'TIED_RANKS');require(topk(np.zeros(31),5) is None and topk_info(np.zeros(31),5)['status']=='NA_BOUNDARY_TIE','A1_TIE_NA_POLICY');ts=stability(np.zeros(31),np.zeros(31),g);require(ts['jaccard_5'] is None and ts['jaccard_10'] is None and ts['jaccard_5_status']==ts['jaccard_10_status']=='NA_BOUNDARY_TIE','A1_TIE_STABILITY_NA')
 require(d24['cohorts']['TON2']['xai_rows']==1000 and d24['cohorts']['CIC34']['xai_rows']==3400 and d24['cohorts']['TON10']['xai_rows']==1000,'CANONICAL_COUNTS');require(d32['PF4']['primary_fidelity'].endswith('no threshold; GradientExplainer N/A_FROZEN_NO_SUBSTITUTION'),'NO_FIDELITY_THRESHOLD')
 print('PF4_PRIMARY_SELFTEST=PASS::45_D24_CASES::ORIGINAL_FULL_XAI::PF4_A1_BOUNDARY_TIE_NA::NATIVE_OUTPUT::SIGNED_ABLATION::ATOMIC_ORDINAL_CHECKPOINT::PF5_NO',flush=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--self-test',action='store_true');ap.add_argument('--root',type=Path);ap.add_argument('--store',type=Path);ap.add_argument('--task',choices=TASKS);ap.add_argument('--family',choices=FAMS);ap.add_argument('--seed',type=int,choices=SEEDS);ap.add_argument('--max-new',type=int,default=8);a=ap.parse_args()
 if a.self_test:selftest();return
 require(all(v is not None for v in (a.root,a.store,a.task,a.family,a.seed)),'REQUIRED_ARGUMENTS');execute(a.root.resolve(),a.store.resolve(),a.task,a.family,a.seed,a.max_new)
if __name__=='__main__':
 try:main()
 except BaseException as e:print('PF4_PRIMARY_STATUS=FAIL_CLOSED::'+type(e).__name__+'::'+str(e),file=sys.stderr,flush=True);traceback.print_exc();sys.exit(1)
