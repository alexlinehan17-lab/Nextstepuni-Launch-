import copy,json,unittest
import construction_2015_higher_q1_q2 as m
class SourceGuard(unittest.TestCase):
 def test_source_and_images(self):
  self.assertEqual(m.validate(json.loads(m.REVIEW.read_text()))['tasks'],7)
 def test_rejects_lost_drawing_marks_context_or_topic(self):
  original=json.loads(m.REVIEW.read_text())
  def card(d,key):return next(t['card']for t in d['tasks']if t['card']['id']=='cons-2015-hl-'+key)
  cases={
   'omitted accessibility':lambda d:d['tasks'].pop(1),
   'increased drawing cap':lambda d:card(d,'q1-a')['rows'][0].update(marks=48),
   'invented presentation band':lambda d:card(d,'q1-a')['rows'][1].update(permittedMarks=list(range(9))),
   'lost required dimensions':lambda d:card(d,'q1-a').update(stem='Draw a door'),
   'lost material and dimension marks':lambda d:card(d,'q2-b').update(totalMarks=18),
   'lost sketch requirement':lambda d:card(d,'q2-a')['rows'][0].update(contextNote='Name three functions'),
   'missing constituent topic':lambda d:d['bindings'][0]['atlasTopicIds'].pop(),
   'wrong curriculum':lambda d:d['bindings'][0].update(canonicalTopicIds=['cons-5-8']),
   'uncertain source':lambda d:d['sourceHashes'].update({m.P:'changed'}),
   'unreviewed source crop':lambda d:d['questionFigures'][0].update(visuallyInspected=False),
   'cut off drawing':lambda d:d['questionFigures'][1].update(rect=[60,104,558,500]),
   'lost route row':lambda d:card(d,'q1-complete')['rows'].pop(),
   'unclassified choice':lambda d:d['selectionLedger'].update(unclassified=1),
  }
  for label,change in cases.items():
   with self.subTest(label=label):
    d=copy.deepcopy(original);change(d)
    with self.assertRaises(AssertionError):m.validate(d,images=False)
if __name__=='__main__':unittest.main()
