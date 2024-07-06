export class Vacancy {
    id: number
    name: string
    salary: Salary
    experience: Experience
    employment: string
    schedule: string
    company: Company
    description: string
    href:string

    constructor(id: number, name: string, salary: Salary, experience: Experience, employment: string, schedule: string, company: Company, description: string, href: string) {
        this.id = id
        this.name = name
        this.salary = salary
        this.experience = experience
        this.employment = employment
        this.schedule = schedule
        this.company = company
        this.description = description
        this.href = href
    }
}