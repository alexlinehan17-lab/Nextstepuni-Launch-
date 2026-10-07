"""Explicit Irish source bindings for the reviewed 2010 practice identities.

These are edition-specific coordinates, never English coordinates reused on a
translation. Shared stems, figure labels and pooled tariff instructions remain
in the crop. Exact key expansion prevents q11aii matching q11aiii.
"""


def regions(page, top, bottom):
    return [{'p': page, 'r': [0, top, 1, bottom]}]


def bind(target, keys, page, top, bottom):
    for key in keys.split():
        assert key not in target, key
        target[key] = regions(page, top, bottom)


def higher():
    paper, scheme = {}, {}
    for keys, page, top, bottom in [
        ('q1a',2,.135,.174),('q1b',2,.180,.204),('q1c',2,.210,.234),
        ('q1di',2,.240,.259),('q1dii',2,.240,.324),('q1e',2,.330,.400),
        ('q1f',2,.405,.475),('q1g',2,.480,.535),('q1h',2,.540,.565),
        ('q1i',2,.570,.610),('q1j',2,.615,.711),
        ('q2a',2,.796,.820),('q2b',2,.826,.850),('q2c',2,.856,.892),
        ('q3o1ai q3o1aii q3o1aiii q3o1aiv',3,.030,.202),
        ('q3o1b',3,.210,.234),('q3o1c',3,.240,.293),
        ('q3o2ai q3o2aii',3,.397,.451),
        ('q3o2b-parasitic q3o2b-deficiency q3o2b-route-hoose q3o2b-route-grass-tetany',3,.457,.512),
        ('q3o2c',3,.517,.556),
        ('q5ai q5aii',4,.030,.084),('q5bi q5bii',4,.090,.146),('q5c',4,.151,.190),
        ('q6a',4,.273,.297),('q6b',4,.303,.342),('q6ci q6cii',4,.348,.402),
        ('q6d',4,.408,.447),
        ('q7bi q7bii q7biii',4,.618,.733),('q7ci q7cii',4,.738,.778),('q7d',4,.784,.823),
        ('q8a',5,.059,.099),('q8b',5,.105,.129),
        ('q9a',5,.360,.400),('q9b',5,.405,.430),('q9c',5,.435,.460),
        ('q9d',5,.465,.490),('q9e',5,.495,.535),
    ]:
        bind(paper,keys,page,top,bottom)
    for letter, top, bottom in [('a',.682,.705),('b',.705,.728),('c',.728,.750),('d',.750,.789)]:
        paper['q4'+letter] = regions(3,.636,.676)+regions(3,top,bottom)
    for letter in 'abcde':
        paper['q9'+letter] = regions(5,.330,.355)+paper['q9'+letter]
    for route in ['i-ii-iii','i-ii-iv','i-iii-iv','ii-iii-iv']:
        paper['q7a-route-'+route] = regions(4,.528,.613)
        paper['q8c-route-'+route] = regions(5,.135,.249)
        scheme['q7a-route-'+route] = regions(10,.057,.349)
        scheme['q8c-route-'+route] = regions(11,.381,.925)
    for keys, page, top, bottom in [
        ('q1a',4,.057,.204),('q1b',4,.203,.352),('q1c',4,.351,.435),
        ('q1di q1dii',4,.434,.485),('q1e',4,.484,.567),('q1f',4,.566,.617),
        ('q1g',4,.616,.667),('q1h',4,.666,.717),('q1i',4,.715,.783),('q1j',4,.781,.900),
        ('q2a',5,.057,.267),('q2b',5,.266,.481),('q2c',5,.480,.581),
        ('q3o1ai q3o1aii q3o1aiii q3o1aiv',6,.057,.234),
        ('q3o1b',6,.233,.382),('q3o1c',6,.381,.550),
        ('q3o2ai q3o2aii',7,.112,.215),
        ('q3o2b-parasitic q3o2b-deficiency q3o2b-route-hoose q3o2b-route-grass-tetany',7,.214,.823),
        ('q3o2c',7,.821,.939),
        ('q4a',8,.057,.202),('q4b',8,.201,.284),('q4c',8,.283,.334),('q4d',8,.333,.466),
        ('q5ai q5aii',8,.570,.738),('q5bi q5bii',8,.736,.869),('q5c',8,.868,.921),
        ('q6a',9,.057,.169),('q6b',9,.168,.268),('q6ci q6cii',9,.267,.383),('q6d',9,.382,.469),
        ('q7bi',10,.348,.386),('q7bii',10,.386,.551),('q7biii',10,.556,.611),
        ('q7ci q7cii',10,.611,.809),('q7d',10,.808,.925),
        ('q8a',11,.057,.267),('q8b',11,.266,.382),
        ('q9a',12,.057,.259),('q9b',12,.258,.341),('q9c',12,.340,.408),
        ('q9d',12,.407,.490),('q9e',12,.489,.608),
    ]:
        bind(scheme,keys,page,top,bottom)
    return paper, scheme


def ordinary():
    paper, scheme = {}, {}
    for keys, page, top, bottom in [
        ('q1a',2,.265,.734),('q1b',2,.756,.865),('q1c',2,.887,.960),
        ('q2-2 q2-3 q2-4 q2-5 q2-6',3,.047,.373),
        ('q3a',3,.396,.570),('q3b',3,.592,.686),
        ('q3c-lactation q3c-colostrum',3,.708,.800),('q3d',3,.820,.912),
        ('q4-mastitis q4-swine-fever q4-brucellosis q4-liver-fluke q4-tuberculosis',4,.047,.287),
        ('q5',4,.291,.960),('q6a',5,.047,.341),('q6b',5,.340,.407),('q6c',5,.411,.484),
        ('q7',5,.485,.953),
        ('q8ai q8aii-strip q8aii-paddock q8aiii-strip-advantage q8aiii-strip-disadvantage q8aiii-paddock-advantage q8aiii-paddock-disadvantage',6,.228,.660),
        ('q8aiv',6,.228,.681),('q8bi q8bii',6,.704,.763),('q8c',6,.786,.812),
        ('q8d-tillering q8d-topping',6,.835,.894),
        ('q9a',7,.047,.170),('q9b',7,.194,.219),('q9c',7,.244,.268),
        ('q9d',7,.244,.318),('q9f',7,.527,.589),
        ('q10ai',8,.047,.332),('q10aii q10aiii',8,.332,.382),
        ('q10aiv q10av',8,.381,.456),('q10bi',8,.455,.760),
        ('q10bii q10biii',8,.759,.834),('q10biv q10bv',8,.833,.931),
        ('q11ai q11aii q11aiii q11aiv',9,.047,.204),
        ('q11bi q11bii q11biii-feeding q11biii-management',9,.210,.302),
        ('q11ci q11cii',9,.309,.400),
        ('q12ai q12aii q12aiii',9,.489,.581),
        ('q12bi q12bii q12biii q12biv',9,.587,.728),
        ('q12ci q12cii q12ciii',9,.735,.843),
        ('q12di-germination q12di-establishment q12dii',9,.850,.925),
        ('q13a',10,.047,.417),('q13bi',10,.429,.795),
        ('q13ci',11,.357,.395),('q13cii',11,.394,.705),
    ]:
        bind(paper,keys,page,top,bottom)
    paper['q13bii'] = regions(10,.429,.795)+regions(11,.047,.315)
    for key, top, bottom in [('q9ei',.367,.391),('q9eii',.391,.416),('q9eiii',.416,.440),
                             ('q9eiv',.416,.465),('q9ev',.465,.490),('q9evi',.489,.514)]:
        paper[key] = regions(7,.244,.268)+regions(7,.342,.367)+regions(7,top,bottom)
    for keys, page, top, bottom in [
        ('q1a',4,.116,.165),('q1b',4,.170,.237),('q1c',4,.242,.273),
        ('q2-2 q2-3 q2-4 q2-5 q2-6',4,.276,.473),
        ('q3a',4,.492,.550),('q3b',4,.552,.646),
        ('q3c-lactation',4,.648,.674),('q3c-colostrum',4,.674,.739),('q3d',4,.746,.777),
        ('q4-mastitis q4-swine-fever q4-brucellosis q4-liver-fluke q4-tuberculosis',5,.067,.245),
        ('q5',5,.245,.413),('q6a q6b q6c',5,.418,.543),('q7',5,.548,.904),
        ('q8ai',6,.131,.160),('q8aii-strip',6,.166,.255),('q8aii-paddock',6,.261,.331),
        ('q8aiii-strip-advantage',6,.338,.420),('q8aiii-strip-disadvantage',6,.427,.478),
        ('q8aiii-paddock-advantage',6,.484,.566),('q8aiii-paddock-disadvantage',6,.572,.654),
        ('q8aiv',6,.659,.723),('q8bi',6,.763,.792),('q8bii',6,.798,.861),
        ('q8c',7,.070,.542),('q8d-tillering',7,.579,.609),('q8d-topping',7,.616,.667),
        ('q9a',8,.067,.115),('q9b',8,.121,.203),('q9c',8,.208,.239),('q9d',8,.245,.276),
        ('q9f',9,.070,.188),
        ('q11ai',11,.067,.109),('q11aii',11,.114,.197),('q11aiii',11,.202,.227),('q11aiv',11,.232,.309),
        ('q11bi q11bii q11biii-feeding',11,.344,.436),('q11biii-management',11,.440,.523),
        ('q11ci',11,.559,.585),('q11cii',11,.589,.714),
        ('q12ai',12,.099,.142),('q12aii q12aiii',12,.146,.222),
        ('q12bi q12bii q12biii',12,.223,.353),('q12biv',12,.358,.471),
        ('q12ci q12cii q12ciii',12,.506,.681),
        ('q12di-germination q12di-establishment q12dii',12,.686,.829),
        ('q13a',13,.132,.361),
    ]:
        bind(scheme,keys,page,top,bottom)
    for key, potato_top, potato_bottom, barley_top, barley_bottom in [
        ('q9ei',.313,.363,.709,.735),('q9eii',.369,.400,.740,.785),
        ('q9eiii',.406,.456,.790,.816),('q9eiv',.462,.512,.821,.847),
        ('q9ev',.517,.599,.852,.896),('q9evi',.604,.667,.901,.925),
    ]:
        scheme[key] = regions(8,.282,.308)+regions(8,potato_top,potato_bottom)+regions(8,barley_top,barley_bottom)
    for key, top, bottom in [
        ('q10ai',.104,.160),('q10aii',.165,.191),('q10aiii',.196,.241),('q10aiv',.246,.272),
        ('q10av',.276,.302),('q10bi',.307,.364),('q10bii',.369,.432),('q10biii',.437,.520),
        ('q10biv',.524,.550),('q10bv',.555,.638),
    ]:
        scheme[key] = regions(10,.067,.099)+regions(10,top,bottom)
    for key, top, bottom in [('q13bi',.396,.521),('q13bii',.396,.521),('q13ci',.527,.602),('q13cii',.527,.602)]:
        scheme[key] = regions(13,.132,.175)+regions(13,top,bottom)
    return paper, scheme


def attach_sources(tasks, paper_reviews):
    """Fail closed when a task or source binding is missing, duplicated or stale."""
    for level, prefix, maps in [('higher','agsci-2010-hl-',higher()),('ordinary','agsci-2010-ol-',ordinary())]:
        paper, scheme = maps
        selected = [task for task in tasks if task['cardIds'][0].startswith(prefix)]
        keys = {cid.removeprefix(prefix) for task in selected for cid in task['cardIds']}
        assert keys == set(paper) == set(scheme), (keys-set(paper),set(paper)-keys,keys-set(scheme),set(scheme)-keys)
        review = next(p for p in paper_reviews if p['lang']=='iv' and p['level']==level)
        expected = (62,43,44) if level=='higher' else (85,48,64)
        freeze = lambda mapping: {tuple((seg['p'],tuple(seg['r'])) for seg in crop) for crop in mapping.values()}
        assert (len(keys),len(freeze(paper)),len(freeze(scheme))) == expected
        for mapping, pages in [(paper,review['paperPagesInspected']),(scheme,review['schemePagesInspected'])]:
            for crop in mapping.values():
                for segment in crop:
                    left,top,right,bottom = segment['r']
                    assert segment['p'] in pages and 0<=left<right<=1 and 0<=top<bottom<=1
        review['practiceTaskCropReview'] = {
            'status':'reviewed','taskBindings':expected[0],
            'distinctPaperCropSets':expected[1],'distinctSchemeCropSets':expected[2],
            'evidence':'Every distinct crop rendered and visually inspected, including shared stems, figures, pooled tariffs and continuation pages. Clipped text and missing shared instructions corrected and re-rendered. Same practice identities as English; edition-specific schemes and source notes retained.',
        }
        for task in selected:
            cid = task['cardIds'][0]
            key = cid.removeprefix(prefix)
            assert all(paper[key]==paper[c.removeprefix(prefix)] and scheme[key]==scheme[c.removeprefix(prefix)] for c in task['cardIds'])
            ref = task['questionRef'].split(' Q',1)[1]
            label = ('Ceist '+ref).replace('Option One','Rogha a hAon').replace('Option Two','Rogha a Dó')
            label = label.replace('parasitic disease','galar seadánach').replace('deficiency disease','galar easpa')
            label = label.replace('Hoose','Cársán').replace('grass-tetany','Teiteanas féir')
            source = {'lang':'iv','paperFileid':review['paperFileid'],'label':label,
                      'paperRegions':paper[key],'schemeRegions':scheme[key],
                      'marksPerRoute':20 if key in ['q9f','q12dii'] and level=='ordinary' else task['marksPerRoute']}
            relevant = [note['note'] for note in review['sourceNotes']
                        if any(task['questionRef'].split(' Q',1)[1].startswith(part.strip().removeprefix('Q'))
                               for part in note['questionRef'].split(','))]
            if relevant:
                source['schemeNote'] = '\n\n'.join(relevant)
            task['translatedSources'] = [source]
