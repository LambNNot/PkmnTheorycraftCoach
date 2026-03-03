import { useEffect, useState } from "react";
import Pokemon from "@/components/pkmn";

export default function Dex() {
  const [dex, setDex] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPKMN = async () => {
      try {
        const response = await fetch("http://localhost:3000/pkmn/");

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (Array.isArray(data)) {
          setDex(data);
        } else if (Array.isArray(data.items)) {
          setDex(data.items);
        } else {
          console.warn("Unexpected response shape:", data);
          setDex([]);
        }
      } catch (error) {
        console.error("Error fetching pkmn:", error);
        setDex([]);
      } finally {
        setLoading(false);
      }
    };

    fetchPKMN();
  }, []);

  return (
    <>
      <h1>THE DEX</h1>

      {loading ? (
        <p>Loading…</p>
      ) : dex.length === 0 ? (
        <p>No Pokémon found.</p>
      ) : (
        <div className="grid grid-cols-5 gap-4">
          {dex.map((p) => (
            <Pokemon
                key={p.dex_no}
                pokemon={p}
            />
          ))}
        </div>
      )}
    </>
  );
}
