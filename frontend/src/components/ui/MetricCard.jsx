function MetricCard({
  label,
  value,
  meta,
  icon: Icon,
  status = "neutral",
  secondary,
}) {
  return (
    <article className={`metric-card metric-card-${status}`}>
      <div className="metric-card-top">
        <div className="metric-card-label">
          {label}
        </div>

        {Icon && (
          <div className="metric-card-icon">
            <Icon size={17} strokeWidth={1.8} />
          </div>
        )}
      </div>

      <div className="metric-card-value">
        {value}
      </div>

      <div className="metric-card-bottom">
        <span className="metric-card-meta">
          {meta}
        </span>

        {secondary && (
          <span className="metric-card-secondary">
            {secondary}
          </span>
        )}
      </div>
    </article>
  );
}

export default MetricCard;