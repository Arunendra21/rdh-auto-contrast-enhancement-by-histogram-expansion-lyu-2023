import os, sys, json
TK = os.path.join(os.path.dirname(__file__), "..", "..", "_toolkit")
sys.path.insert(0, TK)
import build_ce_paper as B
FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
paper = [p for p in json.load(open(os.path.join(TK, "papers.json"))) if p["id"] == 7][0]

def slides(fig):
    return [
     {"title": "Motivation", "bullets": [
        "Low-contrast images (medical, surveillance) are hard to read.",
        "Classic contrast enhancement is irreversible and destroys the original.",
        "We want enhancement AND a hidden payload AND exact recovery."]},
     {"title": "Problem Statement", "bullets": [
        "Enhance global contrast reversibly.",
        "Embed a large payload during enhancement.",
        "Keep brightness stable and recover the exact original."]},
     {"title": "Existing Work", "bullets": [
        "Ni 2006 histogram shifting: fidelity, tiny capacity.",
        "Wu-Huang 2015 CE-RDH: enhances contrast by splitting the two peaks.",
        "This paper: automatic histogram expansion with brightness control."]},
     {"title": "Proposed Method", "bullets": [
        "Iteratively expand the two tallest histogram bins outward.",
        "Each expansion embeds one bit per peak pixel and widens the tonal range.",
        "Average brightness guides how far to expand (automatic stopping)."],
      "image": fig("fig_demo.png")},
     {"title": "Workflow", "bullets": [
        "Pre-shift boundary pixels (location map).",
        "Repeat: pick two peaks -> expand -> embed bits.",
        "Stop when brightness/quality criterion is met.",
        "Receiver reverses every iteration -> exact original."]},
     {"title": "Mathematical Model", "bullets": [
        "Peaks a<b (two tallest bins).",
        "Shift: v<a -> v-1 ; v>b -> v+1 (spread).",
        "Embed: a-pixel bit1->a-1 ; b-pixel bit1->b+1.",
        "Contrast rises with iterations; PSNR falls monotonically."]},
     {"title": "Experimental Setup", "bullets": [
        "USC-SIPI grayscale images, iterations 2..10.",
        "Metrics: payload (bpp), PSNR, RMS contrast, entropy.",
        "Bit-exact reversibility check every run."]},
     {"title": "Results", "bullets": [
        "Contrast (RMS, entropy) rises with iterations.",
        "Payload grows with enhancement strength.",
        "All runs bit-exact reversible."],
      "image": fig("fig_tradeoff.png")},
     {"title": "Advantages", "bullets": [
        "Enhancement and embedding in one pass.",
        "Automatic, brightness-aware stopping.",
        "Fully reversible, no external side channel needed."]},
     {"title": "Limitations", "bullets": [
        "Full-tonal-range images enhance less (boundary limit).",
        "Strong enhancement lowers PSNR.",
        "Contrast metric is global, not local."]},
     {"title": "Future Scope", "bullets": [
        "Local/ROI contrast enhancement.",
        "Perceptual quality-guided stopping.",
        "Extend to color and medical modalities."]},
     {"title": "Conclusion", "bullets": [
        "Reproduced automatic CE-RDH via histogram expansion.",
        "Confirmed the contrast-vs-fidelity trade-off and reversibility.",
        "Consistent with the paper's qualitative claims."]},
     {"title": "References", "bullets": [
        "Lyu, Yue, Yin. Automatic CE via Histogram Expansion. JVCIR 92, 2023.",
        "Wu, Dugelay, Shi. CE-RDH. IEEE SPL 22(1), 2015.",
        "Ni et al. Reversible Data Hiding. IEEE TCSVT 16(3), 2006."]},
    ]

content = dict(
 title="Reproduction Study: Automatic Contrast Enhancement RDH via Histogram Expansion (Lyu et al., 2023)",
 abstract=("This report reproduces the automatic contrast-enhancement reversible data hiding scheme of "
   "Lyu, Yue and Yin, in which image contrast is improved by expanding the two tallest histogram bins "
   "outward while a payload is embedded, and the global average brightness is used to control the "
   "enhancement automatically. We implement the reversible histogram-expansion core, evaluate it on "
   "standard grayscale images, and confirm that contrast (RMS and entropy) rises with the number of "
   "expansion iterations while the process remains bit-exact reversible. The reproduced fidelity/contrast "
   "trade-off matches the trend reported in the paper."),
 keywords="reversible data hiding, contrast enhancement, histogram expansion, brightness preservation, entropy",
 introduction=(
   "Contrast enhancement (CE) improves the readability of low-contrast images, but conventional CE "
   "(e.g. histogram equalisation) is irreversible and permanently alters pixels. Reversible data hiding "
   "with contrast enhancement (RDHCE) couples enhancement with data embedding so that, after the payload "
   "is extracted, the exact original is restored. Lyu et al. propose an automatic scheme that expands the "
   "image histogram to raise contrast and uses the average brightness to decide how much enhancement to "
   "apply. This report reproduces the histogram-expansion core and its contrast/fidelity behaviour."),
 related_work=(
   "Ni et al. (2006, reproduced as Paper 01) introduced histogram shifting with high fidelity but tiny "
   "capacity. Wu, Dugelay and Shi (2015) turned histogram shifting into contrast enhancement by "
   "repeatedly splitting the two highest bins. Subsequent RDHCE works add brightness preservation, "
   "two-dimensional histograms and region-of-interest control (several reproduced in this collection). "
   "Lyu et al. contribute an automatic, brightness-guided stopping rule for the expansion."),
 methodology=(
   "The image histogram is iteratively expanded. In each iteration the two tallest bins a<b are located; "
   "all pixels below a are shifted down by one and all pixels above b up by one, spreading the histogram "
   "and widening the tonal range (this is the contrast gain). One payload bit is then embedded per peak "
   "pixel by expanding each peak outward. Repeating over several iterations progressively enhances "
   "contrast; the average brightness is monitored so enhancement stops at an appropriate level. Boundary "
   "pixels are pre-shifted and recorded in a location map to avoid overflow/underflow.\n\n"
   "### Automatic control\n"
   "Because each iteration both enhances and embeds, the number of iterations trades payload and contrast "
   "against fidelity; the brightness criterion selects an operating point automatically."),
 math=(
   "Let a<b be the two tallest bins. Spread: v' = v-1 for v<a and v' = v+1 for v>b. Embed: a-pixel with "
   "bit x maps to a-x (i.e. a or a-1); b-pixel with bit y maps to b+y. After K iterations the tonal range "
   "widens by up to 2K levels, increasing RMS contrast sigma. Extraction reverses each iteration in LIFO "
   "order and restores boundary pixels from the location map, giving exact recovery."),
 algorithm=(
   "### Embedding\n- Pre-shift 0/255 pixels; record location map.\n"
   "- For k=1..K: find two peaks; spread outer regions; embed bits into peaks.\n"
   "- Stop when the brightness/quality criterion is met.\n\n"
   "### Extraction / recovery\n- For k=K..1: read+collapse each peak; un-spread outer regions.\n"
   "- Restore boundary pixels -> exact original + payload."),
 comparison=(
   "The reproduction confirms the paper's central claims: histogram expansion raises contrast (RMS and "
   "entropy increase) and the scheme is exactly reversible. Absolute PSNR/contrast numbers differ because "
   "the paper's automatic brightness-based stopping and its exact peak-selection heuristics are not fully "
   "specified and its test images differ; the qualitative trade-off is reproduced."),
 cmp_rows=[
   ["Contrast increases with embedding", "Yes", "Yes (RMS & entropy up)"],
   ["Exact reversibility", "Yes", "Yes (bit-exact, verified)"],
   ["Brightness-aware automatic control", "Yes (average brightness)", "Iteration count as proxy control"],
   ["Fidelity vs contrast trade-off", "Reported", "Reproduced (Fig. 2)"]],
 discussion=(
   "Histogram expansion is an elegant way to obtain contrast enhancement for free during embedding. The "
   "reproduction shows the expected monotone trade-off: more iterations mean more payload and more "
   "contrast but lower PSNR. The brightness criterion in the paper is essentially a principled way to "
   "choose where on this curve to stop."),
 limitations=(
   "- Images already spanning the full [0,255] range enhance little (boundary limit).\n"
   "- Strong enhancement reduces PSNR, as expected for CE.\n"
   "- The reproduction uses iteration count as the control proxy rather than the paper's exact brightness rule."),
 future=(
   "Local and ROI-restricted contrast enhancement, perceptual-quality-guided stopping, and extensions to "
   "colour and medical modalities (all represented by other papers in this collection)."),
 conclusion=(
   "We reproduced the automatic histogram-expansion RDHCE scheme, confirming reversible contrast "
   "enhancement and the fidelity/contrast trade-off reported by Lyu et al."),
 refs=[
   'W.-L. Lyu, Y.-J. Yue, and Z. Yin, "Reversible data hiding based on automatic contrast enhancement using histogram expansion," J. Vis. Commun. Image R., vol. 92, 2023.',
   'H.-T. Wu, J.-L. Dugelay, and Y.-Q. Shi, "Reversible image data hiding with contrast enhancement," IEEE Signal Process. Lett., vol. 22, no. 1, pp. 81-85, 2015.',
   'Z. Ni, Y.-Q. Shi, N. Ansari, and W. Su, "Reversible data hiding," IEEE Trans. Circuits Syst. Video Technol., vol. 16, no. 3, pp. 354-362, 2006.',
   'Z. Wang et al., "Image quality assessment: from error visibility to structural similarity," IEEE TIP, vol. 13, no. 4, 2004.'],
 readme_summary=("Automatic contrast-enhancement RDH by iterative histogram expansion (Lyu et al. 2023). "
   "Reproduces reversible contrast enhancement and the fidelity/contrast trade-off on standard images."),
 dataset="Eight 512x512 USC-SIPI grayscale images in ../_toolkit/images/. No download needed.",
 outputs_desc=("- outputs/metrics.json — payload, PSNR, RMS contrast, entropy, reversibility for iterations 2..10.\n"
   "- figures/fig_demo, fig_tradeoff, fig_summary — visual+histograms, trade-off curve, per-image bars."),
 notes=("## What was reproduced\nThe reversible histogram-expansion contrast-enhancement core (shared engine "
   "`_toolkit/ce_rdh.py`) run for 2..10 iterations on the standard image set, with bit-exact reversibility "
   "verified every run.\n\n## Reproduced vs reported\nContrast rises with embedding and the process is exactly "
   "reversible, matching the paper. The paper's *automatic* brightness-based stopping rule and exact peak "
   "heuristics are not fully specified, so the reproduction uses iteration count as the control knob and "
   "reports the resulting trade-off honestly.\n\n## Honesty note\nAll numbers come from the included code on "
   "the bundled images; only cells labelled 'reported' reflect the paper."),
 slides=slides,
)

res, pdf = B.build(paper, FOLDER, content, iters_list=(2, 4, 6, 8, 10), demo_key="lena",
                   deck_title="Brightening the Picture, Losing Nothing:\nReversible Contrast Enhancement by Histogram Expansion",
                   deck_subtitle="A reproduction of Lyu, Yue & Yin (JVCIR, 2023)")
print("PDF:", os.path.exists(pdf) if pdf else False)
