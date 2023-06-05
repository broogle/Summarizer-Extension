import React from 'react';
import Tabs from "./Tabs";
import ET from "../transcripts/English.txt";

class WebsiteSummApi extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			name: '',
			error: null,
			isLoaded: false,
			isLoading: false,
			failedMessage: null
		};
	}

	handleChange = (event) => {

		this.setState({ [event.target.name]: event.target.value });
	}

	handleSubmit = (event) => {

		this.setState({
			isLoading: true,
			isLoaded: false
		});

		var FinalURL = `http://127.0.0.1:5000/api/website/?web_url=${this.state.name}`;

		fetch(FinalURL)
			.then(res => res.json())
			.then(
				(result) => {
					if (result.data.message === "Success") {
						this.setState({
							isLoaded: true,
							isLoading: false,
							message: result.data.message,
							englishTranscript: result.data.eng_summary,
							originalTextLength: result.data.original_txt_length,
							summarizedTextLength: result.data.final_summ_length,
						});
					} else {
						this.setState({
							isLoaded: true,
							isLoading: false,
							failedMessage: result.data.error
						});
					}
				},

				(error) => {
					alert('An Error occured: ' + this.state);
					this.setState({
						isLoaded: true,
						isLoading: false,
						error: error
					});
				}
			)

		event.preventDefault();
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
					<form onSubmit={this.handleSubmit}>
						<label>
                        Website URL:
						</label>
						<input className="input-1" type="url" value={this.state.value} placeholder="Paste your page link here." name="name" onChange={this.handleChange} required autoComplete="off" />
						<input className="submit-1" type="submit" value="Summarize" />
					</form>
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
				console.log("hello");

				return (
					<>
						<form onSubmit={this.handleSubmit}>
							<label>
							Website URL:
							</label>
							<input className="input-1" type="url" value={this.state.value} placeholder="Paste your Page link here." name="name" onChange={this.handleChange} required autoComplete="off" />
							<input className="submit-1" type="submit" value="Summarize" />
						</form>
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
						<form onSubmit={this.handleSubmit}>
							<label>
                            Website URL:
							</label>
							<input className="input-1" type="url" value={this.state.value} placeholder="Paste your Page link here." name="name" onChange={this.handleChange} required autoComplete="off" />
							<input className="submit-1" type="submit" value="Summarize" />
						</form>
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
					<form onSubmit={this.handleSubmit}>
						<label>
                        Website URL:
						</label>
						<input className="input-1" type="url" value={this.state.value} placeholder="Paste your Page link here." name="name" onChange={this.handleChange} required autoComplete="off" />
						<input className="submit-1" type="submit" value="Summarize" />
					</form>
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

export default WebsiteSummApi;