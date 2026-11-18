/** Primary studies checked 10 November 2026. Scope and scheduling limits travel with each claim. */
export const STUDY_EVIDENCE = [
  {
    id: "retrieval",
    title: "Try to remember before rereading",
    guidance: "Attempt an answer from memory before opening your notes.",
    context:
      "In experiments with university students learning prose, retrieval practice improved delayed recall compared with repeated study. This does not establish a universal session length.",
    citation: "Roediger & Karpicke (2006)",
    url: "https://learninglab.psych.purdue.edu/downloads/2006/2006_Roediger_Karpicke_PsychSci.pdf",
  },
  {
    id: "spacing",
    title: "Return to learning over time",
    guidance:
      "Revisit material on separate days and use your results to adjust the next check.",
    context:
      "Cepeda and colleagues studied fact learning across different study gaps and test delays. Helpful spacing depended on how long the information needed to be retained; there was no single best interval.",
    citation: "Cepeda et al. (2008)",
    url: "https://www.evullab.org/pdf/CepedaVulRohrerWixtedPashler-PS-2008.pdf",
  },
  {
    id: "feedback",
    title: "Check and correct your attempt",
    guidance:
      "Compare your answer with a trusted answer, worked example or marking scheme, including answers you were unsure about.",
    context:
      "In general-knowledge experiments, feedback improved later recall of errors and correct answers initially given with low confidence. Confidence alone is not evidence of successful recall.",
    citation: "Butler, Karpicke & Roediger (2008)",
    url: "https://learninglab.psych.purdue.edu/downloads/2008/2008_Butler_Karpicke_Roediger_JEPLMC.pdf",
  },
  {
    id: "interleaving",
    title: "Mix familiar problem types when appropriate",
    guidance:
      "After learning how to solve them, try a mixture of problem types so you have to choose the method yourself.",
    context:
      "A seventh-grade mathematics experiment found benefits on delayed tests from interleaved practice. This supports mixing mathematical problem types, not a claim that switching school subjects always improves learning.",
    citation: "Rohrer, Dedrick & Stershic (2015)",
    url: "https://files.eric.ed.gov/fulltext/ED557355.pdf",
  },
] as const;
