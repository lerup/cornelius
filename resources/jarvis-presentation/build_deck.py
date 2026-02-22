#!/usr/bin/env python3
"""Build JARVIS presentation deck v2 with embedded logo assets."""
import base64, os, subprocess

DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(DIR, "logo-white.png")
SYMBOL_PATH = os.path.join(DIR, "symbol-white.png")

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_B64 = b64(LOGO_PATH)
SYMBOL_B64 = b64(SYMBOL_PATH)
LOGO_SRC = f"data:image/png;base64,{LOGO_B64}"
SYMBOL_SRC = f"data:image/png;base64,{SYMBOL_B64}"

TOTAL = 14

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JARVIS - Inflection</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@page {{ size: 1920px 1080px; margin: 0; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Inter', -apple-system, 'Helvetica Neue', sans-serif; background: #111; color: #fff; }}
.slide {{ width: 1920px; height: 1080px; position: relative; background: #000; overflow: hidden; page-break-after: always; page-break-inside: avoid; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
@media screen {{ body {{ padding: 40px; }} .slide {{ margin: 0 auto 40px auto; box-shadow: 0 2px 60px rgba(255,255,255,0.04); }} }}
@media print {{ body {{ padding: 0; background: #000; }} .slide {{ margin: 0; box-shadow: none; }} }}
.pad {{ padding: 80px; }}
.flex {{ display: flex; }}
.col {{ flex-direction: column; }}
.center {{ align-items: center; justify-content: center; }}
.gap-40 {{ gap: 40px; }}
.gap-24 {{ gap: 24px; }}
.gap-16 {{ gap: 16px; }}
.grow {{ flex: 1; }}
.bg-black {{ background: #000; }}
.bg-dark {{ background: #141414; }}
.bg-mid {{ background: #1A1A1A; }}
.bg-grey {{ background: #808080; }}
.bg-verdant {{ background: #B3BCB5; }}
.c-white {{ color: #fff; }}
.c-grey {{ color: #808080; }}
.c-verdant {{ color: #B3BCB5; }}
.c-azure {{ color: #B4BACC; }}
.c-black {{ color: #000; }}
.c-dim {{ color: #555; }}
.t-hero {{ font-size: 96px; font-weight: 500; letter-spacing: -3px; }}
.t-large {{ font-size: 64px; font-weight: 500; letter-spacing: -2px; line-height: 1.15; }}
.t-headline {{ font-size: 42px; font-weight: 500; letter-spacing: -1px; line-height: 1.25; }}
.t-sub {{ font-size: 26px; font-weight: 400; letter-spacing: -0.5px; }}
.t-body {{ font-size: 19px; font-weight: 400; line-height: 1.6; }}
.t-body-lg {{ font-size: 22px; font-weight: 400; line-height: 1.5; }}
.t-label {{ font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }}
.t-small {{ font-size: 14px; font-weight: 400; }}
.t-tiny {{ font-size: 12px; font-weight: 400; }}
.t-medium {{ font-weight: 500; }}
.t-semi {{ font-weight: 600; }}
.t-bold {{ font-weight: 700; }}
.t-center {{ text-align: center; }}
table {{ border-collapse: collapse; width: 100%; }}
th {{ background: #B3BCB5; color: #000; font-size: 11px; font-weight: 700; text-align: left; padding: 10px 14px; letter-spacing: 1px; text-transform: uppercase; }}
td {{ font-size: 14px; font-weight: 400; padding: 10px 14px; border-bottom: 1px solid rgba(128,128,128,0.12); vertical-align: top; color: #ccc; }}
td:first-child {{ color: #fff; font-weight: 600; }}
tr:nth-child(even) td {{ background: #0a0a0a; }}
.footer-line {{ position: absolute; bottom: 56px; left: 80px; right: 80px; height: 1px; background: #B3BCB5; opacity: 0.15; }}
.slide-num {{ position: absolute; bottom: 28px; right: 80px; font-size: 12px; color: #808080; }}
.logo {{ position: absolute; bottom: 48px; left: 80px; }}
.logo img {{ height: 56px; opacity: 0.85; }}
.verdant-bar {{ width: 4px; background: #B3BCB5; border-radius: 2px; flex-shrink: 0; }}
.azure-bar {{ width: 4px; background: #B4BACC; border-radius: 2px; flex-shrink: 0; }}
.grey-bar {{ width: 4px; background: #808080; border-radius: 2px; flex-shrink: 0; }}
.red-bar {{ width: 4px; background: #cc4444; border-radius: 2px; flex-shrink: 0; }}
.band {{ background: #1A1A1A; border-radius: 6px; padding: 30px 40px; display: flex; gap: 60px; }}
.band-active {{ background: #151a16; border-left: 4px solid #B3BCB5; }}
.arch-box {{ background: #1A1A1A; border-radius: 8px; padding: 24px 32px; }}
.input-panel {{ width: 620px; flex-shrink: 0; background: #0C0C0C; border-right: 1px solid rgba(128,128,128,0.1); padding: 80px 60px; display: flex; flex-direction: column; justify-content: center; }}
.input-query {{ border-left: 3px solid #B3BCB5; padding-left: 24px; font-size: 24px; font-weight: 500; line-height: 1.5; color: #fff; }}
.output-panel {{ flex: 1; padding: 60px; overflow: hidden; }}
.pie-chart {{ width: 220px; height: 220px; border-radius: 50%; flex-shrink: 0; }}
.timeline-block {{ flex: 1; padding: 28px; border-radius: 8px; background: #1A1A1A; }}
.timeline-active {{ background: #1a201b; border: 1px solid rgba(179,188,181,0.3); }}
.category-header {{ font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #B3BCB5; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(179,188,181,0.2); }}
.expert-card {{ background: #111; border-radius: 6px; padding: 16px 20px; margin-bottom: 8px; }}
.source-pill {{ display: inline-flex; align-items: center; gap: 8px; background: #111; border: 1px solid rgba(128,128,128,0.2); border-radius: 6px; padding: 8px 16px; font-size: 13px; font-weight: 500; color: #ccc; }}
.connector {{ display: flex; justify-content: center; }}
.connector-line {{ width: 1px; height: 20px; background: #808080; opacity: 0.3; }}
</style>
</head>
<body>

<!-- ============================================================ -->
<!-- SLIDE 1: TITLE                                                -->
<!-- ============================================================ -->
<section class="slide flex center col" style="padding: 80px;">
  <svg style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;">
    <path d="M350,160 Q280,540 350,920" stroke="#808080" fill="none" stroke-width="1.5" opacity="0.1"/>
    <path d="M1570,160 Q1640,540 1570,920" stroke="#808080" fill="none" stroke-width="1.5" opacity="0.1"/>
  </svg>
  <div class="t-hero" style="margin-bottom: 24px;">Jarvis</div>
  <div class="t-sub c-grey">Just a rather very intelligent system</div>
  <div class="logo"><img src="{LOGO_SRC}"></div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 2: THE PROBLEM                                          -->
<!-- ============================================================ -->
<section class="slide flex">
  <div style="width: 50%; padding: 80px; display: flex; flex-direction: column; justify-content: center;">
    <div class="t-headline" style="margin-bottom: 56px; line-height: 1.3;">A VC's most valuable asset<br>is judgment.</div>
    <div style="display: flex; flex-direction: column; gap: 40px;">
      <div>
        <div class="t-body-lg t-bold" style="margin-bottom: 6px;">It lives in the wrong places.</div>
        <div class="t-body c-grey">Scattered across heads, emails, tools and docs that are siloed and fragmented.</div>
      </div>
      <div>
        <div class="t-body-lg t-bold" style="margin-bottom: 6px;">Scale breaks memory.</div>
        <div class="t-body c-grey">30 portfolio companies. 100+ LPs. 1,000s of relationships.</div>
      </div>
      <div>
        <div class="t-body-lg t-bold" style="margin-bottom: 6px;">Context is fragile.</div>
        <div class="t-body c-grey">It is lost when our memory fails. One departure, one missed handover, and years of pattern recognition disappear.</div>
      </div>
      <div>
        <div class="t-body-lg t-bold" style="margin-bottom: 6px;">The cost of forgetting is invisible.</div>
        <div class="t-body c-grey">You never see the connection you never made.</div>
      </div>
    </div>
  </div>
  <div class="bg-grey" style="width: 50%; padding: 80px; display: flex; flex-direction: column; justify-content: center; gap: 48px;">
    <div class="t-large c-white" style="line-height: 1.15;">JARVIS is our<br>second brain.</div>
    <div style="display: flex; flex-direction: column; gap: 28px;">
      <div class="t-body-lg c-white" style="line-height: 1.5; border-left: 3px solid #fff; padding-left: 24px;">Every connection discoverable.<br>Every context searchable.<br>Nothing forgotten.</div>
    </div>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">2 / {TOTAL}</div>
  <div class="logo"><img src="{LOGO_SRC}"></div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 3: WHAT IS JARVIS                                       -->
<!-- ============================================================ -->
<section class="slide pad flex col">
  <div class="t-headline" style="margin-bottom: 48px;">What is JARVIS</div>
  <div style="display: flex; flex-direction: column; gap: 20px; flex: 1;">
    <div class="band band-active" style="flex: 1;">
      <div style="flex: 1;">
        <div class="t-label c-verdant" style="margin-bottom: 20px;">Individual Brain</div>
        <div style="display: flex; gap: 80px;">
          <div><div class="t-tiny c-grey" style="letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">What you just saw</div><div class="t-body">Cornelius - the full demo</div></div>
          <div><div class="t-tiny c-grey" style="letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">What's next</div><div class="t-body">Each team member gets one</div></div>
        </div>
      </div>
    </div>
    <div class="band" style="flex: 1;">
      <div style="flex: 1;">
        <div class="t-label c-grey" style="margin-bottom: 20px;">Org Brain</div>
        <div style="display: flex; gap: 80px;">
          <div><div class="t-tiny c-grey" style="letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">What you just saw</div><div class="t-body">Portfolio synergies, company updates</div></div>
          <div><div class="t-tiny c-grey" style="letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">What's next</div><div class="t-body">Shared knowledge layer across the team</div></div>
        </div>
      </div>
    </div>
    <div class="band" style="flex: 1;">
      <div style="flex: 1;">
        <div class="t-label c-grey" style="margin-bottom: 20px;">Stakeholder Interface</div>
        <div style="display: flex; gap: 80px;">
          <div><div class="t-tiny c-grey" style="letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">What you just saw</div><div class="t-body c-dim">-</div></div>
          <div><div class="t-tiny c-grey" style="letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">What's next</div><div class="t-body">Curated feeds for founders and LPs</div></div>
        </div>
      </div>
    </div>
  </div>
  <div class="t-sub c-verdant t-semi" style="margin-top: 32px;">Private by default, shared by intent.</div>
  <div class="footer-line"></div>
  <div class="slide-num">3 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 4: HOW IT WORKS (with Data Sources layer)               -->
<!-- ============================================================ -->
<section class="slide pad flex col">
  <div class="t-headline" style="margin-bottom: 28px;">How it works</div>
  <div style="display: flex; flex-direction: column; gap: 0; flex: 1; justify-content: center; max-width: 1100px; margin: 0 auto;">
    <!-- Layer 1: Workflows -->
    <div class="arch-box">
      <div class="t-label c-verdant" style="margin-bottom: 12px;">Workflows</div>
      <div class="t-body" style="margin-bottom: 4px;">Natural language commands that trigger complex multi-step operations</div>
      <div class="t-small c-grey" style="font-style: italic;">"What's new with Hanseatic?" &middot; "Show me connections between Fabric and the portfolio"</div>
    </div>
    <div class="connector"><div class="connector-line"></div></div>
    <!-- Layer 2: AI Agents -->
    <div class="arch-box">
      <div class="t-label c-verdant" style="margin-bottom: 12px;">AI Agents</div>
      <div class="t-body">Semantic search &middot; Connection discovery &middot; Insight extraction &middot; Research synthesis</div>
      <div class="t-small c-grey" style="margin-top: 4px;">Claude as the reasoning engine</div>
    </div>
    <div class="connector"><div class="connector-line"></div></div>
    <!-- Layer 3: Knowledge Graph -->
    <div class="arch-box">
      <div class="t-label c-verdant" style="margin-bottom: 12px;">Knowledge Graph</div>
      <div class="t-body">Obsidian &middot; Markdown files &middot; Local-first &middot; No vendor lock-in</div>
      <div class="t-small c-grey" style="margin-top: 4px;">223 notes &middot; 1,300+ connections &middot; You own your data</div>
    </div>
    <div class="connector"><div class="connector-line"></div></div>
    <!-- Layer 4: Data Sources -->
    <div class="arch-box" style="border: 1px solid rgba(128,128,128,0.15);">
      <div class="t-label c-grey" style="margin-bottom: 14px;">Data Sources</div>
      <div class="t-small c-grey" style="margin-bottom: 14px;">Raw data ingested from operational tools via API connectors and structured into the knowledge graph</div>
      <div style="display: flex; flex-wrap: wrap; gap: 10px;">
        <div class="source-pill">
          <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" rx="3" fill="#1a73e8" opacity="0.8"/><text x="8" y="12" font-size="10" fill="white" text-anchor="middle" font-weight="700">G</text></svg>
          Gmail
        </div>
        <div class="source-pill">
          <svg width="16" height="16" viewBox="0 0 16 16"><polygon points="2,2 14,2 14,14 2,14" fill="#0066DA" opacity="0.8" rx="2"/><text x="8" y="12" font-size="8" fill="white" text-anchor="middle" font-weight="700">GD</text></svg>
          Google Drive
        </div>
        <div class="source-pill">
          <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" rx="3" fill="#2ECC71" opacity="0.8"/><text x="8" y="12" font-size="8" fill="white" text-anchor="middle" font-weight="700">Ca</text></svg>
          Carta
        </div>
        <div class="source-pill">
          <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" rx="3" fill="#2CA01C" opacity="0.8"/><text x="8" y="12" font-size="8" fill="white" text-anchor="middle" font-weight="700">QB</text></svg>
          QuickBooks
        </div>
        <div class="source-pill">
          <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" rx="3" fill="#fff" opacity="0.9"/><text x="8" y="12" font-size="9" fill="#000" text-anchor="middle" font-weight="700">N</text></svg>
          Notion
        </div>
        <div class="source-pill">
          <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" rx="3" fill="#5B5FC7" opacity="0.8"/><text x="8" y="12" font-size="8" fill="white" text-anchor="middle" font-weight="700">At</text></svg>
          Attio
        </div>
        <div class="source-pill">
          <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" rx="3" fill="#0A66C2" opacity="0.8"/><text x="8" y="12" font-size="8" fill="white" text-anchor="middle" font-weight="700">Li</text></svg>
          LinkedIn
        </div>
        <div class="source-pill">
          <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" rx="3" fill="#4285F4" opacity="0.8"/><text x="8" y="12" font-size="8" fill="white" text-anchor="middle" font-weight="700">Gc</text></svg>
          Calendar
        </div>
        <div class="source-pill">
          <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" rx="3" fill="#808080" opacity="0.5"/><text x="8" y="12" font-size="9" fill="white" text-anchor="middle" font-weight="700">+</text></svg>
          Web Clipper
        </div>
      </div>
    </div>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">4 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 5: ARCHITECTURE - FIRST PRINCIPLES                      -->
<!-- ============================================================ -->
<section class="slide pad flex col">
  <div class="t-headline" style="margin-bottom: 32px;">Architecture: first principles</div>
  <div style="display: flex; flex-direction: column; align-items: center; gap: 0; flex: 1; justify-content: center;">
    <div class="bg-verdant" style="border-radius: 8px; padding: 24px 48px; text-align: center; width: 780px;">
      <div class="t-label c-black" style="margin-bottom: 10px; letter-spacing: 2px;">Institutional Intelligence</div>
      <div class="t-small c-black">The firm knows everything every team member knows. No knowledge lost. Every connection discoverable.</div>
    </div>
    <div style="width: 1px; height: 24px; background: #808080; opacity: 0.3;"></div>
    <div class="flex" style="width: 780px; background: #1A1A1A; border-radius: 8px; overflow: hidden;">
      <div class="verdant-bar"></div>
      <div style="padding: 24px 36px;">
        <div class="t-label c-verdant" style="margin-bottom: 10px;">Network of Brains</div>
        <div class="t-small" style="line-height: 1.6;">Every team member runs their own AI-augmented knowledge graph.<br>The network connects them. Individual intelligence compounds into institutional intelligence.</div>
      </div>
    </div>
    <div style="width: 1px; height: 24px; background: #808080; opacity: 0.3;"></div>
    <div class="flex" style="width: 780px; background: #1A1A1A; border-radius: 8px; overflow: hidden;">
      <div class="azure-bar"></div>
      <div style="padding: 24px 36px;">
        <div class="t-label c-azure" style="margin-bottom: 10px;">Two Vaults per Person</div>
        <div class="t-small" style="line-height: 1.6;">
          <strong>Personal vault:</strong> private thinking, health, personal notes.<br>
          <strong>Company vault:</strong> research, portfolio, strategy, contacts.<br>
          <span class="c-grey">Hard boundary. Separate directories. Separate indexes.</span>
        </div>
      </div>
    </div>
    <div style="width: 1px; height: 24px; background: #808080; opacity: 0.3;"></div>
    <div class="flex gap-24" style="width: 780px;">
      <div class="flex grow" style="background: #1A1A1A; border-radius: 8px; overflow: hidden;">
        <div class="grey-bar"></div>
        <div style="padding: 24px 28px;">
          <div class="t-label c-grey" style="margin-bottom: 10px;">Sync via Git</div>
          <div class="t-small" style="line-height: 1.6;">Company vault = private GitHub repo.<br>Clone, pull, commit, push.<br><span class="c-grey">Full history. Offline-capable.</span></div>
        </div>
      </div>
      <div class="flex grow" style="background: #1A1A1A; border-radius: 8px; overflow: hidden;">
        <div class="grey-bar"></div>
        <div style="padding: 24px 28px;">
          <div class="t-label c-grey" style="margin-bottom: 10px;">AI Layer is Local</div>
          <div class="t-small" style="line-height: 1.6;">Claude Code on each Mac Mini.<br>FAISS index per vault, per machine.<br><span class="c-grey">No cloud AI sees private data.</span></div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">5 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 6: ARCHITECTURE - PRIVACY MODEL                         -->
<!-- ============================================================ -->
<section class="slide flex">
  <div style="width: 55%; padding: 80px 40px 80px 80px; display: flex; flex-direction: column;">
    <div class="t-headline" style="margin-bottom: 36px;">Architecture: privacy model</div>
    <div style="flex: 1; display: flex; gap: 32px; align-items: flex-start; padding-top: 16px;">
      <div style="flex: 1; background: #1A1A1A; border-radius: 10px; padding: 24px; min-height: 520px;">
        <div class="t-small t-semi t-center" style="margin-bottom: 20px;">Alex's Mac Mini</div>
        <div style="background: #0a0a0a; border-radius: 6px; padding: 16px; margin-bottom: 12px; border-left: 3px solid #cc4444;">
          <div class="t-small t-semi">Personal Vault</div>
          <div class="t-tiny c-grey" style="margin-top: 4px;">local only - never syncs</div>
        </div>
        <div style="text-align: center; margin: 4px 0;">
          <span class="t-tiny" style="color: #cc4444; letter-spacing: 1px; font-weight: 700; font-size: 9px;">PRIVACY BOUNDARY</span>
          <div style="height: 1px; background: #cc4444; opacity: 0.3; margin-top: 4px;"></div>
        </div>
        <div style="background: #0a0a0a; border-radius: 6px; padding: 16px; margin-top: 12px; border-left: 3px solid #B3BCB5;">
          <div class="t-small t-semi">Inflection Vault</div>
          <div class="t-tiny c-verdant" style="margin-top: 4px;">shared via git</div>
        </div>
        <div style="background: #0a0a0a; border-radius: 6px; padding: 16px; margin-top: 12px;">
          <div class="t-small t-semi">Claude Code + FAISS</div>
          <div class="t-tiny c-grey" style="margin-top: 4px;">runs locally</div>
        </div>
      </div>
      <div style="flex: 1; background: #1A1A1A; border-radius: 10px; padding: 24px; min-height: 520px;">
        <div class="t-small t-semi t-center" style="margin-bottom: 20px;">Jonatan's Mac Mini</div>
        <div style="background: #0a0a0a; border-radius: 6px; padding: 16px; margin-bottom: 12px; border-left: 3px solid #cc4444;">
          <div class="t-small t-semi">Personal Vault</div>
          <div class="t-tiny c-grey" style="margin-top: 4px;">local only - never syncs</div>
        </div>
        <div style="text-align: center; margin: 4px 0;">
          <span class="t-tiny" style="color: #cc4444; letter-spacing: 1px; font-weight: 700; font-size: 9px;">PRIVACY BOUNDARY</span>
          <div style="height: 1px; background: #cc4444; opacity: 0.3; margin-top: 4px;"></div>
        </div>
        <div style="background: #0a0a0a; border-radius: 6px; padding: 16px; margin-top: 12px; border-left: 3px solid #B3BCB5;">
          <div class="t-small t-semi">Inflection Vault</div>
          <div class="t-tiny c-verdant" style="margin-top: 4px;">shared via git</div>
        </div>
        <div style="background: #0a0a0a; border-radius: 6px; padding: 16px; margin-top: 12px;">
          <div class="t-small t-semi">Claude Code + FAISS</div>
          <div class="t-tiny c-grey" style="margin-top: 4px;">runs locally</div>
        </div>
      </div>
    </div>
    <div style="display: flex; justify-content: center; margin-top: 20px;">
      <div style="background: #1A1A1A; border-radius: 8px; padding: 16px 48px; text-align: center; border: 1px dashed rgba(179,188,181,0.3);">
        <div class="t-small t-semi">GitHub <span class="c-grey t-tiny">(private org repo)</span></div>
        <div class="t-tiny c-verdant" style="margin-top: 4px;">git push / pull &larr;&rarr; Inflection vaults only</div>
      </div>
    </div>
  </div>
  <div style="width: 45%; padding: 80px 80px 80px 40px; display: flex; flex-direction: column; justify-content: center; gap: 44px;">
    <div><div class="t-body-lg t-semi c-verdant" style="margin-bottom: 12px;">What stays private</div><div class="t-body c-grey" style="line-height: 1.7;">Personal vault never leaves your machine. No symlinks, no shared access, no exceptions.</div></div>
    <div><div class="t-body-lg t-semi c-verdant" style="margin-bottom: 12px;">What syncs</div><div class="t-body c-grey" style="line-height: 1.7;">Company vault syncs via git. You control what enters. One-way valve: personal to company. Never reverse.</div></div>
    <div><div class="t-body-lg t-semi c-verdant" style="margin-bottom: 12px;">How AI stays contained</div><div class="t-body c-grey" style="line-height: 1.7;">Claude Code runs locally on each Mac Mini. Vector indexes are per-vault, per-machine. No cloud inference on private data.</div></div>
    <div><div class="t-body-lg t-semi c-verdant" style="margin-bottom: 12px;">How conflicts resolve</div><div class="t-body c-grey" style="line-height: 1.7;">Git handles merge conflicts on markdown. Last editor owns the merge. Author attribution via frontmatter.</div></div>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">6 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 7: SECTION INTRO                                        -->
<!-- ============================================================ -->
<section class="slide flex center col">
  <div class="t-large t-center" style="margin-bottom: 28px;">One question. Full context.</div>
  <div class="t-sub c-grey t-center">Six queries that take 30 minutes today<br>and 30 seconds with JARVIS.</div>
  <div class="footer-line"></div>
  <div class="slide-num">7 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 8: EXAMPLE 1 - PORTFOLIO INTELLIGENCE                   -->
<!-- ============================================================ -->
<section class="slide flex">
  <div class="input-panel">
    <div class="t-label c-grey" style="margin-bottom: 32px;">Input</div>
    <div class="input-query">I need a quick view of the portfolio. What are our top 5 positions by NAV and trajectory?</div>
  </div>
  <div class="output-panel" style="display: flex; flex-direction: column; gap: 28px; padding-top: 48px;">
    <div class="t-label c-verdant" style="margin-bottom: 0;">Output</div>
    <div style="display: flex; gap: 40px; align-items: center;">
      <div class="pie-chart" style="background: conic-gradient(#B3BCB5 0deg 100.8deg, #B4BACC 100.8deg 169.2deg, #909090 169.2deg 219.6deg, #606060 219.6deg 262.8deg, #404040 262.8deg 295.2deg, #252525 295.2deg 360deg);"></div>
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <div class="t-small"><span style="display:inline-block;width:12px;height:12px;background:#B3BCB5;border-radius:2px;margin-right:8px;vertical-align:middle;"></span><strong>Fabric</strong> &mdash; 28%</div>
        <div class="t-small"><span style="display:inline-block;width:12px;height:12px;background:#B4BACC;border-radius:2px;margin-right:8px;vertical-align:middle;"></span><strong>Ark</strong> &mdash; 19%</div>
        <div class="t-small"><span style="display:inline-block;width:12px;height:12px;background:#909090;border-radius:2px;margin-right:8px;vertical-align:middle;"></span><strong>Ubitium</strong> &mdash; 14%</div>
        <div class="t-small"><span style="display:inline-block;width:12px;height:12px;background:#606060;border-radius:2px;margin-right:8px;vertical-align:middle;"></span><strong>Hedy</strong> &mdash; 12%</div>
        <div class="t-small"><span style="display:inline-block;width:12px;height:12px;background:#404040;border-radius:2px;margin-right:8px;vertical-align:middle;"></span><strong>Tune Insight</strong> &mdash; 9%</div>
        <div class="t-small c-grey"><span style="display:inline-block;width:12px;height:12px;background:#252525;border-radius:2px;margin-right:8px;vertical-align:middle;"></span>Other (9) &mdash; 18%</div>
      </div>
    </div>
    <table>
      <thead><tr><th style="width:14%;">Company</th><th style="width:10%;">NAV</th><th style="width:16%;">Trajectory</th><th style="width:60%;">Signal</th></tr></thead>
      <tbody>
        <tr><td>Fabric</td><td>4.2M</td><td style="color:#B3BCB5;">&#9650;&#9650; Strong up</td><td>Series A termsheet from Lux Capital at 3.2x markup. VPU tape-out on schedule.</td></tr>
        <tr><td>Ark</td><td>2.9M</td><td style="color:#B3BCB5;">&#9650;&#9650; Strong up</td><td>NATO DIANA cohort selected. 2,400 units deployed. Revenue 3x YoY.</td></tr>
        <tr><td>Ubitium</td><td>2.1M</td><td style="color:#B3BCB5;">&#9650; Up</td><td>Elite CTO hired (ex-NVIDIA). First silicon Q3. $1.2M in LOIs.</td></tr>
        <tr><td>Hedy</td><td>1.8M</td><td style="color:#B3BCB5;">&#9650; Up</td><td>Bundeswehr pilot contract signed. Team doubled to 14. Runway 24 months.</td></tr>
        <tr><td>Tune Insight</td><td>1.4M</td><td style="color:#808080;">&#9679; Stable</td><td>Revenue growing 40% QoQ. FHE performance breakthrough - 12x speedup.</td></tr>
      </tbody>
    </table>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">8 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 9: EXAMPLE 2 - LP NETWORK                               -->
<!-- ============================================================ -->
<section class="slide flex">
  <div class="input-panel">
    <div class="t-label c-grey" style="margin-bottom: 32px;">Input</div>
    <div class="input-query">I need a list of the top 10 LPs who can write $500K - $3M checks and who are based in NY or Boston.</div>
  </div>
  <div class="output-panel" style="padding-top: 40px; padding-bottom: 20px;">
    <div class="t-label c-verdant" style="margin-bottom: 16px;">Output</div>
    <table style="font-size: 13px;">
      <thead><tr><th style="width:4%;">#</th><th style="width:22%;">LP / Family Office</th><th style="width:14%;">Location</th><th style="width:13%;">Check Range</th><th style="width:16%;">Partner</th><th style="width:31%;">Status</th></tr></thead>
      <tbody>
        <tr><td>1</td><td>Serafund</td><td>New York</td><td>$1M - $3M</td><td>David Wachtel</td><td>Met at EUVC Summit. Follow-up Feb 18.</td></tr>
        <tr><td>2</td><td>Northstar Ventures FO</td><td>Boston</td><td>$500K - $2M</td><td>Rebecca Haines</td><td>Warm intro via Lakestar. First call done.</td></tr>
        <tr><td>3</td><td>Comerica Wealth</td><td>New York</td><td>$1M - $2.5M</td><td>James Okoro</td><td>LP in Outsized. Asked for intro to us.</td></tr>
        <tr><td>4</td><td>Tiedemann Advisors</td><td>New York</td><td>$500K - $1.5M</td><td>Sarah Lindgren</td><td>Met at Slush NYC. Deep tech allocation expanding.</td></tr>
        <tr><td>5</td><td>Kendall Capital Partners</td><td>Boston</td><td>$1M - $3M</td><td>Michael Cheng</td><td>Ex-a16z scout. Interested in EU defense.</td></tr>
        <tr><td>6</td><td>Beacon Hill FO</td><td>Boston</td><td>$500K - $1M</td><td>Anna Kowalski</td><td>Referred by Earlybird. Prefers co-invest.</td></tr>
        <tr><td>7</td><td>Sievert Family Office</td><td>New York</td><td>$2M - $3M</td><td>Henrik Sievert</td><td>German-American family. Infra background.</td></tr>
        <tr><td>8</td><td>Winthrop Partners</td><td>Boston</td><td>$500K - $2M</td><td>Thomas Walsh</td><td>MIT endowment adjacent. Compute thesis.</td></tr>
        <tr><td>9</td><td>Atlas Merchant Capital</td><td>New York</td><td>$1M - $2M</td><td>Diana Proust</td><td>Allocating to emerging managers. Data room requested.</td></tr>
        <tr><td>10</td><td>Peregrine Ventures FO</td><td>New York</td><td>$500K - $1.5M</td><td>Robert Tanaka</td><td>LP in Blueyard. Complementary EU exposure.</td></tr>
      </tbody>
    </table>
    <div class="t-tiny c-grey" style="margin-top: 16px;">Sources: Mars LP CRM, meeting notes, email threads, event logs. 3 have requested data room. 2 are LPs in co-investor funds.</div>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">9 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 10: EXAMPLE 3 - EXPERT NETWORK                          -->
<!-- ============================================================ -->
<section class="slide flex">
  <div class="input-panel">
    <div class="t-label c-grey" style="margin-bottom: 32px;">Input</div>
    <div class="input-query">I am researching the electrification of the mining industry. Who are the top experts on this in my network?<br><br><span class="c-grey" style="font-size: 18px;">Pick one for each: founder, policy expert, co-investor.</span></div>
  </div>
  <div class="output-panel" style="padding-top: 40px; display: flex; flex-direction: column; gap: 24px;">
    <div class="t-label c-verdant" style="margin-bottom: 0;">Output</div>
    <div><div class="category-header">Founder</div><div class="expert-card"><div style="display:flex;justify-content:space-between;align-items:baseline;"><div class="t-body t-semi">Lars Henriksson</div><div class="t-tiny c-verdant">Strongest match</div></div><div class="t-small c-grey" style="margin-top:4px;">CEO & Founder, Epiroc Electrification (prev. Boliden)</div><div class="t-small c-grey" style="margin-top:8px;line-height:1.5;">Built the first fully electric underground mine in Sweden. 15 years in mining electrification. Met at Nordic Innovation Summit. Connected via Radical deal flow.</div></div></div>
    <div><div class="category-header">Policy Expert</div><div class="expert-card"><div style="display:flex;justify-content:space-between;align-items:baseline;"><div class="t-body t-semi">Dr. Maria Teresa Vasconcelos</div><div class="t-tiny c-verdant">Direct contact</div></div><div class="t-small c-grey" style="margin-top:4px;">European Commission DG GROW - Head of Unit, Raw Materials</div><div class="t-small c-grey" style="margin-top:8px;line-height:1.5;">Led the Critical Raw Materials Act. Keynote at EUVC panel. Exchanged emails on SQM and lithium supply chains.</div></div></div>
    <div><div class="category-header">Co-Investor</div><div class="expert-card"><div style="display:flex;justify-content:space-between;align-items:baseline;"><div class="t-body t-semi">Arnaud Castaignet</div><div class="t-tiny c-verdant">Monthly sync</div></div><div class="t-small c-grey" style="margin-top:4px;">Partner at Lux Capital - Climate & Industrial</div><div class="t-small c-grey" style="margin-top:8px;line-height:1.5;">Led investments in Redwood Materials and Lilac Solutions. Co-invested with us in Fabric. Active in battery/mining convergence thesis.</div></div></div>
    <div><div class="category-header" style="color:#808080;border-color:rgba(128,128,128,0.2);">Also flagged (unsolicited)</div><div style="display:flex;gap:16px;"><div class="expert-card" style="flex:1;"><div class="t-small t-semi">Prof. Kai Vuorilehto</div><div class="t-tiny c-grey">Aalto University, Battery Tech Lab. 3 papers in our library on mining fleet electrification.</div></div><div class="expert-card" style="flex:1;"><div class="t-small t-semi">Jessica Obermayer</div><div class="t-tiny c-grey">McKinsey, Metals & Mining. Co-authored report we clipped. Jonatan met her in Zurich.</div></div></div></div>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">10 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 11: EXAMPLE 4 - COMPETITIVE LANDSCAPE                   -->
<!-- ============================================================ -->
<section class="slide flex">
  <div class="input-panel">
    <div class="t-label c-grey" style="margin-bottom: 32px;">Input</div>
    <div class="input-query">I am evaluating a counter-UAS company. List all companies we've seen in 12 months building competitive or complementary products.</div>
  </div>
  <div class="output-panel" style="padding-top: 36px; display: flex; flex-direction: column; gap: 16px; overflow: hidden;">
    <div class="t-label c-verdant" style="margin-bottom: 0;">Output</div>
    <div><div class="category-header">Competitive - Direct Counter-UAS</div>
    <table style="font-size: 12px;"><thead><tr><th style="width:14%;">Company</th><th style="width:12%;">HQ</th><th style="width:34%;">Product</th><th style="width:40%;">Our Assessment</th></tr></thead><tbody>
      <tr><td>Dedrone</td><td>Virginia, US</td><td>RF-based drone detection + classification platform</td><td>Acq. by Axon. Strong detection, weak kinetic defeat.</td></tr>
      <tr><td>DroneShield</td><td>Sydney, AU</td><td>Multi-sensor detection + electronic countermeasures</td><td>Public (ASX). Hardware-heavy, high unit cost. NATO.</td></tr>
      <tr><td>Sentrycs</td><td>Tel Aviv, IL</td><td>Protocol-based cyber takeover of drones</td><td>Passed. Single-vector, fragile vs autonomous drones.</td></tr>
    </tbody></table></div>
    <div><div class="category-header" style="color:#B4BACC;border-color:rgba(180,186,204,0.2);">Complementary - Adjacent Stack</div>
    <table style="font-size: 12px;"><thead><tr><th style="width:14%;background:#B4BACC;">Company</th><th style="width:22%;background:#B4BACC;">Product</th><th style="width:18%;background:#B4BACC;">Stack Layer</th><th style="width:46%;background:#B4BACC;">Connection</th></tr></thead><tbody>
      <tr><td style="color:#B3BCB5;">Hedy <span class="t-tiny c-grey">(portfolio)</span></td><td>Resilient mesh communications</td><td>Comms infrastructure</td><td>Portfolio company. Direct bridge to any C-UAS investment.</td></tr>
      <tr><td>Echodyne</td><td>Metamaterial scanning radar</td><td>Radar detection</td><td>Reviewed Nov 2025. Too late stage. Potential Hedy partner.</td></tr>
      <tr><td>Bluehalo</td><td>Directed energy (LOCUST laser)</td><td>Kinetic defeat</td><td>In defense research notes. US-focused, no EU presence.</td></tr>
      <tr><td>Quantum Systems</td><td>Fixed-wing VTOL recon drones</td><td>ISR / surveillance</td><td>Met founder at Munich Security. Bundeswehr supplier.</td></tr>
      <tr><td>Phosphorus</td><td>IoT/OT cybersecurity</td><td>Cyber hardening</td><td>Auto-discovered. Tune Insight link via encrypted compute.</td></tr>
    </tbody></table></div>
    <div class="t-tiny c-grey" style="margin-top: 4px;">3 direct competitors. 5 complementary stack components. 1 portfolio company (Hedy) with direct integration potential.</div>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">11 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 12: EXAMPLE 5 - PORTFOLIO FUNDRAISING                   -->
<!-- ============================================================ -->
<section class="slide flex">
  <div class="input-panel">
    <div class="t-label c-grey" style="margin-bottom: 32px;">Input</div>
    <div class="input-query">Which of our portfolio companies are raising funds in the next 3 months and in which order of magnitude?</div>
  </div>
  <div class="output-panel" style="padding-top: 40px; display: flex; flex-direction: column; gap: 20px;">
    <div class="t-label c-verdant" style="margin-bottom: 0;">Output</div>
    <div class="t-small c-grey">5 companies with active or expected fundraises in the next 90 days. Dilution and NAV projections based on latest board materials, comparable rounds, and investor signals in the knowledge base.</div>
    <table>
      <thead><tr>
        <th style="width:13%;">Company</th>
        <th style="width:12%;">Round</th>
        <th style="width:10%;">Timing</th>
        <th style="width:12%;">Target Raise</th>
        <th style="width:14%;">Pre-Money</th>
        <th style="width:10%;">Dilution</th>
        <th style="width:14%;">Our NAV Post</th>
        <th style="width:15%;">Markup</th>
      </tr></thead>
      <tbody>
        <tr>
          <td>Fabric</td><td>Series A</td><td>Q2 2026</td><td>$12M</td><td>$35M</td>
          <td>25%</td><td style="color:#B3BCB5;">$6.3M</td><td style="color:#B3BCB5;">3.2x</td>
        </tr>
        <tr>
          <td>Deep Earth</td><td>Series A</td><td>Q2 2026</td><td>$8M</td><td>$25M</td>
          <td>24%</td><td style="color:#B3BCB5;">$3.8M</td><td style="color:#B3BCB5;">2.5x</td>
        </tr>
        <tr>
          <td>Hedy</td><td>Seed Ext.</td><td>Q1 2026</td><td>$4M</td><td>$18M</td>
          <td>18%</td><td style="color:#B3BCB5;">$2.1M</td><td style="color:#B3BCB5;">1.8x</td>
        </tr>
        <tr>
          <td>Radical</td><td>Seed Ext.</td><td>Q2 2026</td><td>$3M</td><td>$16M</td>
          <td>16%</td><td>$1.9M</td><td>1.5x</td>
        </tr>
        <tr>
          <td>Tune Insight</td><td>Bridge</td><td>Q1 2026</td><td>$2M</td><td>$15M (flat)</td>
          <td>12%</td><td style="color:#808080;">$1.4M</td><td style="color:#808080;">1.0x</td>
        </tr>
      </tbody>
    </table>
    <!-- Summary bar -->
    <div style="display: flex; gap: 32px; padding: 20px 24px; background: #111; border-radius: 8px; border-left: 3px solid #B3BCB5;">
      <div>
        <div class="t-tiny c-grey" style="text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Total Raises</div>
        <div class="t-body-lg t-semi">$29M</div>
      </div>
      <div>
        <div class="t-tiny c-grey" style="text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Avg Dilution</div>
        <div class="t-body-lg t-semi">19%</div>
      </div>
      <div>
        <div class="t-tiny c-grey" style="text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Portfolio NAV Impact</div>
        <div class="t-body-lg t-semi c-verdant">+$3.2M</div>
      </div>
      <div>
        <div class="t-tiny c-grey" style="text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Pro-Rata Required</div>
        <div class="t-body-lg t-semi">$1.1M</div>
      </div>
    </div>
    <div class="t-tiny c-grey">Sources: Board decks, investor update letters, Carta cap tables, partner call notes. Fabric and Deep Earth termsheets are live. Hedy and Tune Insight timelines from founder conversations.</div>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">12 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 13: EXAMPLE 6 - FUND PERFORMANCE                        -->
<!-- ============================================================ -->
<section class="slide flex">
  <div class="input-panel">
    <div class="t-label c-grey" style="margin-bottom: 32px;">Input</div>
    <div class="input-query">Display our fund performance over the last 8 quarters by showing TVPI, MOIC and DPI over time.</div>
  </div>
  <div class="output-panel" style="padding-top: 40px; display: flex; flex-direction: column; gap: 20px;">
    <div class="t-label c-verdant" style="margin-bottom: 0;">Output</div>
    <div class="t-small c-grey">Mercury Fund (Fund II) - performance metrics Q2 2024 through Q1 2026. Gross MOIC based on portfolio markings. Net TVPI after fees and carry. DPI reflects realized distributions.</div>

    <!-- SVG Chart -->
    <div style="position: relative;">
      <svg viewBox="0 0 920 420" width="920" height="420" style="overflow: visible;">
        <!-- Grid -->
        <line x1="60" y1="20" x2="60" y2="360" stroke="#333" stroke-width="1"/>
        <line x1="60" y1="360" x2="880" y2="360" stroke="#333" stroke-width="1"/>
        <!-- Y grid lines -->
        <line x1="60" y1="20" x2="880" y2="20" stroke="#1a1a1a" stroke-width="1"/>
        <line x1="60" y1="105" x2="880" y2="105" stroke="#1a1a1a" stroke-width="1"/>
        <line x1="60" y1="190" x2="880" y2="190" stroke="#1a1a1a" stroke-width="1"/>
        <line x1="60" y1="275" x2="880" y2="275" stroke="#1a1a1a" stroke-width="1"/>
        <!-- Y labels -->
        <text x="50" y="25" fill="#808080" font-size="11" text-anchor="end" font-family="Inter, sans-serif">1.6x</text>
        <text x="50" y="110" fill="#808080" font-size="11" text-anchor="end" font-family="Inter, sans-serif">1.2x</text>
        <text x="50" y="195" fill="#808080" font-size="11" text-anchor="end" font-family="Inter, sans-serif">0.8x</text>
        <text x="50" y="280" fill="#808080" font-size="11" text-anchor="end" font-family="Inter, sans-serif">0.4x</text>
        <text x="50" y="365" fill="#808080" font-size="11" text-anchor="end" font-family="Inter, sans-serif">0.0x</text>
        <!-- X labels -->
        <text x="60" y="390" fill="#808080" font-size="11" text-anchor="middle" font-family="Inter, sans-serif">Q2'24</text>
        <text x="177" y="390" fill="#808080" font-size="11" text-anchor="middle" font-family="Inter, sans-serif">Q3'24</text>
        <text x="294" y="390" fill="#808080" font-size="11" text-anchor="middle" font-family="Inter, sans-serif">Q4'24</text>
        <text x="411" y="390" fill="#808080" font-size="11" text-anchor="middle" font-family="Inter, sans-serif">Q1'25</text>
        <text x="528" y="390" fill="#808080" font-size="11" text-anchor="middle" font-family="Inter, sans-serif">Q2'25</text>
        <text x="645" y="390" fill="#808080" font-size="11" text-anchor="middle" font-family="Inter, sans-serif">Q3'25</text>
        <text x="762" y="390" fill="#808080" font-size="11" text-anchor="middle" font-family="Inter, sans-serif">Q4'25</text>
        <text x="880" y="390" fill="#B3BCB5" font-size="11" text-anchor="middle" font-weight="600" font-family="Inter, sans-serif">Q1'26</text>

        <!-- MOIC line (gross) - top line -->
        <polyline points="60,138 177,128 294,118 411,100 528,82 645,65 762,46 880,30"
          fill="none" stroke="#808080" stroke-width="2" stroke-dasharray="6,4"/>
        <!-- MOIC dots -->
        <circle cx="880" cy="30" r="4" fill="#808080"/>

        <!-- TVPI line (net) - middle line -->
        <polyline points="60,143 177,137 294,131 411,118 528,103 645,88 762,73 880,58"
          fill="none" stroke="#B3BCB5" stroke-width="2.5"/>
        <!-- TVPI dots -->
        <circle cx="880" cy="58" r="4" fill="#B3BCB5"/>

        <!-- DPI line - bottom -->
        <polyline points="60,360 177,360 294,360 411,360 528,356 645,356 762,349 880,343"
          fill="none" stroke="#B4BACC" stroke-width="2"/>
        <!-- DPI dots -->
        <circle cx="880" cy="343" r="4" fill="#B4BACC"/>

        <!-- End labels -->
        <text x="895" y="34" fill="#808080" font-size="12" font-weight="600" font-family="Inter, sans-serif">1.55x</text>
        <text x="895" y="62" fill="#B3BCB5" font-size="12" font-weight="600" font-family="Inter, sans-serif">1.42x</text>
        <text x="895" y="347" fill="#B4BACC" font-size="12" font-weight="600" font-family="Inter, sans-serif">0.08x</text>
      </svg>
    </div>

    <!-- Legend -->
    <div style="display: flex; gap: 32px; align-items: center;">
      <div class="t-small" style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 24px; height: 2.5px; background: #B3BCB5;"></div> <strong>Net TVPI</strong> <span class="c-grey">1.42x</span>
      </div>
      <div class="t-small" style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 24px; height: 2px; background: #808080; border-top: 2px dashed #808080;"></div> <strong>Gross MOIC</strong> <span class="c-grey">1.55x</span>
      </div>
      <div class="t-small" style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 24px; height: 2px; background: #B4BACC;"></div> <strong>DPI</strong> <span class="c-grey">0.08x</span>
      </div>
    </div>

    <!-- Summary metrics -->
    <div style="display: flex; gap: 32px; padding: 16px 24px; background: #111; border-radius: 8px; border-left: 3px solid #B3BCB5;">
      <div><div class="t-tiny c-grey" style="text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Net IRR</div><div class="t-body t-semi c-verdant">18.4%</div></div>
      <div><div class="t-tiny c-grey" style="text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Called Capital</div><div class="t-body t-semi">72%</div></div>
      <div><div class="t-tiny c-grey" style="text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Reserves</div><div class="t-body t-semi">$2.8M</div></div>
      <div><div class="t-tiny c-grey" style="text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Vintage</div><div class="t-body t-semi">2022</div></div>
    </div>

    <div class="t-tiny c-grey">Sources: QuickBooks (cash flows), Carta (cap tables and markings), quarterly LP reports. Markings follow IPEV guidelines. Next LP report due March 31.</div>
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">13 / {TOTAL}</div>
</section>

<!-- ============================================================ -->
<!-- SLIDE 14: ROADMAP + CLOSE                                     -->
<!-- ============================================================ -->
<section class="slide pad flex col">
  <div class="t-headline" style="margin-bottom: 48px;">Roadmap</div>
  <div style="display: flex; gap: 20px; margin-bottom: auto;">
    <div class="timeline-block timeline-active">
      <div class="t-label c-verdant" style="margin-bottom: 16px;">Q1 2026</div>
      <div class="t-body t-semi" style="margin-bottom: 12px;">Individual brains</div>
      <div class="t-small c-grey" style="line-height: 1.6;">Mac Mini per person<br>Two vaults each<br>Full Cornelius stack<br>Team onboarding</div>
    </div>
    <div class="timeline-block">
      <div class="t-label c-grey" style="margin-bottom: 16px;">Q2 2026</div>
      <div class="t-body t-semi" style="margin-bottom: 12px;">Shared org layer</div>
      <div class="t-small c-grey" style="line-height: 1.6;">Git-synced company vault<br>Cross-brain search<br>Author attribution<br>Merge conventions</div>
    </div>
    <div class="timeline-block">
      <div class="t-label c-grey" style="margin-bottom: 16px;">Q3 2026</div>
      <div class="t-body t-semi" style="margin-bottom: 12px;">Stakeholder interface</div>
      <div class="t-small c-grey" style="line-height: 1.6;">Founder briefs<br>LP portfolio updates<br>Curated knowledge feeds<br>Automated reporting</div>
    </div>
    <div class="timeline-block">
      <div class="t-label c-grey" style="margin-bottom: 16px;">Long Term</div>
      <div class="t-body t-semi" style="margin-bottom: 12px;">External rollout</div>
      <div class="t-small c-grey" style="line-height: 1.6;">Offer to portfolio companies<br>Productize for other funds<br>Open-source components<br>Community development</div>
    </div>
  </div>
  <div style="display: flex; align-items: center; justify-content: center; padding-top: 48px;">
    <img src="{SYMBOL_SRC}" style="height: 64px; opacity: 0.9;">
  </div>
  <div class="footer-line"></div>
  <div class="slide-num">{TOTAL} / {TOTAL}</div>
</section>

</body>
</html>'''

# Write HTML
html_path = os.path.join(DIR, "jarvis-deck-v2.html")
with open(html_path, "w") as f:
    f.write(HTML)
print(f"HTML written to {html_path}")

# Convert to PDF via Chrome headless
pdf_path = os.path.join(DIR, "JARVIS-Deck-v2.pdf")
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome, "--headless", "--disable-gpu", "--no-sandbox",
    f"--print-to-pdf={pdf_path}",
    "--no-margins", "--paper-width=20", "--paper-height=11.25",
    "--no-pdf-header-footer",
    f"file://{html_path}"
]
result = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_path):
    size = os.path.getsize(pdf_path)
    print(f"PDF written to {pdf_path} ({size:,} bytes, {TOTAL} slides)")
else:
    print(f"PDF conversion failed: {result.stderr}")
