import { useState } from 'react'
/**
 * ThemeInput Component
 * 
 * This component renders a form that allows the user to input a theme for story generation.
 * It validates the input to ensure the theme is not empty, displays an error message if needed,
 * and calls the onSubmit callback with the entered theme when the form is submitted.
 * 
 * Props:
 * - onSubmit: function to handle the submitted theme value
 */
function Themeinput({onSubmit}) {
    
    const [theme,setTheme] = useState("");
    const [error,setErro] = useState("");
    
    const handleSubmit = (e) => {
        e.preventDefault();
        if(!theme.trim()){
            setError("Please enter a theme name");
            return;
        }
        onSubmit(theme);
    }

    return (
    <div className='theme-input-container '>
        <h2>Generate Your Story</h2>
        <p>Enter a theme for your story</p>
        <form onSubmit={handleSubmit}>
            <div className='input-group'>
                <input
                type="text"
                value={theme}
                onChange={(e)=>setTheme(e.target.value)}
                placeholder='e.g. Adventure, Romance, Mystery'
                className={error?'error':''}
                />
                {error && <p className='error-text'>{error}</p>}
            </div>
            <button type='submit' className='generate-btn'>Generate Story</button>
        </form>
    </div>)
}
export default ThemeInput;
