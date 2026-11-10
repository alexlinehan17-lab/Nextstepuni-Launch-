"""Independent visual task census. Never derives a denominator from cards.

2026HL: all16 written pages,8 aural pages and30 scheme pages inspected.
Printed task count46;320marks across all practice alternatives; selecting one
of each10-mark language-awareness pair gives the cover's220+80=300marks.
GWpp13–14 has six prompts under one40-mark grid. Its numbered genres are not
separate questions; the legacy reader stops before the sixth prompt onp14.
"""
import hashlib
from pathlib import Path


def reviewed_keys(year, level):
    if (year, level) == (2011, 'hl'):
        # Independent visual review of all16 paper,8 aural and24 scheme pages.
        # Four summary asks retain four leaves under one collective45 task.
        root=Path(__file__).resolve().parents[3]/'examiner-reports/russian'
        for relative,digest in {
            'papers/2011-hl-000-paper.pdf':'282f90bd9437359bb15917f4254fbd1e2c79b07912d7211abc7272c0be0429d9',
            'papers/2011-hl-A00-paper.pdf':'d914563a421a1aeb5dcadcd0a70e5d0e0c4c2c538075452df12be1445645ee1d',
            'schemes/2011-hl.pdf':'0e0ba4dc7e9bffee7675b899d8380ed4102c50d5c0c84ffb7decf39362e5979e',
        }.items():assert hashlib.sha256((root/relative).read_bytes()).hexdigest()==digest
        keys=[('C1',q,None,r) for q in (1,2,3,4) for r in ('i','ii')]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]
        keys += [(u,None,None,None) for u in ('LA1','CA1','LA2')]
        keys += [(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys)==19
        keys += [('L1',q,None,r) for q,r in [(1,None),(2,None),(3,None),(4,'i'),(4,'ii')]]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(3,'iii')]]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None)]]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None),(4,'i'),(4,'ii')]]
        assert len(keys)==len(set(keys))==39
        return set(keys)
    if (year, level) == (2012, 'hl'):
        # Independent 52-page visual census:20 written +20 listening.
        # C1Q2(ii) remains in the denominator despite its unresolved 2x2=6.
        root=Path(__file__).resolve().parents[3]/'examiner-reports/russian'
        for relative,digest in {
            'papers/2012-hl-000-paper.pdf':'b7757711e6c73bd6f4d7648501364cb252d771bce02177a4c52893137c6ff04a',
            'papers/2012-hl-A00-paper.pdf':'6391789ba2e09bca4df17e74473f2355d32c0fa11516b9e824bebb82aad8efad',
            'schemes/2012-hl.pdf':'eb369d55edcd65c40ace69eac2206c44ba545ddd0118658364537e5f9ac2e4fe',
        }.items():assert hashlib.sha256((root/relative).read_bytes()).hexdigest()==digest
        keys=[('C1',q,None,r) for q,rs in [(1,('i','ii')),(2,('i','ii','iii')),(3,('i','ii')),(4,(None,))] for r in rs]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]+[(u,None,None,None) for u in ('LA1','CA1')]
        keys += [('LA2',q,None,None) for q in (1,2)]+[(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys)==20
        keys += [('L1',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(4,None)]]
        keys += [('L2',q,None,None) for q in (1,2,3,4)]
        keys += [('L3',q,None,r) for q in (1,2,3) for r in ('i','ii')]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None),(4,None)]]
        assert len(keys)==len(set(keys))==40
        return set(keys)
    if (year, level) == (2013, 'hl'):
        # Independent 44-page visual census. The conflicting CA1 allocation
        # remains in this denominator even while its runtime task is held.
        root=Path(__file__).resolve().parents[3]/'examiner-reports/russian'
        for relative,digest in {
            'papers/2013-hl-000-paper.pdf':'36835056dd0dbc40697f132b2a00484df1118ece3f364a8263992dc1a3c4dbc0',
            'papers/2013-hl-A00-paper.pdf':'849f2d530c3a5d5cfc2667bff1f4b38be719483beab856f06d826b51b1640f02',
            'schemes/2013-hl.pdf':'b14c59425b38ee71743c5b59b119baad4071759692f069d143abc421b5ac4b6d',
        }.items():assert hashlib.sha256((root/relative).read_bytes()).hexdigest()==digest
        keys=[('C1',q,None,r) for q,rs in [(1,('i','ii','iii')),(2,('i','ii')),(3,('i','ii','iii')),(4,('i','ii'))] for r in rs]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]+[(u,None,None,None) for u in ('LA1','CA1','LA2')]
        keys += [(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys)==21
        keys += [('L1',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(4,'i'),(4,'ii')]]
        keys += [('L2',q,None,None) for q in (1,2,3)]+[('L3',q,None,None) for q in (1,2,3,4)]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None),(4,'i'),(4,'ii')]]
        assert len(keys)==len(set(keys))==40
        return set(keys)
    if (year, level) == (2014, 'hl'):
        # Independent 44-page visual census:20 written and20 listening.
        # CA1 is separate from LA1; each complete writing choice pool is one task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2014-hl-000-paper.pdf':'2260a53d30344848d06148108aac814aa7b99616d68dddec815ce79604877b91',
            'papers/2014-hl-A00-paper.pdf':'3cf21d1f34576eda4ce0b6bc126152ea7f8b289c105cd5e7e711774bf10f1f66',
            'schemes/2014-hl.pdf':'fb5cfc36f2f64fc1a8fc068bbad392ff99eb2ff5792c37267dfcabc0d0ad1f48',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys=[('C1',q,None,r) for q,rs in [(1,('i','ii')),(2,('i','ii','iii')),(3,('i','ii')),(4,(None,))] for r in rs]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]
        keys += [(u,None,None,None) for u in ('LA1','CA1')]+[('LA2',None,None,r) for r in ('i','ii')]
        keys += [(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys)==20
        keys += [('L1',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(4,None)]]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L3',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(3,None),(4,None)]]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        assert len(keys)==len(set(keys))==40
        return set(keys)
    if (year, level) == (2016, 'ol'):
        # Independent 44-page visual census: 34 written and 39 listening.
        # Handwriting IR1(i) is LA1; language awareness contributes4 inside IR2.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2016-ol-000-paper.pdf':'c664fa1ab4abdf8fc3eaec74dbde93201a196141aba9deb2b04744d3d048c7f8',
            'papers/2016-ol-A00-paper.pdf':'b40b68b3174a9a4191343d4b01a7dc257730fc3df790c5f48a00b65e6dfe7ee4',
            'schemes/2016-ol.pdf':'4242b1be879b2ff9973f75aabf3135478afe1e59b098d2c694ff581d1ce84616',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys=[('IR1',None,None,r) for r in ('ii','iii','iv','v','vi','vii','viii','ix')]
        keys += [('IR2',None,None,r) for r in ('i','ii','iii','iv','v','vi','vii')]
        keys += [('CD',q,None,r) for q in (1,2,3,4) for r in (('i','ii','iii','iv') if q==4 else ('i','ii','iii'))]
        keys += [(u,None,None,None) for u in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys)==34
        keys += [('L1',q,None,r) for q in (1,2,3,4) for r in (('i','ii') if q==4 else ('i','ii','iii'))]
        keys += [('L2',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii'),(3,'iii'),(3,'iv')]]
        keys += [('L3',q,None,r) for q,rs in [(1,('i','ii','iii','iv')),(2,('i','ii','iii')),(3,('i','ii'))] for r in rs]
        keys += [('L4',q,None,r) for q,rs in [(1,('i','ii','iii','iv')),(2,('i','ii','iii')),(3,('i','ii')),(4,('i','ii','iii'))] for r in rs]
        assert len(keys)==len(set(keys))==73
        return set(keys)
    if (year, level) == (2015, 'hl'):
        # Original 44-page visual census: 44 printed asks. The two L3 Q3
        # leaves share one published eight-mark task, hence 43 cards.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2015-hl-000-paper.pdf': '119308b8b944f4a21dab09cf461ebb94c84cb4289458b38925634cc74ed45e66',
            'papers/2015-hl-A00-paper.pdf': 'ffc5916d6a67988ce34ebc982b8d10c62e420e01593ae9c953008e0035439dbd',
            'schemes/2015-hl.pdf': '210b81b664cfac3107aed4c750d839c70c82777d40b92c805f7f5db60d1c730c',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1',q,None,r) for q in (1,2,3,4) for r in (('i','ii','iii','iv') if q==4 else ('i','ii','iii'))]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]
        keys += [('LA1',None,None,None)] + [('LA2',None,None,r) for r in ('i','ii')]
        keys += [(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys)==24
        keys += [('L1',q,None,None) for q in (1,2,3,4,5)]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(4,None)]]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii'),(4,None)]]
        assert len(keys)==len(set(keys))==44
        return set(keys)
    if (year, level) == (2016, 'hl'):
        # Independent 44-page census: 20 written and 20 listening tasks.
        # The two printed language-awareness tasks Q2.2/Q2.3 stay distinct.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2016-hl-000-paper.pdf': '37d0b278496335fe827bea49c8f89ccc1c77baa706815493557379e4466012d4',
            'papers/2016-hl-A00-paper.pdf': '34402a6c1c8c769f9383e5c93d1c71b5b3e2fac9703ca8045ccb4c89491a623b',
            'schemes/2016-hl.pdf': 'ec7771b35c2c806b9e0f2cc8a35626cd3a8e85a9c991afc8089f4319decc19e4',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1',q,None,r) for q,r in [(1,'i'),(1,'ii'),(1,'iii'),(2,'i'),(2,'ii'),(3,'i'),(3,'ii'),(4,'i'),(4,'ii')]]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]
        keys += [('LA1',None,None,None)] + [('LA2',None,None,r) for r in ('i','ii')]
        keys += [(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys) == 20
        keys += [('L1',q,None,r) for q,r in [(1,None),(2,None),(3,None),(4,'i'),(4,'ii')]]
        keys += [('L2',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None)]]
        keys += [('L3',q,None,r) for q in (1,2,3) for r in ('i','ii')]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None),(4,None)]]
        assert len(keys) == len(set(keys)) == 40
        return set(keys)
    if (year, level) == (2017, 'hl'):
        # Independent 44-page original census: 20 written and 19 listening.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2017-hl-000-paper.pdf': 'f25024625e703cada8bdaf6f3acb2713be820b6d5e9e5ce640087fdcbcd65815',
            'papers/2017-hl-A00-paper.pdf': 'd704a57c8d5b3bded04a8c0da5f3ebacbbea06968dcdb2db2c14f164d1ca262b',
            'schemes/2017-hl.pdf': '4436cf9e87767e3d7092bedbb38ad8818b731d232565d2d0fca1976621e95abd',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(2,'iii'),(3,'i'),(3,'ii'),(4,'i'),(4,'ii'),(4,'iii'),(4,'iv')]]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]
        keys += [(u,None,None,None) for u in ('LA1','LA2')]
        keys += [(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys) == 20
        keys += [('L1',q,None,None) for q in (1,2,3,4)]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        keys += [('L3',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None),(4,None)]]
        assert len(keys) == len(set(keys)) == 39
        return set(keys)
    if (year, level) == (2023, 'hl'):
        # Original51-page visual census:16written+8aural+27scheme.
        # Four whole summaries; each complete writing choice pool is one task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2023-hl-000-paper.pdf': '84c1b64263f16512a296609cc8e6725dccc9c1256ada024183e8f7b2cc29e5b4',
            'papers/2023-hl-A00-paper.pdf': '37f2bd651bc04a93dbd619085ba3eecb44e1976e21d224b87c677b7fdcb284b6',
            'schemes/2023-hl.pdf': '63933208c9846387f93bba3f48c13ec4d8821d7f3af1597998bcc8c531d983de',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1', q, None, r) for q, romans in [(1,('i','ii','iii')),(2,('i','ii')),(3,('i','ii')),(4,('i','ii'))] for r in romans]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]
        keys += [(unit,None,None,roman) for unit in ('LA1','LA2') for roman in ('i','ii')]
        keys += [(unit,q,None,None) for unit,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys) == 21
        keys += [('L1',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L2',q,None,r) for q in (1,2,3) for r in ('i','ii')]
        keys += [('L3',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None)]]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None),(4,None)]]
        assert len(keys) == len(set(keys)) == 41
        return set(keys)
    if (year, level) == (2010, 'ol'):
        # Independent 40-page census: three club-capacity subparts, one named
        # five-floor task, ten dialogue gaps including two in exchange6.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2010-ol-000-paper.pdf': '8a4c29e76ab591c9d406b8cb3fcd57f57cbf7f4b178e32ea6c26614f1ac5502d',
            'papers/2010-ol-A00-paper.pdf': '0fb3329b722ebca3bcd74cd30fac7df55ed2b5ba7ab4d267d19a2af60f021844',
            'schemes/2010-ol.pdf': 'a9fa632484624a15aab956313b463260948d60ae1deaeb4f6344ef4dff2da67e',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('IR1',None,None,r) for r in ('i','ii','iii','iv','v','vi','vii')]
        keys += [('IR2',None,None,r) for r in ('i','iii','iv')]
        keys += [('IR2',None,a,'ii') for a in ('a','b','c')]
        keys += [('CD',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,'i'),(3,None),(4,None)]]
        keys += [(u,None,None,None) for u in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys) == 24
        keys += [('L1',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None),(4,None)]]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(4,None)]]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(2,'i'),(2,'ii'),(3,None)]]
        assert len(keys) == len(set(keys)) == 42
        return set(keys)
    if (year, level) == (2011, 'ol'):
        # Independent 44-page visual census. CD Q2 has no booklet roman marker;
        # the festival time/date/year question remains one total-only task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2011-ol-000-paper.pdf': '66f722cae32f9fe493d4b0c6fc5c3ace6127e75d0ea70e588f14bd3af9c338b7',
            'papers/2011-ol-A00-paper.pdf': '714fb158cd3dbeeb8c556fb529881376db8154a1c6615ad8a3c8a4f4da8bb8ed',
            'schemes/2011-ol.pdf': 'e4160e18369177d720c75bfba145a13289b352affa583db0881a37b058df1716',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('IR1',None,None,r) for r in ('i','ii','iii','iv','v','vi','vii','viii','ix')]
        keys += [('IR2',None,None,r) for r in ('i','ii','iii','iv')]
        keys += [('CD',q,None,r) for q in (1,4,5) for r in ('i','ii')]
        keys += [('CD',q,None,None) for q in (2,3)]
        keys += [(u,None,None,None) for u in ('LA2','MM','SD','SA','EW')]
        assert len(keys) == 26
        keys += [('L1',q,None,None) for q in range(1,5)]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        keys += [('L3',q,None,None) for q in range(1,4)]
        keys += [('L4',q,None,None) for q in range(1,5)]
        assert len(keys) == len(set(keys)) == 42
        return set(keys)
    if (year, level) == (2012, 'ol'):
        # Independent 44-page census. Menu task (iv) has four priced subparts;
        # the grammar task belongs to the AVOR text and is not that handwriting.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2012-ol-000-paper.pdf': 'b6aba8df1ea656cf4efa1f1189ebfe6fb204c30969bc0a8d0645ddc3aadc9d61',
            'papers/2012-ol-A00-paper.pdf': '45db827722fbc93fcea8970edde10c6e30cd8011d343a33ffc2caedaf25d4fa6',
            'schemes/2012-ol.pdf': '8dfb1ad867bbb88bbbaf13a5608bd0c0c9c94eae8a792f6f4104e13cb17d0071',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('IR1',None,None,r) for r in ('i','ii','iii')]
        keys += [('IR1',None,a,'iv') for a in ('a','b','c','d')]
        keys += [('IR2',None,None,r) for r in ('i','ii','iii')]
        keys += [('CD',q,None,r) for q in (1,2) for r in ('i','ii','iii')]
        keys += [('CD',q,None,None) for q in (3,4)]
        keys += [(u,None,None,None) for u in ('LA2','MM','SD','SA','EW')]
        assert len(keys) == 23
        keys += [('L1',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(4,None)]]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None)]]
        keys += [('L3',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(3,None)]]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None),(4,None)]]
        assert len(keys) == len(set(keys)) == 42
        return set(keys)
    if (year, level) == (2013, 'ol'):
        # Independent 44-page visual census. The two restaurant subparts are
        # distinct asks; nine learner groups belong to one choose-five task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2013-ol-000-paper.pdf': '48a29fa96259ea535913e07fde760949d91f854dacb10ae8a90cdb0eb9b18a07',
            'papers/2013-ol-A00-paper.pdf': '3aa28cebff239c2f82bdbf2d82e085112eaf1b8d514d0931e1d1bd37b8d79de2',
            'schemes/2013-ol.pdf': '0aafd6dfe0224a50fd53f45934ebb0e32e9241b05ba51c2854e8b712a792a0be',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('IR1',None,None,'i'),('IR1',None,'a','ii'),('IR1',None,'b','ii'),('IR1',None,None,'iii')]
        keys += [('IR2',None,None,r) for r in ('i','ii')]
        keys += [('CD',q,None,r) for q,rs in [(1,('i','ii','iii','iv')),(2,('i','ii')),(3,('i','ii')),(4,('i','ii','iii','iv'))] for r in rs]
        keys += [(u,None,None,None) for u in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys) == 24
        keys += [('L1',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None),(4,None)]]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None)]]
        keys += [('L3',q,None,None) for q in range(1,5)]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None),(4,None)]]
        assert len(keys) == len(set(keys)) == 42
        return set(keys)
    if (year, level) == (2014, 'ol'):
        # Independent 44-page visual census, hash-bound before authoring.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2014-ol-000-paper.pdf': 'fa8c43f85b8c65aa24a0989c22213a548c729106057965052908d8a887107eef',
            'papers/2014-ol-A00-paper.pdf': '1e2b3340b53b7ecd8f8e2deeb9ff5ed3b96914f41f3c77aafe21e13f37468720',
            'schemes/2014-ol.pdf': 'b3186b37ad28e970e617c4c9fc3710628400da21c59a2dd18e51f444799e2d3c',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [(unit, None, None, roman) for unit in ('IR1', 'IR2') for roman in ('i','ii','iii','iv','v','vi')]
        keys += [('CD', q, None, roman) for q in range(1,5) for roman in ('i','ii','iii')]
        keys += [(unit, None, None, None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys) == 30
        keys += [('L1', q, None, r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None),(4,None)]]
        keys += [('L2', q, None, r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        keys += [('L3', q, None, r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(4,None)]]
        keys += [('L4', q, None, r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        assert len(keys) == len(set(keys)) == 50
        return set(keys)
    if (year, level) == (2015, 'ol'):
        # Independent 44-page visual census. Three separately numbered/priced
        # matching exercises; two cultural essays share one 30-mark choice task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2015-ol-000-paper.pdf': '6ac6846e912d21fb2bb26784c390da98e538e0ca6ec40aabfd43acf23025cd1f',
            'papers/2015-ol-A00-paper.pdf': 'aef9d92ffb824252084ce34575e43d03ebe224d7840c9c5f27ca3f7732e24064',
            'schemes/2015-ol.pdf': '6dab67571e6bf05778257e96590973615860ba212d718eb19742c73cfdf5ef88',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('IR1', None, None, r) for r in ('i','ii','iii','iv','v','vi','vii','viii','ix')]
        keys += [('IR2', None, None, r) for r in ('i','ii','iii','iv','v','vi','vii','viii')]
        keys += [('CD', q, None, r) for q, rs in [(1,('i','ii','iii')),(2,('i','ii')),(3,('i','ii','iii')),(4,('i','ii'))] for r in rs]
        keys += [('MM', None, None, r) for r in ('i','ii','iii')]
        keys += [(u, None, None, None) for u in ('LA1','LA2','SD','SA','EW')]
        assert len(keys) == 35
        keys += [('L1', q, None, None) for q in range(1,6)]
        keys += [('L2', q, None, r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L3', q, None, r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None),(4,None)]]
        keys += [('L4', q, None, None) for q in range(1,5)]
        assert len(keys) == len(set(keys)) == 54
        return set(keys)
    if (year, level) == (2018, 'ol'):
        # Independent44-page visual census:20written+8aural+16scheme.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2018-ol-000-paper.pdf':'ecdc14883748d1b8784886a5a8daa9215273c90f666d88a4750cf31958b4e018',
            'papers/2018-ol-A00-paper.pdf':'d5f944ddcacabec032c48ee1bfc130b4cdf60e96905e27376570afe5297d5c9c',
            'schemes/2018-ol.pdf':'fcb24b1b07dc2d5369a4c27506485b2e0670f79dfdfb68b556efc289fac62bc3',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys=[('IR1',None,None,r) for r in ('i','ii','iii','iv','v','vi','vii')]
        keys += [('IR2',q,None,None) for q in range(1,5)]
        keys += [('CD',q,None,r) for q,romans in [(1,('i','ii','iii','iv')),(2,('i','ii')),(3,(None,)),(4,('i','ii'))] for r in romans]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys)==26
        keys += [('L1',q,None,None) for q in (1,2,3,4,5)]
        keys += [('L2',q,None,None) for q in (1,2,3,4)]
        keys += [('L3',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None)]]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,None),(3,'i'),(3,'ii')]]
        assert len(keys)==len(set(keys))==43
        return set(keys)
    if (year, level) == (2019, 'ol'):
        # Independent48-page visual census:20written+8aural+20scheme.
        # Both discourse dialogues are required; TWO cultural topics share30.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2019-ol-000-paper.pdf':'41d32895142e7d84b407db7aba924b55c6f436cf04f8e5d42752008d52766857',
            'papers/2019-ol-A00-paper.pdf':'f0a5627680ab08fd5249384d34e2d95dd67eba058144feb7c6458ea1683f2dbb',
            'schemes/2019-ol.pdf':'8622b34ca8c3a357141ced0ff917e9ebeea56e3f3783e86f3f1403d5e32a3237',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys=[('IR1',q,None,None) for q in range(1,8)]
        keys += [('IR2',q,None,None) for q in range(1,6)]
        keys += [('CD',q,None,r) for q,romans in [(1,('i','ii','iii','iv')),(2,('i','ii','iii')),(3,('i','ii'))] for r in romans]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys)==27
        keys += [('L1',q,None,None) for q in (1,2,3,4,5)]
        keys += [('L2',q,None,None) for q in (1,2,3,4)]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None)]]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None)]]
        assert len(keys)==len(set(keys))==44
        return set(keys)
    if (year, level) == (2021, 'ol'):
        # Independent52-page visual sweep. Adjusted175written+100listening;
        # all practice alternatives305. Each complete choice pool is one task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2021-ol-000-paper.pdf':'9f52fa220c7d5e407d32de63d657e8e43b822d782872c57b4e8f84b9b3c4f796',
            'papers/2021-ol-A00-paper.pdf':'bab6aad288773bf503848dc4e868b6c0c5dbac13ae118e4bc19e03f9ac0521c4',
            'schemes/2021-ol.pdf':'2a4833b1c9cda239dac9671a3a9a7a6bbdf2d93d5ab58954e928dc0c49f9bc14',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys=[('IR1',None,None,r) for r in ('i','ii','iii','iv','v','vi','vii','viii')]
        keys += [('IR2',None,None,r) for r in ('i','ii','iii','iv')]
        keys += [('CD',q,None,r) for q,romans in [(1,('i','ii','iii')),(2,('i','ii','iii','iv')),(3,('i','ii')),(4,('i','ii'))] for r in romans]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys)==29
        keys += [('L1',q,None,None) for q in (1,2,3,4)]
        keys += [('L2',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None),(4,None)]]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None),(4,None)]]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None)]]
        assert len(keys)==len(set(keys))==47
        return set(keys)
    if (year, level) == (2022, 'ol'):
        # Independent53-page sweep. Adjusted175written+100listening;
        # all practice alternatives305. Each complete choice pool is one task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2022-ol-000-paper.pdf':'a706a1a3b4a1898ebe170609a5b699388178b8dd45461a60a546e4381b8882cd',
            'papers/2022-ol-A00-paper.pdf':'ed8dc696911237310a16ce4e7ed7bc2c16381aecf33ecc78fc976469119796fd',
            'schemes/2022-ol.pdf':'184ff292e15bf7702b94bdb4e7626d7bfb538bfb948bed4c85ae4efe01df7399',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys=[('IR1',q,None,None) for q in range(1,7)]
        keys += [('IR2',1,None,r) for r in ('i','ii','iii','iv')]
        keys += [('CD',q,None,r) for q,romans in [(1,(None,)),(2,('i','ii')),(3,(None,)),(4,('i','ii')),(5,(None,)),(6,(None,))] for r in romans]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys)==24
        keys += [(unit,q,None,r) for unit in ('L1','L2') for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(4,None)]]
        keys += [('L3',q,None,None) for q in (1,2,3,4)]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None)]]
        assert len(keys)==len(set(keys))==42
        return set(keys)
    if (year, level) == (2022, 'hl'):
        # Independent51-page sweep (16written+8aural+27scheme). Adjusted
        # choice:170written+80listening; all practice alternatives320.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2022-hl-000-paper.pdf': '73b129f223b597be6e096ded274e54b6fbc43260ee0f0b4c356b9477e956b273',
            'papers/2022-hl-A00-paper.pdf': '86914ac9598814d8c89db30655a24271c4d5f97ddbfe1d0e976938d495f7bb6d',
            'schemes/2022-hl.pdf': '7f539dcb7b70c18e30b1047e463426bd2715926ddfe16a6daa0a93b995907071',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1',q,None,r) for q,romans in [(1,('i','ii','iii')),(2,('i','ii')),(3,('i','ii','iii')),(4,(None,))] for r in romans]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]
        keys += [(unit,None,None,r) for unit in ('LA1','LA2') for r in ('i','ii')]
        keys += [(unit,q,None,None) for unit,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys)==21
        keys += [(unit,q,None,r) for unit in ('L1','L2') for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(3,None),(4,None)]]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,None),(3,None),(4,'i'),(4,'ii')]]
        keys += [('L4',q,None,r) for q in (1,2,3) for r in ('i','ii')]
        assert len(keys)==len(set(keys))==44
        return set(keys)
    if (year, level) == (2023, 'ol'):
        # Independent53-page visual census:20written+8aural+25scheme.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2023-ol-000-paper.pdf': '28b5a7cf5e15f3c2da6f6938f3b2f13abd888eab5dabd16f28b6966fb1e0e4ce',
            'papers/2023-ol-A00-paper.pdf': 'a5ecc7cb74169bcd00d5bc69fe2ce083c96019f449d31515ada7041d2a298b32',
            'schemes/2023-ol.pdf': 'da5064b6da1f3906e010bf0ae0610add8100a8b00964149bb6d2ca97593e1b5b',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [(unit,q,None,None) for unit in ('IR1','IR2') for q in range(1,8)]
        keys += [('CD',q,None,r) for q,romans in [(1,('i','ii')),(2,('i','ii')),(3,('i','ii','iii')),(4,('i','ii'))] for r in romans]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys) == 29
        keys += [(unit,q,None,r) for unit in ('L1','L2') for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None)]]
        keys += [('L4',q,None,None) for q in (1,2,3,4)]
        assert len(keys) == len(set(keys)) == 47
        return set(keys)
    if (year, level) == (2024, 'ol'):
        # All20written+8aural+25scheme pages independently inspected.
        # CD booklet3(iii)/(iv) are misnumbered(iv)/(v) in the scheme.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2024-ol-000-paper.pdf': '7ca7754d00496ebdc9ce022665c6eba8f7378bf7325d02d46ceab168f3761970',
            'papers/2024-ol-A00-paper.pdf': '9384428ab46b24725f66f30afafdfb22048b4507de24e6307eb2df4fe1ea547c',
            'schemes/2024-ol.pdf': 'ecba77fed2ef00afe4503bb1d4ed4b5ea0c5803a53727338592764406fbee44a',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('IR1',q,None,r) for q,romans in [(1,('i','ii')),(2,('i','ii')),(3,('i','ii','iii')),(4,(None,))] for r in romans]
        keys += [('IR2',q,None,None) for q in range(1,8)]
        keys += [('CD',q,None,r) for q,romans in [(1,('i','ii')),(2,('i','ii','iii')),(3,('i','ii','iii','iv'))] for r in romans]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys) == 30
        keys += [(unit,q,None,r) for unit in ('L1','L2','L3') for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        assert len(keys) == len(set(keys)) == 50
        return set(keys)
    if (year, level) == (2024, 'hl'):
        # Independent original-PDF sweep:16written+8aural+28scheme pages.
        # Twelve comprehension asks; four whole summaries; each complete
        # writing choice pool and discourse exercise remains one task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2024-hl-000-paper.pdf': 'c154f981d7a257665eb0a71e24e2246dc5e0e14431297819ff91017da79fc1c7',
            'papers/2024-hl-A00-paper.pdf': '98df8494df03f7ff48a5438d5202036813c4d9a7525d102ca75c9201c95a54c9',
            'schemes/2024-hl.pdf': '3fd5f06ee6dbc78e1ef53bcaa1e1e6f9a6d822c6ee898a69f16ec34cf0aac999',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1', q, None, r) for q, romans in [(1, ('i','ii')), (2, ('i','ii','iii','iv')), (3, ('i','ii','iii','iv')), (4, ('i','ii'))] for r in romans]
        keys += [('C2', q, None, None) for q in (1,2,3,4)]
        keys += [(unit, None, None, roman) for unit in ('LA1','LA2') for roman in ('i','ii')]
        keys += [(unit, question, None, None) for unit, question in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys) == 24
        keys += [(unit,q,None,r) for unit in ('L1','L2','L3','L4') for q in (1,2,3) for r in ('i','ii')]
        assert len(keys) == len(set(keys)) == 48
        return set(keys)
    if (year, level) == (2025, 'hl'):
        # Independent visual review: all16 written,8 aural,27 scheme pages.
        # Four complete summaries include their discretionary component;
        # five essay topics and six guided prompts remain two choice pools.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2025-hl-000-paper.pdf': '671650c672d92ab191f615700de4dfd7077835d86223a2e976a8818809c8d97f',
            'papers/2025-hl-A00-paper.pdf': 'edcc2149eddeababbeb62a5e471c22de654b4fb74bbf671b2e12c0e5abb921fe',
            'schemes/2025-hl.pdf': '3c74de1d1d5d35a4e0e9ada2b5e7754446722444003f480a2bd876c90c27a52b',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1', q, None, r) for q, romans in [(1, ('i','ii','iii')), (2, ('i','ii')), (3, ('i','ii','iii')), (4, (None,))] for r in romans]
        keys += [('C2', q, None, None) for q in (1,2,3,4)]
        keys += [(unit, None, None, roman) for unit in ('LA1','LA2') for roman in ('i','ii')]
        keys += [(unit, question, None, None) for unit, question in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys) == 21
        for unit in ('L1','L3'):
            keys += [(unit,q,None,r) for q in (1,2,3) for r in ('i','ii')]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(3,None)]]
        assert len(keys) == len(set(keys)) == 43
        return set(keys)
    if (year, level) == (2025, 'ol'):
        # Independent visual sweep:20written+8aural+26scheme pages. The
        # event table and each complete alternative pool are single tasks.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2025-ol-000-paper.pdf': 'a32ab3a53c7d4b97e511656c01384558307700f6d4874dc34337f067c988acc4',
            'papers/2025-ol-A00-paper.pdf': '5621c29b27d2a9b226e8f239a058e24cebe90aa904f18d6bb4fcab31f7454a77',
            'schemes/2025-ol.pdf': '2da580d0bece12bce51802feedb9117cc96d0a28ba5a334d61cd93055f3104d3',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('IR1', q, None, r) for q in (1,2,3,4) for r in ('i','ii')]
        keys += [('IR2',1,None,r) for r in ('i','ii')]
        keys += [('IR2',q,None,None) for q in (2,3,4,5)]
        keys += [('CD',q,None,r) for q in (1,2) for r in ('i','ii','iii')]
        keys += [('CD',3,None,r) for r in ('i','ii')]
        keys += [('CD',4,None,r) for r in ('i','ii','iii','iv')]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys) == 32
        keys += [(unit,q,None,r) for unit in ('L1','L2','L3','L4') for q in (1,2,3) for r in ('i','ii')]
        assert len(keys) == len(set(keys)) == 56
        return set(keys)
    if year != 2026 or level not in ('hl', 'ol'):
        return None
    root = Path(__file__).resolve().parents[3]
    sources = {
        'papers/2026-hl-000-paper.pdf': 'e9fd3cede429b88a1f530fe18a494af3e2cdeb98ba218c932c3d4a72fe147992',
        'papers/2026-hl-A00-paper.pdf': 'c0c4ed2e47c5476de8d68179f90acf383c79d2648e77b7bc34589d32caeccb6d',
        'schemes/2026-hl.pdf': 'e56810faf2cb2b34e30216c07b4ff771d1cc6f99b91fb6fcf1d47d045d8265be',
    } if level == 'hl' else {
        'papers/2026-ol-000-paper.pdf': '118ab2d6814246c2a9f071945a888fd1ec7be42a46d2d9cf996a25703103f070',
        'papers/2026-ol-A00-paper.pdf': 'd6a8bb9334a155937d15c2287001e5e5e9bd0606993df7f449185cb3837df966',
        'schemes/2026-ol.pdf': '7fb47439b0e1322e592da32dc160f2f164a84c8ac4810d02b18e7a17d3d89047',
    }
    for relative, digest in sources.items():
        path = root / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
    keys = []
    if level == 'ol':
        # Original paper pp3–4: eight asks; pp7–8: seven asks, including one
        # four-heading table. pp13–14: ten comprehension asks. Each complete
        # LA, matching, dialogue or writing choice pool is one task.
        keys += [('IR1', q, None, r) for q in (1, 2, 3, 4) for r in ('i', 'ii')]
        keys += [('IR2', q, None, None) for q in (1, 2, 3, 4, 5, 6, 7)]
        keys += [('CD', q, None, r) for q in (1, 2) for r in ('i', 'ii')]
        keys += [('CD', q, None, r) for q in (3, 4) for r in ('i', 'ii', 'iii')]
        keys += [(unit, None, None, None) for unit in ('LA1', 'LA2', 'MM', 'SD', 'SA', 'EW')]
        assert len(keys) == 31
        for unit in ('L1', 'L3'):
            keys += [(unit, q, None, r) for q in (1, 2, 3) for r in ('i', 'ii')]
        keys += [('L1', 1, None, 'iii'), ('L3', 2, None, 'iii')]
        keys += [('L2', q, None, r) for q in (1, 2) for r in ('i', 'ii')]
        keys += [('L2', 3, None, None)]
        keys += [('L4', q, None, r) for q in (1, 2, 3) for r in ('i', 'ii')]
        assert len(keys) == len(set(keys)) == 56
        return set(keys)
    for question, romans in [(1, ('i','ii','iii')), (2, ('i','ii')), (3, ('i','ii')), (4, ('i','ii','iii'))]:
        keys += [('C1', question, None, roman) for roman in romans]
    keys += [('C2', q, None, None) for q in (1,2,3,4)]
    keys += [(unit, None, None, roman) for unit in ('LA1','LA2') for roman in ('i','ii')]
    keys += [(unit, question, None, None) for unit, question in [('SD',3),('GR',1),('SE',2),('GW',3)]]
    for unit in ('L1','L3','L4'):
        keys += [(unit,q,None,r) for q in (1,2,3) for r in ('i','ii')]
    keys += [('L2',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(2,'iii'),(3,None)]]
    assert len(keys) == len(set(keys)) == 46
    return set(keys)
