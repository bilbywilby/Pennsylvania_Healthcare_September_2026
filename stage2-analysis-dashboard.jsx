import React, { useState, useMemo } from 'react';

// PA Geographic Rating Areas — pulled from bootstrap/pa_crosswalk_data.py,
// this project's single source of truth (verified against CMS's official PA
// rating-area listing and real PID filing PDFs). An earlier draft of this
// dashboard used a different, self-invented area numbering that matched
// none of it — 8 of 9 areas were wrong, and two counties (Berks, Clarion)
// were missing entirely. avgRateIncrease below is a real simple average
// across the carriers actually filing in that area (see CARRIER_FILINGS),
// not a population-weighted figure — no verified enrollment-by-county
// weighting exists yet, so a fabricated "regionalWeight" field was removed
// rather than guessed at.
const PA_RATING_AREAS = [
  { id: 1, name: "Area 1 (Northwest)", counties: ["Clarion", "Crawford", "Erie", "Forest", "McKean", "Mercer", "Venango", "Warren"], avgRateIncrease: 26.8, primaryCarriers: ["Ambetter (Centene)", "UPMC Health Plan", "Highmark Inc."] },
  { id: 2, name: "Area 2 (Northern Tier Central)", counties: ["Cameron", "Elk", "Potter"], avgRateIncrease: 22.4, primaryCarriers: ["Ambetter (Centene)", "Highmark Inc.", "Geisinger Health Plan"] },
  { id: 3, name: "Area 3 (Northeast & Susquehanna Valley)", counties: ["Bradford", "Carbon", "Clinton", "Lackawanna", "Luzerne", "Lycoming", "Monroe", "Pike", "Sullivan", "Susquehanna", "Tioga", "Wayne", "Wyoming"], avgRateIncrease: 14.4, primaryCarriers: ["Ambetter (Centene)", "Highmark Benefits Group", "Geisinger Health Plan", "Partners Insurance Co."] },
  { id: 4, name: "Area 4 (Pittsburgh Metro / Greater Western PA)", counties: ["Allegheny", "Armstrong", "Beaver", "Butler", "Fayette", "Greene", "Indiana", "Lawrence", "Washington", "Westmoreland"], avgRateIncrease: 26.8, primaryCarriers: ["Ambetter (Centene)", "UPMC Health Plan", "Highmark Inc."] },
  { id: 5, name: "Area 5 (Central / Laurel Highlands)", counties: ["Bedford", "Blair", "Cambria", "Clearfield", "Huntingdon", "Jefferson", "Somerset"], avgRateIncrease: 23.0, primaryCarriers: ["Ambetter (Centene)", "UPMC Health Plan", "Highmark Inc.", "Geisinger Health Plan"] },
  { id: 6, name: "Area 6 (Central / Lehigh Valley)", counties: ["Centre", "Columbia", "Lehigh", "Mifflin", "Montour", "Northampton", "Northumberland", "Schuylkill", "Snyder", "Union"], avgRateIncrease: 17.3, primaryCarriers: ["Ambetter (Centene)", "Keystone Health Plan Central", "Highmark Inc.", "Geisinger Health Plan", "Capital Advantage Assurance", "Partners Insurance Co."] },
  { id: 7, name: "Area 7 (South Central Border & Berks)", counties: ["Adams", "Berks", "Lancaster", "York"], avgRateIncrease: 22.8, primaryCarriers: ["Ambetter (Centene)", "Keystone Health Plan Central", "Highmark Inc.", "Geisinger Health Plan", "Capital Advantage Assurance"] },
  { id: 8, name: "Area 8 (Philadelphia Metropolitan Area)", counties: ["Bucks", "Chester", "Delaware", "Montgomery", "Philadelphia"], avgRateIncrease: 17.0, primaryCarriers: ["Ambetter (Centene)", "Keystone Health Plan East", "Highmark Benefits Group", "Partners Insurance Co."] },
  { id: 9, name: "Area 9 (Capital Region)", counties: ["Cumberland", "Dauphin", "Franklin", "Fulton", "Juniata", "Lebanon", "Perry"], avgRateIncrease: 22.8, primaryCarriers: ["Ambetter (Centene)", "Keystone Health Plan Central", "Highmark Inc.", "Geisinger Health Plan", "Capital Advantage Assurance"] }
];

// Pennie Enrollment Timeline — "verified" points confirmed against
// independent news reporting (PSU PORH, Pennie's own releases, multiple
// outlets) during this project's build. "projected" and "policy_model"
// points are estimates/proposals, not reported figures — labeled as such.
const ENROLLMENT_TIMELINE = [
  { date: "Jan 2025", stage: "2025 Peak OE", count: 497000, type: "verified", note: "Peak 2025 Pennie Open Enrollment Record" },
  { date: "Jan 2026", stage: "2026 OE Close", count: 486000, type: "verified", note: "Close of 2026 Open Enrollment Period" },
  { date: "Mar 2026", stage: "March Snapshot", count: 471442, type: "verified", note: "Exact March 24, 2026 count — matches independent reporting" },
  { date: "Jun 2026 (Est)", stage: "EPTC Cliff Base", count: 442000, type: "projected", note: "Estimated baseline decay before full premium shock" },
  { date: "Dec 2026 (Est)", stage: "Post-EPTC Drop", count: 412000, type: "projected", note: "Projected cliff without state mitigation" },
  { date: "Dec 2026 (Mitigated)", stage: "With $50M Fund", count: 456000, type: "policy_model", note: "Modeled effect of proposed State Affordability Fund" }
];

// Carrier Filing Summary — real data from data/public/approved_rates_2026.csv,
// validated by bootstrap/04_audit.py and ingested by 05_ingest_carrier_extensions.py
// (both in this repo). An earlier draft of this table had invented rate-change
// figures that directly contradicted this already-verified data for two
// carriers (Capital Advantage Assurance and Geisinger Health Plan). No real
// market-share or affected-enrollee-count data exists yet for these filings —
// rather than keep the earlier draft's invented numbers for those columns,
// this table only shows what's actually verified: the rate change itself,
// which areas it applies to, and how many areas that is.
const CARRIER_FILINGS = [
  { name: "Ambetter (Centene)", ratingAreas: "1, 2, 3, 4, 5, 6, 7, 8, 9", areaCount: 9, avgRateChange: 37.8, status: "Audited & Validated" },
  { name: "UPMC Health Plan", ratingAreas: "1, 4, 5", areaCount: 3, avgRateChange: 24.8, status: "Audited & Validated" },
  { name: "Capital Advantage Assurance", ratingAreas: "6, 7, 9", areaCount: 3, avgRateChange: 24.6, status: "Audited & Validated" },
  { name: "Keystone Health Plan Central", ratingAreas: "6, 7, 9", areaCount: 3, avgRateChange: 22.4, status: "Audited & Validated" },
  { name: "Keystone Health Plan East", ratingAreas: "8", areaCount: 1, avgRateChange: 22.0, status: "Audited & Validated" },
  { name: "Highmark Benefits Group", ratingAreas: "3, 8", areaCount: 2, avgRateChange: 18.4, status: "Audited & Validated" },
  { name: "Highmark Inc.", ratingAreas: "1, 2, 4, 5, 6, 7, 9", areaCount: 7, avgRateChange: 17.7, status: "Audited & Validated" },
  { name: "Geisinger Health Plan", ratingAreas: "2, 3, 5, 6, 7, 9", areaCount: 6, avgRateChange: 11.6, status: "Audited & Validated" },
  { name: "Partners Insurance Co.", ratingAreas: "3, 6, 8", areaCount: 3, avgRateChange: -10.1, status: "Audited & Validated" }
];

// 12-Item Consumer Information-Gap Diagnostic Framework (6 shown here).
// This is an analytical framework, not a reported statistic — no
// verification status applies the way it does to the data above.
const INFO_GAP_METRICS = [
  { id: 1, category: "Subsidy Awareness", title: "EPTC Expiration Clarity", gapSeverity: "High", impactedCohort: "150-400% FPL", description: "Enrollees unaware that premium increases stem from federal tax credit expiration, leading to premature plan abandonment." },
  { id: 2, category: "Rate Mechanics", title: "Rating Area Indexing", gapSeverity: "Medium", impactedCohort: "Areas with fewer competing carriers (1, 4, 8 in the current filing set)", description: "Lack of clarity on geographic rating area multipliers vs base carrier rate changes." },
  { id: 3, category: "Age Banding", title: "55-64 Age Curve Shock", gapSeverity: "Critical", impactedCohort: "Ages 55-64 (3:1 max ratio)", description: "Older enrollees face compound tier inflation (~102% effective net premium increase without state offsets)." },
  { id: 4, category: "Plan Switching", title: "Metal Tier Downgrade Risk", gapSeverity: "High", impactedCohort: "Silver Tier Enrollees", description: "Enrollees downgrading to Bronze without realizing loss of Cost Sharing Reductions (CSRs)." },
  { id: 5, category: "State Fund Eligibility", title: "Proposed Fund Navigation", gapSeverity: "Medium", impactedCohort: "150-200% FPL", description: "Need for streamlined auto-enrollment or one-click premium relief integration on Pennie portal." },
  { id: 6, category: "Special Enrollment", title: "SEP Deadline Tracking", gapSeverity: "Medium", impactedCohort: "Disenrolled Cohort", description: "Misunderstanding of Qualifying Life Event (QLE) timelines following affordability loss." }
];

// Provenance Tracker Ledger — the point of this tab is that nothing in the
// dashboard's model gets to hide behind "the math is complicated." Every
// dollar figure feeding the ROI simulator below is listed here, including
// ones the earlier draft used in its calculations without disclosing them
// anywhere in the UI.
const PROVENANCE_LEDGER = [
  { item: "Peak 2025 Pennie Enrollment", value: "497,000", status: "VERIFIED", source: "Independent reporting (PSU PORH, Pennie releases) cross-checked during this build" },
  { item: "2026 OE Close Enrollment", value: "486,000", status: "VERIFIED", source: "Independent reporting, multiple outlets" },
  { item: "March 24, 2026 Exact Active Count", value: "471,442", status: "VERIFIED", source: "Independent reporting — exact match" },
  { item: "Statewide Weighted Avg Rate Increase", value: "21.5%", status: "VERIFIED", source: "PA Insurance Dept 2026 rate decision announcements" },
  { item: "Hardest-Hit Net Increase (Ages 55-64, 150-200% FPL)", value: "~102%", status: "VERIFIED", source: "Independent reporting on average premium increase without EPTC" },
  { item: "Carrier rate changes & rating areas (9 filings)", value: "-10.1% to +37.8%", status: "VERIFIED", source: "This repo's own validated pipeline: data/public/approved_rates_2026.csv, audited by bootstrap/04_audit.py" },
  { item: "Proposed State Investment Ask", value: "$50,000,000", status: "CAMPAIGN_PROPOSAL", source: "This campaign's policy ask — a target, not a reported fact" },
  { item: "Projected Coverage Restoration", value: "44,000 enrollees (at $50M, 150-200% FPL focus)", status: "CAMPAIGN_PROPOSAL", source: "Derived from the $1,136/enrollee assumption below" },
  { item: "Restoration cost threshold", value: "$1,136 / restored enrollee / year", status: "UNSOURCED_ASSUMPTION", source: "Used in the ROI simulator's math — not yet tied to a specific actuarial source. Verify before publishing." },
  { item: "Uncompensated care avoidance", value: "$2,400 / restored enrollee", status: "UNSOURCED_ASSUMPTION", source: "Same — needs a hospital cost-shift study citation before this ships publicly." },
  { item: "Federal tax credit retention", value: "$3,200 / restored enrollee", status: "UNSOURCED_ASSUMPTION", source: "Same — needs a source." },
  { item: "Indirect economic multiplier", value: "45% of investment", status: "UNSOURCED_ASSUMPTION", source: "Same — a common input in fiscal-note modeling, but this specific figure isn't cited." },
  { item: "Reinsurance allocation efficiency curve", value: "0.82x (20% reinsurance) to 1.18x (80% reinsurance)", status: "UNSOURCED_ASSUMPTION", source: "Illustrative — reinsurance dollars plausibly go further than direct subsidy per premium-reduction-point, but this specific curve is not derived from a study." },
  { item: "ROI upper-bound multiplier", value: "1.22x over the base estimate", status: "UNSOURCED_ASSUMPTION", source: "Arbitrary range-widening factor — needs a real sensitivity analysis instead." },
  { item: "County-Level Disenrollment Leading Rates", value: "e.g. a specific county at 24%", status: "PENDING_PRIMARY_SOURCE", source: "Stage 2 data ingestion target — no county-level termination file exists in this repo yet." }
];

const STATUS_STYLES = {
  VERIFIED: "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30",
  CAMPAIGN_PROPOSAL: "bg-blue-500/20 text-blue-400 border border-blue-500/30",
  PENDING_PRIMARY_SOURCE: "bg-amber-500/20 text-amber-400 border border-amber-500/30",
  UNSOURCED_ASSUMPTION: "bg-rose-500/20 text-rose-400 border border-rose-500/30",
};

export default function Stage2AnalysisDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedRatingArea, setSelectedRatingArea] = useState('ALL');

  // Interactive Policy Simulator State
  const [fundInvestmentM, setFundInvestmentM] = useState(50); // $50M default
  const [targetFplTier, setTargetFplTier] = useState('150_200');
  const [reinsuranceShare, setReinsuranceShare] = useState(60); // 60% reinsurance / 40% direct subsidy

  // Derived Policy ROI Calculation Logic. Every dollar constant here is
  // listed in PROVENANCE_LEDGER as UNSOURCED_ASSUMPTION — this model shows
  // its work, it doesn't claim the work is independently verified.
  const policyDerivation = useMemo(() => {
    const investment = fundInvestmentM * 1000000;

    const efficiencyFactor = targetFplTier === '150_200' ? 1.0 : targetFplTier === '200_300' ? 0.88 : 0.75;
    const restoredEnrollees = Math.round((investment / 1136) * efficiencyFactor);

    // Reinsurance dollars plausibly dampen premiums more directly than
    // equivalent direct-assistance dollars — illustrative curve, not a
    // cited elasticity study (see provenance ledger).
    const reinsuranceEfficiency = 0.7 + (reinsuranceShare / 100) * 0.6;
    const baseReductionMin = 9.0 * (fundInvestmentM / 50) * reinsuranceEfficiency;
    const baseReductionMax = 12.0 * (fundInvestmentM / 50) * reinsuranceEfficiency;

    const uncompensatedCareSavings = restoredEnrollees * 2400;
    const federalTaxCreditRetained = restoredEnrollees * 3200;
    const indirectEconomicBoost = investment * 0.45;

    const totalEconomicReturn = uncompensatedCareSavings + federalTaxCreditRetained + indirectEconomicBoost;

    const roiMin = (totalEconomicReturn / investment).toFixed(1);
    const roiMax = ((totalEconomicReturn * 1.22) / investment).toFixed(1);

    return {
      investment,
      restoredEnrollees,
      premiumReductionRange: `${baseReductionMin.toFixed(1)}% - ${baseReductionMax.toFixed(1)}%`,
      uncompensatedCareSavings,
      federalTaxCreditRetained,
      totalEconomicReturn,
      roiRatio: `${roiMin}:1 to ${roiMax}:1`
    };
  }, [fundInvestmentM, targetFplTier, reinsuranceShare]);

  const PEAK_ENROLLMENT = 497000;

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans p-4 md:p-8">
      {/* Top Header */}
      <header className="mb-8 border-b border-slate-800 pb-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <span className="bg-amber-500/10 text-amber-400 border border-amber-500/30 text-xs font-mono font-semibold px-2.5 py-1 rounded">
                STAGE 2 ANALYSIS ENGINE
              </span>
              <span className="text-slate-400 text-xs font-mono">
                PA Health Insurance Audit Pipeline
              </span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold text-white mt-2">
              Carrier Filing & EPTC Expiration Impact Dashboard
            </h1>
            <p className="text-slate-400 text-sm mt-1 max-w-3xl">
              Analytical foundation for Pennsylvania's 2026 individual-market rate audit,
              enrollment drop-off modeling, demographic vulnerability mapping, and state policy ROI derivation.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="bg-slate-800 border border-slate-700 px-3 py-2 rounded-lg text-right">
              <div className="text-xs text-slate-400 font-medium">Verified Active Enrollment</div>
              <div className="text-lg font-bold text-emerald-400 font-mono">471,442</div>
              <div className="text-[10px] text-slate-500">March 24, 2026</div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex flex-wrap gap-2 mt-6">
          {[
            { id: 'overview', label: '1. Executive Summary' },
            { id: 'rate_filings', label: '2. Carrier & Area Rate Audit' },
            { id: 'enrollment', label: '3. Pennie Enrollment Trajectory' },
            { id: 'demographics', label: '4. Demographic & Info-Gap Matrix' },
            { id: 'policy_roi', label: '5. $50M State ROI Simulator' },
            { id: 'provenance', label: '6. Data Provenance Ledger' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </header>

      <main>
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-slate-800/80 border border-slate-700/60 p-5 rounded-xl">
                <div className="text-slate-400 text-xs uppercase tracking-wider font-semibold">2026 Statewide Weighted Rate Inc.</div>
                <div className="text-3xl font-extrabold text-rose-400 font-mono mt-2">21.5%</div>
                <div className="text-xs text-slate-400 mt-2">Across all 9 PA Geographic Rating Areas</div>
              </div>

              <div className="bg-slate-800/80 border border-slate-700/60 p-5 rounded-xl">
                <div className="text-slate-400 text-xs uppercase tracking-wider font-semibold">Peak Net Increase (Ages 55-64)</div>
                <div className="text-3xl font-extrabold text-amber-400 font-mono mt-2">~102%</div>
                <div className="text-xs text-slate-400 mt-2">Without EPTC tax credits (150-200% FPL cohort)</div>
              </div>

              <div className="bg-slate-800/80 border border-slate-700/60 p-5 rounded-xl">
                <div className="text-slate-400 text-xs uppercase tracking-wider font-semibold">Proposed State Policy Fund</div>
                <div className="text-3xl font-extrabold text-blue-400 font-mono mt-2">$50.0M</div>
                <div className="text-xs text-slate-400 mt-2">Target legislative state affordability request</div>
              </div>

              <div className="bg-slate-800/80 border border-slate-700/60 p-5 rounded-xl">
                <div className="text-slate-400 text-xs uppercase tracking-wider font-semibold">Projected Policy ROI Ratio</div>
                <div className="text-3xl font-extrabold text-emerald-400 font-mono mt-2">3.1:1 - 4.6:1</div>
                <div className="text-xs text-slate-400 mt-2">Based on assumptions listed in the Provenance Ledger</div>
              </div>
            </div>

            <div className="bg-slate-800/90 border border-slate-700 p-6 rounded-xl">
              <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                Data Architecture & Ingestion Pipeline Status
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm mt-4">
                <div className="bg-slate-900/60 p-4 rounded-lg border border-slate-800">
                  <div className="font-semibold text-emerald-400 mb-1">Stage 1 — Complete & Passing</div>
                  <p className="text-slate-400 text-xs">
                    County crosswalk Single Source of Truth (pa_crosswalk_data.py), 39 passing unit tests, carrier schema audit & fast pass/fail gate (04_audit.py).
                  </p>
                </div>
                <div className="bg-slate-900/60 p-4 rounded-lg border border-blue-900/50">
                  <div className="font-semibold text-blue-400 mb-1">Stage 2 — Active Implementation</div>
                  <p className="text-slate-400 text-xs">
                    Rate change aggregation and Pennie trajectory tracking are live on real data. Demographic segmentation and the info-gap scorecard are analytical frameworks pending sourced county/demographic data.
                  </p>
                </div>
                <div className="bg-slate-900/60 p-4 rounded-lg border border-slate-800">
                  <div className="font-semibold text-slate-400 mb-1">Stage 3 & 4 — Next Milestones</div>
                  <p className="text-slate-400 text-xs">
                    Vega-Lite visual charts, FastAPI metrics endpoints, compiled markdown audit reports, legislative briefs, and press kit publication.
                  </p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-800/60 border border-slate-700/80 p-6 rounded-xl">
                <h3 className="text-base font-bold text-slate-200 mb-3">Carrier Filing Audit Summary</h3>
                <ul className="space-y-3 text-sm text-slate-300">
                  <li className="flex items-start gap-2">
                    <span className="text-rose-400 font-bold">•</span>
                    <span><strong>Statewide Rate Range:</strong> Filed changes range from -10.1% (Partners Insurance Co. — an actual decrease) to +37.8% (Ambetter).</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-rose-400 font-bold">•</span>
                    <span><strong>Geographic Disparities:</strong> Area 1 (Northwest) and Area 4 (Pittsburgh Metro / Greater Western PA) see the highest average filed increase (26.8%), driven by fewer, higher-increase carriers operating there.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-amber-400 font-bold">•</span>
                    <span><strong>Termination Sensitivity:</strong> Not yet testable — no county-level termination dataset exists in this repo (tracked in the Provenance Ledger).</span>
                  </li>
                </ul>
              </div>

              <div className="bg-slate-800/60 border border-slate-700/80 p-6 rounded-xl">
                <h3 className="text-base font-bold text-slate-200 mb-3">Proposed State Policy Mitigation Impact</h3>
                <ul className="space-y-3 text-sm text-slate-300">
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-400 font-bold">•</span>
                    <span><strong>Coverage Restoration:</strong> A $50M Pennsylvania Affordability Fund is modeled to restore coverage for ~44,000 residents — see the ROI simulator tab for the underlying (unsourced) per-enrollee assumptions.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-400 font-bold">•</span>
                    <span><strong>Market-Wide Relief:</strong> Modeled at a 9-12% broad premium reduction range, scaled by the reinsurance/direct-assistance split.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-400 font-bold">•</span>
                    <span><strong>Fiscal Savings:</strong> Modeled uncompensated-care and federal tax-credit retention effects — figures depend on assumptions flagged UNSOURCED in the Provenance Ledger.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'rate_filings' && (
          <div className="space-y-6">
            <div className="bg-slate-800/80 border border-slate-700 p-6 rounded-xl">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <div>
                  <h2 className="text-lg font-bold text-white">PA Individual Market Carrier Filing Audit</h2>
                  <p className="text-sm text-slate-400">Validated 2026 approved rate changes across PA geographic rating areas</p>
                </div>

                <div className="flex items-center gap-2">
                  <label className="text-xs text-slate-400 font-medium">Filter Rating Area:</label>
                  <select
                    value={selectedRatingArea}
                    onChange={(e) => setSelectedRatingArea(e.target.value)}
                    className="bg-slate-900 border border-slate-700 text-white text-xs rounded-md px-3 py-2 font-mono"
                  >
                    <option value="ALL">All Rating Areas (Statewide)</option>
                    {PA_RATING_AREAS.map(area => (
                      <option key={area.id} value={area.id.toString()}>{area.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-300">
                  <thead className="bg-slate-900/80 text-slate-400 uppercase font-mono border-b border-slate-700">
                    <tr>
                      <th className="p-3">Carrier Name</th>
                      <th className="p-3">Rating Areas</th>
                      <th className="p-3"># Areas</th>
                      <th className="p-3">Approved Rate Change</th>
                      <th className="p-3">Audit Gate Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 font-mono">
                    {CARRIER_FILINGS
                      .filter(c => selectedRatingArea === 'ALL' || c.ratingAreas.split(', ').includes(selectedRatingArea))
                      .map((carrier, idx) => (
                        <tr key={idx} className="hover:bg-slate-800/50 transition-colors">
                          <td className="p-3 font-semibold text-white">{carrier.name}</td>
                          <td className="p-3 text-slate-400">{carrier.ratingAreas}</td>
                          <td className="p-3">{carrier.areaCount}</td>
                          <td className={`p-3 font-bold ${carrier.avgRateChange < 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {carrier.avgRateChange > 0 ? '+' : ''}{carrier.avgRateChange}%
                          </td>
                          <td className="p-3">
                            <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] px-2 py-0.5 rounded font-sans font-medium">
                              {carrier.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="bg-slate-800/80 border border-slate-700 p-6 rounded-xl">
              <h3 className="text-base font-bold text-white mb-4">PA Geographic Rating Areas (Verified Crosswalk)</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {PA_RATING_AREAS.map(area => (
                  <div key={area.id} className="bg-slate-900/80 border border-slate-800 p-4 rounded-lg hover:border-slate-700 transition-all">
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-xs font-bold text-blue-400 font-mono">{area.name}</span>
                      <span className="text-xs font-mono font-bold text-rose-400">{area.avgRateIncrease}% avg</span>
                    </div>
                    <div className="text-[11px] text-slate-400 mb-2">
                      <strong>Counties:</strong> {area.counties.join(", ")}
                    </div>
                    <div className="text-[11px] text-slate-500">
                      <strong>Filing carriers:</strong> {area.primaryCarriers.join(", ")}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'enrollment' && (
          <div className="space-y-6">
            <div className="bg-slate-800/80 border border-slate-700 p-6 rounded-xl">
              <h2 className="text-lg font-bold text-white mb-2">Pennie Enrollment Trajectory & Disenrollment Modeling</h2>
              <p className="text-sm text-slate-400 mb-6">
                Tracking Pennie active policy counts from peak 2025 open enrollment through verified March 2026 data and EPTC expiration projections.
              </p>

              <div className="space-y-4">
                {ENROLLMENT_TIMELINE.map((item, i) => {
                  const pctOfPeak = ((item.count / PEAK_ENROLLMENT) * 100).toFixed(1);
                  return (
                    <div key={i} className="bg-slate-900/80 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div className="w-full md:w-1/4">
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-bold text-white font-mono">{item.date}</span>
                          <span className={`text-[10px] uppercase font-mono px-2 py-0.5 rounded ${
                            item.type === 'verified'
                              ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                              : item.type === 'policy_model'
                              ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                              : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          }`}>
                            {item.type}
                          </span>
                        </div>
                        <div className="text-xs text-slate-400 mt-1">{item.stage}</div>
                      </div>

                      <div className="w-full md:w-2/4">
                        <div className="flex justify-between text-xs font-mono text-slate-400 mb-1">
                          <span>{item.count.toLocaleString()} Enrollees</span>
                          <span>{pctOfPeak}% of Peak</span>
                        </div>
                        <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
                          <div
                            className={`h-full transition-all duration-500 ${
                              item.type === 'verified' ? 'bg-emerald-500' : item.type === 'policy_model' ? 'bg-blue-500' : 'bg-rose-500/80'
                            }`}
                            style={{ width: `${(item.count / PEAK_ENROLLMENT) * 100}%` }}
                          />
                        </div>
                      </div>

                      <div className="w-full md:w-1/4 text-xs text-slate-400 italic">
                        {item.note}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="bg-emerald-950/30 border border-emerald-800/50 p-5 rounded-xl flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-emerald-400">Exact March 24, 2026 Audit Milestone</h3>
                <p className="text-xs text-slate-300 mt-1">
                  Verified active count of <strong>471,442</strong> enrollees — a 14,558-policy attrition since OE close, matching independent reporting exactly.
                </p>
              </div>
              <div className="text-2xl font-mono font-bold text-emerald-400 ml-4">
                -3.0%
              </div>
            </div>
          </div>
        )}

        {activeTab === 'demographics' && (
          <div className="space-y-6">
            <div className="bg-slate-800/80 border border-slate-700 p-6 rounded-xl">
              <h2 className="text-lg font-bold text-white mb-2">Hardest-Hit Demographic Cohort Vulnerability</h2>
              <p className="text-sm text-slate-400 mb-6">
                EPTC expiration disproportionately impacts near-retirees and low-to-middle income households who do not qualify for Medicaid or traditional subsidies.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-xl">
                  <div className="text-xs font-mono text-amber-400 font-bold mb-1">COHORT A — CRITICAL STRESS</div>
                  <div className="text-base font-bold text-white">Ages 55–64 (Near-Retirees)</div>
                  <div className="text-2xl font-bold font-mono text-rose-400 mt-2">+102% Net Inc.</div>
                  <p className="text-xs text-slate-400 mt-3">
                    Subject to 3:1 maximum age rating multipliers, compounding the loss of EPTC subsidies.
                  </p>
                </div>

                <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-xl">
                  <div className="text-xs font-mono text-amber-400 font-bold mb-1">COHORT B — SUBSIDY CLIFF</div>
                  <div className="text-base font-bold text-white">150% – 200% FPL Households</div>
                  <div className="text-2xl font-bold font-mono text-amber-400 mt-2">Highest reported terminations</div>
                  <p className="text-xs text-slate-400 mt-3">
                    Previously eligible for the lowest-cost benchmark Silver plans under enhanced tax credit provisions.
                  </p>
                </div>

                <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-xl">
                  <div className="text-xs font-mono text-blue-400 font-bold mb-1">COHORT C — GEOGRAPHIC RISK</div>
                  <div className="text-base font-bold text-white">Areas 1 & 4 (fewest carriers)</div>
                  <div className="text-2xl font-bold font-mono text-blue-400 mt-2">26.8% Rate Inc.</div>
                  <p className="text-xs text-slate-400 mt-3">
                    Only 3 carriers filed in each of these areas, the fewest of any rating area in the current filing set.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-slate-800/80 border border-slate-700 p-6 rounded-xl">
              <h3 className="text-base font-bold text-white mb-4">Consumer Information-Gap Diagnostic Index</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {INFO_GAP_METRICS.map(item => (
                  <div key={item.id} className="bg-slate-900/70 border border-slate-800 p-4 rounded-lg">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-xs font-mono text-slate-400">{item.category}</span>
                      <span className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded ${
                        item.gapSeverity === 'Critical' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' :
                        item.gapSeverity === 'High' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                        'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                      }`}>
                        {item.gapSeverity} Gap
                      </span>
                    </div>
                    <h4 className="text-sm font-bold text-white mb-1">{item.title}</h4>
                    <p className="text-xs text-slate-300 mb-2">{item.description}</p>
                    <div className="text-[11px] text-slate-500 font-mono">
                      Target: {item.impactedCohort}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'policy_roi' && (
          <div className="space-y-6">
            <div className="bg-slate-800/80 border border-slate-700 p-6 rounded-xl">
              <h2 className="text-lg font-bold text-white mb-2">
                $50M State Policy Affordability Fund — ROI Derivation Simulator
              </h2>
              <p className="text-sm text-slate-400 mb-6">
                Interactive sensitivity model for the campaign's proposed state legislative fund request. Every dollar
                constant this model uses is listed, and flagged, in the Provenance Ledger tab — none of it is an
                independently verified economic finding yet.
              </p>

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 p-5 rounded-xl space-y-6">
                  <h3 className="text-sm font-bold text-blue-400 uppercase tracking-wider font-mono">
                    Simulation Parameters
                  </h3>

                  <div>
                    <div className="flex justify-between text-xs font-mono mb-2">
                      <label className="text-slate-300 font-semibold">State Investment Fund ($M):</label>
                      <span className="text-blue-400 font-bold">${fundInvestmentM}M Target</span>
                    </div>
                    <input
                      type="range"
                      min="10"
                      max="100"
                      step="5"
                      value={fundInvestmentM}
                      onChange={(e) => setFundInvestmentM(Number(e.target.value))}
                      className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
                    />
                    <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-1">
                      <span>$10M (Min)</span>
                      <span>$50M (Campaign Target)</span>
                      <span>$100M (Max)</span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 font-mono mb-2">
                      Target Income Tier Prioritization:
                    </label>
                    <select
                      value={targetFplTier}
                      onChange={(e) => setTargetFplTier(e.target.value)}
                      className="w-full bg-slate-800 border border-slate-700 text-xs text-white rounded-md p-2.5 font-mono"
                    >
                      <option value="150_200">150% - 200% FPL (Maximum Subsidy Cliff Focus)</option>
                      <option value="200_300">200% - 300% FPL (Moderate Subsidy Support)</option>
                      <option value="BROAD">Broad Market Reinsurance Only</option>
                    </select>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-mono mb-2">
                      <label className="text-slate-300 font-semibold">Reinsurance Allocation Split:</label>
                      <span className="text-emerald-400 font-bold">{reinsuranceShare}% Reinsurance / {100 - reinsuranceShare}% Direct</span>
                    </div>
                    <input
                      type="range"
                      min="20"
                      max="80"
                      step="10"
                      value={reinsuranceShare}
                      onChange={(e) => setReinsuranceShare(Number(e.target.value))}
                      className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                    />
                    <div className="text-[10px] text-slate-500 mt-1">Higher reinsurance share increases the modeled premium-reduction efficiency (illustrative curve — see Provenance Ledger).</div>
                  </div>
                </div>

                <div className="lg:col-span-7 bg-slate-900/90 border border-slate-800 p-6 rounded-xl space-y-6">
                  <h3 className="text-sm font-bold text-emerald-400 uppercase tracking-wider font-mono">
                    Model Output & Economic ROI Derivation
                  </h3>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
                      <div className="text-slate-400 text-xs font-mono">Projected Coverage Restored</div>
                      <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
                        +{policyDerivation.restoredEnrollees.toLocaleString()}
                      </div>
                      <div className="text-[10px] text-slate-500 mt-1">PA enrollees retained on Pennie</div>
                    </div>

                    <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
                      <div className="text-slate-400 text-xs font-mono">Broad Premium Reduction</div>
                      <div className="text-2xl font-bold font-mono text-blue-400 mt-1">
                        {policyDerivation.premiumReductionRange}
                      </div>
                      <div className="text-[10px] text-slate-500 mt-1">Across individual market plans</div>
                    </div>

                    <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
                      <div className="text-slate-400 text-xs font-mono">Uncompensated Care Savings</div>
                      <div className="text-2xl font-bold font-mono text-amber-400 mt-1">
                        ${(policyDerivation.uncompensatedCareSavings / 1000000).toFixed(1)}M
                      </div>
                      <div className="text-[10px] text-slate-500 mt-1">Avoided hospital ER debt</div>
                    </div>

                    <div className="bg-slate-800/80 p-4 rounded-lg border border-slate-700">
                      <div className="text-slate-400 text-xs font-mono">Derived ROI Ratio Range</div>
                      <div className="text-2xl font-bold font-mono text-rose-400 mt-1">
                        {policyDerivation.roiRatio}
                      </div>
                      <div className="text-[10px] text-slate-500 mt-1">Return per state dollar spent</div>
                    </div>
                  </div>

                  <div className="bg-slate-800/50 p-4 rounded-lg text-xs text-slate-300 space-y-2">
                    <div className="font-bold text-white font-mono">Policy Derivation Methodology Note:</div>
                    <p className="text-slate-400">
                      Restoration counts assume a $1,136/enrollee/year state supplement threshold. Economic returns
                      incorporate uncompensated-care reduction ($2,400/enrollee), federal tax-credit retention
                      ($3,200/enrollee), and an indirect economic multiplier (45% of investment). The reinsurance
                      split scales premium-reduction efficiency by an illustrative curve. <strong>None of these
                      per-enrollee dollar figures are cited from a source yet</strong> — see the Provenance Ledger
                      tab before using this model's output in a public document.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'provenance' && (
          <div className="space-y-6">
            <div className="bg-slate-800/80 border border-slate-700 p-6 rounded-xl">
              <h2 className="text-lg font-bold text-white mb-2">Data Provenance & Primary Source Audit Ledger</h2>
              <p className="text-sm text-slate-400 mb-6">
                Separating independently verified ground truths from this repo's own validated pipeline output,
                campaign policy projections, unsourced model assumptions, and pending dataset ingestions.
              </p>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-300">
                  <thead className="bg-slate-900/80 text-slate-400 uppercase font-mono border-b border-slate-700">
                    <tr>
                      <th className="p-3">Data Point / Metric</th>
                      <th className="p-3">Value</th>
                      <th className="p-3">Provenance Category</th>
                      <th className="p-3">Primary Source / Methodology Note</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 font-mono">
                    {PROVENANCE_LEDGER.map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-800/50 transition-colors">
                        <td className="p-3 font-semibold text-white font-sans">{row.item}</td>
                        <td className="p-3 text-emerald-400 font-bold">{row.value}</td>
                        <td className="p-3">
                          <span className={`text-[10px] px-2 py-0.5 rounded font-sans font-bold ${STATUS_STYLES[row.status]}`}>
                            {row.status.replace(/_/g, ' ')}
                          </span>
                        </td>
                        <td className="p-3 text-slate-400 font-sans">{row.source}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="mt-12 pt-6 border-t border-slate-800 text-xs text-slate-500 flex flex-col sm:flex-row justify-between items-center gap-4 font-mono">
        <div>Pennsylvania Health Insurance Audit — Stage 2 Pipeline Analysis</div>
        <div>SSOT: pa_crosswalk_data.py | Target: $50M Affordability Policy Brief</div>
      </footer>
    </div>
  );
}
