const express = require('express')
const router = express.Router()
const crypto = require('node:crypto')
const starshipshJSON = require('./starships.json')
const {validateShip} = require('./scheme/starships')

router.use((req, res, next) => {
    next()
})

router.get('/', (req, res) => {
    res.status(200).send('<h1>Welcome to Star Wars Starships API</h1>')
})

router.route('/starships')
    .get((req, res) => {
        res.status(200).send(starshipshJSON)
    })
    .post((req, res) => {
        const result = validateShip(req.body)

        if (result.error) {
            return res.status(401).json({error: JSON.parse(result.error.message) })
        }

        const newShip = {
            id: crypto.randomUUID(),
            created: Date.now(),
            ...result.data
        }

        starshipshJSON.push(newShip)
        return res.status(201).send(newShip)
    })

router.route('/starships/:name')
    .get((req, res) => {
        const { name } = req.params
        if (name) {
            const filteredShip = starshipshJSON.filter(
                ship => ship.name.toLowerCase().replace(' ', '') === name.toLowerCase().replace(' ', '')
            )
            return res.json(filteredShip)
        }
        res.status(404).send(`No se encontró la nave ${name}`)
    })


module.exports = router
