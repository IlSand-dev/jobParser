"use client"
import { useSearchParams } from 'next/navigation'
import { useState } from "react";
import { useEffect } from "react";
import {Vacancy} from "../../models/Vacancy"
import React from "react";
import VacancyComponent from './VacancyComponent';


const host = "http://0.0.0.0:8000/"

export default function VacancyPage({params}: {params: {id: number}}){
    return (
        <main className="flex min-h-screen flex-col items-center justify-between p-24">
                <VacancyComponent id={params.id}></VacancyComponent>
        </main>
    )

}