const express = require('express')
const starships = require('./route')
const app = express()

const PORT = global.process.port ?? 3000

app.use('/', starships)

app.listen(PORT, () => {
    console.log(`App listening on port http://localhost:${PORT}`)
})