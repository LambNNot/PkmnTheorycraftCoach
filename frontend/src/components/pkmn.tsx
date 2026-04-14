
export interface Pokemon {
  dex_no: number;
  species: string;
  typeCode: number;
  forme: string;
  ability_one_id: number;
  ability_two_id: number;
  base_hp: number;
  base_atk: number;
  base_def: number;
  base_spa: number;
  base_spd: number;
  base_spe: number;
  weight: number;
}

interface PokemonProps {
  pokemon: Pokemon;
}

export default function Pokemon({ pokemon }: PokemonProps) {
  return (
    <div className="border-solid border-2 grid grids-cols-1">
      <h2 className="font-bold justify-self-start">
        #{pokemon.dex_no} {pokemon.species}
      </h2>
      <ul className="justify-self-start">
        {pokemon.forme && <li>Forme: {pokemon.forme}</li>}
        <li><b>Type Code:</b> {pokemon.typeCode}</li>
        <li><b>Ability ID 1:</b> {pokemon.ability_one_id}</li>
        <li><b>Ability ID 2:</b> {pokemon.ability_two_id}</li>
        <li><b>Weight: </b> {pokemon.weight}</li>
      </ul>

      <h3>Base Stats</h3>
      <ul className="grid grid-cols-2 gap-2 p-4">
        <li>HP: {pokemon.base_hp}</li>
        <li>ATK: {pokemon.base_atk}</li>
        <li>DEF: {pokemon.base_def}</li>
        <li>SPA: {pokemon.base_spa}</li>
        <li>SPD: {pokemon.base_spd}</li>
        <li>SPE: {pokemon.base_spe}</li>
      </ul>
    </div>
  );
}
