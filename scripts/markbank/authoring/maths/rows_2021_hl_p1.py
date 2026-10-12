import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import L, LPC, MPC, HPC, PC, FC, FCM, ZC, SOL, NOTE, STEP
Q = 'If solving as a quadratic equation: '; LN = 'If solving as two linear equations: '
WI = 'If solving without isolating variables: '; IV = 'If solving by isolating variables: '
ROWS = {
 'maths-2021-hl-p1-q1-b': [L(SOL, 'Answer: 2 + 3i, −2 − 3i'), L(NOTE, 'Accept 2 + 3i for Full Credit'),
     L(LPC, '(a + bi)² = −5 + 12i'), L(LPC, 'r or θ found'), L(LPC, '−5 + 12i plotted on Argand diagram.'),
     L(LPC, 'Shows some knowledge of De Moivre’s theorem'), L(MPC, 'Relevant equation in a single variable'),
     L(MPC, 'Writes −5 + 12i in polar form'), L(HPC, 'Finds a = 2 or b = 3'), L(HPC, '−2 − 3i found'),
     L(HPC, 'Correct solution in polar form (accept with mishandling of 2nπ)')],
 'maths-2021-hl-p1-q1-c': [L(SOL, 'n = 0: z = 2(cos π/3 + i sin π/3) = 1 + √3i'), L(SOL, 'n = 2: z = 2(cos 5π/3 + i sin 5π/3) = 1 − √3i'),
     L(NOTE, 'polar form must be used to achieve any credit'), L(LPC, 'r found'), L(LPC, 'θ found'),
     L(LPC, '−8 + 0i plotted on an Argand diagram'), L(LPC, 'Shows some knowledge of De Moivre’s theorem'),
     L(HPC, 'One root evaluated in the form a + bi from De Moivre’s expression'), L(HPC, 'Three solutions in polar form')],
 'maths-2021-hl-p1-q2-a': [L(SOL, '|−3 + p| = 5'), L(SOL, 'p = −2 or p = 8'),
     L(Q + LPC, 'x = −3 substituted into equation'), L(Q + MPC, 'relevant quadratic in p found'),
     L(Q + HPC, 'quadratic factorised'), L(Q + HPC, 'one missing or incorrect term in quadratic, but finishes correctly.'),
     L(LN + LPC, '1 linear equation'), L(LN + LPC, 'x = −3 substituted into equation'),
     L(LN + MPC, '1 value of p found'), L(LN + HPC, 'Both linear equations in p given')],
 'maths-2021-hl-p1-q3-a': [L(SOL, 'xz = 2√2'), L(SOL, 'yz = 8√6'), L(SOL, 'xy = 4√3'), L(SOL, '⇒x²y²z² = 384'),
     L(SOL, '⇒xyz = √384 = 8√6 [cm³]'), L(NOTE, '(2√2)(8√6)(4√3) on its own is not awarded any credit.'),
     L(WI + LPC, 'xy, xz, and yz stated'), L(WI + LPC, 'Volume = xyz'), L(WI + MPC, 'xz = 2√2 and yz = 8√6 and xy = 4√3'),
     L(WI + HPC, 'x²y²z² = (2√2)(8√6)(4√3)'), L(IV + LPC, 'xz = 2√2, or similar'), L(IV + HPC, '1 dimension found')],
 'maths-2021-hl-p1-q3-b-ii': [L(SOL, '[as 3^m > 0, then 3^m ≠ −5, so:]'), L(SOL, '= log₃7 − log₃3'), L(SOL, '= log₃7 − 1'),
     L(LPC, 'Some work in writing given equation in the form of that in (b)(i)'), L(LPC, '–5 explicitly excluded'),
     L(LPC, 'x = 3^m'), L(MPC, '3^m = 7/3'), L(HPC, 'm isolated correctly, for example,'), L(HPC, 'm = log₃(7/3)'),
     L(FCM, '3^m = −5 written down, and not explicitly excluded')],
 'maths-2021-hl-p1-q9-a-i': [L(SOL, '95 = Ae^((−0·081)(0)) + 20'), L(SOL, '75 = A'),
     L(LPC, 'Some substitution into function, including A = 75'), L(HPC, 'Equation in A'), L(HPC, 'Substitutes A = 75 and t = 0')],
 'maths-2021-hl-p1-q9-d': [L(SOL, 'dV/dt = −1/20'), L(SOL, 'and dV/dx = 3x²'), L(SOL, 'dx/dt = dV/dt ÷ dV/dx'), L(SOL, '= −4/15 cm/sec'),
     L(NOTE, 'Accept if the rates of change are treated as positive.'),
     L(LPC, 'States a relevant derivative, for example, dV/dt'), L(LPC, 'x³ = 1/64'),
     L(MPC, 'Any two of the following:'), L(MPC, 'dV/dt = −1/20'), L(MPC, 'dV/dx = 3x²'), L(MPC, 'x = 1/4'), L(MPC, 'dx/dt = dV/dt ÷ dV/dx , or similar'),
     L(HPC, 'and any two others from the MPC list above'), L(FCM, 'Unit incorrect or omitted')],
}
