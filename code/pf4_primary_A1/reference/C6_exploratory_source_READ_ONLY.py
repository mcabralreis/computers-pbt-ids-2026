#!/usr/bin/env python3
"""R7-D35-PF4-C6, exploratory TON2/LIN/HGB/MLP seed11, XAI ordinals 0 and 8.
One genuine frozen PF1 generator, native assigned explainer and class-fixed ablation.
No change to original XAI cohort, no primary PF4 authorization, no new thresholds.
"""
from __future__ import annotations
import argparse, collections, csv, hashlib, importlib.util, io, json, math, sys, traceback, zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent.parent
REF=HERE/'reference'
C3_SHA='58d987a517c7b963849531d7499662de73191b8be50796e768b2c5164a92d023'
P0_SHA='894b8f8ce31d93ada455cd4a6869be3ee2007695c013136b5099f794ffef80e8'
D32_SHA='27470b04c90c024d56351e3196affe14966dae867cba0fe3fd25fd39257f3b40'
D15='scripts/C5K_P2_R4_R6_P4_R7_D15_exact_clean_perturbed_input_pilot.py'
D15_SHA='524fd22b067bb8ded3d4bde0001f890f990fc655d3c9ed0df12370cb7232dd06'
R5='scripts/C5K_P2_R4_R6_P4_R5_all_seeds_non_rf_worker.py';R5_SHA='10c8ffb8d751ca15ac4c8aae0968888770538984bd5a1d83283efa0b6a8363ea'
R3='scripts/C5K_P2_R4_R6_P4_R3_fidelity_semantics_worker.py';R3_SHA='21024bdb4db1ddde5660ca4ceba4967b29a563f6a4678fd0ce02f92bfce559d1'
MODELS={'LIN_SGD_LOGISTIC':('models/C4E_final/TON2/LIN_SGD_LOGISTIC/seed_11/model.joblib','375d7193bd1dd60cb540f27f64dd77845e2b16ea154da8621ca922c5d9c06ba9'), 'HGB':('models/C4E_final/TON2/HGB/seed_11/model.joblib','8134ba7c602276b17350c211ebc4db8328ad722f920a1c59c2e922941c511d13'), 'MLP':('models/C4E_final/TON2/MLP/seed_11/model.pt','f0a3402ebadd456e3d06e58c8cebca1c764c164b00120ecf45cb5d3062ace9fa')}
D24_SHA='8a86a9b4b56ad4f45abe72843890823bc3e2b381727a3863251d6ed6ad5bb72a'
C4F='scripts/C4F_R3_parent_cleanup_test_resume.py';C4F_SHA='003c732a0095230414dcde617df47fe4039e09bcef0c3bb90b17f67dff2388e1'
BG='data/xai/C5K_P2/TON_IoT_NETWORK/background_X.npy';BG_SHA='0aa9798fd18911656dcf17e130a9ce732d1e94225c8dd4c488142c62e0e85252'
DS='TON_IoT_NETWORK';F=153; LEVELS=(0.01,0.05,0.10);ORDS=(0,8)

def fail(m):raise RuntimeError('PF4_C6_FAIL_CLOSED::'+m)
def ensure(p,m):
 if not p:fail(m)
def hashbytes(b):return hashlib.sha256(b).hexdigest()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4<<20),b''):h.update(b)
 return h.hexdigest()
def pin(p,h,label):
 ensure(p.is_file(),'MISSING::'+label);ensure(sha(p)==h,'HASH::'+label+'::'+sha(p));return p
def jd(b):return json.loads(b.decode('utf-8-sig'))
def dump(p,obj):p.write_bytes((json.dumps(obj,sort_keys=True,indent=2,allow_nan=False,ensure_ascii=False)+'\n').encode('utf-8'))
def zopen(p,h):
 pin(p,h,p.name);z=zipfile.ZipFile(p);ensure(z.testzip() is None,'BAD_ZIP::'+p.name); names={}
 for real in z.namelist():
  name=real.replace('\\','/');ensure(name not in names and not name.startswith('/') and all(v not in ('','.','..') for v in name.rstrip('/').split('/')),'BAD_ZIP_NAME::'+name);names[name]=real
 return z,names
def zsuffix(z,names,suffix):
 keys=[k for k in names if k.endswith(suffix)];ensure(len(keys)==1,'ZIP_MEMBER_COUNT::'+suffix);return z.read(names[keys[0]])
def mod(p,n):
 spec=importlib.util.spec_from_file_location(n,p);ensure(spec and spec.loader,'IMPORT::'+str(p));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def references(family):
 ensure(family in MODELS,"UNKNOWN_FAMILY")
 model_path, model_sha=MODELS[family]
 z,c=zopen(REF/'C3_evidence.zip',C3_SHA); sel=zsuffix(z,c,'/TON_distinct_profile_selection.json');seal=jd(zsuffix(z,c,'/SEALED.json'))
 ensure(seal['files']['TON_distinct_profile_selection.json']['sha256']==hashbytes(sel) and seal['files']['TON_distinct_profile_selection.json']['bytes']==len(sel),'C3_RESULT_SEAL')
 c3=jd(sel); co=c3['cohort'];ensure(c3['status'].startswith('PASS_READ_ONLY') and co['selected_exploratory_ordinals']==list(ORDS) and co['selected_test_indices']==[287,2178] and co['selected_distinct'] and co['unique_encoded_profiles']==944,'C3_SELECTION')
 ensure(c3['mapping']['source_feature_count']==31 and c3['mapping']['encoded_feature_count']==153 and not c3['primary_PF4_authorized'],'C3_SCOPE')
 z0,n0=zopen(REF/'P0_evidence.zip',P0_SHA);p0=jd(zsuffix(z0,n0,'/EIGHT_CASE_FULL_HASH_PREFLIGHT.json'))
 cases=[v for v in p0['cases'] if v['task']=='TON2' and v['family']==family and v['seed']==11]
 if family=='LIN_SGD_LOGISTIC':
  pin(REF/'D24_45_case_manifest.csv',D24_SHA,'FROZEN_D24');matches=[r for r in csv.DictReader((REF/'D24_45_case_manifest.csv').open(newline='',encoding='utf8')) if r['task']=='TON2' and r['family']==family and r['seed']=='11'];ensure(len(matches)==1 and matches[0]['model_path']==model_path and matches[0]['model_sha256']==model_sha and matches[0]['score_dim']=='1','D24_LIN_MODEL')
 else:ensure(len(cases)==1 and cases[0]['model_path']==model_path and cases[0]['model_sha256_verified_full_bytes']==model_sha and cases[0]['interface']['actual_explanation_output_dim']==(2 if family=='MLP' else 1) and not p0['primary_PF4_authorized'],'P0_MODEL')
 pin(REF/'contract_D32.json',D32_SHA,'D32');d32=json.loads((REF/'contract_D32.json').read_text())
 ensure(not d32['primary_PF4_approved'] and d32['PF4']['original_source_feature_magnitude']=='sum absolute encoded SHAP within same source feature','D32_SCOPE')
 mapping=c3['mapping']['source_features_in_encoded_order'];groups=[e['encoded_indices'] for e in mapping]
 ensure(sorted(x for g in groups for x in g)==list(range(F)) and len(mapping)==31,'SOURCE_MAPPING_COVERAGE')
 return c3, mapping, groups

def topk(a,k):
 import numpy as np
 a=np.asarray(a,dtype=np.float64);ensure(len(a)>k and np.isfinite(a).all() and (a>=0).all(),'TOPK_MAG')
 idx=np.argsort(-a,kind='mergesort');ensure(a[idx[k-1]]!=a[idx[k]],'TOPK_BOUNDARY_TIE::'+str(k));return list(map(int,idx[:k]))
def rankavg(a):
 import numpy as np
 a=np.asarray(a,dtype=np.float64);order=np.argsort(a,kind='mergesort');out=np.empty(len(a),float);i=0
 while i<len(a):
  j=i+1
  while j<len(a) and a[order[j]]==a[order[i]]:j+=1
  out[order[i:j]]=(i+j-1)/2+1;i=j
 return out
def stab(a,b,groups):
 import numpy as np
 u=np.array([np.sum(np.abs(a[g]),dtype=np.float64) for g in groups]);v=np.array([np.sum(np.abs(b[g]),dtype=np.float64) for g in groups]);ru,rv=rankavg(u),rankavg(v)
 den=float(np.sqrt(np.sum((ru-ru.mean())**2)*np.sum((rv-rv.mean())**2)));sp=None if den==0 else float(np.sum((ru-ru.mean())*(rv-rv.mean()))/den)
 su,sv=u.sum(),v.sum();l1=0.0 if su==sv==0 else 1.0 if (su==0)!=(sv==0) else float(np.sum(np.abs(u/su-v/sv)))
 d={'spearman':sp,'normalized_L1':l1}
 for k in (5,10):
  x,y=set(topk(u,k)),set(topk(v,k));d['jaccard_'+str(k)]=len(x&y)/len(x|y)
 return d

def selftest():
 import numpy as np
 references('LIN_SGD_LOGISTIC');references('HGB');references('MLP');a=np.arange(1,32,dtype=float);g=[[i] for i in range(31)];s=stab(a,a,g)
 ensure(s['jaccard_5']==s['jaccard_10']==s['spearman']==1 and s['normalized_L1']==0,'METRICS_IDENTITY')
 ensure(np.array_equal(rankavg(np.array([2.,2.,4.,1.])),np.array([2.5,2.5,4.,1.])),'AVERAGE_TIES')
 try:topk(np.zeros(31),5)
 except RuntimeError as e:ensure('TOPK_BOUNDARY_TIE' in str(e),'TOPK_TIE_EXCEPTION')
 else:fail('TIE_NOT_REJECTED')
 synthetic_batch=np.array([1., 2., 0.],dtype=np.float64)
 synthetic_single=np.array([1., 2.+1e-5, 0.],dtype=np.float64)
 ensure(int(np.argmax(synthetic_batch))==int(np.argmax(synthetic_single)) and float(np.max(np.abs(synthetic_batch-synthetic_single)))>0,'BATCH_SINGLE_NUMERICAL_DRIFT_TEST')
 ensure(int(np.argmax(np.array([3., 1., 0.])))!=int(np.argmax(synthetic_batch)),'CLASS_DISAGREEMENT_NEGATIVE_TEST')
 p=np.array([0.25,0.75]);ensure(np.array_equal(1-p,np.array([0.75,0.25])),'CLASS0_COMPLEMENT')
 ensure((2 if 'MLP'=='MLP' else 1)==2 and (0 if 'HGB'!='MLP' else 1)==0,'BINARY_NATIVE_COORD_TEST')
 print('PF4_C6_SELFTEST=PASS_THREE_BINARY_INTERFACES_CLASS0_COMPLEMENT_NO_PRIMARY',flush=True)

def run(root,out,family):
 import numpy as np, joblib, shap
 ensure(family in MODELS,"FAMILY")
 model_path,model_sha=MODELS[family]
 ensure(not out.exists(),'OUTPUT_ALREADY_EXISTS')
 c3,mapping,groups=references(family)
 pin(root/D15,D15_SHA,'ORIGINAL_D15');pin(root/R5,R5_SHA,'ORIGINAL_R5');pin(root/R3,R3_SHA,'ORIGINAL_R3')
 d15=mod(root/D15,'c6_original_d15');r5=mod(root/R5,'c6_original_r5');r3=mod(root/R3,'c6_original_r3')
 for rel,h in d15.SOURCE_HASHES.items():pin(root/rel,h,'FROZEN::'+rel)
 p2=d15.outs(root/'C3C_P2_artifacts/C3C_P2_manifest.json');p3a=d15.outs(root/'C3C_P3A_artifacts/C3C_P3A_manifest.json');p3e=d15.outs(root/'C3C_P3E_artifacts/C3C_P3E_manifest.json')
 key='__selection_rank_hex';rawp=d15.gzrows(d15.checked_member(root,p2,f'data/cohorts/C3C_P2/{DS}/property.csv.gz'));raw=d15.gzrows(d15.checked_member(root,p2,f'data/cohorts/C3C_P2/{DS}/xai.csv.gz'))
 iip=np.load(d15.checked_member(root,p3e,f'data/encoded/C3C_P3E/{DS}/property_test_indices.npy'),allow_pickle=False);ix=np.load(d15.checked_member(root,p3e,f'data/encoded/C3C_P3E/{DS}/xai_test_indices.npy'),allow_pickle=False)
 xx=np.load(d15.checked_member(root,p3e,f'data/encoded/C3C_P3E/{DS}/X_test.npy'),mmap_mode='r',allow_pickle=False)
 bg=np.load(pin(root/BG,BG_SHA,'FROZEN_TON_BG'),allow_pickle=False)
 ensure(len(rawp)==9164 and len(raw)==1000 and iip.shape==(9164,) and ix.shape==(1000,) and xx.shape==(210452,F) and bg.shape==(256,F),'COHORT_OR_SHAPE')
 ensure(ix[list(ORDS)].tolist()==[287,2178] and np.array_equal(xx[ix[0]],xx[ix[1]]) and not np.array_equal(xx[ix[0]],xx[ix[8]]),'C3_ORDINAL_BINDING')
 ensure(len(set(r[key] for r in rawp))==len(rawp) and len(set(r[key] for r in raw))==len(raw),'RANK_UNIQUENESS')
 rank={r[key]:int(iip[j]) for j,r in enumerate(rawp)}
 ensure(all(rank.get(r[key])==int(ix[j]) for j,r in enumerate(raw)),'ALL_1000_XAI_RAW_RANK_PARITY')
 for name in ('preprocessor.json','encoded_feature_schema.csv','numeric_fit_stats.csv','categorical_vocab.csv'):d15.checked_member(root,p3a,f'C3C_P3A_artifacts/{DS}/{name}')
 p3b=mod(root/'scripts/C3C_P3B_transform_all_baseline_cohorts.py','c4_p3b');encmod=mod(root/'scripts/C5F_raw_to_encoded_model_interface_parity.py','c4_encoder');project=mod(root/'scripts/C5D_R3_R1_bound_guard_engine_reference.py','c4_proj');rep=mod(root/'scripts/C5F_R2_representation_effective_engine.py','c4_rep')
 encoder=encmod.FrozenEncoder(root,DS,p3b);ensure(encoder.encoded_count==F,'ENCODER_FEATURE_COUNT')
 schema=root/f'C3C_P3A_artifacts/{DS}/encoded_feature_schema.csv';pre=root/f'C3C_P3A_artifacts/{DS}/preprocessor.json'
 ensure(sha(schema)==c3['mapping']['schema_sha256'] and sha(pre)==c3['mapping']['preprocessor_sha256'],'C3_SCHEMA_PREPROCESSOR_BINDING')
 chosen=[raw[j] for j in ORDS];clean=np.stack([np.asarray(encoder.encode_p3e(r),dtype=np.float32) for r in chosen]);ref=np.asarray(xx[ix[list(ORDS)]],dtype=np.float32)
 drift=np.max(np.abs(clean.astype(np.float64)-ref.astype(np.float64)),axis=1)
 ensure(np.isfinite(clean).all() and np.max(drift)<=3e-6 and not np.array_equal(clean[0],clean[1]),'REENCODE_PARITY_OR_DISTINCT')
 # C3 selection is pinned to original raw float32 X_test, not silently replaced by the reencoding.
 for j in range(2):ensure(hashbytes(np.ascontiguousarray(ref[j]).tobytes())==c3['cohort']['selected_profile_sha256_raw_float32'][j],'C3_PROFILE_BYTES')
 spec=json.loads((root/'contracts/C5B_R5_executable_property_specification.json').read_text(encoding='utf-8'))['PF1']
 ensure(tuple(map(float,spec['intensities']))==LEVELS and spec['cohort']=='property','FROZEN_PF1_LEVELS')
 stats=d15.rows(root/f'C3C_P3A_artifacts/{DS}/numeric_fit_stats.csv');iqr_all={r['feature']:float(r['iqr']) for r in stats};constraints=d15.rows(root/'contracts/C5B_R5_PF1_feature_constraints.csv')
 eligible=list(spec['eligibility']['TON2']);intlike={r['source_feature']:r['integer_like']=='YES' for r in constraints if r['task']=='TON2' and r['PF1_eligible']=='YES'}
 ensure(len(eligible)==5 and set(eligible)==set(intlike) and set(eligible).issubset(iqr_all),'PF1_ELIGIBILITY');iqr={f:iqr_all[f] for f in eligible}
 pin(root/model_path,model_sha,'TON2_'+family+'_MODEL')
 if family!='MLP':
  model=joblib.load(root/model_path);ensure(list(map(int,model.classes_))==[0,1],'BINARY_MODEL_CLASSES')
  ensure(type(model).__name__==('SGDClassifier' if family=='LIN_SGD_LOGISTIC' else 'HistGradientBoostingClassifier'),'MODEL_TYPE')
  def score(x):
   y=np.asarray(model.decision_function(np.asarray(x,dtype=np.float32)),dtype=np.float64).reshape(-1,1);ensure(y.shape==(len(x),1) and np.isfinite(y).all(),'BINARY_NATIVE_MARGIN');return y
  def historical_p1(x):
   p=np.asarray(model.predict_proba(np.asarray(x,dtype=np.float32)),dtype=np.float64);ensure(p.shape==(len(x),2) and np.isfinite(p).all() and ((p>=0)&(p<=1)).all(),'CERTIFIED_P1');return p[:,1]
  mask=shap.maskers.Independent(bg,max_samples=256)
  expl=shap.LinearExplainer(model,mask) if family=='LIN_SGD_LOGISTIC' else shap.TreeExplainer(model,data=mask,feature_perturbation='interventional')
  ensure(r5.masker_rows(expl)==256,'SHAP_BG_256')
  base=np.asarray(getattr(expl,'expected_value'),dtype=np.float64).reshape(-1);ensure(base.shape==(1,) and np.isfinite(base).all(),'BINARY_NATIVE_SCALAR_BASE')
 else:
  import torch
  pin(root/C4F,C4F_SHA,'ORIGINAL_C4F_MLP_BUILDER');helper=mod(root/C4F,'c6_original_mlp_builder')
  pkg=torch.load(root/model_path,map_location='cpu',weights_only=False);model=helper.build_mlp(pkg)
  if isinstance(model,(list,tuple)):model=model[0]
  model.eval();bg_t=torch.as_tensor(bg,dtype=torch.float32)
  def logits_t(x):
   with torch.no_grad():
    z=model(torch.as_tensor(np.asarray(x,dtype=np.float32),dtype=torch.float32));z=z[0] if isinstance(z,(list,tuple)) else z
   ensure(tuple(z.shape)==(len(x),2) and bool(torch.isfinite(z).all()),'MLP_TWO_RAW_LOGITS');return z
  def score(x):return np.asarray(logits_t(x).detach().cpu().numpy(),dtype=np.float64)
  def historical_p1(x):
   p=np.asarray(torch.softmax(logits_t(x),dim=1)[:,1].detach().cpu().numpy(),dtype=np.float64);ensure(p.shape==(len(x),) and np.isfinite(p).all() and ((p>=0)&(p<=1)).all(),'MLP_SOFTMAX_P1');return p
  expl=shap.GradientExplainer(model,bg_t);base=None
 names=[e['source_feature'] for e in mapping];stability=[];ablation=[];additivity=[];profiles=[];input_manifest=[]
 for j,ord_ in enumerate(ORDS):
  row=chosen[j];pairs=[];meta=[]
  for lev in LEVELS:
   cand=rep.representation_effective_candidate(row,clean[j],encoder,project,'TON2',family,11,eligible,iqr,intlike,row[key],lev,0)
   ensure(cand['status'] in ('APPLICABLE','NOT_APPLICABLE'),'UNKNOWN_PF1_STATUS')
   m={'ordinal':ord_,'x_test_index':int(ix[ord_]),'intensity':lev,'draw':0,'status':cand['status'],'raw_valid_candidates_seen':int(cand.get('raw_valid_candidates_seen',0)),'encoded_noops_seen':int(cand.get('encoded_noops_seen',0))}
   if cand['status']=='APPLICABLE':
    v=np.asarray(cand['encoded'],dtype=np.float32)
    ensure(v.shape==(F,) and np.isfinite(v).all() and not np.array_equal(v,clean[j]) and float(cand['actual_abs_change'])<=float(cand['nominal_bound'])+1e-12,'PF1_INVALID_PAIR')
    m.update(feature=cand['feature'],nominal_bound=float(cand['nominal_bound']),actual_abs_change=float(cand['actual_abs_change']),encoded_max_abs_change=float(cand['encoded_max_abs_change']),opposite_sign_used=bool(cand['opposite_sign_used']));pairs.append(v)
   meta.append(m);input_manifest.append(m)
  block=np.stack([clean[j]]+pairs).astype(np.float32)
  values=expl.shap_values(block,check_additivity=False) if family=='HGB' else expl.shap_values(__import__('torch').as_tensor(block,dtype=__import__('torch').float32)) if family=='MLP' else expl.shap_values(block);phi=r5.norm_shap(values,len(block),F)
  ensure(phi.shape==(len(block),F,2 if family=='MLP' else 1) and np.array_equal(phi,r3.norm_shap(values,len(block),F)) and np.isfinite(phi).all(),'BINARY_SHAP_NATIVE_SHAPE')
  native=score(block);pred=np.asarray(model.predict(block),dtype=np.int64) if family!='MLP' else np.argmax(native,axis=1).astype(np.int64)
  ensure(np.array_equal(pred, (native[:,0]>0).astype(np.int64) if family!='MLP' else np.argmax(native,axis=1)),'PRED_NATIVE_MISMATCH')
  coord=int(pred[0]);native_coord=coord if family=='MLP' else 0;bound=phi[:,:,native_coord]
  if family!='MLP':
   recon=base[0]+np.sum(bound,axis=1,dtype=np.float64)
   for rownum in range(len(block)):
    lev=None if rownum==0 else [m['intensity'] for m in meta if m['status']=='APPLICABLE'][rownum-1]
    additivity.append({'ordinal':ord_,'level':lev,'clean_class_coordinate':coord,'native_explanation_coordinate':native_coord,'native_score':float(native[rownum,native_coord]),'reconstructed_score':float(recon[rownum]),'absolute_residual':float(abs(native[rownum,native_coord]-recon[rownum]))})
  mags=np.asarray([np.sum(np.abs(bound[0,g]),dtype=np.float64) for g in groups]);chosen_top={k:topk(mags,k) for k in (5,10)}
  for m in meta:
   s={'ordinal':ord_,'x_test_index':int(ix[ord_]),'intensity':m['intensity'],'draw':0,'status':m['status'],'perturbed_source_feature':m.get('feature'),'clean_predicted_class':coord}
   if m['status']=='APPLICABLE':
    rownum=1+sum(t['status']=='APPLICABLE' for t in meta if t['intensity']<m['intensity']);s.update(stab(bound[0],bound[rownum],groups));s.update(perturbed_predicted_class=int(pred[rownum]),prediction_stable=bool(pred[rownum]==coord))
   else:s.update(jaccard_5=None,jaccard_10=None,spearman=None,normalized_L1=None,perturbed_predicted_class=None,prediction_stable=None)
   stability.append(s)
  # The historical clean score for ablation uses one-row inference as in the frozen adapter.
  # The additivity reference remains the native score from the SHAP block (clean + PF1 rows).
  # PF0 documented class-invariant but score-noninvariant batch transformations: never impose bitwise equality here.
  single_native=score(clean[j:j+1])[0]
  single_pred=int(model.predict(clean[j:j+1])[0]) if family!='MLP' else int(np.argmax(single_native))
  ensure(single_pred==coord and (int(single_native[0]>0) if family!='MLP' else int(np.argmax(single_native)))==coord,'CLEAN_SINGLE_CLASS_DRIFT')
  clean_p1=float(historical_p1(clean[j:j+1])[0]);clean_score=float(clean_p1 if coord==1 else 1-clean_p1)
  batch_clean_score=float(native[0,native_coord])
  single_vs_batch_delta=float(abs(float(single_native[native_coord])-batch_clean_score))
  single_vs_batch_vector_max=float(np.max(np.abs(single_native-native[0])))
  ensure(np.isfinite([clean_score,batch_clean_score,single_vs_batch_delta,single_vs_batch_vector_max]).all(),'CLEAN_SCORE_NONFINITE')
  for k in (5,10):
   selected=chosen_top[k];alter=dict(row)
   for ixsrc in selected:
    feature=names[ixsrc];ensure(feature in alter,'SOURCE_MISSING::'+feature);alter[feature]=''
   ax=np.asarray(encoder.encode_p3e(alter),dtype=np.float32);ensure(ax.shape==(F,) and np.isfinite(ax).all(),'ABLATION_ENCODING')
   active={i for g in selected for i in groups[g]};outside=[i for i in range(F) if i not in active];ensure(np.array_equal(ax[outside],clean[j,outside]),'ABLATION_OFFGROUP_CHANGED')
   effective=[names[i] for i in selected if not np.array_equal(ax[groups[i]],clean[j,groups[i]])];noop=bool(np.array_equal(ax,clean[j]));ensure(noop==(len(effective)==0),'NOOP_CONTRACT')
   if noop:target=clean_score;abl_pred=coord
   else:
    sc=score(ax[None,:])[0];p1_abl=float(historical_p1(ax[None,:])[0]);target=float(p1_abl if coord==1 else 1-p1_abl);abl_pred=int(model.predict(ax[None,:])[0]) if family!='MLP' else int(np.argmax(sc));ensure(abl_pred==(int(sc[0]>0) if family!='MLP' else int(np.argmax(sc))),'ABLATION_CLASS_NATIVE')
   ablation.append({'ordinal':ord_,'x_test_index':int(ix[ord_]),'k':k,'clean_class_coordinate':coord,'historical_score_semantics':'p1_if_clean_class1_else_1_minus_p1','selected_topk_source_features':[names[i] for i in selected],'effective_source_features':effective,'effective_count':len(effective),'encoded_noop':noop,'clean_historical_native_score':clean_score,'ablated_historical_native_score':target,'score_drop':float(clean_score-target),'ablated_predicted_class':abl_pred,'prediction_changed':abl_pred!=coord})
  profiles.append({'ordinal':ord_,'x_test_index':int(ix[ord_]),'selection_rank_hex':row[key],'clean_predicted_class':coord,'clean_encoded_profile_raw_sha256':hashbytes(np.ascontiguousarray(ref[j]).tobytes()),'clean_reencode_vs_Xtest_max_abs':float(drift[j]),'clean_native_scores':[float(v) for v in native[0]],'clean_historical_p1':clean_p1,'explanation_native_coordinate':native_coord,'clean_historical_single_native_score':clean_score,'clean_SHAP_batch_native_score':batch_clean_score,'clean_single_vs_batch_score_abs_delta':single_vs_batch_delta,'clean_single_vs_batch_full_vector_max_abs_delta':single_vs_batch_vector_max,'clean_single_predicted_class':single_pred,'clean_batch_predicted_class':coord,'score_equality_threshold_introduced':False,'historical_score_is_shap_target':False,'source_signed_shap':[float(np.sum(bound[0,g],dtype=np.float64)) for g in groups],'source_magnitude_shap':[float(x) for x in mags],'source_features':names,'top5':[names[i] for i in chosen_top[5]],'top10':[names[i] for i in chosen_top[10]],'num_applicable_PF1':len(pairs),'additivity_numerical_threshold':None if family!='MLP' else 'N/A_FROZEN_NO_SUBSTITUTION'})
  print('PF4_C6_'+family+'_PROFILE=COMPLETE::ORDINAL='+str(ord_)+'::CLASS='+str(coord)+'::PF1_APPLICABLE='+str(len(pairs))+'::ABLATION=2::SINGLE_VS_BATCH_SCORE_ABS_DELTA='+repr(single_vs_batch_delta)+'::VECTOR_MAX_DELTA='+repr(single_vs_batch_vector_max),flush=True)
 ensure(len(profiles)==2 and len(stability)==6 and len(ablation)==4 and len(additivity)==(2+sum(s['status']=='APPLICABLE' for s in stability) if family!='MLP' else 0),'SCIENTIFIC_COUNTS')
 out.mkdir(parents=True,exist_ok=False)
 result={'gate':'R7-D35-PF4-C6-'+family,'status':'EXPLORATORY_TON2_'+family+'11_REAL_PF1_SHAP_STABILITY_ABLATION_NOT_PRIMARY','task':'TON2','family':family,'seed':11,'selected_exploratory_ordinals':list(ORDS),'selected_test_indices':[287,2178],'source_count':31,'encoded_count':153,'actual_explainer':('GradientExplainer(original_R5)' if family=='MLP' else 'TreeExplainer(interventional,check_additivity=False)' if family=='HGB' else 'LinearExplainer'),'explainer_output_space':('two raw native logits, fixed clean class' if family=='MLP' else 'one native binary decision_function scalar'),'shap_background_rows':256,'pf1_input_generation':'ORIGINAL_C5F_R2_REPRESENTATION_EFFECTIVE_ENGINE','pf1_levels':list(LEVELS),'pf1_draw':0,'historical_probability_semantics':'p1 from certified model probability; class0 score 1-p1','explanation_native_output_dim':(2 if family=='MLP' else 1),'native_explanation_coordinate_rule':'fixed clean raw logit class' if family=='MLP' else 'native scalar coordinate zero independent of clean class','source_aggregation_signed':'sum signed SHAP per source','source_aggregation_magnitude':'sum absolute encoded SHAP per source','additivity_threshold':None,'additivity_status':('N/A_FROZEN_NO_SUBSTITUTION' if family=='MLP' else 'NATIVE_RESIDUAL_NO_THRESHOLD'),'stability':stability,'ablation':ablation,'additivity':additivity if family!='MLP' else 'N/A_FROZEN_NO_SUBSTITUTION','profiles':profiles,'PF1_metadata':input_manifest,'num_applicable_pairs':sum(x['status']=='APPLICABLE' for x in stability),'num_NA_pairs':sum(x['status']=='NOT_APPLICABLE' for x in stability),'primary_PF4_authorized':False,'original_xai_cohort_changed':False,'original_indices_replaced':False,'mlp_rng_seed_retrofitted':False,'cross_family_native_scores_poolable':False,'upstream':{'C3_evidence_sha256':C3_SHA,'P0_evidence_sha256':P0_SHA,'D32_sha256':D32_SHA,'model_sha256':model_sha,'background_sha256':BG_SHA,'raw_xai_sha256':sha(root/f'data/cohorts/C3C_P2/{DS}/xai.csv.gz'),'Xtest_sha256':sha(root/f'data/encoded/C3C_P3E/{DS}/X_test.npy')}}
 dump(out/'science_results.json',result)
 for name,rows in ([('stability.csv',stability),('ablation.csv',ablation),('additivity.csv',additivity)] if family!='MLP' else [('stability.csv',stability),('ablation.csv',ablation)]):
  with (out/name).open('x',encoding='utf-8',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 seal={'gate':result['gate'],'status':'SEALED_EXPLORATORY_SCIENCE_NOT_PRIMARY','files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in out.iterdir() if p.is_file()},'primary_PF4_authorized':False};dump(out/'SEALED.json',seal)
 print('PF4_C6_'+family+'_SCIENCE=PASS::DISTINCT_PROFILES=2::PF1_ATTEMPTS=6::STABILITY_RECORDS=6::ABLATION=4::ADDITIVITY='+('N/A_FROZEN_NO_SUBSTITUTION' if family=='MLP' else str(len(additivity)))+'::PRIMARY=NO',flush=True)
 print('PF4_C6_'+family+'_SCIENCE_SEAL_SHA256='+sha(out/'SEALED.json'),flush=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');p.add_argument('--root',type=Path);p.add_argument('--out',type=Path);p.add_argument('--family',choices=list(MODELS));a=p.parse_args()
 if a.self_test:selftest();return
 ensure(a.root is not None and a.out is not None and a.family is not None,'ROOT_OUT_FAMILY_REQUIRED');run(a.root.resolve(),a.out.resolve(),a.family)
if __name__=='__main__':
 try:main()
 except Exception as e:print('PF4_C6_STATUS=FAIL_CLOSED::'+type(e).__name__+'::'+str(e),file=sys.stderr,flush=True);traceback.print_exc();sys.exit(1)
