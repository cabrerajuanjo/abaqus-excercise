import React from "react";

interface FormResultDetailProps {
    message: string | null;
    messageType: "error" | "success"; // New prop to determine message type
}

const FormResultDetail: React.FC<FormResultDetailProps> = ({ message, messageType }) => {
    if (!message) return null;

    const messageClasses =
        messageType === "error" ? "text-red-600" : "text-green-600";

    return (
        <div className={`${messageClasses} text-sm mt-4 text-center`}>
            *{message}
        </div>
    );
};

export { FormResultDetail, type FormResultDetailProps };

