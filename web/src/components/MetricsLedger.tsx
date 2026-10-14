import type { FindingMetrics, MetricValue, MetricsSnapshot } from '../api/types';

function Metric({ m, className }: { m: MetricValue; className?: string }) {
  if (m.status === 'defined' && m.value != null) {
    return <td className={className}>{m.value.toFixed(2)}</td>;
  }
  return (
    <td className="undef" title={m.reason ?? undefined}>
      {m.status === 'undefined_single_class' ? 'Undefined — one class only' : 'Not computed'}
    </td>
  );
}

function RocAuc({ f }: { f: FindingMetrics }) {
  if (f.roc_auc.status === 'defined' && f.roc_auc.value != null) {
    return <td>{f.roc_auc.value.toFixed(2)}</td>;
  }
  if (f.roc_auc.status === 'undefined_single_class') {
    return (
      <td className="undef" title={f.roc_auc.reason ?? undefined}>
        Undefined — one class only (n+ = {f.n_positive})
      </td>
    );
  }
  return (
    <td className="undef" title={f.roc_auc.reason ?? undefined}>
      Not computed
    </td>
  );
}

/** Ledger rendering of /metrics. Never prints numbers when the snapshot is unavailable. */
export function MetricsLedger({ snapshot }: { snapshot: MetricsSnapshot }) {
  if (snapshot.status === 'unavailable') {
    return (
      <div>
        <p>
          <span className="stamp">Metrics unavailable</span>
        </p>
        <p className="reason">{snapshot.reason}</p>
      </div>
    );
  }
  const facts: [string, string][] = [
    ['Dataset', snapshot.dataset_id ?? '—'],
    ['Partition', snapshot.partition === 'test' ? 'Held-out test' : 'Validation'],
    ['Split method', snapshot.split_method ?? '—'],
    ['Grouping unit', snapshot.grouping_unit ?? '—'],
    ['Studies', String(snapshot.n_studies ?? '—')],
    ['Model', snapshot.model ? `${snapshot.model.model_id} ${snapshot.model.model_version}` : '—'],
    ['Preprocessing', snapshot.preprocessing?.version ?? '—'],
    ['Snapshot', snapshot.created_at ?? '—'],
    ['Calibration', snapshot.calibration === 'assessed' ? 'Assessed' : 'Not assessed'],
  ];
  return (
    <div>
      <dl className="facts">
        {facts.map(([k, v]) => (
          <div key={k}>
            <dt>{k}</dt>
            <dd>{v}</dd>
          </div>
        ))}
      </dl>
      <div className="ledger-table-wrap">
        <table className="metrics">
          <caption className="sr-only">Per-finding metrics</caption>
          <thead>
            <tr>
              <th scope="col">Finding</th>
              <th scope="col">Positives</th>
              <th scope="col">Negatives</th>
              <th scope="col">Unknown (excluded)</th>
              <th scope="col">ROC AUC</th>
              <th scope="col">PR AUC</th>
              <th scope="col">Prevalence</th>
              <th scope="col">Sensitivity @ threshold</th>
              <th scope="col">Specificity @ threshold</th>
            </tr>
          </thead>
          <tbody>
            {(snapshot.per_finding ?? []).map((f) => (
              <tr key={f.finding_id}>
                <td>{f.finding_id}</td>
                <td>{f.n_positive}</td>
                <td>{f.n_negative}</td>
                <td>{f.n_unknown}</td>
                <RocAuc f={f} />
                <Metric m={f.pr_auc} />
                <td>{f.prevalence != null ? f.prevalence.toFixed(2) : '—'}</td>
                <Metric m={f.sensitivity} />
                <Metric m={f.specificity} />
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {snapshot.macro_roc_auc ? (
        <p className="reason">
          Macro ROC AUC{' '}
          {snapshot.macro_roc_auc.value != null
            ? snapshot.macro_roc_auc.value.toFixed(2)
            : 'undefined'}{' '}
          over {snapshot.macro_roc_auc.included.length} finding(s)
          {snapshot.macro_roc_auc.excluded.length
            ? `; excluded: ${snapshot.macro_roc_auc.excluded.map((r) => `${r.code} (${r.message})`).join(', ')}`
            : ''}
          .
        </p>
      ) : null}
    </div>
  );
}
