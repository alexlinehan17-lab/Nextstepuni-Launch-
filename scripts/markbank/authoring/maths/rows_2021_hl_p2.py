import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import L, LPC, MPC, HPC, PC, FC, FCM, ZC, SOL, NOTE, STEP
ROWS = {
 'maths-2021-hl-p2-q1-b': [L(SOL, '= 0∙1673 … + 0∙3248 … + 0∙2866 …'), L(SOL, '= 0∙7787 …'), L(SOL, '= 0∙78 [2 D.P.]'),
     L(LPC, 'First line of solution'), L(LPC, '0·15 or 0·85 or 3/20 or 17/20 or (11 1)'), L(HPC, 'Two out of P(0), P(1), P(2) fully substituted')],
 'maths-2021-hl-p2-q1-c': [L(SOL, '= 0·1968 … + 0·3474 … + 0·2758 …'), L(SOL, '= 0·82019 …'), L(SOL, '= 0·82 [2 D.P.]'), L(NOTE, 'Accept 82·02%'),
     L(LPC, 'First line of solution'), L(LPC, '0·15 or 0·85 or 3/20 or 17/20 or (10 1)'), L(HPC, 'Two out of P(0), P(1), P(2) fully substituted')],
 'maths-2021-hl-p2-q4-a-ii': [L(SOL, 'cos2A = cos²A − sin²A'), L(SOL, '= 1 − 2sin²(θ/2)'), L(SOL, 'using a right-angled triangle cos θ/2 = 2/√5'),
     L(LPC, 'cosθ = cos²(θ/2) − sin²(θ/2)'), L(LPC, 'Valid work to find cos(θ/2) from sin(θ/2)'), L(LPC, 'Some relevant substitution'),
     L(MPC, 'Finds cos θ/2 = 2/√5.'), L(MPC, 'Also accept cos θ/2 = cos (sin⁻¹ 1/√5) = 0·8944 …'), L(MPC, 'cosθ = (1 − sin²(θ/2)) − sin²(θ/2)'),
     L(HPC, 'cos θ formula fully substituted')],
 'maths-2021-hl-p2-q8-a-i': [L(SOL, 'Top 10% means 90% below.'), L(SOL, 'P(z < 1·28) = 0·8997.'), L(SOL, '⇒x = 222∙08'), L(SOL, 'Minimum mark of 223'),
     L(NOTE, 'Accept use of P(z < 1·29), to give x = 222·44'), L(NOTE, 'Accept answer rounded to 222 instead of 223'),
     L(LPC, 'Mean or standard deviation indicated'), L(LPC, 'z-formula with some substitution'), L(MPC, 'z-score found (1∙28 or 1·29)'),
     L(MPC, 'z-formula fully substituted ((x − 176)/36)'), L(HPC, '(x − 176)/36 = 1·28')],
 'maths-2021-hl-p2-q8-c-i': [L(SOL, 'Assuming no replacement:'), L(SOL, '18/23 × 17/22 × 16/21 × 5/20'), L(SOL, '= 0·11518 … = 0·1152 [4 D.P.]'),
     L(SOL, 'Assuming replacement:'), L(SOL, '= 0∙10420 … = 0∙1042 [4 D.P.]'),
     L(NOTE, 'multiplication between relevant terms is necessary to be awarded above Low Partial Credit'),
     L(LPC, 'One relevant fraction'), L(MPC, 'Product of four fractions, two of them correct'),
     L(HPC, '18/23 × 17/22 × 16/21 × 5/20')],
 'maths-2021-hl-p2-q10-a-i': [L(SOL, 'P(2 from the 1st 9 are O-) × P(10th is O-)'), L(SOL, '= 0∙01028 … = 0∙0103 [4 D.P.]'),
     L(LPC, '8/100 or 92/100 or (9 2)'), L(LPC, 'First line of solution indicated (accept with “and” instead of ×)')],
 'maths-2021-hl-p2-q10-a-ii': [L(SOL, '1 − P(none are O-)'), L(SOL, '= 0·34091 … = 0·3409 [4 D.P.]'),
     L(SOL, 'P(1 or 2 or 3 or 4 or 5 are O-)'), L(LPC, 'First line of either solution'), L(HPC, 'Three terms in second solution')],
}
