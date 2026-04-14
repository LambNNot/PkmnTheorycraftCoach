import { useEffect, useState } from "react";
import Pokemon from "@/components/pkmn";
import PokeSet from "@/components/pokeset"

async function hashDictionary(obj) {
  // 1. Sort keys and create a stable string representation
  const sortedStr = JSON.stringify(obj, Object.keys(obj).sort());
  
  // 2. Encode string as UTF-8
  const msgBuffer = new TextEncoder().encode(sortedStr);
  
  // 3. Hash the message using SHA-256
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  
  // 4. Convert ArrayBuffer to hex string
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}


export default function MySets() {
  const [dex, setDex] = useState([]);
  const [isLoading, setLoading] = useState(true);
  const [setName, setSetName] = useState("");
  const [speciesName, setSpeciesName] = useState("");
  const [item, setItem] = useState("");
  const [ability, setAbility] = useState("");
  const [typeOne, setTypeOne] = useState("");
  const [typeTwo, setTypeTwo] = useState("");
  const [forme, setForme] = useState("");
  const [user, setUser] = useState("");

  useEffect(() => {
    const fetchPKMN = async () => {
      console.log("Fetching...")
      try {
        const response = await fetch(
        "http://localhost:3000/pkmn/search_set?" +
            new URLSearchParams({
            ...(setName && { set_name: setName }),
            ...(speciesName && { species_name: speciesName }),
            ...(item && { item }),
            ...(ability && { ability }),
            ...(typeOne && { type_one: typeOne }),
            ...(typeTwo && { type_two: typeTwo }),
            ...(forme && { forme }),
            ...(user && { author: user }),
          })
        );

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log(data)

        setDex(data); 

      } catch (error) {
        console.error("Error fetching pkmn:", error);
        setDex([]);
      } finally {
        setLoading(false);
      }
    };

    fetchPKMN();
  }, [setName, speciesName, item, ability, typeOne, typeTwo, forme, user]);

  return (
    <>
    <h1>My Sets</h1>

    <div className="flex flex-col gap-3 mb-6">
      <input
        type="text"
        placeholder="Enter username"
        value={user}
        onChange={(e) => setUser(e.target.value)}
        className="border p-2"
      />

      <input
        type="text"
        placeholder="Set name"
        value={setName || ""}
        onChange={(e) => setSetName(e.target.value)}
        className="border p-2"
      />

      <input
        type="text"
        placeholder="Species name"
        value={speciesName || ""}
        onChange={(e) => setSpeciesName(e.target.value)}
        className="border p-2"
      />

      <input
        type="text"
        placeholder="Item"
        value={item || ""}
        onChange={(e) => setItem(e.target.value)}
        className="border p-2"
      />

      <input
        type="text"
        placeholder="Ability"
        value={ability || ""}
        onChange={(e) => setAbility(e.target.value)}
        className="border p-2"
      />

      <input
        type="text"
        placeholder="Type one"
        value={typeOne || ""}
        onChange={(e) => setTypeOne(e.target.value)}
        className="border p-2"
      />

      <input
        type="text"
        placeholder="Type two"
        value={typeTwo || ""}
        onChange={(e) => setTypeTwo(e.target.value)}
        className="border p-2"
      />

      <input
        type="text"
        placeholder="Forme"
        value={forme || ""}
        onChange={(e) => setForme(e.target.value)}
        className="border p-2"
      />
    </div>

    {isLoading ? (
      <p>Loading…</p>
    ) : dex.length === 0 ? (
      <p>No Pokémon found.</p>
    ) : (
      <div className="grid grid-cols-5 gap-4">
        {dex.map((p) => (
          <PokeSet
            key={hashDictionary(p)}
            pokeset={p}
          />
        ))}
      </div>
    )}
  </>
  );
}
