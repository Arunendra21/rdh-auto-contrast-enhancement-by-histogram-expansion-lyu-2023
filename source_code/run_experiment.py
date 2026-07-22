"""Standalone experiment runner: runs the CE-RDH engine on the standard set
and writes figures/ + outputs/metrics.json. (build_deliverables.py also calls
this internally.)"""
import os, sys
TK = os.path.join(os.path.dirname(__file__), "..", "..", "_toolkit")
sys.path.insert(0, TK)
import ce_experiment as CE
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
res = CE.run_ce(os.path.join(ROOT, "figures"), os.path.join(ROOT, "outputs"),
                iters_list=[2, 4, 6, 8, 10], demo_key="lena")
print("Done. Reversible everywhere:",
      all(res[n][it]["reversible"] for n in res for it in res[n]))
