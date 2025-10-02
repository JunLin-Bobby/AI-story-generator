import {useState, useEffect} from "react"
import {useNavigate} from "react-router-dom";
import axios from "axios";
import ThemeInput from "./ThemeInput.jsx";
import LoadingStatus from "./LoadingStatus.jsx";
import {API_BASE_URL} from "../util.js";

function StoryGenerator(){
    const navigate = useNavigate()
    const[theme, setTheme] = useState("");
    const[jobId,setJobId] = useState(null);
    const[jobStatus,setJobStatus] = useState(null);
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    //每當jobid或jobstatus改變
    //如果job狀態還在processing, 每5秒查詢一次
    useEffect(() => {
        let pollInterval;

        if (jobId && jobStatus === "processing") {
            pollInterval = setInterval(() => {
                pollJobStatus(jobId)
            }, 5000)
        }

        return () => {
            if (pollInterval) {
                clearInterval(pollInterval)
            }
        }
    }, [jobId, jobStatus])

    //發送theme到後端生成story，取得job狀態判斷請求是否成功
    const generateStory = async (theme)=>{
        setLoading(true)
        setError(null)
        setTheme(theme)

        try{
            const response = await axios.post(`${API_BASE_URL}/stories/create`,{theme});
            const {job_id,status} = response.data;
            setJobId(job_id);
            setJobStatus(status);
            console.log("generated job:",job_id,status);
            //開始查詢job狀態
            pollJobStatus(job_id)
        }catch(e){
            setLoading(false);
            setError(`Failed to generate story: ${e.message}`);
        }
    }
    //查詢job status, 如果已完成就查詢story
    const pollJobStatus = async (jobId) => {
        try{
            const response = await axios.get(`${API_BASE_URL}/jobs/${jobId}`);
            const {status,story_id,error:jobError} = response.data;
            setJobStatus(status);
            console.log("response data:", response.data);
            console.log("Polled job status:", status, story_id, jobError);

            if(status==="completed"&&story_id){
                //獲取story
                fetchStory(story_id);
            }else if(status==="failed"||jobError){
                setError(jobError || "Failed to generate story")
                setLoading(false)
            }    
        }catch(e){
            if(e.response?.status!=404){
                setError(`Failed to check story status: ${e.message}`)
                setLoading(false)
            }
        }
    }
    //根據已生成的storyid 跳轉到前端該story頁面
    const fetchStory = async (id) => {
        try{
            setLoading(false)
            setJobStatus("completed")
            navigate(`/story/${id}`);

        }catch(e){
            setError(`Failed to load story: ${e.message}`)
            setLoading(false)
        }
    }
    const reset = () => {
        setJobId(null)
        setJobStatus(null)
        setError(null)
        setTheme("")
        setLoading(false)
    }

    return (<div className="story-generator">
        
        {error && <div className="error-message">
            <p>{error}</p>
            <button onClick={reset}>Try Again</button>
        </div>}

        {!jobId && !error && !loading && <ThemeInput onSubmit={generateStory}/>}
        {loading && <LoadingStatus theme={theme} />}

    </div>)
}export default StoryGenerator;