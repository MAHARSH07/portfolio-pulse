import {
    Bell,
    Bot,
    BriefcaseBusiness,
    Globe2,
    Newspaper,
    Settings,
} from "lucide-react";

const iconMap = {
    Portfolio: BriefcaseBusiness,
    Market: Globe2,
    News: Newspaper,
    Alerts: Bell,
    "AI Assistant": Bot,
    Settings,
};

function PlaceholderPage({ title, description }) {
    const Icon = iconMap[title] || Settings;

    return (
        <section className="placeholder-page">
            <div className="placeholder-icon">
                <Icon size={24} strokeWidth={1.7} />
            </div>

            <p className="eyebrow">PORTFOLIOPULSE</p>

            <h1>{title}</h1>

            <p className="placeholder-description">
                {description}
            </p>

            <span className="placeholder-badge">
                Coming soon
            </span>
        </section>
    );
}

export default PlaceholderPage;