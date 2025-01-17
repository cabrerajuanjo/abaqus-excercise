import axios from "axios";
import React, { useState } from "react";

const FileUploadForm: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [initialAmount, setInitialAmount] = useState<string | "">("");
    const [showConfirmation, setShowConfirmation] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);
        }
    };

    const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setInitialAmount(value === "" ? "" : value);
    };

    const handleFormSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (file && initialAmount !== "") {
            const form = new FormData()
            form.append("file", file)
            form.append("initial_total", initialAmount)
            const uploadData = async () => {
                try {
                    await axios.post(
                        `http://localhost:8000/portfolio/load-data`, form
                    );
                } catch (error) {
                    console.error("Error fetching data:", error);
                }
            }
            uploadData();
        } else {
            console.error("Please provide both a file and an initial amount.");
        }
    };

    const handleResetDb = () => {
        console.log("Database reset initiated.");
        const resetDb = async () => {
            try {
                await axios.post(
                    `http://localhost:8000/portfolio/reset`
                );
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        }
        resetDb();
        setShowConfirmation(false);
    };

    const openConfirmationModal = () => {
        setShowConfirmation(true);
    };

    const closeConfirmationModal = () => {
        setShowConfirmation(false);
    };

    return (
        <div className="bg-white shadow-md rounded-lg p-6 space-y-4 w-1/2">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload File and Set Initial Amount</h2>
            <form onSubmit={handleFormSubmit} className="space-y-4">
                <div>
                    <label htmlFor="file" className="block text-gray-700 font-medium mb-2">
                        Tablas de pesos y precios:
                    </label>
                    <input
                        type="file"
                        id="file"
                        onChange={handleFileChange}
                        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>
                <div>
                    <label htmlFor="initialAmount" className="block text-gray-700 font-medium mb-2">
                        Valor inicial de portfolios:
                    </label>
                    <input
                        
                        type="number"
                        id="initialAmount"
                        value={initialAmount}
                        onChange={handleAmountChange}
                        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>
                <button
                    type="submit"
                    className="py-2 px-4 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600"
                >
                    Submit
                </button>
            </form>
            <button
                onClick={openConfirmationModal}
                className="py-2 px-4 bg-red-500 text-white font-medium rounded-lg hover:bg-red-600"
            >
                Reset Database
            </button>

            {showConfirmation && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
                    <div className="bg-white rounded-lg shadow-lg p-6 space-y-4">
                        <h3 className="text-lg font-semibold text-gray-800">Confirm Reset</h3>
                        <p className="text-gray-600">Are you sure you want to reset the database? This action cannot be undone.</p>
                        <div className="flex justify-end space-x-4">
                            <button
                                onClick={closeConfirmationModal}
                                className="py-2 px-4 bg-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-400"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleResetDb}
                                className="py-2 px-4 bg-red-500 text-white font-medium rounded-lg hover:bg-red-600"
                            >
                                Confirm
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default FileUploadForm;
