class Salary{
    minimal: number
    maximum: number
    currency: string
    type: string

    constructor(minimal: number, maximum: number, currency:string, type:string){
        this.minimal = minimal
        this.maximum = maximum
        this.currency = currency
        this.type = type
    }
}