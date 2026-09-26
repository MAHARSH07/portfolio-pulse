import { useEffect } from "react";
import {
    AlertCircle,
    CheckCircle2,
    X,
} from "lucide-react";

function Notification({ notification, onClose }) {
    useEffect(() => {
        if (!notification) {
            return undefined;
        }

        const timeoutId = setTimeout(() => {
            onClose();
        }, 3000);

        return () => {
            clearTimeout(timeoutId);
        };
    }, [notification, onClose]);

    if (!notification) {
        return null;
    }

    const isSuccess = notification.type === "success";

    return (
        <div
            className={`notification ${
                isSuccess
                    ? "notification-success"
                    : "notification-error"
            }`}
            role="status"
        >
            <div className="notification-icon">
                {isSuccess ? (
                    <CheckCircle2
                        size={17}
                        strokeWidth={1.9}
                    />
                ) : (
                    <AlertCircle
                        size={17}
                        strokeWidth={1.9}
                    />
                )}
            </div>

            <span className="notification-message">
                {notification.message}
            </span>

            <button
                className="notification-close"
                onClick={onClose}
                aria-label="Close notification"
            >
                <X size={15} />
            </button>
        </div>
    );
}

export default Notification;