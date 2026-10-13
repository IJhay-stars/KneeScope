import type { ModelCard } from '../api/types';

export function ModelCardView({ card }: { card: ModelCard }) {
  return (
    <div>
      {card.status === 'draft' ? (
        <p>
          <span className="stamp">Draft</span>
        </p>
      ) : null}
      {card.sections.map((s) => (
        <section key={s.section_id}>
          <h3>{s.title}</h3>
          {s.body.split(/\n{2,}/).map((para, i) => (
            <p key={i}>{para}</p>
          ))}
        </section>
      ))}
      <h3>Limitations</h3>
      <ol className="footnotes">
        {card.limitations.map((l, i) => (
          <li key={i}>{l}</li>
        ))}
      </ol>
    </div>
  );
}
