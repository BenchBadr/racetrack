import { useState } from "react";
import './accordion.css';
import { useGameContext } from "../../ctx/GameContext";

const Accordion = ({ children, id, title, custom=null }) => {
    const {solver, setSolver} = useGameContext();

  
    const handleCheckboxChange = () => {
      setSolver(!solver);
    };
    
    const special = ['tips','info','warn','check'];
    if (special.includes(title.toLowerCase())) {
      return (
        <div className={title.toLowerCase()}>
          {title.length ? title : ''}
        </div>
      )
    }
    return (
      <div className="accordion" style={{border:!custom ? 'current' : 'none'}}>
        <div className="tab">
          <input 
            type="checkbox" 
            name={`accordion-${id}`}
            id={`cb${id}`} 
            checked={solver} 
            onChange={handleCheckboxChange}
          />
          <label htmlFor={`cb${id}`} className="tab__label reset" style={{background:custom ? 'none' : 'current', color:custom ? custom : 'current'}}>
            {title}
            <div>
              {solver}
              <a className='material-icons'>{solver ? 'toggle_on' : 'toggle_off'}</a>
            </div>
          </label>
          <div className="tab__content">
            {children}
          </div>
        </div>
      </div>
    );
  };
  

export default Accordion;