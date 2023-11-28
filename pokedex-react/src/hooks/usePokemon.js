import { useState, useEffect } from 'react'
import { getPokemons } from '../services/pokemons'

export function usePokemons() {
  const [pokemons, setPokemons] = useState()

  const refreshPokemons = () => {
    getPokemons().then(newPokemons => setPokemons(newPokemons))
  }

  useEffect(refreshPokemons, [])

  return {pokemons, refreshPokemons}
}