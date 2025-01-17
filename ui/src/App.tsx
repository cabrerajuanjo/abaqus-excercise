import React, { useState } from "react";
import Charts from "./components/Charts";
import FileUpload from "./components/FileUpload";
import Transact from "./components/Transact";

const PortfolioDashboard: React.FC = () => {
    const [activeTab, setActiveTab] = useState("charts"); // "charts" or "forms"

    return (
        <div className="min-h-screen bg-gray-100 p-8 space-y-8">
            <h1 className="text-3xl font-bold">Portfolios</h1>
            <div className="flex space-x-4 mb-6">
                <button
                    className={`py-2 px-4 rounded-lg font-medium ${activeTab === "charts" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-700"
                        }`}
                    onClick={() => setActiveTab("charts")}
                >
                    Evolución de portfolios
                </button>
                <button
                    className={`py-2 px-4 rounded-lg font-medium ${activeTab === "loadReset" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-700"
                        }`}
                    onClick={() => setActiveTab("loadReset")}
                >
                    Cargar / Resetear DB
                </button>
                <button
                    className={`py-2 px-4 rounded-lg font-medium ${activeTab === "transact" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-700"
                        }`}
                    onClick={() => setActiveTab("transact")}
                >
                    Compra / Venta
                </button>
            </div>

            {activeTab === "charts" && (
                <div className="gap-8">
                    <Charts />
                </div>
            )}

            {activeTab === "loadReset" && (
                <div className="gap-8">
                    <FileUpload />
                </div>
            )}

            {activeTab === "transact" && (
                <div className="gap-8">
                    <Transact />
                </div>
            )}
        </div>
    );
};

export default PortfolioDashboard;
