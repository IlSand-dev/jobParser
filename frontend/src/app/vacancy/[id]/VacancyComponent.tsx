"use client"
import { useState } from "react";
import { useEffect } from "react";
import {Vacancy} from "../../models/Vacancy"
import React from "react";


const host = "http://0.0.0.0:8000/"

export default function VacancyComponent(params: {id: number}){


    const [error, setError] = useState(null)
    const [isLoaded, setIsLoaded] = useState(false)
    const [vacancy, setVacancies] = useState<Vacancy | null>(null)

    useEffect(() => {
        fetch(host+"vacancy/"+params.id,{
            headers: {
                'User-Agent': 'My User Agent 1.0'
            }
        })
        .then(res => res.json() as Promise<Vacancy>)
        .then(
        (result) => {
            setIsLoaded(true)
            setVacancies(result)
        },  
        (error) => {
            setIsLoaded(true)
            setError(error)
        }
    )
    }, [])
    if (error){
        return <div>Ошибка: {error['message']}</div>
    } else if(!isLoaded){
        return <div>Загрузка...</div>
    } else{
        let salary = ""
        if (vacancy?.salary == null){
            salary = "Не указана"
        } else {
            if (vacancy.salary.minimal == null)
                salary = "До " + vacancy.salary.maximum.toLocaleString("ru")
            else if (vacancy.salary.maximum == null)
                salary = "От " + vacancy.salary.minimal.toLocaleString("ru")
            else
                salary = vacancy.salary.minimal.toLocaleString("ru") + "-" + vacancy.salary.maximum.toLocaleString("ru")
            salary += vacancy.salary.currency 
        }
        
        let experience = ""
        if (vacancy?.experience == null){
            experience = "Не требуется"
        } else {
            if (vacancy.experience.minimal == null)
                experience = "Меньше " + vacancy.experience.maximum + (vacancy.experience.maximum>1?" лет":" года")
            else if (vacancy.experience.maximum == null)
                experience = "Больше " + vacancy.experience.minimal + (vacancy.experience.minimal>1?" лет":" года")
            else
                experience = "От " + vacancy.experience.minimal + (vacancy.experience.minimal==1?" года":"") + " до " + vacancy.experience.maximum + " лет"
        }

        const employment = vacancy?.employment != null?vacancy?.employment:""
        const schedule = vacancy?.schedule != null?vacancy?.schedule:""

        const address = vacancy?.company.address != null?", " + vacancy?.company.address:""

        return (
            <div>
                <h1 className="bold">{vacancy!.name}</h1>
                <p>Зарплата: {salary}</p>
                <p>Требуемый опыт работы: {experience}</p>
                <p>{employment}, {schedule}</p>
                <p>Работодатель: {vacancy?.company.name}</p>
                <p>Адрес: {vacancy?.company.city}{address}</p>
                <p>Ссылка на вакансию: <a href={vacancy?.href}>{vacancy?.href}</a></p>
                <br></br>
                <strong>Описание: </strong>
                <div dangerouslySetInnerHTML={{__html: vacancy!.description}}></div>
            </div>
        )
    }
    

}