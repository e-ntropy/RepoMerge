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
   d=PACKAGE/'reports'/split;m=json.loads((d/'metrics_by_repository.json').read_text());h=json.loads((d/'training_history.json').read_text());s=json.loads((d/'preparation_stats.json').read_text())
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
if __name__=='__main__':unittest.main()
