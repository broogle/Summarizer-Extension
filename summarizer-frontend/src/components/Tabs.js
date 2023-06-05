import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Tab from './Tab';

class Tabs extends Component {
	static propTypes = {
		children: PropTypes.instanceOf(Array).isRequired,
	}

	constructor(props) {
		super(props);

		console.log(this.props);
		let activeTab;
		if(Array.isArray(this.props.children)){
			activeTab = this.props.children[0].props.label
		}
		else{
			activeTab = this.props.children.props.label;
		}
		this.state = {
			activeTab: activeTab
		};
		console.log('*********************************', this.state);
	}

	onClickTabItem = (tab) => {
		this.setState({ activeTab: tab });
	}

	render() {
		const {onClickTabItem,props: {children},state: {activeTab}} = this;

		return (
			<div className="tabs">
				<ol className="tab-list">
					{(Array.isArray(children))
					?children.map((child) => {
						const { label } = child.props;
							return <Tab
								activeTab={activeTab}
								key={label}
								label={label}
								onClick={onClickTabItem}
							/>
					})
					:
						<Tab
								activeTab={activeTab}
								key={children.props.label}
								label={children.props.label}
								onClick={onClickTabItem}
							/>
						}
				</ol>
				<div>
					{(children.length>0)?
					children.map((child) => {
						if (child.props.label !== activeTab) return undefined;
						return child.props.children;
					})
					:
					(children.props.label !== activeTab) ? undefined:children.props.children
					}
				</div>
			</div>
		);
	}
}

export default Tabs;