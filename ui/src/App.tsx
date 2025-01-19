import React, { useState } from "react";
import Charts from "./components/Charts";
import FileUpload from "./components/FileUpload";
import Transact from "./components/Transact";

const PortfolioDashboard: React.FC = () => {
    const [activeTab, setActiveTab] = useState("charts"); // "charts" or "forms"

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-900 to-blue-950 p-8 text-[#ddd9ca]">
            <h1 className="text-4xl font-bold mb-8 text-center">Portfolios</h1>
            <div className="flex justify-center space-x-4 mb-8">
                <button
                    className={`py-3 px-6 rounded-lg font-medium ${activeTab === "charts"
                        ? "bg-blue-600"
                        : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                        }`}
                    onClick={() => setActiveTab("charts")}
                >
                    Evolución de Portfolios
                </button>
                <button
                    className={`py-3 px-6 rounded-lg font-medium ${activeTab === "loadReset"
                        ? "bg-blue-600"
                        : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                        }`}
                    onClick={() => setActiveTab("loadReset")}
                >
                    Cargar / Resetear DB
                </button>
                <button
                    className={`py-3 px-6 rounded-lg font-medium ${activeTab === "transact"
                        ? "bg-blue-600"
                        : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                        }`}
                    onClick={() => setActiveTab("transact")}
                >
                    Compra / Venta
                </button>
            </div>
            <div className="p-2 max-w-7xl mx-auto">
                {activeTab === "charts" && (
                    <div className="space-y-2">
                        <Charts />
                    </div>
                )}
                {activeTab === "loadReset" && (
                    <div className="space-y-2">
                        <FileUpload />
                    </div>
                )}
                {activeTab === "transact" && (
                    <div className="space-y-2">
                        <Transact />
                    </div>
                )}
            </div>
        </div>);
};

export default PortfolioDashboard;
