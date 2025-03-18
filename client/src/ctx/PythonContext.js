import React, { useState, useEffect, createContext } from 'react';
import { usePython, usePythonConsole } from 'react-py';
import { useGameContext } from './GameContext';

export const PythonContext = createContext(null);

export const PythonWrapper = ({children}) => {
  const [output, setOutput] = useState([]);
  const [outputErr, setOutputErr] = useState([]);
  const [num, setNum] = useState(0);
  const { runPython, stdout, stderr, isLoading, isRunning, isReady, scope }  = usePython();
  const { bools, setBools, setSolver } = useGameContext();


  const runPythonFunc = (code, i) => {
    setNum(i)
    runPython(code)
  }

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  

  const updateOut = () => {
    let temp = output;
    temp[num] = stdout || '';
    setOutput(temp)
    const lines = stdout.split('\n')

    for (const line of lines) {
      if (line.startsWith('bools ')) {
        // const coords = [parseInt(line.split(' ')[1]), parseInt(line.split(' ')[2])]
        // const tempBools = [...bools];
        // tempBools[coords[0]] = [...tempBools[coords[0]]];
        // tempBools[coords[0]][coords[1]] = 1;
        // setBools(tempBools);
        setBools(JSON.parse(line.split(' ').slice(1).join('')))
      }
      if (line.startsWith('end')){
        setSolver(2)
      }
    }
  }

  const updateErr = () => {
    let temp2 = outputErr;
    temp2[num] = stderr || '';
    setOutputErr(temp2)
  }


  useEffect(() => {
    updateOut()
    updateErr()
  }, [stdout, stderr])



  return (
    <PythonContext.Provider
    value={{runPythonFunc, isLoading, isRunning, isReady, num, setNum, output, outputErr, stdout, stderr}}
    >
      {children}
    </PythonContext.Provider>
  )
}
