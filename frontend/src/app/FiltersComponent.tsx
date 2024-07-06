
"use client"
import React, {useEffect, useState} from "react";



const host = "http://0.0.0.0:8000/"
export function FiltersComponent(params: {
    setSalary: React.Dispatch<React.SetStateAction<number>>,
    setExperience: React.Dispatch<React.SetStateAction<string>>,
    employment: string[],
    setEmployment: React.Dispatch<React.SetStateAction<string[]>>,
    schedule: string[],
    setSchedule: React.Dispatch<React.SetStateAction<string[]>>,
}){
    const [error, setError] = useState(null)
    const [isLoaded, setIsLoaded] = useState(false)

    const onExperienceChange = (e:any) => {
        params.setExperience(e.target.value)
    }
    
    const onEmploymentChange = (e:React.ChangeEvent<HTMLInputElement>) => {
        if (params.employment.includes(e.target.value)){
            params.setEmployment(params.employment.filter(value => value != e.target.value))
        }else{
            params.setEmployment(params.employment.concat(e.target.value))
        }
    }

    const onScheduleChange = (e:React.ChangeEvent<HTMLInputElement>) => {
        if (params.schedule.includes(e.target.value)){
            params.setSchedule(params.schedule.filter(value => value != e.target.value))
        }else{
            params.setSchedule(params.schedule.concat(e.target.value))
        }
    }
    return (
        <>
            <div>
                <label>
                    Зарплата:<hr/> <input type="number" placeholder="0" onChange={e => params.setSalary(Math.max(+e.target.value, 0))}></input>₽
                </label>
            </div>
            <br/>
            <div>
                Опыт работы:
                <p><label><input type="radio" name="experienceRadio" value="noExperience" onChange={onExperienceChange}></input>Без опыта</label></p>
                <p><label><input type="radio" name="experienceRadio" value="between1And3" onChange={onExperienceChange}></input>От 1 до 3 лет</label></p>
                <p><label><input type="radio" name="experienceRadio" value="between3And6" onChange={onExperienceChange}></input>От 3 до 6 лет</label></p>
                <p><label><input type="radio" name="experienceRadio" value="moreThan6" onChange={onExperienceChange}></input>Более 6 лет</label></p>
            </div>
            <br/>
            <div>
                Тип занятости:
                <p><label><input type="checkbox" name="employmentCheckbox" value="full" onChange={onEmploymentChange}></input>Полная занятость</label></p>
                <p><label><input type="checkbox" name="employmentCheckbox" value="part" onChange={onEmploymentChange}></input>Частичная занятость</label></p>
                <p><label><input type="checkbox" name="employmentCheckbox" value="project" onChange={onEmploymentChange}></input>Проектная работа</label></p>
                <p><label><input type="checkbox" name="employmentCheckbox" value="volunteer" onChange={onEmploymentChange}></input>Волонтерство</label></p>
                <p><label><input type="checkbox" name="employmentCheckbox" value="probation" onChange={onEmploymentChange}></input>Стажировка</label></p>
            </div>
            <br/>
            <div>
                График работы:
                <p><label><input type="checkbox" name="employmentCheckbox" value="fullDay" onChange={onScheduleChange}></input>Полный день</label></p>
                <p><label><input type="checkbox" name="employmentCheckbox" value="shift" onChange={onScheduleChange}></input>Сменный график</label></p>
                <p><label><input type="checkbox" name="employmentCheckbox" value="flexible" onChange={onScheduleChange}></input>Гибкий график</label></p>
                <p><label><input type="checkbox" name="employmentCheckbox" value="remote" onChange={onScheduleChange}></input>Удаленная работа</label></p>
                <p><label><input type="checkbox" name="employmentCheckbox" value="flyInFlyOut" onChange={onScheduleChange}></input>Вахтовый метод</label></p>
            </div>
        </>
    )
}