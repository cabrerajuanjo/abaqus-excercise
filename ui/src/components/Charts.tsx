import React, { useEffect, useState } from "react";
import TotalsChart from "./TotalsChart";
import WeightsChart from "./WeightsChart";
import { DateRange } from "../types/ChartProps.type";
import axios from "axios";

const PortfolioDashboard: React.FC = () => {
    const [dateRange, setDateRange] = useState<DateRange>({ dateMin: "", dateMax: "" });
    const [fetchTrigger, setFetchTrigger] = useState(false);
    const [activeTab, setActiveTab] = useState("totals"); // "totals" or "weights"

    useEffect(() => {
        fetchData();
    }, [])

    const fetchData = async () => {
        try {
            const response = await axios.get<string[]>(
                `${import.meta.env.VITE_API_URL ?? ""}/portfolio/dates`
            );
            setDateRange({ dateMin: response.data[0], dateMax: response.data[response.data.length - 1] })
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setDateRange((prev) => ({ ...prev, [name]: value }));
    };

    const handleFetchData = () => {
        setFetchTrigger((prev) => !prev); // Toggle to trigger data fetching
    };

    return (
        <div className="p-6 from-blue-900 to-gray-900 min-h-screen w-full">
            <div className="mb-8 bg-gradient-to-br from-[#0f1d36] to-[#3c4b5e] shadow-lg rounded-lg p-8 max-w-96 mx-auto">
                <form
                    className="space-y-6"
                    onSubmit={(e) => {
                        e.preventDefault();
                        handleFetchData();
                    }}
                >
                    <div>
                        <label className="block text-gray-300 font-medium mb-2" htmlFor="dateMin">
                            Fecha de Inicio:
                        </label>
                        <input
                            id="dateMin"
                            name="dateMin"
                            type="date"
                            value={dateRange.dateMin}
                            onChange={handleDateChange}
                            className="block w-full p-1 text-gray-900 bg-gray-100 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        />
                    </div>
                    <div>
                        <label className="block text-gray-300 font-medium mb-2" htmlFor="dateMax">
                            Fecha de Fin:
                        </label>
                        <input
                            id="dateMax"
                            name="dateMax"
                            type="date"
                            value={dateRange.dateMax}
                            onChange={handleDateChange}
                            className="block w-full p-1 text-gray-900 bg-gray-100 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        />
                    </div>
                </form>
            </div>
            <div className="min-w-full mx-auto">
                <div className="flex space-x-4 mb-6">
                    <button
                        className={`w-1/2 py-3 rounded-lg font-medium text-sm ${activeTab === "totals"
                            ? "bg-blue-600"
                            : "bg-gray-200 text-gray-700"
                            }`}
                        onClick={() => setActiveTab("totals")}
                    >
                        Gráfica Totales
                    </button>
                    <button
                        className={`w-1/2 py-3 rounded-lg font-medium text-sm ${activeTab === "weights"
                            ? "bg-blue-600"
                            : "bg-gray-200 text-gray-700"
                            }`}
                        onClick={() => setActiveTab("weights")}
                    >
                        Gráfica Pesos
                    </button>
                </div>
                {activeTab === "totals" && (
                    <div className="bg-gradient-to-br from-gray-700 to-gray-900 shadow-lg rounded-lg p-6">
                        <TotalsChart dateRange={dateRange} fetchTrigger={fetchTrigger} />
                    </div>
                )}
                {activeTab === "weights" && (
                    <div className="bg-gradient-to-br from-gray-700 to-gray-900 shadow-lg rounded-lg p-6">
                        <WeightsChart dateRange={dateRange} fetchTrigger={fetchTrigger} />
                    </div>
                )}
            </div>
        </div>
    );
};

export default PortfolioDashboard;
