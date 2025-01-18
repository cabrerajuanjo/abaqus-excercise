import axios from "axios";
import React, { useEffect, useState } from "react";

const Transaction: React.FC = () => {
    const [formData, setFormData] = useState({
        date: "",
        portfolio: "",
        asset: "",
        operation: "",
        amount: "",
    });
    const [portfolios, setPortfolios] = useState<string[]>([])
    const [assets, setAssets] = useState<string[]>([])

    useEffect(() => {
        fetchData();
    }, [])

    const fetchData = async () => {
        try {
            const assetsP = axios.get<string[]>(
                `${import.meta.env.VITE_API_URL}/portfolio/assets`
            );
            const portfoliosP = axios.get<string[]>(
                `${import.meta.env.VITE_API_URL}/portfolio/portfolios`
            );
            const [assets, portfolios] = await Promise.all([assetsP, portfoliosP]);
            setAssets(assets.data);
            setPortfolios(portfolios.data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/portfolio/transact`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                console.log("Transaction submitted successfully");
                setFormData({ date: "", portfolio: "", asset: "", operation: "", amount: "" });
            } else {
                console.error("Failed to submit transaction", response.statusText);
            }
        } catch (error) {
            console.error("Error submitting transaction:", error);
        }
    };

    return (
        <div className="mb-8 bg-gradient-to-br from-[#0f1d36] to-[#3c4b5e] shadow-lg rounded-lg p-8 max-w-96 mx-auto">
            <h2 className="text-2xl font-bold text-center">Registrar Transacción</h2>
            <form onSubmit={handleSubmit} className="space-y-1">
                <div>
                    <label htmlFor="date" className="block text-gray-300 font-medium mb-2">
                        Fecha:
                    </label>
                    <input
                        type="date"
                        id="date"
                        name="date"
                        value={formData.date}
                        onChange={handleInputChange}
                        className="block w-full p-1 text-gray-900 bg-gray-100 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        required
                    />
                </div>

                <div>
                    <label htmlFor="portfolio" className="block text-gray-300 font-medium mb-2">
                        Portafolio:
                    </label>
                    <select
                        id="portfolio"
                        name="portfolio"
                        value={formData.portfolio}
                        onChange={handleInputChange}
                        className="block w-full p-1 text-gray-900 bg-gray-100 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        required
                    >
                        <option selected disabled value="">
                            -- Seleccionar --
                        </option>
                        {portfolios.map((portfolio) => (
                            <option key={portfolio} value={portfolio}>
                                {portfolio}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label htmlFor="asset" className="block text-gray-300 font-medium mb-2">
                        Activo:
                    </label>
                    <select
                        id="asset"
                        name="asset"
                        value={formData.asset}
                        onChange={handleInputChange}
                        className="block w-full p-1 text-gray-900 bg-gray-100 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        required
                    >
                        <option disabled selected value="">
                            -- Seleccionar --
                        </option>
                        {assets.map((asset) => (
                            <option key={asset} value={asset}>
                                {asset}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label htmlFor="operation" className="block text-gray-300 font-medium mb-2">
                        Operación:
                    </label>
                    <select
                        id="operation"
                        name="operation"
                        value={formData.operation}
                        onChange={handleInputChange}
                        className="block w-full p-1 text-gray-900 bg-gray-100 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        required
                    >
                        <option disabled selected value="">
                            -- Seleccionar --
                        </option>
                        <option value="BUY">Comprar</option>
                        <option value="SELL">Vender</option>
                    </select>
                </div>

                <div>
                    <label htmlFor="amount" className="block text-gray-300 font-medium mb-2">
                        Monto:
                    </label>
                    <input
                        type="number"
                        id="amount"
                        name="amount"
                        value={formData.amount}
                        onChange={handleInputChange}
                        className="block w-full p-1 text-gray-900 bg-gray-100 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        required
                    />
                </div>

                <button
                    type="submit"
                    className="w-full py-3 bg-blue-600 mt-16 font-semibold rounded-lg shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                    Enviar Transacción
                </button>
            </form>
        </div>);
};

export default Transaction;
