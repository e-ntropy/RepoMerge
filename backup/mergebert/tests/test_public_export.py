import unittest,pathlib,json,random,sys,ast
PACKAGE=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE/'colab_reference/scripts'))
from common import normalize,original_compute,fast_compute,PATTERNS

def signature(items):return [(x.seq1Range.start,x.seq1Range.end,x.seq2Range.start,x.seq2Range.end) for x in items]
class PublicExportTests(unittest.TestCase):
 def test_alignment_matches_reference(self):
  rng=random.Random(42);cases=[([],[]),(['a'],[]),([],['b']),(['a','b','a'],['b','a','b'])]
  for _ in range(250):cases.append(([rng.choice('abcdef') for _ in range(rng.randrange(90))],[rng.choice('abcdef') for _ in range(rng.randrange(90))]))
  for a,b in cases:self.assertEqual(signature(original_compute(a,b)),signature(fast_compute(a,b)))
 def test_exact_match_normalization(self):
  self.assertEqual(normalize('<s> int x = 1;\n'),normalize('int x=1;'))
  self.assertNotEqual(normalize('int x=1;'),normalize('int x=2;'))
  self.assertEqual(len(PATTERNS),9)
 def test_recorded_totals(self):
  for split,train,total,matches in [('sort_by_prerepo',6674,1663,1011),('sort_by_realtime',6669,1668,559)]:
   d=PACKAGE/'archive/local_runs'/split;m=json.loads((d/'metrics_by_repository.json').read_text());h=json.loads((d/'training_history.json').read_text());s=json.loads((d/'preparation_stats.json').read_text())
   self.assertEqual(s['80']['total'],train);self.assertEqual(s['20']['total'],total)
   self.assertEqual(len(h),10);self.assertTrue(all(x['samples_seen']==train for x in h))
   self.assertEqual(sum(x['total'] for k,x in m.items() if k!='OVERALL'),total)
   self.assertEqual(sum(x['matches'] for k,x in m.items() if k!='OVERALL'),matches)
   self.assertEqual(m['OVERALL']['matches'],matches);self.assertEqual(m['OVERALL']['total'],total)
 def test_notebook_is_clean_and_source_consistent(self):
  nb=json.loads((PACKAGE/'colab_reference/mergebert.ipynb').read_text(encoding='utf-8'))
  for i,c in enumerate(nb['cells']):
   self.assertEqual(c['metadata'],{})
   if c['cell_type']=='code':
    self.assertEqual(c['outputs'],[]);self.assertIsNone(c['execution_count'])
    expected=(PACKAGE/'colab_reference'/('cell_'+str(i)+'.py')).read_text(encoding='utf-8')
    self.assertEqual(ast.dump(ast.parse(''.join(c['source']))),ast.dump(ast.parse(expected)))
 def test_current_cloud_tables_and_denominators(self):
  m=json.loads((PACKAGE/'reports/cloud_confirmed_1663_20261114/metrics_by_repository.json').read_text())
  rows=m['repositories'];self.assertEqual(len(rows),11)
  for key,value in [('matches',549),('evaluated',1591),('missing',72),('total',1663)]:
   self.assertEqual(sum(r[key] for r in rows),value);self.assertEqual(m['overall'][key],value)
  self.assertAlmostEqual(m['overall']['em_pct'],549/1663*100)
  self.assertAlmostEqual(m['overall']['macro_em_pct'],sum(r['matches']/r['total']*100 for r in rows)/11)
  self.assertEqual(round(m['overall']['macro_em_pct'],2),33.43)
  for r in rows:
   self.assertEqual(r['evaluated']+r['missing'],r['total'])
   self.assertEqual(round(r['matches']/r['total']*100,2),r['em_pct'])
   line='| {} | {} | {} | {} | {} | {:.2f} |'.format(r['repository'],r['matches'],r['evaluated'],r['missing'],r['total'],r['em_pct'])
   for doc in ['RESULTS.md','REVIEW_RESPONSE_ZH.md']:
    self.assertIn(line,(PACKAGE/doc).read_text(encoding='utf-8'))
  self.assertEqual(m['missing_prediction_policy'],'count_as_failure')
  for doc in ['README.md','RESULTS.md','REVIEW_RESPONSE_ZH.md']:
   text=(PACKAGE/doc).read_text(encoding='utf-8');self.assertIn('33.01',text);self.assertIn('33.43',text)
   self.assertNotIn('60.79',text);self.assertNotIn('33.51',text)
if __name__=='__main__':unittest.main()
