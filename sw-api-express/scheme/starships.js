const z = require('zod')

const shipSchema = z.object({
    name: z.string({
        required_error: 'Name is required'
    }),
    model: z.string(),
    manufacturers: z.string(),
    cost_in_credits: z.number().positive(),
    length: z.number().positive(),
    max_atmosphering_speed: z.number().positive(),
    crew: z.string(),
    passengers: z.number().positive(),
})

function validateShip(object) {
    return shipSchema.safeParse(object)
}

function validateShipPartial(object) {
    return shipSchema.partial(object)
}

module.exports = {
    validateShip,
    validateShipPartial
}