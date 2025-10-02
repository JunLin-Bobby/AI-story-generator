import {useState,useEffect} from 'react';
import {useParams, useNavigate} from "react-router-dom"
import axios from 'axios';
import LoadingStatus from "./LoadingStatus.jsx";
import StoryGame from "./StoryGame.jsx";
import {API_BASE_URL} from "../util.js";



/**
 * StoryLoader Component
 * 
 * This component is responsible for fetching story data from the backend API.
 * While the data is being loaded (`loading` is true), it displays the LoadingStatus component.
 * If an error occurs during fetching, it displays the error message.
 * Once the story data is successfully loaded, it renders the story content.
 * 
 * State:
 * - loading: boolean indicating whether the story is being loaded
 * - error: string containing any error message from the fetch process
 * - story: the fetched story data (object or null)
 * 
 * Props:
 * (none)
 */

function StoryLoader() {
    const {id} = useParams();
    const navigate = useNavigate();
    const [story,setStory] = useState(null);
    const [error,setError] = useState(null);
    const [loading,setLoading] = useState(true);

    useEffect(() => {
        loadStory(id)
    }, [id])

    const loadStory = async (storyId) => {
        setLoading(true);
        setError(null);
        
        try{
            const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`);
            setStory(response.data);
            setLoading(false);
        }catch(err){
            if(err.response===404){
                setError("Story not found.");
            }else{
                setError("Failed to load story. Please try again later.");
            }
        }finally{
            setLoading(false);
        }
    }
    // navigate to home page
    const createNewStory = () => {
        navigate("/");
    }

    if(loading){
        return <LoadingStatus theme={story} />
    }

    if(error){
        return (
        <div className="story-loader">
            <div className="error-message">
                <h2>Story Not Found</h2>
                <p>{error}</p>
                <button onClick={createNewStory}>Go to Story Generator</button>
            </div>
        </div>
        )
    }

    if(story){
        console.log("Loaded story:",story);
        return <div className="story-loader">
            <StoryGame story={story} onNewStory ={createNewStory}/>
        </div>
    }
}

export default StoryLoader;