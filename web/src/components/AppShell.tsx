import { NavLink, Outlet, useMatch } from 'react-router-dom';
import { api } from '../api/client';
import type { Health } from '../api/types';
import { useAsync } from '../hooks/useAsync';
import { HatchBlock, StateGlyph } from './StateGlyph';

function RunModeChip() {
  const health = useAsync<Health>('health', (signal) => api.health({ signal }));
  if (health.phase === 'error') {
    return (
      <span className="mode-chip failed" title={`${health.error.code}: ${health.error.message}`}>
        <StateGlyph status="failed" />
        API unreachable
      </span>
    );
  }
  if (health.phase !== 'ready') {
    return (
      <span className="mode-chip" aria-busy="true">
        Checking API…
      </span>
    );
  }
  const h = health.data;
  if (h.mode === 'fixture') {
    return (
      <span
        className="mode-chip"
        title="No model is loaded. Results come from development fixtures."
      >
        <HatchBlock />
        Fixture mode
      </span>
    );
  }
  return (
    <span className="mode-chip" title="A model checkpoint is loaded.">
      Model: <span className="mono">{h.model_version ?? 'unknown'}</span>
    </span>
  );
}

export function AppShell() {
  const onStudy = useMatch('/studies/:studyId');
  return (
    <div className="app">
      <header className="topbar">
        <div className="wordmark">
          <b>KneeScope</b>
          <small>Knee MRI research review</small>
        </div>
        <nav className="nav" aria-label="Primary">
          <NavLink to="/" end>
            Studies
          </NavLink>
          {onStudy ? (
            <NavLink to={onStudy.pathname}>Review</NavLink>
          ) : (
            <span aria-disabled="true" title="Open a study from Studies to review it">
              Review
            </span>
          )}
          <NavLink to="/evaluation">Evaluation</NavLink>
        </nav>
        <span className="spacer" />
        <RunModeChip />
      </header>
      <main id="main">
        <Outlet />
      </main>
      <footer className="footer">
        <b>Research prototype — not for diagnosis.</b>
        <span>Scores are uncalibrated model outputs unless stated.</span>
      </footer>
    </div>
  );
}
