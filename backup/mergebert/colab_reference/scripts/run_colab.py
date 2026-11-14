import pathlib,subprocess,sys,time,os,json,shutil
from common import BASE, REFERENCE
SCRIPTS=REFERENCE/'scripts'
os.environ['PYTHONUTF8']='1'
flags=getattr(subprocess,'CREATE_NO_WINDOW',0)
def run(root,script,extra=None):
 args=[sys.executable,'-u',str(SCRIPTS/script),root.name.replace('colab_reproduction_','')]+(extra or [])
 suffix='_smoke' if extra and '--smoke' in extra else ''
 with (root/'logs'/(pathlib.Path(script).stem+suffix+'.log')).open('a',encoding='utf-8') as log:
  p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',creationflags=flags)
  (root/'reports'/(pathlib.Path(script).stem+suffix+'.process.json')).write_text(json.dumps({'pid':p.pid,'args':args}),encoding='utf-8')
  print('START',root.name,script,extra,flush=True)
  for line in p.stdout:log.write(line);log.flush();print(root.name,line.rstrip(),flush=True)
  result=p.wait()
  if result:raise RuntimeError(f'{script} failed: {result}')
def main():
 for split in ['sort_by_prerepo','sort_by_realtime']:
  root=BASE/('colab_reproduction_'+split);print('WAITING_DATA',split,flush=True)
  if not (root/'reports/preparation_stats.json').exists():raise FileNotFoundError('Run import_data.py for both splits, then prepare_all.py first')
  for f in SCRIPTS.glob('*.py'):shutil.copy2(f,root/'scripts'/f.name)
  if not (root/'checkpoints/mergebert.pt').exists():
   run(root,'verify_features.py')
   run(root,'train_all.py',['--smoke'])
   run(root,'train_all.py')
  if not (root/'reports/metrics_by_repository.json').exists():run(root,'evaluate_all.py')
  run(root,'verify_final.py')
  print('EXPERIMENT_COMPLETE',split,flush=True)
 print('ALL_COLAB_RUNS_COMPLETE',flush=True)
if __name__=='__main__':main()