import React from 'react';
import Charts from './components/Charts';
// import FileUploadForm from './FileUploadForm';
// import TransactionForm from './TransactionForm';

const PortfolioDashboard = () => {
    return (
        <div className="min-h-screen bg-gray-100 p-8 space-y-8">
            <h1 className="text-3xl font-bold">Portfolio Dashboard</h1>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <Charts />
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* <FileUploadForm /> */}
                {/*<TransactionForm />*/}
            </div>
        </div>
    );
};

export default PortfolioDashboard;
