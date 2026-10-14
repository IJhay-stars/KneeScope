import { useEffect, useRef, useState } from 'react';
import { sliceUrl } from '../api/client';
import type { Plane, SeriesSummary } from '../api/types';

type Loaded = { url: string; status: 'ready' | 'error' };

/**
 * Draws the server-rendered PNG for one slice into a neutral well. `sliceIndex` is 0-based;
 * corner annotations show it 1-based. No crosshairs, no overlays, no motion between slices.
 */
export function SliceViewer({
  studyId,
  series,
  plane,
  sliceIndex,
  fixtureStripe,
}: {
  studyId: string;
  series: SeriesSummary;
  plane: Plane;
  sliceIndex: number;
  fixtureStripe: boolean;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const url = sliceUrl(studyId, series.series_id, sliceIndex);
  const [loaded, setLoaded] = useState<Loaded | null>(null);
  const [attempt, setAttempt] = useState(0);
  const { rendered_width: width, rendered_height: height } = series;

  useEffect(() => {
    let cancelled = false;
    const img = new Image();
    img.onload = () => {
      if (cancelled) return;
      const ctx = canvasRef.current?.getContext('2d');
      if (ctx) {
        ctx.imageSmoothingEnabled = true;
        ctx.clearRect(0, 0, width, height);
        ctx.drawImage(img, 0, 0, width, height);
      }
      setLoaded({ url, status: 'ready' });
    };
    img.onerror = () => {
      if (!cancelled) setLoaded({ url, status: 'error' });
    };
    img.src = attempt === 0 ? url : `${url}${url.includes('?') ? '&' : '?'}retry=${attempt}`;
    return () => {
      cancelled = true;
    };
  }, [url, width, height, attempt]);

  const state = loaded?.url === url ? loaded.status : 'loading';
  const total = series.num_slices;
  const label = `${series.description ?? series.series_id}, ${plane} plane, slice ${sliceIndex + 1} of ${total}, study ${studyId}`;

  return (
    <div className={`viewer${fixtureStripe ? ' fixture' : ''}`} aria-busy={state === 'loading'}>
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        role="img"
        aria-label={label}
        // Keep the previous slice visible while the next loads: no flicker, no transition.
        style={{ visibility: loaded === null || state === 'error' ? 'hidden' : 'visible' }}
      />
      <div className="corner tl">
        {studyId}
        <br />
        {series.description ?? series.series_id}
      </div>
      <div className="corner tr">Rendered slice (PNG)</div>
      <div className="corner bl">
        {sliceIndex + 1} / {total}
        <br />
        {plane}
      </div>
      <div className="corner br">Fit</div>
      {state === 'loading' && loaded === null ? (
        <div className="viewer-msg">Loading slice…</div>
      ) : null}
      {state === 'error' ? (
        <div className="viewer-msg">
          <div>
            <p>Slice image could not be loaded.</p>
            <button type="button" className="btn" onClick={() => setAttempt((n) => n + 1)}>
              Retry
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
