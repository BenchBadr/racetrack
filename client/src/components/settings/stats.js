import React, {useContext, useEffect} from 'react';
import { useGameContext } from '../../ctx/GameContext';

const Stats = () => {
    const {mistakes, progress} = useGameContext();

    return (
        <div style={{paddingTop:'150px'}}>
            <hr></hr>
            <a>Progress</a>
            <div className='stats' style={{color:progress==100 ? 'var(--green)' : 'currentColor'}}>{progress}%</div>
            <hr></hr>
            Mistakes
            <div className='stats'>{mistakes}</div>
            <hr></hr>
        </div>
    )
}

export default Stats;