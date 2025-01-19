export type DateRange = {
    dateMin: string,
    dateMax: string,
}

export type ChartProps = {
    dateRange: DateRange;
    fetchTrigger: boolean;
};
