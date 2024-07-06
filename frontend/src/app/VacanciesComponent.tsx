
"use client"
import React, {useEffect, useState} from "react";
import Link from "next/link";
import Pagination from "@mui/material/Pagination"
import Button from "@mui/material/Button"
import SendIcon from "@mui/icons-material/Send"

import {Vacancy} from "./models/Vacancy"



const host = "http://0.0.0.0:8000/"
export function VacanciesComponent(params: {
        salary: number,
        experience: string,
        employment: string[],
        schedule: string[],
    }
){
    const [error, setError] = useState(null)
    const [isLoaded, setIsLoaded] = useState(false)
    const defaultValue: Array<Vacancy> = []
    const [vacancies, setVacancies] = useState(defaultValue)
    const [pages, setPages] = useState(0)
    const [currentPage, setPage] = useState(1)
    const [searchText, setSearchText] = useState("")
    const [isSent, setIsSent] = useState(false)

    const handlePage = (event: React.ChangeEvent<unknown>, value: number) => {
        setIsLoaded(false);
        setPage(value);
      };

    const onSendClick = () => {
        setIsSent(true)
        setIsLoaded(false)
    }
    

    useEffect(() => {
        const text_query = searchText!=""?("text=" + searchText):""
        const salary_query = params.salary>0?("only_with_salary=true&salary="+params.salary):""
        const experience_query = params.experience!=""?("experience="+params.experience):""
        const employment_query = params.employment.length>0?("employment="+params.employment.join(",")):""
        const schedule_query = params.schedule.length>0?("schedule="+params.schedule.join(",")):""
        fetch(host+"vacancySearch/?page="+(currentPage-1)+"&"+[text_query, salary_query, experience_query, employment_query, schedule_query].filter(query => query!="").join("&"),{
            headers: {
                'User-Agent': 'My User Agent 1.0'
            }
        })
        .then(res => res.json() as Promise<Array<Vacancy>>)
        .then(
        (result: any) => {
            setIsSent(false)
            setIsLoaded(true)
            setVacancies(result['items'])
            setPages(result['pages'])
        },  
        (error) => {
            setIsSent(false)
            setIsLoaded(true)
            setError(error)
        }
    )
    }, [currentPage, isSent])

    if (error){
        return <div>Ошибка: {error['message']}</div>
    } else if(!isLoaded){
        return <div>Загрузка...</div>
    } else{
        return (
            <>
            <label><input onChange={e => setSearchText(e.target.value)} name="search" defaultValue={searchText}></input>  <Button onClick={onSendClick}>{<SendIcon color="action"/>}</Button></label>
            <ul>
                {vacancies.map((vacancy, i) => (
                    <li key={vacancy.id}>
                        <Link href={"vacancy/"+vacancy.id+"/"}>{vacancy.name} </Link>
                    </li>
                ))}
            </ul>
            <Pagination page={currentPage} count={pages} onChange={handlePage}></Pagination>
            </>
        )
    }
}