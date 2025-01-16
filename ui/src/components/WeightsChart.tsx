import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import Chart, {ChartDataset} from "chart.js/auto";
import { ChartProps } from "../types/ChartProps.type";

type PortfolioData = {
    date: string;
    asset: string;
    portfolio: string;
    weight: number;
};

type AssetColor = Record<string, string>

const WeightsChart: React.FC<ChartProps> = ({dateRange, fetchTrigger}) => {
    const chartRefs = useRef<Record<string, Chart>>({});
    const [data, setData] = useState<PortfolioData[]>([]);


    useEffect(() => {
        if (!dateRange.dateGt || !dateRange.dateLt) return;

        const fetchData = async () => {
            try {
                const response = await axios.get<PortfolioData[]>(
                    `http://localhost:8000/portfolio/weights?date__gt=${dateRange.dateGt}&date__lt=${dateRange.dateLt}`
                );
                setData(response.data);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
    }, [dateRange, fetchTrigger])

    useEffect(() => {
        if (data.length === 0) return;

        // Clear any existing charts
        Object.values(chartRefs.current).forEach((chart) => chart.destroy());

        // Group data by portfolio
        const portfolios = data.reduce<Record<string, PortfolioData[]>>((acc, item) => {
            if (!acc[item.portfolio]) acc[item.portfolio] = [];
            acc[item.portfolio].push(item);
            return acc;
        }, {});

        const assetColor: AssetColor = {}
        // Generate charts for each portfolio
        Object.entries(portfolios).forEach(([portfolio, portfolioData]) => {
            const ctx = document.getElementById(`weights-${portfolio}`) as HTMLCanvasElement;
            if (!ctx) return;

            const labels = new Set<string>()
            portfolioData.forEach((item) => {
                labels.add(item.date)
            });

            const datasets: Record<string, ChartDataset> = {};

            portfolioData.forEach((item) => {
                if (!datasets[item.asset]) {
                    assetColor[item.asset] = assetColor[item.asset]?? getRandomColor();

                    datasets[item.asset] = {
                        label: item.asset,
                        data: [],
                        fill: true,
                        backgroundColor: assetColor[item.asset],
                        pointRadius: 1
                    };
                }
                datasets[item.asset].data.push(item.weight);
            });

            chartRefs.current[portfolio] = new Chart(ctx, {
                type: "line",
                data: {
                    labels: [...labels],
                    datasets: Object.values(datasets),
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "top",
                        },
                        title: {
                            display: true,
                            text: `${portfolio}`,
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Date",
                            },
                        },
                        y: {
                            stacked: true,
                            title: {
                                display: true,
                                text: "Weight",
                            },
                        },
                    },
                },
            });
        });

        return () => {
            // Destroy charts on cleanup
            Object.values(chartRefs.current).forEach((chart) => chart.destroy());
        };
    }, [data]);

    // Utility function to generate random colors
    const getRandomColor = (): string => {
        const letters = "0123456789ABCDEF";
        let color = "#";
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    };

    // Group data by portfolio to generate canvas elements
    const portfolios = [...new Set(data.map((item) => item.portfolio))];

    return (
        <div>
            {portfolios.map((portfolio) => (
                <div key={portfolio}>
                    <canvas className="w-full" id={`weights-${portfolio}`} />
                </div>
            ))}
        </div>
    );
};

export default WeightsChart;
