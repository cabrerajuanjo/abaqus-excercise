import axios, { AxiosError } from "axios";
import React, { useEffect, useState } from "react";
import { DateRange } from "../types/ChartProps.type";
import { FormResultDetail, type FormResultDetailProps } from "./FormErrorDetail";

const Transaction: React.FC = () => {
    // const [errorMessage, setErrorMessage] = useState<FormResultDetailProps>({message: null, messageType: 'success'});
    const [resultMessage, setResultMessage] = useState<FormResultDetailProps>({ message: null, messageType: 'success' });
    const [formData, setFormData] = useState({
        date: "",
        portfolio: "",
        asset: "",
        operation: "",
        amount: "",
    });
    const [portfolios, setPortfolios] = useState<string[]>([])
    const [assets, setAssets] = useState<string[]>([])
    const [dateRange, setDateRange] = useState<DateRange>({ dateMin: "", dateMax: "" });

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
            const datesP = axios.get<string[]>(
                `${import.meta.env.VITE_API_URL}/portfolio/dates`
            );
            const [assets, portfolios, dates] = await Promise.all([assetsP, portfoliosP, datesP]);
            setAssets(assets.data);
            setPortfolios(portfolios.data);
            setDateRange({ dateMin: dates.data[0], dateMax: dates.data[dates.data.length - 1] })
            setFormData({ ...formData, date: dateRange.dateMin })
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
            await axios.post(`${import.meta.env.VITE_API_URL}/portfolio/transact`, formData, {
                headers: {
                    "Content-Type": "application/json",
                },
            });

            console.log("Transaction submitted successfully");
            setResultMessage({ message: "Transacción realizada correctamente", messageType: "success" })
        } catch (error) {
            if (error instanceof AxiosError && error.response) {
                if (error.response.data.extra.code === "INSUFFICIENT_ASSETS") {
                    setResultMessage({
                        message: `Insuficiente. Monto de ${formData.asset} en ${formData.portfolio} en ${formData.date} es ${error.response.data.extra.currentAssets}`,
                        messageType: "error"
                    });
                }
                if (error.response.data.extra.code === "ASSET_NOT_FOUND") {
                    setResultMessage({
                        message: `Activo ${formData.asset} en ${formData.portfolio} en ${formData.date} no fue encontrado en la base de datos`, messageType: "error"
                    });
                }
            }
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
                        min={dateRange.dateMin}
                        max={dateRange.dateMax}
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
            <FormResultDetail message={resultMessage.message} messageType={resultMessage.messageType} />
        </div>);
};

export default Transaction;
