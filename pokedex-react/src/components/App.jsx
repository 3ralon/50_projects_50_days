import { usePokemons } from '../hooks/usePokemon'
import { PokemonCard } from './PokemonCard'

export const App = () => {
  const {pokemons, refreshPokemons} = usePokemons()

  const handleClick = () => {
    refreshPokemons()
  }

  return (
    <main>
      <h1>React Pokedex</h1>
      <button onClick={handleClick}>Get new pokemons</button>
      <ul>
        {
          pokemons && pokemons.length > 0 ? (
            pokemons.map(pokemon => (
              <li key={pokemon.name}>
                <PokemonCard pokemonName={pokemon.name}/>
              </li>
            ))
          ) : (
            <p>No pokemons found</p>
          )
        }  
      </ul>
          
    </main>
  )
}