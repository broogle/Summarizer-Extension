import './App.css';
import BackendAPI from './components/BackendApi';
import FileSummApi from './components/FileSummApi';
import WebsiteSummApi from './components/WebsiteSummApi';
import VideoSummApi from './components/VideoSummApi';

function App() {
	return (
		<div className="App">
			<header className="App-header">
				<h1>Youtube Summarizer</h1>
				<pre><div className="line"></div></pre>
				<div className="Card"><BackendAPI /></div>
				<div className="line"></div>
				<br/>
				<h1>Website Content Summarizer</h1>
				<div className="Card"><WebsiteSummApi /></div>
				<br/>
				<h1>Text File Content Summarizer</h1>
				<div className="Card"><FileSummApi/></div>
				<br />
				<h1>Video Content Summarizer</h1>
				<div className="Card"><VideoSummApi /></div>	
			</header>
			{/* <footer className="footer">
				Made by - Legends of the waste
			</footer> */}
		</div>
	);
}

export default App;
