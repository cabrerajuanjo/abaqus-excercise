import axios, { AxiosPromise } from "axios";
import { DateRange } from "../types/ChartProps.type";

type DateBasedPaginatedData<T> = {
    page: number,
    datesInPage: number,
    recordsInPage: number,
    totalPages: number,
    results: T[]
}

export async function dateBasedPaginatedFetch<T>(dateRange: DateRange, takeDate: number, path: string): Promise<T[]> {
    const firstPage = await axios.get<DateBasedPaginatedData<T>>(
        `${import.meta.env.VITE_API_URL}/${path}?date__gt=${dateRange.dateMin}&date__lt=${dateRange.dateMax}&page=1&takeDates=${takeDate}`
    );
    const totalPages = firstPage.data.totalPages;
    const firstPageData = firstPage.data.results
    const remainingPagesP: AxiosPromise<DateBasedPaginatedData<T>>[] = []
    for (let i = 2; i <= totalPages; i++) {
        remainingPagesP.push(axios.get<DateBasedPaginatedData<T>>(
            `${import.meta.env.VITE_API_URL}/${path}?date__gt=${dateRange.dateMin}&date__lt=${dateRange.dateMax}&page=${i}&takeDates=${takeDate}`
        ));
    }
    const remainingPagesData = (await Promise.all(remainingPagesP)).map((item) => {
        return item.data.results
    }).reduce((acc, curr) => {
        return [...acc, ...curr]
    }, [])

    return [...firstPageData, ...remainingPagesData];
}
