import {
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent as ReactKeyboardEvent,
} from 'react';
import { useParams } from 'react-router-dom';
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-react';
import { ApiRequestError, api } from '../api/client';
import {
  PLANES,
  type FindingDefinition,
  type FindingResult,
  type Plane,
  type PredictionResponse,
  type StudyDetail,
  type StudyLabels,
} from '../api/types';
import { ErrorPanel } from '../components/ErrorPanel';
import { FindingRow, type LabelReveal } from '../components/FindingRow';
import { ProvenanceStrip } from '../components/ProvenanceStrip';
import { SliceViewer } from '../components/SliceViewer';
import { useAsync } from '../hooks/useAsync';

const PLANE_LABEL: Record<Plane, string> = {
  sagittal: 'Sagittal',
  coronal: 'Coronal',
  axial: 'Axial',
};

type Analysis =
  | { phase: 'idle' }
  | { phase: 'running' }
  | { phase: 'done'; result: PredictionResponse }
  | { phase: 'error'; error: ApiRequestError };

type Labels =
  | { phase: 'idle' }
  | { phase: 'loading' }
  | { phase: 'ready'; data: StudyLabels }
  | { phase: 'error'; error: ApiRequestError };

const middle = (n: number) => Math.floor((n - 1) / 2);

export function ReviewPage() {
  const { studyId = '' } = useParams();
  const study = useAsync<StudyDetail>(`study:${studyId}`, (signal) =>
    api.study(studyId, { signal }),
  );
  const profile = useAsync('findings', (signal) => api.findings({ signal }));

  return (
    <>
      {study.phase === 'ready' && profile.phase === 'ready' ? (
        // Keyed by study: selection, analysis and revealed labels reset on study change.
        <Workspace
          key={study.data.study_id}
          study={study.data}
          definitions={profile.data.findings}
        />
      ) : (
        <div
          className="browser"
          aria-busy={study.phase === 'loading' || profile.phase === 'loading'}
        >
          {study.phase === 'error' ? (
            <ErrorPanel
              error={study.error}
              title="Study could not be loaded"
              onRetry={study.reload}
            />
          ) : profile.phase === 'error' ? (
            <ErrorPanel
              error={profile.error}
              title="Findings list could not be loaded"
              onRetry={profile.reload}
            />
          ) : (
            <p className="muted">Loading study…</p>
          )}
        </div>
      )}
    </>
  );
}

function notEvaluated(d: FindingDefinition): FindingResult {
  return {
    finding_id: d.finding_id,
    display_name: d.display_name,
    status: 'not_evaluated',
    explanation_available: false,
  };
}

function Workspace({
  study,
  definitions,
}: {
  study: StudyDetail;
  definitions: FindingDefinition[];
}) {
  const planesPresent = PLANES.filter((p) => study.planes_available.includes(p));
  const [plane, setPlane] = useState<Plane | null>(planesPresent[0] ?? null);
  const seriesForPlane = useMemo(
    () => (plane ? study.series.filter((s) => s.plane === plane) : []),
    [study.series, plane],
  );
  const [seriesId, setSeriesId] = useState<string | null>(seriesForPlane[0]?.series_id ?? null);
  const series = seriesForPlane.find((s) => s.series_id === seriesId) ?? seriesForPlane[0] ?? null;
  const [slice, setSlice] = useState(series ? middle(series.num_slices) : 0);

  const [analysis, setAnalysis] = useState<Analysis>({ phase: 'idle' });
  const [labels, setLabels] = useState<Labels>({ phase: 'idle' });
  const [revealed, setRevealed] = useState<ReadonlySet<string>>(new Set());
  const [announcement, setAnnouncement] = useState('');
  const runningRef = useRef(false);

  const choosePlane = (p: Plane) => {
    if (!study.planes_available.includes(p) || p === plane) return;
    const first = study.series.find((s) => s.plane === p);
    setPlane(p);
    setSeriesId(first?.series_id ?? null);
    setSlice(first ? middle(first.num_slices) : 0); // switching plane resets to the middle slice
  };
  const chooseSeries = (id: string) => {
    const s = study.series.find((x) => x.series_id === id);
    if (!s) return;
    setSeriesId(id);
    setSlice(middle(s.num_slices));
  };
  const lastSlice = (series?.num_slices ?? 1) - 1;
  const goTo = (i: number) => setSlice(Math.min(Math.max(i, 0), lastSlice));

  const run = () => {
    if (runningRef.current) return;
    runningRef.current = true;
    setAnalysis({ phase: 'running' });
    setAnnouncement('Analysis started.');
    api
      .predict({ study_id: study.study_id })
      .then((result) => {
        setAnalysis({ phase: 'done', result });
        setAnnouncement('Analysis complete.');
      })
      .catch((e: unknown) => {
        const error =
          e instanceof ApiRequestError
            ? e
            : new ApiRequestError({ code: 'INTERNAL_ERROR', message: 'Unexpected client error.' });
        setAnalysis({ phase: 'error', error });
        setAnnouncement(`Analysis failed. ${error.code}.`);
      })
      .finally(() => {
        runningRef.current = false;
      });
  };

  const reveal = (findingId: string) => {
    setRevealed((prev) => new Set(prev).add(findingId));
    if (labels.phase === 'idle' || labels.phase === 'error') {
      setLabels({ phase: 'loading' });
      api
        .labels(study.study_id)
        .then((data) => setLabels({ phase: 'ready', data }))
        .catch((e: unknown) =>
          setLabels({
            phase: 'error',
            error:
              e instanceof ApiRequestError
                ? e
                : new ApiRequestError({
                    code: 'INTERNAL_ERROR',
                    message: 'Unexpected client error.',
                  }),
          }),
        );
    }
  };

  const keyHandler = useRef<(e: KeyboardEvent) => void>(() => {});
  useEffect(() => {
    keyHandler.current = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      const t = e.target;
      if (
        t instanceof HTMLElement &&
        (t.tagName === 'INPUT' || t.tagName === 'SELECT' || t.tagName === 'TEXTAREA')
      ) {
        return;
      }
      const planeKeys: Record<string, Plane> = { '1': 'sagittal', '2': 'coronal', '3': 'axial' };
      switch (e.key) {
        case 'j':
        case 'ArrowDown':
          goTo(slice + 1);
          break;
        case 'k':
        case 'ArrowUp':
          goTo(slice - 1);
          break;
        case 'PageDown':
          goTo(slice + 10);
          break;
        case 'PageUp':
          goTo(slice - 10);
          break;
        case 'Home':
          goTo(0);
          break;
        case 'End':
          goTo(lastSlice);
          break;
        case 'r':
          if (analysis.phase !== 'running') run();
          break;
        default: {
          const p = planeKeys[e.key];
          if (!p) return;
          choosePlane(p);
        }
      }
      e.preventDefault();
    };
  });
  useEffect(() => {
    const listener = (e: KeyboardEvent) => keyHandler.current(e);
    window.addEventListener('keydown', listener);
    return () => window.removeEventListener('keydown', listener);
  }, []);

  const result = analysis.phase === 'done' ? analysis.result : null;
  const source = result?.provenance.source ?? null;
  const rows: FindingResult[] = result ? result.findings : definitions.map(notEvaluated);
  const labelFor = (id: string): LabelReveal | undefined => {
    if (!revealed.has(id)) return undefined;
    if (labels.phase === 'ready') {
      return { phase: 'ready', label: labels.data.labels.find((l) => l.finding_id === id) ?? null };
    }
    if (labels.phase === 'error') {
      return { phase: 'error', code: labels.error.code, message: labels.error.message };
    }
    return { phase: 'loading' };
  };

  return (
    <div className="workspace">
      <section className="stage" aria-label="Viewer">
        <div className="stage-head">
          <div>
            <h1>
              <span className="mono">{study.study_id}</span>{' '}
              <span className="muted">{study.display_label}</span>
            </h1>
          </div>
          <PlaneTabs study={study} plane={plane} onChoose={choosePlane} />
          {seriesForPlane.length > 0 ? (
            <label className="series-select">
              Series
              <select
                className="field"
                value={series?.series_id ?? ''}
                onChange={(e) => chooseSeries(e.target.value)}
              >
                {seriesForPlane.map((s) => (
                  <option key={s.series_id} value={s.series_id}>
                    {s.description ?? s.series_id} ({s.num_slices})
                  </option>
                ))}
              </select>
            </label>
          ) : null}
        </div>

        {series && plane ? (
          <SliceViewer
            studyId={study.study_id}
            series={series}
            plane={plane}
            sliceIndex={slice}
            fixtureStripe={study.origin === 'fixture' || source === 'fixture'}
          />
        ) : (
          <div className="viewer">
            <div className="viewer-msg">
              This study has no series with a known plane to display.
            </div>
          </div>
        )}

        <div className="controls" role="group" aria-label="Slice controls">
          <button
            type="button"
            className="btn icon-btn"
            aria-label="First slice"
            title="First slice (Home)"
            disabled={!series}
            onClick={() => goTo(0)}
          >
            <ChevronsLeft className="i" aria-hidden="true" />
          </button>
          <button
            type="button"
            className="btn icon-btn"
            aria-label="Previous slice"
            title="Previous slice (k, ↑)"
            disabled={!series}
            onClick={() => goTo(slice - 1)}
          >
            <ChevronLeft className="i" aria-hidden="true" />
          </button>
          <input
            type="range"
            aria-label="Slice"
            min={1}
            max={Math.max(series?.num_slices ?? 1, 1)}
            value={slice + 1}
            disabled={!series}
            aria-valuetext={`Slice ${slice + 1} of ${series?.num_slices ?? 0}`}
            onChange={(e) => goTo(Number(e.target.value) - 1)}
          />
          <button
            type="button"
            className="btn icon-btn"
            aria-label="Next slice"
            title="Next slice (j, ↓)"
            disabled={!series}
            onClick={() => goTo(slice + 1)}
          >
            <ChevronRight className="i" aria-hidden="true" />
          </button>
          <button
            type="button"
            className="btn icon-btn"
            aria-label="Last slice"
            title="Last slice (End)"
            disabled={!series}
            onClick={() => goTo(lastSlice)}
          >
            <ChevronsRight className="i" aria-hidden="true" />
          </button>
          <span className="mono slice-readout">
            {series ? `${slice + 1} / ${series.num_slices}` : '— / —'}
          </span>
        </div>
      </section>

      <aside className="findings" aria-label="Findings">
        <div className="col-head">
          <div>
            <h2>Findings</h2>
            <p>Model scores for the active finding profile</p>
          </div>
          <button
            type="button"
            className="btn primary"
            onClick={run}
            disabled={analysis.phase === 'running'}
          >
            {analysis.phase === 'running' ? 'Analysing…' : 'Run analysis'}
          </button>
        </div>
        <div className="sr-only" role="status" aria-live="polite">
          {announcement}
        </div>
        {analysis.phase === 'running' ? (
          <div className="run-status">Analysing… waiting for the API.</div>
        ) : null}
        {analysis.phase === 'error' ? (
          <ErrorPanel error={analysis.error} title="Analysis failed" onRetry={run} />
        ) : null}
        {result ? <ProvenanceStrip result={result} /> : null}
        {result?.missing_planes.length ? (
          <div className="run-status">
            Missing planes: {result.missing_planes.map((p) => PLANE_LABEL[p]).join(', ')}
          </div>
        ) : null}
        <ul className="finding-list" aria-busy={analysis.phase === 'running'}>
          {rows.map((f) => (
            <FindingRow
              key={f.finding_id}
              finding={f}
              source={source}
              reveal={labelFor(f.finding_id)}
              onRevealLabel={() => reveal(f.finding_id)}
              onRetry={run}
            />
          ))}
        </ul>
      </aside>
    </div>
  );
}

function PlaneTabs({
  study,
  plane,
  onChoose,
}: {
  study: StudyDetail;
  plane: Plane | null;
  onChoose: (p: Plane) => void;
}) {
  const enabled = PLANES.filter((p) => study.planes_available.includes(p));
  const onKey = (e: ReactKeyboardEvent) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const i = plane ? enabled.indexOf(plane) : 0;
    const next = enabled[(i + (e.key === 'ArrowRight' ? 1 : -1) + enabled.length) % enabled.length];
    if (next) {
      onChoose(next);
      document.getElementById(`tab-${next}`)?.focus();
      e.preventDefault();
    }
  };
  return (
    <div className="tabs" role="tablist" aria-label="Plane" onKeyDown={onKey}>
      {PLANES.map((p, idx) => {
        const present = study.planes_available.includes(p);
        const count = study.series.filter((s) => s.plane === p).length;
        return (
          <button
            key={p}
            id={`tab-${p}`}
            type="button"
            role="tab"
            aria-selected={plane === p}
            disabled={!present}
            tabIndex={plane === p ? 0 : -1}
            title={
              present
                ? `${PLANE_LABEL[p]} (${idx + 1})`
                : `${PLANE_LABEL[p]} series not available for this study`
            }
            onClick={() => onChoose(p)}
          >
            {present ? PLANE_LABEL[p] : `${PLANE_LABEL[p]} — not available`}
            {count > 1 ? <span className="mono"> ({count})</span> : null}
          </button>
        );
      })}
    </div>
  );
}
