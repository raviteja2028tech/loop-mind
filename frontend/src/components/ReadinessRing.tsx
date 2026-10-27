/** Circular readiness indicator — spec.md Student Dashboard §9 and Skill
 * Gap Analysis §11 both use the same visual. Only --accent/--border are
 * used, per the theme's no-rainbow chart rule. */
export function ReadinessRing({ percentage }: { percentage: number }) {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - Math.max(0, Math.min(100, percentage)) / 100);
  return (
    <svg width={104} height={104} viewBox="0 0 104 104" className="shrink-0">
      <circle cx={52} cy={52} r={radius} fill="none" stroke="var(--border)" strokeWidth={10} />
      <circle
        cx={52}
        cy={52}
        r={radius}
        fill="none"
        stroke="var(--accent)"
        strokeWidth={10}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform="rotate(-90 52 52)"
        style={{ transition: "stroke-dashoffset 300ms ease" }}
      />
      <text x={52} y={58} textAnchor="middle" fontSize={22} fontWeight={600} fill="var(--text)">
        {percentage}%
      </text>
    </svg>
  );
}
