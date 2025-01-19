import axios from "axios";
import React, { useState } from "react";
import Spinner from "./Spinner";
import { FormResultDetail, FormResultDetailProps } from "./FormErrorDetail";

const FileUploadForm: React.FC = () => {
    const [resultMessage, setResultMessage] = useState<FormResultDetailProps>({ message: null, messageType: 'success' });
    const [file, setFile] = useState<File | null>(null);
    const [initialAmount, setInitialAmount] = useState<string | "">("");
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [showSpinner, setShowSpinner] = useState(false);

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
                setShowSpinner(true)
                try {
                    await axios.post(
                        `${import.meta.env.VITE_API_URL}/portfolio/load-data`, form
                    );
                    setResultMessage({ message: "Datos cargados correctamente", messageType: "success" })
                } catch (error) {
                    setResultMessage({ message: "Error al cargar data. Assegúrese de haber reiniciado la base de datos y que la hoja de datos sea válida", messageType: "error" })
                    console.error("Error fetching data:", error);
                }
                setShowSpinner(false)
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
                    `${import.meta.env.VITE_API_URL}/portfolio/reset`
                );
                setResultMessage({ message: "Base de datos reiniciada correctamente", messageType: "success" })
            } catch (error) {
                setResultMessage({ message: "Hubo un problema al reiniciar la base de datos", messageType: "error" })
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
        <div className="mb-8 bg-gradient-to-br from-[#0f1d36] to-[#3c4b5e] shadow-lg rounded-lg p-8 max-w-96 mx-auto">
            <h2 className="text-2xl font-bold text-center">Subir Archivo y Configurar Valor Inicial</h2>
            <form onSubmit={handleFormSubmit} className="space-y-6">
                <div>
                    <label htmlFor="file" className="block text-gray-300 font-medium mb-2">
                        Tablas de pesos y precios:
                    </label>
                    <input
                        type="file"
                        id="file"
                        required
                        onChange={handleFileChange}
                        className="block w-full p-1 text-gray-900 bg-gray-100 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                    />
                </div>

                <div>
                    <label htmlFor="initialAmount" className="block text-gray-300 font-medium mb-2">
                        Valor inicial de portfolios:
                    </label>
                    <input
                        type="number"
                        id="initialAmount"
                        required
                        value={initialAmount}
                        onChange={handleAmountChange}
                        className="block w-full p-1 text-gray-900 bg-gray-100 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                    />
                </div>

                <button
                    type="submit"
                    className="w-full py-3 bg-blue-600 font-semibold rounded-lg shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                    {!showSpinner && (<span>Subir</span>)}
                    {showSpinner && (<Spinner />)}
                </button>
            </form>

            <button
                onClick={openConfirmationModal}
                className="w-full py-3 mt-8 bg-red-600 font-semibold rounded-lg shadow-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
            >
                Reiniciar Base de Datos
            </button>

            {showConfirmation && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
                    <div className="bg-white rounded-lg shadow-lg p-6 space-y-4 w-96">
                        <h3 className="text-lg font-semibold text-gray-800">Confirmar Reinicio</h3>
                        <p className="text-gray-600">¿Estás seguro de que deseas reiniciar la base de datos? Esta acción no se puede deshacer.</p>
                        <div className="flex justify-end space-x-4">
                            <button
                                onClick={closeConfirmationModal}
                                className="py-2 px-4 bg-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-400 focus:outline-none"
                            >
                                Cancelar
                            </button>
                            <button
                                onClick={handleResetDb}
                                className="py-2 px-4 bg-red-600 font-medium rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
                            >
                                Confirmar
                            </button>
                        </div>
                    </div>
                </div>
            )}
            <FormResultDetail message={resultMessage.message} messageType={resultMessage.messageType} />
        </div>
    );
};

export default FileUploadForm;
