# Open questions for you

These are the decisions that change what gets built next. Everything in the repository so far does not
depend on them; the next phase does.

1. **Which decisions will the citizens inform first?** Product concept tests, price points, policy
   messaging, service design, or something else? The test plan (level 4, "effects") has to be built around
   the kind of stimulus you care about, and the calibration survey has to ask about it.

2. **Who is the first client: public sector, private sector, or the people sector?** This changes the
   topics (policy attitudes vs consumer behaviour vs civic participation), the acceptable error, and in
   Singapore whether a government partnership (AI Singapore, IPS, the SSRC programme) is the route to data.

3. **Do you agree with US first and Singapore in parallel, China later with Taiwan as the Mandarin pilot?**
   If Singapore must be first for business reasons, say so: the plan changes to commissioning the
   Singapore survey immediately, since that is the only way to get individual-level and experiment data there.

4. **Are the proposed pass marks acceptable?** (`docs/02_how_we_measure_accuracy.md`, section 3). In
   particular, is a 6-point average error on answer shares good enough for your decisions, or do you need
   survey-grade precision (2-3 points), which would mean the simulator is used to *supplement* surveys
   rather than replace them?

5. **Budget for human ground truth.** The research is clear that a small real sample per country and
   topic is what makes simulations usable. Is roughly S$60-120k for a 2,000-person Singapore survey with a
   retest and two experiments acceptable for phase 2? For the US, open data covers phase 1.

6. **Model access.** The simulator's own bulk calls are billed separately from this chat session, so a
   large run needs an Anthropic API key. Without one I ran a bounded stress test by writing predictions
   in-session (`docs/results/stress_test/`). To run thousands of questions, repeats and prompt variants I need an Anthropic API key (and, for the China/Taiwan work, access to
   Qwen or DeepSeek, which can be self-hosted or via their APIs). Which models are you willing to use and
   where may data be sent?

7. **Data access I cannot complete alone.** World Values Survey wave 7 (Singapore and China microdata)
   must be downloaded through a web form; CGSS and CFPS need a registration or application in your name or
   an institution's; Pew ATP and ANES need free accounts. Are you happy to create those accounts, or should
   we route through a university partner?

8. **Languages for Singapore.** Should the first Singapore version be English only (how most surveys are
   fielded), or should we build Mandarin, Malay and Tamil variants from the start and test whether language
   changes the answers?

9. **Individual twins or groups?** The evidence says group-level simulation is where the value is today
   and individual twins are weak. Do you need individual-level twins (for example for a panel product), or
   is segment-level enough for the first product?

10. **Publication.** A Singapore LLM-opinion benchmark would be a first. Do you want results published
    (which helps credibility and partnerships) or kept private?
