#!/usr/bin/env python3
"""Publish-ready artwork and scheme label keys for Biology completion cards.

The first Biology figure wave covered 2021--2025 only.  The completion layer
also reaches the recovered 2016--2020 papers and groups whole printed tasks, so
it needs the task's complete artwork rather than one leaf-sized fragment.  This
script imports the already-inspected legacy SEC crops where they are complete,
re-renders the handful whose old crop cut a label or a second panel, and emits
the bindings and scheme-stated label keys consumed by ``biology_all.py``.

Every rectangle below was checked against a full-page render.  Coordinates are
PDF points, not pixels, so the output is reproducible at any render scale.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[3]
PAPERS = ROOT / "examiner-reports" / "biology" / "papers"
LEGACY_ROOT = ROOT / "public" / "exam-figures" / "biology"
SOURCE_ROOT = ROOT / "exam-papers" / "biology" / "figures"
AUTHORED = ROOT / "scripts" / "markbank" / "authored"
CATALOGUE = AUTHORED / "biology-completion-figures.json"
BINDINGS_PATH = AUTHORED / "biology-completion-figure-bindings.json"
LABELS_PATH = AUTHORED / "biology-completion-label-keys.json"
MANIFEST = ROOT / "components" / "MarkBank" / "figures.json"


def label(letter: str, meaning: str, asked: bool = True):
    return {
        "letter": letter,
        "meaning": meaning,
        "askedInThisQuestion": asked,
    }


# Meanings are lifted from the matching scheme.  Where the scheme assesses a
# label's role but never gives the structure a name, that limitation is stated
# rather than filled from general biological knowledge.
LABELS = {
    "bio-2016-hl-completion-q5": [
        label("A", "Stigma"),
        label("B", "Pollen tube"),
        label("C", "Egg, female gamete or ovum"),
        label("D", "Pollen grain — the structure whose arrival at A is assessed", False),
        label("E", "The two structures formed from D by mitosis; the scheme does not name them separately", False),
        label("F", "Ovule"),
    ],
    "bio-2016-ol-completion-q7a": [
        label("A", "Eyepiece"), label("B", "Stage or platform")],
    "bio-2016-ol-completion-q14b": [
        label("A", "Kidney"), label("B", "Ureter"),
        label("C", "Urinary bladder — its assessed function is to store urine", False)],
    "bio-2016-ol-completion-q15a": [
        label("Testa", "Protection"),
        label("Cotyledon", "Food store for the seed"),
        label("Plumule", "Part that becomes the shoot"),
        label("Radicle", "Part that becomes the root"),
    ],
    "bio-2016-ol-completion-q15b": [
        label("A", "Protein coat"), label("B", "Nucleic acid, DNA or RNA")],
    "bio-2017-hl-completion-q3": [
        label("A", "Protein"), label("B", "Lipid, phospholipid or fatty acid")],
    "bio-2017-ol-completion-q4": [
        label("A", "Liver"), label("B", "Stomach"), label("C", "Pancreas")],
    "bio-2017-ol-completion-q6": [
        label("A", "Hypha or stolon"), label("B", "Rhizoid"),
        label("C", "Sporangium")],
    "bio-2017-ol-completion-q12b": [
        label("A", "Vagina"), label("B", "Uterus or womb"),
        label("C", "Ovary"), label("D", "Oviduct or Fallopian tube"),
        label("E", "Endometrium or womb lining")],
    "bio-2017-ol-completion-q13b": [
        label("A", "Sensory neuron"), label("B", "Interneuron or relay neuron"),
        label("C", "Motor neuron")],
    "bio-2017-ol-completion-q13c": [
        label("A", "Cerebrum"), label("B", "Medulla oblongata"),
        label("C", "Cerebellum")],
    "bio-2017-ol-completion-q14b": [
        label("A", "Cells marked A; the scheme assesses their chloroplasts rather than a tissue name", False),
        label("B", "Stoma"), label("C", "Guard cells")],
    "bio-2017-ol-completion-q15a": [
        label("A", "Optic nerve"), label("B", "Retina"), label("C", "Lens")],
    "bio-2017-ol-completion-q15b": [
        label("A", "Artery"), label("B", "Vein"), label("C", "Capillary")],
    "bio-2018-hl-completion-q6": [
        label("X", "Bowman's capsule"),
        label("Y", "Distal convoluted tubule or DCT")],
    "bio-2018-ol-completion-q2": [
        label("A", "Ligament"), label("B", "Cartilage"),
        label("C", "Synovial fluid")],
    "bio-2018-ol-completion-q4": [
        label("A", "Penis"), label("B", "Testis"),
        label("C", "Urethra; sperm duct or vas deferens was also allowed")],
    "bio-2018-ol-completion-q6": [
        label("A", "Not named in the marking scheme", False),
        label("B", "Cell wall"),
        label("C", "Not named in the marking scheme", False),
        label("D", "Vacuole"), label("E", "Nucleus")],
    "bio-2018-ol-completion-q12c": [
        label("A", "Hair"), label("B", "Blood vessel or blood vessels"),
        label("C", "Sweat gland")],
    "bio-2018-ol-completion-q14a": [
        label("A", "Semicircular canals — function: balance"),
        label("B", "Cochlea — function: hearing"),
        label("C", "Eardrum — function: hearing")],
    "bio-2018-ol-completion-q15a": [
        label("A", "Stigma"), label("B", "Anther"),
        label("C", "Ovary or ovule"),
        label("D", "Not named in the marking scheme", False)],
    "bio-2018-ol-completion-q15b": [
        label("A", "Phloem"), label("B", "Xylem"), label("C", "Root hair")],
    "bio-2019-hl-completion-q14a": [
        label("A", "Cerebellum"), label("B", "Cerebrum"),
        label("C", "Pituitary gland"), label("D", "Medulla oblongata"),
        label("E", "Spinal cord"), label("F", "Hypothalamus")],
    "bio-2019-ol-completion-q6": [
        label("A", "Eyepiece"), label("B", "Stage"),
        label("C", "Objective lens"),
        label("F", "Candidate-added label for the coarse-focus knob")],
    "bio-2019-ol-completion-q14b": [
        label("A", "Thyroid"), label("B", "Pancreas")],
    "bio-2019-ol-completion-q15a": [
        label("A", "Dendrite"), label("B", "Axon"),
        label("C", "Cell body; nucleus was also allowed")],
    "bio-2019-ol-completion-q15b": [
        label("A", "Renal vein"), label("B", "Renal artery"),
        label("C", "Ureter")],
    "bio-2019-ol-completion-q15c": [
        label("A", "Bud"), label("B", "Pseudopod or false foot")],
    "bio-2020-hl-completion-q4": [
        label("G", "Guanine"), label("J", "Nucleotide"),
        label("K", "Base pair or complementary bases"),
        label("L", "Hydrogen bonding")],
    "bio-2020-hl-completion-q6": [
        label("A", "Site labelled A; the scheme names the released substance as a neurotransmitter", False),
        label("B", "Axon")],
    "bio-2020-hl-completion-q14c": [
        label("A", "Lag stage"), label("B", "Log stage"),
        label("C", "Stationary stage"),
        label("Y", "Population or number of microorganisms")],
    "bio-2020-ol-completion-q3": [
        label("A", "The arrow already printed on the diagram; the scheme does not name it", False),
        label("R", "Candidate-added arrow representing respiration"),
        label("P", "Candidate-added arrow from atmospheric carbon dioxide to plants, representing photosynthesis"),
        label("B", "Candidate-added arrow from fossil fuels to the atmosphere, representing burning")],
    "bio-2020-ol-completion-q12b": [
        label("A", "Larynx"), label("B", "Trachea"),
        label("C", "Bronchiole"), label("D", "Bronchus")],
    "bio-2020-ol-completion-q12c": [
        label("A", "Villus"), label("B", "Alveolus")],
    "bio-2020-ol-completion-q14b": [
        label("A", "Vacuole"), label("B", "Cell wall"),
        label("C", "Cell membrane"), label("D", "Mitochondria")],
    "bio-2020-ol-completion-q15a": [
        label("A", "Lens"), label("B", "Sclera"),
        label("C", "Optic nerve"), label("D", "Retina")],
    "bio-2020-ol-completion-q15c": [
        label("A", "Penis"), label("B", "Urethra"),
        label("C", "Sperm duct"), label("D", "Testes")],
    "bio-2021-hl-completion-q5": [
        label("A", "Ovulation"), label("B", "Morula"),
        label("C", "Blastocyst"), label("D", "Implantation")],
    "bio-2021-ol-completion-q7": [
        label("X", "Candidate-added mark at a synovial joint; the accepted joint type depends on its placement"),
        label("F", "Candidate-added mark on the femur")],
    "bio-2021-ol-completion-q16a": [
        label("A", "Semicircular canals — function: balance"),
        label("B", "Cochlea — function: hearing or conversion of vibrations to nerve impulses"),
        label("C", "Eardrum — function: detect sound or pass vibrations to the middle ear")],
    "bio-2022-hl-completion-q15b": [
        label("A", "Cortex"), label("B", "Medulla or pyramid"),
        label("C", "Pelvis")],
    "bio-2023-ol-completion-q5": [
        label("A", "Eyepiece"), label("B", "Objective lens")],
    "bio-2023-ol-completion-q7": [
        label("A", "Dendrite"), label("B", "Axon"),
        label("C", "Schwann cell or myelin sheath")],
    "bio-2023-ol-completion-q16b": [
        label("X", "Iris"), label("Y", "Cornea"), label("Z", "Lens"),
        label("d", "Diameter of the pupil", False)],
    "bio-2024-ol-completion-q2": [
        label("X", "The bud"),
        label("Y", "The parent yeast cell; X is the bud", False),
        label("Z", "Nucleus")],
    "bio-2025-hl-completion-q4": [
        label("X", "Phospholipid"), label("Y", "Protein")],
    "bio-2025-hl-completion-q16a": [
        label("A", "Sporangium"), label("B", "Spore"), label("C", "Stolon")],
    "bio-2025-hl-completion-q16b": [
        label("A", "Capillary"), label("B", "Alveolus"),
        label("C", "Red blood cell"), label("X", "Carbon dioxide or CO2"),
        label("Y", "Oxygen or O2")],
    "bio-2025-hl-completion-q17d": [
        label("A", "Head — role: holds the nucleus, DNA or genes"),
        label("B", "Tail — role: movement")],
    "bio-2025-ol-completion-q15c": [
        label("A", "Sperm duct"), label("B", "Prostate gland"),
        label("C", "Testis")],
    "bio-2025-ol-completion-q17b": [
        label("P", "Cartilage"), label("Q", "Synovial fluid"),
        label("R", "Ligament")],
    "bio-2025-ol-completion-q17c": [
        label("A", "Intercostal muscle"), label("B", "Bronchus"),
        label("C", "Trachea")],
}


# Later inspected figures that are already live in the central manifest.
EXISTING = {
    "bio-2021-ol-completion-q7": "biology-2021-OL-paper1-p07-i0",
    "bio-2021-ol-completion-q16a": "biology-2021-OL-paper2-p07-i1",
    "bio-2023-ol-completion-q5": "biology-2023-OL-paper1-p06-i0",
    "bio-2023-ol-completion-q16b": "biology-2023-OL-paper2-p07-i1",
    "bio-2024-ol-completion-q2": "biology-2024-OL-paper1-p04-i0",
    "bio-2025-hl-completion-q4": "biology-2025-HL-paper1-p06-i1",
    "bio-2025-hl-completion-q16a": "biology-2025-HL-paper2-p07-i1",
    "bio-2025-hl-completion-q16b": "biology-2025-HL-paper2-p07-i0",
    "bio-2025-hl-completion-q17d": "biology-2025-HL-paper2-p10-i0",
    "bio-2025-ol-completion-q17b": "biology-2025-OL-paper2-p09-i0",
}


def spec(card_id, ref, file, theme, *, legacy=None, pdf=None, page=None,
         rect=None, visible=None):
    return {
        "cardId": card_id,
        "questionRef": ref,
        "file": file,
        "theme": theme,
        "legacy": legacy,
        "pdf": pdf,
        "page": page,
        "rect": rect,
        "visible": visible,
    }


# Complete legacy crops, opened and checked against the corresponding paper.
LEGACY = [
    spec("bio-2016-hl-completion-q5", "2016 HL Q5", "biology-2016-HL-paper-p05-i90.png", "flowering-plant sexual reproduction from pollination through fertilisation", legacy="biology-2016-hl-q5-flowering-plant-reproduction.png"),
    spec("bio-2016-ol-completion-q7a", "2016 OL Q7(a)", "biology-2016-OL-paper-p05-i90.png", "a complete light microscope with the eyepiece and stage leaders", legacy="biology-2016-ol-microscope-labelled.png"),
    spec("bio-2016-ol-completion-q14b", "2016 OL Q14(b)", "biology-2016-OL-paper-p13-i90.png", "the complete human urinary system", legacy="biology-2016-ol-human-urinary-system.png"),
    spec("bio-2016-ol-completion-q15a", "2016 OL Q15(a)", "biology-2016-OL-paper-p13-i91.png", "a seed section with the four printed structure names used by the matching task", legacy="biology-2016-ol-seed-structure.png"),
    spec("bio-2016-ol-completion-q15b", "2016 OL Q15(b)", "biology-2016-OL-paper-p13-i92.png", "a virus with intact A and B leader lines", legacy="biology-2016-ol-microbe-labelled-ab.png"),
    spec("bio-2017-ol-completion-q6", "2017 OL Q6", "biology-2017-OL-paper-p04-i90.png", "Rhizopus with its horizontal hyphae, rhizoids and sporangia", legacy="biology-2017-ol-q6-rhizopus.png"),
    spec("bio-2017-ol-completion-q12b", "2017 OL Q12(b)", "biology-2017-OL-paper-p10-i90.png", "the complete human female reproductive system", legacy="biology-2017-ol-q9-female-reproductive-system.png"),
    spec("bio-2017-ol-completion-q13b", "2017 OL Q13(b)", "biology-2017-OL-paper-p11-i90.png", "all three neurons in a human reflex arc", legacy="biology-2017-ol-reflex-arc-neurons.png"),
    spec("bio-2017-ol-completion-q15a", "2017 OL Q15(a)", "biology-2017-OL-paper-p14-i90.png", "a section through the human eye with A, B and C intact", legacy="biology-2017-ol-q15-human-eye.png"),
    spec("bio-2018-ol-completion-q4", "2018 OL Q4", "biology-2018-OL-paper-p03-i90.png", "the complete human male reproductive system", legacy="biology-2018-ol-q4-male-reproductive-system.png"),
    spec("bio-2018-ol-completion-q6", "2018 OL Q6", "biology-2018-OL-paper-p04-i90.png", "a complete plant cell with all five leaders", legacy="biology-2018-ol-q6-plant-cell.png"),
    spec("bio-2018-ol-completion-q12c", "2018 OL Q12(c)", "biology-2018-OL-paper-p10-i90.png", "a full section through human skin", legacy="biology-2018-ol-skin-section.png"),
    spec("bio-2018-ol-completion-q14a", "2018 OL Q14(a)", "biology-2018-OL-paper-p12-i90.png", "the human ear with its printed contextual labels and A, B and C", legacy="biology-2018-ol-q14-human-ear.png"),
    spec("bio-2018-ol-completion-q15a", "2018 OL Q15(a)", "biology-2018-OL-paper-p14-i90.png", "a complete longitudinal section through a flower", legacy="biology-2018-ol-q15-flower-section.png"),
    spec("bio-2019-ol-completion-q6", "2019 OL Q6", "biology-2019-OL-paper-p05-i90.png", "the paper's laboratory microscope photograph", legacy="biology-2019-ol-q6-microscope-labelled.png", visible=["A", "B", "C"]),
    spec("bio-2019-ol-completion-q14b", "2019 OL Q14(b)", "biology-2019-OL-paper-p07-i90.png", "the two human endocrine glands and their anatomical context", legacy="biology-2019-ol-endocrine-glands-labelled.png"),
    spec("bio-2019-ol-completion-q15a", "2019 OL Q15(a)", "biology-2019-OL-paper-p08-i90.png", "a complete motor neuron", legacy="biology-2019-ol-q15-motor-neuron-labelled.png"),
    spec("bio-2019-ol-completion-q15b", "2019 OL Q15(b)", "biology-2019-OL-paper-p08-i91.png", "a human kidney and its attached vessels and ureter", legacy="biology-2019-ol-q15-human-kidney-labelled.png"),
    spec("bio-2019-ol-completion-q15c", "2019 OL Q15(c)", "biology-2019-OL-paper-p09-i90.png", "the complete yeast and amoeba comparison", legacy="biology-2019-ol-q15-yeast-amoeba.png"),
    spec("bio-2020-hl-completion-q14c", "2020 HL Q14(c)", "biology-2020-HL-paper-p07-i90.png", "the full microorganism population-growth curve and both axes", legacy="biology-2020-hl-microbial-growth-curve.png"),
    spec("bio-2020-ol-completion-q3", "2020 OL Q3", "biology-2020-OL-paper-p04-i90.png", "the incomplete carbon-cycle diagram on which candidates add arrows", legacy="biology-2020-ol-q3-carbon-cycle.png", visible=["A"]),
    spec("bio-2020-ol-completion-q12b", "2020 OL Q12(b)", "biology-2020-OL-paper-p04-i90.png", "the complete human breathing system", legacy="biology-2020-ol-respiratory-system.png"),
    spec("bio-2020-ol-completion-q14b", "2020 OL Q14(b)", "biology-2020-OL-paper-p06-i90.png", "a complete labelled plant cell", legacy="biology-2020-ol-plant-cell.png"),
    spec("bio-2020-ol-completion-q15a", "2020 OL Q15(a)", "biology-2020-OL-paper-p07-i90.png", "a section through the human eye with all four leaders", legacy="biology-2020-ol-human-eye.png"),
    spec("bio-2020-ol-completion-q15c", "2020 OL Q15(c)", "biology-2020-OL-paper-p07-i91.png", "the complete human male reproductive system", legacy="biology-2020-ol-male-reproductive-system.png"),
]


# Fresh crops replacing clipped legacy extractions or covering later gaps.
CROPS = [
    spec("bio-2017-hl-completion-q3", "2017 HL Q3", "biology-2017-HL-paper-p04-i91.png", "the complete cell-membrane ultrastructure diagram", pdf="2017-hl-paper.pdf", page=4, rect=(90, 65, 495, 255)),
    spec("bio-2017-ol-completion-q4", "2017 OL Q4", "biology-2017-OL-paper-p03-i91.png", "the complete human digestive-system figure with all three lettered leaders", pdf="2017-ol-paper.pdf", page=3, rect=(180, 355, 530, 515)),
    spec("bio-2017-ol-completion-q13c", "2017 OL Q13(c)", "biology-2017-OL-paper-p11-i91.png", "the complete sagittal section through the human brain", pdf="2017-ol-paper.pdf", page=11, rect=(55, 600, 265, 780)),
    spec("bio-2017-ol-completion-q14b", "2017 OL Q14(b)", "biology-2017-OL-paper-p12-i91.png", "the complete leaf cross-section and its A, B and C leaders", pdf="2017-ol-paper.pdf", page=12, rect=(190, 420, 355, 600)),
    spec("bio-2017-ol-completion-q15b", "2017 OL Q15(b)", "biology-2017-OL-paper-p14-i91.png", "all three blood-vessel cross-sections, structural captions and A, B and C", pdf="2017-ol-paper.pdf", page=14, rect=(90, 425, 555, 615)),
    spec("bio-2018-hl-completion-q6", "2018 HL Q6", "biology-2018-HL-paper-p06-i91.png", "the complete nephron, associated blood supply and target-area box", pdf="2018-hl-paper.pdf", page=6, rect=(145, 60, 390, 350)),
    spec("bio-2018-ol-completion-q2", "2018 OL Q2", "biology-2018-OL-paper-p02-i91.png", "the complete synovial-joint diagram and all three leaders", pdf="2018-ol-paper.pdf", page=2, rect=(175, 335, 330, 490)),
    spec("bio-2018-ol-completion-q15b", "2018 OL Q15(b)", "biology-2018-OL-paper-p14-i91.png", "the complete transverse section of a dicot root", pdf="2018-ol-paper.pdf", page=14, rect=(220, 455, 420, 580)),
    spec("bio-2019-hl-completion-q14a", "2019 HL Q14(a)", "biology-2019-HL-paper-p07-i91.png", "the complete central-nervous-system figure and all six lettered leaders", pdf="2019-hl-040-paper.pdf", page=7, rect=(135, 170, 480, 325)),
    spec("bio-2020-hl-completion-q4", "2020 HL Q4", "biology-2020-HL-paper-p06-i91.png", "the complete DNA structural diagram with G, J, K and L intact", pdf="2020-hl-038-paper.pdf", page=6, rect=(125, 75, 515, 270)),
    spec("bio-2020-hl-completion-q6", "2020 HL Q6", "biology-2020-HL-paper-p08-i91.png", "the complete sensory neuron, its direction box and all printed labels", pdf="2020-hl-038-paper.pdf", page=8, rect=(80, 70, 480, 270)),
    spec("bio-2020-ol-completion-q12c", "2020 OL Q12(c)", "biology-2020-OL-paper-p04-i91.png", "both exchange structures, villus A and alveolus B, in one crop", pdf="2020-ol-040-paper.pdf", page=4, rect=(165, 470, 520, 635)),
    spec("bio-2021-hl-completion-q5", "2021 HL Q5", "biology-2021-HL-paper-p07-i90.png", "the complete embryo-development sequence from ovulation to implantation", pdf="2021-hl-038-paper.pdf", page=7, rect=(140, 80, 485, 370)),
    spec("bio-2022-hl-completion-q15b", "2022 HL Q15(b)", "biology-2022-HL-paper-p06-i90.png", "the complete kidney and nephron pair, including all printed anatomical labels", pdf="2022-hl-040-paper.pdf", page=6, rect=(115, 140, 535, 405)),
    spec("bio-2023-ol-completion-q7", "2023 OL Q7", "biology-2023-OL-paper-p08-i90.png", "the complete neuron and candidate direction-arrow box", pdf="2023-ol-038-paper.pdf", page=8, rect=(85, 75, 505, 280)),
    spec("bio-2025-ol-completion-q15c", "2025 OL Q15(c)", "biology-2025-OL-paper-p06-i90.png", "the complete male reproductive-system figure without the preceding foetus diagram", pdf="2025-ol-040-paper.pdf", page=6, rect=(390, 535, 540, 730)),
    spec("bio-2025-ol-completion-q17c", "2025 OL Q17(c)", "biology-2025-OL-paper-p10-i90.png", "the complete human breathing system, alveolus inset and diaphragm", pdf="2025-ol-040-paper.pdf", page=10, rect=(320, 100, 545, 355)),
]


def source_dir(filename: str):
    parts = filename.split("-")
    return SOURCE_ROOT / f"{parts[1]}-{parts[2].lower()}"


def description(row):
    visible = row["visible"] or [x["letter"] for x in LABELS[row["cardId"]]]
    named = ", ".join(visible)
    return (
        f"Complete inspected SEC artwork for {row['questionRef']}, showing "
        f"{row['theme']}. Every printed label used by the task ({named}) and "
        "its leader line are intact; no marking-scheme answer overlay is present."
    )


def main():
    manifest = json.loads(MANIFEST.read_text())
    missing_existing = sorted(set(EXISTING.values()) - set(manifest))
    if missing_existing:
        raise SystemExit(f"existing Biology figure key(s) missing: {missing_existing}")

    rows = LEGACY + CROPS
    new_ids = {row["cardId"] for row in rows}
    all_ids = new_ids | set(EXISTING)
    if all_ids != set(LABELS):
        raise SystemExit(
            f"figure/label id drift: no figure={sorted(set(LABELS)-all_ids)}, "
            f"no labels={sorted(all_ids-set(LABELS))}")

    catalogue = []
    bindings = dict(EXISTING)
    for row in rows:
        out_dir = source_dir(row["file"])
        out_dir.mkdir(parents=True, exist_ok=True)
        destination = out_dir / row["file"]
        if row["legacy"]:
            source = LEGACY_ROOT / row["legacy"]
            if not source.exists():
                raise SystemExit(f"legacy Biology crop missing: {source}")
            shutil.copyfile(source, destination)
        else:
            source = PAPERS / row["pdf"]
            with pymupdf.open(source) as doc:
                page = doc[row["page"] - 1]
                clip = pymupdf.Rect(*row["rect"])
                if not page.rect.contains(clip):
                    raise SystemExit(f"crop outside page: {row['cardId']} {clip}")
                pix = page.get_pixmap(
                    matrix=pymupdf.Matrix(3, 3), clip=clip, alpha=False)
                pix.save(destination)

        figure_key = row["file"].removesuffix(".png")
        bindings[row["cardId"]] = figure_key
        visible = row["visible"] or [x["letter"] for x in LABELS[row["cardId"]]]
        visible_set = set(visible)
        catalogue.append({
            "file": row["file"],
            "kind": "figure",
            "drawingComplete": True,
            "truncated": False,
            "description": description(row),
            "lettersVisible": visible,
            "labelMeanings": [
                {"letter": item["letter"], "meaning": item["meaning"]}
                for item in LABELS[row["cardId"]]
                if item["letter"] in visible_set
            ],
            "questionRef": row["questionRef"],
            "notes": (
                "Completion-layer artwork. Checked against the full paper page "
                "and decoded only from the corresponding marking scheme."),
        })

    CATALOGUE.write_text(
        json.dumps(catalogue, ensure_ascii=False, indent=1) + "\n")
    BINDINGS_PATH.write_text(
        json.dumps(dict(sorted(bindings.items())), ensure_ascii=False, indent=1) + "\n")
    LABELS_PATH.write_text(
        json.dumps(dict(sorted(LABELS.items())), ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {len(catalogue)} new Biology figures")
    print(f"wrote {len(bindings)} bindings and {len(LABELS)} label keys")


if __name__ == "__main__":
    main()
