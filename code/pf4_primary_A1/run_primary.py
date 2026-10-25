#!/usr/bin/env python3
"""Primary PF4 transaction launcher; one verified case or all 45; archival always."""
from __future__ import annotations
import argparse,csv,hashlib,json,re,subprocess,sys,traceback,zipfile
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
WORKER=HERE/'scripts/primary_case.py'

def require(a,b):
 if not a:raise RuntimeError('PF4_LAUNCH_FAIL_CLOSED::'+str(b))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4<<20),b''):h.update(b)
 return h.hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf8')
def source():
 m=json.loads((HERE/'PACKAGE_MANIFEST.json').read_text(encoding='utf8'));fil=m['files'];actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='PACKAGE_MANIFEST.json'}
 require(actual==set(fil),'PACKAGE_FILESET::missing='+str(sorted(set(fil)-actual))+'::extra='+str(sorted(actual-set(fil))))
 for rel,v in fil.items():
  p=HERE/rel;require(p.stat().st_size==v['bytes'] and sha(p)==v['sha256'],'PACKAGE_SHA::'+rel)
 digest=hashlib.sha256(json.dumps(fil,sort_keys=True,separators=(',',':')).encode()).hexdigest();require(digest==m['source_manifest_sha256'],'SOURCE_MANIFEST_SHA')
 require(m['primary_PF4_authorized_by_user'] is True and m['PF5_authorized'] is False and len(m['case_ids'])==45,'AUTHORIZATION_SCOPE')
 print('PF4_PRIMARY_PACKAGE=PASS::FILES='+str(len(fil))+'::MATRIX=45::AUTHORIZED_PF4_YES::PF5_NO',flush=True)
def progress(s):
 vals=[x.strip() for x in re.split('[\r\n]+',s) if x.strip()]
 return all(re.fullmatch(r'\d+%\|[^\r\n]*\|\s*\d+/\d+\s*\[[^\r\n]*\]',v) for v in vals)
def cases():
 with (HERE/'reference/D24_45_case_manifest.csv').open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f))
 return [(x['task'],x['family'],int(x['seed'])) for x in r]
def brief_status(store):
 from scripts.primary_case import verify_checkpoint,manifest
 manifest();total=0;count=0
 for task,family,seed in cases():
  target=3400 if task=='CIC34' else 1000;folder=store/task/family/('seed_'+str(seed))/'checkpoints';n=0
  if folder.is_dir():
   for p in folder.iterdir():
    require(p.name.startswith('ordinal_') and len(p.name)==14 and p.name[8:].isdigit(),'UNKNOWN_CHECKPOINT::'+p.name)
    verify_checkpoint(p,task,family,seed,int(p.name[8:]));n+=1
  print('PF4_STATUS::'+task+'::'+family+'::seed='+str(seed)+'::'+str(n)+'/'+str(target),flush=True);total+=target;count+=n
 print('PF4_PRIMARY_STATUS=SEALED_'+str(count)+'_OF_'+str(total)+'_CANONICAL_CASE_ORDINALS',flush=True)
 return count,total

def archive(run,store,archivepath,scope):
 require(not archivepath.exists(),'ARCHIVE_EXISTS');withcase=scope if scope!='all' else None
 with zipfile.ZipFile(archivepath,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for p in sorted(run.rglob('*')):
   if p.is_file():z.write(p,'transaction/'+p.relative_to(run).as_posix())
  paths=[store] if withcase is None else [store/withcase]
  for top in paths:
   if not top.exists():continue
   for p in sorted(top.rglob('*')):
    if p.is_file():z.write(p,'primary_store/'+p.relative_to(store).as_posix())
  for p in sorted(HERE.rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:z.write(p,'frozen_source/'+p.relative_to(HERE).as_posix())
 with zipfile.ZipFile(archivepath) as z:require(z.testzip() is None,'ZIP_CRC')
 print('PF4_PRIMARY_EVIDENCE='+str(archivepath),flush=True);print('PF4_PRIMARY_EVIDENCE_SHA256='+sha(archivepath),flush=True)

def launch(root,store,run,archivepath,selection,maxnew):
 source();require(root.is_dir() and store.is_dir(),'ROOT_STORE');require(not run.exists() and not archivepath.exists(),'TRANSACTION_REUSE');run.mkdir(parents=True,exist_ok=False)
 relevant=cases() if selection=='all' else [tuple(selection.split('/'))]
 if selection!='all':relevant=[(relevant[0][0],relevant[0][1],int(relevant[0][2]))]
 require(all(x in cases() for x in relevant),'CASE_SELECTION')
 dump(run/'REQUEST.json',{'gate':'R7-D35-PF4-PRIMARY-P1','selection':selection,'max_new_per_case':maxnew,'requested_cases':relevant,'root':str(root),'store':str(store),'PF5_authorized':False,'primary_PF4_authorized_by_user':True})
 status='FAILED';done=[]
 try:
  for t,f,s in relevant:
   key=t+'__'+f+'__'+str(s);stdout=run/(key+'.stdout.txt');stderr=run/(key+'.stderr.txt');exitf=run/(key+'.exit.txt')
   with stdout.open('wb') as so,stderr.open('wb') as se:p=subprocess.run([sys.executable,'-u',str(WORKER),'--root',str(root),'--store',str(store),'--task',t,'--family',f,'--seed',str(s),'--max-new',str(maxnew)],stdout=so,stderr=se,check=False)
   exitf.write_text(str(p.returncode)+'\n',encoding='utf8');o=stdout.read_text(encoding='utf8',errors='replace');e=stderr.read_text(encoding='utf8',errors='replace')
   for line in o.splitlines():print(line,flush=True)
   require(p.returncode==0,'SCIENCE_EXIT::'+key+'::'+str(p.returncode)+'::'+e[-2500:])
   require(not e or (f=='HGB' and progress(e)),'SCIENCE_STDERR::'+key+'::'+e[-2500:])
   require('PF4_PRIMARY_TRANCHE=PASS::' in o or 'PF4_PRIMARY_CASE=COMPLETE_ALREADY_SEALED' in o,'SCIENCE_MARKER::'+key)
   done.append(key);print('PF4_PRIMARY_VERIFIED_CASE_TRANCHE='+key,flush=True)
  status='PASS';print('PF4_PRIMARY_TRANSACTION=PASS::CASES='+str(len(done))+'::PF5_NO',flush=True)
 except BaseException as e:
  print('PF4_PRIMARY_TRANSACTION=FAIL_CLOSED::'+type(e).__name__+'::'+str(e),file=sys.stderr,flush=True);dump(run/'LAST_FAILURE.json',{'error_type':type(e).__name__,'error':str(e),'completed_case_tranches':done,'no_automatic_reexecution':True});raise
 finally:
  dump(run/'FINAL_STATUS.json',{'status':status,'verified_case_tranches':done,'expected_case_tranches':len(relevant),'primary_PF4_authorized_by_user':True,'PF5_authorized':False});archive(run,store,archivepath,selection)

def selftest():
 source()
 q=subprocess.run([sys.executable,'-u',str(WORKER),'--self-test'],capture_output=True,text=True)
 require(q.returncode==0 and not q.stderr and 'PF4_PRIMARY_SELFTEST=PASS::45_D24_CASES' in q.stdout,'WORKER_SELFTEST::'+repr(q.stderr));print(q.stdout.strip(),flush=True)
 require(progress(' 98%|===================| 39/40 [00:13<00:00]') and progress('') and not progress('UserWarning: duplicate') and not progress('Traceback (most recent call last):'),'STDERR_CLASSIFIER')
 require(len(cases())==45 and len(set(cases()))==45,'STATIC_MATRIX')
 print('PF4_PRIMARY_LAUNCHER_SELFTEST=PASS::NO_MODELS_LOADED::NO_SHAP::NO_PRIMARY_EXECUTED',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');p.add_argument('--status',action='store_true');p.add_argument('--root',type=Path);p.add_argument('--store',type=Path);p.add_argument('--transaction-dir',type=Path);p.add_argument('--evidence',type=Path);p.add_argument('--task');p.add_argument('--family');p.add_argument('--seed',type=int);p.add_argument('--all',action='store_true');p.add_argument('--max-new-per-case',type=int,default=8);a=p.parse_args()
 try:
  if a.self_test:selftest()
  elif a.status:
   require(a.store is not None,'STATUS_STORE_REQUIRED');source();brief_status(a.store.resolve())
  else:
   require(all(x is not None for x in (a.root,a.store,a.transaction_dir,a.evidence)),'ARGS_REQUIRED');require(a.max_new_per_case>=1,'MAX_NEW_POSITIVE');require(a.all != bool(a.task or a.family or a.seed),'SELECTION_MODE')
   if a.all:sel='all'
   else:
    require((a.task,a.family,a.seed) in cases(),'CASE_NOT_D24');sel=a.task+'/'+a.family+'/'+str(a.seed)
   launch(a.root.resolve(),a.store.resolve(),a.transaction_dir.resolve(),a.evidence.resolve(),sel,a.max_new_per_case)
 except BaseException as e:print('PF4_PRIMARY_LAUNCHER_EXIT=1::'+str(e),file=sys.stderr,flush=True);sys.exit(1)
