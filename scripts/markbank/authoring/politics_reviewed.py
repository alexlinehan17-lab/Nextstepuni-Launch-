"""Human-readable decisions made against the rendered paper and scheme pages.

Topic suffixes refer to the canonical curriculum, never a new subject taxonomy.
Unlisted papers remain open work. Counts from extraction do not certify them.
"""

REVIEWED = {
    (2018, 'higher'): {
        'paperPagesReviewed': list(range(1, 25)),
        'schemePagesReviewed': list(range(1, 21)),
        'sourcePages': [7, 8],
        'shortTopics': '0-10 0-5 2-1 3-0 2-5 2-9 0-5 0-6 3-5 0-9 0-6 0-9'.split(),
        'shortMarks': 4,
        'shortMarkNote': 'The scheme marks each short-answer item out of 4. In the full exam, the best five of the ten counted items each receive a further 2 marks. This section-level bonus is not part of an individual practice score.',
        'partMarks': {'1(b)(i)': 2, '1(b)(ii)': 2, '1(i)(i)': 2, '1(i)(ii)': 2},
        'mergeParts': ['1(k)'],
        'dataTopics': {'2': '3-8'},
        'dataMarks': {'2': [15, 15, 30, 25, 25, 40]},
        'topicOverrides': {'2(d)': '1-9', '2(e)': '1-9'},
        'essayTopics': {'3': '0-12', '4(a)': '0-6', '4(b)': '2-5', '5(a)': '3-3', '5(b)': '3-1', '6': '3-4'},
        'criterionAllocations': {
            '1(a)': [('Thinker', 2), ('Political philosophy', 2)],
            '1(e)': [('Thinker', 1), ('Model of education', 1), ('Criticism', 2)],
            '1(g)': [('Advantage', 2), ('Disadvantage', 2)],
            '1(h)': [('First consequence', 2), ('Second consequence', 2)],
            '1(j)': [('First challenge', 2), ('Second challenge', 2)],
            '1(k)': [('Thinker', 2), ('Reason', 2)],
            '1(l)': [('First impact', 2), ('Second impact', 2)],
            '2(a)': [('First piece of information', 5), ('Second piece of information', 5), ('Cohesion', 5)],
            '2(b)': [('First piece of information', 5), ('Second piece of information', 5), ('Cohesion', 5)],
            '2(c)': [('Developed country: first point', 5), ('Developed country: second point', 5), ('Developed country: cohesion', 5), ('Developing country: first point', 5), ('Developing country: second point', 5), ('Developing country: cohesion', 5)],
            '2(d)': [('Authorship: first point', 5), ('Authorship: second point', 5), ('Potential bias: first point', 5), ('Potential bias: second point', 5), ('Relevance', 5)],
            '2(e)': [('Statistics: first point', 5), ('Statistics: second point', 5), ('Evaluation: first point', 5), ('Evaluation: second point', 5), ('Cohesion', 5)],
            '2(f)': [('First point', 10), ('Second point', 10), ('Third point', 10), ('Cohesion', 10)],
        },
        'boundaryNotes': {
            '1(a)': 'Two distinct recall questions, independently marked 2+2; split thinker and philosophy.',
            '1(b)': 'Election-democracy reasoning and Seanad purpose are independent 2-mark tasks.',
            '1(c)': 'Three required definitions share a flexible 4-mark cap: the scheme permits transfer from the first definition to the later two. Retain one task with that conditional allocation.',
            '1(e)': 'Cartoon identification and criticism use one model; retain the linked 1+1+2 marking criteria and original illustration.',
            '1(f)': 'Three open functions share flexible 2+1+1 allocation, with transfer permitted. Retain one 4-mark response.',
            '1(g)': 'Advantage and disadvantage are independently marked 2+2; split, carrying PR-STV into both prompts.',
            '1(h),1(j),1(l)': 'Required pairs of freely chosen examples, not distinct printed routes; retain each response with two criteria.',
            '1(i)': 'Positive and negative effects are independently marked 2+2; retain each printed subpart.',
            '1(k)': 'The reason refers to the thinker selected by the candidate. Keep the dependent pair together with the census context and both criteria.',
            '2(c)': 'Developed and developing country impacts each have a separate 15-mark allocation, including their own cohesion; split with both documents retained.',
            '2(d)': 'Authorship, potential bias and policy relevance have independent allocations of 10, 10 and 5; split with the same report retained.',
            '2(e),2(f)': 'Content and cohesion assess one integrated answer; do not split assessment criteria into questions.',
            '4,5': 'Each printed essay OR is a separate 100-mark route, already represented by its lettered question.',
            '5(b),6': 'And/or and illustrative international organisations are flexible support, not a closed choose-k pool.',
        },
    },
    (2018, 'ordinary'): {
        'paperPagesReviewed': list(range(1, 29)),
        'schemePagesReviewed': list(range(1, 21)),
        'sourcePages': [9, 10],
        'shortTopics': '0-0 2-9 2-0 2-10 3-1 0-12 1-2 3-8 0-6 2-7 1-0 2-7 0-9 2-1 0-9 0-12 3-7 2-5 2-2 0-5'.split(),
        'shortMarks': 5,
        'shortMarkNote': 'Each short-answer item has a base tariff of 5. In the full exam, the best five of the fifteen counted items receive 3 additional marks, and the next five receive 2 additional marks. These section-level bonuses are not part of an individual practice score.',
        'partMarks': {'1(b)(i)': 2, '1(b)(ii)': 3, '1(e)(i)': 1, '1(e)(ii)': 4, '1(o)(i)': 1, '1(o)(ii)': 4},
        'dataTopics': {'2': '2-10', '3': '1-9', '4': '2-0'},
        'dataMarks': {'2': [10, 5, 5, 5, 10, 15], '3': [8, 16, 8, 4, 4], '4': [30, 30]},
        'topicOverrides': {'1(e)(ii)': '1-9', '1(o)(i)': '1-9', '4(b)': '0-12'},
        'essayTopics': {'5': '1-0', '6': '0-6', '7': '3-3', '8': '0-7', '9': '2-5', '10': '3-7'},
        'criterionAllocations': {
            '1(a)': [('First group: name', 2), ('First group: explanation', 1), ('Second group: name', 1), ('Second group: explanation', 1)],
            '1(d)': [('First organisation', 1), ('Second organisation', 1), ('Description of one organisation', 3)],
            '1(e)(ii)': [('Strength', 2), ('Limitation', 2)],
            '1(g)': [('Explanation', 3), ('Example', 2)],
            '1(h)': [('First impact', 2), ('Second impact', 2), ('Third impact', 1)],
            '1(i)': [('Explanation', 3), ('Example', 2)],
            '1(j)': [('Explanation', 3), ('Example', 2)],
            '1(k)': [('Role', 3), ('Name', 2)],
            '1(n)': [('Explanation', 3), ('Example', 2)],
            '1(o)(ii)': [('First reason', 2), ('Second reason', 2)],
            '1(s)': [('First ground', 2), ('Second ground', 1), ('Third ground', 1), ('Fourth ground', 1)],
            '1(t)': [('First statement', 2), ('Second statement', 2), ('Third statement', 1)],
            '2(a)': [('First reason', 5), ('Second reason', 5)],
            '2(e)': [('First difference', 5), ('Second difference', 5)],
            '3(a)': [('First piece of information', 4), ('Second piece of information', 4)],
            '3(b)': [('First strength', 4), ('Second strength', 4), ('First limitation', 4), ('Second limitation', 4)],
            '3(c)': [('First challenge', 4), ('Second challenge', 4)],
            '4(a)': [('First point', 10), ('Second point', 10), ('Cohesion', 10)],
            '4(b)': [('First point', 10), ('Second point', 10), ('Cohesion', 10)],
        },
        'boundaryNotes': {
            '1(a),1(d)': 'Names and explanations depend on the candidate’s chosen groups/organisation; retain each linked response.',
            '1(b)': 'Two independently marked tasks. Carry the ECHR identity into the second task.',
            '1(e)': 'Data retrieval and data evaluation are independent; the latter further splits into a 2-mark strength and a 2-mark limitation.',
            '1(f)': 'Single-correct-answer multiple choice, not a choice of examination routes. Keep all three printed distractors.',
            '1(g),1(i),1(j),1(n)': 'Separately priced definition and example, 3+2: split and carry the defined term into both prompts.',
            '1(k)': 'Role and naming an example are independent 3+2 tasks.',
            '1(l),1(m),1(p),1(q),1(r)': 'Conditional reallocation in the scheme makes these shared-cap responses; keep the full published 5-mark response and its transfer rule.',
            '1(s)': 'Recall four grounds from the statutory set; the paper does not print a finite menu of routes. Keep the 5-mark recall task.',
            '1(t)': 'Three required true/false statements have independent 2, 2 and 1 tariffs; split each statement without turning truth values into alternative routes.',
            '3(b)': 'Two strengths and two limitations each form an independently practicable 8-mark group; split at that boundary.',
            '5-10': 'Might-include lists and familiar examples are optional support; no closed selection requirement.',
            '8': 'School and/or local and/or national level permits flexible scope; no fixed finite number to choose.',
        },
    },
    (2026, 'higher'): {
        'paperPagesReviewed': list(range(1, 29)),
        'schemePagesReviewed': list(range(1, 21)),
        'sourcePages': [8, 9],
        'shortTopics': '1-2 2-2 0-4 0-9 0-5 2-10 0-4 0-9 3-8 0-7 2-1 3-1 0-6 3-7 2-9'.split(),
        'shortMarks': 5,
        'dataTopics': {'2': '3-4'},
        'dataMarks': {'2': [10, 10, 20, 20, 20, 20, 50]},
        'essayTopics': {'3(a)': '0-12', '3(b)': '2-0', '4': '3-4', '5': '0-6', '6': '3-8', '7': '0-12'},
        'promptOverrides': {
            '1(i)': 'What message does this graphic convey about inequality and income distribution in society?',
            '1(m)': 'According to the Consumer Price Index (CPI) June 2025, consumer prices rose by 1.8% over 12 months to June 2025.\nWhat challenges does this data pose for society in Ireland today?',
            '2(g)': 'Drawing on the data presented in both documents and the quotation below, what conclusions can you draw about the perception of Africa as being peripheral and marginal on the global stage?',
        },
        'criterionAllocations': {
            '1(e)': [('First method', 3), ('Second method', 2)],
            '1(g)': [('First aspect', 3), ('Second aspect', 2)],
            '1(j)': [('First example', 3), ('Second example', 2)],
            '1(k)': [('Explanation', 3), ('Example', 2)],
            '2(g)': [('Conclusions', 30), ('Use of documents', 20)],
        },
        'boundaryNotes': {
            '1(e)': 'Two descriptions form one required response; the 3+2 tariff applies across that response, not two selectable methods from a printed pool.',
            '1(g)': 'Two freely chosen aspects, one response. Preserve the asymmetric 3+2 allocation.',
            '1(h)': 'All five filters are required. No finite choice and no per-filter tariff is stated; retain the published total of five.',
            '1(j)': 'Two open examples with a 3+2 allocation, not a finite printed selection.',
            '1(k)': 'Definition and example are separately priced and independently practicable; split during authoring with the term carried into both prompts.',
            '2(g)': 'Conclusions and use of documents assess the same argument; keep one response with both criteria and the additional page-12 map/quotation.',
        },
    },
    (2026, 'ordinary'): {
        'paperPagesReviewed': list(range(1, 29)),
        'schemePagesReviewed': list(range(1, 21)),
        'sourcePages': [10, 11],
        'shortTopics': '2-0 0-0 0-5 2-2 0-6 3-5 2-1 0-5 0-9 2-2 1-0 0-4 3-1 2-10 0-6 3-7 2-1 0-1 3-8 0-5'.split(),
        'shortMarks': 10,
        'partMarks': {'1(d)(i)': 4, '1(d)(ii)': 3, '1(d)(iii)': 3},
        'dataTopics': {'2': '2-0', '3': '1-9', '4': '2-0'},
        'dataMarks': {'2': [10, 10, 10, 10, 10], '3': [5, 5, 10, 15, 15], '4': [10, 10, 15, 15]},
        'essayTopics': {'5': '2-7', '6': '1-2', '7': '0-7', '8': '0-12', '9': '2-5', '10': '3-7'},
        'promptOverrides': {
            '1(h)': 'What is the process for selecting the Northern Ireland Executive and/or ministers?',
            '1(t)': 'Comment on the results of the Presidential Election as presented in this chart:',
            '5': 'Are certain children’s rights being denied or restricted in the world today?\n\nYou may refer to the following in your answer:\n• Children’s rights\n• United Nations Convention on the Rights of the Child (UNCRC)\n• War/conflict\n• Racism\n• Discrimination/prejudice\n• Inequalities\n• Key thinkers e.g. Martha Nussbaum.',
            '6': 'Discuss the idea of protesting in the world today.\n\nYou may refer to the following in your answer:\n• Examples of protests\n• How news of protests spreads\n• Hate speech and free speech\n• Reasons for protesting\n• Responsibilities of the government and citizens\n• Impacts of protests\n• Civil disobedience\n• Key thinkers e.g. Noam Chomsky, John Locke.',
            '7': 'Discuss the reasons why it is important for young people to be involved and participate in decision making processes in Ireland.',
        },
        'criterionAllocations': {
            '1(b)': [('Name', 2), ('Explanation', 8)],
            '1(e)': [('First way', 5), ('Second way', 5)],
            '1(k)': [('Name', 2), ('Explanation', 8)],
            '1(l)': [('First piece of information', 5), ('Second piece of information', 5)],
            '1(n)': [('First way', 5), ('Second way', 5)],
            '1(o)': [('First description', 5), ('Second description', 5)],
            '1(p)': [('Name', 2), ('Description', 8)],
            '1(q)': [('Description', 8), ('Example', 2)],
            '1(s)': [('First cause', 5), ('Second cause', 5)],
            '2(c)': [('2024 grade', 5), ('2025 grade', 5)],
        },
        'boundaryNotes': {
            '1(b)': 'A named group and its explanation depend on the same chosen group; retain one task and the explicit 2+8 components.',
            '1(d)': 'Three independently practicable infographic questions, separately priced at 4, 3 and 3; share the original infographic page.',
            '1(k)': 'Naming and explaining the contribution refer to the same freely chosen person, so retain one linked task with 2+8 components.',
            '1(p)': 'Naming and describing refer to the same freely chosen example; retain one task with 2+8 components.',
            '1(q)': 'Definition and example are independently practicable; split and retain rights-holder context.',
            '2(c)': 'The two separately priced retrievals for 2024 and 2025 are independently practicable; split with the document retained.',
            '3(c)': 'Open selection of a piece of evidence, not a finite enumerated route pool.',
            '4(c)': 'Open choice of an issue and project. “Either document” identifies the admissible evidence, not two closed project responses.',
            '5-10': 'The printed “may refer” headings and thinker examples are optional suggestions, not choose-k routes.',
        },
    },
}


def split_task(identity, label, prompt, *criteria):
    return {'id': identity, 'label': label, 'prompt': prompt, 'criteria': list(criteria)}


# These are bounded transcriptions of the selected task, not new questions.
# The original complete question remains available in the source reader.
REVIEWED[2018, 'higher'].update({
    'promptOverrides': {
        '1(a)': 'Name a thinker you have studied who argues that the taking of people’s wealth through taxes is a form of theft.\nName the political philosophy that promotes individual freedom and favours minimising the role of government.',
        '1(i)(i)': 'Give one positive effect of economic globalisation.',
        '1(i)(ii)': 'Give one negative effect of economic globalisation.',
        '3': 'During his campaign for leadership of Fine Gael, May 2017, Leo Varadkar sent this tweet.\n\nIn the context of the serious social issues facing Irish society today, evaluate whether a new social contract is needed in this country.\n\n[Your answer should be supported by examples and evidence and make reference to at least two named theorists you have studied.]',
    },
    'stemOverrides': {'1(i)': ''},
    'splits': {
        '1(a)': [split_task('thinker', 'Thinker', 'Name a thinker you have studied who argues that the taking of people’s wealth through taxes is a form of theft.', 0),
                 split_task('philosophy', 'Political philosophy', 'Name the political philosophy that promotes individual freedom and favours minimising the role of government.', 1)],
        '1(g)': [split_task('advantage', 'Advantage', 'Give one advantage of Proportional Representation (PR) by single transferable vote (STV).', 0),
                 split_task('disadvantage', 'Disadvantage', 'Give one disadvantage of Proportional Representation (PR) by single transferable vote (STV).', 1)],
        '2(c)': [split_task('developed-country', 'Developed country', 'What conclusions can you draw about the human impact, if any, of climate change on a developed country (Document A)?', 0, 1, 2),
                 split_task('developing-country', 'Developing country', 'What conclusions can you draw about the human impact, if any, of climate change on a developing country (Document B)?', 3, 4, 5)],
        '2(d)': [split_task('authorship', 'Authorship', 'Are the claims made in Document A reliable? Justify your answer by referring to the authorship of the report.', 0, 1),
                 split_task('bias', 'Potential bias', 'Are the claims made in Document A reliable? Justify your answer by referring to the potential bias of the report.', 2, 3),
                 split_task('policy-relevance', 'Policy relevance', 'Are the claims made in Document A reliable? Justify your answer by referring to its relevance to policy and decision makers.', 4)],
    },
    'permittedMarks': {'1(a)': {'Thinker': [0, 2], 'Political philosophy': [0, 2]}, '1(k)': {'Thinker': [0, 2]}},
    'alignmentReviews': {
        '1(a)': {'paper': 'taking of people’s wealth through taxes is a form of theft.', 'scheme': 'Robert Nozick', 'reason': 'Rendered p3 asks the taxation thinker and philosophy; scheme p4 gives Nozick and Libertarianism, 2 marks each.'},
        '1(b)': {'paper': 'Is the election process to Seanad Éireann a democratic process?', 'scheme': 'The Seanad has 60 members.', 'reason': 'Paper p3 election explanation and Seanad purpose match the two adjacent 2-mark blocks on scheme p4.'},
        '1(e)': {'paper': 'education in this cartoon?', 'scheme': 'Banking model of education', 'reason': 'Paper p4 cartoon shows the banking model; scheme p6 identifies Freire and the banking model, followed by the required criticism.'},
        '1(h)': {'paper': 'income inequalities in Ireland', 'scheme': 'Two consequences', 'reason': 'Scheme p7 gives poverty, health, education and crime consequences for the two consequences asked on paper p5.'},
        '1(j)': {'paper': 'regulators of the broadcasting media', 'scheme': 'Content regulation: preventing harm to society', 'reason': 'Scheme p8 lists broadcasting regulation challenges corresponding to paper p5.'},
        '1(k)': {'paper': 'women’s work as carers.', 'scheme': 'Kathleen Lynch, Sylvia Walby', 'reason': 'Scheme p9 names the two thinkers and their explanations of undervaluing care, matching both paper p5 asks.'},
        '1(l)': {'paper': 'Brexit referendum', 'scheme': 'Created fear and anger', 'reason': 'Scheme p9 discusses the media impacts of Brexit campaign rhetoric printed on paper p6.'},
    },
})

REVIEWED[2018, 'ordinary'].update({
    'stemOverrides': {
        '1(b)(ii)': 'The European Court of Human Rights is responsible for ensuring the implementation of the European Convention on Human Rights (ECHR).',
        '1(e)': 'Examine the 2016 Census data on migration and diversity in Ireland.',
        '1(o)': 'In 2017 UNESCO published a report on freedom of expression and media development, showing world trends in the safety of journalists. Examine the chart in the original question.',
    },
    'promptOverrides': {
        '1(m)': 'The tweet below is a comment on the absence of media coverage of the ongoing crisis in the Democratic Republic of the Congo, where over 5 million conflict-related deaths have been recorded since 1998.\n\nDo the media have a social responsibility to report on a major crisis such as this one? Give two reasons for your answer.',
        '1(q)': 'Ireland was one of the countries that signed up to the 2016 Paris Climate Agreement, the international agreement to keep the rise in global temperature below 2 degrees Celsius in the 21st century.\n\nSuggest one action that each of the following can take to lessen greenhouse gas emissions in the effort to realise our commitments under the Paris Agreement:\n• Individual action\n• Community action\n• Government action',
        '9': 'Child labour is an example of an extreme denial of a number of children’s rights as outlined in the United Nations Convention on the Rights of the Child (UNCRC).\n\nArticle 28 of the UNCRC states that every child has the right to an education. Primary education must be free. Secondary education must be available to every child. Discipline in schools must respect children’s human dignity. Wealthy countries must help poorer countries achieve this.\nSource: UNICEF\n\nUsing the example of child labour or any other issue relevant to children, discuss the failure to implement Article 28 of the UNCRC around the world.\n\nUse relevant evidence and examples to support your answer.',
    },
    'splits': {
        '1(e)(ii)': [split_task('strength', 'Strength', 'Describe one strength of census data.', 0), split_task('limitation', 'Limitation', 'Describe one limitation of census data.', 1)],
        '1(g)': [split_task('definition', 'Definition', 'Explain what is meant by ‘civil disobedience’.', 0), split_task('example', 'Example', 'Name an example of civil disobedience.', 1)],
        '1(i)': [split_task('definition', 'Definition', 'Explain the term ‘patriarchy’.', 0), split_task('example', 'Example', 'Give an example of patriarchy in society today.', 1)],
        '1(j)': [split_task('definition', 'Definition', 'Explain the term ‘genocide’.', 0), split_task('example', 'Example', 'Describe an example of ‘genocide’.', 1)],
        '1(k)': [split_task('role', 'Role', 'What is the role of civil society bodies or groups in democratic societies?', 0), split_task('example', 'Example', 'Name one of the civil society bodies or groups in democratic societies.', 1)],
        '1(n)': [split_task('definition', 'Definition', 'Explain what it means for a right to be ‘limited’.', 0), split_task('example', 'Example', 'Give an example of a right being ‘limited’.', 1)],
        '1(t)': [
            split_task('statement-1', 'First statement', 'True or false? Ministers of the Executive are nominated by the political parties in the Northern Ireland Assembly.', 0),
            split_task('statement-2', 'Second statement', 'True or false? The number of Ministers which a party can nominate to the Executive Committee is determined by its share of seats in the Assembly.', 1),
            split_task('statement-3', 'Third statement', 'True or false? The First Minister and Deputy First Minister are nominated by the largest and second largest parties respectively.', 2),
        ],
        '3(b)': [split_task('strengths', 'Strengths', 'Describe two strengths of the methodology used in Document A.', 0, 1),
                 split_task('limitations', 'Limitations', 'Describe two limitations of the methodology used in Document A.', 2, 3)],
    },
    'permittedMarks': {'1(f)': {'Complete response': [0, 5]}, '1(k)': {'Name': [0, 2]}, '1(t)': {'First statement': [0, 2], 'Second statement': [0, 2], 'Third statement': [0, 1]}, '2(c)': {'Complete response': [0, 5]}},
    'alignmentReviews': {
        '1(d)': {'paper': 'Name two human rights organisations in Ireland.', 'scheme': 'Two human rights organisation', 'reason': 'Paper p4 naming and description tasks match scheme p5 1+1+3 components.'},
        '1(m)': {'paper': 'social responsibility to report on a major crisis', 'scheme': 'Two reasons for the social responsibility of the media', 'reason': 'Paper p6 Congo reporting question matches the adjacent 3+2-mark social-responsibility block on scheme p7.'},
        '1(q)': {'paper': 'lessen greenhouse gas emissions', 'scheme': 'Actions to lessen greenhouse gas emissions', 'reason': 'Paper p8 individual/community/government actions match scheme p8 heading, allocation and conditional note.'},
        '1(r)': {'paper': 'right to education enjoyed equally', 'scheme': 'Right to education', 'reason': 'Paper p8 asks two reasons and scheme p8 gives the shared 5-mark allocation and transfer condition.'},
        '4(a)': {'paper': 'Does homelessness negatively affect some of the rights of young people', 'scheme': 'Homelessness and children’s rights', 'reason': 'Paper p13 Sophie/homelessness question matches scheme p13 20 content plus 10 cohesion.'},
    },
})

REVIEWED[2026, 'higher']['topicOverrides'] = {'2(b)': '1-9', '2(e)': '1-9'}
REVIEWED[2026, 'higher']['splits'] = {
    '1(k)': [split_task('definition', 'Definition', 'Explain what it means for human rights to be ‘inalienable’.', 0),
             split_task('example', 'Example', 'Give an example of an inalienable right.', 1)],
}
REVIEWED[2026, 'ordinary'].update({
    'stemOverrides': {'1(d)': 'Answer the question on the infographic from the Central Statistics Office: Equality and Discrimination 2024.'},
    'topicOverrides': {'4(c)': '1-1'},
    'splits': {
        '1(q)': [split_task('definition', 'Definition', 'Describe what a rights holder is.', 0), split_task('example', 'Example', 'Give an example of a rights holder.', 1)],
        '2(c)': [split_task('2024', '2024 grade', 'Referring to Document B, what grade was awarded for online safety in 2024?', 0),
                 split_task('2025', '2025 grade', 'Referring to Document B, what grade was awarded for online safety in 2025?', 1)],
    },
    'permittedMarks': {'1(d)(i)': {'Complete response': [0, 4]}, '2(b)': {'Complete response': [0, 10]}, '2(c)': {'2024 grade': [0, 5], '2025 grade': [0, 5]}},
    'alignmentReviews': {'1(h)': {'paper': 'selecting the Northern Ireland Executive', 'scheme': 'The D’Hondt system', 'reason': 'Paper p5 asks how the executive/ministers are selected. Scheme p7 omits the repeated question but identifies D’Hondt, first/deputy ministers and the justice-minister vote.'}},
})

REVIEWED[2019, 'higher'] = {
    'paperPagesReviewed': list(range(1, 25)), 'schemePagesReviewed': list(range(1, 17)),
    'sourcePages': [7, 8], 'shortMarks': 5,
    'shortTopics': '2-1 0-12 2-2 0-0 3-7 2-0 0-7 2-9 2-9 2-5 3-8 0-12'.split(),
    'dataTopics': {'2': '0-6'}, 'dataMarks': {'2': [10, 10, 20, 20, 20, 20, 50]},
    'topicOverrides': {'2(b)': '1-9', '2(c)': '1-9', '2(d)': '1-9', '2(e)': '0-9', '2(g)': '3-7'},
    'essayTopics': {'3(a)': '0-5', '3(b)': '1-2', '4': '3-7', '5': '2-7', '6(a)': '3-1', '6(b)': '3-3'},
    'criterionAllocations': {
        '1(a)': [('Two explanations', 3), ('Absolute-right example', 1), ('Qualified-right example', 1)],
        '1(f)': [('First responsibility', 2), ('Second responsibility', 2), ('Issue', 1)],
        '1(h)': [('Role', 3), ('Aspect', 2)],
        '1(i)': [('First organisation', 1), ('Second organisation', 1), ('Advantage', 3)],
        '1(k)': [('Theory', 1), ('Outline', 3), ('Theorist', 1)],
        '2(c)': [('Positive aspect', 10), ('Negative aspect', 10)],
        '2(g)': [('Discussion', 30), ('Documents, wider learning and contemporary evidence', 20)],
    },
    'promptOverrides': {
        '1(j)': 'What conclusion can you draw from the ESRI data, presented below, about the connection between social class and equality of opportunity in education in Ireland?',
        '4': 'Given the focus on environmental destruction in recent times, discuss whether a consumer’s purchasing choices can address this problem.\n\n[Your answer should include current examples and evidence to support your position. You should also refer to two or more relevant international agreements/organisations* and/or the views of two or more theorists, one of whom must be named on your course.\n\n*Relevant international agreements or organisations include The United Nations Sustainable Development Goals, Paris Climate Agreement, The World Bank, The World Economic Forum, etc.',
        '6(b)': 'The tweet below is a quote from a speech by Simon Coveney, the Tánaiste and Minister for Foreign Affairs and Trade, to the 2018 British Irish Association’s annual conference.\n\nWith particular reference to the border on the island of Ireland, discuss whether borders define identity.\n\n[Your answer should include examples and evidence from a local and/or global context to support your argument. You should also refer to the views of two theorists you have studied, at least one of whom must be named on your course.]',
    },
    'splits': {
        '1(a)': [split_task('definitions', 'Definitions', 'Explain what is meant when human rights are described as absolute rights and qualified rights.', 0),
                 split_task('absolute-example', 'Absolute-right example', 'Give an example of an absolute right.', 1),
                 split_task('qualified-example', 'Qualified-right example', 'Give an example of a qualified right.', 2)],
        '1(h)': [split_task('role', 'Role', 'Explain the role of the International Monetary Fund (IMF).', 0),
                 split_task('aspect', 'Aspect', 'Describe one positive or one negative aspect of the IMF’s role in the world.', 1)],
        '2(c)': [split_task('positive', 'Positive aspect', 'Give one positive aspect of the authorship of Document B.', 0),
                 split_task('negative', 'Negative aspect', 'Give one negative aspect of the authorship of Document B.', 1)],
    },
    'finiteRoutes': {
        '1(h)#aspect': {'cue': 'one positive or one negative aspect', 'choose': 1,
                       'pool': [('positive', 'positive'), ('negative', 'negative')],
                       'prompt': 'Describe one {selection} aspect of the IMF’s role in the world.'},
        '6(a)': {'cue': 'either Benedict Anderson or Thomas Hylland Eriksen', 'choose': 1,
                 'pool': [('anderson', 'Benedict Anderson'), ('eriksen', 'Thomas Hylland Eriksen')],
                 'prompt': 'In 2018, 200 residents in Wicklow opposed the transformation of the Grand Hotel into a Direct Provision centre which aimed to house 100 refugees.\n\nDiscuss the above incident with particular reference to the ideas of {selection}. Your answer should also include examples and evidence to support your position.'},
    },
    'boundaryNotes': {
        '1(a)': 'First accurate explanation gets 2, the next 1: retain the two definitions under their shared 3-mark tariff. Each example has its own independent 1-mark tariff.',
        '1(b)': 'The cartoon or any other challenge is an open example choice, not a finite printed menu.',
        '1(d)': 'Alternative positions in an evaluative question do not prescribe distinct examination routes; the student justifies a position.',
        '1(e),1(g)': 'The 3+2 tariff permits transfer to the second response; retain the shared 5-mark task.',
        '1(f),1(i),1(k)': 'Later descriptions refer to the candidate’s selected responsibilities, organisation or theory. Keep the dependent response with its explicit components.',
        '1(h)': 'Role and evaluation have separate 3+2 tariffs. Split; expand the explicit positive-or-negative choice within the 2-mark task into two routes.',
        '2(c)': 'Positive and negative authorship assessments have independent 10-mark tariffs; split.',
        '2(g)': 'Discussion and use of evidence assess the same argument; retain one 50-mark response.',
        '3,6': 'Each printed lettered essay alternative is a separate 100-mark route.',
        '4,5,6(b)': 'Required evidence and illustrative agreements/theorists allow open supporting material and geographic contexts; they do not offer a closed set of essay subjects.',
        '6(a)': 'Explicit choice of two named thinkers: mechanically expand two distinct 100-mark essay routes.',
    },
}

REVIEWED[2019, 'ordinary'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 21)),
    'sourcePages': [9, 10], 'shortMarks': 5,
    'shortMarkNote': REVIEWED[2018, 'ordinary']['shortMarkNote'],
    'shortTopics': '0-4 0-9 0-9 3-7 0-5 2-9 2-1 0-4 3-1 3-3 3-7 0-4 0-6 0-6 0-9 3-5 0-6 2-10 1-2 0-5 3-1'.split(),
    'partMarks': {'1(u)(i)': 1, '1(u)(ii)': 2, '1(u)(iii)': 2},
    'mergeParts': ['2(e)'],
    'dataTopics': {'2': '2-7', '3': '1-9', '4': '2-7'},
    'dataMarks': {'2': [5, 5, 5, 10, 15], '3': [5, 5, 15, 10, 15], '4': [20, 20, 20]},
    'topicOverrides': {'1(u)(i)': '1-9', '1(u)(iii)': '1-9', '4(b)': '3-7', '4(c)': '1-1'},
    'essayTopics': {'5': '3-3', '6': '1-0', '7': '0-5', '8': '0-0', '9': '0-9', '10': '2-10'},
    'criterionAllocations': {
        '1(e)': [('First department', 1), ('Second department', 1), ('Work', 3)],
        '1(j)': [('Explanation', 3), ('Example', 2)],
        '1(o)': [('First reason', 2), ('Second reason', 2), ('Third reason', 1)],
        '1(r)': [('Conclusion', 3), ('Advantage', 1), ('Disadvantage', 1)],
        '1(u)(iii)': [('Advantage', 1), ('Disadvantage', 1)],
        '2(d)': [('First reason', 5), ('Second reason', 5)],
        '2(e)': [('Five rights', 5), ('First description', 5), ('Second description', 5)],
        '3(c)': [('First piece of information', 5), ('Second piece of information', 5), ('Description', 5)],
        '3(d)': [('First reason', 5), ('Second reason', 5)],
        '3(e)': [('First advantage', 5), ('Second advantage', 5), ('Disadvantage', 5)],
        '4(c)': [('Action', 5), ('Rationale', 5), ('Description', 5), ('Aims', 5)],
    },
    'promptOverrides': {
        '1(b)': 'Describe two points this image is making about the media. Do you agree with the warning given in this image? Give two reasons for your answer.',
        '1(i)': 'Does this cartoon explain ‘cosmopolitan culture’? Give two reasons for your answer.',
        '2(e)': 'Using the evidence from Document B identify five human rights being denied to Walaa. Describe how two of these human rights are being denied to Walaa.',
        '5': 'We live in world of imagined communities which has a significant impact on how people interact with each other.\n\nDiscuss the idea of ‘us and them’ in relation to recent national and global events.\n\nYou may be able to draw on the following images in your answer.',
        '10': 'The 70th Anniversary of the adoption by the United Nations General Assembly of the Universal Declaration of Human Rights (UDHR) was celebrated on the 10th of December 2018.\n\n70 years later, discuss whether human rights are being protected and promoted in Ireland or is Ireland failing to meet its human rights obligations?\n\nYou may be able to draw on the following image in your answer.',
    },
    'stemOverrides': {'1(u)': 'Examine the 2016 data on Irish Travellers.'},
    'splits': {
        '1(j)': [split_task('definition', 'Definition', 'What is inter-ethnic violence?', 0), split_task('example', 'Example', 'Give one current example of inter-ethnic violence in our world.', 1)],
        '1(r)': [split_task('conclusion', 'Conclusion', 'Looking at the pie-chart below, would you conclude that there is a homelessness problem in Ireland? Justify your answer.', 0),
                 split_task('advantage', 'Advantage', 'Describe one advantage of presenting homelessness data in this way.', 1),
                 split_task('disadvantage', 'Disadvantage', 'Describe one disadvantage of presenting homelessness data in this way.', 2)],
        '1(u)(iii)': [split_task('advantage', 'Advantage', 'Describe one advantage of census data.', 0), split_task('disadvantage', 'Disadvantage', 'Describe one disadvantage of census data.', 1)],
        '3(e)': [split_task('advantages', 'Advantages', 'Document A is produced by the United Nations. Name two advantages of UN agencies gathering, analysing and publishing research.', 0, 1),
                 split_task('disadvantage', 'Disadvantage', 'Document A is produced by the United Nations. Name one disadvantage of UN agencies gathering, analysing and publishing research.', 2)],
    },
    'finiteRoutes': {
        '2(d)': {'cue': 'Give two of these reasons.', 'choose': 2,
                 'pool': [('first', 'first reason'), ('second', 'second reason'), ('third', 'third reason')],
                 'prompt': 'Document B gives the reasons why the family have had to move twice in three months. Give the {selection} in the sentence explaining these moves.',
                 'sourceEvidence': {'page': 10, 'text': "the houses are too expensive here and my parents cannot afford the rent, as our parents can't work here"}},
        '4(c)': {'cue': 'at local or national or international level', 'choose': 1,
                 'pool': [('local', 'local'), ('national', 'national'), ('international', 'international')],
                 'prompt': 'Identify and describe a citizenship project that responds to the needs of refugee populations at {selection} level.\n\nAction · Rationale · Description · Aims'},
    },
    'permittedMarks': {'1(j)': {'Example': [0, 2]}, '2(a)': {'Complete response': [0, 3, 5]}, '2(b)': {'Complete response': [0, 5]}, '2(c)': {'Complete response': [0, 5]}},
    'boundaryNotes': {
        'Section A': 'The paper prints 21 items, a–u. The scheme introduction says 20 but then marks every item through u. Retain all 21; the introductory count is a source inconsistency.',
        '1(b),1(d),1(f),1(g),1(i),1(k),1(l),1(p),1(t)': 'Published shared-cap or conditional 3+2 allocations: keep each 5-mark response and its exact transfer guidance.',
        '1(e)': 'Description depends on a government department named by the candidate; preserve the linked 1+1+3 components.',
        '1(j),1(r),1(u)': 'Split independently priced definition/example, conclusion/advantage/disadvantage, and census subparts respectively.',
        '2(a)': 'Ordered allocation gives 3 for the first correct country and 2 for the second; two retrievals stay together because country-specific marks are not fixed.',
        '2(d)': 'Document B prints three reasons and the task requires two of those: expand the three combinations mechanically, each worth 10.',
        '2(e)': 'Roman i–v label blank answer slots, not five extra tasks. The two descriptions refer to rights selected by the candidate; keep the linked 15-mark task.',
        '3(c)': 'Open selection of two pieces of information from the infographic, not an enumerated finite answer menu. Their linked description stays with them.',
        '3(e)': 'Two advantages and one disadvantage have independent 10+5 tariffs; split.',
        '4(a)': 'The opening says Document A, but Walaa’s statement is on Document B, which the same question then explicitly directs the student to use. Retain the paper wording and both documents.',
        '4(c)': 'The project has four linked 5-mark components. Expand the three explicitly offered project levels, retaining all components on every route.',
        '5-10': 'Optional images, words, prompts and examples are supporting suggestions, not closed choose-k tasks. And/or level wording remains flexible.',
    },
}

# Positional-only pairings were read against the complete rendered pages.
# The 2019 schemes often print only “Valid explanation”, so semantic overlap
# cannot establish these matches. Pin both source cues and the review reason.
REVIEWED[2019, 'higher']['alignmentReviews'] = {
    '1(a)': {'paper': 'absolute rights and qualified rights', 'scheme': 'Two accurate explanations', 'reason': 'Paper p3 has two definitions and two examples; the first scheme p4 block prices precisely those four required elements.'},
    '1(b)': {'paper': 'challenges currently facing the European Union', 'scheme': 'One accurate description of a challenge facing the EU', 'reason': 'Paper p3 EU cartoon question matches scheme p4 EU challenges block.'},
    '1(d)': {'paper': 'Are school uniforms socially divisive', 'scheme': 'Relevant argument', 'reason': 'Paper p4 school-uniform question is the fourth item. Scheme p4 fourth block has its 5-mark argument grid, immediately after Equal Status Acts and before climate actions.'},
    '1(e)': {'paper': 'stem the flow of climate migration', 'scheme': 'Two descriptions of relevant actions', 'reason': 'Paper p4 asks two actions; scheme p5 first block prices the same paired response, with its transfer note.'},
    '1(f)': {'paper': 'upholding the United Nations Convention on the Rights of the Child', 'scheme': 'Ireland signed up to the UNCRC in 1992', 'reason': 'Paper p5 responsibilities and issue match scheme p5 2+2+1 block with the explicit UNCRC explanation.'},
    '1(h)': {'paper': 'International Monetary Fund (IMF)', 'scheme': 'One positive or one negative aspect', 'reason': 'Paper p5 role plus chosen aspect is the eighth item; scheme p5 final block separately prices explanation 3 and positive/negative aspect 2.'},
    '1(k)': {'paper': 'theories as to why some countries remain underdeveloped', 'scheme': 'Named theory of development', 'reason': 'Paper p6 theory, outline and theorist match the three named scheme p6 components at 1+3+1.'},
}

REVIEWED[2019, 'ordinary']['alignmentReviews'] = {
    '1(b)': {'paper': 'image is making about the media', 'scheme': 'Two valid points', 'reason': 'Paper p3 second item is the media image. Scheme p4 second block prices its paired points at a shared 5, between Ceann Comhairle and press freedom.'},
    '1(c)': {'paper': 'freedom of the press', 'scheme': 'Valid explanation', 'reason': 'Paper p3 third item and scheme p4 third block have the same printed c identity; the complete surrounding a–d run was visually checked.'},
    '1(d)': {'paper': 'combat climate change in your community', 'scheme': 'Two valid actions', 'reason': 'Paper p4 first item asks two actions; scheme p4 final block prices two actions under its shared 5-mark tariff.'},
    '1(g)': {'paper': 'difference between civil and political rights', 'scheme': 'Two valid points', 'reason': 'Paper p4 item g follows the supranational-body question. Scheme p5 final block is g and has a shared 3+2 tariff; preceding e and f identities were verified.'},
    '1(h)': {'paper': 'role of the civil service in Ireland', 'scheme': 'Valid description', 'reason': 'Paper p4 item h is the civil-service role. Scheme p6 first block is h and has one 5-mark description grid; adjoining g and i positions match.'},
    '1(i)': {'paper': 'cosmopolitan culture', 'scheme': 'Two valid reasons', 'reason': 'Paper p5 cartoon asks two reasons; scheme p6 second block prices those reasons at a shared 5.'},
    '1(j)': {'paper': 'inter‐ethnic violence', 'scheme': 'Valid example', 'reason': 'Paper p5 definition and example match the two distinct 3+2 allocations in scheme p6 item j.'},
    '1(m)': {'paper': 'Explain the term ‘social class’', 'scheme': 'Valid explanation', 'reason': 'Paper p6 item m and scheme p7 first block were read in the complete lettered run; the scheme has only this generic cue and a 5-mark grid.'},
    '1(n)': {'paper': 'social class may affect the experiences of young people', 'scheme': 'Valid description', 'reason': 'Paper p6 item n and scheme p7 second block were matched visually between social-class definition and social-media reasons.'},
    '1(o)': {'paper': 'three reasons why politicians use social media', 'scheme': 'Three valid reasons', 'reason': 'Paper p6 three reasons match scheme p7 2+2+1 block.'},
    '1(p)': {'paper': 'processes currently contributing to making our world increasingly globalised', 'scheme': 'Two valid descriptions', 'reason': 'Paper p6 paired globalisation processes match scheme p7 item p, with a shared 5-mark cap and transfer rule.'},
    '1(q)': {'paper': 'one example of patriarchy', 'scheme': 'Description of one valid example', 'reason': 'Paper p6 item q asks one example; scheme p7 item q gives its 5-mark descriptive grid.'},
    '1(s)': {'paper': 'What point is Taoiseach Leo Varadkar making', 'scheme': 'One valid point', 'reason': 'Paper p7 headline item s matches scheme p8 first block s at 5 marks; adjacent r and t were checked.'},
    '1(t)': {'paper': 'selection of the Northern Ireland Executive', 'scheme': 'Two valid pieces of information', 'reason': 'Paper p8 item t asks two pieces; scheme p8 second block t prices them under its shared 5-mark cap.'},
    '2(d)': {'paper': 'family have had to move twice in three months', 'scheme': 'Houses are too expensive', 'reason': 'Document B p10 and paper p11 match the three source reasons named by scheme p9, any two priced at 5+5.'},
    '3(b)': {'paper': 'limitation of quantitative data', 'scheme': 'Valid description', 'reason': 'Paper p12 second data-analysis task matches scheme p10 second block b, a 5-mark description grid.'},
    '3(d)': {'paper': 'Is Document B a reliable source of data', 'scheme': 'Two valid reasons', 'reason': 'Paper p12 fourth task asks two reliability reasons; scheme p10 fourth block d prices them at 5+5.'},
    '4(a)': {'paper': 'we are old people in children’s bodies', 'scheme': 'Explanation of the statement with reference to Document B', 'reason': 'Paper p13 first question quotes Walaa; scheme p11 first block explicitly refers to the statement and Document B, 20 marks.'},
}

REVIEWED[2019, 'higher']['permittedMarks'] = {'1(a)': {'Two explanations': [0, 2, 3]}}
for key in ['4(a)', '4(b)']:
    REVIEWED[2019, 'ordinary']['permittedMarks'][key] = {'Complete response': [*range(15), *range(16, 21)]}
    REVIEWED[2019, 'ordinary'].setdefault('markNotes', {})[key] = 'The printed SEC descriptor table lists 0–5, 6–10, 11–14 and 16–20. It omits 15; the practice selector follows those printed ranges. The question total remains 20.'

# Independent totals recorded from the paper/mark-scheme boundary review.
# These are not filled from the extractor or from generated deck lengths.
REVIEWED[2018, 'higher']['reviewedTaskCounts'] = {'A': 16, 'B': 9, 'C': 6}
REVIEWED[2018, 'ordinary']['reviewedTaskCounts'] = {'A': 31, 'B': 14, 'C': 6}
REVIEWED[2019, 'higher']['reviewedTaskCounts'] = {'A': 16, 'B': 8, 'C': 7}
REVIEWED[2019, 'ordinary']['reviewedTaskCounts'] = {'A': 27, 'B': 18, 'C': 6}
REVIEWED[2026, 'higher']['reviewedTaskCounts'] = {'A': 16, 'B': 7, 'C': 6}
REVIEWED[2026, 'ordinary']['reviewedTaskCounts'] = {'A': 23, 'B': 15, 'C': 6}

REVIEWED[2020, 'higher'] = {
    'paperPagesReviewed': list(range(1, 25)), 'schemePagesReviewed': list(range(1, 14)),
    'sourcePages': [7, 8], 'shortMarks': 5,
    'shortTopics': '0-4 1-9 3-1 0-9 0-12 0-12 0-5 2-1 2-7 0-6 3-7 3-3'.split(),
    'dataTopics': {'2': '2-2'}, 'dataMarks': {'2': [10, 10, 20, 20, 20, 20, 50]},
    'topicOverrides': {'2(a)': '1-9', '2(c)': '1-9', '2(d)': '1-9', '2(e)': '1-9'},
    'essayTopics': {'3(a)': '2-0', '3(b)': '3-7', '4': '0-4', '5': '0-12', '6(a)': '0-6', '6(b)': '0-6'},
    'criterionAllocations': {
        '1(a)': [('First piece of information', 2), ('Second piece of information', 2), ('Argument', 1)],
        '1(h)': [('Explanation', 3), ('Example', 2)],
        '1(l)': [('Theorist', 1), ('Outline', 4)],
        '2(a)': [('Positive aspect', 5), ('Negative aspect', 5)],
        '2(b)': [('First reason', 5), ('Second reason', 5)],
        '2(c)': [('Positive aspect', 10), ('Negative aspect', 10)],
        '2(f)': [('Socio-economic circumstances', 10), ('Daily challenges', 10)],
        '2(g)': [('Discussion', 30), ('Documents and wider learning', 20)],
    },
    'promptOverrides': {
        '1(b)': 'The 2019 Annual Report published by The European Union Agency for Fundamental Human Rights found that racist harassment and violence is common in the EU but remains invisible in official statistics.\n\nGive two reasons to explain why official statistics are not capturing this data.',
        '1(i)': 'Describe two key elements of the United Nations Declaration on the Right to Development?',
        '3(a)': 'In September 2019, 16-year-old climate activist Greta Thunberg and 15 other young people from around the world filed a legal complaint under the 1989 UN Convention on the Rights of the Child against five countries with some of the worst greenhouse gas emissions.\n\nThe youth activists allege that those governments’ lack of action to combat climate change violates their rights as children.\n\nCritically evaluate the relationship between children’s rights and the climate emergency.',
        '3(b)': 'This was an advertisement for Boerum Apparel, an American-based company that manufactured clothing using fully traceable raw materials and sold humane, sustainable, socially responsible clothing.\n\nThe founder of Boerum Apparel, Teel Lidow created this clothing company with a fully transparent supply chain because he believed that the fashion-conscious now had a conscience.\n\nWhether through positive buying or moral boycott, does ethical consumerism by informed global citizens have the power to end global poverty?\n\n[Your answer should include contemporary examples and evidence to support your argument. You should also refer to the ideas of at least two theorists you have studied one of whom must be named on your course and/or refer to two or more relevant international agreements/organisations (e.g. United Nations Sustainable Development Goals, Paris Climate Agreement 2016, the World Bank, etc.]',
        '5': 'As a function of the social contract the state has a responsibility to ensure the safety of its citizens.\n\nConsequently, should the state spend more money on policing and tackling crime, while spending less on other areas such as housing and social welfare?\n\n[Your answer should include contemporary examples and evidence to support your position. You should also refer to the views of at least two theorists you have studied one of which must be named on your course.]',
        '6(a)': 'According to new research published in 2019 by the Irish Human Rights and Equality Commission and the Economic and Social Research Institute (ESRI), 45% of women and 29% of men provide care for others on a daily basis (childcare and/or adult care).\n\nAccording to journalist Orla O’Connor: ‘The fact that women spend a disproportionate amount of time carrying out unpaid work compared to men has serious economic and social consequences that ultimately lead to a gender gap in pay and in poverty.’\nSource: The Irish Times, January, 2019\n\nCritically assess the view that as long as women in Ireland continue to do unpaid work and care for children and family members, discrimination and gender pay gaps will exist.\n\n[Your answer should include contemporary examples and evidence from a local and/or national context to support your argument. You should also refer to the ideas of at least two theorists you have studied one of which must be named on your course.]',
    },
    'splits': {
        '1(a)': [split_task('role', 'Role', 'Give two pieces of information about the role of the Party Whip of a political party.', 0, 1),
                 split_task('argument', 'Argument', 'Give one argument in favour or against the party whip system.', 2)],
        '1(h)': [split_task('explanation', 'Explanation', 'Explain what it means for states to agree to act to implement rights ‘to the maximum extent of their available resources.’', 0),
                 split_task('example', 'Irish example', 'Describe an Irish example of states agreeing to act to implement rights ‘to the maximum extent of their available resources.’', 1)],
        '2(a)': [split_task('positive', 'Positive aspect', 'Critique one positive aspect of the use of quota sampling in Document B.', 0),
                 split_task('negative', 'Negative aspect', 'Critique one negative aspect of the use of quota sampling in Document B.', 1)],
        '2(c)': [split_task('positive', 'Positive aspect', 'Critique one positive aspect of the presentation of the data in Document B.', 0),
                 split_task('negative', 'Negative aspect', 'Critique one negative aspect of the presentation of the data in Document B.', 1)],
        '2(f)': [split_task('circumstances', 'Socio-economic circumstances', 'Comparing the data in both documents what conclusions would you draw about the socio-economic circumstances of persons with disabilities?', 0),
                 split_task('challenges', 'Daily challenges', 'Comparing the data in both documents what conclusions would you draw about the challenges persons with disabilities face in their daily lives?', 1)],
    },
    'finiteRoutes': {
        '1(a)#argument': {'cue': 'one argument in favour or against', 'choose': 1,
                          'pool': [('favour', 'in favour of'), ('against', 'against')],
                          'prompt': 'Give one argument {selection} the party whip system.'},
        '1(g)': {'cue': 'retained, abolished or reformed', 'choose': 1,
                 'pool': [('retained', 'retained'), ('abolished', 'abolished'), ('reformed', 'reformed')],
                 'prompt': 'Should Seanad Éireann be {selection}? Give two reasons for your opinion.'},
    },
    'boundaryNotes': {
        '1(a)': 'Role information has a distinct 4-mark allocation. Split the 1-mark argument and expand its explicit in-favour/against choice into two routes.',
        '1(b),1(c),1(f),1(g),1(i),1(j),1(k)': 'Two descriptions/reasons have a shared 5-mark cap with conditional transfer; keep each pair together.',
        '1(g)': 'Three printed checkboxes explicitly require choosing retained, abolished or reformed. Expand all three 5-mark routes.',
        '1(h)': 'Explanation and Irish example have independent 3+2 tariffs; split with the maximum-resources principle preserved.',
        '1(l)': 'The outline depends on the named theorist; keep the 1+4 components together. The paper supplies no closed list of theorists.',
        '2(a),2(c)': 'Required positive and negative critiques have independently priced tariffs, 5+5 and 10+10; split.',
        '2(f)': 'Socio-economic circumstances and daily challenges have separate 10-mark allocations; split with both documents.',
        '2(g)': 'Discussion and document use assess one argument; retain the combined 50 marks.',
        '3,6': 'All printed essay alternatives are separate 100-mark routes.',
        '3(b)': 'Whether through positive buying or moral boycott describes the scope of the ethical-consumerism argument, not an instruction to select one route. And/or supporting theorists/agreements remain flexible.',
        '4,6(b)': 'These are evaluative questions inviting a justified conclusion, not closed selection menus.',
    },
    'reviewedTaskCounts': {'A': 17, 'B': 10, 'C': 6},
}

REVIEWED[2020, 'higher']['alignmentReviews'] = {
    '1(b)': {'paper': 'official statistics are not capturing this data', 'scheme': 'Two accurate reasons to explain the statistics', 'reason': 'Paper p3 item b asks two reasons for missing racist-harassment data. Scheme p4 item b, between Party Whip and border controls, has the matching paired-response tariff and transfer rule.'},
    '1(g)': {'paper': 'Should Seanad Éireann be retained, abolished or reformed', 'scheme': 'Two relevant reasons supporting option chosen', 'reason': 'Paper p5 checkboxes require a selected option and two reasons. Scheme p5 item g explicitly prices the two reasons supporting that option.'},
    '1(h)': {'paper': 'to the maximum extent of their available resources', 'scheme': 'Valid example', 'reason': 'Paper p5 explanation and Irish example match scheme p5 final block h: 3 for the explanation and 2 for the example.'},
    '1(i)': {'paper': 'United Nations Declaration on the Right to Development', 'scheme': 'Two accurately described elements of the UNDRD', 'reason': 'Paper p5 full title matches the scheme p6 acronym and its two-element 5-mark allocation.'},
    '1(j)': {'paper': 'increase women’s participation in the world of business', 'scheme': 'Two accurately described initiatives', 'reason': 'Paper p6 first item j asks two initiatives. Scheme p6 second block j gives the paired-initiative grid between UNDRD and the Utrecht initiative.'},
}

REVIEWED[2021, 'higher'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 17)),
    'sourcePages': [8, 9], 'shortMarks': 5,
    'shortTopics': '0-5 0-6 0-7 0-8 1-9 3-5 3-5 3-8 2-5 0-5 3-8 2-10 3-7 0-8 2-2'.split(),
    'dataTopics': {'2': '0-9'}, 'dataMarks': {'2': [10, 10, 20, 20, 20, 20, 50]},
    'topicOverrides': {'2(a)': '1-9', '2(b)': '1-9', '2(c)': '1-9'},
    'essayTopics': {'3': '0-12', '4(a)': '3-8', '4(b)': '2-7', '5': '3-3', '6': '2-3', '7': '0-6'},
    'criterionAllocations': {'2(c)': [('Positive aspect', 10), ('Negative aspect', 10)], '2(g)': [('Evaluation', 30), ('Use of documents', 20)]},
    'promptOverrides': {'2(g)': 'Drawing on both documents, evaluate the necessity for a campaign such as this about misinformation.\n\nExamine the Ireland at UN campaign in the original question.'},
    'splits': {'2(c)': [split_task('positive', 'Positive aspect', 'Critique one positive aspect of the use of multiple sources for statistics as used in Document B.', 0), split_task('negative', 'Negative aspect', 'Critique one negative aspect of the use of multiple sources for statistics as used in Document B.', 1)]},
    'boundaryNotes': {
        '1(a),1(d),1(g),1(h),1(l),1(n),1(o)': 'Each paired response has a shared 5-mark cap with conditional transfer from the first 3-mark point to the second. Keep the whole response and its transfer guidance.',
        '1(h)': 'Development aid and/or debt relief is flexible support, not a fixed number of choices.',
        '2(c)': 'Scheme p8 independently prices positive and negative aspects at 10 marks each; split.',
        '2(g)': 'Evaluation and document use assess one argument, 30+20; keep together with the p12 campaign graphic.',
        '4': 'Both printed essay alternatives are separate 100-mark routes.',
        '3,4,6,7': 'Two theorists must be selected from the open course domain, not a closed printed menu. The and/or agreements wording in 4(a) is flexible support.',
    },
    'reviewedTaskCounts': {'A': 15, 'B': 8, 'C': 6},
}

REVIEWED[2021, 'ordinary'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 21)),
    'sourcePages': [9, 10], 'shortMarks': 10,
    'shortTopics': '0-4 0-6 0-6 0-10 1-9 0-4 0-5 0-7 2-9 1-9 1-8 2-9 3-4 0-5 0-12 2-2 1-9 0-7 2-0 3-7'.split(),
    'partMarks': {'1(q)(i)': 2, '1(q)(ii)': 4, '1(q)(iii)': 4},
    'dataTopics': {'2': '2-10', '3': '1-9', '4': '2-2'},
    'dataMarks': {'2': [5, 5, 15, 5, 20], '3': [10, 10, 10, 10, 10], '4': [10, 10, 20, 20]},
    'topicOverrides': {'1(c)#capitalism': '0-6', '1(f)#role-ngo': '2-4', '1(f)#function-ngo': '2-4', '1(f)#role-statutory': '2-4', '1(f)#function-statutory': '2-4', '2(e)': '2-5', '4(a)': '1-1', '4(b)': '3-1', '4(c)': '0-6'},
    'essayTopics': {'5': '0-9', '6': '2-2', '7': '3-7', '8': '3-5', '9': '0-5', '10': '2-5'},
    'criterionAllocations': {
        '1(a)': [('First department', 3), ('Second department', 3), ('Minister of one named department', 4)],
        '1(b)': [('First strategy', 5), ('Second strategy', 5)],
        '1(d)': [('Theory of government', 8), ('Thinker', 2)],
        '1(f)': [('Role', 5), ('Function', 5)],
        '1(h)': [('Conclusion', 5), ('Reason', 5)],
        '1(i)': [('First treaty or convention', 5), ('Second treaty or convention', 5)],
        '1(j)': [('First way', 5), ('Second way', 5)],
        '1(l)': [('First acronym', 2), ('Second acronym', 2), ('Third acronym', 2), ('Fourth acronym', 2), ('Fifth acronym', 2)],
        '1(o)': [('First opinion', 5), ('Second opinion', 5)],
        '1(q)(ii)': [('Advantage', 2), ('Disadvantage', 2)],
        '1(q)(iii)': [('First observation', 2), ('Second observation', 2)],
        '1(s)': [('First reason', 5), ('Second reason', 5)],
        '1(t)': [('First action', 5), ('Second action', 5)],
        '2(c)': [('First reason from Document A', 5), ('Second reason from Document A', 5), ('Third reason from Document A', 5)],
        '2(e)': [('First reason', 10), ('Second reason', 10)],
        '3(a)': [('First reason', 5), ('Second reason', 5)],
        '3(c)': [('First reason', 5), ('Second reason', 5)],
        '3(d)': [('First linked piece of information', 5), ('Second linked piece of information', 5)],
        '3(e)': [('Advantage', 5), ('Disadvantage', 5)],
    },
    'permittedMarks': {
        '1(a)': {'First department': [0, 3], 'Second department': [0, 3], 'Minister of one named department': [0, 4]},
        '1(d)': {'Thinker': [0, 2]},
        '1(l)': {label + ' acronym': [0, 2] for label in ['First', 'Second', 'Third', 'Fourth', 'Fifth']},
        '1(q)(i)': {'Complete response': [0, 2]},
        '2(a)': {'Complete response': [0, 5]}, '2(b)': {'Complete response': [0, 5]}, '2(d)': {'Complete response': [0, 5]},
    },
    'stemOverrides': {'1(q)': 'Examine the Central Statistics Office graphic on respondents’ views of the current Level 5 response to managing COVID-19 in the original question.'},
    'splits': {
        '1(d)': [split_task('theory', 'Theory of government', 'Explain the theory of government in this image.', 0), split_task('thinker', 'Thinker', 'Name the thinker associated with the theory of government in this image.', 1)],
        '1(f)': [split_task('role', 'Role', 'Explain the role of one of the following: Civil service; Non-governmental organisations; Statutory bodies.', 0), split_task('function', 'Function', 'Explain the function of one of the following: Civil service; Non-governmental organisations; Statutory bodies.', 1)],
        '1(q)(ii)': [split_task('advantage', 'Advantage', 'Give one advantage of surveying people’s opinions.', 0), split_task('disadvantage', 'Disadvantage', 'Give one disadvantage of surveying people’s opinions.', 1)],
        '3(e)': [split_task('advantage', 'Advantage', 'Both Documents A and B are extracts from larger documents. Name one advantage of using extracts like these.', 0), split_task('disadvantage', 'Disadvantage', 'Both Documents A and B are extracts from larger documents. Name one disadvantage of using extracts like these.', 1)],
    },
    'finiteRoutes': {
        '1(c)': {'cue': 'Explain one of the following three terms:', 'choose': 1, 'pool': [('capitalism', 'Capitalism'), ('social-class', 'Social class'), ('patriarchy', 'Patriarchy')], 'prompt': 'Explain the following term: {selection}.'},
        '1(f)#role': {'cue': 'Explain the role and function of one of the following:', 'choose': 1, 'pool': [('civil-service', 'the Civil service'), ('ngo', 'Non-governmental organisations'), ('statutory', 'Statutory bodies')], 'prompt': 'Explain the role of {selection}.'},
        '1(f)#function': {'cue': 'Explain the role and function of one of the following:', 'choose': 1, 'pool': [('civil-service', 'the Civil service'), ('ngo', 'Non-governmental organisations'), ('statutory', 'Statutory bodies')], 'prompt': 'Explain the function of {selection}.'},
        '1(l)': {'cue': 'Write out in full five of the following acronyms:', 'choose': 5, 'pool': [(s.lower(), s) for s in ['UNCRC', 'EU', 'IHREC', 'IMF', 'UN', 'UDHR', 'WHO', 'ECHR', 'WTO']], 'prompt': 'Write out in full these five acronyms: {selection}.'},
    },
    'markNotes': {
        '2(c)': 'The scheme gives three reasons at 5 marks each. Its individual allocations sum to 50 for Question 2, despite the 40-mark question heading. This card follows the explicit 15-mark allocation.',
        '2(e)': 'The scheme explicitly gives two reasons at 10 marks each. Question 2’s allocations total 50, despite its 40-mark heading; the section allocations consequently total 160, despite its 150-mark heading. This card follows the published 20-mark task allocation.',
    },
    'boundaryNotes': {
        '1(a)': 'The minister must head one of the candidate’s named departments: keep the dependent 3+3+4 response. Preserve the historical 2021 scheme.',
        '1(c)': 'One of three printed terms: expand three 10-mark routes.',
        '1(d)': 'The image fixes the theory and thinker; independently priced 8+2 tasks, split with the image retained.',
        '1(f)': 'Role and function have independent 5-mark allocations. Split first, then expand the three printed organisations inside each task: six 5-mark cards.',
        '1(h)': 'The reason must justify the candidate’s own conclusion: retain the linked 5+5 response.',
        '1(l)': 'Closed choose-five-of-nine pool. Generate all C(9,5)=126 ten-mark routes, each retaining five 2-mark acronym criteria.',
        '1(q)': 'Printed roman parts independently priced 2,4,4. Further split ii into its 2-mark advantage and 2-mark disadvantage.',
        '1(b),1(i),1(j),1(o),1(s),1(t)': 'Required pairs from an open domain, not a fixed printed pool. Retain each requested pair with both marking criteria.',
        '2(c)': 'The paper does not print a number or closed reason menu; scheme requires three freely identified reasons from a narrative. Retain one response with the published 3x5 allocation.',
        '3(d)': 'Choose two pieces from a continuous interview: open evidence selection, not a closed enumerated pool.',
        '3(e)': 'Separate 5-mark advantage and disadvantage; split.',
        '5-10': 'May-use/may-draw-on suggestions are optional support. Q7 permits one or more actors, not a fixed finite selection. Do-you-agree is an evaluative conclusion, not a printed menu.',
        'section-headings': 'Scheme p9 Q2 allocations total 50 rather than its 40 heading, making B total 160 rather than 150. Scheme p12 says Section C 150, while paper C is 100 for two 50-mark essays. Preserve individual published tariffs and record these discrepancies.',
    },
    'reviewedTaskCounts': {'A': 156, 'B': 15, 'C': 6},
}

REVIEWED[2021, 'higher']['alignmentReviews'] = {
    '2(g)': {'paper': 'evaluate the necessity for a campaign', 'scheme': 'Evaluation of the need for a campaign such as #Pledge to Pause.', 'reason': 'Paper p12 presents the UN #PledgetoPause campaign; scheme p9 final block prices the matching campaign evaluation 30 plus documents 20.'},
}
REVIEWED[2021, 'ordinary']['alignmentReviews'] = {
    '1(c)': {'paper': 'Explain one of the following three terms:', 'scheme': 'Valid explanation of one term.', 'reason': 'Paper p3 term menu directly corresponds to scheme p5 first block, between women’s participation and the theory cartoon, at 10 marks.'},
    '1(h)': {'paper': 'confidence in politicians', 'scheme': 'Valid conclusions.', 'reason': 'Paper p5 Growing up in Ireland chart asks a conclusion and supporting reason. Scheme p6 first block prices those linked aspects at 5 each.'},
    '1(r)': {'paper': 'meaningful consultation', 'scheme': 'Meaningful consultation.', 'reason': 'Paper p8 definition matches scheme p8 consultation block between the graphic and children’s voices, 10 marks.'},
}
REVIEWED[2021, 'ordinary']['promptOverrides'] = {
    '1(b)': 'Describe two strategies to increase the participation of women in political life.',
    '7': 'Pollution and greenhouse gas levels have fallen across the world due to the halt of economic activity as a result of the global pandemic.\n\nWhat strategies can be used to ensure the world does not return to previous levels?\n\nIn your answer you may focus on one or more of the following: individuals; communities; industries; governments.\n\nYou may be able to draw on the images in the original question in your essay.',
    '8': 'Has globalisation made the world a better place?\n\nYou may be able to draw on the images in the original question in your essay.\n\nYou may refer to a key thinker to support your answer.',
    '9': 'Discuss the strengths and weaknesses of a coalition government.\nYou may use the following words in your essay.\n• Minority government\n• Shared mandate\n• Representation\n• Alliances\n• Compromise/making decisions\n• Power sharing\n• Opposition\n• Leadership\n• Gender',
    '10': 'A child or young person’s circumstances, such as their wealth, gender, ethnicity and where they live, play an important role in shaping their opportunities for education and life.\n\nDo you agree or disagree with this statement. Explain your answer.\n\nYou may also use the following phrases and the images in the original question in your essay.\n• Technology in education\n• Poverty\n• Government policy\n• Developing/developed countries\n• Key thinker e.g. Kathleen Lynch.',
}

REVIEWED[2022, 'higher'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 19)),
    'sourcePages': [8, 9], 'shortMarks': 5,
    'shortTopics': '0-5 1-2 2-5 0-4 0-9 3-8 0-7 1-9 2-7 0-5 3-5 0-5 0-9 0-12 0-8'.split(),
    'dataTopics': {'2': '2-2'}, 'dataMarks': {'2': [10, 10, 20, 20, 20, 20, 50]},
    'topicOverrides': {'2(b)': '1-9', '2(c)': '1-9', '2(d)': '1-9', '2(g)': '3-0'},
    'essayTopics': {'3(a)': '3-1', '3(b)': '2-8', '4': '3-8', '5': '2-0', '6': '0-6', '7': '2-9'},
    'criterionAllocations': {
        '1(c)': [('Explanation', 3), ('Thinker', 2)],
        '1(g)': [('Name', 2), ('Description', 3)], '1(o)': [('Country', 2), ('Explanation', 3)],
        '2(c)': [('Positive aspect', 10), ('Negative aspect', 10)], '2(g)': [('Conclusions', 30), ('Use of documents', 20)],
    },
    'permittedMarks': {'1(c)': {'Thinker': [0, 2]}, '1(g)': {'Name': [0, 2]}, '1(o)': {'Country': [0, 2]}},
    'splits': {
        '1(c)': [split_task('explanation', 'Cartoon message', 'Explain the message portrayed in this cartoon.', 0), split_task('thinker', 'Key thinker', 'Which key thinker would you associate with the view portrayed in this cartoon?', 1)],
        '2(c)': [split_task('positive', 'Positive aspect', 'Critique one positive aspect of the use of case studies as a research methodology as used in Document A.', 0), split_task('negative', 'Negative aspect', 'Critique one negative aspect of the use of case studies as a research methodology as used in Document A.', 1)],
    },
    'promptOverrides': {
        '1(f)': 'In this Irish Times/IPSOS MRBI poll, voters were asked if they would support or be opposed to certain measures to combat climate change.\nWhat message can the Irish Government take from the answer to the question regarding higher taxes on energy and fuel?',
        '1(g)': 'Name and describe a model of youth participation outside of the school environment used by organisations or governments to capture the voice of young people in decision-making processes.',
        '1(i)': 'Explain the significance of this headline in The Guardian in relation to the climate crisis.',
        '1(m)': 'Critically evaluate this image in the context of the growing power and influence of social media.',
        '1(o)': 'Name one non-democratic country and briefly explain how it is governed.',
        '2(g)': 'Based on the evidence presented in both documents and the Census questions in the original question, what conclusions can be made about the evolving nature of Irish identity?',
        '6': 'In the context of the findings of the CSO survey and the theories of Sylvia Walby, evaluate whether contemporary Irish society is a patriarchy.\n\n[Your answer should include contemporary examples and evidence from a national context to support your argument.]',
    },
    'boundaryNotes': {
        '1(a)': 'The explanation is of the candidate’s chosen example: one 5-mark response.',
        '1(b)': 'Two open points share a five-mark cap with conditional transfer from the first point; keep together.',
        '1(c)': 'The cartoon fixes the stimulus; message and associated thinker have independent 3+2 tariffs. Split with the cartoon retained.',
        '1(g),1(o)': 'Description must match the candidate’s selected model/country, explicitly stated in scheme. Keep each linked 2+3 response. No closed menu appears in the paper.',
        '2(c)': 'Scheme pp8–9 explicitly prices positive and negative critiques at 10 each; split.',
        '2(g)': 'Conclusions and document use assess one answer, 30+20. Preserve the p12 Census stimulus, whose own tick-box instructions are source content rather than an exam route menu.',
        '3': 'The printed essay alternatives are two separate 100-mark routes.',
        '3-7': 'Theorists, examples, agreements and and/or support are open or flexible choices; do not enumerate them.',
    },
    'reviewedTaskCounts': {'A': 16, 'B': 8, 'C': 6},
}

REVIEWED[2022, 'higher']['alignmentReviews'] = {
    '1(g)': {'paper': 'Name and describe a model of youth participation', 'scheme': 'Name (2M) and description (3M)', 'reason': 'Paper p5 model naming/description matches scheme p5 final block and its required matching-model note, 2+3.'},
    '2(g)': {'paper': 'evolving nature of Irish identity', 'scheme': 'Conclusions about the evolving nature of Irish identity', 'reason': 'Paper p12 identity/Census task matches the scheme p10 final block, conclusions 30 and documents 20.'},
}

REVIEWED[2022, 'ordinary'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 25)),
    'sourcePages': [10, 11], 'shortMarks': 10,
    'shortTopics': '0-6 1-10 0-5 1-9 2-2 3-8 0-0 2-0 2-0 2-6 3-8 0-4 3-4 1-0 3-4 0-9 0-7 0-6 2-8 0-12'.split(),
    'partMarks': {'1(d)(i)': 2, '1(d)(ii)': 3, '1(d)(iii)': 5},
    'dataTopics': {'2': '2-10', '3': '1-9', '4': '2-10'},
    'dataMarks': {'2': [5, 10, 10, 15, 10], '3': [10, 10, 10, 10, 10], '4': [10, 10, 15, 15]},
    'topicOverrides': {'4(a)': '1-1'},
    'essayTopics': {'5': '0-9', '6': '3-7', '7': '2-7', '8': '0-8', '9': '0-12', '10': '2-2'},
    'criterionAllocations': {
        '1(e)': [(s+' ground', 2) for s in ['First', 'Second', 'Third', 'Fourth', 'Fifth']],
        '1(l)': [('First piece', 5), ('Second piece', 5)], '1(t)': [('First way', 5), ('Second way', 5)],
        '2(b)': [('First sector', 5), ('Second sector', 5)], '2(d)': [('First way', 5), ('Second way', 5), ('Third way', 5)],
    },
    'permittedMarks': {
        '1(d)(i)': {'Complete response': [0, 2]}, '1(d)(ii)': {'Complete response': [0, 3]},
        '1(e)': {s+' ground': [0, 2] for s in ['First', 'Second', 'Third', 'Fourth', 'Fifth']},
        '2(a)': {'Complete response': [0, 5]}, '2(b)': {'First sector': [0, 5], 'Second sector': [0, 5]},
        '2(d)': {'First way': [0, 5], 'Second way': [0, 5], 'Third way': [0, 5]},
    },
    'stemOverrides': {'1(d)': 'Study the Climate and Nature Summit opinion-poll chart on young people’s views on climate change in the original question.'},
    'promptOverrides': {
        '1(n)': 'Describe one strategy used by one of the people below or any one individual of your choice who made a positive impact on their society.\n• Nelson Mandela\n• Mahatma Gandhi',
        '1(o)': 'Using the image in the original question, what conclusion could you draw about inequality in the world today?',
        '1(p)': 'Explain what is meant by ‘bias’ in the media.',
        '5': 'Discuss the dangers of online misinformation/fake news and what can be done to address this issue in a democratic society.\n\nYou may use the infographic and headings in the original question to support your answer. You may also refer to a relevant key thinker you have studied.',
        '7': 'Using the infographic in the original question, discuss issues of inequality in the world today and suggest what can be done to address these issues.\n\nYou may also refer to a key thinker you have studied.',
        '8': 'What are the advantages and disadvantages of a democratic government?\n\nYou may use the following words in your essay:\n• Elections/voting\n• Representatives/representation\n• Power\n• Majority/minority\n• Laws/decision-making\n• Referendum\n• Political parties\n• Human rights/civil liberties\n• Hobbes and Locke\n• Coalition.',
        '9': 'What does the data from St Vincent de Paul in the original question tell us about the social contract in Ireland?',
        '10': 'The Universal Declaration of Human Rights states that ‘All human beings are born free and equal in dignity and rights’.\n\nDiscuss the issue of racism in society today.\n\nYou may use the infographic in the original question to support your answer.',
    },
    'finiteRoutes': {},
    'boundaryNotes': {
        '1(b),1(d)(iii),1(g),1(i),1(k),1(r),1(s),3(d)': 'These tasks print Yes/No checkboxes and require a justified position. Preserve both explicit selectable argument routes, with the whole published tariff on each; they are not single-correct factual quizzes.',
        '1(d)': 'Three printed roman parts have independent 2,3,5 tariffs. Keep the poll graphic with all three, then expand the third part’s Yes/No choice.',
        '1(e)': 'Five recalled grounds from the statutory nine: the paper does not print the answers as a route menu. Retain the recall task with five 2-mark criteria; do not put its answers in the prompt.',
        '1(n)': 'Mandela and Gandhi are illustrative: the paper expressly permits any individual of the candidate’s choice. Keep one open task.',
        '1(l),1(t),2(b),2(d)': 'Required pairs/triples of information, not choices of independent printed task or a choose-k menu. Retain the response with separate published criteria.',
        '2(c)': 'One integrated explanation with a holistic 10-mark grid; no separate eligible/ineligible allocation.',
        '3(e)': 'Open selection of a relevant piece of data to connect with a narrative, not a finite printed pool.',
        '4(d)': 'Open evaluative question without a printed menu or checkboxes; retain a single justified response.',
        '5-10': 'Optional infographic headings, survey questions and thinker suggestions support one holistic 50-mark essay each.',
        'section-heading': 'Scheme p16 labels Section C 150 marks, but the paper requires two 50-mark essays (100). Each practice essay retains its explicit 50-mark tariff.',
    },
    'reviewedTaskCounts': {'A': 29, 'B': 15, 'C': 6},
}

# The printed checkbox menus require a reason for the selected answer.
# Keep that original instruction and constrain only the chosen checkbox.
for _key, _cue, _prompt in [
    ('1(b)', 'Is it important to vote in an election?', 'Is it important to vote in an election? Give a reason for your answer.'),
    ('1(d)(iii)', 'Is there a value to opinion polls?', 'Is there a value to opinion polls? Give a reason for your answer.'),
    ('1(g)', 'Is it important for a school to have a student council?', 'Is it important for a school to have a student council? Explain your answer.'),
    ('1(i)', 'Is the United Nations Convention', 'Is the United Nations Convention on the Rights of the Child (UNCRC) important? Give a reason for your answer.'),
    ('1(k)', 'Is it important that the world unites', 'Is it important that the world unites to tackle climate change? Give a reason for your answer.'),
    ('1(r)', 'are gender quotas the solution', 'Given the statistics in the original question, are gender quotas the solution to increase female representation in the world of business? Give a reason for your answer.'),
    ('1(s)', 'Can universal human rights exist', 'Can universal human rights exist in a culturally diverse world? Give a reason for your answer.'),
    ('3(d)', 'Is Document B a reliable source of data?', 'Is Document B a reliable source of data? Explain your answer.'),
]:
    REVIEWED[2022, 'ordinary']['finiteRoutes'][_key] = {'cue': _cue, 'choose': 1, 'pool': [('yes', 'Yes'), ('no', 'No')], 'prompt': _prompt + '\n\nSelected response: {selection}.'}

REVIEWED[2022, 'ordinary']['alignmentReviews'] = {
    '1(b)': {'paper': 'Is it important to vote in an election?', 'scheme': 'Is it important to vote in an election?', 'reason': 'Paper p3 voting checkbox and reason match scheme p4 second block, with positive and protest arguments and one 10-mark explanation grid.'},
    '1(f)': {'paper': 'understanding of sustainable development', 'scheme': 'Understanding of sustainable development', 'reason': 'Paper p5 definition matches scheme p6 first block and its Brundtland/SDG guidance, 10 marks.'},
    '1(o)': {'paper': 'inequality in the world today', 'scheme': 'Conclusion about inequality in the world today.', 'reason': 'Paper p7 vaccine-distribution image matches scheme p9 first block, whose examples explicitly refer to vaccine inequality.'},
    '1(p)': {'paper': '‘bias’ in the media', 'scheme': 'Explanation of ‘bias’ in the media.', 'reason': 'Paper p8 news cartoon and definition match scheme p9 second block, 10 marks.'},
    '1(r)': {'paper': 'are gender quotas the solution', 'scheme': 'Are gender quotas the solution', 'reason': 'Paper p8 business representation chart and Yes/No choice match scheme p10 first block, which gives both pros and cons.'},
}

REVIEWED[2023, 'higher'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 19)),
    'sourcePages': [8, 9], 'shortMarks': 5,
    'shortTopics': '0-5 0-7 0-5 2-2 3-7 0-5 2-1 3-9 0-9 0-6 0-12 0-6 0-12 3-0 3-4'.split(),
    'dataTopics': {'2': '2-7'}, 'dataMarks': {'2': [10, 10, 20, 20, 20, 20, 50]},
    'topicOverrides': {'2(a)': '1-9', '2(b)': '1-9', '2(c)': '1-9'},
    'essayTopics': {'3': '1-2', '4(a)': '0-12', '4(b)': '2-5', '5': '0-9', '6': '2-8', '7': '3-8'},
    'criterionAllocations': {'1(h)': [('Explanation of theory', 3), ('Associated theorist', 2)], '2(g)': [('Conclusions', 30), ('Use of documents', 20)]},
    'permittedMarks': {'1(h)': {'Associated theorist': [0, 2]}},
    'promptOverrides': {
        '1(l)': 'In your opinion, is the cartoon strip in the original question successful in challenging gender stereotypes? Give a reason for your answer.',
        '1(n)': 'Draw two conclusions about the data from the 2021 Northern Ireland Census in the original question.',
        '2(g)': 'Drawing on both documents and the images in the original question, what conclusions can you draw about global migration and displacement?',
        '5': 'A report published by the Mercy Corps found that, “Social media has emerged as a powerful tool for communication, connection, community and, unfortunately, conflict.”\n\nCritically evaluate the changing nature of contemporary media.\n\n[Your answer should include contemporary examples and evidence from a local and/or global context to support your argument. You should also refer to the ideas of one named theorist you have studied.]',
    },
    'finiteRoutes': {
        '1(m)': {'cue': 'If you had been asked this question', 'choose': 1, 'pool': [('agree', 'Agree'), ('disagree', 'Disagree'), ('dont-know', 'Don’t know')], 'prompt': 'When asked if Ireland should remain a member of the European Union 88% of people surveyed agreed. If you had been asked this question what would your response have been? Explain your answer.\n\nSelected response from the printed poll: {selection}.'},
    },
    'boundaryNotes': {
        '1(a),1(c),1(f),1(n),1(o)': 'Paired points share a five-mark cap with conditional transfer. In o the solution also depends on the chosen cause. Keep these responses whole.',
        '1(h)': 'The named theorist must be associated with the theory the candidate explains. Keep the linked 3+2 response; the paper does not enumerate theories.',
        '1(l)': 'Open evaluation of a cartoon, without a printed answer menu. Keep the justified opinion as one task.',
        '1(m)': 'The question invites the candidate to answer the displayed poll. Its three printed response categories are Agree, Disagree and Don’t know; expand three 5-mark justified-response routes.',
        '2(c)': 'One holistic 20-mark critique; the top band requires both documents and the next permits one. Do not invent a 10+10 document split.',
        '2(g)': 'Conclusions and document use assess one 50-mark answer; preserve the p12 conflict/disaster maps.',
        '4': 'Both printed essay alternatives are separate 100-mark tasks.',
        '3-7': 'At-least, one-or-more and and/or supporting theorists, contexts and illustrative organisations are open choices, not closed route pools.',
    },
    'reviewedTaskCounts': {'A': 17, 'B': 7, 'C': 6},
}

# The causes are the thirteen labelled rows of the first chart on paper p11.
CAUSES_2023_OL = [
    ('corruption', 'Government and private sector corruption'), ('war', 'War and conflict'),
    ('inefficient-government', 'Government is not efficient or competent'), ('exploitation', 'Rich countries tend to exploit developing countries'),
    ('weak-institutions', 'Weak institutions means there is little accountability'), ('global-economy', 'The global economic system favours richer countries'),
    ('authoritarian-regimes', 'Wealthy countries support authoritarian regimes'), ('debt', 'High debt burden for developing countries'),
    ('health-education-spending', 'Not enough spending health and education'), ('poor-health', 'Poor levels of health in general'),
    ('corporate-investment', 'Not enough investment by corporations'), ('colonialism', 'Legacy of colonialism'), ('disease', 'High level of disease'),
]
REVIEWED[2023, 'ordinary'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 23)),
    'sourcePages': [10, 11], 'shortMarks': 10,
    'shortTopics': '1-10 0-12 2-7 3-7 0-0 1-9 0-12 3-8 3-2 0-8 0-6 0-4 0-9 2-4 3-9 0-6 3-5 0-12 3-3 2-0'.split(),
    'partMarks': {'1(h)(i)': 3, '1(h)(ii)': 3, '1(h)(iii)': 4},
    'dataTopics': {'2': '3-8', '3': '1-9', '4': '3-8'},
    'dataMarks': {'2': [5, 10, 10, 15, 10], '3': [10, 10, 10, 10, 10], '4': [10, 10, 15, 15]},
    'topicOverrides': {'4(b)': '1-1'},
    'essayTopics': {'5': '2-7', '6': '0-12', '7': '0-7', '8': '1-2', '9': '2-2', '10': '0-9'},
    'criterionAllocations': {'1(b)': [('Left wing', 5), ('Right wing', 5)], '1(e)': [('First step', 5), ('Second step', 5)], '1(l)': [('First piece', 5), ('Second piece', 5)], '2(d)': [('First cause', 5), ('Second cause', 5), ('Third cause', 5)], '3(b)': [('Strength', 5), ('Limitation', 5)]},
    'permittedMarks': {'1(n)': {'Complete response': [0, 1, 2, 3, 4, 5, 6, 8, 9, 10]}, '2(a)': {'Complete response': [0, 5]}, '2(b)': {'Complete response': [0, 10]}, '2(d)': {'First cause': [0, 5], 'Second cause': [0, 5], 'Third cause': [0, 5]}},
    'markNotes': {'1(n)': 'The published grid gives 0–3, 4–6 and 8–10, omitting 7. This practice score preserves those published values; consult the original scheme.', '3(d)': 'The paper asks about Document A. The scheme includes representative-sample and optional-answer guidance associated with Document B as well as webpage/authorship guidance. Keep the paper’s Document A wording and consult both documents and the original scheme.'},
    'stemOverrides': {'1(h)': 'Examine the Central Statistics Office infographic “Our Lives Outdoors: Protection of the Environment”, April–May 2022, in the original question.'},
    'splits': {
        '1(b)': [split_task('left-wing', 'Left wing', 'The term ‘left wing’ is sometimes used to describe political parties, politicians and policies. What does this term mean?', 0), split_task('right-wing', 'Right wing', 'The term ‘right wing’ is sometimes used to describe political parties, politicians and policies. What does this term mean?', 1)],
        '3(b)': [split_task('strength', 'Strength', 'Describe one strength of on-line surveys as a research method.', 0), split_task('limitation', 'Limitation', 'Describe one limitation of on-line surveys as a research method.', 1)],
    },
    'finiteRoutes': {
        '1(i)': {'cue': 'ethnic or language or religious diversity', 'choose': 1, 'pool': [('ethnic', 'ethnic'), ('language', 'language'), ('religious', 'religious')], 'prompt': 'Comment on {selection} diversity in one European country. Name the country.'},
        '1(q)': {'cue': 'one of the following:', 'choose': 1, 'pool': [('imf', 'International Monetary Fund (IMF)'), ('wto', 'World Trade Organisation (WTO)')], 'prompt': 'Give a brief description of the {selection}.'},
        '2(d)': {'cue': 'name three main causes of poverty', 'choose': 3, 'pool': [(key, 'row ' + str(i + 1)) for i, (key, _) in enumerate(CAUSES_2023_OL)], 'sourceEvidence': {'page': 11, 'text': 'Which of the following do you think are the main causes of poverty in developing countries?'}, 'prompt': 'According to Document B, name the three causes of poverty shown in {selection} of the first chart, counting from the top.'},
        '4(d)': {'cue': 'What answer would you have chosen', 'choose': 1, 'pool': CAUSES_2023_OL, 'sourceEvidence': {'page': 11, 'text': 'Which of the following do you think are the main causes of poverty in developing countries?'}, 'prompt': 'What answer would you have chosen to the question in Document B about the main causes of poverty in developing countries? Give one reason for your choice.\n\nSelected answer: {selection}.'},
    },
    'boundaryNotes': {
        '1(b)': 'Independent definitions priced 5 each; split.',
        '1(d),1(h)(i),1(j),3(c),3(d)': 'Explicit Yes/No checkbox choices with reasons: expand both selectable positions at the published tariff.',
        '1(h)': 'Three separately priced printed parts, 3+3+4. Share the infographic and expand the first part’s Yes/No routes.',
        '1(i)': 'Three explicit types of diversity separated by or, in an openly chosen country: three 10-mark routes; do not enumerate countries.',
        '1(q)': 'Closed IMF/WTO choice: two 10-mark routes.',
        '1(e),1(l)': 'Required pairs from an open domain with two 5-mark criteria.',
        '2(d)': 'The scheme explicitly accepts any three of the chart’s thirteen causes, not just the top three. Expand C(13,3)=286 retrieval routes. Use row numbers in prompts to avoid supplying the answers.',
        '3(b)': 'Independent 5-mark strength and limitation: split.',
        '3(e)': 'Open selection of evidence from the whole mixed prose/chart Document A, not a closed enumerated answer pool.',
        '4(a)': 'The top three reasons are specified, not selected by the candidate. One holistic comment grid, 10 marks.',
        '4(d)': 'Candidate chooses an answer to the first chart’s question: thirteen named causes, thirteen 15-mark justified routes. The second chart’s up-to-three instruction belongs to its original survey, not to the exam candidate.',
        '5-10': 'Optional support and, in Q8, required headings assess one integrated essay. No fixed finite choice among these headings.',
    },
    'reviewedTaskCounts': {'A': 29, 'B': 314, 'C': 6},
}
for _key, _cue, _prompt in [
    ('1(d)', 'Choose to Refuse', 'Do you think that this Choose to Refuse single-use plastic campaign is a good example of an action that an individual could take to achieve sustainable development? Give a reason for your answer.'),
    ('1(h)(i)', 'Would you be one of the 68%', 'Would you be one of the 68% who said they were concerned about climate change? Give a reason for your answer.'),
    ('1(j)', 'Does the Irish system of elections', 'Does the Irish system of elections produce a government that is truly representative of the people? Give one reason for your answer.'),
    ('3(c)', 'Is there a value to researching', 'Is there a value to researching people’s opinions and attitudes? Explain your answer.'),
    ('3(d)', 'Is Document A a reliable source of data?', 'Is Document A a reliable source of data? Explain your answer.'),
]:
    REVIEWED[2023, 'ordinary']['finiteRoutes'][_key] = {'cue': _cue, 'choose': 1, 'pool': [('yes', 'Yes'), ('no', 'No')], 'prompt': _prompt + '\n\nSelected response: {selection}.'}

REVIEWED[2023, 'ordinary']['promptOverrides'] = {
    '5': 'Discuss the impact of climate change on human rights.\n\nYou may use the infographic in the original question to support your answer. You may also refer to a relevant key thinker you have studied.',
    '9': 'Are human rights providing a basis for ensuring equality in society today? Discuss.\n\nYou may refer to the image in the original question and use the words below in your essay.\n• Declarations, Conventions, agreements, treaties\n• Children’s Rights\n• Abuses/violations\n• Gender inequality\n• Racism\n• Hate speech\n• Sport\n• Prejudice/discrimination\n• Key thinker',
}

REVIEWED[2024, 'higher'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 18)),
    'sourcePages': [8, 9], 'shortMarks': 5,
    'shortTopics': '2-1 0-5 3-9 0-9 2-5 2-0 0-12 1-9 0-8 3-0 0-5 0-9 3-4 0-6 0-12'.split(),
    'dataTopics': {'2': '0-6'}, 'dataMarks': {'2': [10, 10, 20, 20, 20, 20, 50]},
    'topicOverrides': {'2(a)': '1-9', '2(b)': '1-9', '2(e)': '1-9'},
    'essayTopics': {'3(a)': '3-3', '3(b)': '2-7', '4': '0-9', '5': '2-9', '6': '0-8', '7': '3-8'},
    'criterionAllocations': {'2(g)': [('Critique', 30), ('Use of documents', 20)]},
    'finiteRoutes': {'1(o)': {'cue': 'either a left or right‐wing', 'choose': 1, 'pool': [('left-wing', 'left-wing'), ('right-wing', 'right-wing')], 'prompt': 'Briefly describe what it means to have a {selection} political viewpoint.'}},
    'promptOverrides': {
        '1(c)': 'Key thinker Andre Gunder-Frank proposed Dependency Theory to try and explain why some countries remain underdeveloped. Briefly explain this theory.',
        '1(h)': 'Comment on the presentation of the message in this image in the context of the climate crisis.',
        '1(l)': 'What conclusions can you draw from the statistics in the original question in relation to the media?',
        '2(g)': 'Drawing on the information in both documents and the statement from Document B in the original question, critique the use of quotas to address gender imbalance in the Irish political system.',
        '3(b)': 'This image is a representation of the poem ‘Home’ by Warsan Shire.\nThe poem explains how some refugees would not leave their home if they were not forced to do so.\n\nDiscuss the refugee crisis in the world today in the context of human rights.\n\n[Your answer should include contemporary examples and evidence from a national and/or global context to support your argument. You should also refer to the ideas of two theorists, one of whom must be named on your course.]',
    },
    'boundaryNotes': {
        '1(a),1(i),1(j),1(k),1(l)': 'Shared five-mark caps with conditional transfer between points. Keep whole, including a’s comparison of two rights categories.',
        '1(o)': 'Explicit either left or right-wing choice: two 5-mark routes.',
        '2(a)': 'Strengths and limitations share one holistic 10-mark grid. No independent component tariff; retain together.',
        '2(c),2(d),2(f)': 'One holistic 20-mark grid with conditions on use of both documents. Do not split by document.',
        '2(f)': 'Local, national or European describes the settings in which women may represent communities. The instruction is to discuss barriers from both documents, not to select one setting; no finite route expansion.',
        '2(g)': 'Critique and use of documents assess one argument, 30+20. Retain the p12 quota graphic and quotation.',
        '3': 'Both printed essay alternatives are separate 100-mark routes; and/or nationalism and cultural identity allows flexible coverage within 3(a).',
        '4-7': 'Open evaluative positions and supporting examples/theorists, not closed answer menus.',
    },
    'reviewedTaskCounts': {'A': 16, 'B': 7, 'C': 6},
}

REVIEWED[2024, 'ordinary'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 22)),
    'sourcePages': [10, 11], 'shortMarks': 10,
    'shortTopics': '2-0 0-12 2-2 1-9 2-5 3-8 1-9 3-5 2-3 2-2 3-4 0-5 3-0 0-6 3-7 2-9 0-9 0-6 0-9 0-6'.split(),
    'partMarks': {'1(d)(i)': 4, '1(d)(ii)': 3, '1(d)(iii)': 3},
    'dataTopics': {'2': '2-10', '3': '1-9', '4': '2-10'},
    'dataMarks': {'2': [5, 20, 5, 10, 10], '3': [5, 5, 10, 15, 15], '4': [10, 10, 15, 15]},
    'topicOverrides': {'2(c)': '2-0', '2(d)': '2-0', '3(d)': '0-6', '3(e)': '0-6', '4(a)': '2-0', '4(b)': '1-9', '4(c)': '1-1', '4(d)': '0-4'},
    'essayTopics': {'5': '2-8', '6': '0-9', '7': '0-6', '8': '1-2', '9': '0-0', '10': '3-7'},
    'criterionAllocations': {'2(b)': [(s+' way', 5) for s in ['First', 'Second', 'Third', 'Fourth']]},
    'permittedMarks': {'2(a)': {'Complete response': [0, 5]}, '2(b)': {s+' way': [0, 5] for s in ['First', 'Second', 'Third', 'Fourth']}, '2(c)': {'Complete response': [0, 5]}},
    'stemOverrides': {'1(d)': 'Answer the questions on the Housing in Ireland infographic from the Central Statistics Office in the original question.'},
    'promptOverrides': {
        '1(h)': 'What does the term ‘Globalisation’ mean?',
        '6': 'Discuss the influence/role of the media in society today.\n\nYou may refer to the following in your answer:\n• Control / ownership / business\n• Reporting the news\n• Disinformation / misinformation\n• Fake news / bias / opinion\n• Politics / democracy\n• Influencers\n• Key thinker e.g. Noam Chomsky.',
        '10': 'According to a 2023 European Union survey, 93% of European people believe climate change is a serious problem facing the world.\n\nDiscuss what actions are needed to achieve sustainable development in the modern world.\n\nYou may use the following in your answer:\n• Consumer purchases\n• Sustainable consumption\n• Industry e.g. fast fashion\n• Renewable resources\n• The role of corporations\n• International agreements e.g. COP 28\n• The role of governments e.g. Climate Action Plan for Ireland, 2023\n• Key thinkers e.g. Vandana Shiva, Fr Seán McDonagh.',
    },
    'finiteRoutes': {},
    'boundaryNotes': {
        '1(b),1(d)(iii),1(j)': 'Printed Yes/No checkboxes invite a position; preserve both justified response routes at the full task tariff.',
        '1(d)': 'Scheme independently prices the three roman parts at 4,3,3. First part asks a factual more/less rent comparison, with one data-supported answer, not alternative practicable argument routes.',
        '1(c),1(g),1(r)': 'Comparison or explanation and example assessed by a single holistic ten-mark grid. No separately priced components.',
        '2(b)': 'All four assistance services in the narrative are required: four 5-mark criteria, no choose-k selection.',
        '3(c)': 'Open choice of a relevant piece of data to connect with the other document, not a closed printed pool.',
        '3(d),3(e)': 'Each response has one holistic 15-mark grid.',
        '4(a)': 'The three biggest areas are fixed by the chart values; this is not a choice of any three categories.',
        '4(b)': 'Open evaluation without printed selectable checkboxes; one ten-mark response.',
        '4(c),4(d)': 'Open choices of issue, project, evidence and policy recommendations; either document permits evidence sources rather than enumerating a finite response menu.',
        '5-10': 'Six holistic 50-mark essays; optional headings and named thinkers support the answer and are not selectable tasks.',
    },
    'reviewedTaskCounts': {'A': 25, 'B': 14, 'C': 6},
}
for _key, _cue, _prompt in [
    ('1(b)', 'Is it important for people to vote', 'Is it important for people to vote in European Union Elections? Explain your answer.'),
    ('1(d)(iii)', 'Is the census a reliable source of data?', 'Is the census a reliable source of data? Explain your answer.'),
    ('1(j)', 'Is it important to have laws against online hate speech?', 'Is it important to have laws against online hate speech?'),
]:
    REVIEWED[2024, 'ordinary']['finiteRoutes'][_key] = {'cue': _cue, 'choose': 1, 'pool': [('yes', 'Yes'), ('no', 'No')], 'prompt': _prompt+'\n\nSelected response: {selection}.'}

REVIEWED[2025, 'higher'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 21)),
    'sourcePages': [8, 9], 'shortMarks': 5,
    'shortTopics': '0-0 0-9 0-12 2-2 2-5 0-8 0-6 3-4 0-5 3-7 2-2 0-8 3-2 2-10 2-6'.split(),
    'dataTopics': {'2': '0-12'}, 'dataMarks': {'2': [10, 10, 20, 20, 20, 20, 50]},
    'topicOverrides': {'2(d)': '1-9'},
    'essayTopics': {'3(a)': '0-8', '3(b)': '1-2', '4': '3-8', '5': '0-9', '6': '2-5', '7': '3-3'},
    'criterionAllocations': {
        '1(a)': [('Group', 2), ('Suggestion for the group', 3)],
        '1(i)': [('First function', 3), ('Second function', 2)], '1(m)': [('First way', 3), ('Second way', 2)],
        '1(l)': [('System', 2), ('Description of that system', 3)],
        '1(o)': [('Key thinker', 2), ('Explanation of theory', 3)],
        '2(g)': [('Conclusions', 30), ('Use of documents', 20)],
    },
    'permittedMarks': {'1(a)': {'Group': [0, 2]}, '1(l)': {'System': [0, 2]}, '1(o)': {'Key thinker': [0, 2]}},
    'splits': {'1(o)': [split_task('thinker', 'Key thinker', 'Name the key thinker associated with the Capabilities Approach.', 0), split_task('theory', 'Theory', 'Briefly explain the Capabilities Approach.', 1)]},
    'finiteRoutes': {'1(c)': {'cue': 'Thomas Hobbes or John Locke', 'choose': 1, 'pool': [('hobbes', 'Thomas Hobbes'), ('locke', 'John Locke')], 'prompt': 'Explain the ‘State of Nature’ concept through the view of {selection}.'}},
    'promptOverrides': {
        '1(a)': 'Identify a group that may be under-represented in the decision-making processes in schools and suggest one way to increase their representation.',
        '4': '“A developed country is not a place where the poor have cars. It’s where the rich use public transportation.” — Gustavo Petro.\n\nDiscuss this statement from Gustavo Petro in the context of sustainable development.\n\n[Your answer should include contemporary examples and evidence such as COP 29 or other relevant national or international agreements to support your argument. You should also refer to the ideas of at least one theorist named on your course.]',
    },
    'boundaryNotes': {
        '1(a),1(l)': 'Open choice of group/system; suggestion or description must match that choice. Preserve each linked 2+3 response.',
        '1(c)': 'Closed printed Hobbes/Locke alternatives yield two five-mark routes.',
        '1(i),1(m)': 'Two required open responses with 3+2 allocations; retain together because they are unlabelled slots in a single selection of two distinct responses, not independent printed tasks.',
        '1(k)': 'One holistic five-mark comparison, no independently priced definitions.',
        '1(o)': 'Fixed Capabilities Approach has independent thinker identification (2) and theory explanation (3); split without supplying the thinker answer.',
        '2(a)-2(f)': 'One holistic grid per printed task: 10,10,20,20,20,20. Reasons or aspects are not a fixed choose-k pool.',
        '2(g)': 'Conclusions and document use assess one answer, 30+20, with the Niebuhr quotation and voting image on p12.',
        '3': 'Both printed alternatives are separate 100-mark essays.',
        '3-7': 'Theorists, contexts, contemporary evidence and illustrative agreements are open or flexible supporting choices.',
    },
    'reviewedTaskCounts': {'A': 17, 'B': 7, 'C': 6},
}

REVIEWED[2025, 'ordinary'] = {
    'paperPagesReviewed': list(range(1, 29)), 'schemePagesReviewed': list(range(1, 21)),
    'sourcePages': [10, 11], 'shortMarks': 10,
    'shortTopics': '1-10 0-1 3-7 1-9 2-0 0-6 0-6 0-5 2-8 2-4 3-3 0-9 3-0 0-5 3-8 2-5 3-5 2-1 0-12 2-2'.split(),
    'partMarks': {'1(d)(i)': 4, '1(d)(ii)': 3, '1(d)(iii)': 3},
    'dataTopics': {'2': '2-7', '3': '1-9', '4': '2-7'},
    'dataMarks': {'2': [5, 10, 15, 10, 10], '3': [5, 5, 10, 15, 15], '4': [10, 10, 15, 15]},
    'topicOverrides': {'2(a)': '3-7', '2(b)': '3-7', '2(e)': '3-8', '3(d)': '2-9', '4(b)': '1-9', '4(c)': '1-1', '4(d)': '2-9'},
    'essayTopics': {'5': '0-8', '6': '0-0', '7': '3-7', '8': '0-9', '9': '2-8', '10': '2-5'},
    'criterionAllocations': {
        '1(a)': [('First reason', 5), ('Second reason', 5)], '1(e)': [('Right', 2), ('Description of unmet right', 8)],
        '1(q)': [('First reason', 5), ('Second reason', 5)], '1(r)': [('Description', 8), ('Example', 2)],
        '2(d)': [('Country', 2), ('Cause of hunger', 8)], '3(c)': [('Key information', 2), ('Link to Document B', 8)],
        '4(a)': [('Similarity', 5), ('Difference', 5)],
    },
    'permittedMarks': {'1(e)': {'Right': [0, 2]}, '1(r)': {'Example': [0, 2]}, '2(a)': {'Complete response': [0, 5]}, '2(b)': {'Complete response': [0, 10]}, '2(d)': {'Country': [0, 2], 'Cause of hunger': [0, 8]}, '3(c)': {'Key information': [0, 2]}},
    'stemOverrides': {'1(d)': 'Examine the 2023 Survey on Income and Living Conditions (SILC) infographic from the Central Statistics Office in the original question.'},
    'splits': {
        '1(r)': [split_task('description', 'Description', 'Describe what a duty bearer is.', 0), split_task('example', 'Example', 'Give an example of a duty bearer.', 1)],
        '4(a)': [split_task('similarity', 'Similarity', 'From Document B, identify one similarity between the data from Haiti and the data from South Sudan.', 0), split_task('difference', 'Difference', 'From Document B, identify one difference between the data from Haiti and the data from South Sudan.', 1)],
    },
    'finiteRoutes': {
        '1(c)': {'cue': 'Is this a good example of an action to', 'choose': 1, 'pool': [('yes', 'Yes'), ('no', 'No')], 'prompt': 'In 2024 the Irish government introduced the Deposit Return Scheme for plastic bottles and aluminium or steel cans. Is this a good example of an action to achieve sustainable development? Explain your answer.\n\nSelected response: {selection}.'},
        '2(d)': {'cue': 'Name one of these countries', 'choose': 1, 'pool': [('haiti', 'the first country column'), ('south-sudan', 'the second country column'), ('sudan', 'the third country column')], 'sourceEvidence': {'page': 11, 'text': 'Haiti'}, 'prompt': 'Document B outlines the main causes of hunger in three countries. Using {selection} in the table, name the country and identify its main cause of hunger.'},
    },
    'markNotes': {'2(e)': 'The printed task refers to Document B. The scheme’s top descriptor mentions both documents; both originals are available for reference.'},
    'promptOverrides': {
        '7': 'The image in the original question highlights the environmental issue of fast fashion facing the world today.\n\nWhat do you think the Irish government and/or international bodies can do to help tackle environmental issues, for example, fast fashion?\n\nYou may refer to the following in your answer:\n• The role of individual efforts\n• What business and corporations can do\n• International agreements (United Nations and the European Union)\n• Underdevelopment and unfair trade\n• Sustainable Development Goals\n• Key thinkers e.g. Sean McDonagh.',
        '8': 'Evaluate the changing nature of contemporary media in society.\n\nYou may refer to the following in your answer:\n• Types of media\n• Control of information\n• Misinformation / Disinformation\n• Regulations\n• Ownership / control of the media\n• The role of advertising\n• Key thinker e.g. Noam Chomsky or Karl Marx.',
    },
    'boundaryNotes': {
        '1(a),1(q)': 'Two required open reasons, each 5 marks; retain the paired recall task with two criteria, not a finite printed pool.',
        '1(c)': 'Explicit Yes/No checkbox menu; two justified ten-mark answer routes. Aluminium or steel describes eligible materials, not a separate candidate choice.',
        '1(d)': 'Three independently priced roman parts: 4,3,3, all retain the CSO graphic.',
        '1(e)': 'The example must demonstrate the selected right being unmet; keep the linked 2+8 response. Rights are recalled, not a printed pool.',
        '1(p),1(s)': 'Open theory recall; and/or is flexible coverage. The State of Nature question does not print a Hobbes/Locke choice (unlike HL); retain one task.',
        '1(r)': 'Fixed duty-bearer concept has independent description (8) and example (2) tariffs; split.',
        '2(d)': 'Three finite country columns: derive one route per column, keeping the linked 2+8 response. Prompt identifies the column position so the retrieval answer is not disclosed.',
        '2(c)': 'All three drivers are required; scheme gives one 15-mark response, not an explicit per-driver tariff.',
        '2(e)': 'Paper refers to Document B; scheme top descriptor says both. Preserve paper wording, note discrepancy, include both sources.',
        '3(c)': 'Open choice of evidence from mixed narrative and infographic; key piece and link remain one linked 2+8 response.',
        '3(e)': 'Open reliability judgement without printed checkbox choices; keep one response.',
        '4(a)': 'Similarity and difference each have five marks; split, retaining both countries and source.',
        '4(b)': 'Chosen data type and matching example form one holistic ten-mark answer.',
        '4(c),4(d)': 'Open project and recommendations, not a finite menu.',
        '5-10': 'Six holistic essays with optional support headings, thinkers and flexible and/or contexts. Each remains 50 marks.',
    },
    'reviewedTaskCounts': {'A': 24, 'B': 17, 'C': 6},
}

# NCCA Strands of Study, Topic 2.3 explicitly locates capitalism in social class.
# https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/politics-and-society/strands-of-study/
REVIEWED[2021, 'higher']['boundaryNotes']['1(b)-topic'] = 'Capitalism is Topic 2.3 Social Class and Gender in NCCA; the cartoon stays with that canonical node.'
REVIEWED[2021, 'ordinary']['boundaryNotes']['1(c)-topic'] = 'Capitalism, social class and patriarchy are Topic 2.3 concepts; all three routes resolve to its canonical node.'
