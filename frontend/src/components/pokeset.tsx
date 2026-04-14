
export interface PokeSet {
  species: string;
  forme: string;
  ability: string;
  item: string;
  tera: string;
  author: string
}

interface PokeSetProps {
  pokeset: PokeSet;
}

export default function PokeSet({ pokeset }: PokeSetProps) {
    console.log(pokeset)
    return (
        <div className="border-solid border-2 grid grids-cols-1 p-2">
        <h2 className="font-bold justify-self-start">
            {pokeset.species}{pokeset.forme && `-${pokeset.forme}`}
        </h2>
        <ul className="justify-self-start">
            <li><b>Item:</b> {pokeset.item}</li>
            <li><b>Ability:</b> {pokeset.ability}</li>
            <li><b>Author:</b> {pokeset.author}</li>
        </ul>
        </div>
    );
}
