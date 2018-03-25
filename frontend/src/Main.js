import React, { Component } from 'react';
import WordCloud from 'react-d3-cloud';

const fontSizeMapper = word => Math.log2(word.value) * 14;
const rotate = word => word.value % 360;

class Main extends Component {

    constructor(props) {
        super(props);
        this.state = {
            url: null,
            loading: false,
            items: null,
            error: null
        }
    }

    load = () => {
        this.setState({loading: true});
        const { url } = this.state;
        const form = new FormData();
        form.append('url', url);
        fetch("/api/words", {method: "POST", body: form})
            .then(r => r.json())
            .then(data => this.setState({items: data.data, loading: false}))
            .catch(e => {
                this.setState({
                    loading: false,
                    error: e
                })
            })
    };

    render() {
        const { value, loading } = this.state;
        let { items } = this.state;
        if (items) {
            items = items.map(i => ({text: i[0], value: i[1]}))
        }
        return(
            <div>
                <div className="form-row align-items-center">
                    <div className="input-group">
                        <input type="text"
                               className="form-control"
                               placeholder="Enter url"
                               value={value}
                               onChange={(e) => this.setState({url: e.target.value})}/>
                        <div className="input-group-append">
                            <button className="btn btn-primary" disabled={loading} onClick={this.load}>Send</button>
                        </div>
                    </div>
                </div>
                {loading ? <p>Loading</p> : null}
                {items
                    ? <WordCloud data={items}
                                 fontSizeMapper={fontSizeMapper}
                                 rotate={rotate}/>
                    : null
                }
            </div>
        )
    }
}

export default Main;