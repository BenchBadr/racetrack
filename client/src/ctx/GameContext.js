import React, { createContext, useContext, useEffect, useState } from 'react';

const GameContext = createContext();

export const useGameContext = () => {
    return useContext(GameContext);
};

export const GameProvider = ({ children }) => {
    const [solver, setSolver] = useState(false);
    const [data, setData] = useState(null);
    const [gridDim, setGridDim] = useState(5);
    const [bools, setBools] = useState([]);
    const [mistakes, setMistakes] = useState(0);
    const [pokemon, setPokemon] = useState(null);
    const [lineData, setLineData] = useState(null);
    const [progress, setProgress] = useState(0);

    return (
        <GameContext.Provider value={{ solver, setSolver, gridDim, setGridDim, mistakes, data, setData, pokemon, setPokemon, lineData, setLineData, setBools, bools, setMistakes, setProgress, progress }}>
            {children}
        </GameContext.Provider>
    );
};