import React, { useState } from "react";
import TotalsChart from "./TotalsChart";
import WeightsChart from "./WeightsChart";
import { DateRange } from "../types/ChartProps.type";

const PortfolioDashboard: React.FC = () => {
    const [dateRange, setDateRange] = useState<DateRange>({ dateGt: "", dateLt: "" });
    const [fetchTrigger, setFetchTrigger] = useState(false);

    const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setDateRange((prev) => ({ ...prev, [name]: value }));
    };

    const handleFetchData = () => {
        setFetchTrigger((prev) => !prev); // Toggle to trigger data fetching
    };

    return (
        <div className="p-6 bg-gray-100 min-h-screen">
            <h1 className="text-3xl font-bold mb-6 text-center">Portfolio Dashboard</h1>
            <div className="mb-8 bg-white shadow-md rounded-lg p-6">
                <form
                    className="flex flex-col space-y-4"
                    onSubmit={(e) => {
                        e.preventDefault();
                        handleFetchData();
                    }}
                >
                    <label className="flex flex-col">
                        <span className="font-medium text-gray-700">Start Date:</span>
                        <input
                            className="mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
                            type="date"
                            name="dateGt"
                            value={dateRange.dateGt}
                            onChange={handleDateChange}
                        />
                    </label>
                    <label className="flex flex-col">
                        <span className="font-medium text-gray-700">End Date:</span>
                        <input
                            className="mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
                            type="date"
                            name="dateLt"
                            value={dateRange.dateLt}
                            onChange={handleDateChange}
                        />
                    </label>
                    <button
                        className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-400 focus:outline-none"
                        type="submit"
                    >
                        Fetch Data
                    </button>
                </form>
            </div>

            <div className="row-auto">
                <div className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">Totals Chart</h2>
                    <div className="bg-white shadow-md rounded-lg p-6">
                        <TotalsChart dateRange={dateRange} fetchTrigger={fetchTrigger} />
                    </div>
                </div>
                <div>
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">Weights Chart</h2>
                    <div className="bg-white shadow-md rounded-lg p-6">
                        <WeightsChart dateRange={dateRange} fetchTrigger={fetchTrigger} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PortfolioDashboard;
