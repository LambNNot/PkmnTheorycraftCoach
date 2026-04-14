import { Link } from "react-router-dom"

export default function NavBar() {
    return (
        <>
        <nav className="gap-4">
            <Link to="/">Home</Link>
            <Link to="/dex">Dex</Link>
            <Link to="/mySets">My Sets</Link>
        </nav>
        </>
        
    );
}