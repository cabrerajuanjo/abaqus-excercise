export type DateRange = {
    dateGt: string,
    dateLt: string,
}

export type ChartProps = {
    dateRange: DateRange;
    fetchTrigger: boolean;
};
