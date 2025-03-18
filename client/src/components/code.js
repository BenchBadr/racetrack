import { ThemeContext } from '../ctx/ThemeContext';
import React, { useState, useEffect, useContext } from 'react';
import 'katex/dist/katex.min.css';
import { Highlight, themes } from "prism-react-renderer"
import { PythonContext } from '../ctx/PythonContext';
import './code.css';
import { useGameContext } from '../ctx/GameContext';


export const CodeBlock = ({ language, code, count=0 }) => {
    const { theme } = useContext(ThemeContext);
    const [isCopied, setIsCopied] = useState(false);
    const canRun = ['py', 'python'].includes(language);
    const pythonValue = useContext(PythonContext);
    const { runPythonFunc, isLoading, isRunning, isReady, output, num, setNum, outputErr, stderr, stdout, scope } = pythonValue || [null, null, null, null, null, null, null]
    const [fullscreen, setFullscreen] = useState(0);
    const [out, setOut] = useState(['', '']);
    const [codeContent, setCodeContent] = useState(code);
    const {bools, lineData, progress, gridDim} = useGameContext();

    useEffect(() => {
      if (num===count){
        setOut([stdout, stderr])
      }
    }, [num, stdout, stderr])


    useEffect(() => {
      const handleKeyDown = (e) => {
        if (e.key === 'Escape') {
          setFullscreen(0); 
        }
      };
  
      document.addEventListener('keydown', handleKeyDown);
  
      return () => {
        document.removeEventListener('keydown', handleKeyDown);
      };
    }, []);



  
    const plainCode = () => {
      const codeArray = Array.isArray(codeContent) ? codeContent : [codeContent];
      const plainCode = codeArray
        .map((item) =>
          typeof item === 'object' ? item.props.children.join('') : item
        )
        .join('');
      return plainCode;
    };
  
    const handleCopy = () => {
      navigator.clipboard.writeText(plainCode()).then(() => {
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 1500);
      });
    };
  
    const customTrim = (codeBlock) => (
      codeBlock.startsWith('> ') ? codeBlock.substring(2,codeBlock.length) : codeBlock
    )

    
    const handleRun = () => {
      let codePreset = `import time\nprogress = ${progress.toString()}`;
      codePreset += `\nbools = ${JSON.stringify(bools)}`;
      codePreset += `\ndim = ${JSON.stringify(gridDim)}`;
      codePreset += `\nline_data = ${JSON.stringify(lineData)}`;
      codePreset += `\ndef click(bools):\n  print(f"bools {bools}")\n  time.sleep(${1/(gridDim)})\n`;
      runPythonFunc(codePreset + '\n' + customTrim(plainCode()).replaceAll('\n> ','\n'), count);
      // setStartTime(Date.now());
    };


  return (
    <>
      {!code ? 
        <code className={`inline-code ${theme}`} style={{ color: 'grey' }}>{code}</code> : (
        <div className="block-code-parent">
          <div className={`copy-btn`} id='#to-hid'>
              <div>
                {!isCopied ? <div style={{userSelect:'none',cursor:'pointer',color:'grey'}} onClick={handleCopy}><a className='material-icons'>content_copy</a></div>: 
                <span className="material-icons" style={{ color: 'green' }}>done</span> }
                {canRun && !(code.includes('while 1')) && !(code.includes('while True')) ? (
                  isReady ? 
                  <div className={`run-btn ${isRunning && num===count ? 'blink' : ''}`}>
                    {!(isRunning && num===count) ? <div className='material-icons' onClick={() => handleRun()}>play_arrow</div> : ``} 
                  </div> :
                  isLoading ? <div className='spinner smaller' /> : null
                ) : null}
              </div>
          </div>
          <Highlighter codeBlock={code} language={language} lines={1} code={codeContent} setCode={setCodeContent} />
          {canRun && isReady ?
            <div className={`code-output auto-height ${fullscreen ? 'infull' : ''}`}>
              {out[0].split('\n').map((line, i) => (<>{line}<br key={i}/></>))}
              <br key='end'></br>
              <a style={{ color: 'var(--red)' }}>
              {out[1].split('\n').map((line, i) => (<>{line}<br/></>))}
              </a>
            </div>
            : null}
             {isReady && canRun ? <span className={`fullscreen-button ${fullscreen ? 'infull' : ''}`} onClick={() => setFullscreen(!fullscreen)}>
              <a className='material-icons'>{!fullscreen ? 'fullscreen' : 'fullscreen_exit'}</a>
              </span> : null}
        </div>
      )}
    </>
  );
};


const Highlighter = ({codeBlock, language='', lines=1, code, setCode}) => {
    const { theme } = useContext(ThemeContext);
    const customTrim = () => (
      code
    )

    const handleChange = (event) => {
      setCode(event.target.value);
      event.target.style.height = 'inherit'; 
    const scrollHeight = event.target.scrollHeight;
    event.target.style.height = scrollHeight + 'px';
    }
    return (
      <div className='blockCode'>
         <textarea onChange={handleChange} value={code} className='ghostarea'></textarea>
        <Highlight
          code={customTrim(code).replaceAll('\n> ','\n')}
          theme={theme==='dark' ? themes.vsDark : themes.github}
          language={language}
        >
          {({ className, style, tokens, getLineProps, getTokenProps }) => (
            <pre style={{...style, background:'transparent'}}>
              {tokens.map((line, i) => (
                <div key={i} {...getLineProps({ line })} style={{paddingLeft:'40px', overflowX:'scroll', maxWidth:'calc(100% - 60px)', whiteSpace:'normal !important'}} className={code.split('\n')[i].startsWith(`> `) ? `selectedLine` : ''}
                >
                  {lines ? <a className='line-display'
                  style={{borderTopLeftRadius:[0,'1rem'][i===0],borderBottomLeftRadius:[0,'1rem'][i==tokens.length-1]}}
                  >{i + 1}</a> : null}
                  <div>
                  {line.map((token, key) => (
                    <span key={key} {...getTokenProps({ token })}/>
                  ))}
                  </div>
                </div>
              ))}
            </pre>
          )}
        </Highlight>
      </div>
    )
  }
  

  