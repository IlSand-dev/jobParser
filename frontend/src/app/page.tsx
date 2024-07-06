"use client"

import React, {useState} from "react";
import {VacanciesComponent} from "@/app/VacanciesComponent"
import {FiltersComponent} from "@/app/FiltersComponent"

export default function Home() {
  const [salary, setSalary] = useState(0)
  const [experience, setExperience] = useState("")
  const [employment, setEmployment] = useState([] as string[])
  const [schedule, setSchedule] = useState([] as string[])

  return (<>
    <main className='items-left position absolute p-24'>
      <FiltersComponent setSalary={setSalary} setExperience={setExperience} employment={employment} setEmployment={setEmployment} schedule={schedule} setSchedule={setSchedule} />
    </main>
    <main className="flex min-h-screen flex-col items-center justify-between p-24">      
      <VacanciesComponent salary={salary} experience={experience} employment={employment} schedule={schedule}/>
    </main>
    </>
  );
}
