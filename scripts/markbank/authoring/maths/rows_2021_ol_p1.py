import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import L, LPC, MPC, HPC, PC, FC, FCM, ZC, SOL, NOTE, STEP
ROWS = {
 'maths-2021-ol-p1-q1-b': [L(SOL, '130∙2/21 × 121 = €750∙20'), L(LPC, '130∙2/21 and stops'), L(LPC, '130∙2 × 121 and stops'), L(LPC, 'Any use of relevant %'),
     L(HPC, '130∙2/21 = 6∙2'), L(HPC, '130∙2 × 121%= 157∙54'), L(HPC, '€620'), L(NOTE, 'Accept correct answer without supporting work')],
 'maths-2021-ol-p1-q2-c': [L(SOL, 'z̅₁ − z₂ = −3 − 4i − (4 + 3i)'), L(SOL, '= −7 − 7i'), L(SOL, '= √98'), L(SOL, '= 7√2'),
     L(LPC, 'Work of relevance for z̅₁ − z₂'), L(MPC, 'z̅₁ − z₂ = −7 − 7i'), L(HPC, '√((−7)² + (−7)²) or √49 + 49'),
     L(NOTE, 'Accept √98 for full credit')],
 'maths-2021-ol-p1-q5-a': [L(SOL, '3(0∙67)² − 6(0∙67) + 7'), L(SOL, '= 4∙3267'), L(SOL, '= 4∙33'),
     L(LPC, 'Any substitution into equation'), L(LPC, 'x = 0·67'), L(HPC, 'f(0∙67) fully substituted'),
     L(NOTE, 'Accept correct answer (4·33) without supporting work'), L(NOTE, '4∙3267 without supporting work merits F*')],
 'maths-2021-ol-p1-q5-c': [L(SOL, '6x − 6 = 0'), L(SOL, 'Min Point = (1, 4)'), L(NOTE, 'If differentiation is not used, award zero marks'),
     L(LPC, 'Any correct differentiation'), L(LPC, 'dy/dx = 0 or dy/dx or f′(x)'), L(MPC, '6x − 6'), L(HPC, 'x co-ordinate found')],
 'maths-2021-ol-p1-q7-d': [L(SOL, '1602∙72 − [60∙06 + 169∙44] ='), L(SOL, '30516 + 12012 + 8472'), L(SOL, '= €51,000'),
     L(LPC, '60∙06 or 169·44 transferred from above'), L(LPC, 'Any use of relevant %'), L(MPC, '1373∙22'), L(HPC, '30 516')],
 'maths-2021-ol-p1-q10-a-i': [L(SOL, '10⁹/250000 = 4000 seconds'), L(SOL, '= 66·67 minutes'), L(SOL, '= 67 minutes'), L(LPC, '10⁹ or equivalent'),
     L(LPC, 'Correct answer without supporting work'), L(LPC, 'Divides by 1000'), L(LPC, 'Use of 60'), L(HPC, '10⁹/250000 or 4000')],
 'maths-2021-ol-p1-q10-b-i': [L(SOL, 'D = 2π(0∙5) = 3∙14 km'), L(SOL, '= 1∙5707 hours or 1∙57'), L(SOL, '= 94∙2 mins'), L(SOL, '= 94 mins'),
     L(LPC, '2πr'), L(LPC, '3∙14 km without work'), L(LPC, 'T = D/S or equivalent'), L(LPC, 'πr² with r = 0∙5 inserted'),
     L(LPC, 'Correct answer without supporting work'), L(MPC, '2π(0∙5)3/6'), L(MPC, '9∙4247 or 9∙42'), L(HPC, '1∙5707 hours or similar')],
 'maths-2021-ol-p1-q10-b-ii': [L(SOL, '= 1∙3117 hours'), L(SOL, '= 1 hour and 18∙7 mins'), L(SOL, '= 79 mins'),
     L(LPC, '1∙15 or 115%'), L(LPC, '3 × 15%'), L(LPC, '3 × 1∙15'), L(LPC, 'T = D/S or equivalent'), L(LPC, 'Correct answer without supporting work'),
     L(MPC, '3(1∙15⁴)/4'), L(HPC, '1·3117 hours or similar'), L(NOTE, 'Award F* for Early Round Off which impacts the answer')],
}
