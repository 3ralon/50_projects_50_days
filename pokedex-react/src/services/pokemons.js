const base_url = 'https://pokeapi.co/api/v2/pokemon/'

export const getPokemons = async () => {
  try {
    const response = await fetch(base_url)
    const json = await response.json()
  
    const pokemons = json.results
    return pokemons?.map(p => ({
      name: p.name
    }))
  } catch (error) {
    throw new Error('Error searching pokemons')
  }
}
