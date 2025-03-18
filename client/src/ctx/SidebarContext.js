import React, { createContext, useState, useContext } from 'react';
import {ThemeContext} from './ThemeContext';
import DiscreteSlider from '../components/settings/DiscreteSlider';
import Stats from '../components/settings/stats';

export const SidebarContext = createContext();

const SidebarProvider = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen((prevIsSidebarOpen) => !prevIsSidebarOpen);
  };

  return (
    <SidebarContext.Provider value={{ isSidebarOpen, toggleSidebar }}>
      <Sidebar/>
      {children}
    </SidebarContext.Provider>
  );
};


const Sidebar = () => {
    const { theme, toggleTheme } = useContext(ThemeContext);
    const { isSidebarOpen, toggleSidebar } = useContext(SidebarContext);
  
    return (
        <> 
        <div onClick={toggleSidebar} className={`burger ${isSidebarOpen ? 'active' : ''}`}>
        <div></div>
        <div></div>
        <div></div>
        </div>
      <aside className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <div className='sidebar-content'>
          <Stats/>
          <DiscreteSlider/>
          <hr></hr>
            <div className='bottom-box'>
            <div onClick={toggleTheme} className='theme-toggle'><a className='material-icons'>{theme!=='light' ? 'light_mode' : 'dark_mode'}</a></div>
            </div>
        </div>
      </aside>
      </>
    );
};  

export default SidebarProvider;