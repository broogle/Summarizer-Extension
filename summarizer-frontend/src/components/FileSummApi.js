import React from 'react';
import Tabs from "./Tabs";
import ET from "../transcripts/English.txt";
import axios from 'axios';

class FileSummApi extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			name: '',
			error: null,
			isLoaded: false,
			isLoading: false,
			failedMessage: null,
            selectedFile: null
		};
	}

	handleChange = (event) => {

		// this.setState({ [event.target.name]: event.target.value });
        this.setState({ selectedFile: event.target.files[0] });
	}

    fileData = () => {
    
        if (this.state.selectedFile) {
           
          return (
            <div>
              <h2>File Details:</h2>
               
  <p>File Name: {this.state.selectedFile.name}</p>
   
               
  <p>File Type: {this.state.selectedFile.type}</p>
   
               
  <p>
                Last Modified:{" "}
                {this.state.selectedFile.lastModifiedDate.toDateString()}
              </p>
   
            </div>
          );
        } else {
          return (
            <div>
              <br />
              <h4>Choose before Pressing the Upload button</h4>
            </div>
          );
        }
      };

	handleSubmit = async (event) => {

		event.preventDefault();

		this.setState({
			isLoading: true,
			isLoaded: false
		});

		const formData = new FormData();
		formData.append(
		  "myFile",
		  this.state.selectedFile,
		  this.state.selectedFile.name
		);
		var FinalURL = `http://127.0.0.1:5000/api/uploadfile?=file_name=${this.state.selectedFile.name}`;
        const result = await axios.post(FinalURL, formData).then(response=>response).catch(err=>console.log(err));
		console.log('res',typeof result);
		console.log('finlResp',result);
		// const newStr = blkstr.join(", ");
		if (result.data.data.message === "Success") {
			this.setState({
				isLoaded: true,
				isLoading: false,
				message: result.data.data.message,
				englishTranscript: result.data.data.eng_summary,
				originalTextLength: result.data.data.original_txt_length,
				summarizedTextLength: result.data.data.final_summ_length})
		} else {
			this.setState({
				isLoaded: true,
				isLoading: false,
				failedMessage: result.data.data.error
			});
		}
		console.log('finl state',this.state);
	}

	stopAudio = () => {

		window.speechSynthesis.cancel();
	}

	textToAudio = () => {

		var synth = window.speechSynthesis;
		var utterance = new SpeechSynthesisUtterance(this.state.englishTranscript);
		synth.speak(utterance);

	}

	render() {

		const { isLoaded, isLoading, message, englishTranscript, originalTextLength, summarizedTextLength } = this.state;

		if (isLoading) {
			console.log("hello----------");
			return (
				<>
					<form onSubmit={this.handleSubmit} method='post'>
						<label>
                        File Upload:
						</label>
						<input className="input-1" type="file" value={this.state.value} placeholder="Upload your file here.." name="name" onChange={this.handleChange} required autoComplete="off" />
						<input className="submit-1" type="submit" value="Summarize" />
					</form>
                    {this.fileData()}
					<center>
						<div className="lds-ripple"><div></div><div></div></div>
					</center>
					<Tabs>
						<div label="English">
							<div className="tab-content-1">
								English Summarized Text Will be Shown Here...
							</div>
						</div>
					</Tabs>
				</>
			);
		} else if (isLoaded) {

			if (message === "Success") {
				console.log("hello?>?>?<?");

				return (
					<>
						<form onSubmit={this.handleSubmit} method='post'>
							<label>
								File Upload:
							</label>
							<input className="input-1" type="file" value={this.state.value} placeholder="Paste your Page link here." name="name" onChange={this.handleChange} required autoComplete="off" />
							<input className="submit-1" type="submit" value="Summarize" />
						</form>
                        {this.fileData()}
						<p>{originalTextLength}<i className="arrow right"></i>{summarizedTextLength}</p>
						<Tabs>
							<div label="English">
								<div className="tab-content">
									<div>
										<center>
											<button className="btn-1" type="button" onClick={this.textToAudio}>Speak</button>
											<button className="btn-1" type="button" onClick={this.stopAudio}>Stop</button>
										</center>
										<center>
										<a href={ET} className="buttonDownload" download="English_Transcript.txt" type="button">Download</a>
										</center>
									</div>
									{englishTranscript}
								</div>
							</div>
						</Tabs>
					</>
				);
			}

			else {

				return (
					<>
						<form onSubmit={this.handleSubmit} method='post'>
							<label>
                            File upload: 
							</label>
							<input className="input-1" type="file" value={this.state.value} placeholder="Paste your Page link here." name="name" onChange={this.handleChange} required autoComplete="off" />
							<input className="submit-1" type="submit" value="Summarize" />
						</form>
                        {this.fileData()}
						<div>
							<br />
							An Error occured: {this.state.failedMessage}.
						</div>
						<Tabs>
							<div label="English">
								<div className="tab-content-1">
									English Summarized Text Will be Shown Here...
								</div>
							</div>
						</Tabs>
					</>
				);
			}

		}

		else {

			return (
				<>
					<form onSubmit={this.handleSubmit} method='post'>
						<label>
                        File Upload:
						</label>
						<input className="input-1" type="file" value={this.state.value} placeholder="Paste your Page link here." name="name" onChange={this.handleChange} required autoComplete="off" />
						<input className="submit-1" type="submit" value="Summarize" />
					</form>
                    {this.fileData()}
					<p>Original Length<i className="arrow right"></i>Final Length</p>
					<Tabs>
						<div label="English">
							<div className="tab-content-1">
								English Summarized Text Will be Shown Here...
							</div>
						</div>
					</Tabs>

				</>
			);
		}

	}
}

export default FileSummApi;