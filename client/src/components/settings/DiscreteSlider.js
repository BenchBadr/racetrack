import * as React from 'react';
import { Slider } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useGameContext } from '../../ctx/GameContext';

const marks = [
  {
    value: 5,
    label: '5',
  },
  {
    value: 10,
    label: '10',
  },
  {
    value: 15,
    label: '15',
  },
  {
    value: 30,
    label: '30',
  },
];

const getValue = (value) => {
  const closestMark = marks.reduce((prev, curr) =>
    Math.abs(curr.value - value) < Math.abs(prev.value - value) ? curr : prev
  );
  return closestMark.value;
};

const StyledSlider = styled(Slider)(({ theme }) => ({
    '& .MuiSlider-markLabel': { 
      color: 'currentColor', 
    },
  }));
  


function DiscreteSlider() {
  const { gridDim, setGridDim } = useGameContext(); 

  const handleChange = (event, newValue) => {
    setGridDim(getValue(newValue));
  };

  return (
    <div style={{padding: '0 20px'}}>
    <a>Grid Size</a>
    <StyledSlider
      value={gridDim}
      onChange={handleChange}
      min={5}
      max={30}
      step={null} 
      marks={marks}
      valueLabelDisplay="auto"
      getAriaValueText={(gridDim) => `${gridDim}`}
    />
    </div>
  );
}

export default DiscreteSlider;