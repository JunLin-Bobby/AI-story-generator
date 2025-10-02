function LoadingStatus({theme}) {
    return (<div className="loading-container">
        <h2>Generating Your {theme} Story</h2>
        // put loading animation 
        <div className="loading-animation">
            <div className="spinner"></div>
        </div>
        
        <p className="loading-info">
            Please wait while we create a unique story for you. This may take a few moments.
        </p>
    </div>)
    
}

export default LoadingStatus;