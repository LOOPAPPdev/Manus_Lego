import { useEffect, useState } from 'react';
import { Badge, GateTable, RequirementTable, Stat, formatDate, toneForStatus } from '@lego/ui';
import { api, type GateReport, type TraceabilityReport } from '../api.js';
import { ErrorNotice, Hint, Loading } from '../components/Feedback.js';

export function GovernancePage() {
  const [gates, setGates] = useState<GateReport | null>(null);
  const [trace, setTrace] = useState<TraceabilityReport | null>(null);
  const [hints, setHints] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();
    void Promise.all([api.gates(controller.signal), api.requirements(controller.signal)]).then(([gateResult, traceResult]) => {
      if (controller.signal.aborted) return;
      const collected: string[] = [];
      if (gateResult.ok) {
        setGates(gateResult.envelope.data.report);
        if (gateResult.envelope.data.hint) collected.push(gateResult.envelope.data.hint);
      } else {
        setError(gateResult.message);
      }
      if (traceResult.ok) {
        setTrace(traceResult.envelope.data.report);
        if (traceResult.envelope.data.hint) collected.push(traceResult.envelope.data.hint);
      } else {
        setError(traceResult.message);
      }
      setHints(collected);
      setLoading(false);
    });
    return () => controller.abort();
  }, []);

  if (loading) {
    return <Loading label="Loading governance evidence" />;
  }

  return (
    <div className="page">
      <header className="detail-header">
        <div>
          <h1>Quality gates and requirement traceability</h1>
          <p className="lede">
            Gates are evaluated from produced artifacts, not from intent. Each requirement maps a NIST SSDF practice to
            implementation files, automated tests and evidence.
          </p>
        </div>
      </header>

      {error ? <ErrorNotice message={error} /> : null}
      {hints.map((hint) => (
        <Hint key={hint}>{hint}</Hint>
      ))}

      <div className="notice notice--info">
        <strong>What this is not.</strong> A passing gate is evidence that a control was implemented and verified for a specific
        commit. NIST does not certify software; this repository maps practices to controls and publishes the evidence.
      </div>

      {trace ? (
        <section className="stats stats--wide">
          <Stat label="Requirements" value={trace.summary.total} hint="mapped to SSDF practices" />
          <Stat label="Verified" value={trace.summary.verified} hint="implementation + passing tests" />
          <Stat label="Partial" value={trace.summary.partial} hint="some evidence missing" />
          <Stat label="Failing" value={trace.summary.failing} hint="linked test failing" />
        </section>
      ) : null}

      <section className="panel">
        <div className="panel__header">
          <h2>Gate report</h2>
          {gates ? (
            <div className="badges">
              <Badge tone={toneForStatus(gates.overall)}>{gates.overall}</Badge>
              <span className="muted small">
                commit {gates.commit.slice(0, 7)} · {formatDate(gates.generated_at)} · {gates.environment}
              </span>
            </div>
          ) : null}
        </div>
        {gates ? <GateTable gates={gates.gates} /> : <p className="muted">No gate report is available for this commit.</p>}
      </section>

      <section className="panel">
        <div className="panel__header">
          <h2>Requirement traceability</h2>
          {trace ? (
            <span className="muted small">
              commit {trace.commit.slice(0, 7)} · {formatDate(trace.generated_at)}
            </span>
          ) : null}
        </div>
        {trace ? <RequirementTable requirements={trace.requirements} /> : <p className="muted">No traceability report is available.</p>}
      </section>
    </div>
  );
}
