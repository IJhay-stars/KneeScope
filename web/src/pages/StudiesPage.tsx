import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Clock } from 'lucide-react';
import { api } from '../api/client';
import { PLANES, type Plane, type StudyList, type StudySummary } from '../api/types';
import { ErrorPanel } from '../components/ErrorPanel';
import { HatchBlock, StateGlyph } from '../components/StateGlyph';
import { useAsync } from '../hooks/useAsync';

const PLANE_LETTER: Record<Plane, string> = { sagittal: 'S', coronal: 'C', axial: 'A' };
const PLANE_LABEL: Record<Plane, string> = {
  sagittal: 'Sagittal',
  coronal: 'Coronal',
  axial: 'Axial',
};

function PlaneSlots({ study }: { study: StudySummary }) {
  return (
    <span className="planes">
      {PLANES.map((p) =>
        study.planes_available.includes(p) ? (
          <span key={p} className="plane-slot">
            <span aria-hidden="true">{PLANE_LETTER[p]}</span>
            <span className="sr-only">{PLANE_LABEL[p]}</span>
          </span>
        ) : (
          <span key={p} className="plane-slot missing">
            <span aria-hidden="true">—</span>
            <span className="sr-only">{PLANE_LABEL[p]} missing</span>
          </span>
        ),
      )}
    </span>
  );
}

function AnalysisStatus({ status }: { status: StudySummary['analysis_status'] }) {
  switch (status) {
    case 'not_run':
      return (
        <span className="status">
          <StateGlyph status="not_evaluated" />
          Not run
        </span>
      );
    case 'cached':
      return (
        <span className="status cached">
          <Clock className="i" aria-hidden="true" />
          Cached
        </span>
      );
    case 'failed':
      return (
        <span className="status failed">
          <StateGlyph status="failed" />
          Failed
        </span>
      );
  }
}

function SkeletonRows() {
  return (
    <>
      {[0, 1, 2, 3].map((i) => (
        <tr key={i} aria-hidden="true">
          {[0, 1, 2, 3, 4, 5].map((c) => (
            <td key={c}>
              <div className="skel" style={{ width: c === 0 ? '70%' : '50%' }} />
            </td>
          ))}
        </tr>
      ))}
    </>
  );
}

export function StudiesPage() {
  const studies = useAsync<StudyList>('studies', (signal) => api.studies({ signal }));
  const [query, setQuery] = useState('');
  const loading = studies.phase === 'loading';
  const list = studies.phase === 'ready' ? studies.data : undefined;
  const rows = (list?.studies ?? [])
    .filter((s) =>
      `${s.study_id} ${s.display_label}`.toLowerCase().includes(query.trim().toLowerCase()),
    )
    .sort((a, b) => a.study_id.localeCompare(b.study_id));

  return (
    <div className="browser">
      <div className="page-head">
        <div>
          <h1>Studies</h1>
          <p>Choose a study to review. Only the metadata needed for review is shown.</p>
        </div>
        <label>
          <span className="sr-only">Filter studies</span>
          <input
            className="field"
            type="search"
            placeholder="Filter by study ID or label"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
      </div>

      {studies.phase === 'error' ? (
        <div className="table-wrap">
          <ErrorPanel
            error={studies.error}
            title="Studies could not be loaded"
            onRetry={studies.reload}
          />
        </div>
      ) : (
        <div className="table-wrap" aria-busy={loading}>
          {loading ? <p className="msg muted">Loading studies…</p> : null}
          {list && list.studies.length === 0 ? (
            <div className="msg">
              <span />
              <div>
                <h2>No permitted studies</h2>
                <p>
                  The API returned no studies. Add studies with{' '}
                  <code>scripts/build_manifest.py</code>.
                </p>
              </div>
            </div>
          ) : (
            <table className="studies">
              <caption className="sr-only">Studies available for review</caption>
              <thead>
                <tr>
                  <th scope="col">Study</th>
                  <th scope="col">Origin</th>
                  <th scope="col">Planes</th>
                  <th scope="col" className="num">
                    Series
                  </th>
                  <th scope="col">Analysis</th>
                  <th scope="col">
                    <span className="sr-only">Action</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <SkeletonRows />
                ) : (
                  rows.map((s) => (
                    <tr key={s.study_id}>
                      <td>
                        <Link to={`/studies/${encodeURIComponent(s.study_id)}`}>
                          <span className="study-id">{s.study_id}</span>
                        </Link>{' '}
                        <span className="muted">{s.display_label}</span>
                      </td>
                      <td>
                        {s.origin === 'fixture' ? (
                          <span className="origin">
                            <HatchBlock />
                            FIXTURE
                          </span>
                        ) : (
                          <span className="origin">Dataset</span>
                        )}
                      </td>
                      <td>
                        <PlaneSlots study={s} />
                      </td>
                      <td className="num mono">{s.series_count}</td>
                      <td>
                        <AnalysisStatus status={s.analysis_status} />
                      </td>
                      <td>
                        <Link
                          to={`/studies/${encodeURIComponent(s.study_id)}`}
                          aria-label={`Open ${s.study_id}`}
                        >
                          Open
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </div>
      )}
      {list?.origin_notice ? <p className="table-note">{list.origin_notice}</p> : null}
    </div>
  );
}
