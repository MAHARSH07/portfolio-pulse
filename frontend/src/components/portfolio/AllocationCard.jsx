import { PieChart } from "lucide-react";

const allocationColors = [
  "#8b7cff",
  "#5b9cff",
  "#3ddc97",
  "#f5bd62",
  "#ff6b7a",
  "#8b95a7",
];

function AllocationCard({ holdings }) {
  const totalInvested = holdings.reduce(
    (total, holding) =>
      total +
      Number(holding.quantity) * Number(holding.average_price),
    0
  );

  const allocations = holdings
    .map((holding, index) => {
      const investedValue =
        Number(holding.quantity) *
        Number(holding.average_price);

      const percentage =
        totalInvested > 0
          ? (investedValue / totalInvested) * 100
          : 0;

      return {
        symbol: holding.symbol,
        investedValue,
        percentage,
        color:
          allocationColors[
            index % allocationColors.length
          ],
      };
    })
    .sort((a, b) => b.percentage - a.percentage);

  const visibleAllocations = allocations.slice(0, 5);

  const otherPercentage = allocations
    .slice(5)
    .reduce((total, item) => total + item.percentage, 0);

  const chartItems = [
    ...visibleAllocations,
    ...(otherPercentage > 0
      ? [
          {
            symbol: "Other",
            percentage: otherPercentage,
            color: "#596273",
          },
        ]
      : []),
  ];

  let currentAngle = 0;

  const gradientSegments = chartItems
    .map((item) => {
      const start = currentAngle;
      const end = currentAngle + item.percentage * 3.6;

      currentAngle = end;

      return `${item.color} ${start}deg ${end}deg`;
    })
    .join(", ");

  return (
    <article className="allocation-card">
      <div className="allocation-header">
        <div>
          <p className="card-eyebrow">
            PORTFOLIO ALLOCATION
          </p>

          <h2>Where your capital is invested</h2>

          <p className="card-description">
            Based on your invested value.
          </p>
        </div>

        <div className="allocation-icon">
          <PieChart size={18} strokeWidth={1.8} />
        </div>
      </div>

      <div className="allocation-content">
        <div
          className="allocation-donut"
          style={{
            background: `conic-gradient(${gradientSegments})`,
          }}
        >
          <div className="allocation-donut-center">
            <span>{holdings.length}</span>
            <small>holdings</small>
          </div>
        </div>

        <div className="allocation-list">
          {chartItems.map((item) => (
            <div
              className="allocation-item"
              key={item.symbol}
            >
              <div className="allocation-name">
                <span
                  className="allocation-dot"
                  style={{
                    backgroundColor: item.color,
                  }}
                />

                <span>{item.symbol}</span>
              </div>

              <strong>
                {item.percentage.toFixed(1)}%
              </strong>
            </div>
          ))}
        </div>
      </div>
    </article>
  );
}

export default AllocationCard;