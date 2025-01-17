import React, { useState } from "react";

const Transaction: React.FC = () => {
    const [formData, setFormData] = useState({
        date: "",
        portfolio: "",
        asset: "",
        operation: "BUY",
        amount: "",
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch("http://localhost:8000/portfolio/transact", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                console.log("Transaction submitted successfully");
                setFormData({ date: "", portfolio: "", asset: "", operation: "BUY", amount: "" });
            } else {
                console.error("Failed to submit transaction", response.statusText);
            }
        } catch (error) {
            console.error("Error submitting transaction:", error);
        }
    };

    return (
        <div className="bg-white shadow-md rounded-lg p-6 space-y-4 w-1/2">
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label htmlFor="date" className="block text-gray-700 font-medium mb-2">
                        Fecha:
                    </label>
                    <input
                        type="date"
                        id="date"
                        name="date"
                        value={formData.date}
                        onChange={handleInputChange}
                        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <div>
                    <label htmlFor="portfolio" className="block text-gray-700 font-medium mb-2">
                        Portafolio:
                    </label>
                    <input
                        type="text"
                        id="portfolio"
                        name="portfolio"
                        value={formData.portfolio}
                        onChange={handleInputChange}
                        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <div>
                    <label htmlFor="asset" className="block text-gray-700 font-medium mb-2">
                        Activo:
                    </label>
                    <input
                        type="text"
                        id="asset"
                        name="asset"
                        value={formData.asset}
                        onChange={handleInputChange}
                        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <div>
                    <label htmlFor="operation" className="block text-gray-700 font-medium mb-2">
                        Operación:
                    </label>
                    <select
                        id="operation"
                        name="operation"
                        value={formData.operation}
                        onChange={handleInputChange}
                        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    >
                        <option value="BUY">Comprar</option>
                        <option value="SELL">Vender</option>
                    </select>
                </div>

                <div>
                    <label htmlFor="amount" className="block text-gray-700 font-medium mb-2">
                        Monto:
                    </label>
                    <input
                        type="number"
                        id="amount"
                        name="amount"
                        value={formData.amount}
                        onChange={handleInputChange}
                        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <button
                    type="submit"
                    className="py-2 px-4 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600"
                >
                    Enviar Transacción
                </button>
            </form>
        </div>
    );
};

export default Transaction;
