#!/usr/bin/env python3
"""
Update investment memo frontmatter with structured trigger fields.
Phase 1 of the Alert System: Standardize trigger data across all memos.
"""

import os
import re
import yaml

MEMO_DIR = "/Users/alexanderruppert/Desktop/Claude/OBSIDIAN VAULT/02-Thinking/Investment Memos"

# Consolidated trigger data from all memos
TRIGGERS = {
    "ASML Memo.md": {
        "buy_below": [1100, 1200],
        "buy_aggressive": 1000,
        "sell_above": None,
        "sell_triggers": [
            "Major expansion of export restrictions (all DUV to China banned)",
            "Evidence of competitive threat from Canon or Chinese EUV",
            "Margin deterioration below 48% gross margin",
            "Management signaling multi-year cycle downturn"
        ],
        "upgrade_catalysts": [
            "Price below $1,000",
            "Upward revision to 2030 targets",
            "High-NA EUV orders accelerating beyond expectations",
            "Insider buying by CEO or CFO"
        ],
        "downgrade_triggers": None,
        "next_catalyst": "2026 guidance execution - revenue EUR 34-39B, China revenue normalizing to ~20%"
    },
    "Adobe (ADBE) Memo.md": {
        "buy_below": [259],
        "buy_aggressive": 220,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": None,
        "downgrade_triggers": [
            "AI tools genuinely displace Creative Cloud for mainstream users",
            "Enterprise segment stagnates"
        ],
        "next_catalyst": None
    },
    "Alibaba (BABA) Memo.md": {
        "buy_below": [157],
        "buy_aggressive": 120,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": None,
        "downgrade_triggers": [
            "Regulatory crackdown resumes",
            "US delisting forced",
            "China macro deterioration accelerates"
        ],
        "next_catalyst": None
    },
    "Allianz Memo.md": {
        "buy_below": [373],
        "buy_aggressive": 330,
        "sell_above": None,
        "sell_triggers": [
            "Major catastrophe causing >EUR 3B in single-event losses",
            "PIMCO suffers quarterly outflows exceeding EUR 30B",
            "Solvency II drops below 180%",
            "New regulatory or litigation risk of Structured Alpha magnitude"
        ],
        "upgrade_catalysts": [
            "Price drops below EUR 330 (P/E < 12x)",
            "FY2025 results exceed EUR 17.5B upper guidance",
            "European equity re-rating accelerates"
        ],
        "downgrade_triggers": None,
        "next_catalyst": "FY2025 preliminary results - February 26, 2026"
    },
    "Alphabet (GOOGL) Memo.md": {
        "buy_below": [240, 260],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": None,
        "downgrade_triggers": [
            "AI disrupts Search monetization materially",
            "Regulatory forced changes to defaults",
            "Cloud growth decelerates below 20%"
        ],
        "next_catalyst": None
    },
    "Amazon (AMZN) Memo.md": {
        "buy_below": [175, 180],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Capex guidance for FY2027 signals normalization to $120-140B range"
        ],
        "downgrade_triggers": [
            "$200B+ capex continues into 2027-2028 without proportional revenue",
            "AWS growth decelerates to 15%",
            "Advertising growth slows to 10-15%"
        ],
        "next_catalyst": "FY2027 capex guidance - key trigger for position sizing"
    },
    "Ambev (ABEV).md": {
        "buy_below": [2.20, 2.40],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "BRL strengthening below 5.5/USD",
            "Price pullback to $2.20-2.40 (8-9% yield)",
            "Special dividend or buyback deploying BRL 25B cash hoard",
            "Heineken share gains plateauing"
        ],
        "downgrade_triggers": [
            "BRL depreciates to 6.5+/USD",
            "Heineken continues gaining share, gross margins drop to 48%"
        ],
        "next_catalyst": None
    },
    "Apple Memo.md": {
        "buy_below": [200, 220],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "AI monetization accelerating Services revenue growth to 20%+",
            "Successful expansion into health or financial services"
        ],
        "downgrade_triggers": None,
        "next_catalyst": None
    },
    "BYD Memo.md": {
        "buy_below": [12.06],
        "buy_aggressive": 8,
        "sell_above": None,
        "sell_triggers": [
            "Significant tariff escalations or sanctions",
            "Margin collapse below 3%",
            "Competitive erosion in China",
            "Severe macro downturn impacting auto demand"
        ],
        "upgrade_catalysts": [
            "Successful European production ramp (Hungary/Turkey)",
            "US-China trade stabilization",
            "Margin expansion above 6%"
        ],
        "downgrade_triggers": None,
        "next_catalyst": "FY2025 results - March 26, 2026"
    },
    "Berkshire Hathaway (BRK-B) Memo.md": {
        "buy_below": [380, 400],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Elephant-sized acquisition deploys $100B+ of cash productively"
        ],
        "downgrade_triggers": [
            "Post-Buffett succession uncertainty",
            "Cash drag from rate cuts",
            "Insurance cycle turns"
        ],
        "next_catalyst": None
    },
    "CNI Memo.md": {
        "buy_below": [88, 101],
        "buy_aggressive": 88,
        "sell_above": 115,
        "sell_triggers": [
            "Net Debt/EBITDA exceeds 3x",
            "Tariff damage proves structural - persistent cross-border volume declines 4+ quarters",
            "Stock reaches $115+ without earnings improvement"
        ],
        "upgrade_catalysts": [
            "Tariff resolution confirmation",
            "Pullback below $88 (converges with IV)",
            "2026 capex step-down boosting FCF toward C$4.0B"
        ],
        "downgrade_triggers": [
            "Net Debt/EBITDA exceeds 3x",
            "Quarterly operating ratio above 63%"
        ],
        "next_catalyst": "Tariff resolution timeline - 2026"
    },
    "Cameco (CCJ) Memo.md": {
        "buy_below": [60, 75],
        "buy_aggressive": 55,
        "sell_above": None,
        "sell_triggers": [
            "Uranium spot falls below $70/lb sustained",
            "Debt/Equity exceeds 0.40",
            "ROE fails to expand above 12% over next 2-3 years"
        ],
        "upgrade_catalysts": [
            "Price pullback to $55-75",
            "Uranium spot price above $120/lb",
            "Westinghouse cash distributions scale to $200M+/year",
            "Long-term contract price above $100/lb"
        ],
        "downgrade_triggers": [
            "Uranium falls below $70/lb sustained",
            "Kazatomprom ramps production aggressively",
            "Nuclear accident event"
        ],
        "next_catalyst": "McArthur River ramp to 25M lbs/year - 2026-2027"
    },
    "Chapters Group (CHAPTERS) Memo.md": {
        "buy_below": None,
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Key person departure from management",
            "Evidence of undisciplined acquisition pricing"
        ],
        "upgrade_catalysts": [
            "Improved financial disclosure",
            "Demonstrated acquisition track record over multiple years"
        ],
        "downgrade_triggers": [
            "Continued opacity with no improvement in reporting"
        ],
        "next_catalyst": None
    },
    "Chevron (CVX) Memo.md": {
        "buy_below": [130, 140],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Hess acquisition deal fails completely",
            "Sustained oil prices below $70/bbl",
            "Operating margins compress below 5% for multiple quarters"
        ],
        "upgrade_catalysts": [
            "Price pullback to $130-140",
            "Oil price spikes on geopolitical events",
            "Hess deal closes successfully",
            "Oil stabilizes above $85/bbl"
        ],
        "downgrade_triggers": [
            "Oil stays below $70/bbl sustained",
            "FCF insufficient to cover buybacks + dividends"
        ],
        "next_catalyst": "Hess acquisition arbitration resolution - 2026"
    },
    "Cloudflare Memo.md": {
        "buy_below": [120, 135],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Revenue growth decelerates below 15% for multiple quarters",
            "SBC exceeds 25% of revenue",
            "Hyperscaler competition erodes market share",
            "GAAP losses widen instead of narrowing"
        ],
        "upgrade_catalysts": [
            "Price drops below $130",
            "GAAP profitability achieved",
            "Multiple consecutive quarters of 30%+ revenue growth",
            "Insider buying by CEO or CFO"
        ],
        "downgrade_triggers": [
            "Revenue growth below 15-20%",
            "AI initiatives fail vs hyperscalers"
        ],
        "next_catalyst": "Q4 2025 earnings - revenue growth re-acceleration and margin progression"
    },
    "Coca-Cola (KO) Memo.md": {
        "buy_below": [55, 60],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "GLP-1 drugs materially reduce sugar beverage consumption",
            "Dividend growth streak broken",
            "FCF deterioration below dividend coverage for extended period"
        ],
        "upgrade_catalysts": [
            "Price pullback to $55-60 (18-20x earnings)",
            "Emerging market volume growth acceleration",
            "Successful zero-sugar/category expansion"
        ],
        "downgrade_triggers": [
            "GLP-1 drugs cause measurable consumption decline",
            "Dividend coverage ratio worsens sustainably"
        ],
        "next_catalyst": "GLP-1 drug adoption data and impact on beverage consumption - ongoing 2026"
    },
    "Coinbase Memo.md": {
        "buy_below": [120, 140],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Crypto winter with revenue below $3B",
            "SBC exceeding 20% of revenue",
            "Regulatory crackdown under future administration",
            "Net cash turning to net debt"
        ],
        "upgrade_catalysts": [
            "Stock drops to $120-140",
            "Subscription/services revenue exceeds 50% of total for two consecutive quarters",
            "Mid-cycle ROIC exceeds 12%"
        ],
        "downgrade_triggers": [
            "Revenue below $3B",
            "Post-2028 regulatory reversal"
        ],
        "next_catalyst": "Deribit acquisition integration and derivatives revenue - 2026"
    },
    "Deutsche Telekom (DTEGY) Memo.md": {
        "buy_below": [30, 33],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "TMUS postpaid churn exceeds 1.2%",
            "TMUS subscriber growth halves from current levels",
            "Net Debt/EBITDA exceeds 3.0x"
        ],
        "upgrade_catalysts": [
            "Stock pulls back to $30-33",
            "TMUS guides to accelerating growth in 2027+",
            "German fiber take-up rate surprise (>20% ahead of schedule)"
        ],
        "downgrade_triggers": [
            "TMUS growth premium lost",
            "German fiber take-up below 15%",
            "Net Debt/EBITDA exceeds 2.75x"
        ],
        "next_catalyst": "Q4 2025 / FY2025 results - February 26, 2026"
    },
    "Exor (EXOR) Memo.md": {
        "buy_below": [55, 60],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Stellantis deterioration accelerates structurally",
            "NAV discount narrows above 25% (overvalued on NAV basis)",
            "Ferrari brand dilution or operational deterioration"
        ],
        "upgrade_catalysts": [
            "Price pullback to $55-60 (NAV discount exceeds 50%)",
            "Stellantis recovery under new leadership",
            "PartnerRe IPO crystallizes value"
        ],
        "downgrade_triggers": [
            "Stellantis further deterioration",
            "Ferrari slowdown"
        ],
        "next_catalyst": "Stellantis new CEO strategy and recovery plan - 2026"
    },
    "Ferrari Memo.md": {
        "buy_below": [280, 300],
        "buy_aggressive": 260,
        "sell_above": None,
        "sell_triggers": [
            "Elettrica EV commercial failure or brand rejection",
            "China weakness spreading to Middle East or US markets",
            "Operating margins below 25% for two or more quarters",
            "Institutional distribution reversing accumulation pattern"
        ],
        "upgrade_catalysts": [
            "Deeper pullback to $260-290",
            "Elettrica launch success in Q2 2026",
            "Sustained revenue re-acceleration above 10% YoY"
        ],
        "downgrade_triggers": [
            "Revenue growth stalls to sub-5%",
            "Elettrica disappoints commercially",
            "EBIT margin compresses below 25%"
        ],
        "next_catalyst": "Elettrica (first full EV) launch - Q2 2026"
    },
    "First Solar (FSLR) Memo.md": {
        "buy_below": [200],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Book-to-bill remaining below 1.0 through H1 2026 even after AD/CVD tariffs",
            "Persistent margin compression below 20% for two consecutive quarters",
            "Chinese manufacturers circumvent FEOC restrictions or AD/CVD tariff walls",
            "Further large customer defaults (>5 GW cumulative beyond BP)"
        ],
        "upgrade_catalysts": [
            "2026 bookings recover toward book-to-bill 1.0+ (upgrade position to 3-4%)",
            "Management guides to gross margins above 35% (upgrade to 3-4%)",
            "Pullback below $200 with improving backlog trajectory (upgrade to 5%)"
        ],
        "downgrade_triggers": [
            "Book-to-bill below 1.0 through H1 2026",
            "2026 midterms producing Republican supermajority attempting 45X repeal"
        ],
        "next_catalyst": "Q4 2025 earnings + 2026 guidance - February 24, 2026"
    },
    "HDFC Bank Memo.md": {
        "buy_below": None,
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "GNPA ratio rises above 2%",
            "RBI imposes material operational restrictions"
        ],
        "upgrade_catalysts": [
            "NIM recovers above 3.5% in next 2-3 quarters (upgrade from 3% to 5%)"
        ],
        "downgrade_triggers": [
            "GNPA above 2% or RBI restrictions (downgrade to HOLD)",
            "ROE fails to recover toward 15%+ by FY2028 (downgrade to PASS)"
        ],
        "next_catalyst": None
    },
    "Incyte (INCY) Memo.md": {
        "buy_below": [70, 75],
        "buy_aggressive": 70,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Jakafi XR FDA approval (would push stock to $120-130)",
            "Povorcitinib Phase 3 wins in vitiligo + prurigo nodularis",
            "Price drops to $70-75"
        ],
        "downgrade_triggers": None,
        "next_catalyst": "Povorcitinib Phase 3 data in vitiligo and prurigo nodularis - 2026"
    },
    "LPTH-LightPath-Technologies-2025-02.md": {
        "buy_below": [5],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Price below $5",
            "Two consecutive quarters of positive operating cash flow",
            "Major multi-year framework agreement with Tier 1 defense prime",
            "Insider buying (executives, not just grants)"
        ],
        "downgrade_triggers": None,
        "next_catalyst": None
    },
    "Lululemon (LULU) Memo.md": {
        "buy_below": [130, 140],
        "buy_aggressive": 130,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "20% pullback to $130-140 range",
            "China accelerates, men's category breaks out, footwear gains traction"
        ],
        "downgrade_triggers": [
            "North America flat, China disappoints, margin compression"
        ],
        "next_catalyst": None
    },
    "Mercado Libre Memo.md": {
        "buy_below": [1500, 1600],
        "buy_aggressive": 1500,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Price declines to $1,500-1,600",
            "Operating margin recovery above 12%",
            "Credit portfolio NPL trends improving"
        ],
        "downgrade_triggers": [
            "Operating margin stays below 10%",
            "Credit portfolio NPL deterioration",
            "Competitive dynamics worsen in Brazil"
        ],
        "next_catalyst": "Q4 2025 earnings - margin recovery signal - February 24, 2026"
    },
    "Mercedes-Benz Group - MBG.DE.md": {
        "buy_below": [45],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Price below EUR 45",
            "Two consecutive quarters of margin improvement in Cars",
            "China quarterly revenue stabilization",
            "Successful CLA launch proving MB.EA competitiveness"
        ],
        "downgrade_triggers": None,
        "next_catalyst": None
    },
    "Microsoft (MSFT) Memo.md": {
        "buy_below": [350],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Price below $350",
            "Capex-to-revenue ratio stabilizing at 25% while revenue grows 15%",
            "Copilot penetration hitting 10%+ of M365 seats"
        ],
        "downgrade_triggers": [
            "AI capex ROI disappoints - Copilot plateaus below 10% penetration",
            "Azure margins compress structurally"
        ],
        "next_catalyst": "Quarterly capex/revenue trajectory and Copilot seat count updates"
    },
    "Molina Healthcare MOH Value Investing Memo.md": {
        "buy_below": [90],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Price below $90",
            "Two consecutive quarters of positive operating cash flow",
            "Insider buying ($1M+ open-market by CEO or CFO)",
            "Medicaid policy clarity - work requirements softened or delayed"
        ],
        "downgrade_triggers": None,
        "next_catalyst": "Q1/Q2 2026 MCR trends and OCF recovery"
    },
    "Moody's Memo.md": {
        "buy_below": [370, 390],
        "buy_aggressive": 370,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Price declines to $370-390",
            "Issuance slowdown in H1 2026 creating entry",
            "Q4 2025 earnings miss on February 18",
            "Broader market correction compressing quality premiums"
        ],
        "downgrade_triggers": [
            "Issuance recession similar to 2022 - MIS revenue drops 10-15%",
            "Regulatory headwinds from US sovereign downgrade"
        ],
        "next_catalyst": "Q4 2025 earnings - February 18, 2026"
    },
    "Netflix (NFLX) Memo.md": {
        "buy_below": [65, 70],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "DOJ blocks WBD deal or forces major IP divestitures + management distraction",
            "Bidding war with Paramount pushes acquisition price materially higher"
        ],
        "upgrade_catalysts": [
            "DOJ clears WBD deal with minimal divestitures + financing at reasonable rates",
            "Deal falls through and Netflix refocuses on tech-native content strategy"
        ],
        "downgrade_triggers": [
            "DOJ blocks deal or forces major divestitures",
            "Bidding war pushes acquisition price higher"
        ],
        "next_catalyst": "WBD shareholder vote - expected April 2026"
    },
    "New Oriental Education Memo.md": {
        "buy_below": [62.72],
        "buy_aggressive": 50,
        "sell_above": 90,
        "sell_triggers": [
            "New regulatory restrictions on non-academic tutoring or test prep",
            "VIE structure challenge by Chinese or US regulators",
            "Revenue growth turns negative for two consecutive quarters",
            "Price above $90 without fundamental improvement"
        ],
        "upgrade_catalysts": None,
        "downgrade_triggers": [
            "New regulatory restrictions on non-academic tutoring",
            "VIE structure challenge",
            "Revenue growth negative two consecutive quarters"
        ],
        "next_catalyst": None
    },
    "Nu Holdings (NU) Memo.md": {
        "buy_below": None,
        "buy_aggressive": [12, 14],
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": None,
        "downgrade_triggers": None,
        "next_catalyst": None
    },
    "PayPal Memo.md": {
        "buy_below": None,
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Branded checkout accelerates decline (goes negative)",
            "Venmo growth stalls below 10%",
            "Free cash flow deteriorates significantly",
            "New CEO articulates no clear strategy"
        ],
        "upgrade_catalysts": [
            "Evidence of branded checkout stabilization (Q2-Q3 2026)",
            "New CEO articulates credible turnaround strategy",
            "Venmo continues 20%+ revenue growth",
            "Insider buying by new management"
        ],
        "downgrade_triggers": [
            "Branded checkout goes negative",
            "Venmo growth stalls below 10%",
            "FCF deteriorates significantly"
        ],
        "next_catalyst": "New CEO Enrique Lores takes over - March 1, 2026"
    },
    "Pfizer Memo.md": {
        "buy_below": None,
        "buy_aggressive": 24,
        "sell_above": None,
        "sell_triggers": [
            "Earnings guidance cuts threatening dividend coverage",
            "Major pipeline failures in late-stage oncology",
            "Debt covenant concerns or credit downgrades",
            "Dividend cut announcement"
        ],
        "upgrade_catalysts": [
            "Positive Phase 3 data on vepdegestrant, atirmociclib",
            "Debt reduction below $60B",
            "2027 EPS estimates stabilizing or increasing",
            "Obesity program showing competitive efficacy (>15% weight loss)"
        ],
        "downgrade_triggers": [
            "Earnings guidance cuts threatening dividend coverage",
            "Major pipeline failures in late-stage oncology",
            "Dividend cut announcement"
        ],
        "next_catalyst": "2026 quarterly earnings trajectory vs $2.80-$3.00 guidance"
    },
    "Procter & Gamble Memo.md": {
        "buy_below": [135, 140],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Price decline to $135-140",
            "Sustained organic volume growth above 3% (not just pricing)",
            "Margin expansion from AI-driven supply chain efficiencies",
            "Tariff resolution removing margin headwind"
        ],
        "downgrade_triggers": None,
        "next_catalyst": None
    },
    "Robinhood (HOOD) Memo.md": {
        "buy_below": [45, 55],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Price below $50",
            "Sustained $1.2B+ quarterly revenue for 4+ quarters proving non-cyclical",
            "PFOF regulatory clarity (removal of ban risk)",
            "Demonstrated positive FCF generation"
        ],
        "downgrade_triggers": None,
        "next_catalyst": None
    },
    "SLB (SLB) Memo.md": {
        "buy_below": [35, 38],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": None,
        "downgrade_triggers": None,
        "next_catalyst": None
    },
    "SQM Memo.md": {
        "buy_below": [60],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Lithium prices sustain above $25,000/ton (take profits at cycle peak)",
            "Codelco deal materially worsens post-2031 economics",
            "FCPA investigation results in material penalty",
            "China lithium demand structurally disappoints"
        ],
        "upgrade_catalysts": None,
        "downgrade_triggers": [
            "Codelco deal materially worsens",
            "FCPA investigation results in material penalty",
            "China lithium demand structurally disappoints"
        ],
        "next_catalyst": "Q4 2025 earnings - expected March 2026"
    },
    "SSR Mining (SSRM) Memo.md": {
        "buy_below": None,
        "buy_aggressive": None,
        "sell_above": 40,
        "sell_triggers": [
            "Gold drops below $2,000/oz sustainably",
            "Copler remediation costs exceed $300M",
            "Reserve replacement fails at Marigold or CC&V"
        ],
        "upgrade_catalysts": None,
        "downgrade_triggers": [
            "Gold drops below $2,000/oz sustainably",
            "Copler remediation costs exceed $300M",
            "Reserve replacement fails at Marigold or CC&V"
        ],
        "next_catalyst": "Copler restart decision - Turkish regulatory approval required"
    },
    "Salesforce (CRM) Memo.md": {
        "buy_below": None,
        "buy_aggressive": 160,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Agentforce becomes the enterprise AI platform",
            "Margins reach 25%+",
            "Revenue reaccelerates"
        ],
        "downgrade_triggers": [
            "Margin expansion stalls",
            "AI competition intensifies",
            "Deal cycles lengthen"
        ],
        "next_catalyst": None
    },
    "Siemens (SIEGY) Memo.md": {
        "buy_below": [105, 115],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Disappointing Q1 FY2026 earnings drives stock to $105-115",
            "Broader European market sell-off",
            "China stimulus failing to lift automation demand"
        ],
        "downgrade_triggers": None,
        "next_catalyst": "Q1 FY2026 earnings report - February 2026"
    },
    "TSMC Memo.md": {
        "buy_below": [280, 300],
        "buy_aggressive": 200,
        "sell_above": None,
        "sell_triggers": [
            "Level 4 escalation: temporary blockade under exercise pretext",
            "China foreign reserves dropping >10% in single quarter",
            "TSMC insider selling or accelerating IP transfers to Arizona",
            "US State Department issuing Taiwan travel advisory"
        ],
        "upgrade_catalysts": [
            "Credible US-China diplomatic freeze on Taiwan",
            "Arizona fab reaches 15%+ of advanced node capacity (2028-2029)",
            "TSMC begins manufacturing 2nm in Arizona"
        ],
        "downgrade_triggers": [
            "Level 4 escalation (temporary blockade)",
            "China foreign reserves rapid decline",
            "TSMC accelerating IP transfers to Arizona"
        ],
        "next_catalyst": None
    },
    "UBER - Value Investing Memo (Feb 2026).md": {
        "buy_below": [65, 70],
        "buy_aggressive": 60,
        "sell_above": None,
        "sell_triggers": [
            "Driver classification ruling materially increases costs",
            "Normalized ROIC trending below 10%",
            "FCF margin declining for two consecutive quarters",
            "AV operators successfully bypassing Uber at scale",
            "Operating margin reversal below 8%"
        ],
        "upgrade_catalysts": [
            "Material AV partnership announcements",
            "Operating margin expansion above 15% in next two quarters",
            "Revenue growth acceleration above 20%"
        ],
        "downgrade_triggers": [
            "Driver classification ruling",
            "ROIC below 10%",
            "FCF margin declining two quarters",
            "Operating margin below 8%"
        ],
        "next_catalyst": None
    },
    "UMG Memo.md": {
        "buy_below": [16, 17],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "AI-generated music captures >15% of streaming hours within 2 years",
            "Spotify renegotiates royalty rates downward by more than 5%",
            "Gross margins continue compressing below 36%",
            "Management levers up beyond 2x Net Debt/EBITDA for acquisitions"
        ],
        "upgrade_catalysts": [
            "Price drops to EUR 16-17",
            "AI licensing deals materialize with meaningful revenue (EUR 300M+)",
            "Gross margins stabilize or reverse above 42%",
            "Management initiates material buyback program"
        ],
        "downgrade_triggers": [
            "AI music >15% of streaming hours",
            "Spotify royalty rates down >5%",
            "Gross margins below 36%"
        ],
        "next_catalyst": None
    },
    "Uranium (U3O8) Commodity Memo.md": {
        "buy_below": [75, 80],
        "buy_aggressive": 70,
        "sell_above": None,
        "sell_triggers": [
            "Kazatomprom returns to full capacity AND another major producer ramps simultaneously",
            "Global reactor shutdowns exceed 10 GWe in a single year",
            "Credible nuclear accident causes policy reversal in 3+ countries"
        ],
        "upgrade_catalysts": [
            "Utility contracting accelerates at $90-110 range",
            "AI data center nuclear buildout accelerates faster than expected",
            "Russia enrichment disruption intensifies",
            "Secondary supply fully exhausts"
        ],
        "downgrade_triggers": [
            "Kazatomprom reverses cut + another producer ramps",
            "Nuclear accident or major policy reversal",
            "Reactor shutdowns >10 GWe/year"
        ],
        "next_catalyst": "Utility inventory depletion and contracting cycle acceleration - late 2026 to early 2027"
    },
    "VICI Properties (VICI) Memo.md": {
        "buy_below": None,
        "buy_aggressive": 25,
        "sell_above": None,
        "sell_triggers": [
            "Tenant stress at Caesars (~40% of rent) or MGM (~30%)",
            "Interest rates stay higher for longer with REIT sector depressed"
        ],
        "upgrade_catalysts": [
            "Rate cuts drive REIT re-rating",
            "Accretive acquisitions",
            "Multiple expansion"
        ],
        "downgrade_triggers": [
            "Tenant stress at Caesars or MGM",
            "Interest rates stay higher for longer"
        ],
        "next_catalyst": None
    },
    "Visa Memo.md": {
        "buy_below": [280, 290],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Stablecoin rails demonstrate >5% cross-border volume displacement",
            "Interchange regulation tightens beyond current settlement terms"
        ],
        "upgrade_catalysts": [
            "DOJ case resolved favorably",
            "Trusted Agent Protocol gains demonstrable traction (AI commerce)",
            "Value-added services accelerate to 30%+ of revenue"
        ],
        "downgrade_triggers": [
            "Stablecoin cross-border volume >5%",
            "Interchange regulation tightens materially",
            "DOJ antitrust structural remedies imposed"
        ],
        "next_catalyst": None
    },
    "Wolters Kluwer Memo.md": {
        "buy_below": None,
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": [
            "Organic growth deceleration below 4% in Tax & Accounting or GRC",
            "Customer churn spikes in Health and Legal divisions",
            "Net Debt/EBITDA trending toward 2.5x+"
        ],
        "upgrade_catalysts": [
            "AI disruption fears fade and multiple re-rates toward 20-25x",
            "Cloud software growth acceleration",
            "AI product integration strengthens competitive position"
        ],
        "downgrade_triggers": [
            "AI disruption materializes in Health and Legal financials",
            "Revenue declines in any division",
            "Net Debt/EBITDA >2.5x"
        ],
        "next_catalyst": None
    },
    "Nitto Boseki (3110) Memo.md": {
        "buy_below": [8000, 10000],
        "buy_aggressive": None,
        "sell_above": None,
        "sell_triggers": None,
        "upgrade_catalysts": [
            "Price correction to JPY 8,000-10,000",
            "ROIC improvement to 15%+",
            "Asahi Kasei Q-glass proves unviable at scale"
        ],
        "downgrade_triggers": None,
        "next_catalyst": "FY2027 earnings release - March 2027 (one-time gain cliff visible)"
    },
}

# Files to skip (not individual stock memos)
SKIP_FILES = {"Public Stocks Expected Return 2026.md"}


def parse_frontmatter(content):
    """Extract frontmatter dict and body from markdown content."""
    if not content.startswith("---"):
        return {}, content

    end_idx = content.index("---", 3)
    fm_str = content[3:end_idx].strip()
    body = content[end_idx + 3:].lstrip("\n")

    fm = yaml.safe_load(fm_str) or {}
    return fm, body


def format_yaml_value(value, indent=0):
    """Format a value for YAML output."""
    prefix = "  " * indent
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        # Quote strings that might be misinterpreted
        if any(c in value for c in ":#{}[]&*?|>!%@`"):
            return f'"{value}"'
        return f'"{value}"'
    elif isinstance(value, list):
        if not value:
            return "[]"
        # Check if simple list of numbers
        if all(isinstance(v, (int, float)) for v in value):
            return "[" + ", ".join(str(v) for v in value) + "]"
        # List of strings - multiline
        lines = []
        for item in value:
            lines.append(f'{prefix}  - "{item}"')
        return "\n" + "\n".join(lines)
    return str(value)


def build_frontmatter(fm_dict, trigger_fields):
    """Build complete frontmatter string with trigger fields."""
    lines = ["---"]

    # Write existing fields first
    trigger_keys = {"buy_below", "buy_aggressive", "sell_above", "sell_triggers",
                    "upgrade_catalysts", "downgrade_triggers", "next_catalyst"}

    for key, value in fm_dict.items():
        if key in trigger_keys:
            continue  # Skip, we'll add these from trigger data

        if isinstance(value, list) and value and isinstance(value[0], str):
            # Tags-style list
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, list) and value:
            lines.append(f"{key}: [{', '.join(str(v) for v in value)}]")
        elif value is None:
            lines.append(f"{key}:")
        elif isinstance(value, str):
            if any(c in value for c in ":#{}[]&*?|>!%@`"):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {value}")

    # Add trigger fields
    lines.append("# --- Alert Triggers ---")

    for key in ["buy_below", "buy_aggressive", "sell_above"]:
        val = trigger_fields.get(key)
        if val is None:
            lines.append(f"{key}: null")
        elif isinstance(val, list):
            lines.append(f"{key}: [{', '.join(str(v) for v in val)}]")
        else:
            lines.append(f"{key}: {val}")

    for key in ["sell_triggers", "upgrade_catalysts", "downgrade_triggers"]:
        val = trigger_fields.get(key)
        if val is None:
            lines.append(f"{key}: null")
        else:
            lines.append(f"{key}:")
            for item in val:
                # Escape quotes in the string
                escaped = item.replace('"', '\\"')
                lines.append(f'  - "{escaped}"')

    nc = trigger_fields.get("next_catalyst")
    if nc is None:
        lines.append("next_catalyst: null")
    else:
        escaped = nc.replace('"', '\\"')
        lines.append(f'next_catalyst: "{escaped}"')

    lines.append("---")
    return "\n".join(lines)


def process_memo(filepath, trigger_data):
    """Update a single memo file with trigger fields."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    fm, body = parse_frontmatter(content)

    # Remove any existing trigger fields from frontmatter
    for key in ["buy_below", "buy_aggressive", "sell_above", "sell_triggers",
                 "upgrade_catalysts", "downgrade_triggers", "next_catalyst"]:
        fm.pop(key, None)

    new_fm = build_frontmatter(fm, trigger_data)
    new_content = new_fm + "\n\n" + body

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main():
    updated = 0
    skipped = 0
    errors = []

    for filename in sorted(os.listdir(MEMO_DIR)):
        if not filename.endswith(".md"):
            continue
        if filename in SKIP_FILES:
            skipped += 1
            continue

        filepath = os.path.join(MEMO_DIR, filename)

        if filename in TRIGGERS:
            try:
                process_memo(filepath, TRIGGERS[filename])
                updated += 1
                print(f"  Updated: {filename}")
            except Exception as e:
                errors.append((filename, str(e)))
                print(f"  ERROR: {filename} - {e}")
        else:
            skipped += 1
            print(f"  Skipped (no trigger data): {filename}")

    print(f"\nDone. Updated: {updated}, Skipped: {skipped}, Errors: {len(errors)}")
    if errors:
        for fn, err in errors:
            print(f"  Error in {fn}: {err}")


if __name__ == "__main__":
    main()
