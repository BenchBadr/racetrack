import React, { useState, useEffect } from 'react';

async function getRandomPokemon() {
  const response = await fetch('/pokemon_data.txt'); 
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const text = await response.text();
  const lines = text.split('\n');
  return lines[Math.floor(Math.random() * lines.length)].trim();
}

async function getRandomPicture(dim) {
  const pokemon = await getRandomPokemon();
  const url = `https://raw.githubusercontent.com/rh-hideout/pokeemerald-expansion/refs/heads/master/graphics/pokemon/${pokemon}/icon.png`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
        if (response.status === 404) {
            console.error(`Pokemon ${pokemon} not found. Trying another one...`);
            return getRandomPicture(dim);
        }
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const blob = await response.blob();
    const image = await createImageBitmap(blob); 

    const canvas = document.createElement('canvas');
    canvas.width = dim;
    canvas.height = dim;
    const ctx = canvas.getContext('2d');

    ctx.imageSmoothingEnabled = false; 
    ctx.drawImage(image, 0, 0, 32, 32, 0, 0, dim, dim);

    const pixelDataHexList = [];
    for (let y = 0; y < dim; y++) {
      const rowHex = [];
      for (let x = 0; x < dim; x++) {
        const data = ctx.getImageData(x, y, 1, 1).data;
        const hexColor = `#${[...data.slice(0, 3)].map(x => x.toString(16).padStart(2, '0')).join('')}`;
        rowHex.push(hexColor);
      }
      pixelDataHexList.push(rowHex);
    }

    const transparency = pixelDataHexList[0][0];
    let nonTransparentCount = 0;
    const processedPixelData = pixelDataHexList.map(row =>
      row.map(pixel => {
        if (pixel !== transparency) {
          nonTransparentCount++; 
          return pixel;
        }
        return '#ffffff';
      })
    );


    return [processedPixelData, pokemon, nonTransparentCount];
  } catch (error) {
    console.error("Error fetching or processing image:", error);
    return [[], null, 0]; 
  }
}

export { getRandomPicture };