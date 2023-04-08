//TODO: Exchange mock request with real one
import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { Page_FlightSerializer_ } from '@schema/Page_FlightSerializer_'

export const ALl_FLIGHTS_KEY = "ALL_FLIGHTS"

export const getFlights = async (page: number, size: number) => {
    const data: Page_FlightSerializer_ = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/flight?page=${page}&size=${size}`)
        .then((res) => {
            return res.data
        })

    return data
}
export const fetchAllFlightsQuery = (page: number, size: number) =>
    useQuery<Page_FlightSerializer_>([ALl_FLIGHTS_KEY, page, size], () =>
        getFlights(page, size),

        {
            keepPreviousData: true
        })
